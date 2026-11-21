"""Versioned single-owner research notebook. All content stays in private storage.

SQLite migrations are additive; revision saves use optimistic concurrency. Imports
are validated entirely before a single transaction and never fetch or execute data.
"""
from __future__ import annotations
import json
import math
import re
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


class AnalysisResourceLimits(Strict):
    memory_mb: int | None = Field(default=None, ge=1, le=8192)
    cpu_seconds: int | None = Field(default=None, ge=1, le=120)
    wall_seconds: int | None = Field(default=None, ge=1, le=180)
    output_bytes: int | None = Field(default=None, ge=1, le=4 * 1024 * 1024)
    file_bytes: int | None = Field(default=None, ge=1, le=64 * 1024 * 1024)


class AnalysisFinding(Strict):
    kind: str = Field(min_length=1, max_length=80)
    text: str = Field(min_length=1, max_length=4000)
    confidence: float = Field(ge=0, le=1)
    evidence_hashes: list[str] = Field(min_length=1, max_length=64)
    source: str | None = Field(default=None, max_length=80)
    limitations: list[str] = Field(default_factory=list, max_length=64)

    @model_validator(mode='after')
    def valid_hashes(self):
        if any(re.fullmatch(r'[0-9a-f]{64}', value) is None for value in self.evidence_hashes):
            raise ValueError('Finding evidence references must be SHA-256 hashes')
        return self


class AnalysisReconstruction(Strict):
    kind: str = Field(min_length=1, max_length=80)
    text: str = Field(min_length=1, max_length=4000)
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    evidence_hashes: list[str] = Field(min_length=1, max_length=64)

    @model_validator(mode='after')
    def valid_hashes(self):
        if any(re.fullmatch(r'[0-9a-f]{64}', value) is None for value in self.evidence_hashes):
            raise ValueError('Reconstruction evidence references must be SHA-256 hashes')
        return self


class AnalysisArtifact(Strict):
    name: str = Field(min_length=1, max_length=128, pattern=r'^[A-Za-z0-9._-]+$')
    sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    size: int = Field(ge=1, le=16 * 1024 * 1024)
    content_type: str = Field(min_length=1, max_length=128)


