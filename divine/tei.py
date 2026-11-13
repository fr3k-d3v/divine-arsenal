"""Narrow project TEI exchange profile; not general TEI P5 schema validation.

Only our exact generated structure round-trips. No DTDs, external entities,
XInclude, stylesheets, HTML rendering, file paths or network retrieval.
"""
import json
from xml.etree import ElementTree as ET
from .notebook import Transcription

NS = 'http://www.tei-c.org/ns/1.0'
ET.register_namespace('', NS)


def encode(document: Transcription) -> str:
    def sub(parent, tag, text=None, **attrs):
        child = ET.SubElement(parent, '{'+NS+'}'+tag, attrs)
        child.text = text
        return child
    root = ET.Element('{'+NS+'}TEI')
    header = sub(root, 'teiHeader')
    desc = sub(header, 'fileDesc')
    title = sub(desc, 'titleStmt')
    sub(title, 'title', document.title)
    sub(title, 'respStmt')
    title[-1].append(ET.Element('{'+NS+'}resp'))
    title[-1][-1].text = 'Transcription attribution'
    sub(title[-1], 'name', document.attribution)
    publication = sub(desc, 'publicationStmt')
    sub(publication, 'p', 'Private local transcription. No publication or independent certification.')
    availability = sub(publication, 'availability')
    sub(availability, 'p', document.rights)
    source = sub(desc, 'sourceDesc')
    sub(source, 'p', json.dumps(document.coordinates.model_dump(), ensure_ascii=False, sort_keys=True))
    encoding = sub(header, 'encodingDesc')
    sub(encoding, 'p', 'Divine Arsenal private exchange profile v1; RECONSTRUCTION. Not TEI schema-certified.')
    # Exact validated model retained for lossless coordinates and editorial metadata.
    notes = sub(desc, 'notesStmt')
    sub(notes, 'note', document.model_dump_json(), type='divine-exchange-v1')
    desc.remove(notes)
    desc.insert(2, notes)
    text = sub(root, 'text', **{'{http://www.w3.org/XML/1998/namespace}lang': document.language})
    body = sub(text, 'body')
    sub(body, 'ab', document.text)
    return ET.tostring(root, encoding='unicode', xml_declaration=True)


def decode(xml: str) -> Transcription:
    if len(xml.encode('utf-8')) > 1_048_576 or '<!' in xml or '<?' in xml.removeprefix("<?xml version='1.0' encoding='utf-8'?>"):
        raise ValueError('Bounded plain XML required; declarations, entities and processing instructions forbidden')
    try:
        root = ET.fromstring(xml)
        note = root.find('.//{'+NS+'}note[@type="divine-exchange-v1"]')
        if note is None:
            raise ValueError('Unsupported TEI exchange profile')
        document = Transcription.model_validate_json(note.text or '')
        # Reject unknown elements/attributes and inconsistent body/header metadata.
        if ET.tostring(root) != ET.tostring(ET.fromstring(encode(document))):
            raise ValueError('Unsupported or inconsistent TEI exchange structure')
        return document
    except (ET.ParseError, TypeError) as exc:
        raise ValueError('Malformed TEI XML') from exc
