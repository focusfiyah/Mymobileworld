#!/usr/bin/env bash
# Clean one Grace VO for the clone: music out (demucs), silence trimmed, mono 44.1k wav.
# Usage: grace/voice/r5/sep.sh IN.(mp4|wav) OUT.wav     (venv: /root/.demucs-venv, see README round 5)
set -euo pipefail
in=$1; out=$2; tmp=$(mktemp -d)
ffmpeg -loglevel error -y -i "$in" -ac 1 -ar 44100 "$tmp/a.wav"
/root/.demucs-venv/bin/python -m demucs --two-stems=vocals -n htdemucs -o "$tmp/sep" "$tmp/a.wav" >/dev/null 2>&1
ffmpeg -loglevel error -y -i "$tmp/sep/htdemucs/a/vocals.wav" -ac 1 -ar 44100 \
  -af "silenceremove=start_periods=1:start_threshold=-45dB:stop_periods=-1:stop_duration=0.35:stop_threshold=-45dB" "$out"
rm -rf "$tmp"
