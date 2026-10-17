#!/usr/bin/env python3
"""Watch a video: sample frames at N fps and tile them into labelled contact sheets.

Use it to look at a reference, a render (the review gate), or B-roll without playing it. Each sheet
covers one shot (with --shots) or one time section, every tile is stamped with its timecode, and an
audio waveform strip of the same span sits under the tiles, so cuts can be checked against hits.

Writes into <out>/:
  sheet_NN.jpg   contact sheets (default 4 columns x up to 16 frames, 9:16 tiles)
  index.md       what each sheet covers, plus video facts. Read this first
  index.json     the same, machine-readable

Usage:
  ./.venv/bin/python scripts/watch.py <video> -o <out_dir> [--fps 2] [--shots shots.json]
                                       [--start S --end S] [--per-sheet 16] [--cols 4] [--tile 270]
--shots: JSON list of [name, start_s, end_s] in the video's time (e.g. the reel's cut plan in reel time).
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=codec_type,width,height,avg_frame_rate:stream_side_data=rotation:format=duration",
                          "-of", "json", str(path)], capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    v = next((s for s in d.get("streams", []) if s.get("codec_type") == "video"), {})
    has_audio = any(s.get("codec_type") == "audio" for s in d.get("streams", []))
    n, den = (v.get("avg_frame_rate") or "0/1").split("/")
    w, h = int(v.get("width", 0)), int(v.get("height", 0))
    rot = next((int(sd["rotation"]) for sd in v.get("side_data_list", []) or [] if "rotation" in sd), 0)
    if abs(rot) in (90, 270):
        w, h = h, w
    return {"duration": float(d.get("format", {}).get("duration", 0)), "width": w, "height": h,
            "fps": round(float(n) / float(den), 3) if float(den) else 0, "audio": has_audio}


def font(size: int) -> ImageFont.ImageFont:
    try:
        return ImageFont.load_default(size=size)
    except TypeError:
        return ImageFont.load_default()


def tc(t: float, fps: float = 0) -> str:
    """mm:ss.hh (hundredths of a second)."""
    cs = int(round(t * 100))
    return f"{cs // 6000:02d}:{(cs // 100) % 60:02d}.{cs % 100:02d}"


def waveform(video: Path, a: float, b: float, width: int, tmp: Path) -> Image.Image | None:
    out = tmp / f"wave_{a:.2f}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{max(b - a, 0.05):.3f}", "-i", str(video),
                    "-filter_complex", f"aformat=channel_layouts=mono,showwavespic=s={width}x110:colors=0x9ad0ff",
                    "-frames:v", "1", str(out)], capture_output=True)
    return Image.open(out).convert("RGB") if out.exists() else None


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("video", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--fps", type=float, default=2.0, help="frames sampled per second")
    ap.add_argument("--shots", type=Path, help="JSON list of [name, start_s, end_s]: one sheet (or more) per shot")
    ap.add_argument("--start", type=float, default=0.0)
    ap.add_argument("--end", type=float, default=None)
    ap.add_argument("--per-sheet", type=int, default=16, help="max frames per sheet")
    ap.add_argument("--cols", type=int, default=4)
    ap.add_argument("--tile", type=int, default=270, help="tile width in px")
    args = ap.parse_args()

    info = probe(args.video)
    end = min(args.end or info["duration"], info["duration"])
    args.out.mkdir(parents=True, exist_ok=True)
    for old in args.out.glob("sheet_*.jpg"):
        old.unlink()

    # Sections: shots, or equal chunks of per-sheet frames.
    if args.shots:
        sections = [(str(n), float(a), float(b)) for n, a, b in json.loads(args.shots.read_text())
                    if float(b) > args.start and float(a) < end]
    else:
        span = args.per_sheet / args.fps
        sections, t = [], args.start
        while t < end - 1e-3:
            sections.append((f"{tc(t, info['fps'])}-{tc(min(t + span, end), info['fps'])}", t, min(t + span, end)))
            t += span

    tile_w = args.tile
    tile_h = int(tile_w * (info["height"] / info["width"])) if info["width"] else int(tile_w * 16 / 9)
    f_lab, f_head = font(18), font(24)
    index = {"video": str(args.video), **info, "sample_fps": args.fps, "sheets": []}
    n_sheet = 0
    with tempfile.TemporaryDirectory() as tmpd:
        tmp = Path(tmpd)
        for name, a, b in sections:
            # Frame times inside the section, centred in each sample slot; at least one per section.
            step = 1.0 / args.fps
            times = [a + step / 2 + i * step for i in range(max(int((b - a) * args.fps), 1))]
            times = [t for t in times if t < b] or [(a + b) / 2]
            for part in range(0, len(times), args.per_sheet):
                chunk = times[part:part + args.per_sheet]
                tiles = []
                for k, t in enumerate(chunk):
                    fp = tmp / f"f_{n_sheet}_{k}.jpg"
                    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(args.video), "-frames:v", "1",
                                    "-vf", f"scale={tile_w}:{tile_h}", str(fp)], capture_output=True)
                    if fp.exists():
                        tiles.append((t, Image.open(fp).convert("RGB")))
                if not tiles:
                    continue
                cols = min(args.cols, len(tiles))
                rows = (len(tiles) + cols - 1) // cols
                head = 40
                sa, sb = chunk[0] - step / 2, min(chunk[-1] + step / 2, b)
                wave = waveform(args.video, sa, sb, cols * tile_w, tmp) if info["audio"] else None
                sheet = Image.new("RGB", (cols * tile_w, head + rows * tile_h + (wave.height + 6 if wave else 0)), (18, 18, 18))
                d = ImageDraw.Draw(sheet)
                d.text((8, 8), f"{name}   {tc(sa, info['fps'])} - {tc(sb, info['fps'])}   ({len(tiles)} frames @ {args.fps:g} fps)",
                       fill=(255, 255, 255), font=f_head)
                for i, (t, img) in enumerate(tiles):
                    x, y = (i % cols) * tile_w, head + (i // cols) * tile_h
                    sheet.paste(img, (x, y))
                    d.rectangle([x, y, x + 96, y + 24], fill=(0, 0, 0))
                    d.text((x + 5, y + 3), tc(t, info["fps"]), fill=(255, 220, 0), font=f_lab)
                if wave:
                    sheet.paste(wave, (0, head + rows * tile_h + 6))
                n_sheet += 1
                path = args.out / f"sheet_{n_sheet:02d}.jpg"
                sheet.save(path, quality=85)
                index["sheets"].append({"file": path.name, "section": name, "start_s": round(sa, 2), "end_s": round(sb, 2),
                                        "frames": len(tiles)})
                print(f"▸ {path.name}  {name}  {sa:.2f}-{sb:.2f}s  ({len(tiles)} frames)", flush=True)

    (args.out / "index.json").write_text(json.dumps(index, indent=1))
    md = [f"# Watch: `{args.video.name}`", "",
          f"{info['width']}×{info['height']}, {info['fps']} fps, {info['duration']:.2f} s, audio: {'yes' if info['audio'] else 'no'}. "
          f"Sampled at {args.fps:g} fps. Each tile is stamped with its timecode; the strip under the tiles is the "
          "audio waveform of the same span (peaks = hits).", "",
          "| Sheet | Section | Start | End | Frames |", "|---|---|---|---|---|"]
    md += [f"| `{s['file']}` | {s['section']} | {s['start_s']} s | {s['end_s']} s | {s['frames']} |" for s in index["sheets"]]
    (args.out / "index.md").write_text("\n".join(md) + "\n")
    print(f"✓ {args.out / 'index.md'}  ({n_sheet} sheets)")


if __name__ == "__main__":
    main()
