#!/usr/bin/env python3
"""KOLKATA round 6: cut the guide's name out of the song's spoken intro.

Director (2026-11-07): the spoken line should be "ami … apnader guide" ("I am … your guide") without the name.
Measured on music/kolkata.wav (speech-band envelope, 20 ms): "Ami" ends 25.60 s; the name runs 26.15–27.95 s;
"apnader guide" starts 28.35 s; between them only the quiet music bed (about −35 dB). The cut removes
25.720 → 28.273 s = 2.553 s = exactly 5 beats at 117.5 BPM, so the bed stays on its beat grid, with a 30 ms
equal-power crossfade at the join.

NOTE: Instagram's library "Kolkata" can't be edited, so this version of the line exists only in the baked _mix.

Usage (studio root): python3 projects/kolkata/tools/song_edit_v6.py
"""
import numpy as np
import soundfile as sf

SRC = "projects/kolkata/music/kolkata.wav"
OUT = "projects/kolkata/music/kolkata_v6_edit.wav"
CUT_A, CUT_B = 25.720, 28.273
XF = 0.030

a, sr = sf.read(SRC, dtype="float32", always_2d=True)
ia, ib, n = int(round(CUT_A * sr)), int(round(CUT_B * sr)), int(round(XF * sr))
t = np.linspace(0, np.pi / 2, n, dtype=np.float32)[:, None]
head, tail = a[:ia + n // 2], a[ib - n // 2:]   # crossfade centred on each cut point: removes exactly CUT_B − CUT_A
join = head[-n:] * np.cos(t) + tail[:n] * np.sin(t)
out = np.concatenate([head[:-n], join, tail[n:]])
sf.write(OUT, out, sr, subtype="PCM_24")
print(f"{OUT}: {len(a) / sr:.3f} s → {len(out) / sr:.3f} s (removed {(len(a) - len(out)) / sr:.3f} s, {XF * 1000:.0f} ms crossfade)")
