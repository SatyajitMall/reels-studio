#!/usr/bin/env python3
"""Check, in the export's own audio, that every sound effect is there, on its frame and above the music.

Claude can't hear the mix. sfx_prep.py measures each file before placement, but nothing measured the export: a sound
that Premiere placed a frame early, one that went missing, or one buried under the song (kolkata v6's tram bell at
−20 dB, caught by ear in review) passed every script.

Each sound effect is a known file, so this looks for that file's own waveform in the export around its planned
time, with no model and no guessing. GCC-PHAT (a whitened cross-correlation, as used to time-align microphones) gives
a sharp peak at the true lag even when the effect sits under a loud song; its peak-to-sidelobe ratio (PSR) says
whether the file is there:
  found      PSR ≥ 15; or PSR ≥ 8 and the fitted level within −6…+9 dB of the planned gain_db (sub-bass booms
             correlate weakly; a wrong time fits 10 dB or more below the plan)        PSR 8–15 otherwise WARN, < 8 FAIL
  offset     where it actually starts vs the plan; more than 2 frames                 FAIL (rule: ≤ 2 frames)
  level      the fitted level vs the planned gain_db, outside −6…+9 dB                WARN (exports are loudness-normalised
             after the mix, so a few dB above the plan is normal)
  masking    its best frequency band against the rest of the mix over its loudest 250 ms; below −10 dB in every
             band                                                                     WARN "masked: listen"
Measured 2026-11-12 (HQ, studio v0.11.0) on kolkata v6 / v6_3 (from their EDLs) and puja-night-2 v5c: all 13 real
placements found and on frame (PSR 9.9–200; the 9.9 is a sub-bass boom, matched by level), all 8 fakes rejected (the
same files at wrong times: PSR 3.6–11.4, and the two in the 8–15 band fitted 19 dB under the plan). A needle drop
planned 3 frames late read −3.0 frames; puja's nine effects all read +0.5 frames, one consistent placement offset.
The masking line has no ground truth yet: the kolkata v6 bell (−20 dB, called "~20 dB under the song" in review) read
+1.4 dB in its best band, the −14 dB re-cue the director accepted +14.2 dB, puja's accepted swishes −3.7…+5.9 dB. The first reel that hears a buried effect logs its
number in a CR, and HQ moves the line.

Why not earshot's own listening here: in a music-led mix some onset is always near any time, so earshot's cue sync
scored a cue with no sound effect as "on frame" (puja v5c), and on kolkata its hit rate equalled chance. earshot
stays for picking sounds (`sfx_fetch.py --rank`, `earshot find`) and, with --sheet, draws the soundtrack.

The sound effects come from the EDL's `audio` list (every entry shorter than --max-s, so music and guide tracks are
skipped) or from a cue sheet with the same keys:
  [{"id": "boom", "file": "assets/sfx/x.wav", "start": 3.80, "in": 0.0, "dur": 1.2, "gain_db": -16}]
start = where the file's `in` point sits on the timeline, as in the EDL.

Writes into -o: sfx_sync.json and SFX_SYNC.md (and sound_sheet.png with --sheet). Exit 1 on any FAIL.

Usage (from the studio root):
  ./.venv/bin/python scripts/sfx_sync.py projects/<reel>/renders/exports/<reel>_v4_mix.mp4 \\
      --edl projects/<reel>/analysis/edl_v4.json -o projects/<reel>/analysis/sfx_sync_v4 [--sheet]
  ./.venv/bin/python scripts/sfx_sync.py <export> --cues projects/<reel>/analysis/sfx_cues_v4.json -o <dir>
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))
from media_info import fps_of  # noqa: E402

SR = 16000
SEARCH_S = 0.3
PSR_FOUND = 15.0
PSR_WEAK = 8.0
LEVEL_LO_DB, LEVEL_HI_DB = -6.0, 9.0
MAX_FRAMES_OFF = 2.0
MASKED_DB = -10.0
TEMPLATE_MAX_S = 1.5
LOUD_WIN_S = 0.25
REFINE_S = 0.04       # the whitened peak can sit a cycle off on a sub-bass boom: refine by plain correlation
BAND_EDGES = np.geomspace(80, 7900, 19)      # 18 log-spaced bands, ~1/3 octave


def decode(path: Path, start: float = 0.0, dur: float | None = None) -> np.ndarray:
    cmd = ["ffmpeg", "-v", "error", "-nostdin", "-ss", f"{max(0.0, start):.4f}", "-i", str(path)]
    if dur is not None:
        cmd += ["-t", f"{dur:.4f}"]
    cmd += ["-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"]
    p = subprocess.run(cmd, capture_output=True)
    if p.returncode != 0:
        raise RuntimeError(p.stderr.decode(errors="replace").strip()[-200:])
    return np.frombuffer(p.stdout, np.float32).astype(np.float64)


def media_dur(path: Path) -> float:
    p = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(path)],
                       capture_output=True, text=True)
    try:
        return float(p.stdout.strip())
    except ValueError:
        return 0.0


def resolve(f: str) -> Path:
    p = Path(f)
    return p if p.is_absolute() else ROOT / p


def load_entries(a) -> list[dict]:
    if a.edl:
        src = json.loads(a.edl.read_text())
        raw = src.get("audio", []) if isinstance(src, dict) else []
    else:
        src = json.loads(a.cues.read_text())
        raw = (src.get("events") or src.get("cues") or []) if isinstance(src, dict) else src
    out = []
    for i, e in enumerate(raw):
        f = resolve(e["file"])
        if any(s in e["file"] for s in a.skip):
            continue
        length = float(e["dur"]) if e.get("dur") else max(0.0, media_dur(f) - float(e.get("in", 0)))
        if a.edl and length > a.max_s:          # music, a guide, an ambience bed: not a sound effect
            continue
        out.append({"id": e.get("id") or f"{Path(e['file']).stem[:28]}@{float(e['start']):g}", "file": f,
                    "start": float(e["start"]), "in": float(e.get("in", 0.0)), "len": length,
                    "gain_db": e.get("gain_db")})
    return out


def gcc_phat(seg: np.ndarray, s: np.ndarray) -> tuple[int, float]:
    """the lag of template s inside seg (valid lags only) and the peak-to-sidelobe ratio of the whitened correlation"""
    n, m = len(seg), len(s)
    nfft = 1 << int(np.ceil(np.log2(n + m)))
    g = np.fft.rfft(seg, nfft) * np.conj(np.fft.rfft(s, nfft))
    g = np.fft.irfft(g / np.maximum(np.abs(g), 1e-12), nfft)[: n - m + 1]
    k = int(np.argmax(g))
    side = np.delete(g, range(max(0, k - 40), k + 40))
    return k, float((g[k] - side.mean()) / max(side.std(), 1e-12))


def band_energy(sig: np.ndarray) -> np.ndarray:
    f = np.abs(np.fft.rfft(sig * np.hanning(len(sig)))) ** 2
    fr = np.fft.rfftfreq(len(sig), 1 / SR)
    return np.array([f[(fr >= lo) & (fr < hi)].sum() for lo, hi in zip(BAND_EDGES[:-1], BAND_EDGES[1:])])


def check(x: np.ndarray, e: dict, fps: float) -> dict:
    s = decode(e["file"], e["in"], min(e["len"], TEMPLATE_MAX_S))
    r = {"id": e["id"], "file": str(e["file"].relative_to(ROOT) if e["file"].is_relative_to(ROOT) else e["file"]),
         "planned_start": e["start"], "planned_gain_db": e["gain_db"]}
    if len(s) < SR * 0.02 or np.sqrt(np.mean(s * s)) < 1e-5:
        return {**r, "verdict": "SKIP", "why": "the file is silent at its in point"}
    s = s - s.mean()
    lo = max(0, int((e["start"] - SEARCH_S) * SR))
    seg = x[lo:min(len(x), int((e["start"] + SEARCH_S) * SR) + len(s))]
    if len(seg) < len(s):
        return {**r, "verdict": "FAIL", "why": "the export ends before this sound"}
    k0, psr = gcc_phat(seg, s)
    # refine: the lag within ±40 ms where the file's waveform fits the mix best (largest positive gain)
    r0, r1 = max(0, k0 - int(REFINE_S * SR)), min(len(seg) - len(s), k0 + int(REFINE_S * SR))
    dots = np.correlate(seg[r0:r1 + len(s)], s, "valid")
    k = r0 + int(np.argmax(dots))
    actual = (lo + k) / SR
    off = (actual - e["start"]) * fps
    w = seg[k:k + len(s)]
    g = float(np.dot(w, s) / np.dot(s, s))
    level = 20 * np.log10(abs(g)) if g > 0 else -120.0
    fit = g * s
    win = min(int(LOUD_WIN_S * SR), len(s))
    j = int(np.argmax(np.convolve(s * s, np.ones(win), "valid")))
    bs, br = band_energy(fit[j:j + win]), band_energy(w[j:j + win] - fit[j:j + win])
    snr = 10 * np.log10(np.maximum(bs, 1e-20) / np.maximum(br, 1e-20))
    kb = int(np.argmax(np.where(bs > bs.max() * 1e-3, snr, -99.0)))
    r.update({"psr": round(psr, 1), "refine_ms": round((k - k0) / SR * 1000, 1), "actual_start": round(actual, 3), "offset_frames": round(off, 2),
              "played_gain_db": round(level, 1), "best_band_hz": [round(BAND_EDGES[kb]), round(BAND_EDGES[kb + 1])],
              "best_band_over_mix_db": round(float(snr[kb]), 1), "loudest_at": round(actual + j / SR, 3)})
    plan = None if e["gain_db"] is None else float(e["gain_db"])
    level_ok = plan is not None and plan + LEVEL_LO_DB <= level <= plan + LEVEL_HI_DB
    if psr < PSR_WEAK or (psr < PSR_FOUND and plan is not None and not level_ok):
        return {**r, "verdict": "FAIL", "why": f"not found within ±{SEARCH_S:g} s (PSR {psr:.1f}"
                + (f", fits {level:.0f} dB vs planned {plan:g}" if plan is not None else "") + "): missing, moved or buried"}
    if abs(off) > MAX_FRAMES_OFF:
        return {**r, "verdict": "FAIL", "why": f"starts {abs(off):.1f} frames {'late' if off > 0 else 'early'} "
                                              f"(rule: ≤ {MAX_FRAMES_OFF:g})"}
    notes = []
    if psr < PSR_FOUND and plan is None:
        notes.append(f"weak match (PSR {psr:.1f}, no planned gain to confirm it): listen at {actual:.2f} s")
    elif psr < PSR_FOUND:
        notes.append(f"matched by level (PSR {psr:.1f}, low sound)")
    if plan is not None and not level_ok:
        notes.append(f"plays at {level:.1f} dB, planned {plan:g} dB")
    if snr[kb] < MASKED_DB:
        notes.append(f"under the mix in every band (best {snr[kb]:+.1f} dB at {BAND_EDGES[kb]:.0f}–{BAND_EDGES[kb + 1]:.0f} Hz):"
                     f" may be masked, listen at {actual + j / SR:.2f} s")
    warn = [n for n in notes if not n.startswith("matched by level")]
    tail = f"{'on frame' if abs(off) < 0.5 else f'{off:+.1f} frames'}, best band {snr[kb]:+.1f} dB over the mix"
    return {**r, "verdict": "WARN" if warn else "PASS", "why": "; ".join(notes) if warn else tail
            + ("".join(f"; {n}" for n in notes))}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("export", type=Path)
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--edl", type=Path, help="the EDL whose `audio` list placed the sounds")
    src.add_argument("--cues", type=Path, help="a cue sheet: [{id, file, start, in, dur, gain_db}]")
    ap.add_argument("-o", "--out", type=Path, required=True)
    ap.add_argument("--fps", type=float, help="default: the export's")
    ap.add_argument("--max-s", type=float, default=12.0, help="EDL entries longer than this are music / beds (skipped)")
    ap.add_argument("--skip", nargs="*", default=["guide"], help="skip audio entries whose path contains any of these")
    ap.add_argument("--sheet", action="store_true", help="also draw the soundtrack with earshot (sound_sheet.png)")
    a = ap.parse_args()
    if not a.export.exists():
        sys.exit(f"No export {a.export}")
    fps = a.fps or fps_of(a.export)
    entries = load_entries(a)
    a.out.mkdir(parents=True, exist_ok=True)
    if not entries:
        (a.out / "SFX_SYNC.md").write_text(f"# SFX sync: {a.export.name}\n\n**SKIP** · no sound effects in the list\n")
        print("SKIP · no sound effects in the list")
        return
    x = decode(a.export)
    rows = [check(x, e, fps) for e in sorted(entries, key=lambda e: e["start"])]
    sheet = None
    if a.sheet:
        from earshot_util import earshot_bin
        exe = earshot_bin()
        cues = a.out / "cues_earshot.json"
        cues.write_text(json.dumps({"fps": fps, "events": [{"t": r.get("actual_start", r["planned_start"]), "id": r["id"]}
                                                             for r in rows]}))
        if exe:
            p = subprocess.run([exe, "sheet", str(a.export), "-o", str(a.out / "sound_sheet.png"), "--cues", str(cues)],
                               capture_output=True, text=True, timeout=900)
            sheet = "sound_sheet.png" if p.returncode == 0 else f"sheet failed: {(p.stderr or p.stdout).strip()[-160:]}"
        else:
            sheet = "earshot not installed (setup.sh)"
    fails = [r for r in rows if r["verdict"] == "FAIL"]
    warns = [r for r in rows if r["verdict"] == "WARN"]
    verdict = "FAIL" if fails else ("WARN" if warns else "PASS")
    (a.out / "sfx_sync.json").write_text(json.dumps({"export": str(a.export), "fps": fps, "verdict": verdict,
                                                     "sounds": rows, "sheet": sheet}, indent=1))
    md = [f"# SFX sync: {a.export.name}", "",
          f"**{verdict}** · {len(rows) - len(fails) - len(warns)} PASS, {len(warns)} WARN, {len(fails)} FAIL of "
          f"{len(rows)} sound effects · {fps:g} fps", "",
          "| planned (s) | sound | verdict | why | PSR | offset (frames) | level (dB) | best band over mix (dB) |",
          "|---|---|---|---|---|---|---|---|"]
    md += [f"| {r['planned_start']:g} | {r['id']} | {r['verdict']} | {r['why']} | {r.get('psr', '')} | "
           f"{r.get('offset_frames', '')} | {r.get('played_gain_db', '')} | {r.get('best_band_over_mix_db', '')} |" for r in rows]
    md += ["", "Each file's own waveform is found in the export's audio: offsets and levels are measurements, not "
           "guesses. A WARN for masking is a lead: listen at that time." + (f" Picture: {sheet}." if sheet else "")]
    (a.out / "SFX_SYNC.md").write_text("\n".join(md) + "\n")
    for r in rows:
        print(f"{r['verdict']:4s} {r['planned_start']:8.2f}  {r['id'][:34]:34s} {r['why']}")
    print(f"\n{verdict} · {a.out / 'SFX_SYNC.md'}")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
