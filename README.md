# ⚔ Divine Arsenal Universal — FR3KD3V

A **local-first astronomical and Hermetic research workbench** with individual birth
profiles and a deterministic personalised AI-agent configuration generator.

**Status: experimental X1 validation build, not production or hosted SaaS.**

## What works in this release

- Real astronomical geocentric planetary longitudes from MIT-licensed Astronomy Engine.
- Moon phases, 28 equal-interval lunar-mansion index, inferred retrograde motion.
- Real sunrise-to-next-sunrise unequal planetary hours with IANA timezone handling.
- Date-only births show explicit uncertainty; exact recorded clock times enable exact
  positions (Ascendant/houses are not yet implemented).
- Private local multiple profiles, current location separated from birthplace, manual private JSON export and profile/workspace deletion.
- Goal-selected agent roles, project-scoped Hermes/Codex/OpenCode files, read-only MCP tools.
- Math-verified 3×3 to 9×9 magic squares for traditional planetary associations.
- Local dashboard, lunar/planetary timing, generated agent preview, birthplace lookup
  only on explicit click and source/precision labels.

## X1 installation

```bash
git clone https://github.com/fr3k-d3v/divine-arsenal.git
cd divine-arsenal
uv sync --extra test
uv run pytest -q
uv run divine-universal serve
# Open http://127.0.0.1:8768 in the X1 browser
```

Use `uv run divine-universal chart --dob YYYY-MM-DD --tz Australia/Sydney`
for a date-only astronomical preview or `uv run divine-universal today --lat -33.8688 --lon 151.2093 --tz Australia/Sydney`.

`uv run python -m divine.mcp_server` provides a read-only MCP stdio server.
For user-specific staged agent workspaces, open the local dashboard and compile a
profile's agent plan; **no global Hermes/Codex/OpenCode settings are modified**.

## Boundaries

- Original personal edition remains at https://github.com/fr3kchy/divine-arsenal.
- Data about each actual user belong on that user's machine, not in GitHub.
- Spiritual/Hermetic meaning is traditional interpretation, not astronomy, prediction,
  physical authority, legal/financial advice, or a reason to run agent commands.
- The local API has no internet-ready authentication. Keep bound to loopback.
- No claim of full ancient textual reconstruction, precise houses, rectification,
  professional electional predictions, hosted SaaS security or production completion.
- Repository includes a roadmap and source/evidence register in docs.

## Upstream foundation

[cosinekitty/astronomy](https://github.com/cosinekitty/astronomy) (MIT),
[astral](https://github.com/sffjunkie/astral) (Apache-2.0),
[Model Context Protocol](https://github.com/modelcontextprotocol/python-sdk) (MIT).
Consult each upstream distribution for exact bundled license terms.


## Research corpus and developer execution

The photographed-source research, archival references, evidence model, rights constraints and engineering translation are documented in:

- [Photographed source corpus and Divine Arsenal design](docs/PHOTOGRAPHED_SOURCE_CORPUS_AND_DIVINE_ARSENAL_DESIGN.md)
- [Primary-source research addendum](docs/research/PRIMARY_SOURCE_RESEARCH_ADDENDUM.md)
- [AI developer master execution plan](docs/AI_DEV_EXECUTION_PLAN.md)
- [Omarchy AI developer handoff prompt](docs/AI_DEV_HANDOFF_PROMPT.md)

The execution plan is authoritative for phased implementation. It keeps original sources, historical scholarship, tradition-specific interpretations, reconstructions and hypotheses distinct. It also establishes rights, privacy, provenance, testing and approval gates.

## Research workbench slices (local experimental build)

- **Source Atlas:** 27 schema-validated public metadata records, search, evidence,
  provenance and separate text/image rights. Records come from the supplied
  research documents; external sources have not been freshly verified here.
- **Psalter:** 150 work IDs, MT five-book navigation, common MT/LXX chapter
  correspondences and edition deep links. No Psalm text bodies are bundled.
  The chapter table is a reconstruction pending edition review; it does not
  resolve verse numbering, superscriptions or Psalm 151.
- **Text lab:** Hebrew RTL input and two explicit versioned symbolic schemes,
  including per-code-point traces and final-letter rules. No inferred authority.
- **Manuscript spike:** paste/upload a bounded IIIF Presentation 3 painting-image
  manifest. Validation is local. External images load only on explicit click,
  from allowlisted institutional hosts. The checked fixture is synthetic;
  a real institutional integration remains unverified.
- **Diagram export:** deterministic SVG mathematical squares with geometry/number
  groups, visible reconstruction labels and algorithm provenance. This is not
  a historical trace or full diagram editor.

The canonical UI is packaged at `divine/web/index.html`; `web/index.html` is a
compatibility symlink. Source and wheel distributions include research data and UI.
The agent currently executing this work is project-scoped. The app can stage
adapter proposals; it does not launch a model agent or enable automation.

Reproduce checks:

```bash
uv sync --extra test
uv run pytest -q
uv run python -m compileall -q divine
node tests/check_web.mjs
uv build --out-dir /tmp/divine-build
uv run python tests/check_wheel.py /tmp/divine-build/*.whl
# With the app running, Chromium and Node installed:
node tests/ui_smoke.mjs
```

The browser smoke writes screenshots of public-only research views under
`docs/execution/evidence/`. Use an empty isolated `DIVINE_DATA_DIR` when checking
UI so no real private profile is loaded into evidence. Where the uv default cache
is read-only, set `UV_CACHE_DIR=/tmp/divine-uv-cache`. This session's sandbox also
blocked TestClient thread wakeups; the same tests passed in the permitted local
execution environment. See [execution status](docs/execution/STATUS.md),
[acceptance matrix](docs/execution/ACCEPTANCE_MATRIX.md) and
[threat model](docs/architecture/SECURITY_AND_PRIVACY.md) for actual scope and gaps.
