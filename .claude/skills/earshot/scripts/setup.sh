#!/usr/bin/env bash
# Installs earshot (github.com/Leonxlnx/earshot, MIT) at the pinned commit into ~/.cache.
# Cloud containers are wiped between sessions, so run this once per session. ~4 min + 1.1 GB of free models.
# Usage: bash setup.sh [--no-models]   (--no-models: sound bank only; listening commands download models on first use)
set -euo pipefail
COMMIT=4ac3d2a
SRC=~/.cache/earshot-src; VENV=~/.cache/earshot-venv
export EARSHOT_HOME=~/.cache/earshot
if [ ! -d "$SRC/.git" ]; then git clone -q https://github.com/Leonxlnx/earshot "$SRC"; fi
git -C "$SRC" fetch -q origin && git -C "$SRC" checkout -q "$COMMIT"
[ -x "$VENV/bin/python" ] || python3 -m venv "$VENV"
"$VENV/bin/python" -c "import torch" 2>/dev/null || "$VENV/bin/pip" install -q torch --index-url https://download.pytorch.org/whl/cpu
"$VENV/bin/pip" install -q -e "$SRC[mcp]"
if [ "${1:-}" != "--no-models" ]; then "$VENV/bin/python" -m earshot doctor --fetch >/dev/null; fi
"$VENV/bin/python" -m earshot doctor | grep -q '^problems: \[\]' && echo EARSHOT_SETUP_OK
