"""v10 (reel-local, 2026-11-12): blend 12 (Pexels diya, AE Timewarp 50 %) and 19 (Veo cracker man, Timewarp 50 %, face from
source) into the director's footage. Director: "looks a little fake ... different from the rest of the footage ... the hand is
not shaking, not moving, and the pan looks too good to be true. Don't change it, optimise it so they blend."

Same pictures, same timing. Two things change, both taken from the director's own clips (tools/measure_blend_v10.py on v8b):
  1. HANDHELD: the camera path of the director's handheld shots (13 C050, 14 C051, 16 C063, 18 C064, 09 C053; measured on the
     v8b master's window, outer ring, 540 px analysis), each detrended (their own pans removed), chained, scaled by GAIN and
     added to the clip as a sub-pixel move, inside a ZOOM margin so no edge shows. 12 keeps its rise; the rise now wanders and
     shakes like a hand. Window px -> source px through each clip's Premiere Scale (12 ~57.7 %, 19 ~101 %).
  2. GRAIN (and for 19 a touch of softness): fine luma + weaker chroma grain, stronger in the shadows, sized so the export's
     grain metric lands at the real clips' level. The export/source ratio is measured per clip (the grade and Sharpen -30
     change it), so the added amount is solved, not guessed.
v10b: on 19 the solved grain landed at 0.20, not 0.48: Premiere's Sharpen -30 on 19 removes fine grain far more than the
content the ratio was measured on. From the measured response (0.53 codes added 0.12 to the metric), 2.0 codes lands 0.48:
  tools/blend_v10.py --only 19 --amp 2.0 --suffix _b
v10c: the review of v10b found 19's 0.5 px softening moves it AWAY from the real shots (edge-detail ratio 0.30 against
0.43-0.58; skin waxier than 18's face), and 19 already has Lumetri Sharpen -30. Softening off, grain and path kept:
  tools/blend_v10.py --only 19 --amp 2.0 --blur 0 --suffix _c
Native yuv422p10le in and out (ProRes 422 HQ, bt709 tags on the raw input as tools/fix19_v8b.py).
Usage (reel folder): ../../.venv/bin/python tools/blend_v10.py
"""
import json
import subprocess
import sys
from pathlib import Path

import numpy as np
from scipy import ndimage

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "scripts"))
import motion_audit as ma  # noqa: E402

MASTER = "renders/masters/could-not-go-home-diwali_v8b_master.mov"
WIN = (0, 606, 1080, 608)
REAL = [("13_C050_paan", 20.56, 22.16), ("14_C051_paan_look", 22.16, 23.76), ("16_C063_foam", 25.36, 26.92),
        ("18_C064_look", 26.92, 28.52), ("09_C053_serve", 12.64, 14.24)]
GAIN, ZOOM = 1.25, 1.02
# name, source, out, frames, Premiere scale (fraction), export grain now, target export grain, luma blur sigma
CLIPS = [
    ("12", "renders/ae/12_S32_diya_tw50.mov", "renders/v10/12_S32_diya_tw50_hand.mov", 88, 0.577, 0.47, 0.50, 0.0, 0),
    ("19", "renders/v8/19_S31_cracker_tw50_facemix.mov", "renders/v10/19_S31_cracker_tw50_hand.mov", 80, 1.01, 0.16, 0.48, 0.5, 90),
]
NOTES = Path("analysis/v10_notes")


def real_path():
    """Chained, detrended camera path of the director's handheld shots, window px per frame."""
    ma.AW = 540
    small, _ = ma.frames(Path(MASTER), WIN, 25.0)
    k = 1080 / small.shape[2]; segs = []; end = np.zeros(2)
    for name, st, en in REAL:
        i0, i1 = int(round(st * 25)) + 2, int(round(en * 25)) - 2
        d = np.array([ma.ring_shift(small[i], small[i + 1]) for i in range(i0, i1 - 1)]) * k
        p = np.vstack([[0, 0], np.cumsum(d, 0)]); t = np.arange(len(p))
        p = p - np.stack([np.polyval(np.polyfit(t, p[:, j], 1), t) for j in range(2)], 1)
        p = p - p[0] + end; end = p[-1]; segs.append(p if not segs else p[1:])
        print(f"  path {name}: {len(p)} frames, rms {np.sqrt((p - p.mean(0)) ** 2).mean():.2f} px")
    return np.vstack(segs)


def grain_metric(y8):
    """As tools/measure_blend_v10.py: luma minus its 3x3 median, std over the flattest 30 %."""
    r = y8 - ndimage.median_filter(y8, 3)
    loc = ndimage.uniform_filter(np.abs(ndimage.sobel(y8)), 9)
    return float(r[loc < np.quantile(loc, 0.3)].std())


