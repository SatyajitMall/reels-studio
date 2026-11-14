#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
for a in "2 C027 m_C027a" "14 C027 m_C027b" "3 C190 m_C190" "5 C222 m_C222" "6 C212 m_C212" "9 C213 m_C213" "9 C215 m_C215" "13 C193 m_C193"; do
  set -- ${=a}; $P tools/shot_trim.py $1 m1d m1e --clip $2 --key $3 || exit 1
done
$P tools/v9_build.py 2 3 5 6 8 9 12 --edl v11 --out v11f || exit 1
for n in 2 3 5 6 8 9 12; do $P tools/bw_render.py $n --src v11f --out bw11 || exit 1; done
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -2
rm -rf $R/analysis/review_v11/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V11A DONE
