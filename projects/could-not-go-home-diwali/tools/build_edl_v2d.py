"""Build EDL v2d for could-not-go-home-diwali (reel-local): v2c + the director's note
"why are random shots of Victoria used, they serve no purpose; use close-ups of handling or selling flowers and firecrackers".

Only the two Kolkata slots change (director's picks from analysis/stock/stock_board_flowers_crackers.jpg):
  02 (L1, after the auto driver): F8 Pexels 8811075, hands laying marigold flowers (Yan Krukau), real time
  11 (L6, before the car-washer looks up): F9 Pexels 6618563, hands holding burning sparklers (Mariam Antadze),
     4K 30 fps interpreted at 25 (83 %, real frames)
Every other shot, the cuts, letter, window, type and end card are v2c's. Both colour versions.
Run from the studio root: .venv/bin/python -I projects/could-not-go-home-diwali/tools/build_edl_v2d.py [--mix 0.6]
"""
import argparse
import json
import sys
from pathlib import Path

STUDIO = Path(__file__).resolve().parents[3]
REEL = Path(__file__).resolve().parents[1]
R = "projects/could-not-go-home-diwali"
sys.path.insert(0, str(REEL / "tools"))
import build_edl_v2 as v2  # noqa: E402

F8 = "raw/stock/pexels-8811075/8811075-hd_1920_1080_25fps.mp4"
F9 = "raw/stock/pexels-6618563/6618563-uhd_2160_3840_30fps.mp4"


def f8_shot(st, en, line):
    dur = round(en - st, 2)
    scale, pos = v2.top_anchor(100.0 * 810 / 1080, 1080, dur)          # 1920×1080 → 4:3 middle fills the window, top kept
    return {"name": "02_F8_marigold_hands", "start": st, "end": en, "clip": f"{R}/{F8}", "src_in": 4.0, "rate": 1,
            "scale": scale, "pos": pos, "ease": "ease", "line": line,
            "shows": "stock F8: hands laying marigold flowers one by one: the Diwali work of the flower sellers",
            "note": "STOCK (Pexels 8811075, Yan Krukau; raw/SOURCES.md): real time 25 fps; top-anchored push +5 %"}


def f9_shot(st, en, line):
    dur = round(en - st, 2)
    sc0, v = 50.0, 0.55                                                    # 2160×3840 → 1080 wide; window on the band at v
    y0 = round(910 - (v - 0.5) * 3840 * sc0 / 100, 1)
    y1 = round(910 - (v - 0.5) * 3840 * sc0 * 1.05 / 100, 1)
    return {"name": "11_F9_sparkler_hands", "start": st, "end": en, "clip": f"{R}/{F9}", "src_in": 0.3, "rate": round(25 / 30, 5),
            "scale": [[0, sc0], [dur, round(sc0 * 1.05, 3)]], "pos": [[0, 540, y0], [dur, 540, y1]], "ease": "ease", "line": line,
            "shows": "stock F9: hands holding burning sparklers (83 %, real frames): Diwali in the hands of others",
            "note": "STOCK (Pexels 6618563, Mariam Antadze; raw/SOURCES.md): 4K 30 fps interpreted at 25 (83 %); window band centred at v 0.55; push +5 %"}


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mix", type=float, default=0.6)
    a = ap.parse_args()
    base = json.loads((REEL / "analysis" / "edl_v2c.json").read_text())
    look = json.loads((REEL / "analysis" / "edl_v2c_look.json").read_text())
    look_dir = REEL / "renders" / "look_v2d"; look_dir.mkdir(parents=True, exist_ok=True)
    for doc_cam, doc_look in ((base, look),):
        for i, s in enumerate(doc_cam["shots"]):
            if s["name"] in ("02_C043_kolkata", "11_C043_kolkata_again"):
                new = (f8_shot if s["name"].startswith("02") else f9_shot)(s["start"], s["end"], s["line"])
                doc_cam["shots"][i] = new
                lnew = dict(new)
                lout = look_dir / f"{new['name']}.mov"
                off = v2.lut_clip(new["clip"], new["src_in"], new["rate"], round(new["end"] - new["start"], 2), lout, a.mix, True)
                lnew["clip"] = str(lout.relative_to(STUDIO)); lnew["src_in"] = round(off, 3)
                doc_look["shots"][i] = lnew
                print("replaced", s["name"], "→", new["name"])
    note = ("v2d = v2c + director note 'why are random shots of Victoria used … use close-ups of handling or selling flowers and "
            "firecrackers': L1's insert = F8 hands laying marigolds, L6's insert = F9 hands holding burning sparklers (Pexels).")
    base["note"] = note + " Camera-true."
    look["note"] = note + f" LOOK PREVIEW: ref_match.cube at {a.mix:.0%}."
    (REEL / "analysis" / "edl_v2d.json").write_text(json.dumps(base, indent=1, ensure_ascii=False))
    (REEL / "analysis" / "edl_v2d_look.json").write_text(json.dumps(look, indent=1, ensure_ascii=False))
    print("wrote analysis/edl_v2d.json and analysis/edl_v2d_look.json")


if __name__ == "__main__":
    main()
