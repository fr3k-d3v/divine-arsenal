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
