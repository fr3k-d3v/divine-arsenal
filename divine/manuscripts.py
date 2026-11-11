"""IIIF Presentation 3 painting-image subset. No network or file access.

A deliberately limited adapter, not a complete IIIF specification validator.
"""
from __future__ import annotations
from urllib.parse import urlsplit
from .catalogue import public_url

IMAGE_HOSTS = frozenset({'iiif.wellcomecollection.org', 'tile.loc.gov',
                         'iiif.io', 'ids.lib.harvard.edu', 'media.nga.gov'})


def image_url(value: str) -> str:
    public_url(value)
    if urlsplit(value).hostname not in IMAGE_HOSTS:
        raise ValueError('Image host is not in the institutional allowlist')
    return value


def label(value) -> str:
    if not isinstance(value, dict) or not value:
        raise ValueError('IIIF language map required')
    items = value.get('en') or value.get('none') or next(iter(value.values()))
    if not isinstance(items, list) or not items or not all(isinstance(v, str) for v in items):
        raise ValueError('Nonempty language-map text required')
    result = ' / '.join(items)
    if len(result) > 2000:
        raise ValueError('Label too long')
    return result


def parse_manifest(raw: dict) -> dict:
    if raw.get('type') != 'Manifest' or raw.get('@context') != 'http://iiif.io/api/presentation/3/context.json':
        raise ValueError('IIIF Presentation 3 Manifest required')
    manifest_id = public_url(raw['id'])
    canvases = raw.get('items')
    if not isinstance(canvases, list) or not 1 <= len(canvases) <= 500:
        raise ValueError('Manifest requires 1–500 canvases')
    pages, ids = [], set()
    for canvas in canvases:
        cid = public_url(canvas['id'])
        if cid in ids or canvas.get('type') != 'Canvas':
            raise ValueError('Canvas IDs must be unique')
        ids.add(cid)
        for size in ('width', 'height'):
            if type(canvas.get(size)) is not int or not 1 <= canvas[size] <= 100000:
                raise ValueError('Canvas dimensions must be bounded positive integers')
        annotations = [a for page in canvas['items'] if page.get('type') == 'AnnotationPage'
                       for a in page.get('items', []) if a.get('motivation') == 'painting']
        if len(annotations) != 1:
            raise ValueError('This adapter supports exactly one painting per canvas')
        annotation = annotations[0]
        if annotation.get('target') != cid or annotation.get('type') != 'Annotation':
            raise ValueError('Painting annotation must target its canvas')
        body = annotation['body']
        if body.get('type') != 'Image' or body.get('format') not in ('image/jpeg', 'image/png'):
            raise ValueError('Only JPEG/PNG painting images supported')
        pages.append({'id': cid, 'label': label(canvas['label']), 'width': canvas['width'],
                      'height': canvas['height'], 'image': image_url(body['id'])})
    rights = raw.get('rights')
    if rights:
        public_url(rights)
    return {'id': manifest_id, 'label': label(raw['label']), 'rights': rights or 'UNKNOWN',
            'required_statement': label(raw['requiredStatement']['value']) if raw.get('requiredStatement') else None,
            'pages': pages, 'evidence': 'RECONSTRUCTION',
            'limitations': 'Supported painting-image subset only; no remote retrieval, OCR, deep zoom or full IIIF conformance claim.'}
