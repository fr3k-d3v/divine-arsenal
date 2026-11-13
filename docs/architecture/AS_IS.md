# Observed architecture

FastAPI `divine/server.py` serves one inline HTML/CSS/JS application and JSON APIs.
`astro.py` uses Astronomy Engine + Astral + zoneinfo; `traditions.py` constructs
normal mathematical squares, with conventional planetary associations separately.
`store.py` stores private JSON payloads in SQLite with a configured private root.
`agents.py` stages disabled goal-selected workspaces. `mcp_server.py` exposes
read-only explicit-input calculations. `cli.py` exposes local commands and server.

Routes: `/`, `/api/health`, profiles collection/detail CRUD, astro by profile,
agent capabilities/preview/compile, traditions, geo/search, research, kamea and
correspondence. Birthplace search alone calls Nominatim after explicit action.
Health currently creates the private root. Default data lives outside this repo;
this session must override DIVINE_DATA_DIR to an isolated allowed location.

Risks: no Host validation (DNS rebinding); cross-site GETs not rejected;
unbounded JSON bodies; broad geo exception; private SQLite lifecycle relies on
context manager that commits but does not explicitly close; generated workspace
paths assume a trusted profile ID. Local owner boundary is not authentication.
No independent precise ephemeris reference fixture. Existing tests cover range
checks, DST, continuity, square invariants, profile lifecycle and staged authority.
