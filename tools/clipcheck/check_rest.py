"""Remaining gate checks for the 2026-10-26 job (GPT Image test, Day One formats, saves). Prints one token per check."""
import json, os, subprocess, sys
from pathlib import Path
M, D, S = Path("/home/user/Mymobileworld"), Path("/home/user/Dayone-ai"), Path("/home/user/claude-skills")
what = sys.argv[1]
if what == "gptimage":
    from PIL import Image
    j = M / "ugc/_tests/gpt-image-2-pov"
    w, h = Image.open(j / "still.png").size
    log = json.loads((j / "kie_log.json").read_text())
    done = [e for e in log if e.get("taskId") and e.get("result")]
    billed = json.loads((M / "grace/billed.json").read_text())
    ok = abs(w / h - 9 / 16) < 0.01 and done and done[-1].get("credits") == 10.0 and done[-1]["taskId"] in billed \
        and "RESULTS" in (j / "README.md").read_text().upper()
    print("GPTIMAGE_OK" if ok else f"GPTIMAGE_BAD {w}x{h} {done[-1] if done else None}")
elif what == "formats":
    f = (D / "formats/shorts.md").read_text(); c = (D / "CLAUDE.md").read_text(); r = (D / "handoff/DAILY_ROUTINE.md").read_text()
    p = (D / "produce.py").read_text()
    ok = all(x in f for x in ("## 1. POV", "## 2. Countdown", "$0.05", "$0.205", "never")) and "formats/shorts.md" in c \
        and "formats/shorts.md" in r and 'shot["type"] == "clip"' in p and "def clip_video" in p
    print("FORMATS_OK" if ok else "FORMATS_MISSING")
elif what == "saved":
    files = ["GLOBAL_MEMORY.md", "CLAUDE_PREFERENCES.txt", "REMEMBER_ME.txt", "REMEMBER_ME_paste.txt"]
    ok = all("Clip check" in (M / "handoff" / f).read_text() and (M / "handoff" / f).read_text() == (D / "handoff" / f).read_text() for f in files)
    ok = ok and "Clip check + real Kie cost" in (M / "CLAUDE.md").read_text() and len((M / "handoff/MEMORY_SHORT.txt").read_text()) <= 2000
    ok = ok and not subprocess.run(["diff", "-rq", str(S / "skills/ugc-product-ad"), str(M / ".claude/skills/ugc-product-ad")], capture_output=True).returncode
    print("SAVED_OK" if ok else "SAVED_MISSING")
elif what == "merged":
    bad = []
    for r in (M, D, S):
        subprocess.run(["git", "-C", str(r), "fetch", "-q", "origin", "main"], capture_output=True)
        head = subprocess.run(["git", "-C", str(r), "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
        if subprocess.run(["git", "-C", str(r), "merge-base", "--is-ancestor", head, "origin/main"]).returncode:
            bad.append(r.name)
        if subprocess.run(["git", "-C", str(r), "status", "--porcelain"], capture_output=True, text=True).stdout.strip():
            bad.append(r.name + " (uncommitted)")
    print("MERGED_OK" if not bad else "NOT_MERGED " + " ".join(bad))
