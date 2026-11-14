#!/usr/bin/env python3
"""Per-frame sharpness / motion / luma for every b-roll clip (puja-night-2 round 5 shot pool).

Round 5 needs many short (0.6–1.3 s) moments for beat cuts, not 17 long shots, so the pool must cover
all 62 clips. Sharpness is measured at 1080x1920 (the reel scale; half-res missed soft heads in round 1),
Laplacian variance on the centre 80 %, plus mean frame difference at 270x480 for motion.

Usage: .venv/bin/python projects/puja-night-2/tools/shot_pool.py [-j 4]
Writes analysis/shot_pool.json: {clip: {"dur", "fps", "sharp": [...], "motion": [...], "luma": [...]}}.
"""
from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ProcessPoolExecutor
from pathlib import Path

import numpy as np
from scipy.ndimage import laplace

REEL = Path(__file__).resolve().parents[1]


def scan(path: Path) -> tuple[str, dict]:
    p = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", "scale=1080:1920,format=gray",
                        "-f", "rawvideo", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8)
    n = len(a) // (1080 * 1920)
    a = a[: n * 1080 * 1920].reshape(n, 1920, 1080)
    sharp, motion, luma, prev = [], [], [], None
    for f in a:
        c = f[192:1728, 108:972].astype(np.float32)
        sharp.append(round(float(laplace(c).var()), 1))
        small = f[::4, ::4].astype(np.float32)
        motion.append(0.0 if prev is None else round(float(np.abs(small - prev).mean()), 2))
        luma.append(round(float(small.mean()) / 255, 3))
        prev = small
    clip = path.stem.split("_")[-1]
    return clip, {"file": path.name, "frames": n, "dur": round(n / 25, 2), "sharp": sharp, "motion": motion, "luma": luma}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("-j", type=int, default=4)
    a = ap.parse_args()
    files = sorted((REEL / "raw/b-roll").glob("*.mov"))
    out = {}
    with ProcessPoolExecutor(a.j) as ex:
        for clip, d in ex.map(scan, files):
            out[clip] = d
            print(f"{clip} {d['dur']:6.2f}s  sharp p50 {np.median(d['sharp']):7.1f}  p90 {np.percentile(d['sharp'], 90):7.1f}", flush=True)
    json.dump(out, open(REEL / "analysis/shot_pool.json", "w"))
    print(f"✓ analysis/shot_pool.json ({len(out)} clips)")


if __name__ == "__main__":
    main()
