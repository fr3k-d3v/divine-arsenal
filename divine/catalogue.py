"""Public bibliographic metadata, independent of private profiles."""
from __future__ import annotations

from functools import lru_cache
from importlib.resources import files
from typing import Literal
from urllib.parse import urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator

Evidence = Literal['VERIFIED FACT', 'OBSERVATION', 'HISTORICAL CLAIM',
                   'TRADITIONAL INTERPRETATION', 'RECONSTRUCTION', 'HYPOTHESIS',
                   'UNKNOWN', 'BLOCKED', 'CONTRADICTED']


def public_url(value: str) -> str:
    parsed = urlsplit(value)
    if (parsed.scheme != 'https' or not parsed.hostname or parsed.username
            or parsed.password or parsed.port not in (None, 443)):
        raise ValueError('An absolute HTTPS URL without credentials is required')
    return value


class Rights(BaseModel):
    model_config = ConfigDict(extra='forbid')
    metadata: str = 'Project-authored bibliographic summary; MIT'
    text: str = 'UNKNOWN — no text bundled'
    images: str = 'UNKNOWN — no images bundled'


class Source(BaseModel):
    model_config = ConfigDict(extra='forbid')
    id: str = Field(pattern=r'^[a-z0-9][a-z0-9-]{1,79}$')
    title: str = Field(min_length=1, max_length=300)
    author: str | None = Field(default=None, max_length=200)
    edition: str | None = Field(default=None, max_length=200)
    date: str | None = Field(default=None, max_length=80)
    publisher: str | None = Field(default=None, max_length=200)
    language: str | None = Field(default=None, max_length=80)
    institution: str | None = Field(default=None, max_length=200)
    shelfmark: str | None = Field(default=None, max_length=80)
    tradition: str = Field(max_length=100)
    medium: Literal['work', 'edition', 'manuscript', 'unresolved']
    evidence: Evidence
    identification: Literal['confirmed', 'probable', 'unresolved']
    source_url: str | None = None
    accessed: str | None = None
    provenance: str
    notes: str
    rights: Rights = Field(default_factory=Rights)

    @field_validator('source_url')
    @classmethod
    def safe_link(cls, value):
        return public_url(value) if value else value

    @model_validator(mode='after')
    def evidence_required(self):
        if self.evidence == 'VERIFIED FACT' and (not self.source_url or not self.accessed):
            raise ValueError('Verified records require inspected source and access date')
        return self


class Catalogue(BaseModel):
    model_config = ConfigDict(extra='forbid')
    version: Literal[1]
    sources: list[Source] = Field(max_length=500)

    @model_validator(mode='after')
    def unique_identifiers(self):
        for key in ('id', 'shelfmark', 'source_url'):
            values = [getattr(s, key) for s in self.sources if getattr(s, key)]
            if len(values) != len(set(values)):
                raise ValueError(f'Duplicate {key}')
        return self


@lru_cache(maxsize=1)
def catalogue() -> Catalogue:
    return Catalogue.model_validate_json(files('divine').joinpath('data/catalogue.json').read_text())


def search_sources(q: str = '', tradition: str = '', evidence: str = '',
                   medium: str = '', language: str = '', date: str = '') -> list[dict]:
    query = q.casefold().strip()
    rows = []
    for source in catalogue().sources:
        data = source.model_dump()
        if any(value and value.casefold() not in str(data[key] or '').casefold()
               for key, value in [('tradition', tradition), ('evidence', evidence),
                                  ('medium', medium), ('language', language), ('date', date)]):
            continue
        exact = ' '.join(str(data[k] or '') for k in ('title', 'author', 'shelfmark')).casefold()
        if query and query not in (exact + ' ' + source.notes.casefold()):
            continue
        rows.append((0 if query and query in exact else 1, source.id, data))
    return [r[2] for r in sorted(rows)]


def schema() -> dict:
    return Catalogue.model_json_schema()
