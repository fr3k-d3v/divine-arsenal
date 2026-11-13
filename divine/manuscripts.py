"""IIIF Presentation 3 painting-image subset. No network or file access.

A deliberately limited adapter, not a complete IIIF specification validator.
"""
from __future__ import annotations
from urllib.parse import urlsplit, unquote
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
    if not all(isinstance(k, str) and isinstance(v, list) and v and all(isinstance(t, str) for t in v) for k, v in value.items()):
        raise ValueError('Invalid IIIF language map')
    items = value.get('en') or value.get('none') or next(iter(value.values()))
    if not isinstance(items, list) or not items or not all(isinstance(v, str) for v in items):
        raise ValueError('Nonempty language-map text required')
    result = ' / '.join(items)
    if len(result) > 2000:
        raise ValueError('Label too long')
    return result


def parse_manifest(raw: dict) -> dict:
    contexts = raw.get('@context')
    if not isinstance(contexts, list):
        contexts = [contexts]
    if raw.get('type') != 'Manifest' or 'http://iiif.io/api/presentation/3/context.json' not in contexts:
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
        annotation_pages = canvas.get('items')
        if not isinstance(annotation_pages, list) or not 1 <= len(annotation_pages) <= 20:
            raise ValueError('Embedded annotation pages required')
        annotations = []
        for page in annotation_pages:
            if not isinstance(page, dict) or page.get('type') != 'AnnotationPage' or not isinstance(page.get('items'), list) or len(page['items']) > 100:
                raise ValueError('Bounded embedded AnnotationPage required')
            for annotation in page['items']:
                if not isinstance(annotation, dict):
                    raise ValueError('Annotation object required')
                if annotation.get('motivation') == 'painting':
                    annotations.append(annotation)
        if len(annotations) != 1:
            raise ValueError('This adapter supports exactly one painting per canvas')
        annotation = annotations[0]
        if annotation.get('target') != cid or annotation.get('type') != 'Annotation':
            raise ValueError('Painting annotation must target its canvas')
        body = annotation['body']
        if body.get('type') != 'Image' or body.get('format') not in ('image/jpeg', 'image/png'):
            raise ValueError('Only JPEG/PNG painting images supported')
        services = body.get('service', [])
        if isinstance(services, dict):
            services = [services]
        if not isinstance(services, list) or len(services) > 10:
            raise ValueError('Bounded image services required')
        service = None
        for candidate in services:
            if not isinstance(candidate, dict):
                raise ValueError('Image service object required')
            if candidate.get('type') == 'ImageService3':
                service = image_url(candidate['id']).rstrip('/')
                if urlsplit(service).query or urlsplit(service).fragment or any(part in ('.', '..') for part in unquote(urlsplit(service).path).split('/')):
                    raise ValueError('Unsafe image service path')
        if service and any(type(body.get(k)) is not int or not 1 <= body[k] <= 100000 for k in ('width', 'height')):
            raise ValueError('Advertised image services require bounded image pixel dimensions')
        pages.append({'id': cid, 'label': label(canvas['label']), 'width': canvas['width'],
                      'height': canvas['height'], 'image': image_url(body['id']), 'image_service': service,
                      'image_width': body.get('width'), 'image_height': body.get('height')})
    rights = raw.get('rights')
    if rights:
        public_url(rights)
    return {'id': manifest_id, 'label': label(raw['label']), 'rights': rights or 'UNKNOWN',
            'required_statement': label(raw['requiredStatement']['value']) if raw.get('requiredStatement') else None,
            'pages': pages, 'evidence': 'RECONSTRUCTION',
            'limitations': 'Supported painting-image subset only; no remote retrieval, OCR or full IIIF conformance claim. Explicit Image API 3 region requests supported when advertised.'}


def region_request(raw: dict, page: int, region: tuple[int, int, int, int], width: int) -> str:
    """Build an advertised Image API 3 request; never retrieve it server-side."""
    manifest = parse_manifest(raw)
    if type(page) is not int or not 0 <= page < len(manifest['pages']):
        raise ValueError('Page index outside manifest')
    canvas = manifest['pages'][page]
    if not canvas['image_service']:
        raise ValueError('No ImageService3 advertised by this canvas')
    if len(region) != 4 or any(type(n) is not int for n in region):
        raise ValueError('Four integer region coordinates required')
    x, y, w, h = region
    if min(x, y) < 0 or min(w, h) < 1 or x+w > canvas['image_width'] or y+h > canvas['image_height']:
        raise ValueError('Region outside canvas bounds')
    if type(width) is not int or not 1 <= width <= min(4096, w):
        raise ValueError('Output width must be 1–4096 without upscaling')
    return f"{canvas['image_service']}/{x},{y},{w},{h}/{width},/0/default.jpg"
