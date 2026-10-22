"""G5: this session's branch is merged into origin/main and pushed, in every repo it changed."""
import subprocess
from pathlib import Path

H = Path(__file__).resolve().parents[3]
bad = []
for repo in ("Mymobileworld", "claude-skills", "Dayone-ai"):
    g = lambda *a: subprocess.run(["git", "-C", str(H / repo), *a], capture_output=True, text=True)
    g("fetch", "-q", "origin")
    if g("merge-base", "--is-ancestor", "HEAD", "origin/main").returncode: bad.append(f"{repo}: HEAD not on origin/main")
    if g("status", "--porcelain", "--untracked-files=no").stdout.strip(): bad.append(f"{repo}: uncommitted changes")
print("MERGED OK" if not bad else f"NOT MERGED: {bad}")
