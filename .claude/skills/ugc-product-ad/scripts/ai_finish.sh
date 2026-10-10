#!/bin/bash
# AI-UGC finish (free), last step before posting. Source: @ericdoesecom (TikTok 7693658375199984927, 2026-10-06):
# "20% film grain + 20% sharpness in CapCut before you upload so TikTok doesn't tag it as AI; for AI UGC also turn saturation down a bit."
# CapCut's % scale is not published; the ffmpeg values below are our match for "20%". Usage: ai_finish.sh IN OUT [grain=6] [sharp=0.6] [sat=0.92]
set -e
IN=$1; OUT=$2; G=${3:-6}; S=${4:-0.6}; SAT=${5:-0.92}
ffmpeg -y -loglevel error -i "$IN" -vf "eq=saturation=$SAT,unsharp=5:5:$S:5:5:0,noise=alls=$G:allf=t" \
  -c:v libx264 -crf 18 -preset veryfast -pix_fmt yuv420p -c:a copy -movflags +faststart "$OUT"
echo "finished $OUT"
