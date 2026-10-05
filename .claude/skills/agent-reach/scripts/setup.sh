#!/usr/bin/env bash
# Agent Reach setup (pinned, idempotent, user-level). Safe to re-run at the start of every session.
# Installs: agent-reach CLI (+ yt-dlp) in ~/.agent-reach-venv, mcporter for Exa search, yt-dlp JS runtime.
# Does NOT install the upstream skill, browser-cookie tools or optional platform CLIs (ask Ralph first).
set -euo pipefail
AR_REV="a19a171"          # github.com/Panniantong/Agent-Reach, reviewed 2026-10-05
MCPORTER_VER="0.14.2"     # npm mcporter, reviewed 2026-10-05
VENV="$HOME/.agent-reach-venv"

if [ ! -x "$VENV/bin/agent-reach" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q --disable-pip-version-check "git+https://github.com/Panniantong/Agent-Reach@${AR_REV}"
fi

# Put the commands on PATH (fall back to ~/.local/bin when /usr/local/bin isn't writable)
BIN=/usr/local/bin; [ -w "$BIN" ] || { BIN="$HOME/.local/bin"; mkdir -p "$BIN"; }
for c in agent-reach yt-dlp; do ln -sf "$VENV/bin/$c" "$BIN/$c"; done

# Exa web search through mcporter (needs Node.js)
if command -v npm >/dev/null; then
  command -v mcporter >/dev/null || npm install -g -s "mcporter@${MCPORTER_VER}"
  mcporter config list 2>/dev/null | grep -q '\bexa\b' || mcporter config add exa https://mcp.exa.ai/mcp --scope home >/dev/null
else
  echo "[!] Node.js missing: Exa search unavailable (everything else works)"
fi

# yt-dlp needs a JS runtime for YouTube
mkdir -p "$HOME/.config/yt-dlp"
grep -qxF -- '--js-runtimes node' "$HOME/.config/yt-dlp/config" 2>/dev/null || echo '--js-runtimes node' >> "$HOME/.config/yt-dlp/config"

echo "Agent Reach ready: $("$VENV/bin/agent-reach" --version) (commands in $BIN). Check channels: agent-reach doctor"
