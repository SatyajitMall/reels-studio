#!/usr/bin/env python3
"""Round 4 ("the first transition is not up to the mark, and neither is all other transition"): render transition
style previews on real cuts, with the music, so the director can choose by watching.
Segments: 1 = her eye opens (esraj -> black blink on the 4.16 swell -> eye opens), A = blink, B = zoom through the eye,
C = hard cut on the stroke + 2-frame warm flash. Preview size 540x960, colour = look A (Kodak 2383 80 %) for preview only.
Usage: python tools/transition_lab.py -o renders/previz/transitions_r4.mp4
"""
import sys, subprocess, argparse, json
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy.ndimage import gaussian_filter
REEL = Path(__file__).resolve().parents[1]; STUDIO = REEL.parents[1]
sys.path.insert(0, str(STUDIO / "scripts")); import look_preview as lp
W, H, FPS = 540, 960, 25; YE = 0.40 * H; XE = 0.5 * W

def read(src, n, ss=0.0, tv=True):
    vf = (f"scale={W}:{H}" + (":in_range=tv:out_range=pc" if tv else "")); 
    p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{ss:.3f}", "-i", str(src), "-frames:v", str(n), "-vf", vf, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(p.stdout, np.uint8); return a[: (a.size // (W * H * 3)) * W * H * 3].reshape(-1, H, W, 3).astype(np.float32) / 255

def zoom(fr, s, cx=XE, cy=YE):
    im = Image.fromarray((fr * 255).astype(np.uint8)); w2, h2 = W / s, H / s
    box = (cx - w2 * cx / W, cy - h2 * cy / H, cx - w2 * cx / W + w2, cy - h2 * cy / H + h2)
    return np.asarray(im.resize((W, H), Image.BICUBIC, box=box)).astype(np.float32) / 255

def zoomblur(fr, s0, s1, taps=6):
    return np.mean([zoom(fr, s0 * (s1 / s0) ** (k / (taps - 1))) for k in range(taps)], axis=0)

yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
def lid(fr, open_):   # open_ 1 = fully open, 0 = shut; almond aperture about the eye-line, upper and lower lids meet on it together
    o = max(open_, 1e-3); rx = 1.35 * W; m_ = 0.18 * H
    ry = np.where(yy < YE, o * (YE + m_), o * (H - YE + m_))
    d = ((xx - XE) / rx) ** 2 + ((yy - YE) / ry) ** 2
    m = np.clip((1 - d) / 0.06, 0, 1); m = gaussian_filter(m, 3)
    return fr * m[..., None]

ease_in = lambda t: t * t; ease_out = lambda t: 1 - (1 - t) ** 2

FE = 0.09 * H   # reference blink: straight lids with a wide soft (faded) edge, measured on Video-14732 at 7.93 and 16.02 s
def slit(fr, o):
    o = max(o, 0.0); top = YE - o * (YE + FE); bot = YE + o * (H - YE + FE)
    m = np.clip((yy - top) / FE, 0, 1) * np.clip((bot - yy) / FE, 0, 1); m = m * m * (3 - 2 * m)
    soft = gaussian_filter(fr, (2.5 * (1 - o), 2.5 * (1 - o), 0)) if o < 0.95 else fr   # the reference's slit content goes soft
    return soft * m[..., None]
CLOSE = [0.62, 0.28, 0.06]; OPEN = [0.22, 0.60, 0.90]   # 25 fps version of the reference's 30 fps curve

def blink_ref(A, B, black=1):
    return list(A[:-3]) + [slit(A[-3 + k], CLOSE[k]) for k in range(3)] + [np.zeros_like(A[0])] * black + [slit(B[k], OPEN[k]) for k in range(3)] + list(B[3:])

def seg_ref_eye_opens():
    es = read(REEL / "renders/gen/esraj_final.mp4", 110, ss=0.6, tv=False); A = es[80:104]
    B = read(REEL / "renders/bakes_v4/05_Oct20_C050.mov", 30)
    return blink_ref(A, B), 3.20, "1  HER EYE OPENS  (reference blink)"

def seg_ref_run():
    A, B = pair(); return blink_ref(A, B), 15.68 - len(A) / FPS, "R  REFERENCE BLINK  (on the drum stroke)"

def seg_ref_drop():
    A = read(REEL / "renders/bakes_v4/04_Oct20_C059.mov", 51)[5:51]; B = read(REEL / "renders/bakes_v4/06_Oct20_C056.mov", 40)
    return blink_ref(A[-24:], B[:30]), 7.88 - 24 / FPS, "R  REFERENCE BLINK  (on the drop, 7.88)"

def seg_eye_opens():
    es = read(REEL / "renders/gen/esraj_final.mp4", 110, ss=0.6, tv=False)   # AI clip, frame-for-frame 24->25
    A = es[80:104]                                                             # reel 3.20-4.16
    B = read(REEL / "renders/bakes_v4/05_Oct20_C050.mov", 30)
    out = list(A[:-5]) + [lid(A[-5 + k], 1 - ease_in((k + 1) / 5)) for k in range(5)]   # lids close over 5 frames onto the swell
    out += [np.zeros_like(A[0])] * 2                                                       # 2 dark frames
    out += [lid(B[k], ease_out((k + 1) / 8)) for k in range(8)] + list(B[8:30])            # her eye opens over 8 frames
    return out, 3.20 - 0.0, "1  HER EYE OPENS  (first transition)"

