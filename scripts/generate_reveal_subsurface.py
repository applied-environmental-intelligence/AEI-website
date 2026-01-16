#!/usr/bin/env python3
"""
Generate a subsurface reveal animation using a semi-circular wipe effect.
Requires a source PNG image and outputs an animated GIF.
"""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

BG_RGBA = (17, 17, 17, 255)  # #111111 solid background


def main():
    parser = argparse.ArgumentParser(description="Generate subsurface reveal GIF")
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("subsurface.png"),
        help="Input PNG source image (default: subsurface.png)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("subsurface_reveal.gif"),
        help="Output GIF file path (default: subsurface_reveal.gif)",
    )
    args = parser.parse_args()

    # Validate input exists
    if not args.input.exists():
        print(f"✗ Error: Input file not found: {args.input}", file=sys.stderr)
        print(
            f"  Please provide a PNG image at {args.input} or use --input to specify a different path.",
            file=sys.stderr,
        )
        return 1

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        generate_animation(args.input, args.output)
        print(f"✓ Generated: {args.output}")
        return 0
    except Exception as e:
        print(f"✗ Error generating subsurface reveal: {e}", file=sys.stderr)
        return 1


def generate_animation(input_path: Path, output_path: Path):
    """Generate the subsurface reveal animation from input_path and save to output_path."""
    # Output settings
    fps = 50
    duration_s = 1.9
    n_frames = max(2, int(duration_s * fps))

    img = Image.open(input_path).convert("RGBA")
    w, h = img.size
    cx = w / 2

    max_r = 1.5 * max(w, h)

    frames = []
    for i in range(n_frames):
        t = i / (n_frames - 1)
        r = t * max_r  # grow past the frame

        # Build mask: half circle with flat edge along the top of the image
        mask = Image.new("L", (w, h), 0)
        draw = ImageDraw.Draw(mask)
        # Flat edge locked at y=0; arc extends downward as radius grows
        draw.pieslice((cx - r, -r, cx + r, r), 0, 180, fill=255)

        # Second mask: hollow out a thinner band behind the leading edge
        band_thickness = w * (0.02 + 0.15 * min(1, t))
        inner_r = max(0, r - band_thickness)
        if inner_r > 0:
            draw.pieslice((cx - inner_r, -inner_r, cx + inner_r, inner_r), 0, 180, fill=0)

        # Fade mask back out as it expands off-screen
        if r > w:
            fade = max(0.0, 1.0 - (r - w) / max(1e-6, max_r - w))
            if fade < 1.0:
                mask = mask.point(lambda x: int(x * fade))

        # Feather mask edges for a soft fade
        mask = mask.filter(ImageFilter.GaussianBlur(radius=max(1, int(w * 0.01))))

        # Apply mask over a dark background
        frame = Image.new("RGBA", (w, h), BG_RGBA)
        revealed = img.copy()
        revealed.putalpha(mask)
        frame = Image.alpha_composite(frame, revealed)
        # Keep palette richer so background stays true to #111111
        frames.append(frame.convert("RGB").quantize(colors=256, method=Image.MEDIANCUT))

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        optimize=True,
    )


if __name__ == "__main__":
    sys.exit(main())
