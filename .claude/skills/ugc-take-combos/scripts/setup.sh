#!/usr/bin/env bash
# One-time setup per session (cloud) or machine: Python packages for take_combos.py / overlay_art.py.
# ffmpeg comes from PATH (preinstalled in Claude cloud sessions) or the imageio-ffmpeg wheel.
set -e
python3 - <<'PY' 2>/dev/null && { echo "take-combos deps OK"; exit 0; }
import faster_whisper, numpy, PIL
PY
pip install -q faster-whisper numpy pillow imageio-ffmpeg
echo "take-combos deps installed (faster-whisper downloads the small.en model on first use, ~10s)"
