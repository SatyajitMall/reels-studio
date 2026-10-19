#!/usr/bin/env python3
"""Prepare sound effects so they mix predictably and land on their cue.

Library SFX differ up to ~10× in level and often start with silence, so at one clip gain some vanish and
others land late. For each file this writes a prepared copy (originals are never touched):
  - trims the leading silence (below --floor, default −40 dBFS), so the AUDIBLE peak sits at the file's start
    and the clip can be placed exactly on its cue frame
  - peak-normalises to --peak (default −3 dBFS); the mix level is then set per use with the clip's gain
  - reports where the transient now sits (it should be within ~2 frames of 0)
Output: <out_dir>/<name>.wav (48 kHz, stereo, 16-bit) and <out_dir>/sfx_prep.json.

Usage:
  ./.venv/bin/python scripts/sfx_prep.py assets/sfx/*.wav -o assets/sfx/prepared
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path


def max_volume(path: Path) -> float | None:
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    m = re.search(r"max_volume:\s*(-?[\d.]+) dB", err)
    return float(m.group(1)) if m else None


def peak_time(path: Path) -> float:
    """Time of the loudest 10 ms window (the transient)."""
    err = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(path), "-af",
                          "asetnsamples=480,astats=metadata=1:reset=1,ametadata=print:key=lavfi.astats.Overall.Peak_level",
                          "-f", "null", "-"], capture_output=True, text=True).stderr
    best_t, best = 0.0, -1e9
    t = None
    for line in err.splitlines():
        m = re.search(r"pts_time:([\d.]+)", line)
        if m:
            t = float(m.group(1))
        m = re.search(r"Peak_level=(-?[\d.]+|-inf)", line)
        if m and t is not None and m.group(1) != "-inf" and float(m.group(1)) > best:
            best, best_t = float(m.group(1)), t
    return best_t


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--peak", type=float, default=-3.0, help="target peak in dBFS")
    ap.add_argument("--floor", type=float, default=-40.0, help="leading-silence threshold in dBFS")
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    report = []
    for f in args.files:
        if f.name.startswith("._") or not f.is_file():
            continue
        before_peak_t = peak_time(f)
        tmp = args.out / f"_{f.stem}_trim.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-af",
                        f"silenceremove=start_periods=1:start_threshold={args.floor}dB:start_silence=0.005",
                        "-ar", "48000", "-ac", "2", str(tmp)], check=True)
        mv = max_volume(tmp)
        gain = 0.0 if mv is None else args.peak - mv
        out = args.out / f"{f.stem}.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-af", f"volume={gain:.2f}dB", "-c:a", "pcm_s16le", str(out)], check=True)
        tmp.unlink(missing_ok=True)
        after_t = peak_time(out)
        row = {"file": f.name, "out": str(out), "peak_before_dbfs": mv, "gain_db": round(gain, 2),
               "transient_before_s": round(before_peak_t, 3), "transient_after_s": round(after_t, 3)}
        report.append(row)
        print(f"✓ {f.name:<34} gain {gain:+6.1f} dB · transient {before_peak_t:.3f}s → {after_t:.3f}s")
    (args.out / "sfx_prep.json").write_text(json.dumps(report, indent=1))
    print(f"✓ {len(report)} prepared → {args.out}")


if __name__ == "__main__":
    main()
