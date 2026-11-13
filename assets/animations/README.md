# Divine Arsenal animation assets

This directory is the canonical landing zone for generated animation sources and derivatives.

## Layout

```text
assets/animations/
  README.md
  manifest.json
  source/       # original GIFs and original spritesheet masters
  gif/          # final 24 fps / 5 s GIFs
  mp4/          # final 24 fps / 5 s MP4s (timing authority)
```

## Ingest rules

1. Preserve source files unchanged.
2. Keep source and derived filenames linked by stable asset ID.
3. Record SHA-256, dimensions, frame count, duration and source relationship in `manifest.json`.
4. Use Git LFS for GIF/MP4 payloads; keep scripts, docs and manifests in ordinary Git.
5. Never mark a payload as committed until the binary exists in this repository and has been fetched back for verification.

## Current state

- The manifest catalogs **99 GIF assets** visible in the ChatGPT Library inventory for 2026-11-13 from 09:00 UTC onward.
- It also records **17 numbered source-to-output processing sets** (1664–1682, excluding 1673 and 1681) observed in the current session.
- **Binary ingest is pending.** This documentation commit does not contain the GIF/MP4 payloads. The manifest explicitly marks this distinction; do not treat catalogue metadata as media storage.
