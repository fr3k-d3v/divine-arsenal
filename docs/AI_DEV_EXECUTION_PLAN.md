# Divine Arsenal — AI Developer Master Execution Plan

**Repository:** https://github.com/fr3k-d3v/divine-arsenal  
**Target branch:** `feat/source-atlas-psalms-visuals` (continue the existing draft PR #7; do not merge or deploy without explicit approval)  
**Product posture:** local-first, evidence-driven, experimental until all release gates pass.  
**Execution doctrine:** OBSERVE → VERIFY → RECONCILE → IMPROVE → TEST → RECORD.

This is the authoritative implementation plan for the AI developer operating on Omarchy. It is deliberately written as an executable work order. Follow phases in dependency order, work autonomously where authority is granted, record blockers precisely, and never fabricate completion.

---

## 0. Mission and definition of success

Build Divine Arsenal into a polished, local-first scholarly and symbolic research workbench that connects:

1. Canonical and historical texts.
2. Manuscript images and editions.
3. Transcriptions, translations and language systems.
4. Symbolic diagrams, seals, number grids and visual reconstructions.
5. Named traditions and their historical relationships.
6. Real astronomical calculations and separately labelled traditional correspondences.
7. Private reflection and user-controlled workspaces.
8. An optional FR3K agent integration with strict authority boundaries.

The product must be beautiful, useful offline, inspectable, reproducible and honest about uncertainty.

**Not the mission:** claim supernatural efficacy, manufacture a single universal occult canon, turn symbolic readings into facts, or allow a reading/ritual/chart to grant agents access to hardware, accounts or files.

### Release definition

A feature is complete only when:
- It exists in the code and is reachable in the UI.
- Data is sourced, versioned and rights-cleared.
- Failure states and uncertainty are represented.
- Unit, integration and security tests pass.
- A human can verify the behaviour using documented steps.
- Evidence is recorded in the repository.
- Deployment is separately verified if deployment is authorised.

A Git commit, green CI, successful build, running process or mock response is not proof of deployed or end-to-end functionality.

---

## 1. Mandatory operating rules for the AI developer

### 1.1 Initial observation

Before changing code:
1. Read `AGENTS.md`, `README.md`, this plan, the photographed-source corpus document and research addendum.
2. Inspect current branch, git status, latest commit, open PRs and CI.
3. Inspect the full repository tree and existing app/API architecture.
4. Run baseline tests exactly as documented.
5. Capture current UI screenshots at phone and desktop sizes if browser tooling is available.
6. Inventory existing features, routes, modules, dependencies, tests, storage and known gaps.
7. Produce `docs/execution/BASELINE.md` with observed facts, commands, outputs, screenshots/paths, failures and unknowns.

Do not overwrite user changes. Do not reset, clean, force-push or rewrite history. Do not expose secrets in logs or evidence.

### 1.2 Evidence labels

Use these labels in docs, UI, API and agent output:

- `VERIFIED FACT`
- `OBSERVATION`
- `HISTORICAL CLAIM`
- `TRADITIONAL INTERPRETATION`
- `RECONSTRUCTION`
- `HYPOTHESIS`
- `UNKNOWN`
- `BLOCKED`
- `CONTRADICTED`

Every claim should link to evidence records. Avoid a single opaque truth/confidence score. Store source-level and claim-level evidence separately.

### 1.3 Autonomy and permissions

The AI developer may autonomously:
- Inspect this repository and local project files.
- Build and test on Omarchy.
- Add code, tests and documentation on a feature branch.
- Use public, rights-cleared research sources.
- Create local fixtures and synthetic test data.
- Improve local visual design and accessibility.

Approval required before:
- Merging PRs to main.
- Deploying to public hosting or changing DNS.
- Publishing private user photos, private journal entries, birth profiles, personal data or local infrastructure details.
- Using paid external APIs or incurring costs.
- Accessing external accounts or changing credentials.
- Enabling agents to write outside a project sandbox.
- Running commands on hardware or physical systems.
- Sending content to third-party model providers.
- Importing copyrighted full-text corpora without a documented licence.

Default to read-only and local. Fail closed.

---

## 2. Target architecture

Use the existing stack where practical. Do not rewrite the working astronomy core merely to introduce a new framework.

### 2.1 Logical components

**A. Experience shell**
- Responsive desktop/mobile navigation.
- Search palette and command palette.
- User-owned workspaces.
- Keyboard-first accessibility.
- Voice input/output only when explicitly enabled.
- Local-first status and source/evidence indicators.

**B. Source Atlas**
- Works, editions, manifestations, manuscript witnesses, physical/digital copies.
- Authors, scribes, translators, editors, publishers and institutions.
- Title pages, copyright pages, catalogue records, page/folio coordinates.
- IIIF manifests and image services.
- Rights and reuse conditions.
- Source-level notes and claim-level citations.

**C. Psalter**
- 150 Psalm work records and five-book grouping.
- Edition-aware text, language and versification.
- Hebrew/Masoretic and LXX/Vulgate coordinate mapping.
- Verse-level references and cross-references.
- Genre/theme tags with attribution and uncertainty.
- Text comparisons and translation notes.
- No generated paraphrase in place of canonical text.

**D. Text & Language Lab**
- Unicode-safe text storage.
- Hebrew right-to-left display and normalization.
- Transliteration distinct from original script.
- Gematria schemes as named, versioned algorithms.
- Letter extraction, permutation and grid transformations.
- Enochian alphabet/glyph records with historical attribution.
- Reproducible operation traces.

**E. Manuscript & Facsimile Viewer**
- IIIF Presentation API 3.0 manifests.
- Deep zoom using IIIF Image API where available.
- Page/folio navigation.
- Parallel facsimile/transcription panes.
- Region annotations and source coordinates.
- OCR/HTR results with confidence and human correction.
- Never claim unavailable digitisation is available.

**F. Symbol & Diagram Studio**
- SVG-first vector geometry.
- Layered diagram construction.
- Number grids, kameas, seals, circles, inscriptions and symmetry.
- Compare scan, transcription, reconstruction and interpretation.
- Export SVG/PNG/PDF only after provenance and rights checks.
- Every generated diagram labelled as generated/reconstructed.

**G. Tradition Graph**
- Nodes: works, people, institutions, concepts, symbols, traditions, editions, manuscripts and claims.
- Edges: authored, translated, copied, cited, influenced, resembles, interpreted-as, disputed-by.
- Every relationship has evidence, date range and attribution.
- Do not infer direct influence from visual similarity alone.

**H. Celestial Workbench**
- Preserve the existing deterministic Astronomy Engine integration.
- Distinguish calculated astronomy from traditional astrological/planetary correspondence.
- Store timezone, observer location, time precision, algorithm/library version and inputs.
- Show uncertainty where birth time/location are unknown.
- Never represent symbolism as causal prediction.

**I. Journal & Reflection**
- Private local-only notes by default.
- User-controlled export and deletion.
- No default cloud sync or telemetry.
- No automated psychological/health/personality diagnosis.
- No private journal ingestion into public model training or public GitHub.

**J. Agent Bridge (later phase)**
- Optional FR3K agent handoff.
- Explicit task manifest, stable job ID, sandbox, lease, permissions, approvals and evidence.
- Symbolic interpretation never grants execution authority.
- OBSERVE, AUTO, APPROVAL and PHYSICAL authority remain separate.
- Immutable terminal states and idempotent jobs.

### 2.2 Data architecture

Start with the existing local persistence pattern. If it is file-based, do not introduce a server database without a demonstrated need. If SQLite is already present or suitable, use migrations and a repository/service boundary.

Minimum logical entities:

- `Work`
- `Expression` (edition, translation, recension, version)
- `Manifestation` (physical copy or digital copy)
- `Witness` (manuscript or textual witness)
- `Agent` (person, institution, software)
- `Source` (catalogue, scholarly publication, primary object)
- `Claim`
- `Evidence`
- `Citation`
- `Passage`
- `CoordinateSystem` (chapter/verse, folio/side/line, page/region)
- `TranslationAlignment`
- `RightsRecord`
- `Symbol`
- `Diagram`
- `DiagramLayer`
- `Transformation`
- `Tradition`
- `Relationship`
- `Calculation`
- `Workspace`
- `JournalEntry`

Every entity gets a stable ID. Preserve source snapshots or hashes when legally permitted; do not mirror copyrighted texts/images without rights.

### 2.3 Provenance model

Map provenance concepts to W3C PROV-DM:
- Entity: source, passage, image, transcription, claim, diagram.
- Activity: scan, OCR, transcription, translation, calculation, annotation, reconstruction.
- Agent: author, translator, institution, human researcher, software tool.
- Derivation: transcription derived from page image; translation derived from edition; diagram derived from scan.
- Attribution/responsibility: who created or reviewed a result.
- Time: when the activity occurred.
- Bundle: provenance record for a research package.

Expose provenance in the UI. Do not reduce it to a badge with no inspectable chain.

---

## 3. Phased execution roadmap

Work in this order. Parallelise independent research and tests, not conflicting writes to the same files.

### Phase 0 — Baseline and architecture audit

Deliverables:
- `docs/execution/BASELINE.md`
- `docs/architecture/AS_IS.md`
- `docs/architecture/TO_BE.md`
- `docs/execution/KNOWN_GAPS.md`

Tasks:
1. Inventory existing modules, APIs, routes, data models, templates, JS/CSS, tests and dependencies.
2. Identify what already works: astronomy, sunrise/sunset, planetary hours, profiles, agent configuration, MCP server, local persistence, deletion/export.
3. Run tests, type/lint checks, build and static checks.
4. Map each existing capability to target architecture.
5. Identify regressions and duplicate implementations.
6. Produce a dependency-aware plan for refactoring only where necessary.

Exit gate:
- Baseline commands and results recorded.
- Existing features and risks mapped.
- No undocumented destructive changes.
- Architecture proposal fits existing project or documents evidence for a change.

### Phase 1 — Source Atlas and research corpus

Deliverables:
- Machine-readable source catalogue (JSON or database seed).
- Source Atlas UI backed by real catalogue data.
- `docs/research/SOURCE_REGISTER.md`
- `docs/research/RIGHTS_REGISTER.md`
- `docs/research/UNRESOLVED_IDENTIFICATIONS.md`

Tasks:
1. Convert every confidently identified photographed book into a structured record.
2. Keep uncertain shelf-spine identifications unresolved.
3. Add Library of Congress Agrippa and Barrett records.
4. Add British Library Sloane MS 3188 and 3189 as separate objects.
5. Investigate the photographed 49×49 grid as a possible Liber Logaeth comparison; keep it HYPOTHESIS until matched.
6. Add source types: primary text, manuscript, modern edition, scholarly reference, popular interpretation.
7. Add title page, edition, publisher, date, language, translator, source institution, shelfmark, stable URL, rights, access date and identification confidence.
8. Add source search/filter by tradition, date, language, medium and evidence class.
9. Add import tooling for public metadata only initially; do not bulk-download entire sites.
10. Build duplicate detection on identifiers/ISBN/shelfmark/manifest URI.

Exit gate:
- All known books are represented or listed in unresolved identification register.
- Every record has provenance and rights state.
- No user-uploaded photographs are committed.
- No unverified title/author is promoted to verified.

### Phase 2 — Psalter: complete, edition-aware foundation

Deliverables:
- `PsalterService`
- Psalm data schema and five-book navigation.
- Hebrew/LXX numbering mapping.
- Edition/rights-aware text provider.
- Search and verse deep-links.
- Test fixture set for numbering edge cases.

Tasks:
1. Create 150 stable Psalm work records.
2. Model five canonical books as an editorial structure, not a hardcoded assumption about every tradition.
3. Model Hebrew/Masoretic and LXX/Vulgate numbering separately.
4. Build a documented coordinate mapping table, including split/merged Psalm cases and superscription/verse-numbering caveats.
5. Support text providers: bundled public-domain source only where rights are verified; licensed external provider behind an adapter; user-imported text with user attestation and licence metadata.
6. Preserve original Hebrew, Unicode normalization form and RTL rendering.
7. Add verse-level source citations and translation labels.
8. Build cross-reference graph as sourced edges, not generated assertions.
9. Add Psalm themes and genres with attribution and multiple tags.
10. Create a reading view with side-by-side translations and optional commentary.

Critical licensing rule:
- KJV is public domain in the United States, but territorial rights, edition scans, typography and any third-party API terms still need checking.
- Do not bundle NIV/ESV/NRSV or other protected translations without an appropriate licence.
- Keep text content, image asset and metadata rights as separate records.

Exit gate:
- 150 Psalm records exist and can be navigated.
- Numbering conversion tests cover known LXX/Masoretic differences.
- No translation text appears without a rights record.
- Psalm citations resolve to the correct edition and coordinate system.
- UI clearly identifies source translation and versification.

### Phase 3 — Text, Hebrew and symbolic computation engine

Deliverables:
- Language registry and script renderer.
- Versioned gematria engine.
- Transformation trace viewer.
- Enochian alphabet registry.
- Property-based and fixture tests.

Tasks:
1. Implement Hebrew normalization/display with RTL support.
2. Distinguish grapheme, code point, transliteration and pronunciation.
3. Implement named gematria methods only after documenting each method's rules.
4. Include standard Hebrew letter values as a named scheme; do not silently apply final-letter variants.
5. Add explicit input validation and reproducible calculation traces.
6. Add letter extraction: first, last, middle, acrostic, skip sequences and word-boundary selection.
7. Add permutations as explicit algorithms with input/output positions.
8. Add Enochian glyph inventory with source attribution, manuscript/edition variant and uncertain mappings.
9. Add grid engine supporting dimensions, coordinate indexing, row/column transforms, rotations and deterministic serialisation.
10. Test Unicode edge cases, right-to-left punctuation and malformed inputs.

Important:
- Do not implement arbitrary “decode hidden message” as if outputs are validated.
- Every result must show algorithm, alphabet version, source text, transformation parameters and output.
- Treat semantic interpretation as a separate human-authored layer.

Exit gate:
- Reproducible results with test vectors.
- Every alphabet/value table versioned and source-attributed.
- RTL UI and copy/paste round-trip verified.
- No silent normalisation or character loss.

### Phase 4 — Manuscript viewer and scholarly transcription

Deliverables:
- IIIF manifest adapter.
- Manifest validator.
- Page viewer and annotation model.
- TEI P5 export/import spike.
- Transcription correction workflow.

Tasks:
1. Support IIIF Presentation API 3.0 manifests.
2. Use IIIF Image API for region/size requests where available.
3. Display page sequence, canvas labels, metadata and rights statements.
4. Support side-by-side page image and transcription.
5. Store page/folio/side/line/region coordinates.
6. Add transcription states: machine draft, human corrected, reviewed, published.
7. Mark illegible text as unclear; never hallucinate missing words.
8. Keep OCR/HTR confidence and engine/version.
9. Export TEI P5 with facsimile/sourceDoc/text structures where applicable.
10. Add region-level annotations for seals, diagrams and marginalia.

Exit gate:
- IIIF manifests validate.
- A user can navigate pages and open a stable page/folio URL.
- Text-to-image alignment is inspectable.
- Transcription corrections preserve previous versions.
- TEI export round-trips through validation.

### Phase 5 — Symbol & Diagram Studio

Deliverables:
- SVG geometry engine.
- Layered editor.
- Diagram catalogue.
- Export and provenance record.
- Golden image and geometry tests.

Tasks:
1. Define a neutral geometric model independent of any one tradition.
2. Support circles, polygons, lines, arcs, paths, text glyphs, grids, labels and anchors.
3. Implement snap/grid, symmetry, rotation, scaling and deterministic coordinate transforms.
4. Support multi-layer composition: source scan, traced geometry, text, annotations, interpretation.
5. Implement kamea/number-square templates only from documented source tables.
6. Provide cell/row/column values and formula validation.
7. Allow image overlay comparison and alignment.
8. Store original scan separately from vector trace.
9. Add export with visible reconstruction label and attribution.
10. Build accessible controls and keyboard operation.

Exit gate:
- SVG is deterministic and editable.
- Geometry tests validate symmetry and coordinate transforms.
- No diagram is presented as authentic source art unless it is the source image.
- Export metadata contains source, creator, date and transformation history.

### Phase 6 — Tradition Graph and research intelligence

Deliverables:
- Graph schema and query API.
- Relationship explorer UI.
- Claim/evidence inspector.
- Citation export.

Tasks:
1. Build entities and relationships with stable IDs.
2. Distinguish direct citation, translation, historical influence, shared motif, analogy and speculative similarity.
3. Add dated relationship intervals and source references.
4. Provide graph filters by tradition, era, author and evidence class.
5. Add conflicting claims side by side.
6. Add research notes with source snapshots/URL and access dates.
7. Add citation export (BibTeX, CSL JSON or RIS where practical).
8. Add search that ranks exact title/author/shelfmark above broad semantic matches.
9. Use LLM summarisation only as a derived layer with citations to underlying source records.
10. Never allow LLM-generated edges to be committed as verified facts without human review.

Exit gate:
- Every displayed relationship has an inspectable source.
- Speculative relationships are visibly labelled.
- Citation export round-trips.
- Search results expose why each item matched.

### Phase 7 — Celestial Workbench integration

Deliverables:
- Audited astronomy service.
- Reproducible calculation records.
- Separate correspondence registry.
- Regression tests.

Tasks:
1. Audit current Astronomy Engine calculations and reference vectors.
2. Preserve geocentric/heliocentric frame distinctions and time scales.
3. Record timezone, coordinates, timestamp precision, ephemeris/library version and algorithm inputs.
4. Separate computed planetary positions from traditional correspondences.
5. Clearly identify any derived or approximate values.
6. Add source-backed correspondence records for each tradition and edition.
7. Do not infer birth data or collect unnecessary sensitive information.
8. Verify all existing calculations with numerical reference tests.

Exit gate:
- Numerical outputs reproducible from stored inputs/version.
- Timezone and time-precision edge cases tested.
- Correspondence layer cannot overwrite astronomy values.
- Unknown birth time remains unknown.

### Phase 8 — Visual system and accessibility

Deliverables:
- Design tokens and component library.
- Responsive navigation.
- Dark manuscript / observatory visual theme.
- Accessibility test report.
- Screenshot evidence.

Visual direction:
- Deep aubergine/ink-black foundations.
- Restrained antique gold for manuscript and archive accents.
- Parchment only for reading surfaces.
- Spectral cyan for live measurements and instrument state.
- Fine-line geometric ornament, not random occult clip-art.
- Strong typography hierarchy: editorial serif for source titles, legible sans-serif for controls/data.
- Dense but calm instrument layouts; avoid endless cards and oversized decorative hero blocks.
- Motion subtle, purposeful and reduced-motion compliant.

Required screens:
1. Command/home.
2. Source Atlas.
3. Source/edition detail.
4. Manuscript viewer.
5. Psalter library and reader.
6. Hebrew/text lab.
7. Symbol/diagram editor.
8. Tradition graph.
9. Celestial workbench.
10. Private journal.
11. Settings, storage, rights and privacy.
12. Agent handoff/approval view (later phase).

Accessibility:
- WCAG 2.2 AA target.
- Keyboard navigation and visible focus.
- Semantic headings/landmarks.
- Accessible names for controls.
- Colour not sole carrier of evidence status.
- Contrast checks.
- Reduced motion.
- RTL tests.
- Mobile touch targets.
- Screen reader smoke tests.

Exit gate:
- Screenshots at mobile and desktop breakpoints.
- Automated accessibility scan plus documented manual checks.
- No broken overflow or unusable RTL.
- Core tasks can be completed by keyboard.

### Phase 9 — Local-first security, privacy and data lifecycle

Deliverables:
- Threat model.
- Privacy/data-flow diagram.
- Export/delete tests.
- Dependency and secret scan report.

Tasks:
1. Map all data flows and local storage locations.
2. Keep journal, personal profiles, birth data and uploaded private photos local by default.
3. Do not add telemetry without opt-in.
4. Validate all imported text/metadata as untrusted input.
5. Sanitize SVG; block script/event-handler injection and external references.
6. Prevent path traversal and unsafe archive extraction.
7. Use allowlisted URL schemes/hosts for remote manifest imports.
8. Add resource limits for huge images, PDFs, OCR jobs and grid transformations.
9. Add backup/export and tested deletion flows.
10. Keep secrets in environment/OS secret store; never in Git or client bundles.
11. Pin and audit dependencies.
12. Provide clear offline behaviour and no silent third-party transmission.

Exit gate:
- Threat model reviewed.
- Secret scan clean.
- Import abuse tests pass.
- Export and deletion tested.
- Network requests documented and controllable.

### Phase 10 — Optional FR3K Agent Bridge

This phase is not required for the first usable scholarly release. Do not block core research functionality on agent integration.

Deliverables:
- Explicit task manifest schema.
- Read-only integration first.
- Approval boundary.
- Audit journal.
- Mock adapter and end-to-end tests.

Rules:
- Agent task must have stable ID, declared goal, input set, workspace, permissions, lease, timeout and terminal state.
- OBSERVE is default.
- AUTO is limited to declared sandbox operations.
- APPROVAL is required for external writes and privileged changes.
- PHYSICAL authority is never inferred; explicit separate approval required.
- Idempotency keys, leases, fencing and immutable terminal states.
- Store raw tool outputs before interpretation.
- Agent can propose a symbolic interpretation but cannot use it to elevate authority.
- Do not put personal journal or birth-profile content into task context by default.

Exit gate:
- Read-only proof first.
- Denied operations fail closed.
- Replay/idempotency and expired lease tests pass.
- Every action has actor, input, output, timestamp and result evidence.

---

## 4. Priority order and parallel workstreams

Do not launch every phase simultaneously. Start with four independent workstreams after Phase 0.

| Workstream | Owner | First deliverable | Depends on |
|---|---|---|---|
| A — Source research | Research agent | Verified source register + rights register | Phase 0 |
| B — Psalter/data | Backend agent | Schema, Psalm coordinate mapping and test vectors | Phase 0 |
| C — Visual experience | Frontend agent | Design tokens, Source Atlas and Psalter responsive UI | Phase 0 |
| D — Quality/security | QA agent | Baseline tests, threat model and CI extensions | Phase 0 |

Then integrate through one orchestrator:
- One shared issue/task ledger.
- Stable task IDs.
- File ownership per worker.
- No parallel writes to the same file.
- Workers submit branch/patch plus evidence.
- Orchestrator reviews, reconciles and runs full tests.
- No worker can merge/deploy.

---

## 5. Repository organisation target

Adapt existing layout; do not blindly move functioning code.

```text
docs/
  architecture/
    AS_IS.md
    TO_BE.md
    DATA_MODEL.md
    SECURITY_AND_PRIVACY.md
  research/
    SOURCE_REGISTER.md
    RIGHTS_REGISTER.md
    UNRESOLVED_IDENTIFICATIONS.md
    PRIMARY_SOURCE_RESEARCH_ADDENDUM.md
  execution/
    BASELINE.md
    KNOWN_GAPS.md
    ACCEPTANCE_MATRIX.md
    RELEASE_CHECKLIST.md
  AI_DEV_EXECUTION_PLAN.md
  AI_DEV_HANDOFF_PROMPT.md

divine/
  core/
  sources/
  psalter/
  language/
  manuscripts/
  symbols/
  graph/
  astronomy/
  privacy/
  agents/

tests/
  unit/
  integration/
  security/
  fixtures/
  golden/

web/
  components/
  pages/
  styles/
  assets/
```

This is a target map, not permission to perform a risky mass refactor. Preserve current package boundaries if they are already coherent.

---

## 6. Required CI and quality gates

Add/retain CI for supported Python versions. Extend it with the checks appropriate to the actual frontend/build stack.

Required:
- Unit tests.
- Integration/API tests.
- Static type checks where configured.
- Lint/format checks.
- Python compileall.
- Frontend lint/build.
- JSON schema validation for source records.
- TEI XML validation for TEI outputs.
- IIIF manifest fixture validation.
- Accessibility smoke tests.
- Secret scanning.
- Dependency vulnerability audit.
- Deterministic numerical tests for astronomy.
- Golden tests for gematria, Unicode, Psalm mapping and SVG geometry.

CI must publish actual counts and failed test names. Do not report “all tests passed” if a job was skipped or unavailable.

---

## 7. Required developer reporting

At the end of each phase, create/update:
- `docs/execution/PHASE_<N>_REPORT.md`
- Changed files and commit SHA.
- Commands executed and exit codes.
- Test counts and full failure details.
- Screenshots or fixture evidence paths.
- Security/privacy impact.
- Known gaps and blockers.
- Whether anything was deployed (default: no).
- Next phase and dependencies.

Status vocabulary:
- NOT STARTED
- IN PROGRESS
- PASS
- FAIL
- BLOCKED
- UNKNOWN
- NOT APPLICABLE

Never mark a phase PASS on the basis of a commit alone.

---

## 8. Definition of done for the first public-ready milestone

The first milestone is **Research Edition 1.0**, not the entire agent platform.

Must include:
1. Source Atlas with verified/uncertain bibliographic records.
2. Rights and provenance registers.
3. Psalter 150-entry index with correct five-book divisions.
4. Psalm numbering architecture that can represent Hebrew and LXX/Vulgate differences.
5. At least one legally usable text edition with explicit rights.
6. Hebrew RTL and named gematria schemes with traceable output.
7. Source-backed Enochian alphabet records.
8. IIIF viewer proof-of-concept against a public institutional manifest.
9. Diagram Studio with source/reconstruction distinction.
10. Search and source citations.
11. Responsive, accessible visual system.
12. Local privacy, export and deletion tests.
13. Full CI and manual QA evidence.
14. Documentation sufficient for another developer to reproduce the setup.

Agent Bridge, advanced OCR/HTR, multi-user sync, paid APIs and cloud deployment are later milestones.

---

## 9. Immediate execution queue

The developer must execute these tasks first, in order:

- [ ] Read all repository instructions and current PR #7.
- [ ] Produce baseline inventory and run existing tests.
- [ ] Validate the current Source Atlas UI and fix any runtime errors.
- [ ] Validate all 150 Psalm navigation links and five-book boundaries.
- [ ] Add a machine-readable catalogue schema and seed data.
- [ ] Add source records for the visible books and all unresolved identifications.
- [ ] Add Sloane MS 3188/3189 research records, with the 49×49 grid match explicitly HYPOTHESIS.
- [ ] Add IIIF manifest adapter spike using an institutional public example.
- [ ] Add TEI P5 sample encoding for one short, rights-cleared transcription.
- [ ] Design and test the Psalm versification mapping model.
- [ ] Implement provenance chain for one source → page → transcription → claim.
- [ ] Add security/privacy threat model and rights register.
- [ ] Produce screenshots and full phase report.
- [ ] Request human review before merge or deployment.

**Do not begin broad UI expansion until the data/provenance model is accepted by tests.** A polished UI on top of untraceable data is a false milestone.

---

## 10. Final engineering doctrine

Divine Arsenal must preserve a strict distinction between:

- What a source says.
- What a scholar argues.
- What a tradition teaches.
- What a modern author interprets.
- What the software calculates.
- What the user personally experiences.
- What is objectively observed in the world.
- What remains unknown.

The product should make deep research possible without pretending to resolve every mystery.

**Build an instrument that can explore meaning without falsifying evidence; calculate without mystifying computation; delegate without surrendering authority; and preserve knowledge without losing its origin.**
