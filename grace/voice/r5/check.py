#!/usr/bin/env python3
"""Gates for voice round 5 (grace/winners/GATES_r4.md). Usage: python3 grace/voice/r5/check.py <samples|rule>"""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def fail(m):
    print("FAIL", m); sys.exit(1)


def samples():
    s = json.load(open(os.path.join(HERE, "samples.json")))["samples"]
    if len(s) != 7:
        fail(f"{len(s)} samples, want 7")
    for x in s:
        for k in ["video_id", "link", "product", "seconds", "rt60_est_ms", "music_removed", "file"]:
            if x.get(k) in (None, ""):
                fail(f"{x.get('video_id')} missing {k}")
        if x["seconds"] < 8 or x["music_removed"] is not True:
            fail(f"{x['video_id']} too short or music not removed")
    print("PASS samples", len(s))


def rule():
    files = ["CLAUDE.md", "grace/voice/README.md", "handoff/REMEMBER_ME.txt", "handoff/REMEMBER_ME_paste.txt",
             "handoff/GLOBAL_MEMORY.md", "handoff/CLAUDE_PREFERENCES.txt"]
    for f in files:
        t = open(os.path.join(REPO, f)).read()
        if "she does" not in t or "2026-10-28" not in t:
            fail(f"{f} has no round-5 rule")
    m = open(os.path.join(REPO, "handoff/MEMORY_SHORT.txt")).read()
    if "own VOs feed" not in m or len(m) > 2000:
        fail(f"MEMORY_SHORT rule missing or {len(m)} chars")
    print("PASS rule")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
