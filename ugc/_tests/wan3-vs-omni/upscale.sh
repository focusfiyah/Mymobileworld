#!/usr/bin/env bash
# Free 720p -> 1080x1920 upscale for Wan 3.0 clips (tested 2026-11-03 on S3_wan3.mp4: label at 2x close to Omni native 1080p,
# no halos on hand edges; matched a free AI upscaler (FSRCNN x2) that took 2 min per 5 s). ~4 s per clip on 4 cores.
# usage: upscale.sh IN.mp4 OUT.mp4   (ai_finish.sh still runs last on the final cut)
set -euo pipefail
ffmpeg -loglevel error -y -i "$1" -vf "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0" -c:v libx264 -crf 16 -preset veryfast -threads 4 -pix_fmt yuv420p "$2"
