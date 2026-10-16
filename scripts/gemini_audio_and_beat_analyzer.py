#!/usr/bin/env python3
"""Gemini Audio Loudness (LUFS / Peak dB) & Music Beat Grid Analyzer.

Complements `scripts/analyze_footage.py` by measuring what the video frame analyzer
misses:
1. Per-clip dialogue loudness (Integrated LUFS, True Peak dBFS, and the exact
   `set_clip_volume` dB adjustment needed in Premiere Pro to hit the -4.5 dBFS
   peak / -14 LUFS target specified in `CLAUDE.md` §3).
2. Music track BPM, beat timestamps, and high-energy "beat drop" points using
   `librosa` (installed in `.venv`), written to `<out_dir>/audio_summary.md`
   and `<out_dir>/beats.json` so Claude can cut B-roll and flash transitions
   on actual musical beats.

Usage:
    ./.venv/bin/python scripts/gemini_audio_and_beat_analyzer.py \
        projects/<reel>/raw/a-roll --music assets/music/track.mp3 \
        -o projects/<reel>/analysis
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
from pathlib import Path

import numpy as np

AUDIO_VIDEO_EXT = {".mp4", ".mov", ".m4v", ".mxf", ".mkv", ".wav", ".mp3", ".m4a", ".aac"}
TARGET_PEAK_DBFS = -4.5
TARGET_LUFS = -14.0


def measure_loudness(path: Path) -> dict:
    """Measure Integrated LUFS and max volume (dBFS) via ffmpeg ebur128 & volumedetect."""
    cmd = [
        "ffmpeg", "-hide_banner", "-nostats", "-i", str(path),
        "-af", "ebur128=peak=true,volumedetect", "-vn", "-f", "null", "-",
    ]
    stderr = subprocess.run(cmd, capture_output=True, text=True).stderr

    i_matches = re.findall(r"I:\s*(-?[0-9.]+)\s*LUFS", stderr)
    tp_matches = re.findall(r"Peak:\s*(-?[0-9.]+)\s*dBFS", stderr)
    max_vol_match = re.search(r"max_volume:\s*(-?[0-9.]+)\s*dB", stderr)
    mean_vol_match = re.search(r"mean_volume:\s*(-?[0-9.]+)\s*dB", stderr)

    lufs = float(i_matches[-1]) if i_matches else None
    peak_db = (
        float(max_vol_match.group(1))
        if max_vol_match
        else (float(tp_matches[-1]) if tp_matches else None)
    )
    mean_db = float(mean_vol_match.group(1)) if mean_vol_match else None

    if lufs is not None and lufs > -70.0:
        gain_for_lufs = round(TARGET_LUFS - lufs, 1)
    else:
        gain_for_lufs = 0.0

    if peak_db is not None and peak_db > -70.0:
        max_safe_gain = round(TARGET_PEAK_DBFS - peak_db, 1)
        recommended_gain_db = round(min(gain_for_lufs, max_safe_gain), 1)
    else:
        recommended_gain_db = 0.0

    return {
        "file": path.name,
        "integrated_lufs": lufs,
        "peak_dbfs": peak_db,
        "mean_dbfs": mean_db,
        "recommended_premiere_gain_db": recommended_gain_db,
    }


def analyze_music_beats(music_path: Path) -> dict:
    """Extract BPM, beat grid timestamps, and top onset energy peaks using librosa."""
    import librosa

    y, sr = librosa.load(str(music_path), sr=22050, mono=True)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.asarray(tempo).item())
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    # Compute onset strength and RMS jumps to detect high-impact beat drops / accents
    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    rms = librosa.feature.rms(y=y)[0]
    times = librosa.times_like(onset_env, sr=sr)

    # Sample onset strength at each detected beat
    beat_strengths = []
    for bt in beat_times:
        idx = int(np.argmin(np.abs(times - bt)))
        beat_strengths.append((round(float(bt), 2), round(float(onset_env[idx]), 2)))

    # Pick top 8 strongest accent beats (spaced at least 2.0s apart) for cuts/drops
    ranked = sorted(beat_strengths, key=lambda x: x[1], reverse=True)
    accents: list[float] = []
    for bt, _ in ranked:
        if all(abs(bt - existing) >= 2.0 for existing in accents):
            accents.append(bt)
        if len(accents) >= 8:
            break
    accents.sort()

    return {
        "file": music_path.name,
        "duration_s": round(float(len(y) / sr), 2),
        "bpm": round(bpm, 1),
        "total_beats": int(len(beat_times)),
        "beat_times_s": [round(float(t), 2) for t in beat_times],
        "downbeats_every_4_s": [round(float(t), 2) for t in beat_times[::4]],
        "major_accent_drops_s": accents,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", type=Path, help="A-roll/B-roll video files or folders")
    ap.add_argument("--music", type=Path, default=None, help="Optional music file to extract beat grid from")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output analysis directory")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for p in args.inputs:
        if p.is_dir():
            files += sorted(f for f in p.iterdir() if f.suffix.lower() in AUDIO_VIDEO_EXT)
        elif p.exists() and p.suffix.lower() in AUDIO_VIDEO_EXT:
            files.append(p)

    clip_stats = [measure_loudness(f) for f in files]
    music_info = analyze_music_beats(args.music) if (args.music and args.music.exists()) else None

    payload = {"dialogue_clips": clip_stats, "music": music_info}
    (args.out / "beats.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = [
        "# Audio Loudness & Beat Grid Analysis",
        "",
        "## 1. Dialogue Loudness & Premiere Pro Gain Targets (Track A1)",
        "",
        "| Clip | Integrated LUFS | Peak dBFS | Mean dBFS | Recommended `set_clip_volume` Adjustment |",
        "|---|---|---|---|---|",
    ]
    for c in clip_stats:
        sign = "+" if c["recommended_premiere_gain_db"] > 0 else ""
        md.append(
            f"| {c['file']} | {c['integrated_lufs']} LUFS | {c['peak_dbfs']} dB | "
            f"{c['mean_dbfs']} dB | **{sign}{c['recommended_premiere_gain_db']} dB** |"
        )

    if music_info:
        md += [
            "",
            f"## 2. Music Beat Grid: `{music_info['file']}` (Track A3)",
            f"- **Estimated Tempo:** {music_info['bpm']} BPM ({music_info['total_beats']} beats over {music_info['duration_s']}s)",
            f"- **Major Accent / Beat-Drop Timestamps (s):** `{', '.join(str(x) for x in music_info['major_accent_drops_s'])}`",
            f"- **4-Bar Downbeats (first 16):** `{', '.join(str(x) for x in music_info['downbeats_every_4_s'][:16])}`",
            "",
            "> Align B-roll entrances (`V2`), flash cuts, and speed-ramp impacts to the Major Accent or 4-Bar Downbeat timestamps above.",
        ]

    out_md = args.out / "audio_summary.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"✓ Wrote {out_md} and {args.out / 'beats.json'}")


if __name__ == "__main__":
    main()
