"""Which session branches hold work that never reached main? (Ralph 2026-10-21: rules learned in one session were
missing in the next. The Shnuggle session never saw the flashlight session's voice notes, and the Cleanwaste session
used the Grace voice without the cleanup steps, because each session starts from main and those branches were never
merged.)

  python3 handoff/branch_sync.py            # this repo, branches pushed in the last 14 days
  python3 handoff/branch_sync.py --days 30

Run it at the start of every session (one fetch, a few seconds) and merge what it lists before relying on CLAUDE.md,
the playbook or the skills. Every job ends with its branch merged into main (CLAUDE.md, "Merging").
Prints SYNC_OK when nothing recent is left unmerged.
"""
import subprocess, sys, time

RULE_FILES = ("CLAUDE.md", "grace/PLAYBOOK.md", "grace/voice/", "handoff/", ".claude/skills/", "skills/", "grace/hooks/")


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True).stdout.strip()


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    git("fetch", "-q", "--prune", "origin")
    since = time.time() - days * 86400; left = 0
    for line in git("for-each-ref", "refs/remotes/origin", "--format=%(committerdate:unix) %(refname:short)").splitlines():
        ts, ref = line.split(" ", 1)
        if ref in ("origin/main", "origin/HEAD", "origin") or int(ts) < since:
            continue
        ahead = git("rev-list", "--count", f"origin/main..{ref}")
        if ahead in ("", "0"):
            continue
        files = git("diff", "--name-only", f"origin/main...{ref}").splitlines()
        rules = [f for f in files if f.startswith(RULE_FILES)]
        left += 1
        print(f"{ref}: +{ahead} commits, {len(files)} files" + (f", RULE FILES: {', '.join(rules[:6])}" if rules else ""))
    print("SYNC_OK" if not left else f"{left} branch(es) not on main: merge them (keep both sides of rule edits, newest rule wins)")


if __name__ == "__main__":
    main()
