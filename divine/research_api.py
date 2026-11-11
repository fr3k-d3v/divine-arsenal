"""Local, bounded public research APIs. Imports never execute or fetch URLs."""
from __future__ import annotations
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field
from . import catalogue, psalter, language, manuscripts, diagrams

router = APIRouter(prefix='/api')


@router.get('/sources/schema')
def source_schema():
    return catalogue.schema()


@router.get('/sources')
def sources(q: str = Query('', max_length=200), tradition: str = Query('', max_length=100),
            evidence: str = Query('', max_length=50), medium: str = Query('', max_length=50),
            language: str = Query('', max_length=80), date: str = Query('', max_length=80)):
    return catalogue.search_sources(q, tradition, evidence, medium, language, date)


@router.get('/sources/{source_id}')
def source(source_id: str):
    for item in catalogue.catalogue().sources:
        if item.id == source_id:
            return item
    raise HTTPException(404, 'Source not found')


@router.post('/sources/validate')
def validate_catalogue(data: catalogue.Catalogue):
    return {'valid': True, 'count': len(data.sources), 'persisted': False}


@router.get('/psalter')
def psalm_index():
    return psalter.index()


@router.get('/psalter/{number}')
def psalm_detail(number: int, edition: str = Query('mt-index', max_length=40)):
    try:
        return psalter.psalm(number, edition)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


class Calculation(BaseModel):
    model_config = ConfigDict(extra='forbid')
    text: str = Field(min_length=1, max_length=2000)
    scheme: str = Field(min_length=1, max_length=80)


@router.post('/language/calculate')
def symbolic_calculation(data: Calculation):
    try:
        return language.calculate(data.text, data.scheme)
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.post('/manuscripts/validate')
def manifest(data: dict):
    try:
        return manuscripts.parse_manifest(data)
    except (ValueError, KeyError, TypeError, AttributeError, IndexError) as exc:
        raise HTTPException(422, 'Unsupported or invalid IIIF manifest') from exc


@router.get('/diagrams/{planet}.svg')
def diagram(planet: str, numbers: bool = True):
    try:
        svg = diagrams.square_svg(planet, numbers)
    except ValueError as exc:
        raise HTTPException(404, str(exc)) from exc
    return Response(svg, media_type='image/svg+xml', headers={
        'Content-Disposition': 'inline; filename="reconstruction.svg"',
        'Content-Security-Policy': "default-src 'none'; style-src 'unsafe-inline'; sandbox"})


@router.get('/provenance/example')
def provenance_example():
    import json
    from importlib.resources import files
    return json.loads(files('divine').joinpath('data/provenance-example.json').read_text())
