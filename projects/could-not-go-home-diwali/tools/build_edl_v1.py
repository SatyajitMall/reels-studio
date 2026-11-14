"""Build EDL v1 for could-not-go-home-diwali (reel-local).

- Bakes Apple Cinematic depth (f/2, as shot) on each used camera clip's range with ±0.48 s handles → raw/baked/
  (tools/cine_bake; frame-aligned starts, so baked t=0 is camera frame start/0.04 exactly).
- Renders V5 overlays: the 4:3 window matte, the six letter lines (Baskerville Italic, cream) and the end card
  (Rozha One title, sign-off, handle).
- Writes analysis/edl_v1.json (scripts/preview_edl.py format) and analysis/bake_map.json.

Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v1.py
"""
import json
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter, ImageFont

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
R = "projects/could-not-go-home-diwali"
FPS = 25
W, H = 1080, 1920
WIN_Y0, WIN_Y1 = 505, 1315          # 4:3 window: 1080×810 centred on the safe-area centre (910)
BASE_SCALE, POS = 37.5, [540, 910]  # 3840×2160 upright → 1440×810: the middle 2880 px (75 %) fill the window
CREAM = (245, 230, 200)
SUP = Path("/System/Library/Fonts/Supplemental")
FONTS = STUDIO / "assets" / "fonts"

# bar downbeats of the guide (analysis/beats.json), snapped to frames
CUTS = [0.0, 1.56, 3.12, 4.68, 6.24, 7.84, 9.44, 11.04, 12.64, 14.24, 15.80, 17.40, 19.00]
RUNTIME = 20.80

LINES = [
    ("Maa, is baar ghar nahi aa paaunga.", "Maa, I can't come home this time."),
    ("Yahan Diwali pe sabse zyada kaam hai.", "Diwali is our busiest night here."),
    ("Tumhare haath ka khaana yaad aata hai.", "I miss food made by your hands."),
    ("Phone pe aarti dikha dena.", "Show me the aarti on the phone."),
    ("Papa se kehna, main theek hoon.", "Tell Papa I'm fine."),
    ("Agle saal, pakka.", "Next year. Promise."),
]

# (name, camera clip id, camera in, framing, shows); framing: "push" = 37.5→39.5 on a hold, "base", or (scale, x, y)
SHOTS = [
    ("01_C047_auto", "C047", 0.60, "push", "auto driver from the back seat; Diwali-lit street through the windscreen"),
    ("02_C048_auto_turn", "C048", 2.40, "base", "the driver turns his head: his profile against the lit street"),
    ("03_C054_parotta", "C054", 0.32, "base", "parotta maker flipping at the tawa, the stall behind him"),
    ("04_C054_parotta_close", "C054", 3.92, (46.0, 752, 1000), "closer: his face and hands at the tawa"),
    ("05_C052_cook_plating", "C052", 1.00, "push", "young cook's hands plating food at the stall"),
    ("06_C053_cook_serving", "C053", 1.20, "base", "the cook hands food across to a customer"),
    ("07_C062_vendor", "C062", 0.52, "base", "jewellery vendor at his street stall, on his phone, red car behind"),
    ("08_C062_vendor_close", "C062", 4.92, (46.0, 787, 830), "closer: the vendor looking into his phone"),
    ("09_C050_paan", "C050", 0.40, "push", "paan maker in white at his stall, wrapping paan"),
    ("10_C051_paan_look", "C051", 0.20, "base", "the paan maker looks away, still, lost in thought"),
    ("11_C063_carwash", "C063", 1.00, "push", "next morning: the young car-washer foaming a scooter"),
    ("12_C064_carwash_look", "C064", 6.72, "base", "he looks up from the work toward the camera"),
]
LINE_OF = lambda i: i // 2  # two shots per line


def camera_path(cid):
    return sorted((REEL / "raw" / "Media").glob(f"*_{cid}.mov"))[0]


def bake_all():
    ranges = {}
    for i, (_, cid, cin, *_r) in enumerate(SHOTS):
        dur = CUTS[i + 1] - CUTS[i]
        lo, hi = ranges.get(cid, (1e9, -1e9))
        ranges[cid] = (min(lo, cin), max(hi, cin + dur))
    out = REEL / "raw" / "baked"
    out.mkdir(parents=True, exist_ok=True)
    bmap = {}
    for cid, (lo, hi) in ranges.items():
        start = max(0.0, round((lo - 0.48) * FPS) / FPS)
        dur = round((hi + 0.48 - start) * FPS) / FPS
        dst = out / f"{cid}_f2_{start:05.2f}.mov"
        if not dst.exists():
            r = subprocess.run([str(REEL / "tools" / "cine_bake"), str(camera_path(cid)), str(dst), "--start", f"{start:.2f}",
                                "--dur", f"{dur:.2f}"], capture_output=True, text=True)
            if r.returncode:
                raise SystemExit(f"bake {cid}: {r.stderr or r.stdout}")
        bmap[cid] = {"camera": str(camera_path(cid).relative_to(STUDIO)), "baked": str(dst.relative_to(STUDIO)),
                     "start": start, "dur": dur, "fnumber": 2.0}
        print(f"baked {cid} {start:.2f}+{dur:.2f}s → {dst.name}")
    (REEL / "analysis" / "bake_map.json").write_text(json.dumps(bmap, indent=1))
    return bmap


def font(path, size, index=0):
    return ImageFont.truetype(str(path), size, index=index)


def wrap(d, text, f, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=f) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur)
            cur = w
    return lines + [cur]


