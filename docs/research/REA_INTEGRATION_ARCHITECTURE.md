# Divine Arsenal ↔ Universal Reverse Engineering Engine integration

**Architecture revision:** 1
**Observed:** 2026-11-13
**Application:** Divine Arsenal Universal, local Research Edition 1.1 branch
**Capability provider:** independently maintained private local URE capability service; private repository identifiers and deployment details are intentionally omitted from this public application repository.
**Integration mode:** local authenticated HTTP; OBSERVE-only from Divine Arsenal

## 1. Ownership and boundaries

Divine Arsenal owns the user-facing research workflows, scholarly source model, notebook, interpretation labels and provenance UI.

The separate URE capability engine owns file ingestion, content hashing, classification, adapter registry, sandboxed workers, job scheduling, evidence storage and reproducible reports. It is a reusable service that Divine Arsenal consumes. It is not a competing Divine Arsenal product and Divine Arsenal does not reimplement its scheduler or adapter runtime.

The original recovered REVERSE ENGINEER ANYTHING workspace is a source-evidence corpus only. The 29 repositories are not vendored, installed or executed by this integration. Selection and licensing observations are recorded in [REA_WORKSPACE_INVENTORY.md](REA_WORKSPACE_INVENTORY.md) and [rea-repository-register.json](rea-repository-register.json).

## 2. Runtime topology

```text
Browser (same-origin only)
        |
        | /api/rea/* — no credential exposed to browser
        v
Divine Arsenal local FastAPI process
  - validates file name, size and request schema
  - pins URE endpoint to IPv4 loopback
  - disables HTTP proxies and redirects
  - supplies bearer token from process environment
  - forces authority=OBSERVE
  - validates hashes and evidence references
  - strips worker IDs, fencing tokens and leases
        |
        | authenticated HTTP to 127.0.0.1 only
        v
URE local API v1
  - SQLite authoritative job state
  - content-addressed input and raw evidence stores
  - versioned adapter registry
  - bounded Bubblewrap worker isolation
  - deterministic evidence-linked reports
```

The URE API is loopback-only. It rejects non-loopback binds, browser Origin requests and mismatched Host headers. It has no remote transport, CORS or arbitrary server-file-path intake. The URE bearer token remains in the Divine Arsenal server process environment; it is never returned by a Divine API route or placed in browser JavaScript.

## 3. Configuration

Divine Arsenal reads these environment variables:

| Variable | Purpose | Rule |
|---|---|---|
| `URE_URL` | URE API origin | Must be numeric IPv4 loopback, e.g. `http://127.0.0.1:18879`; no path, query, fragment or credentials |
| `URE_API_TOKEN` | URE bearer credential | At least 32 UTF-8 bytes; never store in Git |
| `URE_TIMEOUT` | Per-request timeout | 0 < value ≤ 30 seconds; default 10 |

Without a valid token, `GET /api/rea/status` returns `NOT_CONFIGURED`. Invalid or non-loopback endpoints fail closed. The browser cannot choose the URE host.

The URE service is started separately with its own local state directory. Divine Arsenal does not silently install tools, enable a service, or start a provider.

## 4. Divine Arsenal API

| Method | Route | Purpose |
|---|---|---|
| GET | `/api/rea/status` | Authenticated health, safe adapter summaries and worker capacity |
| GET | `/api/rea/adapters` | Safe adapter registry projection |
| POST | `/api/rea/inputs` | Base64 artifact intake; URE hashes and stores original bytes |
| POST | `/api/rea/jobs` | Submit an allowlisted static profile |
| GET | `/api/rea/jobs/{id}` | Poll safe job state |
| GET | `/api/rea/jobs/{id}/report` | Validate and return evidence-linked report |
| POST | `/api/rea/jobs/{id}/cancel` | Request cancellation through URE controller |

The Divine-to-URE bridge currently accepts a maximum of **700,000 bytes** per file because URE API v1 uses a bounded JSON/base64 request body. URE's local CLI has a larger 16 MiB input limit; larger files should be handled with that local CLI until a reviewed streaming API is available. Divine Arsenal does not invent a filesystem-path endpoint or bypass the API boundary.

## 5. Intake and analysis workflow

