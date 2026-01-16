#!/usr/bin/env python3
"""
Generate a 3D animated cable/tube visualization with rotating perspective and traveling blips.
Outputs an animated GIF suitable for web deployment.
"""
import argparse
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


def main():
    parser = argparse.ArgumentParser(description="Generate cable animation GIF")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("cable_animation.gif"),
        help="Output GIF file path (default: cable_animation.gif)",
    )
    args = parser.parse_args()

    # Ensure output directory exists
    args.output.parent.mkdir(parents=True, exist_ok=True)

    try:
        generate_animation(args.output)
        print(f"✓ Generated: {args.output}")
        return 0
    except Exception as e:
        print(f"✗ Error generating cable animation: {e}", file=sys.stderr)
        return 1


def generate_animation(output_path: Path):
    """Generate the cable animation and save to output_path."""
    # Output settings
    W, H = 1920 * 2, 1080 * 2
    S = 2
    W2, H2 = W * S, H * S

    fps = 40
    duration_s = 4.0
    n_frames = int(duration_s * fps)

    # Cable / wireframe geometry (slightly wider)
    r_cable = 0.15
    r_wire = 0.15
    r_inner = r_cable

    # Camera: on-axis, set back so we start outside the tube
    cam_pos = np.array([0.0, 0.0, 6.0], dtype=float)
    up_world = np.array([0.0, 1.0, 0.0], dtype=float)
    f = 1.25

    def normalize(v):
        n = np.linalg.norm(v)
        return v if n == 0 else v / n

    def lookat_basis(cam_pos, target, up_world):
        forward = normalize(target - cam_pos)  # +Z in camera space
        right = normalize(np.cross(forward, up_world))  # +X
        up = np.cross(right, forward)  # +Y
        return right, up, forward

    def project(P, right, up, forward):
        V = P - cam_pos[None, :]
        x = V @ right
        y = V @ up
        z = V @ forward
        z = np.maximum(z, 1e-6)

        # Blend between ortho (0) and full perspective (1)
        persp_mix = 0.9
        xs_p = f * (x / z)
        ys_p = f * (y / z)
        xs = (1 - persp_mix) * x + persp_mix * xs_p
        ys = (1 - persp_mix) * y + persp_mix * ys_p
        return np.stack([xs, ys], axis=1)

    def rot_y(theta):
        c, s = math.cos(theta), math.sin(theta)
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]], dtype=float)

    # Animation: start truly head-on, then rotate to horizontal, hold
    theta_start = math.radians(0.0)
    theta_end = math.radians(90)
    rotate_portion = 0.6
    blip_start = 0.65  # when to start blip travel (as fraction of total animation)

    # Put the cable slightly forward so the opening sits ahead of the camera
    z_center = -3.0

    # Screen center
    cx = W2 / 2
    cy = H2 / 2

    # Choose L + scale so the final horizontal pose spans (slightly beyond) full width
    desired_span_px = W2 * 1.06
    L = 12.0

    # Compute scale that makes the end pose span width
    endpoints_local = np.array([[0.0, 0.0, +L / 2], [0.0, 0.0, -L / 2]], dtype=float)
    R_end = rot_y(theta_end)
    endpoints_world = (R_end @ endpoints_local.T).T + np.array([0.0, 0.0, z_center])
    target = np.array([0.0, 0.0, z_center], dtype=float)
    right, up, forward = lookat_basis(cam_pos, target, up_world)
    pts2 = project(endpoints_world, right, up, forward)
    width_screen = abs(pts2[1, 0] - pts2[0, 0])
    scale = desired_span_px / max(width_screen, 1e-6)
    # Nudge cable downward so the bottom black buffer is only ~one cable height
    cable_half_px = r_wire * scale
    buffer_px = 2 * cable_half_px  # one full cable height as buffer
    cy = H2 - (buffer_px + cable_half_px)

    def to_pixels(pts2):
        return np.stack([cx + pts2[:, 0] * scale, cy - pts2[:, 1] * scale], axis=1)

    # Wireframe primitives (more rings, fewer longitudinal)
    n_phi = 120
    phis = np.linspace(0, 2 * np.pi, n_phi, endpoint=True)

    n_rings = 84
    z_rings = np.linspace(+L / 2, -L / 2, n_rings)
    rings_local = [
        np.stack(
            [
                r_wire * np.cos(phis),
                r_wire * np.sin(phis),
                np.full_like(phis, z),
            ],
            axis=1,
        )
        for z in z_rings
    ]

    # Longitudinals: always top/bottom plus four around the sides
    phi_long = np.deg2rad([-90, 90, 30, -30, 0])
    n_long = phi_long.size
    n_z_samples = 110
    z_line = np.linspace(+L / 2, -L / 2, n_z_samples)
    longs_local = [
        np.stack(
            [
                np.full_like(z_line, r_wire * np.cos(phi)),
                np.full_like(z_line, r_wire * np.sin(phi)),
                z_line,
            ],
            axis=1,
        )
        for phi in phi_long
    ]

    # Cross-section cues at the near end (opening)
    front_outer_local = np.stack(
        [
            r_cable * np.cos(phis),
            r_cable * np.sin(phis),
            np.full_like(phis, +L / 2),
        ],
        axis=1,
    )
    front_inner_local = np.stack(
        [
            r_inner * np.cos(phis),
            r_inner * np.sin(phis),
            np.full_like(phis, +L / 2),
        ],
        axis=1,
    )

    def draw_polyline(draw, pts, width):
        draw.line([tuple(p) for p in pts], fill=ink, width=width, joint="curve")

    # Camera basis fixed on cable midpoint
    target = np.array([0.0, 0.0, z_center], dtype=float)
    right, up, forward = lookat_basis(cam_pos, target, up_world)

    line_w = int(2.2 * S)
    cable_w = int(3.2 * S)
    inner_w = int(2.2 * S)
    ink = 240  # light gray (#f0f0f0)
    bg_level = 17  # dark gray (#111111)

    frames = []
    durations = []
    for i in range(n_frames):
        p = i / (n_frames - 1)
        if p < rotate_portion:
            u = p / rotate_portion
            u = u * u * (3 - 2 * u)
            theta = theta_start + (theta_end - theta_start) * u
        else:
            theta = theta_end

        R = rot_y(theta)

        img = Image.new("L", (W2, H2), bg_level)
        draw = ImageDraw.Draw(img)

        # Dense rings first
        for ring in rings_local:
            Pw = (R @ ring.T).T + np.array([0.0, 0.0, z_center])
            pts2 = project(Pw, right, up, forward)
            draw_polyline(draw, to_pixels(pts2), width=line_w)

        # Sparse longitudinals
        for line in longs_local:
            Pw = (R @ line.T).T + np.array([0.0, 0.0, z_center])
            pts2 = project(Pw, right, up, forward)
            draw_polyline(draw, to_pixels(pts2), width=line_w)

        # Opening (outer + inner)
        Pw_outer = (R @ front_outer_local.T).T + np.array([0.0, 0.0, z_center])
        pts2_outer = project(Pw_outer, right, up, forward)
        draw_polyline(draw, to_pixels(pts2_outer), width=cable_w)

        Pw_inner = (R @ front_inner_local.T).T + np.array([0.0, 0.0, z_center])
        pts2_inner = project(Pw_inner, right, up, forward)
        draw_polyline(draw, to_pixels(pts2_inner), width=inner_w)

        # Blips traveling from center toward each end once rotation is complete
        if theta == theta_end and p >= blip_start:
            raw = (p - blip_start) / max(1e-6, 1 - blip_start)
            hold = 0  # keep the blips overlapped at center briefly
            travel = 0.0 if raw <= hold else min(1.0, (raw - hold) / max(1e-6, 1 - hold))
            blip_half_height = r_cable  # same height as cylinder radius
            travel_range = L * 0.9  # drive past the visible ends
            base_half_width = r_cable * 15  # ensure visible thickness at start
            for zsign in (1.0, -1.0):
                zpos = zsign * (travel * travel_range)
                growth = -1
                blip_half_width = base_half_width + growth
                rect_local = np.array(
                    [
                        [-blip_half_width, -blip_half_height, zpos],
                        [blip_half_width, -blip_half_height, zpos],
                        [blip_half_width, blip_half_height, zpos],
                        [-blip_half_width, blip_half_height, zpos],
                    ],
                    dtype=float,
                )
                Pw_rect = (R @ rect_local.T).T + np.array([0.0, 0.0, z_center])
                pts2_rect = to_pixels(project(Pw_rect, right, up, forward))
                draw.polygon([tuple(p) for p in pts2_rect], fill=ink)

        # Anti-alias
        img = img.filter(ImageFilter.GaussianBlur(radius=0.55))

        # Downsample
        img_small = img.resize((W, H), resample=Image.Resampling.LANCZOS)
        frames.append(img_small.convert("P", palette=Image.Palette.ADAPTIVE, colors=16))
        durations.append(int(1000 / fps))

    # Hold the final frame so it effectively stops
    durations[-1] = 10000  # 10s hold on the last frame

    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        optimize=True,
    )


if __name__ == "__main__":
    sys.exit(main())
