"""Skin-anchored per-shot correction (round 5): per shot, find channel gains (r, 1, b) + a skin-saturation factor so the
shot's mean skin colour lands on one target (the reference's skin: hue ~28 deg, sat ~0.46), blended with neutral balance
so whites don't swing.  Measured on graded on-screen frames; constant per shot.
"""
import colorsys
import numpy as np

TARGET_HUE, TARGET_SAT = 28.0, 0.46
def skin_mask(x):
    R, G, B = x[..., 0] * 255, x[..., 1] * 255, x[..., 2] * 255
    Y = 0.299 * R + 0.587 * G + 0.114 * B; Cb = 128 - 0.1687 * R - 0.3313 * G + 0.5 * B; Cr = 128 + 0.5 * R - 0.4187 * G - 0.0813 * B
    return (Cb > 77) & (Cb < 127) & (Cr > 133) & (Cr < 173) & (Y > 40) & (Y < 220)
def luma(c): return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2]
def solve(frames, w_neutral=0.3, min_frac=0.004, people=None):
    """frames: list of float RGB (graded). people: optional list of person alphas (0..1) gating the skin mask."""
    sk = []; ne = []
    for i, x in enumerate(frames):
        m = skin_mask(x)
        gated = people is not None and people[i] is not None
        if gated: m = m & (people[i] > 0.5)
        if (m.sum() >= 120) if gated else (m.mean() >= min_frac): sk.append(np.array([x[..., c][m].mean() for c in range(3)]))
        y = x @ np.array([0.2126, 0.7152, 0.0722]); mx = x.max(-1); mn = x.min(-1); ch = (mx - mn) / np.maximum(mx, 1e-4)
        n = (y > 0.18) & (y < 0.75) & (ch < 0.2)
        if n.sum() > 200: ne.append(np.array([x[..., c][n].mean() for c in range(3)]))
    if not sk: return np.ones(3), 1.0, {"skin": None}
    s = np.median(sk, axis=0); h, sat, v = colorsys.rgb_to_hsv(*s)
    t = np.array(colorsys.hsv_to_rgb(TARGET_HUE / 360, min(max(TARGET_SAT, sat * 0.85), sat * 1.25 if sat < TARGET_SAT else TARGET_SAT), v))
    t *= luma(s) / max(luma(t), 1e-6)                                  # keep skin brightness
    g_skin = t / np.maximum(s, 1e-6); g_skin /= g_skin[1]
    g = g_skin
    if ne:                                                            # keep neutrals near warm-neutral (R/G 1.04, B/G 0.86)
        n = np.median(ne, axis=0); g_ne = np.array([1.04 * n[1] / n[0], 1.0, 0.86 * n[1] / n[2]])
        g = np.exp((1 - w_neutral) * np.log(g_skin) + w_neutral * np.log(g_ne))
    g = np.clip(g, 0.8, 1.25)
    return g, 1.0, {"skin_hue": h * 360, "skin_sat": sat, "gains": g}
def apply(x, g):
    y0 = x @ np.array([0.2126, 0.7152, 0.0722]); o = np.clip(x * g, 0, 1); y1 = o @ np.array([0.2126, 0.7152, 0.0722])
    return np.clip(o * (y0 / np.maximum(y1, 1e-5))[..., None], 0, 1)     # luminance preserved

def skin_of(frames, min_frac=0.004, people=None):
    sk = []
    for i, x in enumerate(frames):
        m = skin_mask(x)
        gated = people is not None and people[i] is not None
        if gated: m = m & (people[i] > 0.5)
        if (m.sum() >= 120) if gated else (m.mean() >= min_frac): sk.append(np.array([x[..., c][m].mean() for c in range(3)]))
    return np.median(sk, axis=0) if sk else None
def apply_full(x, g, k):
    o = apply(x, g)
    if abs(k - 1) > 1e-3:
        y = (o @ np.array([0.2126, 0.7152, 0.0722]))[..., None]; o = np.clip(y + (o - y) * k, 0, 1)
    return o
def solve_iter(frames, iters=4, w_neutral=0.15, target_sat=0.44, people=None):
    """iterate: re-measure skin after each correction until hue is on target; then match skin saturation."""
    g = np.ones(3); k = 1.0
    for _ in range(iters):
        cur = [apply_full(x, g, 1.0) for x in frames]
        g_step, _, info = solve(cur, w_neutral=w_neutral, people=people)
        g = np.clip(g * g_step, 0.75, 1.35)
        if info.get("skin_hue") is not None and abs(info["skin_hue"] - TARGET_HUE) < 1.5: break
    s = skin_of([apply_full(x, g, 1.0) for x in frames], people=people)
    if s is not None:
        sat = colorsys.rgb_to_hsv(*s)[1]; k = float(np.clip(target_sat / max(sat, 1e-3), 0.85, 1.25))
    return g, k

def people_alphas(frames, tmpdir):
    """person matte per frame via hyperframes remove-background (local model); None where it fails."""
    import subprocess
    from pathlib import Path
    from PIL import Image
    out = []
    for i, x in enumerate(frames):
        a = Path(tmpdir) / f"s{i}.png"; b = Path(tmpdir) / f"s{i}_fg.png"
        Image.fromarray((np.clip(x, 0, 1) * 255).astype(np.uint8)).save(a)
        r = subprocess.run(["npx", "hyperframes", "remove-background", str(a), "-o", str(b), "--device", "cpu"], capture_output=True, text=True, cwd=tmpdir)
        out.append(np.asarray(Image.open(b).convert("RGBA"), np.float32)[..., 3] / 255 if r.returncode == 0 and b.exists() else None)
    return out
