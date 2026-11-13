# Research Edition 1.1 — private scholarly workflows

Observed starting HEAD: `2c6a482`, clean feature branch, three local commits ahead.
Baseline reproduced: 76 tests pass. DNS probes via socket.getaddrinfo failed for
www.loc.gov, iiif.io and www.bl.uk with `[Errno -3] Temporary failure in name
resolution`. No firewall bypass, paid API, external account or remote write.

Implemented:

- Strict private notebook document models for transcriptions, journals, attributed
  relationships and saved IIIF manifests. Additive SQLite migration 1 preserves
  profiles. Optimistic revisions, append-only correction history, conflict-aware
  deletion and copying an earlier revision into the editor. No automatic review,
  publication, OCR/HTR or model invocation.
- Transcriptions preserve exact Unicode and explicitly record registered source,
  edition, page/folio, line, canvas and pixel region, attribution, editorial state,
  rights, language/direction, optional machine engine and confidence. Unclear
  readings are authored by the researcher, never filled automatically.
- Tradition Graph has the 27 source nodes and private, cited relationship edges;
  inspectable attribution, interval, evidence, citation, filters and revisions.
  It starts empty of historical edges; no relationship was invented for a demo.
- Saved IIIF manifests with stable local canvas URLs, previous/next navigation,
  explicit image actions, multilingual/context-array parsing and bounded image
  region request construction for advertised ImageService3 services.
- Private JSON backup/import includes revision content, excludes profiles and
  assigns fresh IDs. Unknown versions/fields, authority/path injection and mixed
  revision kinds fail closed. Limits: 100 documents, 100 revisions each, 900000
  UTF-8 backup bytes, preserving the 1 MiB import boundary. Over-limit writes and
  imports roll back. Imported history timestamps are local import times; no
  external authorship or original timestamp certification is implied.
- Narrow TEI exchange profile exports/reimports exact transcription metadata and
  body. Rejects DTDs, entities, processing instructions and inconsistent/unknown
  structures. This is **not general TEI import or TEI P5 schema validation**.
- Local-only mode defaults on: geocoding blocked, image controls disabled; no
  provider, telemetry, scheduler, global configuration or model agent launched.
- Six independent approximate solar reference vectors from installed Astral 3.2
  compared against Astronomy Engine, 2000–2030 sample dates. Maximum observed
  difference about 0.00454 degrees; acceptance bound 0.03 degrees is not a certified
  accuracy or uncertainty claim. Moon/planet precision validation remains open.

Verification at this milestone: 101 pytest tests pass, one existing dependency
warning; compileall, 142-ID JS syntax check, 40-package dependency compatibility,
source/wheel build, extracted-wheel and actual installed-wheel smoke pass.
Chromium 155 desktop/mobile: 34 assertions, zero JS exceptions or external requests.
Native keyboard navigation/activation, RTL editor, inert markup, journal history,
source coordinate preservation, graph evidence/citations and manifest reload tested.
Initial browser keyboard simulation was incomplete; corrected native Enter text
and reran all assertions. Synthetic records cleaned on success and failure.
Automated checks do not establish full WCAG, screen-reader or human acceptance.

Remaining gates and owners are recorded in KNOWN_GAPS and ACCEPTANCE_MATRIX.
No institutional source, historical text, rights clearance or real usage is
verified by the synthetic workflows. No push, merge or deployment performed.
