#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
for a in "1 C152 v13_C152 m4d" "2 C027 v13_C027a m4d" "15 C028 v13_C028 m4d" "3 C190 v13_C190 m4s" "4 C032 v13_C032 m4d" "5 C222 v13_C222 m4d" "6 C212 v13_C212 m4d" "8 C201 v13_C201 m4d" "9 C213 v13_C213 m4d" "9 C215 v13_C215 m4d" "11 C052 v13_C052 m4d" "11 C216 v13_C216 m4d" "13 C193 v13_C193 m4s"; do
  set -- ${=a}; $P tools/shot_trim.py $1 $4 m4e --clip $2 --key $3 > /dev/null || exit 1
done
$P tools/v9_build.py --edl v13 --out v13g > /dev/null || exit 1
$P tools/preview_assemble.py v13g v13 renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/scan.json --shots $R/analysis/shots_v13.json 2>&1 | tail -1
rm -rf $R/analysis/review_v13/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v13_preview.mp4 -o $R/analysis/review_v13/watch --fps 2 --shots $R/analysis/shots_v13.json 2>&1 | tail -1
echo V13C DONE
