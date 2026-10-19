#!/usr/bin/env python3
"""Make an outside clip (AI-generated, stock) or a still reel-ready before it goes into Premiere.

What it does:
  - frame rate: retimes frame-for-frame to the reel's rate (24 → 25 plays every frame once, about 4 % faster,
    the same as Premiere's interpretation). Never duplicates or blends frames.
  - skips the model's "settle-in" (--start, default 0.5 s for generated clips: the first frames often warp into place)
  - scales and crops to 1080×1920, strips audio, writes ProRes 422 HQ with BT.709 tags
  - --match <still from our footage>: nudges the clip's colour toward our footage (per-channel mean/contrast
    transfer as a 3D LUT, at --strength, default 0.5), so a generated shot sits next to real ones. It's a nudge,
    not a grade: primary correction and the look still happen in Premiere as for any clip.
  - a still image becomes a slow push-in (--push 1.06) of --dur seconds
Writes <out>.mov and <out>_sheet.png (first / middle / last frame, plus the match still if given).

Usage:
  ./.venv/bin/python scripts/conform_clip.py projects/<reel>/renders/gen/<shot>.mp4 -o projects/<reel>/renders/gen/<shot>_conformed \
      [--fps 25] [--start 0.5] [--dur 3.5] [--match still_from_our_footage.png] [--strength 0.5]
  ./.venv/bin/python scripts/conform_clip.py frame.png -o ... --dur 4 --push 1.06        (still → push-in)
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image

W, H = 1080, 1920
IMG_EXT = {".png", ".jpg", ".jpeg", ".webp", ".tif", ".tiff"}


def probe_fps_dur(path: Path) -> tuple[float, float]:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries",
                          "stream=avg_frame_rate:format=duration", "-of", "json", str(path)], capture_output=True, text=True).stdout
    d = json.loads(out or "{}")
    n, den = ((d.get("streams") or [{}])[0].get("avg_frame_rate") or "25/1").split("/")
    return (float(n) / float(den) if float(den) else 25.0), float(d.get("format", {}).get("duration", 0))


def frame(path: Path, t: float, tmp: Path, name: str) -> np.ndarray:
    p = tmp / f"{name}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{t:.3f}", "-i", str(path), "-frames:v", "1",
                    "-vf", f"scale={W}:{H}:force_original_aspect_ratio=increase,crop={W}:{H}", str(p)], check=True)
    return np.asarray(Image.open(p).convert("RGB")).astype(np.float32) / 255


def write_match_lut(clip_frames: list[np.ndarray], ref: np.ndarray, strength: float, cube: Path, size: int = 17) -> dict:
    """Per-channel mean/std transfer (clip → ref), blended by strength, written as a .cube LUT."""
    src = np.concatenate([f.reshape(-1, 3) for f in clip_frames])
    dst = ref.reshape(-1, 3)
    mu_s, sd_s = src.mean(0), src.std(0) + 1e-4
    mu_d, sd_d = dst.mean(0), dst.std(0) + 1e-4
    gain = 1 + strength * (sd_d / sd_s - 1)
    g = np.linspace(0, 1, size, dtype=np.float32)
    b, gg, r = np.meshgrid(g, g, g, indexing="ij")
    rgb = np.stack([r, gg, b], -1).reshape(-1, 3)
    target = (rgb - mu_s) * gain + mu_s + strength * (mu_d - mu_s)
    out = np.clip(target, 0, 1)
    lines = ["TITLE \"conform match\"", f"LUT_3D_SIZE {size}", "DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1"]
    lines += [f"{x:.6f} {y:.6f} {z:.6f}" for x, y, z in out]
    cube.write_text("\n".join(lines) + "\n")
    return {"clip_mean": [round(float(x), 3) for x in mu_s], "ref_mean": [round(float(x), 3) for x in mu_d],
            "gain": [round(float(x), 3) for x in gain]}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True, help="output path without extension")
    ap.add_argument("--fps", type=float, default=25.0, help="the reel's sequence frame rate")
    ap.add_argument("--start", type=float, default=0.5, help="skip this much of the source (generated clips settle in)")
    ap.add_argument("--dur", type=float, help="output duration in seconds (default: the rest of the clip)")
    ap.add_argument("--match", type=Path, help="a still from the reel's own footage to nudge the colour toward")
    ap.add_argument("--strength", type=float, default=0.5)
    ap.add_argument("--push", type=float, default=1.06, help="still input only: end scale of the slow push-in")
    args = ap.parse_args()

    if not args.src.exists():
        sys.exit(f"No file {args.src}")
    args.out.parent.mkdir(parents=True, exist_ok=True)
    mov = args.out.with_suffix(".mov")
    is_still = args.src.suffix.lower() in IMG_EXT
    report: dict = {"source": str(args.src), "out": str(mov), "fps": args.fps}

    with tempfile.TemporaryDirectory(prefix="conform_") as tmpd:
        tmp = Path(tmpd)
        vf_lut = ""
        if is_still:
            dur = args.dur or 4.0
            frames_n = int(round(dur * args.fps))
            # Ken Burns: zoompan on an upscaled still (upscaling first avoids zoompan's integer-step jitter)
            base = (f"scale={W * 4}:{H * 4}:force_original_aspect_ratio=increase,crop={W * 4}:{H * 4},"
                    f"zoompan=z='1+({args.push}-1)*on/{frames_n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames_n}:s={W}x{H}:fps={args.fps}")
            src_args = ["-loop", "1", "-i", str(args.src)]
            pre = base
            report.update(kind="still", duration_s=dur, push=args.push)
        else:
            src_fps, src_dur = probe_fps_dur(args.src)
            ratio = src_fps / args.fps                       # e.g. 24/25 = 0.96: every frame once, ~4 % faster
            avail = max(src_dur - args.start, 0) * ratio
            dur = min(args.dur or avail, avail)
            if dur <= 0:
                sys.exit("Nothing left after --start.")
            src_args = ["-ss", f"{args.start:.3f}", "-i", str(args.src)]
            pre = (f"setpts=PTS*{ratio:.6f},fps={args.fps},"
                   f"scale={W}:{H}:force_original_aspect_ratio=increase:flags=lanczos,crop={W}:{H}")
            report.update(kind="clip", source_fps=src_fps, retime=f"{src_fps:g} → {args.fps:g} fps frame-for-frame ({(1 / ratio - 1) * 100:+.1f} % speed)",
                          skipped_s=args.start, duration_s=round(dur, 3))
        if args.match:
            sample_t = [args.start + 0.2, args.start + (dur / 2), args.start + max(dur - 0.2, 0.3)] if not is_still else [0]
            clip_frames = [frame(args.src, t, tmp, f"c{i}") for i, t in enumerate(sample_t)]
            ref = np.asarray(Image.open(args.match).convert("RGB").resize((W // 4, H // 4))).astype(np.float32) / 255
            cube = tmp / "match.cube"
            report["match"] = {"still": str(args.match), "strength": args.strength,
                               **write_match_lut([f[::4, ::4] for f in clip_frames], ref, args.strength, cube)}
            vf_lut = f",lut3d=file='{cube}'"
        cmd = ["ffmpeg", "-v", "error", "-y", *src_args, "-t", f"{dur:.3f}", "-an", "-vf", pre + vf_lut + ",format=yuv422p10le,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv",
               "-c:v", "prores_ks", "-profile:v", "3", "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
               "-r", f"{args.fps:g}", "-movflags", "+write_colr", str(mov)]
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0 or not mov.exists():
            sys.exit(f"✗ ffmpeg failed:\n{r.stderr[-800:]}")

        # Sheet: first / middle / last (+ the match still)
        _, out_dur = probe_fps_dur(mov)
        tiles = [frame(mov, t, tmp, f"o{i}") for i, t in enumerate([0.02, out_dur / 2, max(out_dur - 0.05, 0)])]
        if args.match:
            tiles.append(np.asarray(Image.open(args.match).convert("RGB").resize((W, H))).astype(np.float32) / 255)
        strip = np.concatenate([(t * 255).astype(np.uint8) for t in tiles], axis=1)
        sheet = args.out.with_name(args.out.name + "_sheet.png")
        Image.fromarray(strip).resize((strip.shape[1] // 5, strip.shape[0] // 5)).save(sheet)
    report["output_duration_s"] = round(out_dur, 3)
    args.out.with_suffix(".json").write_text(json.dumps(report, indent=1))
    print(f"✓ {mov}  ({out_dur:.2f} s @ {args.fps:g} fps)")
    print(f"  sheet: {sheet}" + ("  (last tile = the match still)" if args.match else ""))
    for k in ("retime", "match"):
        if k in report:
            print(f"  {k}: {report[k] if k == 'retime' else report[k]['gain']}")


if __name__ == "__main__":
    main()
