#!/bin/zsh
# Review gate v9 loop 1 fixes: C027 longer render; 2nd deflicker pass on 2/3/4/9; grade trims; rebuild; B&W; previews; scan + watch.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_render_v5.py 2 --ver v9 --edl v9r > renders/final_shots/_log_v9_2.txt 2>&1 || exit 1
grep -h "✓\|stabilise" renders/final_shots/_log_v9_2.txt
$P tools/skin_post.py v9 v9b 2 2>&1 | grep -v Warn | tail -2
$P tools/deflicker.py 2 v9b v9d --iters 3 || exit 1
for n in 3 4 9; do $P tools/deflicker.py $n $( [ $n = 4 ] && echo v6 || echo v9c ) v9d --iters 3 || exit 1; done
$P tools/shot_trim.py 2 v9d v9e && $P tools/shot_trim.py 3 v9d v9e && $P tools/shot_trim.py 9 v9d v9e && $P tools/shot_trim.py 5 v9c v9e && $P tools/shot_trim.py 13 v6 v9e || exit 1
$P tools/v9_build.py 2 3 4 5 6 9 12 || exit 1
for n in 2 3 4 5 6 9 12; do $P tools/bw_render.py $n --src v9f --out bw9 || exit 1; done
$P tools/preview_assemble.py v9f v9 renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 || exit 1
$P tools/preview_assemble.py bw9 v9 renders/previews/pujo-ki-asolei-sobar_v9bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
cd $HOME/Documents/reels-studio
$P scripts/frame_scan.py $R/renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 -o $R/analysis/review_v9/scan.json --shots $R/analysis/shots_v9.json 2>&1 | tail -4
rm -rf $R/analysis/review_v9/watch; $P scripts/watch.py $R/renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 -o $R/analysis/review_v9/watch --fps 2 --shots $R/analysis/shots_v9.json 2>&1 | tail -1
echo FIXB DONE
