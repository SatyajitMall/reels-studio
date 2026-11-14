#!/bin/zsh
# Round 9: new shots through the v5 pipeline (render -> skin post-pass -> deflicker), 3 renders at a time.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
run() { $P tools/shot_render_v5.py $1 --ver v9 --edl v9r > renders/final_shots/_log_v9_$1.txt 2>&1; }
run 2 & run 3 & run 5 & wait
run 6 & run 9 & run 11 & wait
for n in 2 3 5 6 9 11; do grep -h "✓\|stabilise\|Error\|Traceback" renders/final_shots/_log_v9_$n.txt; done
$P tools/skin_post.py v9 v9b 2 3 5 6 9 11 2>&1 | grep -v Warn | tail -12
for n in 2 3 5 6 9 11; do $P tools/deflicker.py $n v9b v9c || exit 1; done
echo RENDER DONE
