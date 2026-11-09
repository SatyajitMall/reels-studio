#!/usr/bin/env python3
"""Scan every frame of a render for short defects that 2 fps contact sheets miss.

Per frame: sharpness (Laplacian energy / luma), change from the previous frame, and mean luma.
Flags, per shot:
  blur_dip    sharpness < 60 % of the shot's median for ≥ 2 frames (camera jerk smear, stabiliser or
              optical-flow smear, overlays washing detail). The my-reel C073 jerks dropped to 0.51.
  frozen      ≥ 4 consecutive frames with almost no change inside a shot (a stall or a held frame)
  luma_jump   a frame-to-frame luma change > 0.05 that isn't at a cut (flicker or strobing transitions)
  black/white whole frames near 0 or 1 (fine at designed fades and flashes; check they're intended)
The first and last 2 frames of each shot are ignored, so cuts don't count as defects.

Writes <out>.json and prints a table of flagged spans. Then look at each span at full frame size.

Usage:
  ./.venv/bin/python scripts/frame_scan.py <video> -o <out.json> [--shots shots.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from media_info import fps_of  # noqa: E402  (robust on rotation-tagged camera files)

W, H = 270, 480
EDGE = 2


def spans(mask: np.ndarray, min_len: int) -> list[tuple[int, int]]:
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j < len(mask) and mask[j]:
                j += 1
            if j - i >= min_len:
                out.append((i, j))
            i = j
        else:
            i += 1
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--shots", type=Path, help="JSON list of [name, start_s, end_s]; default: the whole video as one shot")
    args = ap.parse_args()

    fps = fps_of(args.video)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(args.video), "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    fr = fr[: fr.size // (W * H) * W * H].reshape(-1, H, W).astype(np.float32) / 255
    luma = fr.mean((1, 2))
    lap = np.abs(4 * fr[:, 1:-1, 1:-1] - fr[:, :-2, 1:-1] - fr[:, 2:, 1:-1] - fr[:, 1:-1, :-2] - fr[:, 1:-1, 2:]).mean((1, 2))
    sharp = lap / (luma + 0.05)
    diff = np.concatenate([[np.inf], np.abs(np.diff(fr, axis=0)).mean((1, 2)) * 255])
    dl = np.concatenate([[0.0], np.abs(np.diff(luma))])

    dur = len(fr) / fps
    shots = json.loads(args.shots.read_text()) if args.shots else [["all", 0.0, dur]]
    flags = []
    for name, a, b in shots:
        i0, i1 = int(round(a * fps)) + EDGE, int(round(b * fps)) - EDGE
        if i1 - i0 < 6:
            continue
        s, d, j = sharp[i0:i1], diff[i0:i1], dl[i0:i1]
        med = float(np.median(s))
        for x, y in spans(s < 0.6 * med, 2):
            flags.append({"shot": name, "type": "blur_dip", "t0": round((i0 + x) / fps, 2), "t1": round((i0 + y) / fps, 2),
                          "value": round(float(s[x:y].min() / med), 2), "note": "min sharpness / shot median"})
        for x, y in spans(d < 0.35, 4):
            flags.append({"shot": name, "type": "frozen", "t0": round((i0 + x) / fps, 2), "t1": round((i0 + y) / fps, 2),
                          "value": round(float(d[x:y].mean()), 2), "note": "mean frame change (0–255)"})
        for x, y in spans(j > 0.05, 1):
            flags.append({"shot": name, "type": "luma_jump", "t0": round((i0 + x) / fps, 2), "t1": round((i0 + y) / fps, 2),
                          "value": round(float(j[x:y].max()), 3), "note": "max frame-to-frame luma change"})
    for kind, m in (("black", luma < 0.02), ("white", luma > 0.95)):
        for x, y in spans(m, 1):
            flags.append({"shot": "-", "type": kind, "t0": round(x / fps, 2), "t1": round(y / fps, 2), "value": round(float(luma[x:y].mean()), 3),
                          "note": "whole-frame mean luma"})
    flags.sort(key=lambda f: f["t0"])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps({"video": str(args.video), "fps": fps, "frames": len(fr), "flags": flags}, indent=1))
    print(f"{'type':<10}{'shot':<14}{'from':>7}{'to':>7}  value")
    for f in flags:
        print(f"{f['type']:<10}{str(f['shot']):<14}{f['t0']:>7}{f['t1']:>7}  {f['value']} ({f['note']})")
    print(f"✓ {args.out}  ({len(flags)} flagged spans in {len(fr)} frames)")


if __name__ == "__main__":
    main()
