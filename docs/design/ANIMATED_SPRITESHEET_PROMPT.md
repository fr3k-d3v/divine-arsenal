# Reconstructed reusable prompt — AI frame-by-frame animation spritesheet

**Prompt provenance:** reconstruction from the recovered workflow description. The exact historical prompt text was not retained. Do not cite this as a verbatim transcript.

## Master prompt

Use the supplied reference artwork as the visual and identity anchor. Create a **single, clean, frame-by-frame animation spritesheet** showing one continuous action over sequential frames.

**Frame layout**
- For 9 frames: 3 rows × 3 columns.
- For 12 frames: 3 rows × 4 columns.
- Every cell must have identical width and height.
- Reading order is left-to-right, then top-to-bottom.
- No margins, gutters, borders, cell numbers, captions, labels or watermarks.
- Keep the entire subject inside every cell; do not crop limbs, props or important scene elements at cell boundaries.

**Continuity**
- Preserve the same subject identity, silhouette, clothing, proportions, materials, lighting palette, camera position, lens perspective and background across all frames.
- Keep stationary environmental elements stationary unless their movement is part of the action.
- Do not redesign the subject between frames.
- Make each frame a genuine temporal continuation of the previous one, not a set of unrelated poses.
- Movement must be visible in the subject or environment; do not rely only on a colour shift, glow change or camera shake.
- Distribute motion across the sequence. Use small, coherent transitions between adjacent frames.
- Avoid abrupt jumps, duplicate frames, morphing anatomy, extra limbs, changing props and inconsistent geometry.
- If the animation is intended to loop, make the final frame visually compatible with the first frame.

**Motion brief**
[INSERT THE SPECIFIC ACTION HERE. Describe what moves, direction, timing, intensity and what remains stationary.]

**Visual treatment**
Retain the reference artwork's original art direction, colour palette, texture, atmosphere and level of detail. Render every cell at the same resolution and with consistent exposure and sharpness. The result must read as one animation when the cells are played in order.

Return only the spritesheet. Do not return a collage of different scenes or a contact sheet of unrelated images.

## Recovered test briefs

### Test 1 — 9 frames

A kneeling figure remains recognisable and compositionally consistent. Show a gradual sequence of the robes moving naturally while the surrounding light changes and breathes. The robe motion and light evolution must be visible across multiple frames; do not reduce the animation to a static figure with a single brightness change.

### Test 2 — 12 frames

A figure gradually rises and raises one arm toward a neon cross. Show a coherent progression from the initial lower posture through the rise and arm lift. Preserve the cross, environment, character identity and camera framing across all 12 cells.

## Post-generation frame extraction

Use:

```bash
python scripts/slice_spritesheet.py spritesheet.png \\
  --rows 3 --columns 4 --frame-count 12 --output-dir frames
```

For a 9-frame sheet, use `--rows 3 --columns 3 --frame-count 9`.

The extractor is strict: the source dimensions must divide evenly into the requested grid. If they do not, correct the source sheet rather than silently stretching or unevenly cropping frames.

## Encoding the extracted frames

The original frame duration for the two historical tests is not known. Choose and record the source FPS explicitly. For a numbered batch whose source GIF is 12 frames over 2.880 seconds, the observed source timing is 240 ms per frame (approximately 4.1667 fps); do not assume that timing applies to unrelated generations.

Example source GIF encode (replace `<FPS>` with the chosen, recorded rate):

```bash
ffmpeg -framerate <FPS> -i frames/frame_%03d.png \\
  -vf "split[s0][s1];[s0]palettegen[p];[s1][p]paletteuse=dither=sierra2_4a" \\
  -loop 0 source.gif
```

Example source MP4 encode:

```bash
ffmpeg -framerate <FPS> -i frames/frame_%03d.png \\
  -c:v libx264 -pix_fmt yuv420p -movflags +faststart source.mp4
```

Then, if the deliverable needs the current standard, run the source GIF through `scripts/interpolate_gif_24fps_5s.py`.

## Processing-only request used in this session

The user's instruction was:

> I want you to increase the frame rate to 24fps Interpolate. Then also I want you to extend the animation make it 5 secs.

That instruction applies to an **already animated GIF**. It requests motion-compensated interpolation and five-second duration normalization; it is not the spritesheet-generation prompt above.
