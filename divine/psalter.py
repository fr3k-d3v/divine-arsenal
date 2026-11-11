"""Edition coordinates: chapter-level correspondences, never verse equivalence.

Mapping reference carried in supplied research addendum:
https://academic.oup.com/edited-volume/45761/chapter/398724013
Fresh source retrieval blocked. This common table requires edition review.
"""
from __future__ import annotations

BOOKS = ((1, 41), (42, 72), (73, 89), (90, 106), (107, 150))
EDITIONS = {
    'mt-index': {'id': 'mt-index', 'title': 'Hebrew/Masoretic coordinate index', 'system': 'MT',
                 'language': 'he', 'rights': 'Project-authored index; MIT', 'text_available': False},
    'lxx-index': {'id': 'lxx-index', 'title': 'Common LXX/Vulgate coordinate index', 'system': 'LXX',
                  'language': 'grc', 'rights': 'Project-authored index; MIT', 'text_available': False},
}


def mt_to_lxx(number: int) -> list[int]:
    if not 1 <= number <= 150:
        raise ValueError('Psalm chapter must be 1–150')
    if number <= 8 or number >= 148:
        return [number]
    if number in (9, 10):
        return [9]
    if number in (114, 115):
        return [113]
    if number == 116:
        return [114, 115]
    if number == 147:
        return [146, 147]
    return [number - 1]


def psalm(number: int, edition: str = 'mt-index') -> dict:
    if edition not in EDITIONS:
        raise ValueError('Unknown edition')
    if not 1 <= number <= 150:
        raise ValueError('Psalm chapter must be 1–150')
    works = [number] if EDITIONS[edition]['system'] == 'MT' else [
        n for n in range(1, 151) if number in mt_to_lxx(n)]
    return {'id': f'{edition}:{number}', 'edition': EDITIONS[edition],
            'coordinate': {'chapter': number, 'system': EDITIONS[edition]['system']},
            'works': [{'id': f'psalm-{n:03}', 'mt_chapter': n,
                       'book': next(i for i, (a, b) in enumerate(BOOKS, 1) if a <= n <= b),
                       'lxx_chapters': mt_to_lxx(n)} for n in works],
            'text': None, 'text_status': 'BLOCKED — no verified rights-cleared text provider',
            'mapping_evidence': 'RECONSTRUCTION', 'source_id': 'psalter',
            'mapping_source': 'https://academic.oup.com/edited-volume/45761/chapter/398724013',
            'limitations': 'Common chapter-level table only; split/merge passages and superscriptions require edition-specific verse alignment. LXX Psalm 151 is outside this 150-work index.'}


def index() -> dict:
    return {'editions': list(EDITIONS.values()),
            'books': [{'number': i, 'start': a, 'end': b} for i, (a, b) in enumerate(BOOKS, 1)],
            'psalms': [psalm(n) for n in range(1, 151)]}
