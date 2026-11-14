#!/usr/bin/env python3
"""Round 5 bake (director: "like the reference"; the red clay Durga carries the reel; "tight eyes first" + an AI upscaler).

Three shots, the reference's structure:
  A  0.00-7.88  the singer (AI esraj) as a Screen double exposure over her face (C163, sharpest frame, slow push); title over it
  -- blink on 7.88 (the drop)
  B  7.88-16.00 her eyes live (C163 0.00-4.57, eye-locked, push), slowed ~1.48x by motion interpolation so the haze drifts
  -- blink on 16.00 (the 16.02 accent)
  C 16.00-21.96 closer (C164 0.20-1.90 live, eye-locked) then held on its last frame under the same push; end card
  black on frame 549.
Every close-up crop is taken at source resolution and AI-upscaled with Real-ESRGAN x4plus (tools/realesrgan), then scaled
to 1080x1920. Primary per clip as bake_v6 (grey balance + exposure), pre-look halation. Output renders/bakes_r5/V1_timeline_r5.mov.
Usage: python tools/bake_r5.py [--only A,B,C] [--compose-only]
"""
import sys, json, subprocess, math, tempfile, shutil, argparse
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage
REEL = Path(__file__).resolve().parents[1]; sys.path.insert(0, str(REEL / "tools"))
import bake_v6 as B   # frames(), encoder(), reader(), ease(), slit(), primary_params(), halation(), luma(), smooth(), BL_*

ESR = REEL / "tools/realesrgan/realesrgan-ncnn-vulkan"; MODELS = REEL / "tools/realesrgan/models"
OUT = REEL / "renders/bakes_r5"; W4, H4 = 2160, 3840
TRK = json.loads((REEL / "analysis/eye_tracks_r5.json").read_text())
C163 = str(REEL / "raw/b-roll/A001_10172022_C163.mov"); C164 = str(REEL / "raw/b-roll/A001_10172024_C164.mov")
SINGER = str(REEL / "renders/gen/esraj_final.mp4")
F_B, F_C, F_END = 197, 400, 549          # cut frames (7.88, 16.00) and the black frame
CW = lambda px, span: px / (span * W4)  # crop width fraction for an eye span (fraction of output width)
EYE163, EYE164 = 236, 267               # eye-pair widths in source px (survey round 4b)
PRIM163 = dict(exp=0.10, blk=0.05, sat=0.72)   # v2b fixes for C163's incense haze (no sharpen: the AI upscaler replaces it)
PRIM164 = dict()
SING_W, SING_GAIN = 0.55, 0.80   # v6 check: at 0.70 / 1.0 the white kurta washed shot A to luma 0.41 vs 0.23-0.25 in B/C

def esrgan_dir(src_dir, dst_dir):
    subprocess.run([str(ESR), "-i", str(src_dir), "-o", str(dst_dir), "-n", "realesrgan-x4plus", "-s", "4", "-m", str(MODELS), "-f", "png"],
                   check=True, capture_output=True)

def box_for(ex, ey, cw, u=0.5, v=0.40):
    cwp = cw * W4; chp = cwp * 16 / 9
    l = min(max(ex * W4 - u * cwp, 0), W4 - cwp); t = min(max(ey * H4 - v * chp, 0), H4 - chp)
    return (l, t, l + cwp, t + chp)

def grade(fr, gains, pr):
    x = np.clip(fr * gains, 0, 1)
    if pr.get("sat", 1.0) != 1.0:
        yy = B.luma(x)[..., None]; x = np.clip(yy + (x - yy) * pr["sat"], 0, 1)
    if "blk" in pr: x = np.clip((x - pr["blk"]) / (1 - pr["blk"]), 0, 1)
    return x

def ai_crops(crops, tag):
    """AI-upscale a list of PIL crops (any size); returns 1080x1920 float frames in order (streams through a temp dir)."""
    d = Path(tempfile.mkdtemp(prefix=f"esr_{tag}_")); i = d / "in"; o = d / "out"; i.mkdir(); o.mkdir()
    for k, im in enumerate(crops): im.save(i / f"{k:04d}.png")
    esrgan_dir(i, o)
    out = [np.asarray(Image.open(o / f"{k:04d}.png").convert("RGB").resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255 for k in range(len(crops))]
    shutil.rmtree(d); return out

def sharpest_time(src, t0, t1, ex, ey):
    best = (-1.0, t0)
    for t in np.arange(t0, t1, 1 / 15):
        im = next(B.frames(src, t, 1, False, W4, H4)); g = np.asarray(im.convert("L")).astype(np.float32)
        y0, x0 = int(ey * H4), int(ex * W4); r = g[max(y0 - 200, 0):y0 + 200, max(x0 - 350, 0):x0 + 350]
        best = max(best, (float(ndimage.laplace(r).var()), float(t)))
    return best[1]

def denoise(im):
    """v8: spatial denoise at source resolution before any enlargement (phone HEVC noise and blocking)."""
    d = Path(tempfile.mkdtemp(prefix="dn_")); i = d / "i.png"; o = d / "o.png"; im.save(i)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(i), "-vf", "nlmeans=s=1.6:p=7:r=13", str(o)], check=True)
    out = Image.open(o).convert("RGB"); shutil.rmtree(d); return out

