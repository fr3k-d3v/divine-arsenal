# Acceptance matrix — experimental research slices

| Capability | Implemented evidence | Status / remaining gate |
|---|---|---|
| Phase 0 baseline | fresh 32 tests; architecture/risks inventory | PASS for local baseline; remote PR/CI BLOCKED |
| Source Atlas | 27 records, strict schema, search/filter API/UI, rights inspection | IN PROGRESS: fresh bibliographic verification and accepted metadata import persistence remain |
| Psalter index | all 150 API coordinates tested; five MT books; dedicated UI/deep links | PASS for index only |
| Numbering | boundary vectors, many-to-many inverse round trips | IN PROGRESS: common chapter RECONSTRUCTION; verse/edition verification pending |
| Text edition | text null, explicit blocked provider; no invented bodies | BLOCKED: inspected rights-cleared edition needed |
| Hebrew lab | two named schemes, preserved marks/finals trace, browser RTL check | IN PROGRESS: broader transformations, scholarly table and clipboard/manual review |
| Enochian | UNKNOWN source record, no fabricated glyph inventory | BLOCKED: chart/edition/source verification |
| IIIF | bounded v3 painting subset, 2-page synthetic fixture, browser page selection | IN PROGRESS: public institutional proof, deep zoom, stable reloadable manuscript state pending |
| TEI/provenance | original-fixture source→page→transcription→claim; XML/links tested, UI example | IN PROGRESS: actual source alignment, TEI schema validation, revision workflow/export/import pending |
| Diagrams | deterministic generated SVG, arithmetic, geometry and layer tests | IN PROGRESS: full editor, historical source tracing, overlays, golden image comparisons pending |
| Tradition graph | source IDs and provenance sample only | NOT STARTED: no fabricated historical relationships |
| Astronomy | original tests retained; version/frame metadata, local-clock offset fix | IN PROGRESS: independent numerical reference vectors still required |
| Accessibility | semantic labels, focus, reduced motion; browser desktop/mobile screenshots | IN PROGRESS: no full automated WCAG scan or screen-reader/manual review |
| Privacy/security | lifecycle + input/Host/origin/body/SSRF/SVG/path threat tests | IN PROGRESS: external review, race-proof filesystem operations, CVE/dedicated secret audit pending |
| Build/CI | local sdist+wheel and extracted-wheel HTTP smoke; CI extended | PASS for local build; remote CI UNKNOWN (not fetched/run here) |
| Agent | this implementation session active; config staging retained/disabled | Optional bridge NOT STARTED; no external provider task or global activation |
| Release 1.0 | partial slices only | NOT READY; no deployment, merge, actual external user verification |

## Research Edition 1.1 phase 11 reconciliation (supersedes earlier rows)

| Capability | Actual evidence | State / remaining acceptance |
|---|---|---|
| Transcription editor | private form, Unicode/direction, source/edition/page/line/canvas/region, editorial metadata; browser + API | IMPLEMENTED local workflow; real lawful manuscript/manual acceptance UNKNOWN |
| Revision history | optimistic conflict test, concurrent save winner test, immutable prior payloads, copy-old-revision UI | PASS for bounded notebook; no publication/certification |
| Private journal | local CRUD, revisions, UTF-8 backup/import, all-revision deletion, profile exclusion | PASS local synthetic lifecycle; backups remain user responsibility |
| Tradition Graph | 27 source nodes, attributed dated source-cited edges, filters, inspector/history | IMPLEMENTED graph workflow; verified historical edge corpus BLOCKED |
| IIIF | multilingual/context arrays, bounded annotations, ImageService3 region requests, saved canvas URLs/reload | PASS supported synthetic subset; live institution/full conformance BLOCKED |
| TEI exchange | strict generated project profile, metadata/body consistency, DTD/entity/PI rejection | PASS project profile only; TEI P5 schema validation BLOCKED |
| Import/export | atomic imports, fresh IDs, strict version/fields, capacity rollback, no paths/authority | PASS bounded private bundle; not public corpus publication |
| Astronomy | six independent approximate Astral solar vectors at 0.03 degree bound | PASS solar cross-check; Moon/planet precision UNKNOWN |
| Local-only | external geocoding blocked by default, image actions disabled, no provider | IMPLEMENTED default offline path; explicit link navigation remains user-controlled |
| Keyboard/RTL | actual Chromium native arrow/Enter events, editor direction, reload + mobile layouts | PASS task checks only; full WCAG/manual audit UNKNOWN |
| Build | sdist/wheel and temporary installed-wheel HTTP smoke | PASS local; remote CI UNKNOWN |
| Research Edition 1.1 release | 131 tests and 41 browser assertions do not establish scholarly clearance or human acceptance | NOT READY; see KNOWN_GAPS for owners/actions |


Phase 12 additions: five versioned positional letter operations and four rectangular
grid operations with Unicode/input-position traces; edition-specific verse-coordinate
proposals retain UNKNOWN verse existence/equivalence and null text. 131 tests pass,
41 browser assertions, 155 unique HTML IDs; all form controls have label/ARIA name
sources and three sampled palette contrasts exceed 4.5. Full WCAG remains UNKNOWN.
The complete scope mapping is in REQUIREMENT_DISPOSITION.md.

## REA acceptance — 2026-11-13

