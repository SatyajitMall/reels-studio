#!/usr/bin/env python3
"""Review v10 fixes (analysis/review_v10.md: FAIL, 1 major + 2 minor), v10b. A and C are v10's bakes, unchanged.
  B  #1 softer than A at 100 %: the 21-frame 1x stack averaged detail away. Now the 9 sharpest of 21 frames, shift-and-add at 2x
        (tools/stack_r10b.py; output Laplacian var +45 %), framed a little wider: eye pair 24 -> 28 % (1.10 -> 1.29x).
  B  #2 title on bright gold: the soft dark plate under it -28 % -> -36 %.
  (#3 moving grain: V4 grain 6 -> 9 % in Premiere.)
Output renders/bakes_r10b/V1_timeline_v10b.mov. Usage: python tools/bake_r10b.py [--compose-only]
"""
import sys, json, argparse
from pathlib import Path
import numpy as np
from PIL import Image
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_r5 as R, bake_r7 as R7, bake_r9c as R9C, bake_r10 as R10, stack_r10b as S2
B = R.B
OUT = REEL / "renders/bakes_r10b"; V10 = REEL / "renders/bakes_r10"
B_SPAN = (0.24, 0.28)
R9C.PLATE = (540, 1470, 430, 140, 0.36)

def shot_B():
    N = R.F_C - R.F_B; pr = dict(exp=-0.12); px = 235; c0, c1 = R.CW(px, B_SPAN[0]), R.CW(px, B_SPAN[1])
    p = OUT / "B_stack2x.png"
    if p.exists(): base = Image.open(p).convert("RGB")
    else:
        base, info = S2.stack2x(R7.C208, R7.TRK["2"], 0.8, c0, 21, 9); base.save(p); (OUT / "B_stack2x.json").write_text(json.dumps(info))
    gains = B.primary_params(R.push_from_big(base, c0, c0), wb=0.5, exp=pr["exp"])
    enc = B.encoder(OUT / "B.mov", "rgb48le")
    for k in range(N):
        f = k / (N - 1); cw = c0 + (c1 - c0) * B.ease(f)
        x = B.halation(R.grade(R10.sharpen(R.push_from_big(base, c0, cw, du=0.012 * (f - 0.5))), gains, pr))
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "B", "frames": N, "span": B_SPAN, "enlarge": [round(1080 * s / px, 2) for s in B_SPAN]}

def compose():
    seq = [B.reader(V10 / "A.mov"), B.reader(OUT / "B.mov"), B.reader(V10 / "C.mov")]
    enc = B.encoder(OUT / "V1_timeline_v10b.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= R.F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < R.F_B else (1 if t < R.F_C else 2); x = R7.clarity(next(seq[s]), amt=R10.CLARITY)
            pl = R9C.plate(t)
            if pl is not None: x = x * pl
            if t < 8: x = x * (t / 8)
            for c in (R.F_B, R.F_C):
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_v10b.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--compose-only", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    if not a.compose_only: print(shot_B(), flush=True)
    compose()

if __name__ == "__main__":
    main()
