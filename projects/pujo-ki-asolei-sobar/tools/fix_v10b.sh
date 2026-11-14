#!/bin/zsh
# Gate v10 fixes: person-protected grade trims, face lifts, floors; shot 5/6 timing; rebuild; B&W; previews; scan; watch.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_trim.py 2 v9d v9e || exit 1
$P tools/shot_trim.py 3 v9d v9e || exit 1
$P tools/shot_trim.py 8 v6 v9e --clip C201 --key C201 || exit 1
$P tools/shot_trim.py 9 v6 v9e --clip C213 --key C213 || exit 1
$P tools/shot_trim.py 9 v9d v9e --clip C215 --key 9 || exit 1
$P tools/shot_trim.py 11 v6 v9e --clip C052 --key C052 || exit 1
$P tools/shot_trim.py 11 v9c v9e --clip C216 --key C216 || exit 1
$P tools/shot_trim.py 13 v6 v9e --clip C193 --key 13 || exit 1
$P tools/v9_build.py 2 3 5 6 7 8 9 10 11 12 || exit 1
for n in 2 3 5 6 7 8 9 10 11 12; do $P tools/bw_render.py $n --src v9f --out bw9 || exit 1; done
$P tools/preview_assemble.py v9f v9 renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 || exit 1
$P tools/preview_assemble.py bw9 v9 renders/previews/pujo-ki-asolei-sobar_v10bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 -o $R/analysis/review_v10/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -3
rm -rf $R/analysis/review_v10/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 -o $R/analysis/review_v10/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V10B DONE
