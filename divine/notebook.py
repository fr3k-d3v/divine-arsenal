"""Versioned single-owner research notebook. All content stays in private storage.

SQLite migrations are additive; revision saves use optimistic concurrency. Imports
are validated entirely before a single transaction and never fetch or execute data.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from typing import Annotated, Literal
from uuid import uuid4
from pydantic import BaseModel, ConfigDict, Field, model_validator
from . import catalogue, manuscripts, store


class Strict(BaseModel):
    model_config = ConfigDict(extra='forbid')

    @model_validator(mode='before')
    @classmethod
    def valid_unicode(cls, value):
        # Keep UTF-8 JSON and XML exchange representable, including imported
        # revisions. Preserve legitimate RTL/combining text without normalization.
        def inspect(item):
            if isinstance(item, str):
                if any((ord(c) < 32 and c not in '\t\n\r') or 0xD800 <= ord(c) <= 0xDFFF
                       or ord(c) in (0xFFFE, 0xFFFF) for c in item):
                    raise ValueError('Invalid Unicode scalar or control character')
            elif isinstance(item, dict):
                for key, child in item.items():
                    inspect(key); inspect(child)
            elif isinstance(item, (list, tuple)):
                for child in item:
                    inspect(child)
        inspect(value)
        return value


class Coordinates(Strict):
    source_id: str = Field(min_length=2, max_length=80)
    edition: str = Field(min_length=1, max_length=200)
    page: str = Field(min_length=1, max_length=200)
    canvas: str | None = Field(default=None, max_length=2000)
    line: str | None = Field(default=None, max_length=80)
    region: tuple[int, int, int, int] | None = None

    @model_validator(mode='after')
    def valid(self):
        if self.source_id not in {s.id for s in catalogue.catalogue().sources}:
            raise ValueError('Choose a registered source ID')
        if self.canvas:
            catalogue.public_url(self.canvas)
        if self.region and (any(type(n) is not int for n in self.region)
                            or min(self.region[:2]) < 0 or min(self.region[2:]) <= 0
                            or max(self.region) > 100000):
            raise ValueError('Region is bounded pixel x,y,width,height')
        return self


class Transcription(Strict):
    kind: Literal['transcription']
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(max_length=100000)
    coordinates: Coordinates
    direction: Literal['auto', 'rtl', 'ltr'] = 'auto'
    language: str = Field(default='und', pattern=r'^[a-zA-Z0-9-]{2,35}$')
    state: Literal['machine draft', 'human corrected', 'reviewed'] = 'human corrected'
    attribution: str = Field(min_length=1, max_length=200)
    rights: str = Field(min_length=1, max_length=1000)
    editorial_note: str = Field(default='', max_length=5000)
    engine: str | None = Field(default=None, max_length=200)
    confidence: float | None = Field(default=None, ge=0, le=1)

    @model_validator(mode='after')
    def draft_metadata(self):
        if self.state == 'machine draft' and not self.engine:
            raise ValueError('Machine drafts require an engine/version attribution')
        return self


class Journal(Strict):
    kind: Literal['journal']
    title: str = Field(min_length=1, max_length=200)
    text: str = Field(max_length=100000)


class Relationship(Strict):
    kind: Literal['relationship']
    title: str = Field(min_length=1, max_length=200)
    subject: str = Field(max_length=80)
    object: str = Field(max_length=80)
    predicate: Literal['cites', 'translated-from', 'copied-from', 'influenced-by',
                       'resembles', 'disputes', 'interpreted-as']
    evidence: catalogue.Evidence
    citation: Coordinates
    attribution: str = Field(min_length=1, max_length=200)
    date_range: str = Field(min_length=1, max_length=100)
    note: str = Field(min_length=1, max_length=5000)

    @model_validator(mode='after')
    def known_nodes(self):
        ids = {s.id for s in catalogue.catalogue().sources}
        if self.subject not in ids or self.object not in ids or self.subject == self.object:
            raise ValueError('Relationship endpoints must be distinct registered sources')
        if self.predicate == 'resembles' and self.evidence == 'VERIFIED FACT':
            raise ValueError('Resemblance cannot establish verified historical influence')
        return self


class Manifest(Strict):
    kind: Literal['manifest']
    title: str = Field(min_length=1, max_length=200)
    manifest: dict

    @model_validator(mode='after')
    def supported(self):
        try:
            manuscripts.parse_manifest(self.manifest)
        except (KeyError, TypeError, AttributeError, IndexError) as exc:
            raise ValueError('Invalid IIIF structure') from exc
        return self


Document = Annotated[Transcription | Journal | Relationship | Manifest, Field(discriminator='kind')]


class Save(Strict):
    expected_revision: int = Field(ge=0)
    document: Document


class ImportItem(Strict):
    # IDs and timestamps are intentionally not accepted from an import.
    revisions: list[Document] = Field(min_length=1, max_length=100)

    @model_validator(mode='after')
    def stable_kind(self):
        if len({d.kind for d in self.revisions}) != 1:
            raise ValueError('Revision kinds must agree')
        return self


class Bundle(Strict):
    format: Literal['divine-private-notebook']
    version: Literal[1]
    items: list[ImportItem] = Field(max_length=100)


class Conflict(Exception):
    pass


def _migrate(db):
    db.execute('''CREATE TABLE IF NOT EXISTS notebook_migrations
                  (version INTEGER PRIMARY KEY)''')
    db.execute('''CREATE TABLE IF NOT EXISTS notebook_revisions
                  (id TEXT NOT NULL, revision INTEGER NOT NULL, kind TEXT NOT NULL,
                   payload TEXT NOT NULL, saved_at TEXT NOT NULL,
                   PRIMARY KEY(id, revision))''')
    db.execute('INSERT OR IGNORE INTO notebook_migrations VALUES(1)')
    db.commit()



def _check_capacity(db):
    # Keep exported UTF-8 bundles within the same 1 MiB API import boundary.
    rows = db.execute('SELECT id,payload FROM notebook_revisions ORDER BY id,revision').fetchall()
    groups = {}
    for row in rows:
        groups.setdefault(row['id'], []).append(json.loads(row['payload']))
    raw = {'format': 'divine-private-notebook', 'version': 1,
           'items': [{'revisions': r} for r in groups.values()]}
    if len(json.dumps(raw, ensure_ascii=False).encode('utf-8')) > 900000:
        raise ValueError('Notebook backup limit (900000 UTF-8 bytes) reached; export and delete documents first')

def save(data: Save, item_id: str | None = None) -> dict:
    item_id = store.safe_profile_id(item_id) if item_id else str(uuid4())
    with store._connect() as db:
        _migrate(db)
        db.execute('BEGIN IMMEDIATE')
        latest = db.execute('SELECT revision,kind FROM notebook_revisions WHERE id=? ORDER BY revision DESC LIMIT 1', (item_id,)).fetchone()
        current = latest['revision'] if latest else 0
        if current != data.expected_revision or (latest and latest['kind'] != data.document.kind):
            raise Conflict('Document changed; reload before saving. No revision was overwritten.')
        if current >= 100 or (not latest and db.execute('SELECT COUNT(DISTINCT id) FROM notebook_revisions').fetchone()[0] >= 100):
            raise ValueError('Notebook limit: 100 documents and 100 revisions each; export and delete old documents first')
        revision = current + 1
        db.execute('INSERT INTO notebook_revisions VALUES(?,?,?,?,?)',
                   (item_id, revision, data.document.kind, data.document.model_dump_json(),
                    datetime.now(timezone.utc).isoformat()))
        _check_capacity(db)
    return get(item_id)


def get(item_id: str) -> dict | None:
    store.safe_profile_id(item_id)
    with store._connect() as db:
        _migrate(db)
        rows = db.execute('SELECT * FROM notebook_revisions WHERE id=? ORDER BY revision', (item_id,)).fetchall()
    if not rows:
        return None
    return {'id': item_id, 'revision': rows[-1]['revision'],
            'document': json.loads(rows[-1]['payload']),
            'history': [{'revision': r['revision'], 'saved_at': r['saved_at'],
                         'document': json.loads(r['payload'])} for r in rows]}


def listing(kind: str = '') -> list[dict]:
    with store._connect() as db:
        _migrate(db)
        rows = db.execute('''SELECT r.* FROM notebook_revisions r JOIN
            (SELECT id, MAX(revision) AS revision FROM notebook_revisions GROUP BY id) m
            ON r.id=m.id AND r.revision=m.revision ORDER BY r.saved_at DESC''').fetchall()
    return [{'id': r['id'], 'revision': r['revision'], 'kind': r['kind'],
             'title': json.loads(r['payload'])['title']} for r in rows if not kind or kind == r['kind']]


def delete(item_id: str, expected_revision: int) -> bool:
    store.safe_profile_id(item_id)
    with store._connect() as db:
        _migrate(db)
        db.execute('BEGIN IMMEDIATE')
        latest = db.execute('SELECT MAX(revision) FROM notebook_revisions WHERE id=?', (item_id,)).fetchone()[0]
        if latest is None:
            return False
        if latest != expected_revision:
            raise Conflict('Document changed; reload before deletion')
        db.execute('DELETE FROM notebook_revisions WHERE id=?', (item_id,))
    return True


def export_bundle() -> Bundle:
    # One snapshot transaction, including prior revisions. Profiles are excluded.
    with store._connect() as db:
        _migrate(db)
        rows = db.execute('SELECT id,payload FROM notebook_revisions ORDER BY id,revision').fetchall()
    groups = {}
    for row in rows:
        groups.setdefault(row['id'], []).append(json.loads(row['payload']))
    return Bundle.model_validate({'format': 'divine-private-notebook', 'version': 1,
                                  'items': [{'revisions': r} for r in groups.values()]})


def import_bundle(bundle: Bundle) -> list[str]:
    # Bundle has already passed strict validation. All imported IDs are fresh;
    # import never overwrites existing records or accepts paths/authority fields.
    ids = []
    with store._connect() as db:
        _migrate(db)
        db.execute('BEGIN IMMEDIATE')
        if db.execute('SELECT COUNT(DISTINCT id) FROM notebook_revisions').fetchone()[0] + len(bundle.items) > 100:
            raise ValueError('Import exceeds 100-document notebook limit')
        for item in bundle.items:
            item_id = str(uuid4()); ids.append(item_id)
            for revision, document in enumerate(item.revisions, 1):
                db.execute('INSERT INTO notebook_revisions VALUES(?,?,?,?,?)',
                           (item_id, revision, document.kind, document.model_dump_json(),
                            datetime.now(timezone.utc).isoformat()))
        _check_capacity(db)
    return ids


def graph(q: str = '', evidence: str = '') -> dict:
    sources = catalogue.catalogue().sources
    nodes = [{'id': s.id, 'title': s.title, 'type': s.medium,
              'tradition': s.tradition, 'evidence': s.evidence} for s in sources]
    edges = []
    for row in listing('relationship'):
        record = get(row['id'])
        if not record:
            continue
        d = record['document']
        edges.append({'id': row['id'], 'revision': record['revision'], **d})
    edges = [e for e in edges if (not evidence or e['evidence'] == evidence)
             and (not q or q.casefold() in json.dumps(e, ensure_ascii=False).casefold())]
    return {'nodes': nodes, 'edges': edges, 'notice': 'Private, attributed research claims. No influence inferred from shared names, motifs or catalogue tags.'}
