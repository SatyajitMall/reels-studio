#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/v9_build.py 5 11 || exit 1
$P tools/bw_render.py 5 --src v9f --out bw9 && $P tools/bw_render.py 11 --src v9f --out bw9 || exit 1
$P tools/preview_assemble.py v9f v9 renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 || exit 1
$P tools/preview_assemble.py bw9 v9 renders/previews/pujo-ki-asolei-sobar_v9bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 -o $R/analysis/review_v9/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -4
rm -rf $R/analysis/review_v9/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 -o $R/analysis/review_v9/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo FIX DONE
