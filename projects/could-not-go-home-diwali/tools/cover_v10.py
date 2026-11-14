"""Cover v10 (reel-local, 2026-11-12). Director on the v4f/v6 cover (C051 paan maker, Avenir subtitle line mid-frame):
"No please use a better picture and typography and font style which will fit in my Instagram feed based on the previous post."

The feed (the five earlier covers, analysis/cover_v10/prior_covers.jpg) has one pattern:
  - a full-bleed, cinematic night frame of one person or one idol, the subject in the lower two thirds;
  - the TITLE in the upper third (inside the 3:4 grid crop, y 240-1680), over a dark part of the picture;
  - two type families: DIN Condensed Bold cream caps + a small tracked sub-line (Pujo, Uski),
    or Didot tracked caps + Didot italic + a thin rule + a small tracked credit line (Goddess; Kolkata is a serif too).

Pictures (camera bakes are landscape 3840x2160; a 9:16 slice of 1215 x 2160 goes to 1080 x 1920 with no upscaling):
  A  C048 frame 46: the auto driver turning into profile, glasses catching the lit market (the reel's hook, 0:02).
     Title over the dark canopy.
  B  C064 frame 46: the car washer looking straight into the lens (0:27, "Agle saal, pakka.").
     His face is in the top fifth of the frame, so the title goes low (as Kolkata's), over a darkened lower third.
Grade: each camera frame is quantile-matched to the reel's own render of that shot (v8b master, 16:9 window), so the cover
carries the reel's grade, then a light cinematic finish as on Pujo's A1: S-curve, a warm/teal split, glow on the lights
(never on skin), a vignette and fine grain.
Usage (reel folder): ../../.venv/bin/python tools/cover_v10.py
"""
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

OUT = Path("analysis/cover_v10")
MASTER = "renders/masters/could-not-go-home-diwali_v8b_master.mov"
WIN = (0, 606, 1080, 608)                                      # x, y, w, h of the 16:9 window in the reel
W, H = 1080, 1920
DIN = "../pujo-ki-asolei-sobar/graphics/title/assets/fonts/DINCondensed-Bold.ttf"
DIDOT = "/System/Library/Fonts/Supplemental/Didot.ttc"
CREAM, GOLD, HALO = (245, 230, 200), (233, 196, 106), (26, 15, 5)
# key, bake, frame, crop x0 (of 3840), reel times of the shot (for the grade match), face centre in the cover (x, y)
PICS = {
    "A": ("raw/baked/C048_f2_01.92.mov", 46, 1060, (1.9, 2.4, 2.9), (600, 940)),
    "B": ("raw/baked/C064_f2_06.24.mov", 46, 980, (27.3, 27.8, 28.2), (540, 400)),
}
SUB = "DIWALI  ·  BENGALURU  ·  2026"
luma = lambda x: x @ np.array([0.2126, 0.7152, 0.0722], np.float32)


def camera(path, n):
    b = subprocess.run(["ffmpeg", "-v", "error", "-noautorotate", "-i", path, "-vf", f"select=eq(n\\,{n})", "-frames:v", "1",
                        "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
    return np.frombuffer(b, "<u2").reshape(2160, 3840, 3).astype(np.float32) / 65535


def reel(ts):
    x, y, w, h = WIN
    fr = []
    for t in ts:
        b = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(t), "-i", MASTER, "-frames:v", "1", "-vf", f"crop={w}:{h}:{x}:{y}",
                            "-f", "rawvideo", "-pix_fmt", "rgb48le", "-"], capture_output=True).stdout
        fr.append(np.frombuffer(b, "<u2").reshape(h, w, 3).astype(np.float32) / 65535)
    return np.concatenate(fr, 0)


def match(src, sample, ref, knots=24):
    """Smooth per-channel quantile curve sample -> ref, applied to src (as tools/make_cover_v4f.py)."""
    q = np.linspace(0.005, 0.995, knots); out = np.empty_like(src)
    for c in range(3):
        sq = np.maximum.accumulate(np.quantile(sample[..., c], q) + np.arange(knots) * 1e-6)
        out[..., c] = np.interp(src[..., c], sq, np.quantile(ref[..., c], q))
    return np.clip(out, 0, 1)


KEY = 0.0


