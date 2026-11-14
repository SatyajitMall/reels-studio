#!/bin/zsh
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/shot_trim.py 9 v6 v9e --clip C213 --key C213 || exit 1
$P tools/v9_build.py 8 && $P tools/bw_render.py 8 --src v9f --out bw9 || exit 1
$R/tools/prev_v10.sh