def overlays():
    od = REEL / "renders" / "overlays"
    od.mkdir(parents=True, exist_ok=True)
    # 4:3 window matte
    m = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    ImageDraw.Draw(m).rectangle([0, WIN_Y0, W - 1, WIN_Y1 - 1], fill=(0, 0, 0, 0))
    m.save(od / "window_matte_4x3.png")
    # letter lines, in the black band under the window
    fh = font(SUP / "Baskerville.ttc", 54, 2)
    fe = font(SUP / "Baskerville.ttc", 34, 2)
    x, maxw = 70, 940 - 70
    for n, (hi, en) in enumerate(LINES, 1):
        im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        y = WIN_Y1 + 48
        for ln in wrap(d, hi, fh, maxw):
            d.text((x, y), ln, font=fh, fill=CREAM + (255,))
            y += 66
        y += 8
        for ln in wrap(d, en, fe, maxw):
            d.text((x, y), ln, font=fe, fill=(232, 228, 220, 205))
            y += 44
        assert y < H - 320, f"line {n} enters the bottom IG band"
        im.save(od / f"line_{n:02d}.png")
    # end card
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    title = "Mera diya bhi jalaana"
    ft = font(FONTS / "RozhaOne-Regular.ttf", 92)
    while d.textlength(title, font=ft) > 880:
        ft = font(FONTS / "RozhaOne-Regular.ttf", ft.size - 2)
    tb = d.textbbox((0, 0), title, font=ft)
    tx, ty = (W - (tb[2] - tb[0])) // 2 - tb[0], 820
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).text((tx, ty), title, font=ft, fill=(255, 190, 90, 150))
    glow = glow.filter(ImageFilter.GaussianBlur(12))
    im.alpha_composite(glow)
    d = ImageDraw.Draw(im)
    d.text((tx, ty), title, font=ft, fill=CREAM + (255,))
    fs = font(SUP / "Baskerville.ttc", 36, 2)
    sub = "light my diya too"
    d.text(((W - d.textlength(sub, font=fs)) // 2, ty + 128), sub, font=fs, fill=(232, 228, 220, 200))
    fsig = font(SUP / "Baskerville.ttc", 50, 2)
    sig = "— tumhara beta"
    d.text(((W - d.textlength(sig, font=fsig)) // 2, ty + 230), sig, font=fsig, fill=CREAM + (255,))
    fhd = font("/System/Library/Fonts/HelveticaNeue.ttc", 28, 7)
    hd = "@satyajitmall"
    d.text(((W - d.textlength(hd, font=fhd)) // 2, 1500), hd, font=fhd, fill=(220, 220, 220, 170))
    im.save(od / "end_card.png")


def edl(bmap):
    shots = []
    for i, (name, cid, cin, framing, shows) in enumerate(SHOTS):
        st, en = CUTS[i], CUTS[i + 1]
        dur = round(en - st, 2)
        b = bmap[cid]
        s = {"name": name, "start": st, "end": en, "clip": b["baked"], "src_in": round(cin - b["start"], 2), "rate": 1,
             "rotation": -90, "line": LINES[LINE_OF(i)][0], "shows": shows,
             "note": f"camera {Path(b['camera']).name} in {cin:.2f} s; Cinematic depth baked f/2 (bake start {b['start']:.2f})"}
        if framing == "push":
            s.update(scale=[[0, BASE_SCALE], [dur, 39.5]], pos=POS, ease="ease")
        elif framing == "base":
            s.update(scale=BASE_SCALE, pos=POS)
        else:
            sc, px, py = framing
            s.update(scale=sc, pos=[px, py], note=s["note"] + f"; framing exception: closer beat of the same worker, {1080 / (3840 * sc / 100):.0%} of width")
        shots.append(s)
    shots.append({"name": "13_end_card", "start": CUTS[-1], "end": RUNTIME, "line": "— tumhara beta (title on black)",
                  "shows": "title 'Mera diya bhi jalaana', sign-off, handle"})
    ov = [{"file": f"{R}/renders/overlays/window_matte_4x3.png", "start": 0.0, "end": CUTS[-1]}]
    for n in range(6):
        a, b = CUTS[2 * n], CUTS[2 * n + 2]
        ov.append({"file": f"{R}/renders/overlays/line_{n + 1:02d}.png", "start": round(a + (0.20 if n == 0 else 0.12), 2),
                   "end": round(b - 0.08, 2)})
    ov.append({"file": f"{R}/renders/overlays/end_card.png", "start": CUTS[-1] + 0.12, "end": RUNTIME})
    doc = {"fps": FPS, "runtime": RUNTIME,
           "note": "could-not-go-home-diwali v1: letter A 'Sorry, Maa', 6 lines × 2 bars on the 152 BPM guide (howwdeep.exe original audio), "
                   "2 shots per line, one worker per line. 4:3 window (Scale 37.5, Rotation -90, Position 540,910 + matte), camera-true, "
                   "Cinematic depth baked at f/2. Pushes only on motion.json holds. Plain cuts. Title Rozha One, lines Baskerville Italic.",
           "shots": shots, "overlays": ov,
           "audio": [{"file": f"{R}/audio/guide_ref.wav", "start": 0.0, "in": 0.0, "gain_db": 0.0, "fade_in": 0, "fade_out": 0.2}]}
    (REEL / "analysis" / "edl_v1.json").write_text(json.dumps(doc, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v1.json:", len(shots), "shots,", len(ov), "overlays")


if __name__ == "__main__":
    bm = bake_all()
    overlays()
    edl(bm)
