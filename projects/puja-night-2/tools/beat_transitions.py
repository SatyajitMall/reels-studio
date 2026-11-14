#!/usr/bin/env python3
"""Beat-matched transition overlays rendered from the reel's graded export (puja-night-2 round 6).

Each transition is a short full-frame clip (4 frames before + 4 after the cut by default) built from the
export's own frames, so it matches the grade exactly; place it on a track above everything at cut − pre.
Types:
  zoom   zoom-through: the outgoing shot scales up into a radial blur, the incoming one lands from it
  whip   whip pan: directional motion blur + slide; dir "left" / "right" / "up" / "down" (direction the image moves)
  leak   warm gold light leak sweeping across the cut (replaces hard white flashes)
  dip    soft dip through warm dark (outro; use instead of a dissolve when Warp-stabilised clips have no
         analysed handles: a dissolve over them shows Warp's banner)
A cross / film dissolve needs frames past the cut on both clips, so use Premiere's own transition for that.

Usage:
  .venv/bin/python projects/puja-night-2/tools/beat_transitions.py --source renders/exports/x_body.mp4 \
      --spec '[{"type":"zoom","cut":3.80},{"type":"whip","cut":22.76,"dir":"left"},{"type":"leak","cut":40.44}]' \
      -o renders/overlays/transitions_v6
Writes <out>/t<NN>_<type>_<cut>.mp4 and <out>/manifest.json ([{file, start, frames, type, cut}]).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image
from scipy import ndimage as ndi

W, H, FPS = 1080, 1920, 25


def grab(src: str, t0: float, n: int) -> np.ndarray:
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t0:.3f}", "-i", src, "-frames:v", str(n), "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
    return np.frombuffer(p, np.uint8).reshape(-1, H, W, 3).astype(np.float32)


def shift_blur(f: np.ndarray, dx: float, dy: float, blur: int) -> np.ndarray:
    g = np.roll(np.roll(f, int(dx), axis=1), int(dy), axis=0)
    if blur > 1:
        g = ndi.uniform_filter1d(g, int(blur), axis=1 if abs(dx) >= abs(dy) else 0)
    return g


def zoom(f: np.ndarray, s: float, spread: float, steps: int = 6) -> np.ndarray:
    acc = np.zeros_like(f)
    for k in range(steps):
        sk = s * (1 + spread * k / steps)
        im = Image.fromarray(f.astype(np.uint8)).resize((int(W * sk), int(H * sk)), Image.BILINEAR)
        x0, y0 = (im.width - W) // 2, (im.height - H) // 2
        acc += np.asarray(im, np.float32)[y0:y0 + H, x0:x0 + W]
    return acc / steps


DIRS = {"left": (-1, 0), "right": (1, 0), "up": (0, -1), "down": (0, 1)}


def build(kind: str, A: np.ndarray, B: np.ndarray, n: int, direction: str) -> list[np.ndarray]:
    out = []
    if kind == "zoom":
        for k in range(n):
            out.append(zoom(A[k], 1 + 0.5 * ((k + 1) / n) ** 2, 0.04 + 0.06 * k))
        for k in range(n):
            out.append(zoom(B[k], 1 + 0.5 * ((n - k) / n) ** 2, 0.04 + 0.06 * (n - 1 - k)))
    elif kind == "whip":
        ux, uy = DIRS[direction]
        span = W if ux else H
        for k in range(n):
            d = span * ((k + 1) / n) ** 2 * 0.8
            out.append(shift_blur(A[k], ux * d, uy * d, 40 + 80 * k))
        for k in range(n):
            d = span * ((n - k) / n) ** 2 * 0.8
            out.append(shift_blur(B[k], -ux * d, -uy * d, 40 + 80 * (n - 1 - k)))
    elif kind == "leak":
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        frames = list(A) + list(B)
        m = len(frames)
        for i, f in enumerate(frames):
            p = i / (m - 1)
            cx, a = -300 + 1700 * p, np.sin(np.pi * p)
            leak = np.exp(-(((xx - cx) / 380) ** 2 + ((yy - 700) / 1300) ** 2))[..., None] * np.array([255, 170, 60]) * 0.5 * a
            out.append(f * (1 + 0.25 * a) + leak + 20 * a * np.exp(-(((xx - cx) / 900) ** 2))[..., None])
    elif kind == "dip":   # soft dip through warm dark (an outro dissolve that needs no frames past the cut)
        warm = np.array([26, 15, 6], np.float32)
        for k in range(n):
            a = ((k + 1) / n) ** 1.5 * 0.85
            out.append(A[k] * (1 - a) + warm * a)
        for k in range(n):
            a = ((n - k) / n) ** 1.5 * 0.85
            out.append(B[k] * (1 - a) + warm * a)
    else:
        raise SystemExit(f"unknown type {kind}")
    return out


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", required=True)
    ap.add_argument("--spec", required=True, help="JSON list of {type, cut, dir?, n?}")
    ap.add_argument("--prefix", default="t", help="file-name prefix (keep names unique within the Premiere bin)")
    ap.add_argument("-o", "--out", required=True, type=Path)
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    manifest = []
    for j, t in enumerate(json.loads(a.spec)):
        n = int(t.get("n", 4))
        cut = round(t["cut"] * FPS) / FPS
        A = grab(a.source, cut - n / FPS, n)
        B = grab(a.source, cut, n)
        frames = build(t["type"], A, B, n, t.get("dir", "left"))
        name = f"{a.prefix}{j:02d}_{t['type']}_{cut:.2f}.mp4"
        with tempfile.TemporaryDirectory() as td:
            for i, f in enumerate(frames):
                Image.fromarray(np.clip(f, 0, 255).astype(np.uint8)).save(f"{td}/f{i:04d}.png")
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", str(FPS), "-i", f"{td}/f%04d.png", "-c:v", "libx264",
                            "-crf", "12", "-pix_fmt", "yuv420p", str(a.out / name)], check=True)
        manifest.append({"file": name, "start": round(cut - n / FPS, 2), "frames": len(frames), "type": t["type"], "cut": cut})
        print(f"✓ {name}  start {cut - n / FPS:.2f}")
    json.dump(manifest, open(a.out / "manifest.json", "w"), indent=1)


if __name__ == "__main__":
    main()
