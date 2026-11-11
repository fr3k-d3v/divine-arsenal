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
