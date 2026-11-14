#!/usr/bin/env python3
"""Round 7 (director, 2026-10-23): the B&W version opens in colour and the colour drains out of the whole frame,
leaving only the Durga's gold.

Built with the studio's ffmpeg colour skill (.claude/skills/ffmpeg-color-grading-chromakey): a weighted `blend`
(its "Blend original with LUT" recipe) animated per frame on the timestamp T (its "Animated Color Effects" section),
in RGB (gbrp, studio fix), BT.709 tags + write_colr (studio rule).
  A = shot 1 in full colour (01_C152_v5.mov, the graded v5 render)
  B = shot 1 B&W with gold kept (01_C152_bw.mov, tools/bw_render.py --isolate: person-matted gold key)
  out = A + (B - A) * w(T), w = sine ease-in-out from 0 to 1 between T0 and T1 (source seconds)
Same frames, handles and audio as the inputs, so it drops into the timeline at the same place_in.
Usage: bw_fade.py [--t0 0.3] [--dur 2.4] [--strip] [--a v6 --b bw6 --name bwfade6]   (--strip: stills at timeline 0, 0.5 ... 3.5 s, no render)
"""
import argparse, json, subprocess
from pathlib import Path

REEL = Path(__file__).resolve().parents[1]; R = REEL / "renders" / "final_shots"
ap = argparse.ArgumentParser(); ap.add_argument("--t0", type=float, default=0.3); ap.add_argument("--dur", type=float, default=2.4)
ap.add_argument("--strip", action="store_true"); ap.add_argument("--a", default="v5"); ap.add_argument("--b", default="bw"); ap.add_argument("--name", default="bwfade")
a = ap.parse_args()
A, B = R / f"01_C152_{a.a}.mov", R / f"01_C152_{a.b}.mov"
t0, t1 = a.t0, a.t0 + a.dur
w = f"if(lt(T,{t0}),0,if(gt(T,{t1}),1,0.5-0.5*cos(PI*(T-{t0})/{a.dur})))"
graph = (f"[0:v]format=gbrp10le[a];[1:v]format=gbrp10le[b];[a][b]blend=all_expr='A+(B-A)*{w}',"
         "format=yuv422p10le,setparams=color_primaries=bt709:color_trc=bt709:colorspace=bt709:range=tv[v]")
if a.strip:
    out = REEL / "analysis/look_bw/fade"; out.mkdir(parents=True, exist_ok=True)
    for tl in [0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5]:
        ts = 0.3 + tl
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(A), "-i", str(B), "-filter_complex", graph + f";[v]trim=start={ts},setpts=PTS-STARTPTS,scale=360:640[o]",
                        "-map", "[o]", "-frames:v", "1", str(out / f"t{tl:.1f}.png")], check=True)
    print("strip ->", out)
else:
    tmp = R / "_tmp_bwfade.mov"; name = f"01_C152_{a.name}"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(A), "-i", str(B), "-filter_complex", graph, "-map", "[v]", "-map", "0:a?",
                    "-c:v", "prores_ks", "-profile:v", "3", "-pix_fmt", "yuv422p10le", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-colorspace", "bt709", "-c:a", "copy", "-movflags", "+write_colr", str(tmp)], check=True)
    tmp.rename(R / f"{name}.mov")
    r = json.loads((R / f"01_C152_{a.b}.json").read_text())
    r.update(file=f"{name}.mov", bw=True, colour_fade={"t0": t0, "t1": t1, "curve": "sine in-out", "from": A.name, "to": B.name})
    (R / f"{name}.json").write_text(json.dumps(r, indent=1)); print("✓", name)
