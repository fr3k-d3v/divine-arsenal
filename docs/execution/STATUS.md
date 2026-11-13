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
Final process and health evidence appears below. This is
an app server, not a model provider agent. No paid calls or separate agent runtime,
global config, service, scheduler, external account, remote Git or physical action.

Final runtime observation: **PID 390112**, tool session **89722**, listening only
on **127.0.0.1:8768**. Nine actual HTTP endpoints returned 200 with expected data;
notebook is empty after synthetic cleanup. Final browser rerun: 41 assertions,
no JS exceptions or external requests. Implementation commit **498ca14**;
[evidence/validation-1.1.json](evidence/validation-1.1.json) records actual test,
HTTP and build results. This app process is not a model-agent runtime.

Next work, in order:

1. Source/rights reviewers: when permitted DNS works, inspect one institutional
   item/IIIF service and one lawful Psalm edition; verify exact verse coordinates,
   Sloane 3189 item/folio and Enochian chart before promoting claims or text.
2. Maintainer: finish general diagram/layer editing, local catalogue overlay,
   richer graph entities, OCR/region overlays and broader selectors as mapped in
   REQUIREMENT_DISPOSITION. These are still UNKNOWN, not complete.
3. Edition/astronomy reviewers: pin full TEI schema and obtain independent precise
   Moon/planet/observer vectors; current solar comparison is approximate only.
4. Accessibility/security/release reviewers: full manual/automated audit, clean
   install/remote CI matrix and real-user acceptance before release decisions.

A separate untracked REA directive containing a local mount path remains untouched and excluded from commits. The public 29-repository register is a static inventory derived from the preserved audit; no recovered checkout was executed, imported or vendored. No private material or recovered source was added to the public implementation. No push, merge,
deployment, global configuration, scheduler or paid/provider calls occurred.

## REA integration update — 2026-11-13

- Implemented the Divine Arsenal ↔ URE HTTP-only adapter and dedicated REA analysis workspace.
- Added authenticated loopback status/adapter discovery, bounded file intake, SHA-256 reconciliation, verified profile suggestions, OBSERVE-only job submission, polling, cancellation and evidence-linked reports.
- Added a 29-repository recovered-workspace register and integration architecture. Recovered source checkouts remain unexecuted and unvendored.
- Live same-host checks passed for identify, Ghidra ELF decompilation (32 functions), JADX DEX decompilation (1 source preview) and Kaitai DEX parsing (1 class, 2 methods).
- Divine Arsenal: 142 tests passed; JavaScript syntax valid; 169 unique HTML IDs.
- URE: 172 tests passed, including the report-limitation regression.
- The running URE API is loopback-only on Omarchy. A private mode-0600 token file is outside the repository. No cloud deployment, public release or hardware authority is claimed.

### Final REA verification delta

The final hardening pass adds version-aware adapter resolution, adapter-version-aware idempotency and strict reconstruction evidence-reference validation. Divine Arsenal's current suite is **143 tests passing** (131 baseline + 12 REA tests). The real browser smoke is **49 assertions passing**, with zero console exceptions and zero external requests. The REA UI screenshot is preserved at docs/execution/evidence/rea-analysis.png.
### REA provenance integration

- Added a structured `analysis-reference` notebook document with SHA-256 and evidence-reference validation.
- Successful reports can be explicitly saved to the private notebook; save is idempotent by URE job ID.
- Added optional user-selected registered-source links and local-analysis nodes/OBSERVATION edges in the Tradition Graph.
- Added human review state (`UNREVIEWED` by default), review notes and `UNKNOWN` rights status.
- Execution provenance now includes sandbox profile, network/filesystem policy, OBSERVE permissions, adapter resource limits, timestamps, attempt count and terminal flags. Internal worker IDs, tokens and lease/fencing data remain excluded.
- Current Divine suite: **154 passed**; JavaScript syntax valid; **188 unique HTML IDs**. After the live service restart, Chromium acceptance passed **53 assertions**, including REA save-to-notebook and Tradition Graph navigation, with zero console exceptions or external requests.

## Live end-to-end verification — 2026-11-13

- Restarted URE and Divine Arsenal under enabled user systemd units: `fr3k-ure.service` and `divine-arsenal.service`. Both units are active and enabled; both bind only to IPv4 loopback. The user manager has linger enabled.
- REA authenticated status: **READY**. The live registry reports **17 adapter identities**: 12 verified/enabled OBSERVE adapters (7 existing specialists plus 5 scholarly metadata/structure adapters), 2 enabled but unverified identities, and 3 separately gated/unavailable identities (Frida/APPROVAL, PlatformIO/PHYSICAL, sigrok/PHYSICAL). Divine only suggests verified, enabled OBSERVE profiles.
- Live API acceptance: synthetic fixture uploaded; SHA-256 reconciled; identify job reached `succeeded`; report contained 3 evidence records, 2 unique content hashes and 1 finding; notebook save succeeded; duplicate save was idempotent; `analysis:<document-id>` Tradition Graph node was verified; temporary notebook reference was deleted. The raw synthetic test evidence remains in the private URE evidence store.
- Divine Arsenal tests: **154 passed**. URE tests: **172 passed, 46 subtests passed**. Chromium: **53 assertions**, desktop/mobile viewports, 0 JavaScript exceptions, 0 external requests, 188 unique HTML IDs. `git diff --check`, Python compilation and web syntax checks passed.
- The REA secret is held only in `~/.config/fr3k/divine-arsenal.env` (mode 0600; parent directory mode 0700); no credential is stored in the repository. Reproducible systemd unit templates and installer are in `deploy/systemd/` and `scripts/install-local-services.sh`.
- This verifies the **local integrated research workbench**, not a public/production release. Institutional source/rights review, full WCAG/manual accessibility, external security review, remote CI and scholarly OCR/HTR remain open. No remote deployment or hardware/physical authority is enabled.

## Scholarly adapter expansion — 2026-11-14

- Fixed two integration defects: the URE `/v1/adapters` endpoint now receives the actual verified Bubblewrap state, and the sandbox's strict environment allowlist now admits only the two explicit scholarly worker profile variables required by the reviewed parser. Sandbox reporting now accurately identifies `bubblewrap-static-analysis-v1` rather than labelling every worker synthetic.
- Enabled five additional verified OBSERVE adapters: PDF lexical metadata, TEI XML structure, IIIF Presentation v2/v3 manifests, PNG/JPEG/TIFF header metadata and CSV/TSV structure. Unverified or separately gated adapters remain excluded.
- Live Divine → URE acceptance completed nine synthetic format paths: PDF, TEI XML, IIIF Presentation v2 and v3, PNG, JPEG, TIFF, CSV and TSV. All nine jobs succeeded, each with three evidence records, reconciled SHA-256, OBSERVE authority, denied network, isolated read-only input and reaped worker. CSV/TSV cell values were withheld; formulas were not evaluated; IIIF references were not fetched.
- Live registry: 17 identities, 12 verified/enabled. Full URE suite: **180 unittest cases passed**. Full Divine suite: **155 passed**. Chromium: **53 assertions**, desktop/mobile, zero console exceptions, zero external requests; 188 unique HTML IDs.
- Evidence: `docs/execution/evidence/scholarly-adapter-acceptance-2026-11-14.json` and `docs/research/REA_INTEGRATION_ARCHITECTURE.md` section 13.
- Remaining limits: synthetic fixtures only; no OCR/HTR, pixel decoding, PDF rendering, cell-value output, formula execution, external IIIF fetch, TEI P5 validation, full WCAG/manual review, independent security review, remote CI or public production release.
