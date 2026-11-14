#!/bin/zsh
# Round 10: brighter darker shots, shot 2 rebuilt (face-on angle + eased slow-mo); B&W; previews; scan; watch.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_trim.py 3 v9d v9e && $P tools/shot_trim.py 4 v9d v9e && $P tools/shot_trim.py 5 v9c v9e && $P tools/shot_trim.py 6 v9c v9e && $P tools/shot_trim.py 9 v9d v9e && $P tools/shot_trim.py 8 v6 v9e || exit 1
$P tools/v9_build.py 2 3 4 5 6 7 9 || exit 1
for n in 2 3 4 5 6 7 9; do $P tools/bw_render.py $n --src v9f --out bw9 || exit 1; done
$P tools/preview_assemble.py v9f v9 renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 || exit 1
$P tools/preview_assemble.py bw9 v9 renders/previews/pujo-ki-asolei-sobar_v10bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
mkdir -p $R/analysis/review_v10
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 -o $R/analysis/review_v10/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -3
$P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v10_preview.mp4 -o $R/analysis/review_v10/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V10 DONE
