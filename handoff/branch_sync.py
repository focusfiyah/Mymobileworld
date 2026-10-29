"""Which session branches hold work that never reached main? (Ralph 2026-10-21: rules learned in one session were
missing in the next. The Shnuggle session never saw the flashlight session's voice notes, and the Cleanwaste session
used the Grace voice without the cleanup steps, because each session starts from main and those branches were never
merged.)

  python3 handoff/branch_sync.py            # this repo, branches pushed in the last 14 days
  python3 handoff/branch_sync.py --days 30

Run it at the start of every session (one fetch, a few seconds) and merge what it lists before relying on CLAUDE.md,
the playbook or the skills. Every job ends with its branch merged into main (CLAUDE.md, "Merging").
Prints SYNC_OK when nothing recent is left unmerged.

It compares content, not commits (Ralph 2026-10-24: 29 branches were listed although main already had all their
work; it was ported by hand or re-made later, so the commits never showed as merged). A file the branch changed
counts as missing from main only when main still has the version the branch started from, or when the branch's last
edit of it is newer than main's (newest edit wins, as in the merge rule). Files identical on main, and files main
edited after the branch did, are left out.

Files Ralph decided NOT to merge are listed in handoff/branch_sync_declined.txt of the repo being checked (one path or
folder prefix per line, # notes allowed) and never come up again (Ralph 2026-10-25: "no merge, once again you took care
of the merge in a previous session and mentioned it would not come up again"). Add a line every time he says no.
"""
import subprocess, sys, time

RULE_FILES = ("CLAUDE.md", "grace/PLAYBOOK.md", "grace/voice/", "handoff/", ".claude/skills/", "skills/", "grace/hooks/")


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, text=True, errors="replace").stdout.strip()


def blobs(commit):
    """{path: blob id} for every file in a commit (one call instead of one per file)."""
    out = {}
    for line in git("ls-tree", "-r", commit).splitlines():
        meta, path = line.split("\t", 1)
        out[path] = meta.split()[2]
    return out


def last_edit(base, ref, path):
    t = git("log", "-1", "--format=%ct", f"{base}..{ref}", "--", path)
    return int(t) if t else 0


def declined():
    """Path prefixes Ralph said not to merge (handoff/branch_sync_declined.txt in the checked repo)."""
    f = git("rev-parse", "--show-toplevel") + "/handoff/branch_sync_declined.txt"
    try:
        lines = open(f).read().splitlines()
    except OSError:
        return ()
    return tuple(l.split("#", 1)[0].strip() for l in lines if l.split("#", 1)[0].strip())


def missing(ref, main_blobs, skip=()):
    """Files whose change on ref is not on main, or None when ref shares no history with main."""
    base = git("merge-base", "origin/main", ref)
    if not base:
        return None
    ref_blobs, base_blobs = blobs(ref), blobs(base)
    out = []
    for f in git("diff", "--name-only", base, ref).splitlines():
        b, m, o = ref_blobs.get(f), main_blobs.get(f), base_blobs.get(f)
        if b == m or (skip and f.startswith(skip)):
            continue                      # main already has this exact version
        if m == o or last_edit(base, ref, f) > last_edit(base, "origin/main", f):
            out.append(f)                 # main never took the change, or the branch's edit is the newer one
    return out


def main():
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 14
    git("fetch", "-q", "--prune", "origin")
    since = time.time() - days * 86400; left = unrelated = 0
    main_blobs = blobs("origin/main"); skip = declined()
    for line in git("for-each-ref", "refs/remotes/origin", "--format=%(committerdate:unix) %(refname:short)").splitlines():
        ts, ref = line.split(" ", 1)
        if ref in ("origin/main", "origin/HEAD", "origin") or int(ts) < since:
            continue
        ahead = git("rev-list", "--count", f"origin/main..{ref}")
        if ahead in ("", "0"):
            continue
        files = missing(ref, main_blobs, skip)
        if files is None:
            unrelated += 1
            print(f"{ref}: OLD HISTORY (shares no history with main, e.g. from before the 2026-10-29 media cleanup): "
                  "never merge it; copy its non-media files onto a fresh branch from main by hand")
            continue
        if not files:
            continue
        rules = [f for f in files if f.startswith(RULE_FILES)]
        left += 1
        print(f"{ref}: {len(files)} files main lacks (+{ahead} commits)" + (f", RULE FILES: {', '.join(rules[:6])}" if rules else ""))
    if unrelated:
        print(f"({unrelated} branch(es) share no history with main and were skipped)")
    print("SYNC_OK" if not left else f"{left} branch(es) not on main: merge them (keep both sides of rule edits, newest rule wins)")


if __name__ == "__main__":
    main()
