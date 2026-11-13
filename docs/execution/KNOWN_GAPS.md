# Research Edition 1.1 — unresolved gates

Every unverified gate below remains open; tests/commits are not real usage.

| ID | State | Exact evidence / reason | Next action | Owner |
|---|---|---|---|---|
| SOURCE | BLOCKED | www.loc.gov, iiif.io, www.bl.uk DNS errno -3 on 2026-11-12; 27 supplied metadata summaries have no fresh access date | Inspect authoritative records when permitted DNS works; retain raw lawful evidence and exact edition | Source researcher |
| RIGHTS | BLOCKED | No inspected rights-cleared Psalm edition/provider; text remains null | Verify edition, licence/territory/provider terms before importing bodies | Rights reviewer |
| VERSES | UNKNOWN | Edition-aware verse-coordinate structure implemented; common MT/LXX chapter reconstruction tested; actual verses/superscriptions unverified | Acquire source-backed verse/edition table, review split/merge cases | Textual scholar |
| GRID | UNKNOWN | No matched public plate/folio; Sloane 3188/3189 kept distinct | Verify exact 3189 item then match image/folio; retain HYPOTHESIS | Manuscript researcher |
| ENOCHIAN | BLOCKED | No attested rights-cleared chart/edition inventory | Identify chart source and variant before encoding words/glyphs | Language researcher |
| IIIF-LIVE | BLOCKED | Synthetic fixtures only; institutional network unavailable | Test one lawful institutional manifest/image service and attribution | Source researcher + maintainer |
| TEI-SCHEMA | BLOCKED | Strict project exchange profile round-trips; no pinned full TEI schema available locally | Obtain lawful pinned TEI schema; schema validate broader sourceDoc/facsimile export | Edition maintainer |
| EDITOR-ACCEPTANCE | UNKNOWN | Private coordinate/revision workflow tested synthetically; no human manuscript correction acceptance | Review real lawful transcription with keyboard/RTL and confirm alignment | Human editor |
| GRAPH-CONTENT | BLOCKED | Cited graph workflow works; no newly verified historical edges | Add reviewed source-backed relationships, including disputes and intervals | Historian |
| ATLAS-IMPORT | UNKNOWN | Public metadata validates; accepted metadata not persisted into public atlas | Design reviewed local catalogue overlay and duplicate/conflict UX | Maintainer |
| STUDIO | UNKNOWN | Deterministic SVG squares only, no general tracing/overlay/vector editor or golden-image reference corpus | Implement neutral geometry/layer editor; acquire lawful comparison images | Maintainer + rights reviewer |
| LANGUAGE | UNKNOWN | Two schemes, five positional letter operations and four grid operations tested; historical table attribution and broader selectors not reviewed | Review scholarly rule sources; add explicit skip/permutation/word-boundary selectors if needed | Language reviewer + maintainer |
| ASTRO | UNKNOWN | Six independent approximate solar vectors pass; Moon/planet and precise observer references absent | Acquire independent ephemeris/observational vectors with frame/time/uncertainty | Astronomy reviewer |
| A11Y | UNKNOWN | Browser keyboard/RTL/layout tests; no full automated WCAG or screen-reader/manual audit | Audit all workflows with screen reader and contrast tooling | Accessibility reviewer |
| SECURITY | UNKNOWN | Local threat tests pass; no CVE/secret scanner/external security review; same-owner symlink races residual | Dedicated scanner and filesystem race review; audit backups/export permissions | Security reviewer |
| CI | UNKNOWN | No remote CI observation; local Python 3.13 only | Run remote supported-version matrix when access authorized/available | Maintainer |
| OPTIONAL-AGENT | BLOCKED | No bounded provider task requested; adapters disabled/staging only | Only implement bridge after explicit task/provider/authority requirements | User + maintainer |
| RELEASE | BLOCKED | Rights, institutional, scholarly, manual acceptance and security gates above open | Reassess checklist after independent review; separate merge/deploy instruction | Release reviewer |

Implementation is time/resource bounded, not a claim that viable open editor,
transformation and audit work is impossible. No global activation, paid provider,
scheduler, deployment, push or merge has been performed.

See REQUIREMENT_DISPOSITION.md for the full plan mapping, including general diagram
editing, richer graph types, command palette, OCR/overlays and the separate
untracked REA directive. These are not silently classified as implemented.

## REA integration limits — 2026-11-13

- The browser bridge is capped at 700,000 bytes; use the local URE CLI for larger files.
- URE classification remains signature-based, but verified local OBSERVE adapters now add bounded PDF lexical metadata, TEI XML structure counts, IIIF Presentation v2/v3 manifest counts, PNG/JPEG/TIFF header/IFD metadata and CSV/TSV structure counts. No PDF rendering, OCR/HTR, image pixel decoding, cell-value output, formula evaluation, external IIIF resource fetch or scholarly correctness verdict is provided.
- URE reports are static/synthetic analysis records, not runtime-behaviour, vulnerability, authorship or safety verdicts.
- Frida, PlatformIO, sigrok, serial capture, flashing, physical hardware and Fleet execution remain disabled or separately gated.
- Large-file streaming, OCR/HTR, image interpretation, TEI P5 schema validation, universal IIIF conformance, scholarly correctness review and broader specialist adapters remain open; the nine local scholarly format paths (including IIIF Presentation v2 and v3) and analysis-reference notebook/OBSERVATION graph path are now implemented and sandbox-tested.
- URE and Divine Arsenal now run as enabled user systemd services with restart-on-failure and a private mode-0600 environment file. A documented token-rotation procedure and independent secret-management review remain open.
- Recovered repository upstream freshness, advisories, transitive licensing and redistribution rights remain UNKNOWN; no recovered source code is vendored.
## Closed gap — REA notebook / provenance graph

The previous gap stating that REA reports were not attached to the Divine private notebook or Tradition Graph is closed in source and live acceptance: successful jobs can be saved as structured analysis-reference documents, optionally linked to a registered source, and represented as local OBSERVATION graph nodes/edges. The 53-assertion Chromium run verified the live save-to-notebook and graph path after the controlled service restart.

## Live service acceptance — 2026-11-13

The URE and Divine Arsenal services are managed by enabled user systemd units with restart-on-failure. Their local REA connection is authenticated and READY. The full local browser flow and both automated test suites pass. Five additional scholarly metadata/structure adapters are enabled after the real Bubblewrap probe and nine synthetic format paths (including IIIF Presentation v2 and v3) pass live Divine → URE acceptance. Remaining release gates are unchanged: lawful real source/rights, scholarly correctness, full WCAG/manual accessibility, external security, remote CI, OCR/HTR and physical/remote authority.

## Scholarly adapter verification — 2026-11-14

The five newly enabled adapters and their exact scope are documented in `docs/research/REA_INTEGRATION_ARCHITECTURE.md` section 13. The complete machine-readable record is `docs/execution/evidence/scholarly-adapter-acceptance-2026-11-14.json`. No real manuscript, institutional manifest or customer spreadsheet was used.
