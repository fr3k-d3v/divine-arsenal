# Divine Arsenal animation workflow

**Status:** reproducible workflow documented; binary media ingest is tracked separately in `assets/animations/manifest.json`.
**Repository branch:** `feat/source-atlas-psalms-visuals`
**Scope:** AI-authored frame-by-frame motion, spritesheet extraction, GIF/MP4 encoding, and 24 fps / 5-second normalization.

## Two different operations — do not conflate them

### A. Create real motion with AI-generated frames

The motion in the original tests came from the AI-generated frames, not from FFmpeg.

Recovered test descriptions:

1. **9-frame test:** a kneeling figure, moving robes and changing light.
2. **12-frame test:** a figure rising and raising an arm toward a neon cross.

The workflow was:

1. Use the approved still artwork as the visual reference.
2. Generate a new, uniform spritesheet in which every cell is a sequential animation frame.
3. Slice the sheet into individual frames in row-major order.
4. Encode those frames into a source GIF and/or MP4.
5. Inspect the animation for actual subject movement, frame continuity and unwanted jumps.

Use `scripts/slice_spritesheet.py` to extract the cells. The historical frame-encoding FPS for the two early tests was not retained; set it explicitly rather than inventing a value.

**Important project boundary:** the static Source Atlas / editorial image batch in `docs/design/EXTERNAL_IMAGE_GENERATION_BRIEF.md` still requires one independent image per asset and prohibits sprite sheets as final art deliverables. This animation workflow is a separate, explicitly requested production path. The spritesheet is an intermediate frame container, never the final UI asset.

### B. Interpolate an existing animated GIF to 24 fps and 5 seconds

This is the workflow used for the numbered exports in this session. It starts with an already animated GIF.

1. Read the source GIF's actual frame count, canvas size and cumulative frame duration.
2. Retiming factor = `5000 ms / source duration ms`.
3. Loop the source once for temporal context at the cycle boundary.
4. Apply FFmpeg `minterpolate` motion-compensated interpolation at 24 fps.
5. Trim to exactly 5.000 seconds and encode 120 frames as H.264 MP4.
6. Derive a GIF from that MP4 using a generated palette.
7. Re-time the 120 GIF frames with a 40/50 ms delay pattern. GIF stores delays in 10 ms units, so this pattern gives an average of 24 fps over each 12-frame / 500 ms block.
8. Verify the MP4 with `ffprobe` and the GIF with Pillow.

Install the optional Pillow dependency into the project environment, then run:

```bash
uv pip install --python .venv/bin/python -r scripts/requirements-animation.txt
.venv/bin/python scripts/interpolate_gif_24fps_5s.py input.gif --output-dir output
```

Outputs:

- `<input>_interpolated_24fps_5s.mp4` — authoritative constant-frame-rate deliverable.
- `<input>_interpolated_24fps_5s.gif` — looping preview / portable animated image.

### What “make it 5 seconds” means in this exact implementation

The pipeline normalizes one source cycle to five seconds. It stretches sources shorter than five seconds and speeds up sources longer than five seconds. It does **not** invent new semantic action, extend the scene with a new AI-generated continuation, or add a freeze-frame tail.

Example evidence from the numbered batch:

- IDs 1664–1680 that were present in the session: 12 source frames over 2.880 seconds; normalized to 120 output frames over 5.000 seconds.
- ID 1682: 48 source frames over 5.760 seconds; normalized down to 5.000 seconds. It was shortened, not extended.
- IDs 1673 and 1681 were not present in the session export set or the Library inventory slice used for this record. Their status remains **UNKNOWN**, not assumed generated or missing globally.

### Exact processing settings

| Setting | Value |
|---|---|
| Target MP4 frame rate | 24/1 fps constant |
| Target duration | 5.000 s |
| Target MP4 frames | 120 |
| Interpolation | FFmpeg `minterpolate`, MCI, AOBMC, bidirectional motion estimation, variable-size block compensation |
| MP4 codec | H.264 / libx264 |
| Preset / CRF | medium / 18 |
| Pixel format | yuv420p |
| Audio | none |
| MP4 fast start | enabled |
| GIF frames | 120 |
| GIF delay pattern | 40 ms for 10 frames + 50 ms for 2 frames, repeated 10 times |
| GIF loop | infinite |
| GIF palette | palettegen + paletteuse, Sierra2_4A dithering |

The MP4 is the timing authority. GIF frame delays are quantized to 10 ms and therefore approximate 24 fps on average; they cannot represent a uniform 41.666… ms delay per frame.

### Exact FFmpeg filter chain

```text
setpts=PTS*<5000/source_duration_ms>,
minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,
trim=duration=5,
setpts=PTS-STARTPTS,
pad=ceil(iw/2)*2:ceil(ih/2)*2
```

The executable implementation is in `scripts/interpolate_gif_24fps_5s.py`. It records actual source and output dimensions; do not assume the H.264 canvas will always be identical to an odd-sized source canvas.

## Reproducibility and verification

For every asset, retain:

- original source GIF (never overwrite it);
- final MP4;
- final GIF;
- source and output dimensions;
- source frame count and cumulative duration;
- output frame count, FPS and duration;
- SHA-256 for every binary;
- processing script version and FFmpeg / ffprobe version;
- visual QA status and known interpolation artifacts.

Minimum machine checks:

```bash
ffprobe -v error -select_streams v:0 \\
  -show_entries stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration \\
  -of json output.mp4
```

Expected MP4: `r_frame_rate=24/1`, `avg_frame_rate=24/1`, `nb_frames=120`, `duration=5.000000`.

Expected GIF: 120 frames and cumulative duration 5000 ms.

Machine verification does not prove visual quality. Inspect fast edges, thin geometry, text-like glyphs, hands, robes, lightning and loop seams for interpolation warping or ghosting.

## Asset preservation / Git policy

- Keep source and derived files side by side in the asset catalogue; never replace originals with interpolated derivatives.
- Use Git LFS for large GIF/MP4 payloads. Commit the manifest and processing source as ordinary Git files.
- Keep a stable asset ID and explicit source-to-output mapping.
- The manifest records a Library inventory and session-export metadata. A catalogue entry is **not** proof that its binary payload has been committed.
- Do not commit private Library IDs, user data, credentials or unrelated local files.
- Do not claim the media binaries are in Git until the actual binary paths are present in the commit and verified by fetching them back.

## Provenance note

The earlier 9-frame and 12-frame test descriptions are recovered from the user's conversation. The exact original natural-language generation prompts and original extraction/encoding FPS were not retained verbatim. The companion prompt document is therefore labelled a **reconstructed reusable prompt**, not a verbatim historical prompt.
