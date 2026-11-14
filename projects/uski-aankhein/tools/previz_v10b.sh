#!/usr/bin/env bash
# v10b previz: as previz_v9b.sh with grain 9 % (review v10 #3), and the end card moved up ENDCARD_DY px (review v9 #4: onto the chin, off the scaffold). Local previz: V1 timeline bake + V2 stock band (Screen 65 %) -> look .cube + vignette (the V3 layer) -> V4 grain (Overlay 12 %)
# -> V5 title / end card -> A3 music + A2 booms (-14 dB). Usage: tools/previz.sh <V1.mov> <look.cube> <out.mp4>
set -euo pipefail
cd "$(dirname "$0")/.."
V1="$1"; LUT="$2"; OUT="$3"; ENDCARD_DY="${ENDCARD_DY:--240}"
ffmpeg -v error -y -i "$V1" -i renders/texture/grain_25fps_v1.mov \
  -i graphics/title/renders/title-alpha-v2b.mov -i graphics/endcard/renders/endcard-alpha.mov \
  -i references/ref_audio.wav -i audio/sfx/gemini_bass_drop_boom.wav -filter_complex "
[0:v]scale=in_range=tv:out_range=pc,format=gbrp[g0];

[g0]lut3d=file=$LUT,vignette=angle=0.42[g];
[1:v]scale=in_range=tv:out_range=pc,format=gbrp,tpad=stop_mode=add:stop_duration=1:color=0x808080[gr];
[g][gr]blend=all_mode=overlay:all_opacity=0.09:shortest=1,format=yuv420p[g1];
[2:v]setpts=PTS+8.60/TB[t];[3:v]setpts=PTS+20.6/TB[e];
[g1][t]overlay=0:0:eof_action=pass[g2];[g2][e]overlay=0:${ENDCARD_DY}:eof_action=pass,trim=end=22.0,scale=out_range=tv:out_color_matrix=bt709,format=yuv420p[v];
[5:a]asplit=2[b1][b2];[b1]adelay=7840|7840,volume=-16dB[s1];[b2]adelay=15960|15960,volume=-16dB[s2];
[4:a][s1][s2]amix=inputs=3:normalize=0:duration=first,atrim=end=22.0[a]" -map "[v]" -map "[a]" -r 25 \
  -c:v libx264 -crf 16 -preset medium -pix_fmt yuv420p -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -c:a aac -b:a 256k -movflags +faststart "$OUT"
echo "✓ $OUT"
