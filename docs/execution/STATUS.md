# Research Edition 1.1 — implementation status

2026-11-12 · **INCOMPLETE / NOT PRODUCTION READY**.
Branch `feat/source-atlas-psalms-visuals`; local only, unmerged and undeployed.
Starting HEAD `2c6a482`; continuation implements the private research workflows
recorded in [PHASE_11_REPORT.md](PHASE_11_REPORT.md) and [PHASE_12_REPORT.md](PHASE_12_REPORT.md).

Working local features: 27-record Source Atlas, 150-work edition-aware Psalter
index (no text bodies), named Hebrew symbolic calculations and positional transformations, neutral grids,
verse-coordinate proposals, generated SVG squares,
IIIF subset validation/navigation and saved canvas URLs, private transcription
editor with source coordinates/revisions, attributed Tradition Graph, private
journal, bounded revision-preserving JSON backup/import and narrow TEI exchange.
Local-only mode disables external geocoding and image actions by default.
Profiles and notebook content stay under ignored private/session storage.

Final implementation verification: **131 tests pass**, one existing Starlette warning;
compileall, JS syntax/155 unique IDs, dependency compatibility, source/wheel
builds, extracted-wheel and actual temporary installed-wheel HTTP smoke pass.
Chromium desktop/mobile: **41 assertions**, zero JS exceptions/external requests.
Solar validation adds six independent Astral approximate vectors; no independent
Moon/planet precision certification. See VALIDATION for commands and limits.

Still BLOCKED/UNKNOWN: fresh institutional source/rights verification (DNS errno
-3), rights-cleared Psalm text edition, verified verse correspondences, Enochian
inventory, exact Sloane 3189 item/folio and grid match; live institutional IIIF;
pinned full TEI schema; complete diagram tracing/editor, richer graph entities and broader selectors;
independent Moon/planet references; external security/CVE and manual accessibility/
real-user acceptance; remote CI and untested Python versions. Each has an owner
and next action in KNOWN_GAPS and REQUIREMENT_DISPOSITION. Do not equate the app, tests or commits with actual
users, verified institutions, agent execution or release readiness.

Workbench uses loopback 127.0.0.1:8768 with ignored private/session-1.1 storage.
Final process and health evidence will be appended after all validation. This is
an app server, not a model provider agent. No paid calls or separate agent runtime,
global config, service, scheduler, external account, remote Git or physical action.