def finish(x, face):
    hh, ww = x.shape[:2]; yy, xx = np.mgrid[0:hh, 0:ww].astype(np.float32); fx, fy = face
    y = luma(x); p = 0.38                                        # S-curve on luma, hue kept
    yc = np.where(y < p, p * (y / p) ** 1.10, 1 - (1 - p) * ((1 - y) / (1 - p)) ** 1.08)
    yc = np.where(yc > 0.86, 0.86 + 0.14 * np.tanh((yc - 0.86) / 0.14), yc)
    x = x * (yc / np.maximum(y, 1e-4))[..., None]
    y = luma(x); sh = np.clip(1 - y / 0.45, 0, 1) ** 1.5; hi = np.clip((y - 0.55) / 0.45, 0, 1) ** 1.5
    x = x + sh[..., None] * np.array([-0.012, 0.002, 0.016], np.float32) + hi[..., None] * np.array([0.016, 0.004, -0.016], np.float32)
    face_m = np.exp(-(((xx - fx) / 260) ** 2 + ((yy - fy) / 320) ** 2))
    x = x * (1 + face_m * (2 ** KEY - 1))[..., None]             # soft key on the face
    lin = np.clip(x, 0, 1) ** 2.2; yl = luma(lin)                # glow on the lights only, never on the face
    src = (np.clip((yl - 0.55) / 0.45, 0, 1) * (1 - face_m))[..., None] * lin
    glow = ndimage.gaussian_filter(src, (16, 16, 0)) * 0.5 + ndimage.gaussian_filter(src, (55, 55, 0)) * 0.3
    lin = lin + glow * np.array([1.0, 0.74, 0.48], np.float32)
    x = np.clip(lin, 0, None) ** (1 / 2.2); x = x / (1 + np.maximum(x - 1, 0))
    r = np.sqrt(((xx - fx) / 760) ** 2 + ((yy - fy) / 1150) ** 2)
    x = x * (2 ** (-0.45 * np.clip((r - 0.45) / 0.65, 0, 1) ** 1.5))[..., None]
    rng = np.random.default_rng(10); g = ndimage.gaussian_filter(rng.normal(0, 1, (hh, ww)).astype(np.float32), 0.7)
    g = g / g.std() * 0.010; y = luma(x)
    return np.clip(x + (g * (4 * y * (1 - y)) ** 0.8)[..., None], 0, 1)


def shade_bottom(x, y0, y1, a):
    """Darken the title area: 0 above y0, rising to a at y1 and below."""
    yy = np.arange(x.shape[0], dtype=np.float32)[:, None]
    k = np.clip((yy - y0) / (y1 - y0), 0, 1) ** 1.3 * a
    return x * (1 - k)[..., None]


def tracked_w(font, text, tr):
    return sum(font.getlength(c) for c in text) + tr * (len(text) - 1)


def put(mask, font, text, y, tr):
    d = ImageDraw.Draw(mask); x = (W - tracked_w(font, text, tr)) / 2
    for c in text:
        d.text((x, y), c, font=font, fill=255); x += font.getlength(c) + tr


def composite(img, layers):
    """layers: (mask L, colour). Each gets a dark warm halo (as Pujo/Uski) then the fill."""
    im = img.convert("RGBA")
    for m, col in layers:
        halo = m.filter(ImageFilter.GaussianBlur(12)).point(lambda v: int(v * 0.75))
        im.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), c) for c in HALO], halo)))
        im.alpha_composite(Image.merge("RGBA", (*[Image.new("L", (W, H), c) for c in col], m)))
    return im.convert("RGB")


def type_din(img, top):
    """Pujo / Uski: DIN Condensed Bold caps, cream, 0.08 em tracking; sub-line 0.3 em tracking."""
    size = 118; f = ImageFont.truetype(DIN, size); m = Image.new("L", (W, H), 0)
    y = top
    for ln in ("MAA, IS BAAR GHAR", "NAHI AA PAAUNGA"):
        put(m, f, ln, y - f.getbbox("H")[1], 0.08 * size); y += 1.06 * size
    fs = ImageFont.truetype(DIN, 38); put(m, fs, SUB, y + 0.22 * size - fs.getbbox("H")[1], 0.3 * 38)
    return composite(img, [(m, CREAM)])


