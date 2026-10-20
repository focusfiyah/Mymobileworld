#!/usr/bin/env python3
"""Checks for houseoframeau/GATES_r3.md (looser-wording default + House of Rameau AI/sales facts)."""
import json, os, re, sys
R = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(os.path.dirname(R), "Dayone-ai")
HANDOFF = ["MEMORY_SHORT.txt", "GLOBAL_MEMORY.md", "CLAUDE_PREFERENCES.txt", "REMEMBER_ME.txt", "REMEMBER_ME_paste.txt"]


def fail(m):
    print("FAIL", m); sys.exit(1)


def wording():
    files = ["grace/hooks/HOOKS.md", "grace/PLAYBOOK.md", "CLAUDE.md"] + ["handoff/" + f for f in HANDOFF]
    bad = re.compile(r"(said word for word|hooks?[^.\n]{0,60}(word for word|verbatim))", re.I)
    for f in files:
        for i, line in enumerate(open(os.path.join(R, f)), 1):
            if bad.search(line) and not re.search(r"not word for word|replaces the 2026-10-05 word-for-word|^- 2026-10-0\d", line):
                fail(f"{f}:{i}: {line.strip()[:120]}")
    if "looser wording" not in open(os.path.join(R, "grace/hooks/HOOKS.md")).read():
        fail("HOOKS.md has no looser-wording rule")
    print("PASS wording")


def handoff():
    s = open(os.path.join(R, "handoff/MEMORY_SHORT.txt")).read()
    if len(s) > 2000:
        fail(f"MEMORY_SHORT {len(s)} chars")
    for f in HANDOFF:
        if open(os.path.join(R, "handoff", f)).read() != open(os.path.join(D, "handoff", f)).read():
            fail(f"{f} differs between repos")
    if open(os.path.join(R, "handoff/REMEMBER_ME.txt")).read() != open(os.path.join(R, "handoff/REMEMBER_ME_paste.txt")).read():
        fail("REMEMBER_ME_paste differs from REMEMBER_ME")
    print("PASS handoff")


def hor():
    vs = json.load(open(os.path.join(R, "houseoframeau/videos.json")))["videos"]
    ours = {v["id"] for v in vs if v.get("made_by_us_ai")}
    want = {"7687423934299393310", "7685866438472568095", "7685441537894780190", "7685219777308151070", "7682613984255560990"}
    if ours != want:
        fail(f"AI set {sorted(ours)}")
    sold = {v["id"]: v.get("sales") for v in vs if v["shop_video"]}
    if sold.pop("7685441537894780190") != 1 or any(x != 0 for x in sold.values()):
        fail(f"sales {sold}")
    print("PASS hor")


globals()[sys.argv[1]]()