class AnalysisReference(Strict):
    kind: Literal['analysis-reference']
    title: str = Field(min_length=1, max_length=200)
    provider: Literal['URE'] = 'URE'
    api_version: Literal[1] = 1
    job_id: str = Field(pattern=r'^[0-9a-f]{32}$')
    input_sha256: str = Field(pattern=r'^[0-9a-f]{64}$')
    adapter: str = Field(min_length=1, max_length=160)
    profile: Literal['identify', 'elf', 'ghidra', 'jadx', 'binwalk', 'radare2', 'unblob', 'kaitai', 'pdf', 'tei', 'iiif', 'image', 'grid', 'video']
    authority: Literal['OBSERVE'] = 'OBSERVE'
    state: Literal['succeeded', 'failed', 'timed_out', 'cancelled', 'blocked']
    created_at: float | None = None
    started_at: float | None = None
    finished_at: float | None = None
    attempt_count: int = Field(default=1, ge=1, le=100)
    sandbox_profile: str = Field(default='UNKNOWN', max_length=160)
    network_policy: Literal['DENIED', 'UNKNOWN'] = 'UNKNOWN'
    filesystem_policy: Literal['ISOLATED_READ_ONLY_INPUTS', 'UNKNOWN'] = 'UNKNOWN'
    permissions: list[Literal['OBSERVE']] = Field(default_factory=lambda: ['OBSERVE'], min_length=1, max_length=1)
    resource_limits: AnalysisResourceLimits = Field(default_factory=AnalysisResourceLimits)
    exit_code: int | None = Field(default=None, ge=-255, le=255)
    timed_out: bool = False
    truncated: bool = False
    cancelled: bool = False
    reaped: bool = False
    error: str | None = Field(default=None, max_length=1000)
    evidence_hashes: list[str] = Field(min_length=1, max_length=256)
    artifacts: list[AnalysisArtifact] = Field(default_factory=list, max_length=16)
    findings: list[AnalysisFinding] = Field(default_factory=list, max_length=64)
    reconstructions: list[AnalysisReconstruction] = Field(default_factory=list, max_length=64)
    limitations: list[str] = Field(default_factory=list, max_length=64)
    provider_limitations: list[str] = Field(default_factory=list, max_length=64)
    compatibility_notes: list[str] = Field(default_factory=list, max_length=64)
    source_id: str | None = Field(default=None, min_length=2, max_length=80)
    rights_status: Literal['UNKNOWN', 'CLEARED', 'RESTRICTED'] = 'UNKNOWN'
    review_state: Literal['UNREVIEWED', 'HUMAN_REVIEWED', 'DISPUTED'] = 'UNREVIEWED'
    note: str = Field(default='', max_length=5000)

    @model_validator(mode='after')
    def valid_provenance(self):
        if self.source_id and self.source_id not in {source.id for source in catalogue.catalogue().sources}:
            raise ValueError('Choose a registered source ID or leave the source link empty')
        if self.permissions != ['OBSERVE'] or self.authority != 'OBSERVE':
            raise ValueError('Divine Arsenal notebook references are OBSERVE-only')
        for value in (self.created_at, self.started_at, self.finished_at):
            if value is not None and (isinstance(value, bool) or not math.isfinite(value)):
                raise ValueError('Analysis timestamps must be finite Unix timestamps')
        if self.started_at is not None and self.finished_at is not None and self.finished_at < self.started_at:
            raise ValueError('Analysis finish time cannot precede start time')
        if len(set(self.evidence_hashes)) != len(self.evidence_hashes) or any(
            re.fullmatch(r'[0-9a-f]{64}', value) is None for value in self.evidence_hashes
        ):
            raise ValueError('Evidence references must be unique SHA-256 hashes')
        allowed = set(self.evidence_hashes)
        if (len({item.name for item in self.artifacts}) != len(self.artifacts)
                or any(item.sha256 not in allowed for item in self.artifacts)):
            raise ValueError('Artifact manifest must be unique and evidence-backed')
        if any(not set(f.evidence_hashes).issubset(allowed) for f in self.findings):
            raise ValueError('Finding references must belong to the analysis evidence set')
        if any(not set(r.evidence_hashes).issubset(allowed) for r in self.reconstructions):
            raise ValueError('Reconstruction references must belong to the analysis evidence set')
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


Document = Annotated[Transcription | Journal | Relationship | AnalysisReference | Manifest, Field(discriminator='kind')]


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
        edges.append({'id': row['id'], 'kind': 'relationship', 'revision': record['revision'], **d})
    for row in listing('analysis-reference'):
        record = get(row['id'])
        if not record:
            continue
        d = record['document']
        analysis_node = 'analysis:' + row['id']
        nodes.append({
            'id': analysis_node, 'title': d['title'], 'type': 'analysis',
            'tradition': 'Local analysis', 'evidence': 'OBSERVATION',
            'adapter': d['adapter'], 'state': d['state'],
            'job_id': d['job_id'], 'input_sha256': d['input_sha256'],
        })
        if d.get('source_id'):
            finished = d.get('finished_at')
            date = datetime.fromtimestamp(finished, timezone.utc).date().isoformat() if finished else 'UNKNOWN'
            edges.append({
                'id': row['id'], 'kind': 'analysis-reference', 'subject': d['source_id'],
                'object': analysis_node, 'predicate': 'analyzed-by', 'evidence': 'OBSERVATION',
                'attribution': 'Local URE adapter', 'date_range': date,
                'note': 'Static tool observation; not a historical influence claim. ' + (d.get('note') or ''),
                'citation': {'source_id': d['source_id'], 'edition': 'URE analysis reference',
                             'page': d['job_id'], 'canvas': None, 'line': None, 'region': None,
                             'input_sha256': d['input_sha256'], 'evidence_hashes': d['evidence_hashes']},
            })
    edges = [e for e in edges if (not evidence or e['evidence'] == evidence)
             and (not q or q.casefold() in json.dumps(e, ensure_ascii=False).casefold())]
    return {'nodes': nodes, 'edges': edges,
            'notice': 'Historical relationships are user-attributed. REA analysis nodes and edges are local tool observations, not evidence of historical influence.'}
