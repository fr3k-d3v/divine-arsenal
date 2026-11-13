"""Private research notebook API. No providers, downloads, or publication."""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import Response
from . import notebook

router = APIRouter(prefix='/api/notebook')


def read(item_id):
    try:
        item = notebook.get(item_id)
    except ValueError as exc:
        raise HTTPException(422, 'Canonical UUID required') from exc
    if item is None:
        raise HTTPException(404, 'Notebook document not found')
    return item


def write(data, item_id=None):
    try:
        return notebook.save(data, item_id)
    except notebook.Conflict as exc:
        raise HTTPException(409, str(exc)) from exc
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get('')
def listing(kind: str = Query('', max_length=30)):
    return notebook.listing(kind)


@router.post('', status_code=201)
def create(data: notebook.Save):
    if data.expected_revision != 0:
        raise HTTPException(422, 'New documents start at revision zero')
    return write(data)


@router.get('/export')
def export():
    return Response(notebook.export_bundle().model_dump_json(), media_type='application/json',
                    headers={'Content-Disposition': 'attachment; filename="private-notebook.json"'})


@router.post('/import')
def import_bundle(data: notebook.Bundle):
    try:
        return {'imported_ids': notebook.import_bundle(data), 'published': False}
    except ValueError as exc:
        raise HTTPException(422, str(exc)) from exc


@router.get('/graph')
def graph(q: str = Query('', max_length=200), evidence: str = Query('', max_length=50)):
    return notebook.graph(q, evidence)


@router.get('/{item_id}')
def get(item_id: str):
    return read(item_id)


@router.put('/{item_id}')
def update(item_id: str, data: notebook.Save):
    read(item_id)
    return write(data, item_id)


@router.delete('/{item_id}')
def delete(item_id: str, expected_revision: int = Query(ge=1)):
    read(item_id)
    try:
        return {'deleted': notebook.delete(item_id, expected_revision),
                'note': 'All notebook revisions removed. Exports and filesystem backups remain separate.'}
    except notebook.Conflict as exc:
        raise HTTPException(409, str(exc)) from exc


@router.get('/{item_id}/tei')
def export_tei(item_id: str):
    from . import tei
    item = read(item_id)
    if item['document']['kind'] != 'transcription':
        raise HTTPException(422, 'TEI export requires a transcription')
    return Response(tei.encode(notebook.Transcription.model_validate(item['document'])),
                    media_type='application/tei+xml',
                    headers={'Content-Disposition': 'attachment; filename="private-transcription.tei.xml"',
                             'Content-Security-Policy': "default-src 'none'; sandbox"})
