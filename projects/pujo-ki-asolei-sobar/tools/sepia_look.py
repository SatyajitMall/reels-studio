#!/usr/bin/env python3
"""One sepia film look for every shot, after a per-shot neutral match.

normalise(): removes each shot's own lighting cast (blue street light, green tube light, orange sodium)
             with a robust grey-world on the midtones + an exposure match, so every shot enters the look
             from the same neutral, equally exposed starting point.  Constant per shot (no flicker).
look():      pixelwise (exported as the .cube): filmic S with faded blacks and rolled highlights,
             sepia toning by luminance (dark brown shadows -> amber mids -> warm cream highlights),
             keeping KEEP of the original colour so skin and marigolds still breathe.
Usage: sepia_look.py cube <out.cube> [--keep 0.22]
"""
import sys
import numpy as np

KEEP = 0.22                                     # share of the original (neutralised) colour kept
# sepia ramp: luminance -> tone colour
RX = np.array([0.00, 0.12, 0.35, 0.60, 0.85, 1.00])
RC = np.array([[0.035, 0.022, 0.012],          # deep brown-black (faded, not pure black)
               [0.150, 0.098, 0.060],
               [0.420, 0.300, 0.190],          # warm brown mids
               [0.700, 0.545, 0.380],          # amber
               [0.930, 0.820, 0.640],          # warm cream
               [0.985, 0.935, 0.820]])
TX = np.array([0.0, 0.05, 0.15, 0.30, 0.50, 0.70, 0.88, 1.0])     # filmic tone curve (input luma -> output luma)
TY = np.array([0.03, 0.045, 0.095, 0.218, 0.425, 0.655, 0.835, 0.92])   # faded film floor 0.03 at black (gate loop 2)

def luma(x): return x @ np.array([0.2126, 0.7152, 0.0722])

def normalise(x, gains=None, target=0.36):
    """x float [0,1]. gains: precomputed per-shot (r,g,b,k) or None to measure this frame."""
    if gains is None: gains = measure(x, target)
    r, g, b, k = gains
    x = x * np.array([r, g, b]) * k
    # highlight shoulder: keeps fabric and skin detail in whites the exposure match would clip (v1c review: C228, C201)
    kn = 0.72
    return np.where(x > kn, kn + (1 - kn) * (1 - np.exp(-(x - kn) / (1 - kn))), x).clip(0, 1)

def measure(x, target=0.36, strength=0.9):
    y = luma(x); m = (y > 0.10) & (y < 0.85)
    if m.sum() < 500: m = y > 0.02
    R, G, B = (np.median(x[..., i][m]) for i in range(3))
    gr, gb = (G / max(R, 1e-4)) ** strength, (G / max(B, 1e-4)) ** strength
    xn = x * np.array([gr, 1.0, gb])
    k = (target / max(float(np.mean(luma(np.clip(xn, 0, 1)))), 1e-3)) ** 0.85
    return (gr, 1.0, gb, min(k, 2.4))

def look(x, keep=KEEP):
    y = np.clip(luma(x), 1e-5, 1)
    y2 = np.interp(y, TX, TY)
    tone = np.stack([np.interp(y2, RX, RC[:, c]) for c in range(3)], -1)
    col = x * (y2 / y)[..., None]                       # original colour at the new luminance
    ycol = luma(col)[..., None]
    col = ycol + (col - ycol) * 0.8
    out = tone * (1 - keep) + col * keep
    # keep luminance on the curve after the blend
    out = out * (y2 / np.maximum(luma(out), 1e-5))[..., None]
    return np.clip(out, 0, 1)

if __name__ == "__main__" and sys.argv[1] == "cube":
    keep = float(sys.argv[sys.argv.index("--keep") + 1]) if "--keep" in sys.argv else KEEP
    N = 33; v = np.linspace(0, 1, N); b, g, r = np.meshgrid(v, v, v, indexing="ij")
    out = look(np.stack([r, g, b], -1).reshape(-1, 3), keep)
    with open(sys.argv[2], "w") as f:
        f.write(f'TITLE "pujo-ki-asolei-sobar sepia film look (keep {keep})"\nLUT_3D_SIZE 33\nDOMAIN_MIN 0.0 0.0 0.0\nDOMAIN_MAX 1.0 1.0 1.0\n')
        for p in out: f.write(f"{p[0]:.6f} {p[1]:.6f} {p[2]:.6f}\n")
    print("wrote", sys.argv[2])
