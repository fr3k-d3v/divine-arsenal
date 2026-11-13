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
