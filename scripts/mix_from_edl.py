#!/usr/bin/env python3
"""Rebuild a reel's audio mix with ffmpeg and mux it onto Premiere's picture.

Sanctioned fallback for when a Premiere export comes out silent (seen on Premiere 26.5.2, see
premiere-mcp-reality.md). The reel writes its mix plan to analysis/mix.json:

{
  "duration_s": 41.28,
  "music": {"file": "assets/music/track.mp3", "source_start_s": 61.88, "gain_db": -1.0,
            "fade_in_s": 0.0, "fade_out_s": 0.5},
  "sfx": [{"file": "assets/sfx/gemini_riser_sub_hit.wav", "at_s": 1.23, "gain_db": -16},
          {"file": "assets/sfx/gemini_camera_shutter.wav", "at_s": 4.44, "gain_db": -16}],
  "video": "projects/<reel>/renders/exports/<reel>_v1_premiere.mp4",
  "out": "projects/<reel>/renders/exports/<reel>_v1.mp4"
}

Paths are relative to the studio root. Without "video", a 48 kHz stereo WAV is written to "out".
The mix is summed without normalisation and brick-wall limited at -1 dBFS.

Usage: ./.venv/bin/python scripts/mix_from_edl.py projects/<reel>/analysis/mix.json
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    plan = json.loads(Path(sys.argv[1]).read_text())
    dur = float(plan["duration_s"])
    out = ROOT / plan["out"]
    out.parent.mkdir(parents=True, exist_ok=True)

    inputs: list[str] = []
    chains: list[str] = []
    labels: list[str] = []
    video = ROOT / plan["video"] if plan.get("video") else None
    if video:
        inputs += ["-i", str(video)]
    idx = 1 if video else 0

    m = plan.get("music")
    if m:
        inputs += ["-i", str(ROOT / m["file"])]
        fade_in, fade_out = float(m.get("fade_in_s", 0)), float(m.get("fade_out_s", 0))
        chain = (f"[{idx}:a]atrim=start={float(m.get('source_start_s', 0))}:duration={dur},asetpts=PTS-STARTPTS,"
                 f"aformat=sample_rates=48000:channel_layouts=stereo,volume={float(m.get('gain_db', 0))}dB")
        if fade_in > 0:
            chain += f",afade=t=in:d={fade_in}"
        if fade_out > 0:
            chain += f",afade=t=out:st={max(dur - fade_out, 0)}:d={fade_out}"
        chains.append(chain + "[m]")
        labels.append("[m]")
        idx += 1

    for k, s in enumerate(plan.get("sfx", [])):
        inputs += ["-i", str(ROOT / s["file"])]
        ms = int(round(float(s["at_s"]) * 1000))
        chains.append(f"[{idx}:a]aformat=sample_rates=48000:channel_layouts=stereo,"
                      f"volume={float(s.get('gain_db', -16))}dB,adelay={ms}|{ms}[s{k}]")
        labels.append(f"[s{k}]")
        idx += 1

    if not labels:
        sys.exit("mix.json has no music or sfx")
    chains.append(f"{''.join(labels)}amix=inputs={len(labels)}:normalize=0:duration=longest,"
                  f"apad,atrim=duration={dur},alimiter=limit=0.891:level=false[a]")  # 0.891 = -1 dBFS
    graph = ";".join(chains)

    cmd = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", graph]
    if video:
        cmd += ["-map", "0:v:0", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-t", str(dur), str(out)]
    else:
        cmd += ["-map", "[a]", "-c:a", "pcm_s16le", "-ar", "48000", str(out)]
    subprocess.run(cmd, check=True)

    # The check the skill requires after every export: the result must not be silent.
    err = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "volumedetect", "-vn", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    peak = re.search(r"max_volume:\s*(-?[0-9.]+)", err)
    print(f"✓ {out.relative_to(ROOT)}  (max_volume {peak.group(1) if peak else '?'} dB)")
    if not peak or float(peak.group(1)) < -20:
        sys.exit("✗ mix is near-silent: check the music path, source_start_s and gains")


if __name__ == "__main__":
    main()
