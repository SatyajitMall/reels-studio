#!/usr/bin/env python3
"""Measure per-shot camera shake in a clip or an export.

Tracks frame-to-frame translation (phase correlation with sub-pixel peak), integrates it into a
camera path, and treats what's left after removing the smooth path (Gaussian σ = 6 frames, i.e.
the faster-than-about-3-Hz part) as shake. Reports per shot: jitter RMS and max (px in 1080-wide
space), p95 frame-to-frame jerk, the smooth pan speed, and when the worst moment is.

There's no fixed "shaky" threshold. Fast pans also leave residual, so read pan_px_s alongside.
Use it to (1) rank shots and pick stabilisation candidates, then judge them by eye, and (2) compare
the same shots before and after stabilising: jit_rms and jerk_p95 should drop. On my-reel v6, steady
holds measured 0.5–1.7 px jit_rms, and handheld pans 6–28 px.

Shots come from --shots (JSON list of [name, start_s, end_s] in the video's time) or, if omitted,
consecutive --window second slices.

Usage:
  ./.venv/bin/python scripts/shake_report.py projects/<reel>/renders/exports/<reel>_v3.mp4 \
      -o projects/<reel>/analysis/shake_v3.json [--shots projects/<reel>/analysis/shots_v3.json]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy.ndimage import gaussian_filter1d

sys.path.insert(0, str(Path(__file__).resolve().parent))
from media_info import fps_of  # noqa: E402  (robust on rotation-tagged camera files)

W, H = 270, 480
SCALE = 1080 / W
EDGE = 3  # frames ignored at each shot edge (cuts / transitions)


def shift(a: np.ndarray, b: np.ndarray, win: np.ndarray) -> tuple[float, float]:
    A = np.fft.fft2((a - a.mean()) * win)
    B = np.fft.fft2((b - b.mean()) * win)
    R = A * np.conj(B)
    R /= np.abs(R) + 1e-6
    c = np.fft.ifft2(R).real
    y, x = np.unravel_index(c.argmax(), c.shape)

    def sub(cm: float, c0: float, cp: float) -> float:
        d = cm - 2 * c0 + cp
        return 0.0 if d == 0 else 0.5 * (cm - cp) / d
    yy = y + sub(c[(y - 1) % H, x], c[y, x], c[(y + 1) % H, x])
    xx = x + sub(c[y, (x - 1) % W], c[y, x], c[y, (x + 1) % W])
    if yy > H / 2:
        yy -= H
    if xx > W / 2:
        xx -= W
    return xx * SCALE, yy * SCALE


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True, help="output .json (a .npy of raw shifts is saved beside it)")
    ap.add_argument("--shots", type=Path, help="JSON list of [name, start_s, end_s]")
    ap.add_argument("--window", type=float, default=2.0, help="slice length when --shots is omitted")
    args = ap.parse_args()

    fps = fps_of(args.video)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(args.video), "-vf", f"scale={W}:{H},format=gray",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    fr = fr[: fr.size // (W * H) * W * H].reshape(-1, H, W).astype(np.float32)
    win = np.outer(np.hanning(H), np.hanning(W)).astype(np.float32)
    d = np.array([shift(fr[i], fr[i + 1], win) for i in range(len(fr) - 1)])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.out.with_suffix(".npy"), d)

    dur = len(fr) / fps
    shots = json.loads(args.shots.read_text()) if args.shots else \
        [[f"{t:.1f}s", t, min(t + args.window, dur)] for t in np.arange(0, dur, args.window)]
    res = []
    for name, a, b in shots:
        i0, i1 = int(round(a * fps)) + EDGE, int(round(b * fps)) - EDGE
        seg = d[i0:i1]
        if len(seg) < 8:
            continue
        tx, ty = np.cumsum(seg[:, 0]), np.cumsum(seg[:, 1])
        jx, jy = tx - gaussian_filter1d(tx, 6), ty - gaussian_filter1d(ty, 6)
        j = np.hypot(jx, jy)
        jerk = np.hypot(np.diff(jx), np.diff(jy))
        pan = np.hypot(gaussian_filter1d(seg[:, 0], 6).mean(), gaussian_filter1d(seg[:, 1], 6).mean()) * fps
        res.append({"shot": name, "t": [round(float(a), 2), round(float(b), 2)],
                    "jit_rms": round(float(np.sqrt((j ** 2).mean())), 2), "jit_max": round(float(j.max()), 2),
                    "jerk_p95": round(float(np.percentile(jerk, 95)), 2), "pan_px_s": round(float(pan), 1),
                    "worst_t": round(float(a) + (EDGE + int(j.argmax())) / fps, 2)})
    args.out.write_text(json.dumps(res, indent=1))
    print(f"{'shot':<12}{'jit_rms':>8}{'jit_max':>8}{'jerk95':>8}{'pan/s':>8}  worst")
    for r in sorted(res, key=lambda r: -r["jit_rms"]):
        print(f"{r['shot']:<12}{r['jit_rms']:>8}{r['jit_max']:>8}{r['jerk_p95']:>8}{r['pan_px_s']:>8}  "
              f"{r['worst_t']}")
    print(f"✓ {args.out}")


if __name__ == "__main__":
    main()
