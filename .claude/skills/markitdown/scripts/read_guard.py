#!/usr/bin/env python3
"""PreToolUse hook on Read: documents go through MarkItDown first (Ralph 2026-11-17).

Why: the Diaspo income and expenses session read a PDF with the Read tool instead of converting it,
two days after Ralph made MarkItDown the standard. The rule alone was not enough, so this blocks it.
Allowed: a file md.sh converted (EMPTY = scanned, read as pages) or marked with md.sh --look.
Blocked: any other PDF/Office/EPUB file; the reason tells the session the exact command.
Fails open (exit 0, no output) on anything unexpected so a broken hook never stops work.
"""
import json, os, sys

EXT = {".pdf", ".docx", ".doc", ".pptx", ".ppt", ".xlsx", ".xls", ".epub", ".msg", ".odt", ".ods", ".odp"}
LOG = os.path.expanduser("~/.cache/markitdown/log.tsv")
MD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "md.sh")

def main():
    try:
        data = json.load(sys.stdin)
        path = (data.get("tool_input") or {}).get("file_path") or ""
        tool = data.get("tool_name") or ""
    except Exception:
        return
    if tool.endswith("read_file_content"):   # Drive connector: no file type in the call, so remind, never block
        print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse", "additionalContext":
              "MarkItDown rule: if this Drive file is a PDF, Word, PowerPoint or Excel file, download it "
              f"(download_file_content) and convert it with: bash {MD} FILE OUT.md, then read OUT.md. "
              "Google Docs, Sheets and Slides may be read directly."}}))
        return
    if os.path.splitext(path)[1].lower() not in EXT:
        return
    real = os.path.realpath(path)
    seen = {}
    try:
        for line in open(LOG, encoding="utf-8"):
            p = line.rstrip("\n").split("\t")
            if len(p) >= 3:
                seen[p[1]] = (p[0], p[2])
    except OSError:
        pass
    status, out = seen.get(real, (None, None))
    if status in ("EMPTY", "LOOK"):
        return
    if status == "OK":
        why = f"This document was already converted. Read the Markdown instead: {out}"
    else:
        base = os.path.splitext(real)[0] + ".md"
        why = (f"Standard rule (Ralph 2026-11-15/17): documents are converted with MarkItDown before reading. "
               f"Run: bash {MD} \"{real}\" \"{base}\" then Read {base}. "
               f"Scanned PDF (MD_EMPTY) may then be read as pages. To check how a PDF looks (layout), "
               f"run: bash {MD} --look \"{real}\" \"<reason>\" first.")
    print(json.dumps({"hookSpecificOutput": {"hookEventName": "PreToolUse",
                      "permissionDecision": "deny", "permissionDecisionReason": why}}))

if __name__ == "__main__":
    main()
