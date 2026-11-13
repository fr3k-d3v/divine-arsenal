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

Final running-process HTTP smoke (exit 0): urllib requests to `/api/health`,
`/api/sources`, `/api/psalter`, `/api/docs` all 200 with expected content; no
private profile data printed. PID at check: 303516. This is local runtime
verification only. Final code milestone: `de0bc27`.

## Research Edition 1.1 continuation — phase 11

- Fresh baseline: `UV_CACHE_DIR=/tmp/divine-uv-cache uv run pytest -q`: 76 passed.
  Sandboxed TestClient again hung; identical permitted local command passes.
- Updated full suite: same command: 101 passed, one existing warning (0.63 s).
- `uv run python -m compileall -q divine`: exit 0.
- `node tests/check_web.mjs`: exit 0, 142 unique IDs and valid inline JS.
- `uv pip check`: exit 0, 40 installed packages compatible, not CVE audit.
- `uv build --offline --out-dir /tmp/divine-build-1.1`: exit 0, sdist + wheel.
- `uv run python tests/check_wheel.py /tmp/divine-build-1.1/*.whl`: exit 0.
- `uv run python tests/check_installed_wheel.py /tmp/divine-build-1.1/*.whl`:
  exit 0; real wheel installation in temporary venv without downloads; imports,
  packaged UI/data, HTTP and private notebook create/delete verified. Dependency
  modules reused from project site-packages; this is not a clean OS install.
- `node tests/ui_smoke.mjs`: exit 0, Chromium 155, 34 assertions at 1440×1100 and
  390×844, zero JS exceptions/external requests; evidence JSON and screenshots
  regenerated. Keyboard simulation first failed; complete native Enter event
  corrected the test and all assertions reran. No assertions skipped.
- `git diff --check`: exit 0.
- Python socket DNS probes: www.loc.gov, iiif.io, www.bl.uk each failed with
  `gaierror [Errno -3] Temporary failure in name resolution`. No fresh access date
  or verified institutional/rights claim added.

All uv commands above use UV_CACHE_DIR=/tmp/divine-uv-cache. Test/browser/wheel
HTTP execution uses the permitted local environment due to sandbox thread and
loopback limitations. Notebook test inputs are project-original/synthetic only.
Six solar reference vectors are independently calculated using installed Astral
3.2, not copied from Astronomy Engine; acceptance tolerance 0.03 degrees, maximum
observed difference ~0.00454 degrees. This is a solar algorithm cross-check only.

## Final Research Edition 1.1 verification

Implementation commit: `498ca14`. Evidence:
[evidence/validation-1.1.json](evidence/validation-1.1.json).

| Command / observation | Exit | Actual result |
|---|---:|---|
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run pytest -q --junitxml=/tmp/divine-1.1-tests.xml` | 0 | 131 passed, one existing dependency warning, 0.93 s; JUnit failures/errors/skipped all 0 |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run python -m compileall -q divine` | 0 | compiled |
| `node tests/check_web.mjs` | 0 | valid JavaScript, 155 unique HTML IDs |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv pip check` | 0 | 40 packages compatible |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv build --offline --out-dir /tmp/divine-build-1.1-final` | 0 | source and wheel built; hashes in evidence JSON |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run python tests/check_wheel.py /tmp/divine-build-1.1-final/divine_arsenal_universal-0.1.0-py3-none-any.whl` | 0 | packaged import/data/UI HTTP smoke |
| `UV_CACHE_DIR=/tmp/divine-uv-cache uv run python tests/check_installed_wheel.py /tmp/divine-build-1.1-final/divine_arsenal_universal-0.1.0-py3-none-any.whl` | 0 | actual temporary installation, imports, notebook create/delete, local HTTP |
| `node tests/ui_smoke.mjs` against final restarted app | 0 | 41 assertions, desktop/mobile; no JS exceptions/external requests; synthetic data cleaned |
| local PyYAML parse and expected matrix/13-step assertions | 0 | configuration syntax/shape only; remote CI UNKNOWN |
| `git diff --check` and `git diff --cached --check` | 0 | no whitespace errors |
| `command -v pip-audit`, `command -v gitleaks` | 1 each | scanners unavailable; no full audit claimed |
| targeted `rg` key/token patterns over code/tests/execution docs/README | 1 | no matches; partial pattern check only |
| source archive paths matching private/, REA directive, sqlite3 or key suffix | 1 | no matching entries; not a complete secret audit |
| actual urllib HTTP smoke | 0 | nine endpoints return 200: /, health, sources, Psalter, notebook, graph, notebook export, local docs, OpenAPI |
| `ss -ltnp 'sport = :8768'` | 0 | one listener at 127.0.0.1:8768, app PID 390112 |

Three sampled palette contrast ratios are 8.88 (muted/surface), 16.47
(text/input) and 11.41 (focus/surface). No form controls lack a label/ARIA name
source. These are limited automated checks, not full rendered contrast, semantic
quality, keyboard coverage, screen-reader testing or WCAG conformance. Updated
mobile screenshot visually inspected; it shows part of the lab at its actual
scroll position, not a full-page audit.

Both sandbox-hung pytest sessions were interrupted explicitly (exit 130); the
identical full local suite passes. Earlier app processes from this continuation
were stopped before final restart. Final PID 390112 remains running in tool
session 89722; no global service or model provider agent was launched. Health
confirms local-only and no app automation. Notebook is empty after synthetic test
cleanup; no real profiles or journals used. The separate untracked REA directive
was preserved outside commits and archive inputs. Tracked implementation was
clean after commit 498ca14. A final documentation commit records this evidence.
