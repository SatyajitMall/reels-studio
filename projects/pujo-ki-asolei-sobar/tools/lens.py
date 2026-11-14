"""Synthetic shallow depth of field for iPhone footage: monocular depth -> layered disc (lens) blur with bokeh.

depth():  Depth-Anything-V2-Small (ONNX, CPU), relative inverse depth (bright = near), 518x924 input.
bokeh():  per-pixel circle of confusion from distance to the focus plane; far side up to max_r px,
          near side gentler; layered far-to-near disc blur (so blurred background never bleeds over the
          sharp subject); highlights boosted in linear light before blurring so lights turn into bokeh discs.
Blur is computed at half resolution for the big radii (bokeh is soft anyway), then upsampled.
"""
import sys
from pathlib import Path
import numpy as np
from PIL import Image
from scipy import ndimage, signal

REEL = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REEL / "renders" / "_pylib"))
import onnxruntime as ort  # noqa: E402

_sess = None
def _session():
    global _sess
    if _sess is None:
        so = ort.SessionOptions(); so.log_severity_level = 3; so.intra_op_num_threads = 3   # parallel shot renders don't fight
        _sess = ort.InferenceSession(str(REEL / "renders/models/depth_anything_v2_small/model.onnx"), so, providers=["CPUExecutionProvider"])
    return _sess

def depth(rgb):
    """rgb float [0,1] HxWx3 -> inverse depth HxW (unnormalised, bright = near)."""
    H, W = rgb.shape[:2]
    x = np.asarray(Image.fromarray((rgb * 255).astype(np.uint8)).resize((518, 924), Image.BICUBIC), np.float32) / 255
    x = ((x - [0.485, 0.456, 0.406]) / [0.229, 0.224, 0.225]).transpose(2, 0, 1)[None].astype(np.float32)
    d = _session().run(None, {"pixel_values": x})[0][0]
    return np.asarray(Image.fromarray(d.astype(np.float32)).resize((W, H), Image.BILINEAR))

def _disc(r):
    r = max(r, 0.5); n = int(np.ceil(r)); y, x = np.mgrid[-n:n + 1, -n:n + 1]
    k = np.clip(r + 0.5 - np.sqrt(x * x + y * y), 0, 1)        # anti-aliased disc
    return k / k.sum()

def _blur(img, r):
    if r < 0.75: return img
    k = _disc(r)
    if img.ndim == 2: return signal.fftconvolve(img, k, mode="same")
    return np.stack([signal.fftconvolve(img[..., c], k, mode="same") for c in range(img.shape[2])], -1)

LEVELS = [0, 1.5, 3, 5, 8, 12, 17, 23]

def coc_map(d, focus, far_ref, max_r=20.0, near_r=6.0, near_ref=None, tol=0.06):
    """d: inverse depth (normalised 0..1, 1 = nearest). focus: d at the subject. far_ref: d treated as 'infinity'."""
    span_far = max(focus - far_ref, 0.30)        # min span: near-flat scenes (a pandal backdrop) get proportionally little blur
    far = np.clip((focus - d - tol * span_far) / (span_far * (1 - tol)), 0, 1) ** 0.85 * max_r
    near_ref = 1.0 if near_ref is None else near_ref
    span_near = max(near_ref - focus, 0.30)
    near = np.clip((d - focus - tol * span_near * 2) / span_near, 0, 1) ** 1.2 * near_r
    return np.maximum(far, near), (d > focus)

def bokeh(rgb, d, focus, far_ref, max_r=20.0, near_r=6.0, hi_boost=2.5, protect=None):
    """protect: optional soft person matte (0..1); protected pixels get no blur (faces, hands stay sharp)."""
    H, W = rgb.shape[:2]
    coc, is_near = coc_map(d, focus, far_ref, max_r, near_r)
    if protect is not None: coc = coc * (1 - np.clip(protect, 0, 1))
    lin = rgb ** 2.2
    y = lin @ np.array([0.2126, 0.7152, 0.0722])
    boost = 1 + hi_boost * np.clip((y - 0.55) / 0.45, 0, 1) ** 2       # lights -> bokeh discs
    src = lin * boost[..., None]
    half = lambda a: np.asarray(Image.fromarray(a.astype(np.float32)).resize((W // 2, H // 2), Image.BILINEAR)) if a.ndim == 2 else \
        np.stack([half(a[..., c]) for c in range(a.shape[2])], -1)
    full = lambda a: np.asarray(Image.fromarray(a.astype(np.float32)).resize((W, H), Image.BILINEAR)) if a.ndim == 2 else \
        np.stack([full(a[..., c]) for c in range(a.shape[2])], -1)
    # soft level weights
    w = []
    for i, r in enumerate(LEVELS):
        lo = LEVELS[i - 1] if i else -1e9; hi = LEVELS[i + 1] if i + 1 < len(LEVELS) else 1e9
        wi = np.where(coc <= r, np.clip((coc - lo) / max(r - lo, 1e-6), 0, 1), np.clip((hi - coc) / max(hi - r, 1e-6), 0, 1))
        w.append(wi)
    # background fill: whole frame at the largest far radius (fills holes behind the subject)
    # background fill = normalised convolution of OUT-OF-FOCUS pixels only, so the sharp subject never
    # glows into the blurred background (v1c review: halos on C216, C201, C032)
    bgm = np.clip((coc - 2.0) / 4.0, 0, 1) * (~is_near)
    if bgm.max() < 1e-3: bgm = np.ones_like(coc)
    num = full(_blur(half(src * bgm[..., None]), LEVELS[-1] / 2)); den = full(_blur(half(bgm), LEVELS[-1] / 2))
    out = num / np.maximum(den, 1e-3)[..., None]
    order = sorted(range(len(LEVELS)), key=lambda i: -LEVELS[i])        # far (big blur) first ...
    far_idx = [i for i in order]; near_layers = []
    for i in far_idx:
        r = LEVELS[i]
        m_far = w[i] * (~is_near); m_near = w[i] * is_near
        for m, store in ((m_far, None), (m_near, near_layers)):
            if m.max() < 1e-3: continue
            if r >= 3:
                pm = full(_blur(half(src * m[..., None]), r / 2)); a = full(_blur(half(m), r / 2))
            else:
                pm = _blur(src * m[..., None], r); a = _blur(m, r) if r >= 0.75 else m
            if store is None: out = out * (1 - np.clip(a, 0, 1))[..., None] + pm
            else: store.append((r, pm, a))
    for r, pm, a in sorted(near_layers, key=lambda t: t[0]):        # near layers last, smallest blur first
        out = out * (1 - np.clip(a, 0, 1))[..., None] + pm
    out = out / (1 + np.maximum(out - 1, 0))                          # soft clip boosted lights
    return np.clip(out, 0, 1) ** (1 / 2.2), coc

def focus_value(d, fx, fy, win=0.06):
    H, W = d.shape; x0, x1 = int((fx - win) * W), int((fx + win) * W); y0, y1 = int((fy - win * 0.56) * H), int((fy + win * 0.56) * H)
    return float(np.percentile(d[max(y0, 0):y1, max(x0, 0):x1], 60))
