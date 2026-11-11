# Source register

Canonical machine-readable register: `divine/data/catalogue.json` (27 records).
Schema: `divine/data/catalogue.schema.json`; API: `/api/sources/schema`.

All seed bibliographic assertions are HISTORICAL CLAIM, HYPOTHESIS or UNKNOWN
based on the supplied corpus/addendum. None is newly labelled VERIFIED FACT.
`accessed: null` means the external record was not retrieved in this session.
Do not copy the addendum's research date into a fabricated access date.

The register distinguishes works, editions, manuscripts and unresolved records.
Sloane MS 3188 and 3189 are independent IDs. The shared catalogue collection URL
is retained only for 3188; the exact 3189 record URL remains UNKNOWN. Grid/photo
identification remains HYPOTHESIS. No user images or inscription text included.

Search supports q/title/author/shelfmark/notes, evidence, tradition, medium,
language and date. Missing edition metadata remains null. Search can match a
shelfmark in another record's contrast note; inspect the actual shelfmark field.
`POST /api/sources/validate` validates metadata only, with duplicate identifier,
shelfmark and URL checks. It never persists imports or downloads source content.

Known-book coverage includes the Bible/Polyglot, distinct Biblical passages,
Lumpkin, Freke/Gandy, Agrippa's LOC 1898 object, Barrett 1801, Mathers, Armadel,
González-Wippler, Konstantinos, Huson, Mythic Tarot and Heindel. See unresolved
register for uncertain spines/headings. A source record is not text reuse rights.
