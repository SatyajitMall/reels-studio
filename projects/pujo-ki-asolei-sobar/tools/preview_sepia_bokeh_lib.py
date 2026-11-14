"""optical(): halation + vignette + grain, shared by the preview and the shot renderer."""
import numpy as np
from PIL import Image
from scipy import ndimage
import sepia_look as sl

def optical(x, seed=0, hal=0.22, hal_t=0.80, vig=0.28, floor=0.03, grain=0.022):
    H, W = x.shape[:2]; y = sl.luma(x)
    hi = np.clip((y - hal_t) / (1 - hal_t), 0, 1)[..., None] * x
    bloom = np.stack([ndimage.gaussian_filter(hi[..., c], 26) for c in range(3)], -1) * np.array([1.0, 0.62, 0.34])
    x = 1 - (1 - x) * (1 - hal * bloom)
    yy, xx = np.mgrid[0:H, 0:W]; d = np.sqrt(((xx - W / 2) / (W / 2)) ** 2 + ((yy - H * 0.46) / (H / 2)) ** 2)
    x = floor + (x - floor) * (1 - vig * np.clip((d - 0.45) / 0.85, 0, 1) ** 1.5)[..., None]   # never below the film floor
    g = np.random.default_rng(seed).normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = np.asarray(Image.fromarray(g).resize((W, H), Image.BICUBIC))
    x = x + g[..., None] * grain * (1 - np.abs(sl.luma(x) - 0.5)[..., None] * 1.2)
    return np.clip(x, 0, 1)
