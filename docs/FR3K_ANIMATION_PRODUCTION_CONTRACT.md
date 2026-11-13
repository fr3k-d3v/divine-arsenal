# FR3K animation production contract (2026-11-13)

## Canonical creative brief
Brand lettering must read exactly `-=fR3k=-` (case-sensitive). The currently approved direction is a sharp, slashed, metallic brush-script font integrated into a spiked, angular hexagonal crest. This replaces the older circular industrial emblem. Typography and crest geometry must remain visually stable across frames, while lighting and surrounding effects move independently. Do not fake this with a static font overlay or procedural text pasted on old footage. Review generated spelling; AI generations have previously rendered `fR3K` or other approximations.

## Deliverable
One 60-second portrait video containing TEN distinct styles, six seconds each; provide ten independently playable clips and a master montage. Target 60 fps (3,600 total output frames, 360 frames per style), with a widescreen master if requested. Preserve source keyframes, prompt/seed/settings, individual clips, concat manifest and ffprobe reports. Loop boundaries should be checked, especially if clips are intended to repeat.

## Ten effect families
1. Electric blue lightning / neon energy
2. Solar fire / magma bloom
3. Frozen crystal / ice
4. Violet occult aurora / nebula
5. Toxic green slime
6. Electric storm / charged reactor
7. Water vortex / liquid splash
8. Cyberpunk glitch / neon radar
9. Cosmic vortex / quantum ripples
10. Royal gold / celestial emblem

These are creative effect families; the user may revise order. Each needs its own AI-generated animation, not merely color grading of the blue clip.

## Quality bar: non-negotiable
- User explicitly rejected 1 fps-looking motion, sparse 10-16-keyframe sequences, naive 24/60 fps transcodes, frame duplication, and simple frame blending.
- **Target at least 48 independently AI-rendered temporally coherent keyframes per six-second style** (480 across ten) before any interpolation; more where motion is fast. Keyframe count is a target, not a claim until observed.
- Use motion-aware interpolation only between temporally consistent generated frames; check for ghosting, tearing, letter deformation, frozen effects, flicker and jumps. If insufficient, regenerate actual intermediate AI frames rather than increasing container FPS.
- Aim for 60 fps playback and verify with ffprobe AND visual frame sampling / motion inspection. 60 fps metadata alone is NOT proof of smooth motion.
- Validate every 6-second style independently, transitions, total duration, dimensions, 3,600-frame target, and exact lettering.
- Avoid claiming completion or independent AI generation without evidence. Report keyframe count, interpolated count, output frame count and limitations honestly.

## Previous failures / evidence
- Early 10-style montage used the old round frame.
- Several '24 fps' and '60 fps' versions were only optical flow / blended duplicates of sparse AI keyframes, with perceptually choppy effects.
- A six-style, 36-second render used 16 generated frames per style, interpolated to 144 frames/style; user still found it choppy.
- Later ten-style, 60-second render existed, but reused older geometry and lacked sufficient new AI keyframes.
- A new hexagonal electric-blue six-second test existed, but did not cover the other nine styles.
- Most recent `FR3K_10_Styles_60fps_Blend_Preview.mp4` was reported as 59.93s / 3,596 frames, 60 fps **frame blending only**, not the promised 48 generated keyframes/style. User: 'Better. Still not smooth enough.'
- Generated image/GIF previews are not equivalent to finished videos. Prior ChatGPT sandbox links repeatedly returned 'Not found' for the user; verify file exists and link delivery when exporting.

## Workflow
1. Inspect this contract and repository governance first.
2. Establish exact typography/crest master image and validate lettering.
3. Generate 48+ independently AI-rendered keyframes for each of ten effects, with temporal continuity and geometry lock. Preserve raw assets.
4. Assemble each six-second clip using high-quality motion estimation where safe. Visually inspect slow/fast sections, not just frame counts.
5. Concatenate into a 60-second 60 fps master. Verify exactly 3,600 output frames, no gaps and no accidental freeze/duplicate sequences.
6. Provide downloadable master, ten clips, sources, generation prompts/settings, and manifest; commit instructions/evidence to GitHub. Only claim assets were uploaded if GitHub confirms them.
7. If resources/tools cannot deliver 480 genuinely generated keyframes, disclose partial status and do not substitute interpolated frames as if they were generated.

## Status at time of writing
**SPECIFICATION SAVED; PRODUCTION NOT VERIFIED.** No claim that 480 independent AI keyframes or final 60 fps master has been rendered.