1. The user explicitly selects a local file.
2. The browser enforces the 700,000-byte bridge limit and posts its basename and base64 bytes to Divine Arsenal.
3. Divine Arsenal validates the basename and base64, computes SHA-256, and sends the bytes to URE with fixed provenance `divine-arsenal-local-research`.
4. URE returns its own input descriptor. Divine Arsenal requires the returned SHA-256 and byte size to match the submitted bytes.
5. Divine Arsenal presents only profiles supported by the observed file format and currently enabled/available URE adapters.
6. The user explicitly chooses a profile. Divine Arsenal submits the job with `authority=OBSERVE` and a deterministic idempotency key derived from input hash and profile.
7. The UI polls the URE job ID. URE alone owns state transitions and terminal-state reconciliation.
8. On success, Divine Arsenal retrieves the report, verifies the input hash, checks every finding's evidence references and displays findings, evidence hashes and limitations.
9. URE retains original bytes and raw outputs in its private content-addressed stores. Divine Arsenal does not copy those bytes into its Git repository.

A commit, job submission or running process is not a successful analysis. Only a terminal `succeeded` job with a schema-valid report and valid input/evidence references is displayed as completed.

## 6. Profile selection

The UI never exposes URE's synthetic `AUTO` profile. The application maps formats to profiles as follows, then filters against the live URE registry:

| Observed format | Candidate profiles |
|---|---|
| ELF | identify, ELF metadata, Ghidra, radare2, Binwalk, Unblob |
| APK | identify, JADX, Binwalk, Unblob |
| DEX | identify, Kaitai DEX, JADX |
| Java class | identify, JADX |
| Android boot header | identify, Binwalk, Unblob |
| ZIP | identify, Binwalk, Unblob |
| PE | identify, Binwalk, Unblob |
| Unknown | identify, Binwalk, Unblob |
| PDF, PCAP, JSON, UTF-8 text | identify only |

An adapter is offered only when its live descriptor says it is available, enabled and supported. A profile may still be rejected by URE if the service's capability state changes between discovery and submission; the UI surfaces that as a blocked request rather than falling back to host execution.

## 7. Evidence, authority and security

- **OBSERVE:** default and only authority available from Divine Arsenal. The integrated profiles perform bounded static inspection.
- **AUTO:** not exposed by the Divine bridge. URE's synthetic byte fixture is a simulation, not a real analysis.
- **APPROVAL:** no host writes, network access, installation, privileged operations or active instrumentation are granted here.
- **PHYSICAL:** no serial, flashing, sigrok capture, Frida live instrumentation or hardware control is exposed.

The client disables proxies and redirects, accepts only a numeric loopback endpoint, bounds response bodies, rejects malformed JSON, validates SHA-256 values, verifies evidence references and uses fixed API paths. Job responses are allowlisted; internal worker IDs, lease timestamps, fencing tokens and attempt tokens are deliberately removed. Report execution-attempt metadata is not forwarded to the browser.

Evidence labels remain distinct: CLAIM, OBSERVATION, EVIDENCE, VERIFIED FACT, HYPOTHESIS, SIMULATION and UNKNOWN. Static tool output is an OBSERVATION or evidence record, not a runtime-behaviour or vulnerability verdict.

## 8. Supported formats and known limits

URE's conservative classifier currently recognises ELF, PE, APK/ZIP, DEX, Java class, PDF, PCAP, Android boot headers, JSON and UTF-8 text. Unsupported inputs remain UNKNOWN. Classification is signature-based.

PDF recognition does not mean PDF structure extraction. TIFF/JPEG/PNG currently remain UNKNOWN to the URE classifier. There is no OCR/HTR, manuscript transcription, visual image interpretation, universal IIIF parser or scholarly content extraction in this bridge. Those remain Divine Arsenal research-workbench tasks or future adapters. The current URE API limit also makes the bridge unsuitable for large scans and firmware images.

Ghidra, JADX, Binwalk, radare2, Unblob and Kaitai are implemented as explicit URE adapters with pinned/local verification evidence. Frida, PlatformIO and sigrok remain blocked/disabled. Adapter availability is runtime-dependent and is never inferred from a binary merely appearing on PATH.

## 9. Verification status

### Divine Arsenal integration

- Local pre-integration baseline: 131 tests passed.
- New REA integration tests: 11 passed against a purpose-built local fake URE API.
- Combined suite: 142 tests passed.
- Browser static checks: JavaScript syntax valid; 169 unique HTML IDs.
- Tests cover loopback rejection, configuration absence, upload hash reconciliation, profile filtering, OBSERVE-only submission, cancellation, dangling evidence references, report/job input mismatch and removal of internal fencing data.

### URE provider

The private URE workspace records 171 passing tests and local owned-fixture checks for Ghidra, JADX, Binwalk, radare2, Unblob and Kaitai. Its status explicitly does not claim production deployment, distributed Fleet transport, active Frida, PlatformIO flashing, sigrok hardware capture or broad real-world corpus accuracy.

