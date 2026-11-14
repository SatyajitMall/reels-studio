#!/bin/zsh
# deliver_v3.sh <VERSION> <runtime_s>: KOLKATA deliverables from renders/masters/kolkata_<VERSION>_master.mov (e.g. v3b_M1) (run from the studio root).
#   _mix   H.264 High, guide song baked, loudnorm −14 LUFS / −1.5 dBTP (archive and review only; never posted)
#   _IG    the same picture with silent audio (upload; the song is added in Instagram, CLAUDE.md §4c)
#   phone  ≤ 29 MB review copy of _mix
# then the pregate on _mix (EDL as the shot map; fidelity off: camera_fidelity can't read rotation or the 4:5 window, CR-20261104 #6).
set -e
T=$1; R=$2; P=projects/kolkata; M=$P/renders/masters/kolkata_${T}_master.mov; E=$P/renders/exports; L=$P/analysis/deliver_$T.log
./.venv/bin/python scripts/encode_master.py $M -o $E/kolkata_${T}_raw.mp4 > $L 2>&1
ffmpeg -v error -y -i $E/kolkata_${T}_raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11" -ar 48000 -c:a aac -b:a 320k -shortest -movflags +faststart $E/kolkata_${T}_mix.mp4
ffmpeg -v error -y -i $E/kolkata_${T}_raw.mp4 -f lavfi -i anullsrc=r=48000:cl=stereo -map 0:v -map 1:a -c:v copy -c:a aac -b:a 128k -shortest -movflags +faststart $E/kolkata_${T}_IG.mp4
rm $E/kolkata_${T}_raw.mp4
./.venv/bin/python scripts/encode_master.py $E/kolkata_${T}_mix.mp4 -o $P/renders/previews/kolkata_${T}_phone.mp4 --phone >> $L 2>&1
END=$(python3 -c "print(round($R-0.8,2))")
./.venv/bin/python scripts/pregate.py $E/kolkata_${T}_mix.mp4 --map $P/analysis/edl_$T.json -o $P/analysis/pregate_$T \
  --fps 25 --expect $R --designed 0-0.3 $END-$R --no-fidelity >> $L 2>&1 && echo "PREGATE PASS $T" || echo "PREGATE FAIL $T"
