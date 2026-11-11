# Validation evidence — 2026-11-12

All results below are local observations. Python version 3.13.18; Node v26.12.0;
Chromium 155.0.8059.84. Remote CI's 3.12/3.13 matrix has not been executed here.

| Command | Exit | Observed result |
|---|---:|---|
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv sync --extra test` | 0 | existing locked dependencies installed/compatible |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run pytest -q --junitxml=/tmp/divine-test-results.xml` | 0 | 76 passed, one existing Starlette/httpx deprecation warning, 0.53 s |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run python -m compileall -q divine` | 0 | no compile failures |
| `node tests/check_web.mjs` | 0 | JS syntax valid, 85 unique HTML IDs |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv pip check` | 0 | 40 packages compatible; not CVE audit |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv build --no-build-isolation --out-dir /tmp/divine-build` | 2 | setuptools absent in project venv; resolved by normal isolated offline build |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv build --offline --out-dir /tmp/divine-build` | 0 | cached build backend created sdist and wheel |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run python tests/check_wheel.py /tmp/divine-build/divine_arsenal_universal-0.1.0-py3-none-any.whl` | 0 | extracted-wheel import, catalogue, UI and HTTP verified |
| `node tests/ui_smoke.mjs` | 0 | desktop/mobile task assertions; see evidence/ui-smoke.json |
| `git diff --check` | 0 | no whitespace errors |
| targeted `rg` key/token patterns over new code/tests/docs | 1 | no matches; partial pattern scan, not full secret audit |
| `command -v ruff`, `command -v pip-audit`, `command -v gitleaks` | 1 each | unavailable; no lint/type config or fresh CVE audit claimed |

Full API tests and browser execution need the permitted local environment because
sandbox TestClient thread wakeups hang (see BASELINE.md). No test failures were
hidden: browser first failed an overly narrow shelfmark-search expectation, then
found missing same-document hash navigation; both were corrected and rerun.
Tests have not been skipped to produce the final count.

Evidence files contain only project-authored/public metadata and synthetic input:
`evidence/atlas-desktop.png`, `evidence/atlas-mobile.png`, `evidence/lab-mobile.png`,
`evidence/ui-smoke.json`. Screenshots were inspected for layout. Automated task
checks are not full WCAG conformance, screen-reader review or actual user usage.
Institutional images were not fetched and synthetic IIIF images are not live URLs.
Original TEI fixture is well-formed and linked, not TEI schema-certified.

Local server: `DIVINE_DATA_DIR=$PWD/private/session UV_CACHE_DIR=/tmp/divine-uv-cache uv run divine-universal serve`.
Local API/HTML checks return expected content; no private real profiles were used.
Only the loopback app is started; no global agent, provider, scheduler or systemd
service is installed or activated. No deployment, merge, DNS changes or paid API.
