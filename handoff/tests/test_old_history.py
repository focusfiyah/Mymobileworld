"""After the 2026-10-29 history cleanup, a branch that still carries the old history must never be merged:
branch_sync.missing() returns None for it (shares no history with main) and git itself refuses the merge."""
import importlib.util, os, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]


def run(d, *a, check=True):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True, check=check)


def main():
    d = tempfile.mkdtemp()
    env = {"GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    os.environ.update(env)
    run(d, "init", "-q", "-b", "main")
    Path(d, "a.txt").write_text("old\n"); run(d, "add", "."); run(d, "commit", "-qm", "old root")
    run(d, "branch", "oldwork")                       # a branch on the OLD history
    run(d, "checkout", "-q", "--orphan", "newmain")   # the cleaned history: a different root
    Path(d, "a.txt").write_text("new\n"); run(d, "add", "."); run(d, "commit", "-qm", "new root")
    run(d, "update-ref", "refs/remotes/origin/main", "newmain")
    run(d, "update-ref", "refs/remotes/origin/oldwork", "oldwork")
    spec = importlib.util.spec_from_file_location("bs", HERE / "branch_sync.py"); bs = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bs)
    cwd = os.getcwd(); os.chdir(d)
    try:
        assert bs.missing("origin/oldwork", bs.blobs("origin/main")) is None, "old-history branch not detected"
        m = run(d, "merge", "--no-edit", "oldwork", check=False)
        assert m.returncode != 0 and "unrelated histories" in (m.stderr + m.stdout), "git merged old history"
    finally:
        os.chdir(cwd)
    print("OLD_HISTORY_GUARD_OK")


if __name__ == "__main__":
    main()