### Remaining release gates

- Run a real same-host Divine → URE end-to-end test against the current URE checkout and live adapter registry.
- Verify service restart, token rotation and clean shutdown behaviour.
- Increase large-file intake only through a separately reviewed bounded streaming API.
- Add scholarly PDF/image parsing only with pinned parsers, rights-aware inputs and synthetic plus lawful real fixtures.
- Keep all public scholarly/source/rights and human-review gates from Research Edition 1.1 open until independently accepted.

**Current state:** application bridge and UI are implemented; fake-service integration tests pass. Production deployment and public release are not claimed.

## 10. Live integration verification — 2026-11-13

**Superseding status note:** the earlier statement in section 9 that live end-to-end testing was pending is superseded by the verified same-host runs below.

The Omarchy URE API was started on IPv4 loopback at port 18879 with a private bearer token outside both repositories. The Divine API called that live service through the actual HTTP client. No fake provider was used for these runs.

| Profile | Input | Terminal result | Observed output |
|---|---|---|---|
| identify | Owned UTF-8 text fixture, 34 bytes | succeeded | text classification; 1 finding; 3 evidence records |
| Ghidra | Local /usr/bin/true ELF, 43,320 bytes | succeeded | 32 functions exported; 1 finding; 3 evidence records |
| JADX | Preserved owned DEX fixture, 580 bytes | succeeded | complete static decompilation; 1 source file and 1 preview; 3 evidence records |
| Kaitai | Same owned DEX fixture | succeeded | 1 class and 2 methods parsed; 1 finding; 3 evidence records |

For every run, the application reconciled the input SHA-256, validated the report's input hash and evidence references, and returned authority OBSERVE. No target program was executed. The Ghidra test read a local system ELF file; the Android tests used the URE repository's owned synthetic DEX fixture.

The URE report builder now has a regression-tested generic limitation that accurately says no runtime behaviour, device control or Fleet transport was performed. The already-running API process retains its previously imported report module until a later controlled restart; Divine Arsenal therefore includes a transparent v1 compatibility normalizer for the legacy generic wording and preserves the original provider wording in provider_limitations.

Profile selection requires live adapter status SUPPORTED, available, enabled and verified. Current verified live identities: identify@1.0.0, ghidra.decompile@1.0.0, kaitai.dex@1.0.0, unblob.scan@1.0.0, radare2.analyze@1.0.0, binwalk.scan@1.0.0 and jadx.decompile@1.0.0. elf.metadata@1.0.0 is present but unverified and is not offered. frida@unreviewed, platformio@unreviewed and sigrok@unreviewed are unavailable and remain hidden from profile selection.

## 11. Adapter-version and report-contract hardening

- Profile-to-adapter resolution is prefix-based and version-aware; only the highest currently available, enabled, verified and supported adapter version is offered.
- The deterministic idempotency key includes input SHA-256, profile and resolved adapter identity. A Ghidra/JADX/etc. adapter version change therefore cannot silently reuse an earlier result.
- The returned job adapter identity must equal the identity resolved from the live registry at submission time; a registry race fails closed.
- Evidence records require valid SHA-256 values and string kinds. Findings and reconstructions must reference evidence hashes present in the report. Reconstruction output must also carry a valid output SHA-256.
- The browser smoke now drives the real REA page through file selection, local ingest, profile selection, job completion and report rendering. The captured page is docs/execution/evidence/rea-analysis.png.
## 12. Notebook and provenance-graph integration

Successful jobs can be saved explicitly through `POST /api/rea/jobs/{job_id}/notebook` as a revisioned `analysis-reference` document. The save operation is idempotent by job ID and preserves:

- stable job ID, input SHA-256, profile, adapter/version, OBSERVE authority and permissions;
- created/started/finished timestamps, attempt count, terminal state, exit code and timeout/truncation/cancellation/reaping flags;
- sandbox profile, network/filesystem policy and declared adapter resource limits;
- raw evidence SHA-256 references, derived findings, reconstruction hypotheses and provider limitations;
- optional registered-source link, rights status UNKNOWN, review state UNREVIEWED by default and a separate human note.

The notebook stores references and derived summaries, not raw input bytes, raw stdout/stderr, worker IDs, attempt tokens, leases or fencing tokens. All finding/reconstruction evidence references must resolve to evidence hashes in the same report. A linked analysis appears in the Tradition Graph as an OBSERVATION edge from the selected source to a local analysis node. This edge documents a tool operation only; it is not a historical relationship or influence claim. A user can later mark the record HUMAN_REVIEWED or DISPUTED without changing the immutable analysis fields.
