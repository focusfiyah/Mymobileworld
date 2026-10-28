"""Checks for the Acuna ideas job (GATES.md). Usage: python3 verify.py repo|tracker"""
import ast, re, subprocess, sys

VAULT = "/home/user/obsidian-vault/Brain/Jobs/Acuna Ideas Tracker.md"
DM_PATH = "products/ai-on-autopilot/automation/ig_comment_dm.py"


def repo():
    subprocess.run(["git", "-C", "/home/user/Dayone-ai", "fetch", "-q", "origin", "main"], check=True)
    src = subprocess.run(["git", "-C", "/home/user/Dayone-ai", "show", f"origin/main:{DM_PATH}"],
                         check=True, capture_output=True, text=True).stdout
    ast.parse(src)
    assert '"fields": "id,text,username,from,' in src, "comments call does not ask for 'from'"
    assert 'c.get("username") == OWN' not in src, "own-comment check still uses the empty username"
    assert src.count("_user(c)") >= 5, "commenter not read through _user()"
    print("REPO_OK")


def tracker():
    s = open(VAULT).read()
    rows = re.findall(r"^\| ([1-7]) \|", s, re.M)
    assert sorted(rows) == list("1234567"), f"tracker rows {rows}"
    assert re.search(r"^\| 1 \|.*\| DONE 2026-10-28", s, re.M), "item 1 not marked done"
    print("TRACKER_OK")


if __name__ == "__main__":
    {"repo": repo, "tracker": tracker}[sys.argv[1]]()
