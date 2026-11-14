#!/bin/zsh
# Gate v10 loop 2 fixes (editor-verified): shot 2b frame blend + gentler face lift + cast toward neutral; face lifts on 2a, 5, 7.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_trim.py 14 v9d v9e && $P tools/shot_trim.py 2 v9d v9e && $P tools/shot_trim.py 8 v6 v9e --clip C201 --key C201 && $P tools/shot_trim.py 5 v9c v9e || exit 1
$P tools/v9_build.py 2 5 7 || exit 1
for n in 2 5 7; do $P tools/bw_render.py $n --src v9f --out bw9 || exit 1; done
$R/tools/prev_v10.sh
