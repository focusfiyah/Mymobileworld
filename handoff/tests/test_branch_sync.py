"""Tests for handoff/branch_sync.py on a throwaway repo with a bare origin (no network).

  python3 handoff/tests/test_branch_sync.py      -> "ALL CHECKS PASSED (n)" or the failures
"""
import os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "branch_sync.py"
NOW = int(time.time())


def sh(cwd, *a, t=None):
    env = dict(os.environ)
    if t is not None:
        env["GIT_AUTHOR_DATE"] = env["GIT_COMMITTER_DATE"] = f"{NOW - 86400 + t} +0000"
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True, env=env)
    if r.returncode:
        raise RuntimeError(f"{a}: {r.stderr}")
    return r.stdout


def commit(w, files, msg, t):
    for f, text in files.items():
        (w / f).parent.mkdir(parents=True, exist_ok=True); (w / f).write_text(text)
    sh(w, "git", "add", "-A"); sh(w, "git", "commit", "-qm", msg, t=t)


def main():
    tmp = Path(tempfile.mkdtemp(prefix="bsync_"))
    try:
        sh(tmp, "git", "init", "-q", "--bare", "-b", "main", "origin.git")
        w = tmp / "w"; sh(tmp, "git", "clone", "-q", str(tmp / "origin.git"), "w")
        sh(w, "git", "config", "user.name", "t"); sh(w, "git", "config", "user.email", "t@example.com")
        commit(w, {"CLAUDE.md": "rules v1\n", "S.md": "s v1\n", "R.md": "r v1\n"}, "start", 0)
        sh(w, "git", "push", "-q", "origin", "main")
        base = sh(w, "git", "rev-parse", "HEAD").strip()

        def branch(name, files, t):
            sh(w, "git", "checkout", "-q", "-b", name, base); commit(w, files, name, t)
            sh(w, "git", "push", "-q", "origin", name); sh(w, "git", "checkout", "-q", "main")

        branch("br-new", {"ugc/job/notes.md": "new work\n"}, 10)                  # file main never got
        branch("br-ported", {"handoff/rule.txt": "ported rule\n"}, 20)            # main later gets the same text by hand
        branch("br-old", {"R.md": "r branch edit\n"}, 30)                         # main edits R.md after this
        branch("br-newer", {"CLAUDE.md": "rules v1 + branch rule\n"}, 300)        # newer than main's CLAUDE.md edit
        sh(w, "git", "checkout", "-q", "-b", "br-none", base); sh(w, "git", "push", "-q", "origin", "br-none")
        sh(w, "git", "checkout", "-q", "main")
        commit(w, {"handoff/rule.txt": "ported rule\n"}, "port by hand", 40)
        commit(w, {"R.md": "r main edit\n", "CLAUDE.md": "rules v2\n"}, "main moves on", 200)
        sh(w, "git", "push", "-q", "origin", "main")

        out = subprocess.run([sys.executable, str(SCRIPT)], cwd=w, capture_output=True, text=True).stdout
        checks = [
            ("new file listed", "origin/br-new: 1 files main lacks" in out),
            ("branch edit newer than main's listed as a rule file", "origin/br-newer: 1 files main lacks" in out and "RULE FILES: CLAUDE.md" in out),
            ("work ported to main by hand not listed", "br-ported" not in out),
            ("file main edited after the branch not listed", "br-old" not in out),
            ("branch with nothing ahead not listed", "br-none" not in out),
            ("summary counts 2 branches", "2 branch(es) not on main" in out),
        ]
        results = [(n, c) for n, c in checks]
        for n, c in results:
            print(("PASS " if c else "FAIL ") + n)
        failed = [n for n, c in results if not c]
        if failed:
            print(out)
        print(f"ALL CHECKS PASSED ({len(results)})" if not failed else f"{len(failed)} of {len(results)} FAILED")
        return 1 if failed else 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
