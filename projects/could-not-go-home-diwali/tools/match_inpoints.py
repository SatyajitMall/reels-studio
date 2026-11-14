"""Find, for each v3 shot that plays a half-size pre-render, the frame of its full-size bake that the pre-render starts
on (MSE on small grey frames), so the Premiere build places the bake frame-exact. Writes analysis/build_v3_inpoints.json."""
import json, subprocess
from pathlib import Path
import numpy as np
STUDIO = Path(__file__).resolve().parents[3]; REEL = Path(__file__).resolve().parents[1]
def fr(p, w=54, h=96, t=None):
    cmd = ["ffmpeg", "-v", "error", "-i", str(STUDIO / p)] + (["-t", str(t)] if t else []) + ["-vf", f"scale={w}:{h},format=gray", "-f", "rawvideo", "-"]
    a = np.frombuffer(subprocess.run(cmd, capture_output=True).stdout, np.uint8).astype(np.float32)
    return a[: a.size // (w * h) * w * h].reshape(-1, h, w)
edl = json.loads((REEL / "analysis/edl_v3.json").read_text())
out = {}
for s in edl["shots"]:
    c = s.get("clip") or ""
    if "fx_preview" not in c:
        continue
    b = Path(c).stem
    bake = next(p for p in [f"projects/could-not-go-home-diwali/raw/baked/v2/{b}.mov", f"projects/could-not-go-home-diwali/raw/baked/v2b/{b}.mov"] if (STUDIO / p).exists())
    pv = fr(c, t=0.2)            # first 5 frames of the pre-render
    bk = fr(bake)
    # both decode autorotated to the same (sideways) 9:16 display orientation
    errs = [np.mean([((bk[i + k] - pv[k]) ** 2).mean() for k in range(3)]) for i in range(len(bk) - 3)]
    errs2 = None
    i = int(np.argmin(errs)); e = float(errs[i]); srt = sorted(errs)
    out[s["name"]] = {"bake": bake, "in_frame": i, "in_s": round(i / 25, 3), "mse": round(e, 1), "next_best": round(float(srt[1]), 1)}
    print(f"{s['name']:22s} {bake.split('/')[-2]}/{Path(bake).name:26s} in {i:3d} f ({i/25:.2f} s) mse {e:7.1f} 2nd {srt[1]:7.1f}")
(REEL / "analysis/build_v3_inpoints.json").write_text(json.dumps(out, indent=1))
