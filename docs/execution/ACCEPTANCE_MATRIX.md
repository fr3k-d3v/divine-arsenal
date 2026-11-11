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
