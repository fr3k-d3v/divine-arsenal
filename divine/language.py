"""Bounded symbolic calculations; never an authority or prediction source."""
from __future__ import annotations
import unicodedata

LETTERS = 'אבגדהוזחטיכלמנסעפצקרשת'
VALUES = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300, 400)
FINALS = dict(zip('ךםןףץ', 'כמנפצ'))
SCHEMES = {
    'hebrew-standard-v1': dict(zip(LETTERS, VALUES)),
    'hebrew-ordinal-v1': dict(zip(LETTERS, range(1, 23))),
}


def calculate(text: str, scheme: str) -> dict:
    if scheme not in SCHEMES:
        raise ValueError('Choose an explicit supported scheme')
    if not text or len(text) > 2000:
        raise ValueError('Input must contain 1–2000 code points')
    trace = []
    letters = 0
    for position, char in enumerate(text):
        base = FINALS.get(char, char)
        if base in SCHEMES[scheme]:
            value = SCHEMES[scheme][base]
            action = 'final mapped to base letter' if char in FINALS else 'letter value'
            letters += 1
        elif ('\u0591' <= char <= '\u05c7' and unicodedata.category(char) == 'Mn'):
            value, action = 0, 'Hebrew combining mark; retained, not counted'
        elif char in (' ', '\n', '\t', '\u05be', '\u05c0', '\u05c3', '\u05f3', '\u05f4'):
            value, action = 0, 'separator; retained, not counted'
        else:
            raise ValueError(f'Unsupported code point U+{ord(char):04X} at position {position}')
        trace.append({'position': position, 'character': char, 'code_point': f'U+{ord(char):04X}',
                      'base': base, 'value': value, 'action': action})
    if not letters:
        raise ValueError('At least one Hebrew letter is required')
    return {'label': 'SYMBOLIC', 'evidence': 'RECONSTRUCTION', 'scheme': scheme,
            'input': text, 'normalization': 'none; original code points retained',
            'direction': 'rtl', 'total': sum(t['value'] for t in trace), 'trace': trace,
            'rules': '22 Hebrew base letters; finals use base values; marks and listed separators count zero. Standard: 1–9, 10–90, 100–400. Ordinal: 1–22.',
            'source': 'https://www.chabad.org/library/article_cdo/aid/5541252/jewish/What-Is-Gematria.htm',
            'source_status': 'General tradition reference from supplied corpus; exact software table is an explicit project reconstruction, not a transcribed historical edition.',
            'authority': 'NONE'}


def transform(text: str, algorithm: str, offset: int = 0) -> dict:
    """Explicit Hebrew letter-cluster operations, with original code-point spans.

    Input uses the same allowed alphabet/marks/separators as calculate. Combining
    marks travel with their preceding letter; unanchored marks are rejected.
    Word extraction treats the supported separators as boundaries. No meaning,
    historical attestation, hidden message, pronunciation or authority inferred.
    """
    calculate(text, 'hebrew-standard-v1')  # Shared bounded Unicode vocabulary.
    if algorithm not in ('first-letter-v1', 'last-letter-v1', 'middle-left-v1',
                         'reverse-letters-v1', 'rotate-letters-v1'):
        raise ValueError('Choose a versioned transformation')
    if type(offset) is not int or not -2000 <= offset <= 2000:
        raise ValueError('Offset must be an integer in −2000…2000')
    if algorithm != 'rotate-letters-v1' and offset != 0:
        raise ValueError('Offset applies only to rotate-letters-v1')
    words, current = [], []
    for position, char in enumerate(text):
        if FINALS.get(char, char) in LETTERS:
            current.append({'text': char, 'start': position, 'end': position+1})
        elif unicodedata.category(char) == 'Mn':
            if not current:
                raise ValueError('Combining mark must follow a letter in its word')
            current[-1]['text'] += char
            current[-1]['end'] = position+1
        elif current:
            words.append(current); current = []
    if current:
        words.append(current)
    if algorithm in ('first-letter-v1', 'last-letter-v1', 'middle-left-v1'):
        chosen = [w[0 if algorithm == 'first-letter-v1' else -1 if algorithm == 'last-letter-v1' else (len(w)-1)//2] for w in words]
    else:
        chosen = [cluster for word in words for cluster in word]
        if algorithm == 'reverse-letters-v1':
            chosen = list(reversed(chosen))
        else:
            shift = offset % len(chosen)
            chosen = chosen[shift:] + chosen[:shift]
    return {'label': 'SYMBOLIC', 'evidence': 'RECONSTRUCTION', 'authority': 'NONE',
            'algorithm': algorithm, 'offset': offset, 'input': text,
            'output': ''.join(c['text'] for c in chosen),
            'trace': [{'output_position': i, 'input_start': c['start'],
                       'input_end_exclusive': c['end'], 'text': c['text']}
                      for i, c in enumerate(chosen)],
            'rules': 'Logical Unicode order; letter plus following marks. Separators form words and are omitted from output. Middle chooses the earlier logical letter for even lengths. Rotation is leftward, modulo letter count. Original input and exact spans retained; no normalization.'}


def transform_grid(cells: list[list[str]], operation: str) -> dict:
    """Neutral rectangular matrix operations; no historical grid attribution."""
    if (not isinstance(cells, list) or not 1 <= len(cells) <= 49
            or not all(isinstance(row, list) and 1 <= len(row) <= 49 for row in cells)
            or len({len(row) for row in cells}) != 1):
        raise ValueError('Rectangular grid requires 1–49 rows and columns')
    if any(not isinstance(c, str) or not 1 <= len(c) <= 16
           or any(unicodedata.category(ch) in ('Cc', 'Cf', 'Cs') for ch in c)
           for row in cells for c in row):
        raise ValueError('Grid cells require 1–16 printable code points without controls')
    rows, columns = len(cells), len(cells[0])
    coordinates = [[(r, c) for c in range(columns)] for r in range(rows)]
    if operation == 'rotate-clockwise-v1':
        coordinates = [list(row) for row in zip(*coordinates[::-1])]
    elif operation == 'transpose-v1':
        coordinates = [list(row) for row in zip(*coordinates)]
    elif operation == 'reverse-rows-v1':
        coordinates.reverse()
    elif operation == 'reverse-columns-v1':
        coordinates = [list(reversed(row)) for row in coordinates]
    else:
        raise ValueError('Unknown versioned grid operation')
    return {'label': 'SYMBOLIC', 'evidence': 'RECONSTRUCTION', 'authority': 'NONE',
            'operation': operation, 'input': cells,
            'cells': [[cells[r][c] for r, c in row] for row in coordinates],
            'input_coordinates': coordinates,
            'rules': 'Zero-based row,column indexing in logical array order; no historical association inferred.'}
