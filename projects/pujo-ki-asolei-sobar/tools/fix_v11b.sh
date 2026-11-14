#!/bin/zsh
# Gate v11 loop 1 fixes: re-render C222 (spatial-only denoise) + C212 (from 0.75 s); brightness follows the original; rebuild.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R; L=renders/final_shots
$P tools/shot_render_v5.py 5 --ver m1 --edl v9r --natural-matched > $L/_log_m1_v9r_5.txt 2>&1 &
$P tools/shot_render_v5.py 6 --ver m1 --edl v9r --natural-matched > $L/_log_m1_v9r_6.txt 2>&1 &
wait; grep -h "✓\|Traceback" $L/_log_m1_v9r_5.txt $L/_log_m1_v9r_6.txt
$P tools/deflicker.py 5 m1 m1d --clip C222 && $P tools/deflicker.py 6 m1 m1d --clip C212 || exit 1
for a in "1 C152 g_C152" "3 C190 m_C190" "4 C032 g_C032" "5 C222 m_C222" "6 C212 m_C212" "8 C201 g_C201" "9 C213 m_C213" "9 C215 m_C215" "11 C052 g_C052" "11 C216 g_C216" "13 C193 m_C193"; do
  set -- ${=a}; $P tools/shot_trim.py $1 m1d m1e --clip $2 --key $3 | sed 's/trims {.*}, gain/gain/' || exit 1
done
$P tools/v9_build.py --edl v11 --out v11f || exit 1
for n in 2 3 4 5 6 7 8 9 10 11 12; do $P tools/bw_render.py $n --src v11f --out bw11 > /dev/null || exit 1; done
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -2
rm -rf $R/analysis/review_v11/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V11B DONE
