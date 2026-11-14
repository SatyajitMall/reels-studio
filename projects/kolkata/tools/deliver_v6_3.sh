#!/bin/zsh
# deliver_v6_3.sh: KOLKATA v6_3 (review-gate fixes) deliverables from renders/masters/kolkata_v6_3_master.mov (run from the studio root).
#   _mix   H.264 High, the edited song baked, loudnorm −14 LUFS / −1.5 dBTP. This is the one to POST: the guide's name cut
#          can't exist in Instagram's library audio (round 6), so no _IG version.
#   phone  ≤ 29 MB review copy of _mix
# then the pregate on _mix (EDL v6d as the shot map; fidelity off: camera_fidelity can't read rotation or the 4:5 window, CR-20261104 #6).
set -e
P=projects/kolkata; M=$P/renders/masters/kolkata_v6_3_master.mov; E=$P/renders/exports; L=$P/analysis/deliver_v6_3.log
./.venv/bin/python scripts/encode_master.py $M -o $E/kolkata_v6_3_raw.mp4 > $L 2>&1
J=$(ffmpeg -hide_banner -i $E/kolkata_v6_3_raw.mp4 -af loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json -f null - 2>&1 | sed -n '/^{/,/^}/p')
mi=$(echo $J | python3 -c 'import json,sys;d=json.load(sys.stdin);print(d["input_i"],d["input_tp"],d["input_lra"],d["input_thresh"],d["target_offset"])')
read ii itp ilra ith off <<< "$mi"
ffmpeg -v error -y -i $E/kolkata_v6_3_raw.mp4 -c:v copy -af "loudnorm=I=-14:TP=-1.5:LRA=11:measured_I=${ii}:measured_TP=${itp}:measured_LRA=${ilra}:measured_thresh=${ith}:offset=${off}:linear=true,aresample=48000" -c:a aac -b:a 320k -movflags +faststart $E/kolkata_v6_3_mix.mp4
rm $E/kolkata_v6_3_raw.mp4
./.venv/bin/python scripts/encode_master.py $E/kolkata_v6_3_mix.mp4 -o $P/renders/previews/kolkata_v6_3_phone.mp4 --phone >> $L 2>&1 || echo "phone: encode_master refused (size cap)" >> $L
ls -la $E/kolkata_v6_3_mix.mp4 $P/renders/previews/kolkata_v6_3_phone.mp4 >> $L 2>&1 || true
./.venv/bin/python scripts/pregate.py $E/kolkata_v6_3_mix.mp4 --map $P/analysis/edl_v6d.json -o $P/analysis/pregate_v6_3 \
  --fps 25 --expect 76.20 --designed 0-0.3 75.3-76.2 --no-fidelity --prev $E/kolkata_v6b_mix.mp4 --prev-map $P/analysis/edl_v6d_build2.json >> $L 2>&1 && echo "PREGATE PASS v6_3" || echo "PREGATE FAIL v6_3"
