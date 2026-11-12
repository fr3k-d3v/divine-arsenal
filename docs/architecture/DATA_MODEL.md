# Implemented data model and limits

Source v1: stable ID; nullable author/edition/date/publisher/language/institution/
shelfmark; type, tradition, identification, evidence, source URL, access date,
provenance notes and separate metadata/text/image rights. Pydantic forbids
unknown fields, validates links and duplicates, and exports JSON Schema.
Sources are packaged public metadata. Private profiles remain a separate SQLite
store; research APIs do not read or modify profiles.

Psalter work IDs are `psalm-001` through `psalm-150`, indexed using Hebrew chapter
identity. MT and common LXX coordinate editions are index expressions, not text
translations. A coordinate maps to one or more work IDs; each MT work maps to
one or more LXX chapters. Five-book structure describes MT, not universal LXX
book boundaries. In the LXX UI, columns are labelled INDEX GROUP, not MT books.
Common mapping: 1–8 and 148–150 unchanged; MT 9+10→LXX9; MT11–113→n−1;
MT114+115→113; MT116→114+115; MT117–146→n−1; MT147→146+147.
Mapping source lead is exposed per result, but table remains RECONSTRUCTION
pending edition-specific source review. Verse/superscription equivalence and
Psalm151 are explicitly unsupported. Missing text returns null with BLOCKED.

Language traces preserve every original code point, position, value and action.
No normalization, transliteration or hidden final-letter rule. Two versioned,
explicitly reconstructed schemes are available. Unsupported code points fail
rather than disappearing. No interpretation or authority is derived from sums.

IIIF adapter supports bounded v3 manifests with one JPEG/PNG painting per canvas,
language-map labels, canvas coordinates, rights and attribution statement. This
is a supported subset validator, not full IIIF conformance or deep zoom.
Synthetic TEI fixture demonstrates facsimile/region/text/claim links; well-formed
XML and internal references are tested, but TEI schema validation/import/export
and revision workflow remain unimplemented. The sample is project-original;
no historical transcription or source-image alignment is implied.

SVG uses two groups (geometry and numbers), deterministic coordinates, visible
RECONSTRUCTION/CALCULATION labels and algorithm metadata. It has no arbitrary
SVG input, historical tracing, interactive geometry editor, or source image.


Research Edition 1.1: notebook_revisions is an additive version-1 SQLite table
in the private store, independent of profile rows. Typed transcription, journal,
relationship and manifest documents have UUIDs and optimistic integer revisions.
Prior payloads remain available until explicit all-revision deletion. Unknown
fields/kinds/versions fail closed. See PHASE_11_REPORT and PHASE_12_REPORT for
coordinates, limits and evidence. Graph edges are private researcher assertions,
not inferred historical facts. TEI is a narrow lossless project exchange profile;
full TEI schema certification remains blocked. Backup imports assign new UUIDs
and local timestamps; original event times/authorship are not certified.
