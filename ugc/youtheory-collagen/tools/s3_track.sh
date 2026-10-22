#!/bin/sh
# S3 (2026-10-22): Seedance first-frame take garbles the small box print after 0.3 s; track its own frame 0 (= the approved still) back on, 3 flat areas, no skin mask
set -e; T=tools/label_track.py; R=refs/s3_frame0.png
python3 $T clips/S3_seedance_raw.mp4 /tmp/s3a.mp4 --ref $R --rect 150,836,555,1030 --noskin
python3 $T /tmp/s3a.mp4 /tmp/s3b.mp4 --ref $R --rect 420,722,555,834 --noskin
python3 $T /tmp/s3b.mp4 clips/S3.mp4 --ref $R --rect 150,640,335,828 --noskin