def pair():
    A = read(REEL / "renders/bakes_v4/08_Oct17_C145.mov", 34)[3:32]   # C145 up to the 15.68 cut (29 frames)
    B = read(REEL / "renders/bakes_v4/09_Oct18_C208.mov", 35)[2:33]   # C208 from the cut
    return A, B

def seg_blink():
    A, B = pair(); out = list(A[:-3]) + [lid(A[-3 + k], 1 - ease_in((k + 1) / 3)) for k in range(3)]
    out += [np.zeros_like(A[0])]; out += [lid(B[k], ease_out((k + 1) / 4)) for k in range(4)] + list(B[4:])
    return out, 15.68 - (len(A) + 0) / FPS, "A  BLINK  (lids close on one goddess, open on the next)"

def seg_zoom():
    A, B = pair(); n = 5; out = list(A[:-n])
    for k in range(n): s0 = 1 + 3 * ease_in(k / n); s1 = 1 + 3 * ease_in((k + 1) / n); out.append(zoomblur(A[-n + k], s0, s1))
    for k in range(n): s0 = 4 - 3 * ease_out(k / n); s1 = 4 - 3 * ease_out((k + 1) / n); out.append(zoomblur(B[k], s0, s1))
    out += list(B[n:]); return out, 15.68 - len(A) / FPS, "B  ZOOM THROUGH THE EYE"

def seg_hard():
    A, B = pair(); out = list(A); flash = lambda f, a: np.clip(f + a * np.array([1.0, 0.85, 0.55]) * (0.6 + 0.4 * f), 0, 1)
    out += [flash(B[0], 0.55), flash(B[1], 0.22)] + list(B[2:]); return out, 15.68 - len(A) / FPS, "C  HARD CUT ON THE STROKE  (+ flash on big hits)"

CUBE = None   # --cube: grade the preview with one of the reel's .cube looks instead of look A
def grade(frames):
    lut = lp.creative_lut_dir(); arr = (np.stack(frames) * 255 + 0.5).astype(np.uint8)
    fc = (f"format=gbrp,lut3d=file='{str(CUBE).replace(':', chr(92) + ':')}',vignette=angle=0.42" if CUBE else lp.chain("k500t_2383", lut, 0.8, W))
    p = subprocess.run(["ffmpeg", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "25", "-i", "-",
                        "-filter_complex", fc + ",format=rgb24", "-f", "rawvideo", "-pix_fmt", "rgb24", "-"],
                       input=arr.tobytes(), capture_output=True)
    return np.frombuffer(p.stdout, np.uint8).reshape(-1, H, W, 3).copy()

def main():
    global CUBE
    ap = argparse.ArgumentParser(); ap.add_argument("-o", "--out", required=True); ap.add_argument("--ref", action="store_true", help="reference-style blinks only")
    ap.add_argument("--cube"); a = ap.parse_args(); CUBE = (REEL / a.cube) if a.cube else None
    try: font = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 20)
    except OSError: font = ImageFont.load_default()
    vid, aud, gap = [], [], 10; sheet = []
    for fn in ((seg_ref_eye_opens, seg_ref_drop, seg_ref_run) if a.ref else (seg_eye_opens, seg_blink, seg_zoom, seg_hard)):
        frames, t_audio, label = fn(); g = grade(frames)
        for k in range(len(g)):
            im = Image.fromarray(g[k]); d = ImageDraw.Draw(im); d.rectangle([0, 0, W, 34], fill=(0, 0, 0)); d.text((10, 7), label, font=font, fill=(255, 225, 140)); g[k] = np.asarray(im)
        vid += list(g) + [np.zeros((H, W, 3), np.uint8)] * gap
        aud.append((t_audio, len(g) / FPS)); sheet.append(g)
    tmp = Path(a.out).with_suffix(".tmp.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", "25", "-i", "-",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "16", str(tmp)], input=np.stack(vid).tobytes(), check=True)
    # audio: the reference music under each segment, silence in the gaps
    parts = []; filt = []
    for i, (t0, dur) in enumerate(aud):
        filt.append(f"[1:a]atrim={t0:.3f}:{t0 + dur:.3f},asetpts=PTS-STARTPTS,afade=t=in:d=0.05,afade=t=out:st={dur - 0.08:.3f}:d=0.08,apad=pad_dur={gap / FPS:.3f}[a{i}]")
    filt.append("".join(f"[a{i}]" for i in range(len(aud))) + f"concat=n={len(aud)}:v=0:a=1[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(tmp), "-i", str(REEL / "references/ref_audio.wav"), "-filter_complex", ";".join(filt),
                    "-map", "0:v", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "256k", "-shortest", a.out], check=True)
    tmp.unlink()
    # strip for checking: every 2nd frame around each transition
    rows = []
    for g in sheet:
        c = len(g) // 2 if g is not sheet[0] else 24
        idx = [max(0, min(len(g) - 1, i)) for i in range(c - 8, c + 10, 2)]
        rows.append(np.concatenate([np.asarray(Image.fromarray(g[i]).resize((135, 240))) for i in idx], axis=1))
    Image.fromarray(np.concatenate(rows, axis=0)).save(Path(a.out).with_suffix(".jpg"), quality=88)
    print("✓", a.out, len(vid), "frames")

if __name__ == "__main__":
    main()
