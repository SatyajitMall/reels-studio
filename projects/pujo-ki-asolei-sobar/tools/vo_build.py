#!/usr/bin/env python3
"""Director's own voiceover -> finished VO stem + IG export (2026-10-27, take 6, recorded with tools/vo_recorder).
1 clean    ffmpeg: high-pass 75 Hz, FFT denoise (tracks the room noise), de-esser
2 place    every phrase onto its slot; lines with a cut word are split at the pause before that word so the word lands on the
           cut (duniya f165, sirf ghar f328, bas is mahine f693, jab koi mard f797). Small tempo change only where a phrase
           overran its slot (line 7a, 1.07x); long internal pauses trimmed (line 4, line 10).
3 tone     matched to the reference voice by measured bands (body 200-500 Hz, de-box 750 Hz, air 8-10 kHz), gentle 2:1
           compression (level swing kept close to the reference), room tone under the gaps
4 depth    small-room reverb (synthetic IR, 18 ms pre-delay, RT60 ~0.6 s, wet low-passed) at a low mix
5 mix      VO over the IG export's natural sound; static gain to -14 LUFS + limiter at -1.5 dBTP (no AGC); muxed onto the v13 picture (video copied)
Usage: vo_build.py  -> audio/vo_director/vo_take06_final.wav, renders/exports/pujo-ki-asolei-sobar_v14_IG.mp4, analysis/vo_place.json
"""
import json, subprocess, tempfile
from pathlib import Path
import numpy as np
from scipy import signal
REEL = Path(__file__).resolve().parents[1]; A = REEL / "audio/vo_director"
TAKE = A / "take_06.wav"; T0 = json.loads((A / "take_06.json").read_text())["reel_t0_in_take_s"]
VID = REEL / "renders/exports/pujo-ki-asolei-sobar_v13_IG.mp4"; OUT = REEL / "renders/exports/pujo-ki-asolei-sobar_v14_IG.mp4"
SR, DUR = 48000, 35.8333

def ff(x, af):
    """run a float32 mono buffer through an ffmpeg audio filter chain"""
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", af, "-f", "f32le", "-ar", str(SR), "-ac", "1", "-"],
                       input=x.astype(np.float32).tobytes(), capture_output=True, check=True)
    return np.frombuffer(p.stdout, np.float32).copy()

raw = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(TAKE), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32).copy()
clean = ff(raw, "highpass=f=75:poles=2,afftdn=nr=12:nf=-50:tn=1,deesser=i=0.35:m=0.5:f=0.5")
def lufs(x, sr=SR):
    out = subprocess.run(["ffmpeg", "-v", "info", "-f", "f32le", "-ar", str(sr), "-ac", "1", "-i", "-", "-af", "ebur128", "-f", "null", "-"],
                         input=x.astype(np.float32).tobytes(), capture_output=True).stderr.decode()
    return float(out.rsplit("I:", 1)[1].split("LUFS")[0])

def loudnorm_linear(x, target, tp):
    """static gain to `target` LUFS + a peak limiter at `tp` dBTP"""
    g = target - lufs(x); return f"volume={g:.2f}dB,alimiter=limit={10 ** (tp / 20):.3f}:attack=3:release=60:level=disabled"

rt = lambda t: int((t + T0) * SR)                                # reel time (take clock) -> sample
hop = SR // 100; e = 20 * np.log10(np.sqrt(np.convolve(clean ** 2, np.ones(hop) / hop, "same")[::hop]) + 1e-9)

def dip(a, b):
    """quietest 10 ms point between reel times a and b (the pause before a word)"""
    i0, i1 = int((a + T0) * 100), int((b + T0) * 100); return (i0 + int(np.argmin(e[i0:i1]))) / 100 - T0

s2 = dip(4.42 + 1.0, 4.42 + 1.65)                                # before 'duniya'
s8 = dip(26.24 + 0.8, 26.24 + 1.05)                              # before 'jab koi mard' (after "Shayad isliye")
# (src start, src end, target start, tempo, line)
PLAN = [(0.89, 3.36, 0.34, 1, "1"), (4.42, s2, 4.175, 1, "2a"), (s2, 7.38, 5.50, 1, "2b duniya"),
        (8.23, 9.35, 8.355, 1, "3a"), (9.59, 10.42, 9.65, 1, "3b 28 saal"), (10.71, 12.09, 10.945, 1, "3c sirf ghar"),
        (13.60, 14.30, 13.545, 1, "4a"), (14.59, 15.39, 14.365, 1, "4b"), (15.85, 17.02, 15.43, 1, "5"),
        (18.00, 20.31, 18.07, 1, "6"), (21.29, 23.32, 21.10, 1.07, "7a"), (23.67, 24.97, 23.13, 1, "7b bas is mahine"),
        (26.24, s8, 25.475, 1, "8a shayad isliye"), (s8, 29.13, 26.585, 1, "8b jab koi mard"), (30.16, 32.37, 29.54, 1, "9"),
        (32.97, 33.90, 32.335, 1, "10a"), (35.02, 37.17, 33.565, 1, "10b")]
