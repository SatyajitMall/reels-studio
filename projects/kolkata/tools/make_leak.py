#!/usr/bin/env python3
"""KOLKATA round 5b: a procedural warm light leak (1080×1920, 25 fps), for the director's "cinematic effect" note.

Two files from one render:
  <out>_screen.mov  ProRes 422, the leak on black: Premiere V4 with blend mode Screen (the build);
  <out>_alpha.mov   ProRes 4444 with alpha = the leak's brightness: an overlay for scripts/preview_edl.py, which only
                    composites "normal", so this is an approximation of Screen.
The leak: two soft blobs (amber and rose) that sweep across the frame, peaking at the middle of the clip.

Usage (studio root):
  .venv/bin/python projects/kolkata/tools/make_leak.py -o projects/kolkata/renders/overlays/leak_a --dur 1.0 --seed 1
"""
import argparse
import subprocess

import numpy as np

W, H, FPS = 1080, 1920, 25


def frames(dur, seed, peak):
    rng = np.random.default_rng(seed)
    n = int(round(dur * FPS))
    yy, xx = np.mgrid[0:H:4, 0:W:4].astype(np.float32)  # quarter-res field, upscaled by ffmpeg
    blobs = [  # colour (linear-ish RGB), start x, end x, y, radius
        (np.array([1.0, 0.62, 0.25]), -0.3 * W, 1.2 * W, rng.uniform(0.3, 0.5) * H, 0.55 * W),
        (np.array([1.0, 0.38, 0.42]), 1.3 * W, 0.1 * W, rng.uniform(0.55, 0.75) * H, 0.45 * W),
    ]
    for i in range(n):
        u = i / max(n - 1, 1)
        env = np.sin(np.pi * u) ** 1.5 * peak
        img = np.zeros(xx.shape + (3,), np.float32)
        for col, x0, x1, y, rad in blobs:
            cx = x0 + (x1 - x0) * u
            d2 = ((xx - cx) ** 2 + (yy - y) ** 2 * 0.35) / rad ** 2
            img += np.exp(-d2 * 2.2)[..., None] * col
        img = np.clip(img * env, 0, 1)
        yield (img * 255).astype(np.uint8)


def render(out, dur, seed, peak):
    fr = list(frames(dur, seed, peak))
    h, w = fr[0].shape[:2]
    rgb = np.stack(fr)
    common = ["-f", "rawvideo", "-s", f"{w}x{h}", "-r", str(FPS)]
    up = f"scale={W}:{H}:flags=bicubic"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *common, "-pix_fmt", "rgb24", "-i", "-", "-vf", up,
                    "-c:v", "prores_ks", "-profile:v", "2", "-pix_fmt", "yuv422p10le", f"{out}_screen.mov"],
                   input=rgb.tobytes(), check=True)
    a = rgb.max(axis=3, keepdims=True)
    rgba = np.concatenate([np.where(a > 0, rgb.astype(np.float32) * 255 / np.maximum(a, 1), 0).astype(np.uint8), a], 3)
    subprocess.run(["ffmpeg", "-v", "error", "-y", *common, "-pix_fmt", "rgba", "-i", "-", "-vf", up,
                    "-c:v", "prores_ks", "-profile:v", "4444", "-pix_fmt", "yuva444p10le", f"{out}_alpha.mov"],
                   input=rgba.tobytes(), check=True)
    print(f"{out}_screen.mov / _alpha.mov  {len(fr)} frames")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-o", required=True)
    ap.add_argument("--dur", type=float, default=1.0)
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--peak", type=float, default=0.75)
    a = ap.parse_args()
    render(a.o, a.dur, a.seed, a.peak)
