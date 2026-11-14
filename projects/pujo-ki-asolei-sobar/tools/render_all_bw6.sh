#!/bin/zsh
# Round 8: B&W + gold and the colour fade rebuilt from the deflickered v6 shots; then offline previews of both versions.
cd $HOME/Documents/reels-studio/projects/pujo-ki-asolei-sobar
P=$HOME/Documents/reels-studio/.venv/bin/python
$P tools/bw_render.py 1 --isolate --src v6 --out bw6 || exit 1
for n in 2 3 4 5 6 7 8 9 10 11 12 13; do $P tools/bw_render.py $n --src v6 --out bw6 || exit 1; done
$P tools/bw_fade.py --a v6 --b bw6 --name bwfade6 || exit 1
$P tools/preview_assemble.py v6 v5 renders/previews/pujo-ki-asolei-sobar_v6_preview.mp4 || exit 1
$P tools/preview_assemble.py bw6 v5 renders/previews/pujo-ki-asolei-sobar_v6bw_preview.mp4 --shot1 bwfade6 --bw-text || exit 1
echo ALL DONE
