#!/bin/zsh
# Round 13: trims (+1/2 stop) on the re-deflickered shots, build v13, colour preview, scan, watch.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
for a in "1 C152 v13_C152 m2d" "2 C027 v13_C027a m2d" "15 C028 v13_C028 m2d" "3 C190 v13_C190 m2s" "4 C032 v13_C032 m2d" "5 C222 v13_C222 m2d" "6 C212 v13_C212 m2d" "8 C201 v13_C201 m2d" "9 C213 v13_C213 m2d" "9 C215 v13_C215 m2d" "11 C052 v13_C052 m2d" "11 C216 v13_C216 m2d" "13 C193 v13_C193 m2s"; do
  set -- ${=a}; $P tools/shot_trim.py $1 $4 m2e --clip $2 --key $3 | sed 's/trims {.*}, gain/gain/' || exit 1
done
$P tools/v9_build.py --edl v13 --out v13f || exit 1
$P tools/preview_assemble.py v13f v13 renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -2
$P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V13 DONE
