# Research Edition 1.1 — requirement disposition

This maps remaining broad-plan requirements to tested implementation or explicit
open gates. UNKNOWN development work below remains viable; the continuation was
bounded by implementation/review resources. It is not marked impossible or done.
Owners are roles for the next pass, not assigned agents or permissions.

| Requirement | Disposition and evidence | Exact next action / owner |
|---|---|---|
| Baseline, architecture, local validation | IMPLEMENTED: baseline 76; final suite 131; docs and CI configuration inspected | Remote CI/Python matrix UNKNOWN; maintainer run when access available |
| Source records, rights, duplicates, search | IMPLEMENTED 27 supplied records/schema, distinct Sloane IDs; fresh source verification BLOCKED by DNS errno -3 | Source researcher inspect primary records and edition rights; keep grid HYPOTHESIS |
| Public metadata persistence and scholarly citation formats | UNKNOWN: validation/search only; private backup retains graph citations, no CSL/BibTeX exporter/local atlas overlay | Maintainer implement reviewed overlay, conflict UX and citation format tests |
| Psalter 150 works/book navigation/chapter conversion | IMPLEMENTED; tests cover index and split/merge reconstruction | Textual scholar review edition-specific mapping against authoritative records |
| Psalm text, parallel translations, sourced themes/cross-references | BLOCKED: no inspected rights-cleared edition or verse table; no bodies bundled | Rights/textual reviewer select and inspect lawful provider, then implement text/attribution adapters |
| Verse coordinate model | IMPLEMENTED structure, edition/provider ID and range UI/API; verse existence/equivalence UNKNOWN | Textual scholar verify actual verse/superscription alignments |
| Hebrew rules, Unicode, transformations, grids | IMPLEMENTED two schemes, five letter operations, four matrix operations, exact positional traces and RTL UI | Language reviewer verify historical attribution tables; broader arbitrary permutations/skip/word-boundary selectors UNKNOWN; maintainer extend explicit algorithms |
| Enochian inventory, words/pronunciation/translations | BLOCKED: no identified rights-cleared chart/variant | Language/source researcher verify inventory before encoding |
| IIIF page/image navigation and stable URLs | IMPLEMENTED bounded v3 subset, manifest persistence, canvas URLs, ImageService3 pixel-region requests, fixtures; live institutional proof BLOCKED DNS | Maintainer/source researcher test institutional manifest and matching image service/rights |
| Universal IIIF services/choices/collections/auth/search | UNKNOWN: unsupported structures rejected; no universal conformance claimed | Maintainer add separately bounded adapters and conformance fixtures |
| Transcription coordinates/revisions/editor | IMPLEMENTED private source/edition/page/line/canvas/region, language/direction, notes, machine metadata and conflict history | Human editor verify actual lawful manuscript alignment and correction workflow |
| OCR/HTR execution, region overlays and publication | UNKNOWN: metadata only, no recognizer/overlay/publishing; no image rights cleared | Maintainer evaluate lawful local OCR/overlay pipeline; human review before any publication |
| TEI import/export | IMPLEMENTED exact project exchange profile, malicious XML/inconsistency rejection; full P5 schema BLOCKED no pinned local schema | Edition maintainer obtain lawful pinned schema and expand sourceDoc/facsimile/alignment export |
| Symbol/diagram studio | IMPLEMENTED deterministic labelled SVG square generation and number layers; general editor, overlay, tracing, constraints, PNG/PDF/golden images UNKNOWN | Maintainer implement neutral geometry/layer editor; rights reviewer source comparison assets |
| Tradition Graph | IMPLEMENTED source nodes, private evidence-bearing relationship CRUD, filters, citations/history; historical corpus BLOCKED fresh inspection | Historian enter reviewed relationships; maintainer extend people/concept/claim node types and richer graph filtering/layout (UNKNOWN) |
| Astronomy | IMPLEMENTED existing astronomy + six independent approximate solar vectors, frame/version/precision notes | Astronomy reviewer obtain independent Moon/planet/observer vectors; precision remains UNKNOWN |
| Journal/profile privacy | IMPLEMENTED private opt-in profiles and journal lifecycle, no cloud, profile-excluding notebook backup, deletion; no encryption/auth | Security reviewer audit trusted-owner boundary, backups and filesystem races |
| Import/export/local-only | IMPLEMENTED strict bounded private models, versioned atomic fresh-ID import, rollback/capacity tests; default offline CSP/geocoding | Maintainer keep new adapters no-fetch and separately approved; forensic deletion not claimed |
| Accessibility/mobile/keyboard | IMPLEMENTED browser task checks, RTL, names, palette samples, focus/reduced motion; full audit UNKNOWN | Accessibility reviewer screen reader/manual and full rendered contrast audit |
| Command palette, richer workspace shell, voice | UNKNOWN: ordinary section navigation/private notebook; no palette/voice feature implemented | Maintainer assess command palette/workspace UX; voice must be explicit opt-in |
| Optional agent bridge/runtime | BLOCKED: no provider/task contract, no model runtime started; staged adapters remain disabled | User/maintainer specify bounded task and permitted provider before bridge execution; symbolism grants no authority |
| Security/CVE/secret audit | UNKNOWN: local threat tests/partial scan; dedicated scanners unavailable; not external certification | Security reviewer perform scanners, CVE and same-owner race review |
| Packaging/CI | IMPLEMENTED local sdist/wheel, extracted and actual installed-wheel HTTP smoke; YAML syntax checked | Maintainer verify remote CI and clean-machine installs (UNKNOWN) |
| Recovered REA directive | UNKNOWN separate untracked file preserved; no recovered drive audit/import executed | Establish bounded read-only scope separately; exclude private machine data from public records |
| Human acceptance/release | BLOCKED by scholarly, rights, institution, security and manual gates | Release reviewer close gates; no push/merge/deploy without separate instruction |
