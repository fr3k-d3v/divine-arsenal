#!/usr/bin/env python3
"""Extract an equal-cell AI animation spritesheet into ordered PNG frames."""

from __future__ import annotations

import argparse
from pathlib import Path
from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spritesheet", type=Path)
    parser.add_argument("--rows", type=int, required=True)
    parser.add_argument("--columns", type=int, required=True)
    parser.add_argument("--frame-count", type=int, default=None)
    parser.add_argument("--output-dir", type=Path, default=Path("frames"))
    parser.add_argument("--prefix", default="frame_")
    args = parser.parse_args()

    if args.rows < 1 or args.columns < 1:
        parser.error("--rows and --columns must be positive integers")

    total_cells = args.rows * args.columns
    frame_count = args.frame_count if args.frame_count is not None else total_cells
    if frame_count < 1 or frame_count > total_cells:
        parser.error("--frame-count must be between 1 and rows × columns")

    with Image.open(args.spritesheet) as image:
        width, height = image.size
        if width % args.columns or height % args.rows:
            raise SystemExit(
                f"Grid does not divide evenly: sheet={width}x{height}, "
                f"grid={args.columns}x{args.rows}. Refuse uneven crops."
            )

        cell_w = width // args.columns
        cell_h = height // args.rows
        args.output_dir.mkdir(parents=True, exist_ok=True)

        outputs = []
        for index in range(frame_count):
            row, col = divmod(index, args.columns)
            left = col * cell_w
            top = row * cell_h
            frame = image.crop((left, top, left + cell_w, top + cell_h))
            path = args.output_dir / f"{args.prefix}{index + 1:03d}.png"
            frame.save(path, format="PNG")
            outputs.append(path)

    print(
        f"Extracted {len(outputs)} frames of {cell_w}x{cell_h} "
        f"from {args.spritesheet} into {args.output_dir}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
