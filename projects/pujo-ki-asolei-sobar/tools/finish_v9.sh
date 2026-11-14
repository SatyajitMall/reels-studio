#!/bin/zsh
# Round 9: build the new timeline shots, B&W versions of all 12, offline previews of both versions.
R=$HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar; P=$HOME/Documents/reels-studio/.venv/bin/python
cd $R
$P tools/v9_build.py 2 3 5 6 9 11 || exit 1
for n in 2 3 4 5 6 7 8 9 10 11 12; do $P tools/bw_render.py $n --src v9f --out bw9 || exit 1; done
$P tools/preview_assemble.py v9f v9 renders/previews/pujo-ki-asolei-sobar_v9_preview.mp4 || exit 1
$P tools/preview_assemble.py bw9 v9 renders/previews/pujo-ki-asolei-sobar_v9bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
echo FINISH DONE
