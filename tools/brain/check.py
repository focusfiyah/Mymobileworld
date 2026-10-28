"""Brain check (Ralph 2026-10-26: "Make sure you are adding to you brain for easy recall" -> "Make that a standing rule
for every session"). Run before the final reply of every session, after the brain notes are written and pushed:

  python3 tools/brain/check.py --terms "clip check,billed,gpt image"   # words a later session would search for

Checks the Obsidian vault (default /home/user/obsidian-vault, or --vault):
  1. no broken [[wiki links]] anywhere in Brain/;
  2. a Brain/Sessions note for today exists and Brain/Index.md lists it;
  3. every Brain/Jobs note touched today is listed in Brain/Jobs.md and has a "## Status" section;
  4. every Brain note created today is linked from at least one other note (no orphans);
  5. each --terms word or phrase is found in at least one Brain note (case-insensitive): the recall test;
  6. Brain/Active work.md exists and no longer lists this session (Ralph 2026-10-28: every session claims its topic there
     at the start and removes its line at the end). Session id = session_ + $CLAUDE_CODE_REMOTE_SESSION_ID after cse_,
     or --session.
Prints BRAIN_OK or BRAIN_FAIL with each problem; exit 0 / 1. "Today" = notes changed in the working tree or in
commits since local midnight (git), with the session date from --date (default today).
"""
import argparse, datetime, os, re, subprocess, sys
from pathlib import Path

LINK = re.compile(r"\[\[([^\]|#]+)")


def touched(vault, since):
    """Brain notes changed today: commits since midnight + uncommitted + untracked. Returns (all, created)."""
    def git(*a):
        return subprocess.run(["git", "-C", str(vault), *a], capture_output=True, text=True).stdout.splitlines()
    changed = set(git("log", f"--since={since}", "--name-only", "--pretty=format:", "--", "Brain"))
    created = set(git("log", f"--since={since}", "--diff-filter=A", "--name-only", "--pretty=format:", "--", "Brain"))
    st = git("status", "--porcelain", "--untracked-files=all", "--", "Brain")
    path = lambda l: l[3:].strip('"')                     # git quotes paths that contain spaces
    changed |= {path(l) for l in st}
    created |= {path(l) for l in st if l.startswith("??") or l.startswith("A ")}
    keep = lambda s: {Path(x) for x in s if x.endswith(".md") and (vault / x).exists()}
    return keep(changed), keep(created)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--vault", default="/home/user/obsidian-vault")
    ap.add_argument("--terms", default="", help="comma-separated words a later session would search for")
    ap.add_argument("--date", default=datetime.date.today().isoformat())
    rid = os.environ.get("CLAUDE_CODE_REMOTE_SESSION_ID", "")
    ap.add_argument("--session", default=("session_" + rid.split("cse_", 1)[1]) if rid.startswith("cse_") else "",
                    help="this session's id, as it appears in Brain/Active work.md")
    a = ap.parse_args()
    vault = Path(a.vault); brain = vault / "Brain"
    notes = {p: p.read_text(errors="ignore") for p in brain.rglob("*.md")}
    names = {p.stem for p in notes} | {"CLAUDE"}
    errs = []

    for p, t in notes.items():                                     # 1. links
        for l in LINK.findall(t):
            if l.strip() not in names:
                errs.append(f"broken link [[{l}]] in {p.relative_to(vault)}")

    sessions = [p for p in notes if p.parent.name == "Sessions" and p.stem.startswith(a.date)]   # 2. session log
    if not sessions:
        errs.append(f"no Brain/Sessions note for {a.date}")
    index = notes.get(brain / "Index.md", "")
    for p in sessions:
        if f"[[{p.stem}]]" not in index:
            errs.append(f"Index.md does not list [[{p.stem}]]")

    changed, created = touched(vault, f"{a.date} 00:00")
    jobs_hub = notes.get(brain / "Jobs.md", "")
    for rel in changed:                                            # 3. job notes in the hub, with a status
        p = vault / rel
        if p.parent == brain / "Jobs":
            if f"[[{p.stem}]]" not in jobs_hub:
                errs.append(f"Jobs.md does not list [[{p.stem}]]")
            if "## Status" not in notes.get(p, ""):
                errs.append(f"{rel} has no '## Status' section")

    for rel in created:                                            # 4. no orphans
        p = vault / rel
        if p.name == "Index.md":
            continue
        if not any(f"[[{p.stem}]]" in t for q, t in notes.items() if q != p):
            errs.append(f"{rel} is not linked from any other note")

    for term in [x.strip() for x in a.terms.split(",") if x.strip()]:   # 5. recall test
        if not any(term.lower() in t.lower() for t in notes.values()):
            errs.append(f"recall: '{term}' is in no Brain note")

    active = brain / "Active work.md"                              # 6. active work board
    if not active.exists():
        errs.append("Brain/Active work.md is missing")
    elif a.session and a.session in notes.get(active, ""):
        errs.append(f"Brain/Active work.md still lists {a.session}: remove your line when the work is done")

    print(f"BRAIN_OK ({len(notes)} notes, {len(changed)} changed today, terms found)" if not errs
          else "BRAIN_FAIL:\n  - " + "\n  - ".join(errs))
    return 1 if errs else 0


if __name__ == "__main__":
    sys.exit(main())
