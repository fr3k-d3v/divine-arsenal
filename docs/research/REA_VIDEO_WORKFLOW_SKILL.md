# FR3K REA Video workflow skill

## Trigger
Use this workflow when a user supplies or selects an MP4, MOV, MKV, WebM or AVI for reverse engineering, shot analysis, editing reconstruction or a remake plan.

## Authoritative pipeline
1. Ingest through Divine's local raw video route. Keep the original bytes unchanged and preserve the returned SHA-256.
2. Submit the URE profile video with authority OBSERVE. Do not bypass the URE scheduler or run the parser directly on the host.
3. Review the URE report. Treat shot boundaries, production-method labels, camera/editing timelines and inferred real-material ratios as tool observations, not verified facts.
4. Inspect storyboard.jpg, audio.png, VIDEO.md, breakdown.json, review_tasks.json and review_answers.json. Independent visual review remains PENDING until an actual reviewer records answers.
5. Inspect the Capsule Cinema remake-jobs.json and remake-dry-run.txt. These are a local-machine-specific job graph and a dry-run transcript, not proof that a remake has been generated.
6. Preserve all output hashes and the artifact manifest in the private notebook. Never replace or mutate the original input evidence.
7. If a later review changes the interpretation, create a new versioned review record. Do not silently rewrite a terminal job or promote an unreviewed tool label to VERIFIED FACT.

## Runtime pins
- REA Video v0.1.0, Apache-2.0, commit b08faf2eb53690fc92ddf94576a8c7c3a4a87f89.
- Capsule Cinema, Apache-2.0, commit 97229260c96ee8a3fb37db83027bbc1aefd8f073.
- Separate local runtimes; upstream source is not vendored into URE or Divine.

## Security and execution policy
- URE authority is OBSERVE only. Network is denied in Bubblewrap. Input/runtime are read-only; output is private and bounded; one video worker runs at a time.
- Supported media is capped at 64 MiB, 240 seconds, 4K/60 fps, 14,400 frames, one video stream and four audio streams.
- VLM, OCR/HTR, ASR, speaker separation and stems are disabled.
- Capsule Cinema remake planning and remake-run --dry-run are permitted. Do not run generation without separate explicit user approval, a verified provider configuration and a reviewed cost estimate.
- Current state: Capsule Cinema Python 3.12 runtime installed; provider configuration absent; generation status BLOCKED_NO_PROVIDER_CONFIG. No API key or paid call has been used.
- Do not commit remake-jobs.json or raw local outputs without sanitizing machine-specific paths.

## Output labels
Use CLAIM, OBSERVATION, EVIDENCE, VERIFIED FACT, HYPOTHESIS, SIMULATION and UNKNOWN accurately. A successful tool exit is evidence that the tool ran, not proof that its interpretation is correct.
