# Recovered REVERSE ENGINEER ANYTHING workspace — integration directive

**Observed on:** Omarchy, 2026-11-12  
**Source volume:** Samsung PM9A1 NVMe 2TB, serial S65XNE0R308741, exposed as /dev/sde via Realtek RTL9210 USB bridge.  
**Filesystem:** Btrfs, UUID 304325bc-fd3e-4e3e-9bb9-b1a47aaf5dc7.  
**Mounted source path:** /run/media/fr3k/304325bc-fd3e-4e3e-9bb9-b1a47aaf5dc7  
**Recovered home:** @home/parrot  
**Exact project path:** @home/parrot/Desktop/REVERSE ENGINEER ANYTHING  
**Access note:** desktop automounter mounted the source read-write. An attempt to remount read-only via sudo was blocked by Desktop Commander no-new-privileges. All actions so far have been listing/reading only; no source files have been changed. Treat this source as immutable. Do not install or execute code from it. Do not change mount settings or write to the drive.

## Inventory observed

Workspace root contains:
- README.md
- CLONE_MANIFEST.tsv
- clone-repos.sh
- BLACKWAVE_FLEET_UNIVERSAL_INTEGRATION_AUDIT_2026-10-12.md
- research/REPOS_AND_INTEGRATION_PLAN.md
- research/CONTABO_INTEGRATION_PLAN_2026-10-26.md
- logs/ (clone results, clone output, benchmark cleanup audit)
- repos/ (29 cloned repositories)

README states 29/29 public source checkouts cloned, origin URLs and full HEAD SHAs verified; 29 OK, 0 failed; approximately 309 MiB source checkout size; no software installed or executed from those repositories. This is a historical statement in README, not a fresh re-verification of all 29 SHAs.

The 29 repo names:
1. morluto/rea
2. onekey-sec/unblob
3. kaitai-io/kaitai_struct
4. drazisil/ghidra-mcp
5. Kyworn/slopwise
6. Cossack9989/binwalk-mcp-server
7. abd3lraouf-studios/binexport-ghidra-12
8. 1013503897/jadx-headless-mcp
9. yfe404/frida-mcp
10. KenosInc/sigrok-mcp-server
11. radareorg/radare2-mcp
12. morluto/leantoken
13. morluto/flameox
14. morluto/smokinggun
15. JINGQINLIN/Palimpsest
16. monte1440/ghidra-mcp
17. Hao17/LiteGhidraMCP
18. drvcvt/radare2-mcp
19. neeetman/frida-mcp
20. samudoria/revoid
21. Samael-Z/jadx-headless-mcp
22. Qtty/jadx-mcp-server
23. jl-codes/platformio-mcp
24. lassebm/web-logic-analyzer
25. jguy/sigrok-skill
26. The-Arabi/Reverse-engineering-agent
27. zhuyumi123/REA
28. gmihai2109/reverse-engeeneer-anything
29. rea-tools/rea

Important existing research:
- research/REPOS_AND_INTEGRATION_PLAN.md
- research/CONTABO_INTEGRATION_PLAN_2026-10-26.md
- BLACKWAVE_FLEET_UNIVERSAL_INTEGRATION_AUDIT_2026-10-12.md

Related local evidence found outside the named folder:
- @home/parrot/.local/share/fr3k/rea-doctor/doctor-20261024T150021Z.json
- @home/parrot/.local/share/fr3k/rea-doctor/doctor-20261024T150021Z.stderr
- @home/parrot/.local/share/fr3k/rea-doctor/setup-opencode-hermes-plan.json
- @home/parrot/.local/share/fr3k/rea-doctor/setup-opencode-hermes-plan.stderr
- @home/parrot/fr3k-lab/fr3k-reverse-engineering (separate Git repository; inspect only after separate bounded scope approval or include in read-only inventory as related workspace).

## Required work for Divine Arsenal

1. Immediately inspect both research plans and the Blackwave audit, then produce `docs/research/REA_WORKSPACE_INVENTORY.md` and `docs/research/REA_INTEGRATION_ARCHITECTURE.md`.
2. Create a machine-readable `docs/research/rea-repository-register.json` with all 29 repositories, upstream URL, category, local path, saved manifest SHA, observed local HEAD, dirty status, license status, purpose, capability tags, security risk, maintenance state and integration decision. Do not guess missing values; use UNKNOWN.
3. Compare each candidate's real README, package manifests, source entrypoints and licence files. Static inspection only. Do not execute install scripts, binaries, MCP servers or repository code from the recovered disk.
4. Group capabilities:
   - Core orchestration: morluto/rea, its companions leantoken/flameox/smokinggun; inspect fork divergence before choosing a base.
   - Firmware/container extraction: unblob, binwalk MCP, Kaitai Struct.
   - Native reverse engineering: Ghidra MCP variants, BinExport, radare2 MCP variants.
   - Android: JADX headless MCP variants, Frida MCP variants, revoid.
   - Hardware/protocol: sigrok MCP, sigrok skill, web logic analyzer, PlatformIO MCP.
   - AI reconstruction/workflow: Palimpsest and independent reverse-engineering agent projects.
5. Select adapters based on evidence, not repo count or novelty. Record duplicate/overlapping tools and why one is preferred. Check upstream licences, transitive dependencies, release provenance and security advisories before execution/integration.
6. Design a capability registry and job pipeline inside Divine Arsenal:
   ingest -> identify -> hash -> classify -> select adapter -> sandbox -> execute with declared permissions -> capture raw evidence -> parse -> compare hypotheses -> human verify -> provenance graph -> export.
7. Every analysis job needs stable ID, input SHA-256, adapter/version, sandbox profile, permissions, start/end, resource limits, raw output references, derived results, errors and immutable terminal state.
8. Authority levels: OBSERVE default; AUTO only inside disposable nonprivileged sandbox; APPROVAL for host writes/network/privileged access; PHYSICAL for explicit hardware interaction only. Analysis of unknown binaries must never auto-execute them.
9. Build a reusable, isolated REA worker interface. Prefer adapter plugins or MCP bridges with strict schemas over copying entire upstream repos into Divine Arsenal. Keep third-party code separate and attribution/licensing clear.
10. Divine Arsenal's first integration targets should be scholarly artefacts (PDF, TIFF/JPEG, TEI, IIIF, structured text, grids) and locally owned firmware/APKs. This allows shared provenance and analysis capabilities without coupling occult interpretation to binary execution.
11. For FR3K fleet, make the REA capability service separately deployable and reusable; Divine Arsenal consumes it through a read-only analysis API initially. Do not let this project mutate Omarchy/Contabo/phone hardware or fleet authority.
12. No raw repo mirror or user-specific machine data in public GitHub. Public repo gets authored inventory/architecture, upstream URLs, licence metadata and reproducible integration instructions only. Do not commit proprietary/private code or secrets.

## Immediate first-pass priorities

- Read the 2 research plans and audit document.
- Read README and package.json/server.json/entrypoint/licence for each of 29 repos.
- Inspect saved clone log and manifest for historical SHA data.
- Generate a table with all 29 and status values; note current HEAD only if actually read from git metadata.
- Prioritise REA upstream + core companions, then unblob/Kaitai, Ghidra/radare2, JADX/Frida, sigrok/PlatformIO.
- Do not execute any repository until user approves a separate sandbox execution phase.

This is a newly discovered high-priority dependency and must be incorporated into the current Research Edition 1.1 plan and acceptance matrix. Continue all other independent Divine Arsenal tasks while inventorying it.