#!/usr/bin/env bash
# Rebuild site/media/*.mp4 + posters from picks.txt (videos are not in git; the published Artifact keeps them,
# and a republish that leaves media/ out keeps the old files). Needs: tiktok.py video downloads in $TT/<id>/video.mp4
# and Grace's intro clip at $HERO. Usage: TT=<dir> HERO=<file> bash grace/portfolio/build_media.sh
set -euo pipefail
cd "$(dirname "$0")/site/media"
enc() { id=$1; kind=$2
  if [ "$id" = hero ]; then src=$HERO; vf="scale=720:-2"; crf=27
  elif [ "$kind" = featured ]; then src=$TT/$id/video.mp4; vf="scale=540:-2"; crf=28
  else src=$TT/$id/video.mp4; vf="scale=480:-2"; crf=30; fi
  ffmpeg -nostdin -v error -y -i "$src" -vf "$vf,format=yuv420p" -c:v libx264 -preset medium -crf $crf -profile:v high \
    -movflags +faststart -c:a aac -b:a 64k -ac 2 "$id.mp4"
  [ -f "$id.jpg" ] || ffmpeg -nostdin -v error -y -ss 1.2 -i "$id.mp4" -frames:v 1 -q:v 4 "$id.jpg"; }
export -f enc; export TT HERO
cut -f1,2 ../../picks.txt | tr '\t' ' ' | xargs -P4 -L1 bash -c 'enc $0 $1'
