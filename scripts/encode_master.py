#!/usr/bin/env python3
"""Delivery encode: a ProRes master from Premiere → the files the director and Instagram get (studio default, v0.8).

Premiere's "Match Source - High Bitrate" preset gave 9.2–9.5 Mb/s Main-profile H.264 with blocky darks (uski "very poor on the
iPhone", goddess round 5). So Premiere exports a ProRes 422 master, and this makes:

  delivery  H.264 High, yuv420p (TV range), BT.709 tags, x264 -tune film, CRF 16 capped at 20 Mb/s, AAC 320k 48 kHz,
            +faststart. For `_mix` / `_IG` uploads (Instagram: turn on "Upload at highest quality").
            On goddess v10b: 18.5 Mb/s, PSNR 43.0 dB vs the master (37.7 in the shadows); aq-mode 3 gained nothing there.
  phone     --phone: a 2-pass copy sized to fit --max-mb (default 29 MB) for sending a review copy through the Claude app.
            Same picture settings; its bitrate is lower by design (≈ 7 Mb/s at 30 s, ≈ 4.7 at 45 s), so verify it with the
            `--min-mbps` floor this script prints.

The picture is never resized or re-graded here. Then run `scripts/verify_render.py` on the result.

Usage:
  ./.venv/bin/python scripts/encode_master.py renders/masters/<reel>_v3_master.mov -o renders/exports/<reel>_v3_mix.mp4
  ./.venv/bin/python scripts/encode_master.py renders/masters/<reel>_v3_master.mov -o renders/previews/<reel>_v3_phone.mp4 --phone
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

COLOUR = ["-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-color_range", "tv"]
PICTURE = ["-c:v", "libx264", "-profile:v", "high", "-preset", "slow", "-tune", "film", "-pix_fmt", "yuv420p",
           "-vf", "scale=out_range=tv:out_color_matrix=bt709,format=yuv420p,"
                  "setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv", *COLOUR]
# setparams: an untagged master would otherwise come out with primaries/transfer unset (only the matrix tagged)
AUDIO_KBPS = 320


def duration(path: Path) -> float:
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "json", str(path)],
                         capture_output=True, text=True, check=True).stdout
    return float(json.loads(out)["format"]["duration"])


def has_audio(path: Path) -> bool:
    out = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout
    return bool(out.strip())


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("master", type=Path, help="ProRes (or other high-quality) master, 1080×1920")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--phone", action="store_true", help="2-pass review copy that fits --max-mb")
    ap.add_argument("--max-mb", type=float, default=29.0)
    ap.add_argument("--crf", type=float, default=16.0, help="delivery quality (lower = larger); capped at --max-mbps")
    ap.add_argument("--max-mbps", type=float, default=20.0)
    a = ap.parse_args()
    if not a.master.exists():
        sys.exit(f"No master {a.master}")
    a.out.parent.mkdir(parents=True, exist_ok=True)
    aud = ["-c:a", "aac", "-b:a", f"{AUDIO_KBPS}k", "-ar", "48000"] if has_audio(a.master) else ["-an"]
    base = ["ffmpeg", "-v", "error", "-nostats", "-y", "-i", str(a.master), "-map", "0:v:0", "-map", "0:a:0?", *PICTURE]

    kbps = 0
    if not a.phone:
        cmd = [*base, "-crf", f"{a.crf:g}", "-maxrate", f"{a.max_mbps:g}M", "-bufsize", f"{2 * a.max_mbps:g}M", *aud,
               "-movflags", "+faststart", str(a.out)]
        subprocess.run(cmd, check=True)
    else:
        dur = duration(a.master)
        kbps = int(a.max_mb * 8 * 1000 / dur * 0.97 - (AUDIO_KBPS if "-an" not in aud else 0))
        kbps = min(kbps, int(a.max_mbps * 1000))      # a short reel never gets a bigger copy than the delivery cap
        if kbps < 3000:
            sys.exit(f"{a.max_mb} MB over {dur:.1f} s leaves {kbps} kb/s for picture: too low for a fair review copy")
        with tempfile.TemporaryDirectory() as td:
            log = str(Path(td) / "x264")
            subprocess.run([*base, "-b:v", f"{kbps}k", "-pass", "1", "-passlogfile", log, "-an", "-f", "mp4", "/dev/null"], check=True)
            subprocess.run([*base, "-b:v", f"{kbps}k", "-pass", "2", "-passlogfile", log, *aud, "-movflags", "+faststart", str(a.out)],
                           check=True)
    mb = a.out.stat().st_size / 1e6
    floor = f" --min-mbps {kbps * 0.85 / 1000:.1f}" if a.phone else ""
    print(f"✓ {a.out} ({mb:.1f} MB). Next: ./.venv/bin/python scripts/verify_render.py {a.out}{floor}")


if __name__ == "__main__":
    main()