def type_didot(img, top):
    """Goddess: tracked Didot caps, a large Didot italic line in gold, a thin rule, a small tracked credit line."""
    caps = ImageFont.truetype(DIDOT, 50, index=0); ital = ImageFont.truetype(DIDOT, 92, index=1)
    small = ImageFont.truetype(DIDOT, 30, index=0)
    m1 = Image.new("L", (W, H), 0); m2 = Image.new("L", (W, H), 0)
    put(m1, caps, "MAA, IS BAAR", top, 9)
    put(m2, ital, "ghar nahi aa paaunga", top + 62, 0)
    ImageDraw.Draw(m1).line([(W / 2 - 60, top + 206), (W / 2 + 60, top + 206)], fill=255, width=2)
    put(m1, small, SUB, top + 228, 6)
    return composite(img, [(m1, CREAM), (m2, GOLD)])


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    made = {}
    for k, (path, n, x0, ts, face) in PICS.items():
        cam = camera(path, n)
        g = match(cam, cam[::4, ::4], reel(ts)[::2, ::2])         # whole landscape frame vs the reel's window render
        sl = g[:, x0:x0 + 1215]
        pic = np.asarray(Image.fromarray((sl * 255 + 0.5).astype(np.uint8)).resize((W, H), Image.LANCZOS), np.float32) / 255
        global KEY
        KEY = 0.45 if k == "A" else 0.1                          # the driver's profile sits in shadow
        pic = finish(pic, face)
        if k == "B":
            pic = shade_bottom(pic, 1050, 1500, 0.7)             # the white scooter under the title
        base = Image.fromarray((pic * 255 + 0.5).astype(np.uint8))
        top = 330 if k == "A" else 1330
        made[k + "1"] = type_din(base, top)
        made[k + "2"] = type_didot(base, top - 10)
        print(k, "frame", n, "x0", x0, "mean luma %.3f" % luma(pic).mean(), "title-area luma %.3f" % luma(pic[top - 30:top + 320]).mean())
    for k, im in made.items():
        im.save(OUT / f"cover_{k}.jpg", quality=94)
    # sheet: the four options, full and as the 3:4 grid tile
    t = Image.new("RGB", (4 * 548, 980 + 270), (18, 18, 18)); d = ImageDraw.Draw(t)
    names = {"A1": "A1  driver · DIN caps (Pujo/Uski)", "A2": "A2  driver · Didot (Goddess)",
             "B1": "B1  car washer · DIN caps", "B2": "B2  car washer · Didot"}
    for i, k in enumerate(names):
        t.paste(made[k].resize((540, 960)), (i * 548 + 4, 24)); d.text((i * 548 + 8, 6), names[k], fill=(255, 220, 0))
        t.paste(made[k].crop((0, 240, W, 1680)).resize((180, 240)), (i * 548 + 4, 1000)); d.text((i * 548 + 190, 1004), "grid tile 3:4", fill=(200, 200, 200))
    t.save(OUT / "cover_options.jpg", quality=90)
    # feed mock: each option beside the earlier covers as 3:4 tiles, newest first
    prior = ["../we-never-treated-her-like-a-goddess/deliver/cover.jpg", "../uski-aankhein/deliver/cover.jpg",
             "../pujo-ki-asolei-sobar/deliver/cover.jpg", "../kolkata/deliver/kolkata_v8_cover.jpg",
             "../puja-night-2/renders/stills/cover/cover_A_C139_46.80.png"]
    tile = lambda im: im.convert("RGB").resize((W, H)).crop((0, 240, W, 1680)).resize((300, 400))
    pt = [tile(Image.open(p)) for p in prior]
    f = Image.new("RGB", (4 * (3 * 302 + 40), 2 * 402 + 30), (255, 255, 255)); d = ImageDraw.Draw(f)
    for i, k in enumerate(names):
        ox = i * (3 * 302 + 40); d.text((ox + 4, 6), k + " in the grid", fill=(0, 0, 0))
        tiles = [tile(made[k])] + pt
        for j, tl in enumerate(tiles[:6]):
            f.paste(tl, (ox + (j % 3) * 302, 26 + (j // 3) * 402))
    f.save(OUT / "feed_mock.jpg", quality=88)
    print("cover_options.jpg, feed_mock.jpg")


if __name__ == "__main__":
    main()
