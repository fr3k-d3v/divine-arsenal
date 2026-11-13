# Recovered REVERSE ENGINEER ANYTHING workspace — inventory

**Evidence date:** 2026-11-12
**Mode:** OBSERVE; static repository inspection only
**Machine-readable register:** [rea-repository-register.json](rea-repository-register.json)

## Executive summary

The preserved audit records **29/29 public source checkouts** as locally accessible at the time of inspection. Their local origin identities and 40-character HEADs were read and matched against the recovered workspace naming. **28 checkouts had no tracked changes; onekey-sec/unblob had 54 tracked changes** in ROMFS test-output fixtures. Untracked files were excluded from the audit and remain UNKNOWN.

No recovered repository code, build, installer, binary, MCP server, APK, firmware image or skill was executed. No source-drive writes were made. This is a historical local snapshot, not an upstream freshness or authenticity check.

The current integration pass generated this register from the preserved machine-readable audit in the private URE workspace. The original recovered snapshot was not re-read during this pass; its expected workspace was not present in the previously observed mount directory.

## Candidate groups and decisions

- **REA core and orchestration:** morluto/rea is retained as a contract/reference source only. Divine Arsenal does not import its broad MCP/browser/native/PTY orchestration surface or create a second scheduler. leantoken, flameox and smokinggun are deferred for their distinct source-indexing, runtime-profiling and source-complexity roles. Forks and independent orchestration agents are deferred or rejected where they duplicate the authoritative engine or have broad authority.
- **Firmware and containers:** onekey-sec/unblob is a candidate only after provenance reconciliation and sandbox quotas; the preserved checkout had 54 tracked fixture changes. The Binwalk MCP candidate is blocked by missing root licence evidence and extraction/tool verification. slopwise has a claimed MIT label but no licence file. Kaitai's repository is an umbrella; compiler, runtime and schema component licensing must be evaluated separately.
- **Native binaries:** Ghidra MCP variants are not copied; their scripting/network surfaces and missing licence evidence make a direct, bounded headless adapter preferable. BinExport is deferred. The radareorg MCP wrapper is preferred over the non-commercial fork as a reference, but Divine Arsenal consumes the independently verified URE static adapter rather than importing the MCP wrapper.
- **Android:** duplicate JADX MCP servers are deferred; the URE engine has its own pinned JADX CLI adapter. Frida integrations remain disabled because active instrumentation requires separate APPROVAL and PHYSICAL authority. revoid is a duplicate wrapper candidate and remains deferred.
- **Hardware and protocols:** sigrok, PlatformIO and logic-analyser projects remain disabled/deferred. Physical capture, serial access, flashing and live instrumentation are not granted by this integration.
- **Reconstruction and AI workflows:** Palimpsest is MIT-observed but deferred; generated reconstructions remain HYPOTHESIS until independently checked. The separate reverse-engineering-agent project is rejected as a duplicate orchestrator with broad execution authority and missing licence evidence.

## Repository register

