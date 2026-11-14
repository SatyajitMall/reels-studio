#!/usr/bin/env bash
# v10 delivery encode (director on v9c on iPhone: "very poor quality"; Premiere's "Match Source - H.264 High Bitrate" gave
# Main profile at 9.5 Mb/s, B-frames ~23 KB, so grain and dark gradients broke into blocks). From Premiere's ProRes 422 master:
# H.264 High, CRF 15, tune film, aq-mode 3 (more bits in the darks), light deblock, 2 s GOP, BT.709 tv range, AAC 320k.
# Usage: tools/encode_hq.sh <master.mov> <out.mp4> [limit]   (limit: add the true-peak limiter used for the _mix_tp guide)
set -euo pipefail
IN="$1"; OUT="$2"; AF="anull"; [ "${3:-}" = "limit" ] && AF="alimiter=limit=0.8:level=false"
ffmpeg -v error -y -i "$IN" -map 0:v:0 -map 0:a:0 \
  -c:v libx264 -preset slow -crf 15 -tune film -profile:v high -level 4.2 -pix_fmt yuv420p \
  -x264-params "aq-mode=3:aq-strength=0.9:deblock=-1,-1:keyint=50:min-keyint=25" -maxrate 40M -bufsize 80M \
  -color_range tv -color_primaries bt709 -color_trc bt709 -colorspace bt709 \
  -af "$AF" -c:a aac -b:a 320k -ar 48000 -movflags +faststart "$OUT"
echo "✓ $OUT"
