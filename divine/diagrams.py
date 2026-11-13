"""Deterministic project-created SVG. Arbitrary SVG imports are unsupported."""
from __future__ import annotations
import json
from xml.etree.ElementTree import Element, SubElement, tostring
from .traditions import planetary_kamea


def square_svg(planet: str, numbers: bool = True) -> str:
    data = planetary_kamea(planet)
    n = data['order']
    root = Element('svg', {'xmlns': 'http://www.w3.org/2000/svg', 'viewBox': '0 0 600 690',
                           'role': 'img', 'aria-labelledby': 'title desc'})
    SubElement(root, 'title', {'id': 'title'}).text = f"RECONSTRUCTION — {data['planet']} mathematical square"
    SubElement(root, 'desc', {'id': 'desc'}).text = 'Project-generated orientation; not a historical facsimile. SYMBOLIC associations grant no authority.'
    SubElement(root, 'metadata').text = json.dumps({
        'creator': 'Divine Arsenal', 'algorithm': 'normal-magic-square-v1',
        'source': 'divine.traditions.magic_square', 'source_type': 'software algorithm',
        'historical_source': None, 'evidence': 'RECONSTRUCTION',
        'transformations': ['generate normal square', 'map cells to 540-unit grid'],
        'numbers_visible': numbers, 'constant': data['constant']}, sort_keys=True)
    SubElement(root, 'rect', {'width': '600', 'height': '690', 'fill': '#13101e'})
    SubElement(root, 'text', {'x': '30', 'y': '30', 'fill': '#f6e8ce', 'font-size': '18'}).text = 'RECONSTRUCTION · ' + data['planet']
    grid = SubElement(root, 'g', {'id': 'geometry', 'stroke': '#e8bc6e', 'fill': 'none'})
    labels = SubElement(root, 'g', {'id': 'numbers', 'fill': '#f6e8ce', 'font-size': '20',
                                    'text-anchor': 'middle', 'dominant-baseline': 'middle'})
    step = 540 / n
    for i in range(n + 1):
        coordinate = f'{30 + i * step:.6f}'
        SubElement(grid, 'line', {'x1': coordinate, 'y1': '60', 'x2': coordinate, 'y2': '600'})
        coordinate = f'{60 + i * step:.6f}'
        SubElement(grid, 'line', {'x1': '30', 'y1': coordinate, 'x2': '570', 'y2': coordinate})
    if numbers:
        for r, row in enumerate(data['grid']):
            for c, value in enumerate(row):
                SubElement(labels, 'text', {'x': f'{30 + (c + .5)*step:.6f}',
                                           'y': f'{60 + (r + .5)*step:.6f}'}).text = str(value)
    SubElement(root, 'text', {'x': '30', 'y': '635', 'fill': '#f6e8ce', 'font-size': '16'}).text = f"CALCULATION · {n} × {n} · sum {data['constant']}"
    SubElement(root, 'text', {'x': '30', 'y': '665', 'fill': '#f6e8ce', 'font-size': '13'}).text = 'Generated geometry; historical orientations may differ. Creator: Divine Arsenal.'
    return tostring(root, encoding='unicode')
