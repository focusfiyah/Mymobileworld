#!/usr/bin/env bash
# Convert a document to Markdown with Microsoft MarkItDown (pinned). Installs it on first use.
# Usage: md.sh <file-or-url> [out.md]        (no out.md = print to stdout)
#        md.sh --look <file> "<reason>"      (allow the Read tool to open this file as pages,
#                                             e.g. to check the layout of a PDF we made)
# Every conversion is logged in ~/.cache/markitdown/log.tsv; read_guard.py (Read hook) checks it.
set -euo pipefail
VER=0.1.9
LOG="$HOME/.cache/markitdown/log.tsv"; mkdir -p "$(dirname "$LOG")"
abs() { python3 -c 'import os,sys;print(os.path.realpath(sys.argv[1]))' "$1"; }
if [ "${1:-}" = "--look" ]; then
  [ $# -ge 3 ] || { echo 'usage: md.sh --look <file> "<reason>"' >&2; exit 2; }
  printf 'LOOK\t%s\t%s\n' "$(abs "$2")" "$3" >> "$LOG"; echo "MD_LOOK_OK $2" >&2; exit 0
fi
[ $# -ge 1 ] || { echo "usage: md.sh <file-or-url> [out.md]" >&2; exit 2; }
if ! markitdown --version 2>/dev/null | grep -q "$VER"; then
  pip install -q "markitdown[pdf,docx,pptx,xlsx,xls,outlook]==$VER" >&2 2>/dev/null || pip install -q --break-system-packages "markitdown[pdf,docx,pptx,xlsx,xls,outlook]==$VER" >&2
fi
if [ $# -lt 2 ]; then markitdown "$1"; exit 0; fi
markitdown "$1" -o "$2"; out=$(tr -d '[:space:]' < "$2" | wc -c)
src="$1"; [ -e "$1" ] && src=$(abs "$1")
# An image-only (scanned) PDF converts to almost nothing: say so instead of passing on an empty file.
if [ "$out" -lt 5 ]; then
  printf 'EMPTY\t%s\t%s\n' "$src" "$(abs "$2")" >> "$LOG"
  echo "MD_EMPTY: $1 gave $out characters (scanned or image-only?). Read its pages as images instead (Read with pages)." >&2; exit 3
fi
printf 'OK\t%s\t%s\n' "$src" "$(abs "$2")" >> "$LOG"
echo "MD_OK $2 ($out characters)" >&2