def ai_still(im):
    """AI-upscale one crop (x4plus) and return the big PIL image."""
    d = Path(tempfile.mkdtemp(prefix="esrS_")); (d / "i").mkdir(); (d / "o").mkdir(); im.save(d / "i" / "a.png")
    esrgan_dir(d / "i", d / "o"); big = Image.open(d / "o" / "a.png").convert("RGB"); shutil.rmtree(d); return big

def push_from_big(big, cw0, cw, n_out=(1080, 1920), du=0.0):
    """big = AI-upscaled image of the crop at cw0 (eyes at u .5, v .40); return the tighter view at cw, eyes kept at (.5, .40)."""
    bw, bh = big.size; s = cw / cw0; w, h = bw * s, bh * s
    l = 0.5 * bw - 0.5 * w + du * bw; t = 0.40 * bh - 0.40 * h
    l = min(max(l, 0), bw - w)
    return np.asarray(big.resize(n_out, Image.LANCZOS, box=(l, t, l + w, t + h))).astype(np.float32) / 255

def shot_A():
    N = F_B; tr = TRK["2"]; t_s = sharpest_time(C163, 0.0, 2.0, 0.4311, 0.4837)
    j = int(round(t_s * 30)); ex, ey = tr["ex"][min(j, len(tr["ex"]) - 1)], tr["ey"][min(j, len(tr["ey"]) - 1)]
    cw0, cw1 = CW(EYE163, 0.36), CW(EYE163, 0.42)
    im = next(B.frames(C163, t_s, 1, False, W4, H4)); crop = im.crop(tuple(round(v) for v in box_for(ex, ey, cw0)))
    d = Path(tempfile.mkdtemp(prefix="esrA_")); (d / "i").mkdir(); (d / "o").mkdir(); crop.save(d / "i" / "a.png")
    esrgan_dir(d / "i", d / "o"); big = Image.open(d / "o" / "a.png").convert("RGB"); shutil.rmtree(d)
    base0 = push_from_big(big, cw0, cw0); gains = B.primary_params(base0, wb=0.5, exp=PRIM163["exp"])
    sing = list(B.frames(SINGER, 0.0, N, False, 1080, 1920)); sing += [sing[-1]] * (N - len(sing))
    sg = B.primary_params(np.asarray(sing[N // 2]).astype(np.float32) / 255, wb=0.0, exp=0.0)
    enc = B.encoder(OUT / "A.mov", "rgb48le")
    for k in range(N):
        cw = cw0 + (cw1 - cw0) * B.ease(k / (N - 1))
        x = grade(push_from_big(big, cw0, cw), gains, PRIM163); x = B.halation(x)
        s = np.clip(np.asarray(sing[k]).astype(np.float32) / 255 * sg * SING_GAIN, 0, 1) ** 1.2
        x = 1 - (1 - x) * (1 - SING_W * s)                   # the singer as a Screen double exposure (as the reference)
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "A", "frames": N, "still_t": t_s}

def shot_B():
    N = F_C - F_B; tr = TRK["2"]; n_src = 137
    ex_s = B.smooth(tr["ex"][:n_src], 1.5); ey_s = B.smooth(tr["ey"][:n_src], 1.5)
    cw0, cw1 = CW(EYE163, 0.44), CW(EYE163, 0.52)
    crops = []
    for j, im in enumerate(B.frames(C163, 0.0, n_src, False, W4, H4)):
        cw = cw0 + (cw1 - cw0) * B.ease(j / (n_src - 1)); crops.append(im.crop(tuple(round(v) for v in box_for(ex_s[j], ey_s[j], cw))))
    fr = ai_crops(crops, "B"); gains = B.primary_params(fr[n_src // 2], wb=0.5, exp=PRIM163["exp"])
    raw = OUT / "B_raw.mov"; enc = B.encoder(raw, "rgb48le")
    for x in fr:
        x = B.halation(grade(x, gains, PRIM163)); enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait()
    # slow ~1.48x with motion-compensated interpolation (static idol + drifting haze): 137 -> 203 frames
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(raw), "-vf",
                    f"setpts=PTS*{N + 2}/{n_src},minterpolate=fps=25:mi_mode=mci:mc_mode=aobmc:me_mode=bidir:vsbmc=1,tpad=stop_mode=clone:stop=6",
                    "-frames:v", str(N), "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-color_range", "tv", str(OUT / "B.mov")], check=True)
    return {"shot": "B", "frames": N, "src_frames": n_src}

def shot_C():
    N = F_END - F_C; tr = TRK["3"]; n_live = 51
    ex_s = B.smooth(tr["ex"][:n_live], 1.5); ey_s = B.smooth(tr["ey"][:n_live], 1.5)
    cw0, cw1 = CW(EYE164, 0.68), CW(EYE164, 0.76)   # clearly closer than B's last frame (0.52), so the 16.00 blink reveals her closer
    cwk = lambda k: cw0 + (cw1 - cw0) * B.ease(k / (N - 1))
    src = list(B.frames(C164, 0.20, n_live, False, W4, H4))
    crops = [src[j].crop(tuple(round(v) for v in box_for(ex_s[j], ey_s[j], cwk(j)))) for j in range(n_live)]
    hold_cw = cwk(n_live); crops.append(src[-1].crop(tuple(round(v) for v in box_for(ex_s[-1], ey_s[-1], hold_cw))))
    d = Path(tempfile.mkdtemp(prefix="esrC_")); (d / "i").mkdir(); (d / "o").mkdir()
    for k, im in enumerate(crops): im.save(d / "i" / f"{k:04d}.png")
    esrgan_dir(d / "i", d / "o")
    live = [np.asarray(Image.open(d / "o" / f"{k:04d}.png").convert("RGB").resize((1080, 1920), Image.LANCZOS)).astype(np.float32) / 255 for k in range(n_live)]
    big = Image.open(d / "o" / f"{n_live:04d}.png").convert("RGB"); shutil.rmtree(d)
    gains = B.primary_params(live[n_live // 2], wb=0.5, exp=0.0)
    enc = B.encoder(OUT / "C.mov", "rgb48le")
    for k in range(N):
        # live, then held on the last frame under a constant-speed push to the last frame (an eased stop read as "frozen" 21.36-21.88)
        x = live[k] if k < n_live else push_from_big(big, hold_cw, hold_cw + (cw1 * 0.97 - hold_cw) * (k - n_live + 1) / (N - n_live))
        x = B.halation(grade(x, gains, PRIM164)); enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes())
    enc.stdin.close(); enc.wait(); return {"shot": "C", "frames": N, "live": n_live}

def compose():
    seq = [B.reader(OUT / "A.mov"), B.reader(OUT / "B.mov"), B.reader(OUT / "C.mov")]; bounds = [0, F_B, F_C, F_END]
    enc = B.encoder(OUT / "V1_timeline_r5.mov", "rgb48le"); n = 0
    for t in range(550):
        if t >= F_END: x = np.zeros((1920, 1080, 3), np.float32)
        else:
            s = 0 if t < F_B else (1 if t < F_C else 2); x = next(seq[s])
            if t < 8: x = x * (t / 8)                                           # fade in from black
            for c in (F_B, F_C):                                                # the reference's blink on both cuts
                k = t - c
                if -3 <= k < 0: x = B.slit(x, B.BL_CLOSE[k + 3])
                elif k == 0: x = np.zeros_like(x)
                elif 1 <= k <= 3: x = B.slit(x, B.BL_OPEN[k - 1])
        enc.stdin.write((np.clip(x, 0, 1) * 65535 + 0.5).astype("<u2").tobytes()); n += 1
    enc.stdin.close(); enc.wait(); print("V1_timeline_r5.mov:", n, "frames")

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--only", default="A,B,C"); ap.add_argument("--compose-only", action="store_true"); a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True); log = OUT / "bake_r5.json"; meta = json.loads(log.read_text()) if log.exists() else {}
    if not a.compose_only:
        for s in a.only.split(","):
            m = {"A": shot_A, "B": shot_B, "C": shot_C}[s.strip()](); meta[s.strip()] = m; print(m, flush=True)
            log.write_text(json.dumps(meta, indent=1))
    compose()

if __name__ == "__main__":
    main()
