#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_trim.py 6 m1d m1e --clip C212 --key m_C212 && $P tools/shot_trim.py 11 m1d m1e --clip C216 --key g_C216 || exit 1
$P tools/v9_build.py --edl v11 --out v11f || exit 1
for n in 2 3 4 5 6 7 8 9 10 11 12; do $P tools/bw_render.py $n --src v11f --out bw11 > /dev/null || exit 1; done
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -2
rm -rf $R/analysis/review_v11/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V11C DONE
