#!/usr/bin/env python3
"""Step-print stutter (the Wong Kar-wai / "Two Sides of Bangkok" chaos beat): each frame is held for 2–3 frames
and smeared by a long shutter, so motion reads as staccato streaks.

Measured on the reference: a new image every 2–3 frames at 30 fps (≈ 12 steps per second), on handheld moves
around a person and on traffic passing close, for 1–4 s at a time. Here:
  long shutter   average --blur consecutive source frames first (3 ≈ a 360° shutter at 12 steps/s); 0 = crisp
  step           keep --step images per second (12 by default)
  hold           re-time to the reel's --fps, so each image holds for 2–3 frames (12 → 25 gives 2,2,2,2,3…)
Writes ProRes 422 HQ with BT.709 tags (a planned effect shot: it replaces the clip at the same timeline position,
as an After Effects render does), and checks the result: it counts how long each image actually holds.

Premiere alternative: the Posterize Time effect (Frame Rate 12) on the clip does the hold, but not the shutter smear.

Usage:
  ./.venv/bin/python scripts/step_print.py raw/b-roll/C186.mov -o renders/fx/C186_step.mov --start 4 --dur 2 --fps 25
  ./.venv/bin/python scripts/step_print.py <clip> -o <out.mov> --step 8 --blur 4      # heavier, choppier
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np


def src_fps(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=avg_frame_rate",
                          "-of", "csv=p=0", str(path)], capture_output=True, text=True).stdout.strip().splitlines()
    n, d = (out[0].strip().strip(",").split(",")[0] if out else "25/1").split("/")  # iPhone files may add a field
    return float(n) / float(d) if float(d) else 25.0


def hold_pattern(path: Path) -> list[int]:
    """Run lengths of identical consecutive frames in the output (what the viewer actually sees)."""
    def decode(extra: list[str]) -> bytes:
        return subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), *extra, "-vf", "scale=96:-2,format=gray",
                               "-f", "rawvideo", "-"], capture_output=True).stdout
    w, h = 96, len(decode(["-frames:v", "1"])) // 96
    fr = np.frombuffer(decode([]), np.uint8)
    frames = fr[: fr.size // (w * h) * w * h].reshape(-1, h, w).astype(np.int16)
    runs, n = [], 1
    for i in range(1, len(frames)):
        if np.abs(frames[i] - frames[i - 1]).mean() < 0.5:
            n += 1
        else:
            runs.append(n)
            n = 1
    runs.append(n)
    return runs


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("clip", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--start", type=float, default=0.0, help="source in-point (s)")
    ap.add_argument("--dur", type=float, help="length (s); default to the end")
    ap.add_argument("--fps", type=float, help="the reel's sequence rate (default: the clip's own)")
    ap.add_argument("--step", type=float, default=12.0, help="new images per second (12 = the reference)")
    ap.add_argument("--blur", type=int, default=3, help="source frames averaged per image (long shutter); 0 or 1 = none")
    a = ap.parse_args()
    if not a.clip.exists():
        sys.exit(f"No clip {a.clip}")
    sfps = src_fps(a.clip)
    fps = a.fps or sfps
    if a.step >= fps:
        sys.exit(f"--step {a.step} must be below the output rate {fps:g}")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    vf = [f"fps={sfps:g}"]
    if a.blur > 1:
        vf.append(f"tmix=frames={a.blur}")
    vf += [f"fps={a.step:g}", f"fps={fps:g}", "format=yuv422p10le",
           "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv"]
    cmd = ["ffmpeg", "-v", "error", "-y", "-ss", f"{a.start}", *(["-t", f"{a.dur}"] if a.dur else []), "-i", str(a.clip), "-map", "0:v:0", "-an", "-dn",
           "-vf", ",".join(vf), "-c:v", "prores_ks", "-profile:v", "3", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-colorspace", "bt709", "-movflags", "+write_colr", str(a.out)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode:
        sys.exit(p.stderr.strip()[:500])
    runs = hold_pattern(a.out)
    inner = runs[1:-1] or runs
    steps_per_s = fps / (sum(inner) / len(inner))
    rep = {"clip": str(a.clip), "out": str(a.out), "start": a.start, "dur": a.dur, "fps": fps, "step": a.step, "blur": a.blur,
           "holds_frames": runs, "measured_steps_per_s": round(steps_per_s, 2)}
    a.out.with_suffix(".json").write_text(json.dumps(rep, indent=1))
    print(f"✓ {a.out}  holds {min(inner)}–{max(inner)} frames → {steps_per_s:.1f} images/s at {fps:g} fps "
          f"(blur {a.blur} frames)")


if __name__ == "__main__":
    main()
