"""Cover v10b (reel-local, 2026-11-12). Director on the B1 cover (C064 car washer): "does not look festive enough", then
"can we use a free stock image of a man looking at crackers as a cover?"

The reel already holds one: Pexels photo 5882889 (Pragyan Bezbaruah, Pexels licence, raw/stock/pexels-5882889/), the man
crouching to light a cracker at night. It is the source of the reel's last shot (19, AI-animated in the reel). The cover
uses the PHOTO itself, not the AI frames, so the cover has no generated pixels.

Picture: a 9:16 slice of the full photo (2361 x 4198 from x0 = CX0, downscaled to 1080 x 1920, no upscaling). The man and the
flame sit in the lower 60 %; the dark wall above takes the title in the upper third, inside the 3:4 grid crop (y 240-1680),
as on every earlier cover. The photo keeps its own colour (it is the reel's anchor for shot 19); the finish is cover_v10's
(S-curve, split tone, glow on the lights only with the face protected, vignette, grain), so it sits with A/B in the feed.
Type: the feed's two families from cover_v10 (C1 DIN Condensed cream caps, C2 Didot caps + gold italic).
Usage (reel folder): ../../.venv/bin/python tools/cover_v10b.py
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cover_v10 as cv  # noqa: E402

PHOTO = "raw/stock/pexels-5882889/pexels-photo-5882889.jpeg"
CX0 = 100                         # crop x0 in the photo (2564 wide); the slice is 2361 wide = 4198 * 9 / 16
FACE = (642, 864)                 # the man's face in the cover (for the glow guard and the vignette centre)
TOP_DIN, TOP_DIDOT = 300, 290
DIDOT_SCALE = 1.12                # the dark top has room: the Didot type a touch larger than cover_v10 (grid-tile legibility)
STREAK = (430, 500, 570, 890)     # x0, x1, y0, y1 (cover px): a cyan light streak on the wall, right under the sub-line
OUT = cv.OUT


def remove_streak(pic):
    """Paint out the cyan streak: each row inside the box is replaced by a linear blend of the wall either side of it,
    only where the picture is brighter than that plate, with a feathered box. The wall is dark (luma ~0.02), so the
    plate is clean; nothing of the man or the flame is in the box."""
    x0, x1, y0, y1 = STREAK
    out = pic.copy()
    left = pic[y0:y1, x0 - 8:x0].mean(1); right = pic[y0:y1, x1:x1 + 8].mean(1)
    t = np.linspace(0, 1, x1 - x0, dtype=np.float32)[None, :, None]
    plate = left[:, None, :] * (1 - t) + right[:, None, :] * t
    reg = pic[y0:y1, x0:x1]
    wgt = np.clip((cv.luma(reg) - cv.luma(plate) - 0.004) / 0.02, 0, 1)
    from scipy import ndimage
    wgt = ndimage.gaussian_filter(ndimage.maximum_filter(wgt, 5), 2.5)
    fx = np.clip(np.minimum(np.arange(x1 - x0), np.arange(x1 - x0)[::-1]) / 10, 0, 1)
    fy = np.clip(np.minimum(np.arange(y1 - y0), np.arange(y1 - y0)[::-1]) / 20, 0, 1)
    wgt = np.clip(wgt, 0, 1) * fy[:, None] * fx[None, :]
    out[y0:y1, x0:x1] = reg * (1 - wgt[..., None]) + plate * wgt[..., None]
    return out


def type_didot(img, top, s):
    """cover_v10.type_didot (Goddess: tracked Didot caps, gold italic, a thin rule, a tracked credit line), scaled by s."""
    from PIL import ImageFont
    caps = ImageFont.truetype(cv.DIDOT, round(50 * s), index=0); ital = ImageFont.truetype(cv.DIDOT, round(92 * s), index=1)
    small = ImageFont.truetype(cv.DIDOT, round(30 * s), index=0)
    if ital.getlength("ghar nahi aa paaunga") > cv.W - 80:
        raise SystemExit("italic line too wide")
    m1 = Image.new("L", (cv.W, cv.H), 0); m2 = Image.new("L", (cv.W, cv.H), 0)
    cv.put(m1, caps, "MAA, IS BAAR", top, 9 * s)
    cv.put(m2, ital, "ghar nahi aa paaunga", top + 62 * s, 0)
    ImageDraw.Draw(m1).line([(cv.W / 2 - 60 * s, top + 206 * s), (cv.W / 2 + 60 * s, top + 206 * s)], fill=255, width=2)
    cv.put(m1, small, cv.SUB, top + 228 * s, 6 * s)
    return cv.composite(img, [(m1, cv.CREAM), (m2, cv.GOLD)])


def main():
    im = ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB")
    w, h = im.size
    cw = round(h * 9 / 16)
    if CX0 + cw > w:
        raise SystemExit(f"crop {CX0}+{cw} wider than {w}")
    sl = im.crop((CX0, 0, CX0 + cw, h)).resize((cv.W, cv.H), Image.LANCZOS)
    pic = remove_streak(np.asarray(sl, np.float32) / 255)
    cv.KEY = 0.0
    pic = cv.finish(pic, FACE)
    base = Image.fromarray((pic * 255 + 0.5).astype(np.uint8))
    y = cv.luma(pic)
    print(f"photo {w}x{h}, slice {cw}x{h} from x {CX0}; mean luma {y.mean():.3f}, title area {y[TOP_DIN - 30:TOP_DIN + 320].mean():.3f}")
    made = {"C1": cv.type_din(base, TOP_DIN), "C2": type_didot(base, TOP_DIDOT, DIDOT_SCALE)}
    for k, m in made.items():
        m.save(OUT / f"cover_{k}.jpg", quality=94)
    # sheet: C1, C2 and the earlier B1 for comparison, full and as the 3:4 grid tile
    show = {"C1": "C1  cracker man · DIN caps (Pujo/Uski)", "C2": "C2  cracker man · Didot (Goddess)",
            "B1": "B1  car washer (now in deliver/)"}
    imgs = {"C1": made["C1"], "C2": made["C2"], "B1": Image.open(OUT / "cover_B1.jpg").convert("RGB")}
    t = Image.new("RGB", (3 * 548, 980 + 270), (18, 18, 18)); d = ImageDraw.Draw(t)
    for i, k in enumerate(show):
        t.paste(imgs[k].resize((540, 960)), (i * 548 + 4, 24)); d.text((i * 548 + 8, 6), show[k], fill=(255, 220, 0))
        t.paste(imgs[k].crop((0, 240, cv.W, 1680)).resize((180, 240)), (i * 548 + 4, 1000))
        d.text((i * 548 + 190, 1004), "grid tile 3:4", fill=(200, 200, 200))
    t.save(OUT / "cover_options_C.jpg", quality=90)
    # feed mock: each C option beside the earlier covers as 3:4 tiles, newest first
    prior = ["../we-never-treated-her-like-a-goddess/deliver/cover.jpg", "../uski-aankhein/deliver/cover.jpg",
             "../pujo-ki-asolei-sobar/deliver/cover.jpg", "../kolkata/deliver/kolkata_v8_cover.jpg",
             "../puja-night-2/renders/stills/cover/cover_A_C139_46.80.png"]
    tile = lambda x: x.convert("RGB").resize((cv.W, cv.H)).crop((0, 240, cv.W, 1680)).resize((300, 400))
    pt = [tile(Image.open(p)) for p in prior]
    f = Image.new("RGB", (2 * (3 * 302 + 40), 2 * 402 + 30), (255, 255, 255)); d = ImageDraw.Draw(f)
    for i, k in enumerate(("C1", "C2")):
        ox = i * (3 * 302 + 40); d.text((ox + 4, 6), k + " in the grid", fill=(0, 0, 0))
        for j, tl in enumerate([tile(made[k])] + pt):
            f.paste(tl, (ox + (j % 3) * 302, 26 + (j // 3) * 402))
    f.save(OUT / "feed_mock_C.jpg", quality=88)
    print("cover_C1.jpg, cover_C2.jpg, cover_options_C.jpg, feed_mock_C.jpg")


if __name__ == "__main__":
    main()
