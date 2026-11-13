# FR3K Ten-Style AI Keyframe Animation Workflow

Status: **documented, reproducible pipeline specification**. Last observed run: 2026-11-13. This is an animation-production recipe for Divine Arsenal visual assets, **not** a production integration, shipped feature, or evidence of independent AI rendering of every video frame.

## Scope and design constraints

Generate **ten distinct animated styles**, each in **native landscape composition (16:9)** and **native portrait composition (9:16)**. A square image centered in black, blurred side extensions, and stretched portrait-to-landscape frames **fail** the art-direction gate. Keep the supplied emblem/wordmark **geometrically consistent and legible** throughout. Never replace the Divine Arsenal mark with FR3K branding in Divine Arsenal deliverables: use this workflow with an approved Divine Arsenal logo/asset, keeping FR3K samples as references only.

| Order | Style | Required distinctive effect |
| --- | --- | --- |
| 1 | Liquid Chrome | reflective liquid-metal sheets, flowing specular highlights |
| 2 | Neon Ripple Field | magenta/cyan concentric wavefronts and interference |
| 3 | Aurora Flow | green/teal aurora curtains and sweeping luminous ribbons |
| 4 | Nebula Whirlpool | purple-blue starfields, swirling plasma and cosmic dust |
| 5 | Magma Bloom | molten red/orange lava blossoms and expanding thermal cracks |
| 6 | Solar Vortex | fiery corona, golden plasma arcs and orbiting flares |
| 7 | Cosmic Emblem | celestial rays, galaxy filaments and crystalline glow |
| 8 | Green Slime | vivid acid-green viscous liquid, drips, bubbles and splashes |
| 9 | Electric Blue | branching blue lightning, electric arcs and pulses |
| 10 | Water Vortex | liquid-blue rotating wave, droplets, bubbles and caustics |

## AI generation contract

For **each** style and **each** orientation, independently generate a short sequence of **nine consecutive AI-rendered keyframes**, retaining stable logo geometry, consistent camera/framing and recognizable motion across frames. Generate 16:9 imagery **as widescreen imagery**; generate 9:16 imagery **as portrait imagery**. Do not reuse one orientation by stretching or blurred filling. Include explicit beginning/end continuity where possible for seamless loops. Verify exact logo spelling and geometry visually. If an AI tool distorts the emblem, regenerate that style rather than silently compositing an unrelated symbol.

**Important provenance:** nine AI keyframes per clip are **not** 144 independent AI-generated frames. The remaining 135 video frames are optical-flow interpolations. The previous delivered widescreen run reused available landscape AI keyframes; some were 4:3 landscape sources cropped to 16:9. That is an observed compromise, **not** the native-16:9 gold standard. Some of the seven original styles also reused cosmic/solar material and therefore need art-direction review before claiming strong differentiation.

## Exact observed video assembly settings

- Per style: 9 AI keyframes, 16 output frames per keyframe interval, including the last-to-first transition = **144 video frames**.
- Frame rate: **24 FPS**, therefore **6 seconds** per style.
- Ten-style collection: **1,440 frames**, **60 seconds**.
- Preview interpolation working size: **640 × 360** for widescreen, **360 × 640** for portrait.
- Export: **1920 × 1080** (16:9) or **1080 × 1920** (9:16), H.264, yuv420p, +faststart. These resolutions are **upscaled exports**, not proof of native-resolution AI rendering.
- Optical flow: OpenCV `cv2.DISOpticalFlow_create(cv2.DISOPTICAL_FLOW_PRESET_FAST)`. Compute forward and reverse flows for adjacent keyframes; remap each frame toward the other and blend by `t=k/16`, for `k=0..15`. Include the frame-9 → frame-1 wrap.
- Resize keyframes with Lanczos, **preserve aspect ratio** and center-crop only if source is already in the correct orientation. Do not stretch. Native orientation-specific keyframes are preferred over any crop.
- Encode per-style previews with ffmpeg raw `bgr24` input at 24 FPS, `libx264`, `-pix_fmt yuv420p`, `-movflags +faststart`.
- Widescreen observed final upscale: `-vf scale=1920:1080:flags=lanczos,unsharp=3:3:0.30:3:3:0,setsar=1 -c:v libx264 -preset veryfast -crf 23 -pix_fmt yuv420p -movflags +faststart`.
- Portrait observed final upscale: `-vf scale=1080:1920:flags=lanczos,unsharp=3:3:0.35:3:3:0,setsar=1 -c:v libx264 -preset veryfast -crf 22 -pix_fmt yuv420p -movflags +faststart`.
- Join ten matching streams using an ffmpeg concat-demuxer file and `-f concat -safe 0 -i concat.txt -c copy -movflags +faststart combined.mp4`.
- Package individual MP4 files into a ZIP separately; always also provide the **direct combined MP4**, since ZIP delivery was inconvenient on Android.

## Source mapping from observed FR3K widescreen run

The following local file names were used as landscape keyframe sources in the observed widescreen render; **these are not committed assets**:

```text
Liquid_Chrome       animated_fr3k_cosmic_logo.png
Neon_Ripple_Field   animated_fr3k_nebula_vortex_grid.png
Aurora_Flow         neon_fr3k_nebula_animation.png
Nebula_Whirlpool    animated_fr3k_nebula_logo.png
Magma_Bloom         animated_fiery_fr3k_solar_emblem.png
Solar_Vortex        fiery_fr3k_sun_logo_animation.png
Cosmic_Emblem       animated_fr3k_solar_nebula_logo.png
Green_Slime         fr3k_toxic_slime_vortex_animation.png
Electric_Blue       electric_fr3k_lightning_vortex_grid.png
Water_Vortex        fr3k_underwater_vortex_animation.png
```

This source mapping records what was **actually rendered**, not a claim that each image is an ideal representation of its named style. For Divine Arsenal, generate or supply separately approved imagery and track asset IDs, hashes, prompt briefs, model, date and provenance in its asset manifest.

## Verification gates

1. Check all ten outputs exist and are independently viewable; count exactly 144 frames per style and 1,440 frames in the combined collection with `ffprobe -count_frames`.
2. Confirm 24 FPS, six seconds per style, 60 seconds combined, 16:9 or 9:16 pixel dimensions, and no letterboxing.
3. Inspect representative first/middle/last frames, the transition between styles, and the loop seam for tearing, ghosting, logo deformation, incorrect text and camera jumps.
4. Inspect distinctness: slime must look viscous, electricity must have branching arcs, water must show fluid dynamics, etc. Do **not** pass recolored cosmic backgrounds as genuinely distinct styles.
5. Report keyframes separately from interpolated frames and report upscaled exports separately from native-resolution AI generations.
6. Avoid publishing generated assets until licensing, trademark/branding and any sensitive-source checks are satisfied. Keep private user profiles out of the public repo.
7. If the project requires a native-resolution, per-frame AI master, treat that as **future work** and do not promote this interpolation workflow as equivalent.

## Reuse inside Divine Arsenal

Use this document as an art-generation instruction for the Divine Arsenal visual pipeline. Substitute the approved Divine Arsenal iconography, palette and scene concepts while retaining ten-style structure, output sizes, duration, motion and verification gates. Work in a feature branch/PR under existing repository governance. Save finished approved asset manifests and reproducible commands to GitHub; large video binaries should use an approved artifact store with durable links and hashes rather than assuming chat sandbox files are durable.

**Observed verification of latest widescreen FR3K combined file (local only):** `1920x1080`, `24/1 FPS`, `1440 frames`, `60.000000 seconds`, approximately 45.3 MB. The original portrait combined video was separately delivered as `1080x1920`, 60 seconds.
