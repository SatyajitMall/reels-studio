#!/bin/zsh
# Gate v11 loop 2 fixes (editor-verified): C027 re-rendered lighter (red light kept), dhaki at 1x; skin anchor on C190 / C193; teal line on C213.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R; L=renders/final_shots
$P tools/shot_render_v5.py 2 --ver m1 --edl v9r --natural-matched > $L/_log_m1_v9r_2.txt 2>&1 &
$P tools/shot_render_v5.py 14 --ver m1 --edl v9r --natural-matched > $L/_log_m1_v9r_14.txt 2>&1 &
$P tools/skin_post.py m1d m1s 3 13 2>&1 | grep -v Warn &
wait; grep -h "✓\|Traceback" $L/_log_m1_v9r_2.txt $L/_log_m1_v9r_14.txt
$P tools/deflicker.py 2 m1 m1d --clip C027 && $P tools/deflicker.py 14 m1 m1d --clip C027 || exit 1
for a in "2 C027 m_C027a m1d" "14 C027 m_C027b m1d" "3 C190 m_C190 m1s" "13 C193 m_C193 m1s" "9 C213 m_C213 m1d"; do
  set -- ${=a}; $P tools/shot_trim.py $1 $4 m1e --clip $2 --key $3 | sed 's/trims {.*}, gain/gain/' || exit 1
done
$P tools/v9_build.py 2 3 8 12 --edl v11 --out v11f || exit 1
for n in 2 3 8 12; do $P tools/bw_render.py $n --src v11f --out bw11 > /dev/null || exit 1; done
$P tools/preview_assemble.py v11f v11 renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 || exit 1
$P tools/preview_assemble.py bw11 v11 renders/previews/pujo-ki-asolei-sobar_v11bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -1
rm -rf $R/analysis/review_v11/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v11_preview.mp4 -o $R/analysis/review_v11/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo V11E DONE
