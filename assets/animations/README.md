# Divine Arsenal animation assets

This is the canonical binary asset catalogue for Divine Arsenal.

## Layout

```text
assets/animations/
  manifest.json          # Library catalogue, provenance and processing-set metadata
  binary-manifest.json   # SHA-256, byte count and exact path for all 132 binaries
  BUNDLE_README.md       # Original transfer-bundle notes
  TRANSFER_RECEIPT.md    # Integrity, Git LFS and remote verification evidence
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
- 348,889,575 bytes of media
- Git LFS stores 107 unique objects (duplicate content is deduplicated)

## Publication status

All 132 media files are committed on the feat/source-atlas-psalms-visuals branch and published through Git LFS. The remote branch SHA matches the local commit. All 132 GitHub LFS pointer files were fetched through the GitHub Contents API and their OID SHA-256 and byte size matched binary-manifest.json.

## Git policy

All media payloads are tracked with Git LFS. Keep source assets immutable; derivatives must retain a stable mapping to their source in binary-manifest.json. Do not commit transfer chunks or temporary archives.

## Verification

See TRANSFER_RECEIPT.md for the archive hash, individual file hashes, LFS upload result and remote pointer verification.
