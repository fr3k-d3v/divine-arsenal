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


def verse_reference(number: int, index_edition: str, text_edition: str,
                    verse_start: int, verse_end: int | None = None) -> dict:
    """Edition-aware coordinate proposal, not verification of verse existence.

    Zero may represent a superscription only if the named edition uses it. No
    verse count, chapter/verse equivalence, text rights or text body is inferred.
    """
    chapter = psalm(number, index_edition)
    if not isinstance(text_edition, str) or not text_edition.strip() or len(text_edition) > 200:
        raise ValueError('A specific text edition/provider identifier is required')
    if any(ord(c) < 32 for c in text_edition):
        raise ValueError('Edition identifier must not contain controls')
    if verse_end is None:
        verse_end = verse_start
    if any(type(n) is not int or not 0 <= n <= 999 for n in (verse_start, verse_end)) or verse_end < verse_start:
        raise ValueError('Verse coordinates require integers 0–999 in ascending order')
    return {'text_edition': text_edition, 'coordinate': {**chapter['coordinate'],
            'verse_start': verse_start, 'verse_end': verse_end},
            'work_candidates': [w['id'] for w in chapter['works']],
            'evidence': 'UNKNOWN', 'validation': 'Coordinate structure only; verse existence, superscription convention and equivalence are UNVERIFIED for this edition.',
            'text': None, 'text_status': chapter['text_status'],
            'rights': 'UNKNOWN — an edition identifier is not a redistribution licence'}
