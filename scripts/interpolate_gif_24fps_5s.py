#!/usr/bin/env python3
"""Normalize an animated GIF to 120 motion-interpolated frames / 24 fps / 5 s."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image

FPS = 24
DURATION_SECONDS = 5
FRAME_COUNT = FPS * DURATION_SECONDS


def run(command: list[str]) -> str:
    result = subprocess.run(command, check=True, capture_output=True, text=True)
    return result.stdout.strip()


def gif_metadata(path: Path) -> dict:
    with Image.open(path) as image:
        width, height = image.size
        frames = 0
        duration_ms = 0
        while True:
            frames += 1
            duration_ms += int(image.info.get("duration", 0))
            try:
                image.seek(image.tell() + 1)
            except EOFError:
                break
    return {
        "width": width,
        "height": height,
        "frames": frames,
        "duration_ms": duration_ms,
        "bytes": path.stat().st_size,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, default=Path("."))
    args = parser.parse_args()

    source = args.source.resolve()
    output_dir = args.output_dir.resolve()
    if not source.is_file():
        parser.error(f"Source GIF does not exist: {source}")
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        raise SystemExit("ffmpeg and ffprobe must be installed and available on PATH")

    source_meta = gif_metadata(source)
    if source_meta["duration_ms"] <= 0:
        raise SystemExit("Source GIF has no usable frame timing")

    output_dir.mkdir(parents=True, exist_ok=True)
    stem = source.stem
    mp4_path = output_dir / f"{stem}_interpolated_24fps_5s.mp4"
    gif_path = output_dir / f"{stem}_interpolated_24fps_5s.gif"

    stretch_factor = (DURATION_SECONDS * 1000) / source_meta["duration_ms"]
    vf = (
        f"setpts=PTS*{stretch_factor:.12f},"
        "minterpolate=fps=24:mi_mode=mci:mc_mode=aobmc:"
        "me_mode=bidir:vsbmc=1,"
        "trim=duration=5,setpts=PTS-STARTPTS,"
        "pad=ceil(iw/2)*2:ceil(ih/2)*2"
    )

    with tempfile.TemporaryDirectory(prefix="da-animation-") as temp_dir:
        raw_gif = Path(temp_dir) / "palette.gif"

        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-stream_loop", "1", "-i", str(source),
            "-vf", vf, "-an", "-frames:v", str(FRAME_COUNT), "-r", str(FPS),
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-pix_fmt", "yuv420p", "-movflags", "+faststart",
            str(mp4_path),
        ])

        width = source_meta["width"]
        height = source_meta["height"]
        palette_filter = (
            f"[0:v]format=rgb24,crop={width}:{height}:0:0,split[s0][s1];"
            "[s0]palettegen=stats_mode=full[p];"
            "[s1][p]paletteuse=dither=sierra2_4a"
        )
        run([
            "ffmpeg", "-y", "-hide_banner", "-loglevel", "error",
            "-i", str(mp4_path), "-filter_complex", palette_filter,
            "-loop", "0", str(raw_gif),
        ])

        with Image.open(raw_gif) as image:
            frames = []
            while True:
                frames.append(image.copy().convert("P"))
                try:
                    image.seek(image.tell() + 1)
                except EOFError:
                    break

        if len(frames) != FRAME_COUNT:
            raise SystemExit(
                f"GIF conversion produced {len(frames)} frames; expected {FRAME_COUNT}"
            )

        # GIF delays are quantized to 10 ms. This 40/50 ms pattern makes
        # every 12-frame block exactly 500 ms: 24 fps average over 5 seconds.
        delays = [
            50 if index % 12 in (5, 11) else 40
            for index in range(FRAME_COUNT)
        ]
        frames[0].save(
            gif_path,
            save_all=True,
            append_images=frames[1:],
            duration=delays,
            loop=0,
            optimize=True,
            disposal=2,
        )

    probe = json.loads(run([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries",
        "stream=width,height,r_frame_rate,avg_frame_rate,nb_frames,duration",
        "-of", "json", str(mp4_path),
    ]))["streams"][0]
    gif_result = gif_metadata(gif_path)

    if probe.get("r_frame_rate") != "24/1":
        raise SystemExit(f"Unexpected MP4 frame rate: {probe.get('r_frame_rate')}")
    if probe.get("avg_frame_rate") != "24/1":
        raise SystemExit(f"Unexpected average frame rate: {probe.get('avg_frame_rate')}")
    if int(probe.get("nb_frames", 0)) != FRAME_COUNT:
        raise SystemExit(f"Unexpected MP4 frame count: {probe.get('nb_frames')}")
    if abs(float(probe.get("duration", 0)) - DURATION_SECONDS) > 0.001:
        raise SystemExit(f"Unexpected MP4 duration: {probe.get('duration')}")
    if gif_result["frames"] != FRAME_COUNT or gif_result["duration_ms"] != 5000:
        raise SystemExit(f"Unexpected GIF timing: {gif_result}")

    print(json.dumps({
        "source": {"filename": source.name, **source_meta},
        "mp4": {"filename": mp4_path.name, **probe},
        "gif": {"filename": gif_path.name, **gif_result},
        "settings": {
            "fps": FPS,
            "duration_seconds": DURATION_SECONDS,
            "frames": FRAME_COUNT,
            "stretch_factor": stretch_factor,
            "interpolation": "minterpolate mci/aobmc/bidir/vsbmc",
        },
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