PRE_PAD, POST_PAD, FADE = 0.04, 0.08, 0.012
vo = np.zeros(int((DUR + 1.5) * SR), np.float32); log = []
for i, (a, b, tgt, tempo, name) in enumerate(PLAN):
    a0 = a - PRE_PAD; b0 = b + POST_PAD
    if i + 1 < len(PLAN): b0 = min(b0, PLAN[i + 1][0] - 0.01) if PLAN[i + 1][0] > a else b0
    seg = clean[rt(a0):rt(b0)].copy()
    if tempo != 1: seg = ff(seg, f"atempo={tempo}")
    n = int(FADE * SR); w = np.ones(len(seg), np.float32); w[:n] = np.linspace(0, 1, n); w[-n:] = np.linspace(1, 0, n); seg *= w
    st = int((tgt - PRE_PAD / tempo) * SR); vo[st:st + len(seg)] += seg
    log.append({"phrase": name, "src_reel_s": [round(a, 3), round(b, 3)], "target_s": round(tgt, 3), "end_s": round(tgt + (b - a) / tempo, 3), "tempo": tempo,
                "shift_s": round(tgt - a, 3)})

# tone toward the reference voice
# (pass 2, measured against the reference: lows were +2.9 dB heavy, 200-500 Hz 1.6 dB thin, 8-12 kHz 5 dB dull, level swing 2.2 vs 3.1 dB)
vo = ff(vo, "equalizer=f=140:t=h:w=200:g=0.5,equalizer=f=320:t=q:w=1.2:g=2.5,equalizer=f=750:t=q:w=1.4:g=-2,"
            "equalizer=f=3500:t=q:w=1.5:g=1.0,equalizer=f=8000:t=q:w=1.2:g=3.5,equalizer=f=10500:t=q:w=1.0:g=3,"
            "acompressor=threshold=-22dB:ratio=2:attack=8:release=150:makeup=2.5dB:knee=6")
# depth: small room
rng = np.random.default_rng(6); L = int(0.9 * SR); t = np.arange(L) / SR
ir = rng.normal(0, 1, L) * np.exp(-6.9 * t / 0.6); ir[:int(0.018 * SR)] = 0
for d, g in ((0.011, 0.5), (0.017, 0.35), (0.023, 0.3), (0.031, 0.22)): ir[int(d * SR)] += g * 8
ir = signal.lfilter(*signal.butter(2, 6000 / (SR / 2)), ir); ir /= np.sqrt((ir ** 2).sum())
wet = signal.fftconvolve(vo, ir)[:len(vo)].astype(np.float32)
wet = signal.lfilter(*signal.butter(2, 180 / (SR / 2), "high"), wet).astype(np.float32)
vo = vo + 0.16 * wet / (np.sqrt((wet ** 2).mean()) / max(np.sqrt((vo ** 2).mean()), 1e-9))
# room tone under the whole VO (the take's own quiet pre-roll, cleaned, looped with crossfades) so gaps never drop to digital silence
rt_src = clean[int(0.05 * SR):int(1.05 * SR)]; xf = int(0.2 * SR); tone = np.zeros(len(vo), np.float32); pos = 0
win = np.ones(len(rt_src), np.float32); win[:xf] = np.linspace(0, 1, xf); win[-xf:] = np.linspace(1, 0, xf)
while pos < len(tone): seg = (rt_src * win)[:len(tone) - pos]; tone[pos:pos + len(seg)] += seg; pos += len(rt_src) - xf
vo = vo + tone * (10 ** (-62 / 20) / max(np.sqrt((tone ** 2).mean()), 1e-9))
vo = vo[:int((DUR + 0.25) * SR)]; k = int(0.25 * SR); vo[-k:] *= np.linspace(1, 0, k)
stem = A / "vo_take06_final.wav"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "f32le", "-ar", str(SR), "-ac", "1", "-i", "-", "-af", loudnorm_linear(vo, -16, -2),
                "-ar", str(SR), "-c:a", "pcm_s24le", str(stem)], input=vo.astype(np.float32).tobytes(), check=True)
# mix over the IG export's natural sound and mux onto the picture (video stream copied); static gain to -14 LUFS
nat = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(VID), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
stem_x = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(stem), "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
m = min(len(nat), len(stem_x)); VOLDB = -14.0 - lufs(nat[:m] + stem_x[:m]) - 0.3
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(VID), "-i", str(stem), "-filter_complex",
                "[0:a]aformat=sample_rates=48000:channel_layouts=stereo[n];[1:a]aformat=sample_rates=48000:channel_layouts=stereo[v];"
                f"[v][n]amix=inputs=2:normalize=0:duration=first,volume={VOLDB:.2f}dB,alimiter=limit=0.84:attack=3:release=60:level=disabled,aresample=48000[a]",
                "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "320k", "-movflags", "+faststart", "-shortest", str(OUT)], check=True)
(REEL / "analysis/vo_place.json").write_text(json.dumps({"take": TAKE.name, "reel_t0_in_take_s": T0, "split_duniya": round(s2, 3),
                                                        "split_jab": round(s8, 3), "phrases": log}, indent=1))
for r in log: print(f"{r['phrase']:18s} src {r['src_reel_s'][0]:6.2f}-{r['src_reel_s'][1]:6.2f} -> {r['target_s']:6.2f}-{r['end_s']:6.2f}  shift {r['shift_s']:+.2f}" + (f"  tempo {r['tempo']}" if r['tempo'] != 1 else ""))
print("✓", stem.name, "+", OUT.name)
