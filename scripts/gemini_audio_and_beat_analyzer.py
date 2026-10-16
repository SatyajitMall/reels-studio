#!/usr/bin/env python3
"""Audio loudness (LUFS / peak dB) and music beat-grid analyser.

Complements `scripts/analyze_footage.py` by measuring what the frame analyser misses:
1. Per-clip dialogue loudness (integrated LUFS, peak dBFS, and the `set_clip_volume`
   dB change that hits the -4.5 dBFS peak / -14 LUFS target). Only when clips are passed.
2. Music: BPM, every beat, bar downbeats (every 4th beat), strongest accents, an
   energy map with labelled sections (intro / build / drop / breakdown / outro), and
   candidate start/end points for 15 / 30 / 45 / 60 s reels.
Writes `<out>/audio_summary.md` and `<out>/beats.json`.

Usage:
    ./.venv/bin/python scripts/gemini_audio_and_beat_analyzer.py --music assets/music/track.mp3 -o projects/<reel>/analysis
    ./.venv/bin/python scripts/gemini_audio_and_beat_analyzer.py projects/<reel>/raw/a-roll --music ... -o ...   (adds dialogue loudness)
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
TARGET_LENGTHS_S = (15, 30, 45, 60)


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


def label_sections(bars: list[dict], duration: float, first_beat: float, last_beat: float) -> list[dict]:
    """Group bars into energy sections and name them. Heuristic: levels are relative to the track."""
    if not bars:
        return [{"label": "no beat detected", "start_s": 0.0, "end_s": round(duration, 2)}]
    db = np.array([b["energy_db"] for b in bars])
    smooth = np.convolve(db, np.ones(3) / 3, mode="same") if len(db) >= 3 else db
    hi, lo = np.percentile(smooth, 70), np.percentile(smooth, 30)
    level = ["high" if v >= hi else "low" if v <= lo else "mid" for v in smooth]

    # Merge runs, then fold runs shorter than 2 bars into the previous run.
    runs: list[list] = []
    for i, lv in enumerate(level):
        if runs and runs[-1][0] == lv:
            runs[-1][2] = i
        else:
            runs.append([lv, i, i])
    merged: list[list] = []
    for r in runs:
        if merged and (r[2] - r[1] + 1) < 2:
            merged[-1][2] = r[2]
        elif merged and merged[-1][0] == r[0]:
            merged[-1][2] = r[2]
        else:
            merged.append(r)

    sections = []
    if first_beat > 1.0:
        sections.append({"label": "intro (no beat)", "start_s": 0.0, "end_s": round(first_beat, 2), "level": "low"})
    seen_high = False
    for k, (lv, a, b) in enumerate(merged):
        start, end = bars[a]["start_s"], bars[b]["end_s"]
        later_high = any(m[0] == "high" for m in merged[k + 1:])
        if lv == "high":
            name = "drop / full" if not seen_high else "full"
            seen_high = True
        elif not seen_high:
            name = "intro" if k == 0 and lv == "low" else "build"
        elif later_high:
            name = "breakdown"
        else:
            name = "outro"
        if sections and sections[-1]["label"] == name:  # e.g. low/mid/low "build" runs read as one build
            sections[-1]["end_s"] = round(end, 2)
            sections[-1]["level"] = "mixed" if sections[-1]["level"] != lv else lv
        else:
            sections.append({"label": name, "start_s": round(start, 2), "end_s": round(end, 2), "level": lv})
    if duration - last_beat > 1.0:
        sections.append({"label": "outro (no beat)", "start_s": round(last_beat, 2), "end_s": round(duration, 2), "level": "low"})
    return sections


def candidate_cuts(bars: list[dict], hits: list[float], sections: list[dict], duration: float) -> dict:
    """For each target length, rank start downbeats: early first hit, high energy, clean ending."""
    if not bars:
        return {}
    starts = [b["start_s"] for b in bars]
    ends = sorted(set([b["end_s"] for b in bars] + [round(duration, 2)]))
    boundaries = {s["end_s"] for s in sections} | {round(duration, 2)}
    out = {}
    for target in TARGET_LENGTHS_S:
        ranked = []
        for i, s in enumerate(starts):
            # End on the bar boundary closest to the target length.
            e = min(ends, key=lambda x: abs((x - s) - target))
            if e <= s or abs((e - s) - target) > 2.5:
                continue
            in_win = [b["energy_db"] for b in bars if b["start_s"] >= s and b["end_s"] <= e + 0.01]
            if not in_win:
                continue
            first_hit = next((h for h in hits if s <= h <= e), None)
            hit_delay = (first_hit - s) if first_hit is not None else 99.0
            clean_end = min(abs(e - x) for x in boundaries) < 0.5
            phrase_start = i % 4 == 0
            score = (float(np.mean(in_win))
                     + (3.0 if hit_delay <= 3.0 else 0.0)
                     + (2.0 if clean_end else 0.0)
                     + (1.0 if phrase_start else 0.0))
            ranked.append({
                "start_s": round(s, 2), "end_s": round(e, 2), "length_s": round(e - s, 2),
                "first_hit_after_s": round(hit_delay, 2) if first_hit is not None else None,
                "mean_energy_db": round(float(np.mean(in_win)), 1),
                "ends_on_section_or_track_end": clean_end,
                "starts_on_phrase": phrase_start,
                "score": round(score, 2),
            })
        ranked.sort(key=lambda r: r["score"], reverse=True)
        # Keep the best 3 that don't overlap the start of a better one by < 4 s.
        picks: list[dict] = []
        for r in ranked:
            if all(abs(r["start_s"] - p["start_s"]) >= 4.0 for p in picks):
                picks.append(r)
            if len(picks) == 3:
                break
        out[str(target)] = picks
    return out


def analyze_music_beats(music_path: Path) -> dict:
    """BPM, beat grid, bar downbeats, accents, energy sections and candidate cuts (librosa)."""
    import librosa

    y, sr = librosa.load(str(music_path), sr=22050, mono=True)
    duration = float(len(y) / sr)
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    bpm = float(np.asarray(tempo).item())
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    times = librosa.times_like(onset_env, sr=sr)
    rms = librosa.feature.rms(y=y)[0]
    rms_times = librosa.times_like(rms, sr=sr)

    # Onset strength at each beat
    beat_strengths = []
    for bt in beat_times:
        idx = int(np.argmin(np.abs(times - bt)))
        beat_strengths.append((round(float(bt), 2), round(float(onset_env[idx]), 2)))

    # Top 8 accents, at least 2 s apart
    ranked = sorted(beat_strengths, key=lambda x: x[1], reverse=True)
    accents: list[float] = []
    for bt, _ in ranked:
        if all(abs(bt - existing) >= 2.0 for existing in accents):
            accents.append(bt)
        if len(accents) >= 8:
            break
    accents.sort()
    # "Hits" for candidate scoring: beats in the top 15 % of onset strength
    thr = np.percentile([s for _, s in beat_strengths], 85) if beat_strengths else 0
    hits = [bt for bt, s in beat_strengths if s >= thr]

    # Bars = every 4th beat; energy per bar in dB relative to the loudest bar
    downbeats = [float(t) for t in beat_times[::4]]
    bars = []
    for i, start in enumerate(downbeats):
        end = downbeats[i + 1] if i + 1 < len(downbeats) else (float(beat_times[-1]) if len(beat_times) else duration)
        if end <= start:
            continue
        seg = rms[(rms_times >= start) & (rms_times < end)]
        if seg.size:
            bars.append({"bar": i + 1, "start_s": round(start, 2), "end_s": round(end, 2),
                         "energy": float(np.sqrt(np.mean(seg ** 2)))})
    peak = max((b["energy"] for b in bars), default=1e-9) or 1e-9
    for b in bars:
        b["energy_db"] = round(20 * np.log10(max(b.pop("energy"), 1e-9) / peak), 1)

    first_beat = float(beat_times[0]) if len(beat_times) else 0.0
    last_beat = float(beat_times[-1]) if len(beat_times) else duration
    sections = label_sections(bars, duration, first_beat, last_beat)

    return {
        "file": music_path.name,
        "duration_s": round(duration, 2),
        "bpm": round(bpm, 1),
        "bar_s": round(4 * 60 / bpm, 3) if bpm else None,
        "total_beats": int(len(beat_times)),
        "first_beat_s": round(first_beat, 2),
        "last_beat_s": round(last_beat, 2),
        "beat_times_s": [round(float(t), 2) for t in beat_times],
        "bar_downbeats_s": [round(t, 2) for t in downbeats],
        "major_accent_drops_s": accents,
        "bars": bars,
        "sections": sections,
        "candidate_cuts": candidate_cuts(bars, hits, sections, duration),
    }


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("inputs", nargs="*", type=Path, help="Dialogue clips or folders (optional; adds the loudness table)")
    ap.add_argument("--music", type=Path, default=None, help="Music file to extract the beat grid from")
    ap.add_argument("-o", "--out", type=Path, required=True, help="Output analysis directory")
    args = ap.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for p in args.inputs:
        if p.is_dir():
            files += sorted(f for f in p.iterdir()
                            if f.suffix.lower() in AUDIO_VIDEO_EXT and not f.name.startswith("._"))
        elif p.exists() and p.suffix.lower() in AUDIO_VIDEO_EXT:
            files.append(p)

    clip_stats = [measure_loudness(f) for f in files]
    music_info = analyze_music_beats(args.music) if (args.music and args.music.exists()) else None

    payload = {"dialogue_clips": clip_stats, "music": music_info}
    (args.out / "beats.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")

    md = ["# Audio Loudness & Beat Grid Analysis", ""]
    if clip_stats:
        md += [
            "## Dialogue loudness & Premiere gain targets (A1)",
            "",
            "| Clip | Integrated LUFS | Peak dBFS | Mean dBFS | Recommended `set_clip_volume` change |",
            "|---|---|---|---|---|",
        ]
        for c in clip_stats:
            sign = "+" if c["recommended_premiere_gain_db"] > 0 else ""
            md.append(
                f"| {c['file']} | {c['integrated_lufs']} LUFS | {c['peak_dbfs']} dB | "
                f"{c['mean_dbfs']} dB | **{sign}{c['recommended_premiere_gain_db']} dB** |"
            )
        md.append("")

    if music_info:
        m = music_info
        md += [
            f"## Music: `{m['file']}` (A3)",
            f"- **Tempo:** {m['bpm']} BPM · 1 bar = {m['bar_s']} s · {m['total_beats']} beats over {m['duration_s']} s",
            f"- **Beats detected:** {m['first_beat_s']} s → {m['last_beat_s']} s (outside that range there's no steady beat)",
            f"- **Strongest accents (s):** `{', '.join(str(x) for x in m['major_accent_drops_s'])}`",
            f"- **Bar downbeats (every 4th beat; first 16):** `{', '.join(str(x) for x in m['bar_downbeats_s'][:16])}`",
            "",
            "### Energy / sections",
            "Heuristic labels from per-bar loudness relative to the loudest bar. Check by ear before committing a section.",
            "",
            "| Section | Start | End | Length | Level |",
            "|---|---|---|---|---|",
        ]
        for s in m["sections"]:
            md.append(f"| {s['label']} | {s['start_s']} s | {s['end_s']} s | {round(s['end_s'] - s['start_s'], 1)} s | {s.get('level', '')} |")
        md += ["", "### Candidate cuts", "Start on a bar downbeat; end on the bar closest to the target length. "
               "Scored on energy, first hit ≤ 3 s in, a clean ending (section or track end) and starting on a 4-bar phrase.", "",
               "| Target | Start | End | Length | First hit after | Mean energy | Clean end | Phrase start |",
               "|---|---|---|---|---|---|---|---|"]
        for target, picks in m["candidate_cuts"].items():
            for p in picks:
                hit = f"{p['first_hit_after_s']} s" if p["first_hit_after_s"] is not None else "–"
                md.append(f"| {target} s | {p['start_s']} s | {p['end_s']} s | {p['length_s']} s | {hit} | "
                          f"{p['mean_energy_db']} dB | {'yes' if p['ends_on_section_or_track_end'] else 'no'} | "
                          f"{'yes' if p['starts_on_phrase'] else 'no'} |")
        md += ["", "> Cut section changes and hero shots on accents or bar downbeats (CLAUDE.md §4c). Full per-bar energy is in `beats.json`."]

    out_md = args.out / "audio_summary.md"
    out_md.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"✓ Wrote {out_md} and {args.out / 'beats.json'}")


if __name__ == "__main__":
    main()
