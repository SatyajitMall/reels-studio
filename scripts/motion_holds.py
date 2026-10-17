#!/usr/bin/env python3
"""Find static holds and camera moves (pans/tilts) in every clip.

Holds (≥ --min-hold s of near-still camera) are where digital push/pull moves look intentional;
moves are real camera pans/tilts with direction. Handheld shake inside a hold doesn't count as a
move. Uses phase correlation on 10 fps grey frames.

Writes <out>/motion.json: {clip: {dur, holds: [[t0, t1]], moves: [[t0, t1, dir, px]], mean_speed}}.
dir is the direction the camera moves: L/R/U/D.

Usage:
  ./.venv/bin/python scripts/motion_holds.py projects/<reel>/raw/b-roll -o projects/<reel>/analysis [--skip C008,C018]
"""
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

import numpy as np

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mkv"}
W, H, FPS = 54, 96, 10
SCALE = 1080 / W
STILL_SPEED, STILL_DIFF, MOVE_SPEED = 8.0, 6.0, 20.0  # px/step in 1080 space; mean abs grey diff
MIN_MOVE = 0.8


def runs(mask: np.ndarray, min_len: float) -> list[tuple[int, int]]:
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]:
                j += 1
            if (j - i) / FPS >= min_len:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out


def analyse(path: Path, min_hold: float) -> dict | None:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={FPS},scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    if fr.size < W * H * 4:
        return None
    fr = fr[: fr.size // (W * H) * W * H].reshape(-1, H, W).astype(float)
    sh = []
    for a, b in zip(fr[:-1], fr[1:]):
        A, B = np.fft.fft2(a - a.mean()), np.fft.fft2(b - b.mean())
        R = A * np.conj(B)
        R /= np.abs(R) + 1e-9
        c = np.abs(np.fft.ifft2(R))
        y, x = np.unravel_index(c.argmax(), c.shape)
        if y > H / 2:
            y -= H
        if x > W / 2:
            x -= W
        sh.append((x * SCALE, y * SCALE, np.abs(a - b).mean()))
    sh = np.array(sh)
    sp = np.hypot(sh[:, 0], sh[:, 1])
    k = 5  # 0.5 s smoothing
    sm = np.convolve(sp, np.ones(k) / k, "same")
    dm = np.convolve(sh[:, 2], np.ones(k) / k, "same")
    holds = [[round(i / FPS, 2), round(j / FPS, 2)] for i, j in runs((sm < STILL_SPEED) & (dm < STILL_DIFF), min_hold)]
    moves = []
    for i, j in runs(sm >= MOVE_SPEED, MIN_MOVE):
        dx, dy = sh[i:j, 0].sum(), sh[i:j, 1].sum()
        # Image content shifts opposite to the camera: content moving left = camera panning right.
        d = ("R" if dx < 0 else "L") if abs(dx) > abs(dy) else ("D" if dy < 0 else "U")
        moves.append([round(i / FPS, 2), round(j / FPS, 2), d, int(abs(dx) + abs(dy))])
    return {"dur": round(len(fr) / FPS, 2), "holds": holds, "moves": moves, "mean_speed": round(float(sp.mean()), 1)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--skip", default="", help="comma-separated clip ids to skip")
    ap.add_argument("--min-hold", type=float, default=2.0, help="shortest hold worth reporting (s)")
    args = ap.parse_args()
    skip = {s.strip() for s in args.skip.split(",") if s.strip()}
    files: list[Path] = []
    for p in args.inputs:
        files += sorted(f for f in p.iterdir() if f.suffix.lower() in VIDEO_EXT and not f.name.startswith("._")) \
            if p.is_dir() else [p]
    res = {}
    for f in files:
        cid = f.stem.split("_")[-1]
        if cid in skip:
            continue
        r = analyse(f, args.min_hold)
        if r:
            res[cid] = r
            print(f"▸ {cid}: {len(r['holds'])} holds, {len(r['moves'])} moves", flush=True)
    args.out.mkdir(parents=True, exist_ok=True)
    (args.out / "motion.json").write_text(json.dumps(res, indent=1))
    print(f"✓ {args.out / 'motion.json'}")


if __name__ == "__main__":
    main()
