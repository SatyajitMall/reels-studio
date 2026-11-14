#!/usr/bin/env python3
"""song_fit.py — Stage 6 of research/SONG_RESEARCH_METHOD.md (reel-local prototype, KOLKATA; CR-20261106-kolkata-song-research).

Compares candidate songs against the reel's target length, target energy arc and the footage's steady-hold lengths,
so the audition starts from numbers. It doesn't judge meaning: story fit is scored from the lyrics in Stage 5.

Per song:
  tempo     BPM, bar length, and the half-time feel when the beat is > 120 BPM (a 152 BPM song plays like 76)
  holds     how a typical steady hold of our footage (median of analysis/motion.json holds, usable clips) sits on the
            bar grid: bars per shot and shots in the target length
  section   the best continuous window of --length s starting on a bar downbeat, scored against --arc (relative
            energy targets, e.g. 0.35,0.55,0.8,1.0,0.7), with a small bonus for ending at a section end
  vocals    (--vocals) word-level timing by local Whisper: words per 10 s inside the best window, and the longest gap
            without singing (room for pictures)
Writes <out>/SONG_FIT.md and <out>/song_fit.json.

Usage (studio root):
  ./.venv/bin/python projects/kolkata/tools/song_fit.py audio1.mp3 audio2.wav ... -o projects/kolkata/research/fit \
      [--length 45] [--arc 0.35,0.55,0.8,1.0,0.7] [--motion projects/kolkata/analysis/motion.json] [--vocals]
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from gemini_audio_and_beat_analyzer import analyze_music_beats  # noqa: E402


def footage_hold(motion: Path, orientation: Path | None) -> float:
    m = json.loads(motion.read_text())
    bad = set()
    if orientation and orientation.exists():
        bad = set(json.loads(orientation.read_text()).get("unusable", {}).keys())
    lens = [b - a for c, v in m.items() if c not in bad for a, b in (v.get("holds") or []) if b - a >= 1.0]
    return float(np.median(lens)) if lens else 3.0


def best_windows(mus: dict, length: float, arc: list[float], top: int = 3) -> list[dict]:
    bars = mus["bars"]
    e = np.array([b["energy_db"] for b in bars], float)
    lo, hi = np.percentile(e, 5), np.percentile(e, 98)
    en = np.clip((e - lo) / max(hi - lo, 1e-6), 0, 1)
    sec_ends = {round(s["end_s"], 2) for s in mus["sections"]}
    out = []
    for i, b in enumerate(bars):
        t0 = b["start_s"]; j = i
        while j < len(bars) and bars[j]["end_s"] - t0 < length - 0.4:
            j += 1
        if j >= len(bars):
            break
        seg = en[i:j + 1]
        tgt = np.interp(np.linspace(0, 1, len(seg)), np.linspace(0, 1, len(arc)), arc)
        err = float(np.sqrt(np.mean((seg - tgt) ** 2)))
        t1 = bars[j]["end_s"]
        clean = any(abs(t1 - s) < 0.8 for s in sec_ends)
        score = round((1 - err) * 100 + (5 if clean else 0), 1)
        out.append({"start": round(t0, 2), "end": round(t1, 2), "len": round(t1 - t0, 2), "arc_err": round(err, 3),
                    "clean_end": clean, "score": score,
                    "energy": [round(x, 2) for x in np.interp(np.linspace(0, len(seg) - 1, 6), np.arange(len(seg)), seg)]})
    out.sort(key=lambda w: -w["score"])
    picked = []
    for w in out:   # non-overlapping top windows
        if all(abs(w["start"] - p["start"]) > length / 2 for p in picked):
            picked.append(w)
        if len(picked) == top:
            break
    return picked


def vocals(path: Path, start: float, end: float, lang: str) -> dict:
    with tempfile.TemporaryDirectory() as td:
        wav = Path(td) / "v.wav"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(start), "-t", str(end - start), "-i", str(path), "-ac", "1",
                        "-ar", "16000", str(wav)], check=True)
        subprocess.run([sys.executable, str(ROOT / "scripts/transcribe_local.py"), str(wav), "--edit-dir", td,
                        "--model", "large-v3-turbo", "--language", lang], check=True, capture_output=True)
        d = json.loads(next(Path(td, "transcripts").glob("*.json")).read_text())
    w = [x for x in d.get("words", []) if x.get("type", "word") == "word"]
    if not w:
        return {"words_per_10s": 0.0, "longest_gap_s": round(end - start, 1), "first_word_s": None}
    gaps = [b["start"] - a["end"] for a, b in zip(w, w[1:])] + [w[0]["start"], (end - start) - w[-1]["end"]]
    return {"words_per_10s": round(len(w) / (end - start) * 10, 1), "longest_gap_s": round(max(gaps), 1),
            "first_word_s": round(w[0]["start"], 1)}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("audio", nargs="+", type=Path)
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--length", type=float, default=45.0)
    ap.add_argument("--arc", default="0.35,0.55,0.8,1.0,0.7")
    ap.add_argument("--motion", type=Path, default=ROOT / "projects/kolkata/analysis/motion.json")
    ap.add_argument("--orientation", type=Path, default=ROOT / "projects/kolkata/analysis/orientation.json")
    ap.add_argument("--vocals", action="store_true")
    ap.add_argument("--language", default="bn")
    a = ap.parse_args()
    arc = [float(x) for x in a.arc.split(",")]
    hold = footage_hold(a.motion, a.orientation)
    a.out.mkdir(parents=True, exist_ok=True)
    res = []
    for p in a.audio:
        print("▸", p.name, flush=True)
        mus = analyze_music_beats(p)
        bpm, bar = mus["bpm"], mus["bar_s"]
        feel_bar = bar * 2 if bpm > 120 else bar
        bps = max(1, round(hold / feel_bar))
        wins = best_windows(mus, a.length, arc)
        r = {"file": str(p), "bpm": bpm, "bar_s": bar, "feel": "half-time" if bpm > 120 else "as is",
             "feel_bar_s": round(feel_bar, 2), "duration_s": mus["duration_s"], "hold_median_s": round(hold, 2),
             "bars_per_shot": bps, "shot_s": round(bps * feel_bar, 2), "shots_in_length": round(a.length / (bps * feel_bar)),
             "windows": wins}
        if a.vocals and wins:
            r["vocals"] = vocals(p, wins[0]["start"], wins[0]["end"], a.language)
        res.append(r)
    (a.out / "song_fit.json").write_text(json.dumps(res, indent=1))
    L = [f"# Song fit ({a.length:.0f} s, arc {a.arc}; footage median steady hold {hold:.2f} s)", "",
         "| Song | BPM (feel) | bar | shot = | shots | best section | arc err | clean end | 2nd | vocals (words/10 s · longest gap) |",
         "|---|---|---|---|---|---|---|---|---|---|"]
    for r in res:
        w = r["windows"]; w0 = w[0] if w else {}
        v = r.get("vocals")
        L.append(f"| {Path(r['file']).name} | {r['bpm']:.0f} ({r['feel']}) | {r['feel_bar_s']} s | {r['bars_per_shot']} bar ≈ {r['shot_s']} s | "
                 f"{r['shots_in_length']} | {w0.get('start', '–')}–{w0.get('end', '–')} s | {w0.get('arc_err', '–')} | "
                 f"{'yes' if w0.get('clean_end') else 'no'} | {(str(w[1]['start']) + '–' + str(w[1]['end'])) if len(w) > 1 else '–'} | "
                 f"{(str(v['words_per_10s']) + ' · ' + str(v['longest_gap_s']) + ' s') if v else '–'} |")
    L += ["", "Arc err = RMS distance (0–1) between the window's normalised per-bar energy and the target arc; lower is better.",
          "Energy shape of each best window (6 points, 0–1) is in song_fit.json. Story fit is not measured here (Stage 5)."]
    (a.out / "SONG_FIT.md").write_text("\n".join(L) + "\n")
    print("✓", a.out / "SONG_FIT.md")


if __name__ == "__main__":
    main()
