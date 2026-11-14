"""Cover v10c (reel-local, 2026-11-12). Director: "C2 is good, can we find a few other stock" -> stock board D (Pexels) ->
"Only try D5": Pexels 19467413 by Aswin (Pexels licence, raw/stock/pexels-19467413/), a young man holding a sparkler in the dark.

Same build as C2 (tools/cover_v10b.py): a 9:16 slice of the full photo (2250 x 4000 from x0 = CX0 -> 1080 x 1920, no
upscaling), the photo's own colour, cover_v10's finish (glow on the sparkler, never on the face), and the type the director
picked ("I like the white and yellow combination"): cream Didot caps + gold Didot italic + rule + sub-line.
The photo is 3000 wide and the man + sparkler span about 2330 px, so the slice trims the sparkler's longest left spikes and the
edge of his right sleeve (x0 400 keeps more of the sparkler; the sleeve matters less). His hair starts at y ~608 in the cover, so the title block sits higher and at 1.0x (C2 used 1.12x).
Usage (reel folder): ../../.venv/bin/python tools/cover_v10c.py
"""
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageOps

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cover_v10 as cv  # noqa: E402
import cover_v10b as cb  # noqa: E402

PHOTO = "raw/stock/pexels-19467413/pexels-photo-19467413.jpeg"
CX0 = 400
FACE = (640, 776)
TOP, SCALE = 262, 1.0
OUT = cv.OUT


def main():
    im = ImageOps.exif_transpose(Image.open(PHOTO)).convert("RGB")
    w, h = im.size
    cw = round(h * 9 / 16)
    if CX0 + cw > w:
        raise SystemExit(f"crop {CX0}+{cw} wider than {w}")
    pic = np.asarray(im.crop((CX0, 0, CX0 + cw, h)).resize((cv.W, cv.H), Image.LANCZOS), np.float32) / 255
    cv.KEY = 0.0
    pic = cv.finish(pic, FACE)
    base = Image.fromarray((pic * 255 + 0.5).astype(np.uint8))
    y = cv.luma(pic)
    print(f"photo {w}x{h}, slice {cw}x{h} from x {CX0}; mean luma {y.mean():.3f}, title area {y[TOP - 20:TOP + 280].mean():.3f}")
    d5 = cb.type_didot(base, TOP, SCALE)
    d5.save(OUT / "cover_D5.jpg", quality=94)
    c2 = Image.open(OUT / "cover_C2.jpg").convert("RGB")
    show = {"D5": ("D5  sparkler · Didot (white + gold)", d5), "C2": ("C2  cracker man · Didot (now in deliver/)", c2)}
    t = Image.new("RGB", (2 * 548, 980 + 270), (18, 18, 18)); d = ImageDraw.Draw(t)
    for i, (k, (lab, img)) in enumerate(show.items()):
        t.paste(img.resize((540, 960)), (i * 548 + 4, 24)); d.text((i * 548 + 8, 6), lab, fill=(255, 220, 0))
        t.paste(img.crop((0, 240, cv.W, 1680)).resize((180, 240)), (i * 548 + 4, 1000))
        d.text((i * 548 + 190, 1004), "grid tile 3:4", fill=(200, 200, 200))
    t.save(OUT / "cover_options_D5.jpg", quality=90)
    prior = ["../we-never-treated-her-like-a-goddess/deliver/cover.jpg", "../uski-aankhein/deliver/cover.jpg",
             "../pujo-ki-asolei-sobar/deliver/cover.jpg", "../kolkata/deliver/kolkata_v8_cover.jpg",
             "../puja-night-2/renders/stills/cover/cover_A_C139_46.80.png"]
    tile = lambda x: x.convert("RGB").resize((cv.W, cv.H)).crop((0, 240, cv.W, 1680)).resize((300, 400))
    pt = [tile(Image.open(p)) for p in prior]
    f = Image.new("RGB", (2 * (3 * 302 + 40), 2 * 402 + 30), (255, 255, 255)); d = ImageDraw.Draw(f)
    for i, (k, (lab, img)) in enumerate(show.items()):
        ox = i * (3 * 302 + 40); d.text((ox + 4, 6), k + " in the grid", fill=(0, 0, 0))
        for j, tl in enumerate([tile(img)] + pt):
            f.paste(tl, (ox + (j % 3) * 302, 26 + (j // 3) * 402))
    f.save(OUT / "feed_mock_D5.jpg", quality=88)
    print("cover_D5.jpg, cover_options_D5.jpg, feed_mock_D5.jpg")


if __name__ == "__main__":
    main()