| Acceptance item | Result | Evidence |
|---|---|---|
| Divine-to-URE authenticated loopback bridge | PASS | Live URE status, adapter registry, input upload and report retrieval |
| OBSERVE-only job submission | PASS | API hardcodes OBSERVE; synthetic AUTO is rejected |
| Verified adapter filtering | PASS | Live registry filters unverified ELF metadata; unavailable Frida/PlatformIO/sigrok are not offered |
| ELF specialist adapter | PASS | Ghidra decompiled 32 functions from owned /usr/bin/true fixture |
| Android specialist adapters | PASS | JADX exported 1 DEX source preview; Kaitai parsed 1 class and 2 methods |
| Evidence integrity | PASS | SHA-256 input match, 3 evidence records per specialist run, report evidence references validated |
| Internal worker/fencing data exposure | PASS | Divine response strips worker IDs, leases, tokens and execution attempt records |
| UI and automated tests | PASS | 142 Divine tests; 172 URE tests; 169 unique UI IDs and valid JavaScript syntax |
| Large-file and scholarly OCR/HTR support | NOT ACCEPTED | Explicitly outside current 700 KB HTTP bridge and signature-classifier scope |

### Final hardening delta

The profile resolver now selects the highest live verified adapter version and includes that identity in the idempotency key. A provider adapter upgrade therefore creates a distinct job identity instead of replaying an old adapter result. Report reconstructions are rejected unless their SHA-256 and evidence references validate. Final count: 143 Divine tests, 172 URE tests and 49 real-browser assertions.
### REA provenance acceptance

| Acceptance item | Result | Evidence |
|---|---|---|
| Safe execution envelope | PASS | Sandbox profile, network/filesystem policy, OBSERVE permissions, adapter resource limits, timestamps and terminal flags are sanitized |
| Private notebook evidence reference | PASS | API route saves successful job reports as revisioned analysis-reference documents; idempotent by job ID |
| Evidence integrity in notebook | PASS | Input SHA-256, raw evidence hashes, findings and reconstruction references validated |
| Optional source association | PASS | Source ID must exist in the registered catalogue; absent source remains unlinked |
| Tradition Graph provenance | PASS | Analysis nodes and optional source-to-analysis OBSERVATION edges; no historical influence inferred |
| Human verification | PASS | UNREVIEWED default; HUMAN_REVIEWED/DISPUTED annotation is distinct from tool output |
| Browser save flow | PASS | 53-assertion Chromium run on the restarted live app: upload → identify → evidence report → private notebook save → Tradition Graph; zero JS exceptions/external requests |

### Live integrated acceptance — 2026-11-13

| Gate | Result | Evidence |
|---|---|---|
| Service lifecycle | PASS | `fr3k-ure.service` and `divine-arsenal.service` enabled/active with restart-on-failure; local-only bind |
| Authenticated URE connection | PASS | Divine `/api/rea/status` returned READY after systemd-managed restart |
| Live registry reconciliation | PASS | 17 identities; 12 verified/enabled OBSERVE adapters are offered for execution; unverified and gated identities remain excluded |
| Scholarly format adapters | PASS | Nine real Bubblewrap service round trips: PDF, TEI XML, IIIF v2/v3, PNG, JPEG, TIFF, CSV and TSV; evidence and OBSERVE authority validated |
| Live upload and analysis | PASS | Synthetic fixture SHA-256 matched; identify job succeeded; OBSERVE authority retained |
| Report evidence | PASS | 3 raw evidence records, 2 unique hashes, 1 finding; dangling references rejected by tests |
| Private notebook persistence | PASS | Save succeeded; repeated save returned the same reference; unique SHA-256 references validated |
| Tradition Graph provenance | PASS | `analysis:<document-id>` node appeared as OBSERVATION; no historical influence inferred |
| Synthetic record cleanup | PASS | Test notebook reference removed after graph verification; raw URE evidence retained privately |
| Divine test suite | PASS | 154 tests passed |
| URE test suite | PASS | 172 tests and 46 subtests passed |
| Browser acceptance | PASS | 53 assertions; desktop/mobile; zero console exceptions or external requests |
| Public production release | NOT ACCEPTED | Scholarly rights/correctness, full accessibility, external security, remote CI and OCR/HTR gates remain open |

### Scholarly adapter delta — 2026-11-14

| Gate | Result | Evidence |
|---|---|---|
| Verified sandbox registry wiring | PASS | URE registry enables scholarly adapters only when the actual Bubblewrap isolation probe passes |
| Scholarly worker environment | PASS | Only `URE_SCHOLARLY_PROFILE` and `URE_SCHOLARLY_FORMAT` were added to the strict worker environment allowlist |
| PDF lexical metadata | PASS | Live Divine → URE PDF job succeeded; 3 evidence records; lexical-only limitation preserved |
| TEI XML structure | PASS | Live job succeeded; DTD/entity rejection covered by tests |
| IIIF Presentation v2/v3 | PASS | Both live manifest jobs succeeded; no external context or resource fetch |
| PNG/JPEG/TIFF metadata | PASS | Three live image-header jobs succeeded; no pixel decoding |
| CSV/TSV structure | PASS | Both live jobs succeeded; cell values withheld; formulas not executed |
| URE regression suite | PASS | 180 unittest cases passed, including scholarly parser and real Bubblewrap service round trips |
| Divine regression suite | PASS | 155 tests passed |
| Browser regression | PASS | 53 Chromium assertions; zero console exceptions/external requests |
| Public production release | NOT ACCEPTED | Real institutional corpus, rights, scholarly correctness, full accessibility, external security and remote CI remain open |
