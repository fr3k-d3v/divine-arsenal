# Phase 0 baseline — 2026-11-12

OBSERVATION: branch `feat/source-atlas-psalms-visuals`, clean initial checkout;
HEAD `89edb51`. Required docs and all existing Python, HTML/JS, tests and CI read.

Commands and results:

| Command | Exit | Result |
|---|---:|---|
| `git status --short` | 0 | empty |
| `git branch --show-current` | 0 | requested feature branch |
| `uv sync --extra test` | 2 | default cache read-only; no dependency mutation |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv sync --extra test` | 0 | 43 resolved, 40 checked |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run pytest -q` | pending | first 29 tests complete; API TestClient hangs, investigation ongoing |
| `curl --max-time 15 -I https://iiif.io/api/presentation/3.0/` | 6 | DNS unavailable |
| `curl --max-time 10 -I https://github.com/fr3k-d3v/divine-arsenal/pull/7` | 6 | DNS unavailable |

BLOCKED: public PR #7/CI and fresh source/standards retrieval by network DNS
restrictions. No proxy, connected account or paid retrieval used to bypass them.
Supplied research is a secondary repository record, not fresh verification.
The previously reported 32-pass baseline is historical; not yet reproduced here.
Node, Chromium and Firefox are present; Playwright/Puppeteer are not installed.
No frontend build, lint or type-check configuration exists initially.

The current Source Atlas is a static JS array, without citations/rights records.
Psalter creates 150 external KJV links, five correct ranges, but has no edition
model, text provider or coordinate mapping. No Hebrew/IIIF/TEI/SVG export exists.
Runtime/UI evidence will be recorded separately. No deployment performed.
