#!/usr/bin/env python3
"""Analyse clips (or reference reels) so Claude can see them without dumping raw video.

For each video it writes, into <out_dir>/<clip_stem>/:
  contact.png   - grid of evenly spaced frames, timecode-stamped
  stats.json    - technical metadata + per-sample exposure / white-balance / saturation readings
and one <out_dir>/summary.md covering every clip (read this first).

With --reference it also detects cuts and reports shot lengths (pacing),
which is how a reference reel is turned into concrete editing parameters.

Usage:
  python scripts/analyze_footage.py projects/<reel>/raw/a-roll projects/<reel>/raw/b-roll -o projects/<reel>/analysis
  python scripts/analyze_footage.py projects/<reel>/references -o projects/<reel>/analysis/references --reference
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mkv", ".avi", ".webm"}
THUMB_W = 270  # 9:16 thumb = 270x480


def probe(path: Path) -> dict:
    out = subprocess.run(
        ["ffprobe", "-v", "error", "-print_format", "json", "-show_format", "-show_streams", str(path)],
        capture_output=True, text=True).stdout
    data = json.loads(out or "{}")
    v = next((s for s in data.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in data.get("streams", []) if s.get("codec_type") == "audio"), None)
    num, den = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = float(num) / float(den) if float(den) else 0.0
    rot = 0
    for sd in v.get("side_data_list", []) or []:
        if "rotation" in sd:
            rot = int(sd["rotation"])
    w, h = int(v.get("width", 0)), int(v.get("height", 0))
    if abs(rot) in (90, 270):
        w, h = h, w
    return {
        "file": path.name,
        "duration_s": round(float(data.get("format", {}).get("duration", 0)), 2),
        "width": w, "height": h,
        "orientation": "vertical" if h > w else "horizontal" if w > h else "square",
        "fps": round(fps, 3),
        "slowmo_headroom": "yes (can slow to ~{:.0f}%)".format(30 / fps * 100) if fps >= 50 else "no",
        "codec": v.get("codec_name"),
        "pix_fmt": v.get("pix_fmt"),
        "bit_depth": 10 if "10" in (v.get("pix_fmt") or "") else 8,
        "color_transfer": v.get("color_transfer"),
        "color_primaries": v.get("color_primaries"),
        "likely_log_or_hdr": (v.get("color_transfer") in ("arib-std-b67", "smpte2084")) or None,
        "has_audio": a is not None,
    }


def grab_frames(path: Path, duration: float, n: int) -> list[tuple[float, Image.Image]]:
    frames = []
    for i in range(n):
        t = duration * (i + 0.5) / n
        raw = subprocess.run(
            ["ffmpeg", "-v", "error", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
             "-vf", f"scale={THUMB_W}:-2", "-f", "image2pipe", "-vcodec", "png", "-"],
            capture_output=True).stdout
        if raw:
            from io import BytesIO
            frames.append((t, Image.open(BytesIO(raw)).convert("RGB")))
    return frames


def frame_stats(img: Image.Image) -> dict:
    a = np.asarray(img).astype(np.float32) / 255.0
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    luma = 0.2126 * r + 0.7152 * g + 0.0722 * b
    mx, mn = a.max(axis=2), a.min(axis=2)
    sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0)
    mid = (luma > 0.15) & (luma < 0.85)  # judge white balance on midtones only
    rm, gm, bm = (float(c[mid].mean()) if mid.any() else float(c.mean()) for c in (r, g, b))
    return {
        "luma_mean": round(float(luma.mean()), 3),
        "luma_p02": round(float(np.percentile(luma, 2)), 3),
        "luma_p98": round(float(np.percentile(luma, 98)), 3),
        "clipped_highlights_pct": round(float((luma > 0.98).mean() * 100), 2),
        "crushed_shadows_pct": round(float((luma < 0.02).mean() * 100), 2),
        "saturation_mean": round(float(sat.mean()), 3),
        "warm_cool": round(rm - bm, 3),     # + warm / - cool
        "green_magenta": round(gm - (rm + bm) / 2, 3),  # + green cast / - magenta
    }


def describe(s: dict) -> list[str]:
    notes = []
    if s["luma_mean"] < 0.30: notes.append("underexposed")
    elif s["luma_mean"] > 0.62: notes.append("bright / possibly overexposed")
    if s["luma_p98"] - s["luma_p02"] < 0.55: notes.append("flat / low contrast (log-like?)")
    if s["clipped_highlights_pct"] > 3: notes.append(f"{s['clipped_highlights_pct']}% clipped highlights")
    if s["crushed_shadows_pct"] > 5: notes.append(f"{s['crushed_shadows_pct']}% crushed shadows")
    if s["warm_cool"] > 0.06: notes.append("warm cast")
    elif s["warm_cool"] < -0.04: notes.append("cool/blue cast")
    if s["green_magenta"] > 0.03: notes.append("green tint")
    elif s["green_magenta"] < -0.03: notes.append("magenta tint")
    if s["saturation_mean"] < 0.15: notes.append("desaturated")
    elif s["saturation_mean"] > 0.45: notes.append("very saturated")
    return notes or ["balanced"]


def contact_sheet(frames: list[tuple[float, Image.Image]], cols: int) -> Image.Image:
    if not frames:
        return Image.new("RGB", (THUMB_W, THUMB_W), "black")
    tw = max(f.width for _, f in frames)
    th = max(f.height for _, f in frames)
    rows = (len(frames) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * tw, rows * th), (20, 20, 20))
    d = ImageDraw.Draw(sheet)
    for i, (t, f) in enumerate(frames):
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(f, (x, y))
        label = f"{int(t // 60):02d}:{t % 60:05.2f}"
        d.rectangle([x, y, x + 78, y + 16], fill=(0, 0, 0))
        d.text((x + 4, y + 2), label, fill=(255, 255, 0))
    return sheet


def detect_cuts(path: Path, threshold: float) -> list[float]:
    err = subprocess.run(
        ["ffmpeg", "-hide_banner", "-i", str(path), "-vf",
         f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"],
        capture_output=True, text=True).stderr
    return [float(m) for m in re.findall(r"pts_time:([0-9.]+)", err)]


def analyse(path: Path, out_dir: Path, n_frames: int, reference: bool, threshold: float) -> dict:
    meta = probe(path)
    d = out_dir / path.stem
    d.mkdir(parents=True, exist_ok=True)
    frames = grab_frames(path, meta["duration_s"], n_frames)
    cols = 6 if meta["orientation"] == "vertical" else 4
    contact_sheet(frames, cols).save(d / "contact.png")
    samples = [{"t": round(t, 2), **frame_stats(f)} for t, f in frames]
    keys = [k for k in samples[0] if k != "t"] if samples else []
    avg = {k: round(float(np.mean([s[k] for s in samples])), 3) for k in keys}
    result = {**meta, "average": avg, "read": describe(avg) if avg else [], "samples": samples,
              "contact_sheet": str(d / "contact.png")}
    if reference:
        cuts = detect_cuts(path, threshold)
        bounds = [0.0] + cuts + [meta["duration_s"]]
        shots = [round(b - a, 2) for a, b in zip(bounds, bounds[1:]) if b - a > 0.05]
        result["pacing"] = {
            "cuts": len(cuts),
            "avg_shot_s": round(float(np.mean(shots)), 2) if shots else None,
            "median_shot_s": round(float(np.median(shots)), 2) if shots else None,
            "shortest_s": min(shots) if shots else None,
            "longest_s": max(shots) if shots else None,
            "first_cut_s": round(cuts[0], 2) if cuts else None,
            "cut_times": [round(c, 2) for c in cuts],
        }
    (d / "stats.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="+", type=Path, help="video files or folders")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("-n", "--frames", type=int, default=12)
    ap.add_argument("--reference", action="store_true", help="also measure pacing (cut detection)")
    ap.add_argument("--scene-threshold", type=float, default=0.15)  # 0.3 missed over half the cuts in a dark night-light reference (v0.2.4)
    args = ap.parse_args()

    files: list[Path] = []
    for p in args.inputs:
        if p.is_dir():
            files += sorted(f for f in p.iterdir()
                           if f.suffix.lower() in VIDEO_EXT and not f.name.startswith("._"))  # skip macOS metadata
        elif p.suffix.lower() in VIDEO_EXT:
            files.append(p)
    if not files:
        sys.exit("No video files found.")

    args.out.mkdir(parents=True, exist_ok=True)
    rows = []
    for f in files:
        print(f"▸ {f.name}", flush=True)
        rows.append(analyse(f, args.out, args.frames, args.reference, args.scene_threshold))

    lines = ["# Footage analysis", "",
             "| Clip | Dur | Res | fps | Slow-mo | Bit depth | Exposure | Contrast range | Warm/Cool | Read |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        a = r["average"]
        lines.append(
            f"| {r['file']} | {r['duration_s']}s | {r['width']}x{r['height']} | {r['fps']} | {r['slowmo_headroom']} | "
            f"{r['bit_depth']} | {a.get('luma_mean')} | {a.get('luma_p02')}–{a.get('luma_p98')} | "
            f"{a.get('warm_cool')} | {', '.join(r['read'])} |")
    if any("pacing" in r for r in rows):
        lines += ["", "## Pacing (references)", "",
                  "| Reference | Cuts | Avg shot | Median | Shortest | First cut |", "|---|---|---|---|---|---|"]
        for r in rows:
            p = r.get("pacing")
            if p:
                lines.append(f"| {r['file']} | {p['cuts']} | {p['avg_shot_s']}s | {p['median_shot_s']}s | "
                             f"{p['shortest_s']}s | {p['first_cut_s']}s |")
    lines += ["", "Exposure = mean luma 0–1 (≈0.40–0.50 is a healthy talking-head). "
              "Warm/Cool: + warm, − cool. Contact sheets: `<clip>/contact.png`."]
    (args.out / "summary.md").write_text("\n".join(lines) + "\n")
    print(f"✓ {args.out / 'summary.md'}")


if __name__ == "__main__":
    main()
