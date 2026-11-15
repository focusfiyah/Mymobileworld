#!/usr/bin/env bash
# Convert a document to Markdown with Microsoft MarkItDown (pinned). Installs it on first use.
# Usage: md.sh <file-or-url> [out.md]    (no out.md = print to stdout)
set -euo pipefail
VER=0.1.9
[ $# -ge 1 ] || { echo "usage: md.sh <file-or-url> [out.md]" >&2; exit 2; }
if ! markitdown --version 2>/dev/null | grep -q "$VER"; then
  pip install -q "markitdown[pdf,docx,pptx,xlsx,xls,outlook]==$VER" >&2 2>/dev/null || pip install -q --break-system-packages "markitdown[pdf,docx,pptx,xlsx,xls,outlook]==$VER" >&2
fi
if [ $# -ge 2 ]; then markitdown "$1" -o "$2"; out=$(wc -c < "$2"); else markitdown "$1" | tee /dev/stderr >/dev/null; exit 0; fi
# An image-only (scanned) PDF converts to almost nothing: say so instead of passing on an empty file.
if [ "$out" -lt 40 ]; then echo "MD_EMPTY: $1 gave $out bytes (scanned or image-only?). Read its pages as images instead." >&2; exit 3; fi
echo "MD_OK $2 ($out bytes)" >&2
