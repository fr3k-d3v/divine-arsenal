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
