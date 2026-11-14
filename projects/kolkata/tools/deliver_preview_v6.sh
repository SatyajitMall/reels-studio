#!/bin/zsh
# KOLKATA round 6: loudness-matched copy, 720p phone copy (29 MB cap at 78.8 s: encode_master --phone refuses), pregate.
# Usage (studio root): zsh projects/kolkata/tools/deliver_preview_v6.sh
set -e
P=projects/kolkata
SP=${TMPDIR:-/tmp}
I=$P/renders/previews/kolkata_v6_p1.mp4
L=$P/renders/previews/kolkata_v6_p1_ln.mp4
O=$P/renders/previews/kolkata_v6_p1_phone.mp4
J=$(ffmpeg -hide_banner -i $I -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
mi=$(echo $J | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["input_i"],d["input_tp"],d["input_lra"],d["input_thresh"],d["target_offset"])')
read ii itp ilra ith off <<< "$mi"
ffmpeg -v error -y -i $I -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=${ii}:measured_TP=${itp}:measured_LRA=${ilra}:measured_thresh=${ith}:offset=${off}:linear=true,aresample=48000" -c:a aac -b:a 256k -movflags +faststart $L
ffmpeg -v error -y -i $L -vf scale=720:1280:flags=lanczos -c:v libx264 -profile:v high -preset slow -b:v 2750k -pass 1 -passlogfile $SP/p5b -an -f mp4 /dev/null
ffmpeg -v error -y -i $L -vf scale=720:1280:flags=lanczos -c:v libx264 -profile:v high -preset slow -b:v 2750k -maxrate 4000k -bufsize 8000k -pass 2 -passlogfile $SP/p5b -c:a aac -b:a 128k -movflags +faststart $O
ls -la $L $O
./.venv/bin/python scripts/pregate.py $L --map $P/analysis/edl_v6.json -o $P/analysis/pregate_v6_p1 --fps 25 --expect 76.20 \
  --designed 0-0.3 29.25-29.85 75.3-76.2 --no-fidelity > $P/analysis/pregate_v6.log 2>&1 || true
cat $P/analysis/pregate_v6_p1/PREGATE.md | head -16
