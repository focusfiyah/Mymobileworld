#!/usr/bin/env python3
"""Claim Telegram updates so only ONE session ever acts on a message.

Why (Ralph 2026-11-06, "So let's make sure that doesn't happen"): Grace's stocking
stuffer request (updates 786406544-546) was picked up by two sessions at once
(the on-demand "Telegram task check" and the outfit-edits session, which polls
Telegram for Grace's notes). getUpdates keeps returning a message until it is
acknowledged, and both acknowledged only after spawning, so each started its own
session: Grace got two info lists, Drive got duplicate files, the asset index
was edited twice.

How: a claim is a file claims/<update_id>.json on the branch `telegram-claims`
of this repo, written with one git push. A git push that is not a fast-forward
is refused, so two sessions racing for the same update cannot both win: the
loser refetches, sees the claim and backs off. All update ids in one call are
claimed together or not at all.

Usage (run from anywhere inside the Mymobileworld clone):
  python3 tools/telegram/claim.py claim 786406544 786406545 --session <session_id> --topic "Stocking Stuffer Finds"
      -> CLAIM_OK            you own them: act, then acknowledge with getUpdates offset
      -> CLAIMED_BY <session> <topic> (exit 3)   someone else owns at least one: do NOT act
  python3 tools/telegram/claim.py status 786406544 [...]
      -> one line per id: FREE or CLAIMED_BY <session> <topic> <time>
  python3 tools/telegram/claim.py selftest
      -> SELFTEST_OK (claims two fake ids, checks a second claim is refused, removes nothing:
         test ids are 1000000000+ and never real updates)
"""
import json, os, subprocess, sys, tempfile, time, datetime

BRANCH = "telegram-claims"
REMOTE = "origin"


def git(*args, env=None, check=True, inp=None):
    r = subprocess.run(["git", *args], capture_output=True, text=True, env=env, input=inp)
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {r.stderr.strip()}")
    return r


def fetch():
    """Fetch the claims branch. Returns its commit sha, or None if it does not exist yet."""
    r = git("fetch", "-q", REMOTE, f"+refs/heads/{BRANCH}:refs/remotes/{REMOTE}/{BRANCH}", check=False)
    if r.returncode != 0:
        if "couldn't find remote ref" in r.stderr or "not found" in r.stderr.lower():
            return None
        raise RuntimeError(f"fetch failed: {r.stderr.strip()}")
    return git("rev-parse", f"refs/remotes/{REMOTE}/{BRANCH}").stdout.strip()


def read_claim(tip, uid):
    if not tip:
        return None
    r = git("show", f"{tip}:claims/{uid}.json", check=False)
    if r.returncode != 0:
        return None
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"session": "?", "topic": "unreadable claim file"}


def claim(uids, session, topic):
    for attempt in range(6):
        tip = fetch()
        taken = [(u, read_claim(tip, u)) for u in uids]
        taken = [(u, c) for u, c in taken if c]
        if taken:
            mine = all(c.get("session") == session for _, c in taken)
            if mine and len(taken) == len(uids):
                print("CLAIM_OK (already yours)")
                return 0
            if not mine:
                u, c = next((u, c) for u, c in taken if c.get("session") != session)
                print(f"CLAIMED_BY {c.get('session')} {c.get('topic','')!r} (update {u}, {c.get('at','')})")
                return 3
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        with tempfile.TemporaryDirectory() as td:
            env = dict(os.environ, GIT_INDEX_FILE=os.path.join(td, "index"))
            if tip:
                git("read-tree", tip, env=env)
            else:
                git("read-tree", "--empty", env=env)
            for u in uids:
                body = json.dumps({"update_id": u, "session": session, "topic": topic, "at": now}, indent=1) + "\n"
                blob = git("hash-object", "-w", "--stdin", inp=body).stdout.strip()
                git("update-index", "--add", "--cacheinfo", f"100644,{blob},claims/{u}.json", env=env)
            tree = git("write-tree", env=env).stdout.strip()
            cenv = dict(os.environ, GIT_AUTHOR_NAME="Claude", GIT_AUTHOR_EMAIL="noreply@anthropic.com",
                        GIT_COMMITTER_NAME="Claude", GIT_COMMITTER_EMAIL="noreply@anthropic.com")
            msg = f"claim telegram {','.join(map(str, uids))} for {session}: {topic}"
            parent = ["-p", tip] if tip else []
            commit = git("commit-tree", tree, *parent, "-m", msg, env=cenv).stdout.strip()
        r = git("push", "-q", REMOTE, f"{commit}:refs/heads/{BRANCH}", check=False)
        if r.returncode == 0:
            print("CLAIM_OK")
            return 0
        # Rejected: someone pushed first (or a network blip). Refetch and look again.
        time.sleep(2 * (attempt + 1))
    print("CLAIM_ERROR: could not push the claim after 6 tries; do NOT act, tell Ralph")
    return 2


def status(uids):
    tip = fetch()
    for u in uids:
        c = read_claim(tip, u)
        print(f"{u} FREE" if not c else f"{u} CLAIMED_BY {c.get('session')} {c.get('topic','')!r} {c.get('at','')}")
    return 0


def selftest():
    base = 1000000000 + int(time.time()) % 100000000
    a, b = base, base + 1
    out = subprocess.run([sys.executable, __file__, "claim", str(a), str(b), "--session", "selftest_A", "--topic", "selftest"],
                         capture_output=True, text=True)
    if "CLAIM_OK" not in out.stdout:
        print("SELFTEST_FAIL first claim:", out.stdout, out.stderr); return 1
    out2 = subprocess.run([sys.executable, __file__, "claim", str(b), "--session", "selftest_B", "--topic", "selftest"],
                          capture_output=True, text=True)
    if out2.returncode != 3 or "CLAIMED_BY selftest_A" not in out2.stdout:
        print("SELFTEST_FAIL second claim was not refused:", out2.stdout, out2.stderr); return 1
    out3 = subprocess.run([sys.executable, __file__, "claim", str(a), "--session", "selftest_A", "--topic", "selftest"],
                          capture_output=True, text=True)
    if "CLAIM_OK" not in out3.stdout:
        print("SELFTEST_FAIL re-claim by owner:", out3.stdout); return 1
    print(f"SELFTEST_OK (ids {a},{b}: first claim won, rival refused, owner re-claim ok)")
    return 0


def main(argv):
    if not argv or argv[0] not in ("claim", "status", "selftest"):
        print(__doc__); return 1
    cmd, rest = argv[0], argv[1:]
    if cmd == "selftest":
        return selftest()
    session = topic = None
    uids = []
    i = 0
    while i < len(rest):
        if rest[i] == "--session":
            session = rest[i + 1]; i += 2
        elif rest[i] == "--topic":
            topic = rest[i + 1]; i += 2
        else:
            uids.append(int(rest[i])); i += 1
    if not uids:
        print("give at least one update id"); return 1
    if cmd == "status":
        return status(uids)
    if not session:
        print("--session <your session id> is required (get_session shows it)"); return 1
    return claim(uids, session, topic or "")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