def read(path, w, h):
    b = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-"], capture_output=True).stdout
    a = np.frombuffer(b, np.uint16); n = w * h * 2; out = []
    for i in range(a.size // n):
        f = a[i * n:(i + 1) * n].astype(np.float32)
        out.append([f[:w * h].reshape(h, w), f[w * h:w * h * 3 // 2].reshape(h, w // 2), f[w * h * 3 // 2:].reshape(h, w // 2)])
    return out


def window_luma8(y10, scale):
    """The source luma as the export's window sees it: resized by the Premiere scale, 8-bit codes."""
    y = ndimage.zoom(y10, scale, order=1) if abs(scale - 1) > 0.02 else y10
    return y / 4.0


def move(plane, dx, dy, cx_div):
    """Zoom about the centre by ZOOM and shift by (dx, dy) source px; chroma planes have half the x resolution."""
    h, w = plane.shape
    m = np.array([1 / ZOOM, 1 / ZOOM]); c = np.array([(h - 1) / 2, (w - 1) / 2])
    off = c - m * c - np.array([dy, dx / cx_div]) / ZOOM
    return ndimage.affine_transform(plane, m, offset=off, order=3, mode="nearest")


def grain_field(rng, h, w, sigma):
    g = ndimage.gaussian_filter(rng.normal(0, 1, (h, w)).astype(np.float32), sigma)
    return g / g.std()


def main():
    NOTES.mkdir(parents=True, exist_ok=True); Path("renders/v10").mkdir(parents=True, exist_ok=True)
    only = sys.argv[sys.argv.index("--only") + 1] if "--only" in sys.argv else None
    amp_over = float(sys.argv[sys.argv.index("--amp") + 1]) if "--amp" in sys.argv else None
    suffix = sys.argv[sys.argv.index("--suffix") + 1] if "--suffix" in sys.argv else ""
    blur_over = float(sys.argv[sys.argv.index("--blur") + 1]) if "--blur" in sys.argv else None
    path = real_path() * GAIN
    rep = {"gain": GAIN, "zoom": ZOOM, "path_frames": len(path)}
    for key, src, dst, nf, sc, g_now, g_tgt, blur, off in CLIPS:
        if only and key != only:
            continue
        dst = dst.replace(".mov", suffix + ".mov")
        if blur_over is not None:
            blur = blur_over
        w, h = (1920, 1080) if key == "12" else (1080, 1920)
        X = read(src, w, h)
        if len(X) != nf:
            raise SystemExit(f"{src}: {len(X)} frames, expected {nf}")
        pth = path[off:off + nf] - path[off:off + nf].mean(0)
        if len(pth) < nf:
            raise SystemExit("real path too short")
        pth_src = pth / sc
        # grain: export/source ratio from the clip as it is, then solve the added amount
        rng = np.random.default_rng(int(key))
        samp = [X[i][0] for i in (5, nf // 2, nf - 6)]
        m0 = np.mean([grain_metric(window_luma8(y, sc)) for y in samp]); ratio = g_now / m0
        need_src = np.sqrt(max((g_tgt / ratio) ** 2 - m0 ** 2, 0))          # metric units at window scale
        unit = np.mean([grain_metric(window_luma8(y + 4.0 * grain_field(rng, h, w, 0.6), sc)) for y in samp])
        unit = np.sqrt(max(unit ** 2 - m0 ** 2, 1e-6))                        # metric per 1 code (8-bit) of grain, source px
        amp = need_src / unit if amp_over is None else amp_over               # 8-bit codes
        print(f"{key}: source metric {m0:.3f}, export/source {ratio:.2f}, add grain {amp:.2f} codes (8-bit), "
              f"path rms {np.sqrt((pth ** 2).sum(1).mean()):.2f} window px = {np.sqrt((pth_src ** 2).sum(1).mean()):.2f} source px")
        enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "yuv422p10le", "-s", f"{w}x{h}", "-r", "25",
                                "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", "-i", "-",
                                "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", dst], stdin=subprocess.PIPE)
        for i, (Y, U, V) in enumerate(X):
            dx, dy = pth_src[i]
            Y = move(Y, dx, dy, 1); U = move(U, dx, dy, 2); V = move(V, dx, dy, 2)
            if blur:
                Y = ndimage.gaussian_filter(Y, blur)
            yn = np.clip((Y - 64) / 876, 0, 1)
            wgt = 0.75 + 0.5 * (1 - yn) - 0.4 * np.clip((yn - 0.85) / 0.15, 0, 1)   # more in the shadows, little in highlights
            Y = Y + 4.0 * amp * wgt * grain_field(rng, h, w, 0.6)
            cg = grain_field(rng, h, w // 2, 1.0) * 4.0 * amp * 0.35
            U = U + cg; V = V - 0.6 * cg + grain_field(rng, h, w // 2, 1.0) * 4.0 * amp * 0.2
            planes = [np.clip(np.rint(p), 0, 1023).astype(np.uint16) for p in (Y, U, V)]
            enc.stdin.write(b"".join(p.tobytes() for p in planes))
        enc.stdin.close(); enc.wait()
        rep[key] = {"src": src, "out": dst, "frames": nf, "scale": sc, "grain_added_8bit": round(float(amp), 3),
                    "export_over_source": round(float(ratio), 3), "luma_blur": blur,
                    "path_window_px": [[round(float(a), 3), round(float(b), 3)] for a, b in pth]}
        print("  ->", dst)
    (NOTES / f"blend_v10{suffix}.json").write_text(json.dumps(rep, indent=1))


if __name__ == "__main__":
    main()
