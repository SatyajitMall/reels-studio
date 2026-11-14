#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/v9_build.py 6 --edl v11 --out v11f && $P tools/bw_render.py 6 --src v11f --out bw11 > /dev/null || exit 1
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -1
rm -rf $R/analysis/review_v11/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
cd $R && $P - <<'PY'
import subprocess, numpy as np
for f in ["renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4", "renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4"]:
    raw = subprocess.run(["ffmpeg","-v","error","-i",f,"-vf","scale=270:480","-f","rawvideo","-pix_fmt","gray","-"],capture_output=True).stdout
    F = np.frombuffer(raw,np.uint8).reshape(-1,480,270).astype(np.float32); d = np.abs(np.diff(F, axis=0)).mean((1,2))
    print(f.split("/")[-1], len(F), "frames, dups:", [k+1 for k in range(len(d)) if d[k] < 0.05])
PY
echo V11D DONE
