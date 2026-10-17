#!/usr/bin/env python3
"""Per-shot colour QA of an export, measured on every frame.

Per shot: mean luma, p02/p98, crushed % (luma < 0.02), clipped % (any channel > 0.98),
saturation, midtone casts (R−B warm/cool, G−M green/magenta), mean midtone hue (degrees),
luma flicker and cast drift. Flags shots that miss the montage targets from the my-reel pilot:
  - luma within ±0.03 of the montage median (shots should sit together),
  - crushed < 25 % (unless it's a true-black sky, which you judge by eye),
  - clipped < 2 %,
  - --gold: midtone hue 30–45° on warm shots (Kodak 2393-style looks push red; fix it with
    look-layer temperature + a little green tint, not by cooling clips, which turns orange pink),
  - blue/cool shots: |G−M| ≤ 0.02.

Flags are prompts to look, not failures. The director-approved my-reel v6 had 16 of 21 shots
flagged, mostly by intent: a dark establishing opener, blue accent shots and true-black skies.
Fix the unintended ones; leave the deliberate ones, and say why in project.md.

Shots come from --shots (JSON list of [name, start_s, end_s]) or consecutive --window slices.

Usage:
  ./.venv/bin/python scripts/colour_report.py projects/<reel>/renders/exports/<reel>_v5.mp4 \
      -o projects/<reel>/analysis/colour_v5.json [--shots shots.json] [--gold]
"""
from __future__ import annotations

import argparse
import colorsys
import json
import subprocess
from pathlib import Path

import numpy as np

W, H = 270, 480
EDGE = 2
KEYS = ["luma", "p02", "p98", "crush%", "clip%", "sat", "R-B", "G-M", "hue"]


def fps_of(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip()
    n, d = (out or "25/1").split("/")
    return float(n) / float(d) if float(d) else 25.0


def stats(f: np.ndarray) -> list[float]:
    r, g, b = f[..., 0], f[..., 1], f[..., 2]
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mx, mn = f.max(2), f.min(2)
    sat = np.where(mx > 0.05, (mx - mn) / np.maximum(mx, 1e-3), 0)
    mid = (y > 0.15) & (y < 0.85)
    if mid.any():
        rb = float((r - b)[mid].mean())
        gm = float((g - (r + b) / 2)[mid].mean())
        hue = colorsys.rgb_to_hsv(float(r[mid].mean()), float(g[mid].mean()), float(b[mid].mean()))[0] * 360
    else:
        rb = gm = hue = 0.0
    return [float(y.mean()), float(np.percentile(y, 2)), float(np.percentile(y, 98)), float((y < 0.02).mean() * 100),
            float((mx > 0.98).mean() * 100), float(sat[y > 0.1].mean()) if (y > 0.1).any() else 0.0, rb, gm, hue]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--shots", type=Path, help="JSON list of [name, start_s, end_s]")
    ap.add_argument("--window", type=float, default=2.0)
    ap.add_argument("--gold", action="store_true", help="check warm shots against the 30–45° gold hue target")
    args = ap.parse_args()

    fps = fps_of(args.video)
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(args.video), "-vf", f"scale={W}:{H}", "-pix_fmt", "rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    fr = np.frombuffer(raw, np.uint8)
    fr = fr[: fr.size // (W * H * 3) * W * H * 3].reshape(-1, H, W, 3).astype(np.float32) / 255
    S = np.array([stats(f) for f in fr])
    args.out.parent.mkdir(parents=True, exist_ok=True)
    np.save(args.out.with_suffix(".npy"), S)

    dur = len(fr) / fps
    shots = json.loads(args.shots.read_text()) if args.shots else \
        [[f"{t:.1f}s", t, min(t + args.window, dur)] for t in np.arange(0, dur, args.window)]
    res = []
    for name, a, b in shots:
        seg = S[int(a * fps) + EDGE: int(b * fps) - EDGE]
        if len(seg) < 3:
            continue
        d = {"shot": name, "t": [round(float(a), 2), round(float(b), 2)]}
        for j, k in enumerate(KEYS):
            d[k] = round(float(seg[:, j].mean()), 3)
        d["luma_flicker"] = round(float(np.abs(np.diff(seg[:, 0])).mean() * 1000), 2)
        d["cast_drift"] = round(float(seg[:, 6].max() - seg[:, 6].min()), 3)
        res.append(d)

    med = float(np.median([d["luma"] for d in res])) if res else 0.0
    for d in res:
        flags = []
        if abs(d["luma"] - med) > 0.03:
            flags.append(f"luma {d['luma'] - med:+.3f} vs montage")
        if d["crush%"] > 25:
            flags.append("crushed > 25 %")
        if d["clip%"] > 2:
            flags.append("clipped > 2 %")
        warm = d["R-B"] > 0.05
        if args.gold and warm and not (30 <= d["hue"] <= 45):
            flags.append(f"hue {d['hue']:.0f}° (gold 30–45°)")
        if d["R-B"] < -0.02 and abs(d["G-M"]) > 0.02:
            flags.append("cool shot with green/magenta cast")
        d["flags"] = flags

    args.out.write_text(json.dumps({"montage_luma_median": round(med, 3), "shots": res}, indent=1))
    print(f"montage luma median {med:.3f}")
    print(f"{'shot':<12}" + "".join(f"{k:>8}" for k in KEYS) + "  flags")
    for d in res:
        print(f"{d['shot']:<12}" + "".join(f"{d[k]:>8.3f}" for k in KEYS) + "  " + "; ".join(d["flags"]))
    print(f"✓ {args.out}  ({sum(1 for d in res if d['flags'])} of {len(res)} shots flagged)")


if __name__ == "__main__":
    main()
