from __future__ import annotations

from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter


def main():
    src = Path("subsurface.png")
    if not src.exists():
        raise FileNotFoundError(f"Missing {src}")

    # Output settings
    fps = 50
    duration_s = 1.9
    n_frames = max(2, int(duration_s * fps))
    out_gif = Path("subsurface_reveal.gif")

    img = Image.open(src).convert("RGBA")
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

        # Second mask: hollow out a thinner band behind the leading edge, growing from ~2% to ~8%
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

        # Apply mask over a black background
        frame = Image.new("RGBA", (w, h), (0, 0, 0, 255))
        revealed = img.copy()
        revealed.putalpha(mask)
        frame = Image.alpha_composite(frame, revealed)
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=64))

    frames[0].save(
        out_gif,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        optimize=True,
    )
    print(f"Saved {out_gif}")


if __name__ == "__main__":
    main()