| Repository | Candidate | Observed HEAD | Licence observation | Tracked status | Integration decision |
|---|---|---|---|---|---|
| 1013503897/jadx-headless-mcp | JADX static | c9d8408fc90b | Apache-2.0 | TRACKED_CLEAN | Candidate reference only; prefer existing P4 worker and installed verified CLI. |
| abd3lraouf-studios/binexport-ghidra-12 | Function export | 1f8511e7dc9f | Apache-2.0 | TRACKED_CLEAN | Defer pending installed Ghidra validation and P6 need. |
| Cossack9989/binwalk-mcp-server | Firmware | e70298a33756 | UNKNOWN | TRACKED_CLEAN | BLOCKED license and tool/extraction verification. |
| drazisil/ghidra-mcp | Ghidra | d77c40f2a2a6 | UNKNOWN | TRACKED_CLEAN | Defer missing license; existing P1/P5 direct headless path preferred. |
| drvcvt/radare2-mcp | radare/Rizin | 4d3075946928 | CC-BY-NC-SA-4.0 | TRACKED_CLEAN | BLOCKED licensing review; prefer radareorg candidate if needed. |
| gmihai2109/reverse-engeeneer-anything | REA fork | d2aed172ab79 | MIT | TRACKED_CLEAN | Defer duplicate fork; no evidence it is preferable to original. |
| Hao17/LiteGhidraMCP | Ghidra | ca5ccd768bc8 | UNKNOWN | TRACKED_CLEAN | Reject broad scripting bridge for initial read-only adapter. |
| jguy/sigrok-skill | Signals workflow | 51f9223935cf | MIT | TRACKED_CLEAN | Read-only workflow reference; do not invoke recovered skill. |
| JINGQINLIN/Palimpsest | Reconstruction | acd9ce902795 | MIT | TRACKED_CLEAN | Defer; reconstructions remain HYPOTHESIS. |
| jl-codes/platformio-mcp | Embedded build | f3928e8bc40f | MIT | TRACKED_CLEAN | Disabled; physical/build authorization and isolated toolchain needed. |
| kaitai-io/kaitai_struct | Binary format umbrella | 4fb24924d213 | UNKNOWN at umbrella | TRACKED_CLEAN | BLOCKED component/license provenance; not an installed compiler. |
| KenosInc/sigrok-mcp-server | Signals | 71a652dcae5a | MIT | TRACKED_CLEAN | Defer physical capture; future offline decode only after tool review. |
| Kyworn/slopwise | Firmware diff | 3b4ceec5f3f4 | CLAIM MIT; no license file | TRACKED_CLEAN | BLOCKED license text; prefer P6 structural diff fixture design. |
| lassebm/web-logic-analyzer | Signals viewer | 8d354c9fb494 | MIT | TRACKED_CLEAN | Defer UI/physical paths; possible offline capture viewer later. |
| monte1440/ghidra-mcp | Ghidra | 092afdb1f446 | UNKNOWN | TRACKED_CLEAN | Defer overlapping bridge; missing license and unnecessary network surface. |
| morluto/flameox | Runtime profiling | c7ea167bf51b | MIT | TRACKED_CLEAN | Disabled for this static milestone; active instrumentation separately gated. |
| morluto/leantoken | Source indexing | 5cfab83047d4 | MIT OR Apache-2.0 | TRACKED_CLEAN | Defer; context indexing not required for static artifact analysis. |
| morluto/rea | REA core | edf46248f2a4 | MIT | TRACKED_CLEAN | Reference contracts only; no second scheduler or broad MCP transplant. Prior sync ancestry unresolved. |
| morluto/smokinggun | Source complexity | cf3a3872a263 | MIT | TRACKED_CLEAN | Defer; source complexity separate from binary analysis. |
| neeetman/frida-mcp | Instrumentation | 18d2ac715e9b | UNKNOWN | TRACKED_CLEAN | BLOCKED license; disabled active instrumentation. |
| onekey-sec/unblob | Firmware extraction | a902ee6dfa14 | MIT | TRACKED_MODIFIED_54 | Candidate only after provenance reconciliation and sandbox quotas; no recovered runtime execution. |
| Qtty/jadx-mcp-server | JADX static | 4e6d890d1d37 | UNKNOWN | TRACKED_CLEAN | Defer duplicate persistent server; missing license. |
| radareorg/radare2-mcp | Native static | 562c0cf23c42 | MIT wrapper | TRACKED_CLEAN | Preferred radare wrapper reference over NC fork; direct read-only CLI adapter first; still disabled. |
| rea-tools/rea | REA alternate source | 7fa2864e68a3 | MIT text; relationship UNKNOWN | TRACKED_CLEAN | BLOCKED independent provenance; do not treat as official release. |
| Samael-Z/jadx-headless-mcp | JADX static | 866505a14827 | UNKNOWN | TRACKED_CLEAN | Defer duplicate server; missing license. |
| samudoria/revoid | JADX static | 712af7ed816e | UNKNOWN | TRACKED_CLEAN | Defer duplicate wrapper; missing license. |
| The-Arabi/Reverse-engineering-agent | Agent orchestration | c16af7d5c25f | UNKNOWN | TRACKED_CLEAN | Reject duplicate orchestrator; missing license and broad authority. |
| yfe404/frida-mcp | Instrumentation | fb7d6c7c74bd | UNKNOWN | TRACKED_CLEAN | BLOCKED license and active instrumentation authority. |
| zhuyumi123/REA | REA fork | 7aa4d768eb15 | MIT | TRACKED_CLEAN | Defer fork duplication; no proven unique safe adapter need. |

## Evidence and limitations

- Preserved audit identity check: VERIFIED: all 29 normalized local origin URLs match recovered owner/repository directory identity and clone manifest naming; 40-character HEAD read locally..
- The clone manifest and its evidence digest are recorded in plan_evidence. Per-checkout saved manifest digests were not available and are explicitly UNKNOWN.
- Licence status reflects local licence-file observations only. It does not establish complete transitive licence obligations, provenance authenticity, redistribution permission or legal advice.
- Upstream freshness, releases, advisories and maintenance state were not checked; those fields remain UNKNOWN.
- The 54 unblob tracked changes are not interpreted as source defects. The audit notes they may be content or mode differences.
- Detailed README hashes, dependency manifests, licence-file hashes, source-sample hashes and risk-surface file lists are preserved per repository in the JSON register.
- The source audit is a candidate-selection input. Actual URE adapters are separately implemented, pinned, sandboxed and tested; Divine Arsenal does not execute the recovered checkouts.
