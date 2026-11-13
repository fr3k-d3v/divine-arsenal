# Divine Arsenal animation assets

This is the canonical binary asset catalogue for Divine Arsenal.

## Layout

```text
assets/animations/
  manifest.json          # Library catalogue, provenance and processing-set metadata
  binary-manifest.json   # SHA-256, byte count and exact path for all 132 binaries
  BUNDLE_README.md       # Original transfer-bundle notes
  TRANSFER_RECEIPT.md    # Integrity and transfer evidence
  source/
    gif/                 # Original/non-derivative GIF sources
    mp4/                 # Original and combined MP4 sources
  derived/
    gif/                 # Doubled-FPS and 24fps/5s GIF derivatives
    mp4/                 # 24fps/5s MP4 derivatives (timing authority)
```

## Inventory

- 99 GIF files
- 33 MP4 files
- 132 binary files total
- 348,889,575 bytes before Git LFS pointer storage

## Current ingestion state

All 132 media binaries are present on Omarchy and pass SHA-256 verification. GitHub LFS publication is pending the commit and remote object verification; see TRANSFER_RECEIPT.md.

## Git policy

All media payloads are tracked with Git LFS. Keep source assets immutable; derivatives must retain a stable mapping to their source in binary-manifest.json. Do not commit transfer chunks or temporary archives.

## Verification

Every binary has a SHA-256 in binary-manifest.json. The original transfer archive SHA-256 is recorded in manifest.json under binary_ingest. A file is considered GitHub-published only after the LFS push succeeds and a fresh fetch of the branch confirms the expected pointer objects.
