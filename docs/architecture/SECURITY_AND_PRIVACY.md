# Local threat model — implementation review, not external security certification

Data flows: browser → loopback FastAPI → packaged public research metadata or
private SQLite. Astronomy executes locally. Birthplace lookup explicitly calls
Nominatim. IIIF validation never calls a URL; an explicitly requested image loads
in the browser from an allowlisted institutional host. External citation links
open provider sites. No telemetry, cloud model calls, schedulers or agent launch.

| Threat | Control / test | Residual limitation |
|---|---|---|
| DNS rebinding / foreign websites | Local client, Host, Origin and cross-site fetch checks | No authenticated multi-user boundary; trusted OS account required |
| JSON resource abuse | Stream-bounded 1 MiB bodies, source/canvas/Unicode limits | No rate limiting; owner can still exhaust local resources |
| XSS in imported labels | textContent, no innerHTML; CSP; JPEG/PNG-only images | Inline script/style need unsafe-inline; full CSP nonce work remains |
| SSRF / local file retrieval | No manifest fetch; allowlisted image hosts; HTTPS, no credentials/alternate ports | Institution availability/rights/redirects unverified; CSP limits image origins |
| SVG script/event injection | Generated fixed vocabulary only; no arbitrary SVG import | Future editor/import must add separate sanitizer |
| Workspace path traversal / symlinks | Canonical UUID, resolved path containment before mkdir/write/delete; random private temp files | Concurrent hostile OS-owner symlink swaps not fully race-proof |
| Private profile leaks | Separate storage, 0700 root/0600 database, no-store API, minimized list, explicit export/delete | No encryption/auth; exports/backups not erased by deletion |
| Symbol-based privilege escalation | Calculations grant NONE; plans remain OBSERVE/disabled | Staged files are proposals, not a sandbox enforcement engine |
| Historical/copyright misrepresentation | Evidence and per-asset rights exposed; no full-text/scans | Fresh external rights/source verification BLOCKED |

Existing lifecycle integration covers profile CRUD, local export payload, staging
and workspace deletion. SQLite connections now close explicitly. WAL/backups,
filesystem snapshots and browser downloads have separate lifecycles; secure_delete
is not a claim of forensic erasure. Malicious local OS owners are outside the
single-owner trust boundary. Network restriction was not bypassed.

Validation: tests/test_research.py threat cases and browser smoke. No fresh CVE
audit or dedicated secret scanner available; uv dependency compatibility is not a
vulnerability audit. Manual diff review and targeted secret-pattern scan are only
partial checks. Do not call this production ready.


Research Edition 1.1 adds strict private notebook imports with atomic rollback,
version/kind/coordinate/Unicode validation and optimistic concurrency. Backup
capacity stays under the API's 1 MiB boundary; imports assign fresh IDs and never
execute content. Profile data is excluded from notebook backups. TEI rejects DTDs,
entities, processing instructions and unknown/inconsistent profile structures.
Default local-only mode blocks external geocoding and image origins in CSP as
well as disabling image actions. No model, scheduler, telemetry or remote write.
Deletion removes notebook rows/revisions, not independent exports or filesystem
backups; no encryption, authentication or forensic erasure is claimed.
