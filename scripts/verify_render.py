#!/usr/bin/env python3
"""Check the EXPORTED FILE before it goes to the director or Instagram (the last gate, after the review gate).

frame_scan.py and the review gate judge the pictures; this checks the encoded file itself:
  video     codec, 1080×1920, frame rate (--fps), bitrate (≥ 8 Mb/s), 8-bit 4:2:0, BT.709 colour tags
            (missing tags make some players show faces redder; --fix-tags writes a tagged copy, lossless)
  black     black runs (blackdetect). Any run counts unless it's in the last --fade-end seconds (a designed fade)
  freeze    frozen stretches ≥ 0.5 s (freezedetect): a warning, since a hold can be deliberate
  timing    duration vs --expect (±1 frame); audio vs video length (≤ 0.12 s)
  audio     present and not silent; loudness by profile:
              mix       integrated −14 LUFS ±2 (Instagram normalises around there) and true peak ≤ −1 dBTP
              ig-quiet  the no-music upload version (the music is added in Instagram): true peak ≤ −1 dBTP only
Writes VERIFY.md and render-sheet.png next to the file (or into --out). Exit 1 if any check FAILs.

Usage:
  ./.venv/bin/python scripts/verify_render.py projects/<reel>/renders/exports/<reel>_v3_mix.mp4 [--fps 25] [--expect 49.76]
  ./.venv/bin/python scripts/verify_render.py <reel>_v3_IG.mp4 --profile ig-quiet
  ./.venv/bin/python scripts/verify_render.py <file> --fix-tags        # writes <file>_tagged.mp4
  ./.venv/bin/python scripts/verify_render.py <file> --fix-loudness    # mix profile: writes <file>_-14LUFS.mp4 (picture copied)
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


def run(cmd: list[str]) -> str:
    p = subprocess.run(cmd, capture_output=True, text=True)
    return p.stdout + p.stderr


def probe(path: Path) -> dict:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                          "stream=index,codec_type,codec_name,width,height,avg_frame_rate,bit_rate,pix_fmt,color_space,"
                          "color_transfer,color_primaries,duration:format=duration,bit_rate", "-of", "json", str(path)],
                         capture_output=True, text=True).stdout
    return json.loads(out or "{}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("file", type=Path)
    ap.add_argument("--profile", choices=["mix", "ig-quiet"], default="mix")
    ap.add_argument("--fps", type=float, help="expected frame rate (the reel's sequence rate)")
    ap.add_argument("--expect", type=float, help="expected duration in seconds")
    ap.add_argument("--fade-end", type=float, default=1.0, help="black allowed in the last N s (designed fade)")
    ap.add_argument("--out", type=Path, help="folder for VERIFY.md / render-sheet.png (default: next to the file)")
    ap.add_argument("--fix-tags", action="store_true", help="write a BT.709-tagged copy (lossless remux)")
    ap.add_argument("--fix-loudness", action="store_true", help="mix profile: write a copy at −14 LUFS, true peak ≤ −1 (video copied)")
    args = ap.parse_args()

    f = args.file
    if not f.exists():
        sys.exit(f"No file {f}")
    info = probe(f)
    v = next((s for s in info.get("streams", []) if s.get("codec_type") == "video"), {})
    a = next((s for s in info.get("streams", []) if s.get("codec_type") == "audio"), None)
    dur = float(info.get("format", {}).get("duration", 0))
    rows: list[tuple[str, str, str]] = []  # (status, check, detail)

    def add(ok: bool | None, check: str, detail: str) -> None:
        rows.append(("PASS" if ok else "WARN" if ok is None else "FAIL", check, detail))

    # Video basics
    n, d = (v.get("avg_frame_rate") or "0/1").split("/")
    fps = float(n) / float(d) if float(d) else 0.0
    add(v.get("codec_name") in ("h264", "hevc"), "codec", f"{v.get('codec_name')} (Instagram wants H.264 or HEVC)")
    add((v.get("width"), v.get("height")) == (1080, 1920), "resolution", f"{v.get('width')}×{v.get('height')} (expected 1080×1920)")
    if args.fps:
        add(abs(fps - args.fps) < 0.01, "frame rate", f"{fps:g} fps (expected {args.fps:g})")
    else:
        add(True, "frame rate", f"{fps:g} fps")
    vbr = float(v.get("bit_rate") or info.get("format", {}).get("bit_rate") or 0) / 1e6
    add(vbr >= 8 if vbr else None, "video bitrate", f"{vbr:.1f} Mb/s (≥ 8 keeps detail through Instagram's re-encode)")
    add(v.get("pix_fmt") in ("yuv420p", "yuvj420p"), "pixel format", f"{v.get('pix_fmt')} (8-bit 4:2:0 is the safe upload format)")
    tags = (v.get("color_primaries"), v.get("color_transfer"), v.get("color_space"))
    tag_ok = tags == ("bt709", "bt709", "bt709")
    add(tag_ok, "BT.709 tags", f"primaries/transfer/matrix = {'/'.join(str(t) for t in tags)}" + ("" if tag_ok else " → run with --fix-tags"))

    # Timing
    if args.expect:
        add(abs(dur - args.expect) <= 1.0 / (fps or 25) + 1e-3, "duration", f"{dur:.3f} s (expected {args.expect:.3f} ± 1 frame)")
    else:
        add(True, "duration", f"{dur:.3f} s")
    if a:
        adur = float(a.get("duration") or dur)
        vdur = float(v.get("duration") or dur)
        add(abs(adur - vdur) <= 0.12, "audio/video length", f"audio {adur:.3f} s vs video {vdur:.3f} s")

    # Black and frozen runs (on a downscaled decode; fast)
    bd = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-vf", "scale=270:-2,blackdetect=d=0.08:pix_th=0.08", "-an", "-f", "null", "-"])
    blacks = [(float(s), float(e)) for s, e in re.findall(r"black_start:([\d.]+) black_end:([\d.]+)", bd)]
    bad_black = [(s, e) for s, e in blacks if s < dur - args.fade_end]
    add(not bad_black, "black frames",
        "none" if not blacks else "; ".join(f"{s:.2f}–{e:.2f} s{' (end fade)' if (s, e) not in bad_black else ''}" for s, e in blacks))
    fz = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-vf", "scale=270:-2,freezedetect=n=0.003:d=0.5", "-an", "-f", "null", "-"])
    starts = re.findall(r"freeze_start: ([\d.]+)", fz)
    ends = re.findall(r"freeze_end: ([\d.]+)", fz)
    freezes = [(float(s), float(e) if i < len(ends) else dur) for i, (s, e) in enumerate(zip(starts, ends + [str(dur)] * len(starts)))]
    add(None if freezes else True, "frozen stretches",
        "none" if not freezes else "; ".join(f"{s:.2f}–{e:.2f} s" for s, e in freezes) + " (deliberate hold? check)")

    # Audio
    lufs = tp = None
    if not a:
        add(args.profile == "ig-quiet" and None, "audio", "no audio track")
    else:
        eb = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(f), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
        m_i = re.findall(r"I:\s+(-?[\d.]+) LUFS", eb)
        m_tp = re.findall(r"Peak:\s+(-?[\d.]+|-inf) dBFS", eb)
        lufs = float(m_i[-1]) if m_i else None
        tp = float(m_tp[-1]) if m_tp and m_tp[-1] != "-inf" else None
        silent = tp is None or tp < -45
        add(not silent, "audio present", "silent" if silent else f"true peak {tp:.1f} dBTP")
        if tp is not None:
            add(tp <= -1.0, "true peak", f"{tp:.1f} dBTP (≤ −1 so Instagram's encode doesn't clip)")
        if args.profile == "mix" and lufs is not None:
            add(None if not (-16 <= lufs <= -12) else True, "loudness",
                f"{lufs:.1f} LUFS integrated (target −14 ± 2; Instagram turns louder files down, quieter ones play quiet)")
        elif lufs is not None:
            add(True, "loudness", f"{lufs:.1f} LUFS (no-music upload version: not judged)")

    # Sheet: 5 frames across the file
    out_dir = args.out or f.parent
    out_dir.mkdir(parents=True, exist_ok=True)
    stem = f.stem
    sheet = out_dir / f"{stem}_render-sheet.png"
    picks = [0.05, dur * 0.25, dur * 0.5, dur * 0.75, max(dur - 0.05, 0)]
    inputs = []
    for t in picks:
        inputs += ["-ss", f"{t:.3f}", "-i", str(f)]
    run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
         "".join(f"[{i}:v]scale=216:384,setsar=1[v{i}];" for i in range(5)) + "".join(f"[v{i}]" for i in range(5)) + "hstack=inputs=5",
         "-frames:v", "1", str(sheet)])

    if args.fix_tags and not tag_ok:
        bsf = "hevc_metadata" if v.get("codec_name") == "hevc" else "h264_metadata"
        fixed = f.with_name(f.stem + "_tagged" + f.suffix)
        run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-map", "0", "-c", "copy", "-bsf:v",
             f"{bsf}=colour_primaries=1:transfer_characteristics=1:matrix_coefficients=1",
             "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", str(fixed)])
        rows.append(("INFO", "fix-tags", f"wrote {fixed.name}; re-run the check on it"))

    if args.fix_loudness and args.profile == "mix" and lufs is not None and not (-15 <= lufs <= -13):
        gain = -14.0 - lufs
        fixed = f.with_name(f"{f.stem}_-14LUFS{f.suffix}")
        run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-map", "0:v", "-map", "0:a", "-c:v", "copy",
             "-af", f"volume={gain:.2f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac", "-b:a", "320k", str(fixed)])
        eb2 = run(["ffmpeg", "-hide_banner", "-nostats", "-i", str(fixed), "-vn", "-af", "ebur128=peak=true", "-f", "null", "-"])
        i2 = re.findall(r"I:\s+(-?[\d.]+) LUFS", eb2); p2 = re.findall(r"Peak:\s+(-?[\d.]+) dBFS", eb2)
        rows.append(("INFO", "fix-loudness", f"wrote {fixed.name}: {gain:+.1f} dB → {i2[-1] if i2 else '?'} LUFS, "
                                              f"true peak {p2[-1] if p2 else '?'} dBTP; re-run the check on it"))

    fails = [r for r in rows if r[0] == "FAIL"]
    md = [f"# VERIFY: `{f.name}`", "", f"Profile **{args.profile}** · {'**FAIL**' if fails else 'PASS'} · sheet `{sheet.name}`", "",
          "| Result | Check | Detail |", "|---|---|---|"] + [f"| {s} | {c} | {d} |" for s, c, d in rows]
    report = out_dir / f"{stem}_VERIFY.md"
    report.write_text("\n".join(md) + "\n")
    for s, c, d in rows:
        print(f"{s:<5} {c:<20} {d}")
    print(f"{'✗ FAIL' if fails else '✓ PASS'}  {report}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
