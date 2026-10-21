#!/usr/bin/env python3
"""Measure a reference reel and OUR cut the same way, and compare them (the teardown loop).

analyze_footage.py --reference measures only the reference. This puts both side by side, so the
question "are we cutting like the reel the director loves?" gets numbers, not impressions.

Measured per video (identical method for both):
  pacing    cuts (scene change ≥ --threshold, default 0.15 as in analyze_footage), cuts per minute,
            average / median / shortest / longest shot, first cut
  motion    mean frame-to-frame change at 5 fps (how busy the picture is), and its peak
  picture   mean luma, contrast (p02–p98), saturation, warm/cool
  sound     integrated loudness (LUFS), loudness range (LRA), true peak
  sheet     contact sheet, one tile every --every seconds (for what pixels can't count: type, faces, graphics)
Pixels can't tell you about on-screen words, captions or what the audio says. Count those by eye on the sheets.

Usage:
  ./.venv/bin/python scripts/teardown.py --ref projects/<reel>/references/ref1.mp4 --ours projects/<reel>/renders/exports/<reel>_v3_mix.mp4 \
      -o projects/<reel>/analysis/teardown_v3
  ./.venv/bin/python scripts/teardown.py --ref a.mp4 --ref b.mp4 --ours v3.mp4 -o ...     (several references)
  ./.venv/bin/python scripts/teardown.py --ref ref1.mp4 -o projects/<reel>/analysis/teardown   (Phase 1: references only, targets)
Writes <out>/<name>/report.json + sheet.png per video, and <out>/COMPARE.md (with --ours) or <out>/TEARDOWN.md (references only).
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np

SW, SH = 135, 240  # small 9:16 analysis frames


def probe(path: Path) -> tuple[float, float]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=avg_frame_rate:format=duration", "-of", "json", str(path)], capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    rate = ((d.get("streams") or [{}])[0].get("avg_frame_rate") or "25/1").splitlines()[0]
    n, den = rate.split("/")
    return (float(n) / float(den) if float(den) else 25.0), float(d.get("format", {}).get("duration", 0))


def frames(path: Path, fps: float) -> np.ndarray:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(path), "-vf", f"fps={fps},scale={SW}:{SH}", "-pix_fmt", "rgb24",
                          "-f", "rawvideo", "-"], capture_output=True).stdout
    a = np.frombuffer(raw, np.uint8)
    return a[: a.size // (SW * SH * 3) * SW * SH * 3].reshape(-1, SH, SW, 3).astype(np.float32) / 255


def measure(video: Path, out: Path, threshold: float, every: float) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    fps, dur = probe(video)
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(video), "-vf", f"select='gt(scene,{threshold})',showinfo",
                          "-an", "-f", "null", "-"], capture_output=True, text=True).stderr
    cuts = [float(x) for x in re.findall(r"pts_time:([\d.]+)", err)]
    bounds = [0.0] + cuts + [dur]
    spans = [b - a for a, b in zip(bounds, bounds[1:])]
    flashes = sum(1 for x in spans if x < 0.12)        # a flash or a 1–2 frame transition reads as two cuts
    shots = [x for x in spans if x >= 0.12]

    f5 = frames(video, 5)
    y = f5 @ np.array([0.2126, 0.7152, 0.0722], np.float32)
    diff = np.abs(np.diff(y, axis=0)).mean((1, 2)) * 255 if len(y) > 1 else np.zeros(1)
    mx, mn = f5.max(3), f5.min(3)
    sat = np.where(mx > 0.05, (mx - mn) / np.maximum(mx, 1e-3), 0)
    yflat = y.reshape(len(y), -1)

    eb = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(video), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"],
                        capture_output=True, text=True).stderr
    def last(pat: str) -> float | None:
        m = re.findall(pat, eb)
        return float(m[-1]) if m and m[-1] != "-inf" else None

    tiles = max(int(dur // every), 1)
    cols = min(8, tiles)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(video), "-vf",
                    f"fps=1/{every},scale=-2:320,tile={cols}x{(tiles + cols - 1) // cols}", "-frames:v", "1", str(out / "sheet.png")])  # keeps the aspect: landscape refs too

    rep = {
        "video": str(video), "duration_s": round(dur, 2), "fps": round(fps, 3),
        "pacing": {"cuts": len(shots) - 1 if shots else 0, "flashes": flashes,
                   "cuts_per_min": round((len(shots) - 1) / dur * 60, 1) if dur and shots else 0,
                   "avg_shot_s": round(float(np.mean(shots)), 2) if shots else None,
                   "median_shot_s": round(float(np.median(shots)), 2) if shots else None,
                   "shortest_s": round(min(shots), 2) if shots else None, "longest_s": round(max(shots), 2) if shots else None,
                   "first_cut_s": round(cuts[0], 2) if cuts else None, "cut_times": [round(c, 2) for c in cuts]},
        "motion": {"mean_change": round(float(diff.mean()), 2), "p90_change": round(float(np.percentile(diff, 90)), 2)},
        "picture": {"luma": round(float(y.mean()), 3),
                    "contrast": round(float(np.mean(np.percentile(yflat, 98, axis=1) - np.percentile(yflat, 2, axis=1))), 3),
                    "saturation": round(float(sat.mean()), 3),
                    "warm_cool": round(float((f5[..., 0] - f5[..., 2]).mean()), 3)},
        "sound": {"lufs": last(r"I:\s+(-?[\d.]+) LUFS"), "lra": last(r"LRA:\s+(-?[\d.]+) LU"), "true_peak": last(r"Peak:\s+(-?[\d.]+|-inf) dBFS")},
        "sheet": str(out / "sheet.png"),
    }
    (out / "report.json").write_text(json.dumps(rep, indent=1))
    return rep


ROWS = [  # (label, path, unit, tolerance for a "differs" flag as a relative fraction, or None to only show)
    ("Duration", ("duration_s",), "s", None),
    ("Cuts per minute", ("pacing", "cuts_per_min"), "", 0.25),
    ("Average shot", ("pacing", "avg_shot_s"), "s", 0.25),
    ("Median shot", ("pacing", "median_shot_s"), "s", 0.25),
    ("Shortest shot", ("pacing", "shortest_s"), "s", None),
    ("Flashes / 1–2 frame transitions", ("pacing", "flashes"), "", None),
    ("Longest shot", ("pacing", "longest_s"), "s", 0.5),
    ("First cut", ("pacing", "first_cut_s"), "s", 0.5),
    ("Motion (mean change)", ("motion", "mean_change"), "", 0.3),
    ("Motion (p90)", ("motion", "p90_change"), "", 0.3),
    ("Luma", ("picture", "luma"), "", 0.2),
    ("Contrast (p98−p02)", ("picture", "contrast"), "", 0.15),
    ("Saturation", ("picture", "saturation"), "", 0.2),
    ("Warm/cool (R−B)", ("picture", "warm_cool"), "", None),
    ("Loudness", ("sound", "lufs"), "LUFS", None),
    ("Loudness range", ("sound", "lra"), "LU", None),
    ("True peak", ("sound", "true_peak"), "dBTP", None),
]


def get(rep: dict, path: tuple) -> float | None:
    for k in path:
        rep = rep.get(k) if isinstance(rep, dict) else None
    return rep  # type: ignore[return-value]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--ref", type=Path, action="append", required=True, help="a reference video (repeatable)")
    ap.add_argument("--ours", type=Path, help="our export (leave out in Phase 1 to measure references only)")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--threshold", type=float, default=0.15)
    ap.add_argument("--every", type=float, default=1.0, help="contact-sheet tile spacing (s)")
    args = ap.parse_args()

    reps = []
    for v in [*args.ref, *([args.ours] if args.ours else [])]:
        print(f"▸ measuring {v.name}", flush=True)
        reps.append(measure(v, args.out / v.stem, args.threshold, args.every))
    if not args.ours:  # Phase 1: the reference numbers become the brief's targets
        fmt = lambda x, u: "–" if x is None else f"{x}{(' ' + u) if u else ''}"
        md = [f"# Teardown: {len(reps)} reference(s)", "", f"Scene threshold {args.threshold}. Put these in the brief as targets; "
              "rerun with --ours on each export to compare.", "",
              "| Measure | " + " | ".join(f"ref: {Path(r['video']).stem}" for r in reps) + " |", "|" + "---|" * (len(reps) + 1)]
        md += [f"| {label} | " + " | ".join(fmt(get(r, path), unit) for r in reps) + " |" for label, path, unit, _ in ROWS]
        md += ["", "## Contact sheets (count by eye: on-screen words, captions, graphics, faces, transitions)", ""]
        md += [f"- `{Path(r['sheet']).relative_to(args.out)}`" for r in reps]
        (args.out / "TEARDOWN.md").write_text("\n".join(md) + "\n")
        print("\n".join(md[4:]))
        print(f"✓ {args.out / 'TEARDOWN.md'}")
        return
    refs, ours = reps[:-1], reps[-1]

    head = "| Measure | " + " | ".join(f"ref: {Path(r['video']).stem}" for r in refs) + " | **ours** | Read |"
    md = [f"# Teardown: `{Path(ours['video']).name}` vs {len(refs)} reference(s)", "",
          "Same method for every video (scene threshold "
          f"{args.threshold}). Flags mark where ours differs from the reference average by more than the tolerance. "
          "A flag is a question for the brief, not an error: the director may want us to differ.", "",
          head, "|" + "---|" * (len(refs) + 3)]
    flags = []
    for label, path, unit, tol in ROWS:
        rv = [get(r, path) for r in refs]
        ov = get(ours, path)
        vals = [x for x in rv if isinstance(x, (int, float))]
        read = ""
        if tol is not None and vals and isinstance(ov, (int, float)) and np.mean(vals):
            rel = (ov - np.mean(vals)) / abs(np.mean(vals))
            if abs(rel) > tol:
                read = f"ours {rel:+.0%}"
                flags.append(f"{label}: ours {ov} vs reference {np.mean(vals):.2f} ({rel:+.0%})")
        fmt = lambda x: "–" if x is None else f"{x}{(' ' + unit) if unit else ''}"
        md.append(f"| {label} | " + " | ".join(fmt(x) for x in rv) + f" | **{fmt(ov)}** | {read} |")
    md += ["", "## Biggest differences", ""] + ([f"- {f}" for f in flags] or ["- none beyond tolerance"])
    md += ["", "## Contact sheets (count by eye: on-screen words, captions, graphics, faces, transitions)", ""]
    md += [f"- `{Path(r['sheet']).relative_to(args.out)}`" for r in reps]
    (args.out / "COMPARE.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[4: 4 + len(ROWS) + 2]))
    print(f"✓ {args.out / 'COMPARE.md'}")


if __name__ == "__main__":
    main()
