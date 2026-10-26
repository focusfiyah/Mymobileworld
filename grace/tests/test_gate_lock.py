"""Tests for the Production Book, the budget lock and the paid-task ledger in grace/gate.py + grace/paid.py.
Builds a throwaway repo with a bare "origin" and a second clone (another session), no network, no paid calls.

  python3 grace/tests/test_gate_lock.py      -> "ALL CHECKS PASSED (n)" or the first failure
"""
import contextlib, importlib, io, json, os, shutil, subprocess, sys, tempfile, time
from pathlib import Path

HERE = Path(__file__).resolve().parents[2]
os.environ.setdefault("SPEND_OFFLINE", "1")   # grace/billed.py: no Kie lookups for the fake task ids
results = []


def ok(name, cond, detail=""):
    results.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else f"  [{detail[:400]}]"))


def sh(cwd, *a):
    r = subprocess.run(a, cwd=cwd, capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{a}: {r.stderr}")
    return r.stdout


def exits(fn, *a, **k):
    """Run fn; return (exited, message+stderr)."""
    err = io.StringIO()
    try:
        with contextlib.redirect_stderr(err):
            fn(*a, **k)
        return False, err.getvalue()
    except SystemExit as e:
        return True, f"{e.code}\n{err.getvalue()}"


def make_repo(tmp):
    remote = tmp / "origin.git"; sh(tmp, "git", "init", "-q", "--bare", "-b", "main", str(remote))
    work = tmp / "a"; sh(tmp, "git", "clone", "-q", str(remote), str(work))
    for w in ("user.name", "user.email"):
        sh(work, "git", "config", w, "test@example.com")
    (work / "grace").mkdir()
    for f in ("gate.py", "paid.py", "spend.py", "billed.py", "kie_fields.py", "kie_fields.json", "prompt_check.py"):
        shutil.copy(HERE / "grace" / f, work / "grace" / f)
    (work / "grace/spend.json").write_text(json.dumps({"monthly_cap_usd": 100, "caps_by_month": {time.strftime("%Y-%m"): None}, "other": []}))
    tpl = work / ".claude/skills/ugc-product-ad/templates"; tpl.mkdir(parents=True)
    shutil.copy(HERE / ".claude/skills/ugc-product-ad/templates/plan-message.md", tpl)
    job = work / "ugc/demo"; (job / "research").mkdir(parents=True)
    (job / "scripts.md").write_text("Hook line. It's in the orange cart.\n")
    old = time.time() - 100; os.utime(job / "scripts.md", (old, old))
    steps = ["playbook", "coach_research", "viral_board", "product_facts", "hooks", "humanizer", "readability", "line_sources", "compare"]
    c = {"scripts": ["scripts.md"], "vo_lines": [], "audience_legacy": True}
    for k in steps:
        (job / "research" / f"{k}.md").write_text("proof\n"); c[k] = {"proof": [f"research/{k}.md"]}
    (job / "checklist.json").write_text(json.dumps(c))
    sh(work, "git", "add", "-A"); sh(work, "git", "commit", "-qm", "init"); sh(work, "git", "push", "-q", "origin", "HEAD:main")
    sh(work, "git", "checkout", "-qb", "session-a"); sh(work, "git", "push", "-q", "-u", "origin", "session-a")
    return remote, work, job


def fill_book(job, total):
    text = (job / "BOOK.md").read_text()
    import re
    text = re.sub(r"_{3,}", "x", text).replace("$__", "$1.00")
    text = re.sub(r"(?m)^TOTAL: \$[\d.]+$", f"TOTAL: ${total}", text)
    (job / "BOOK.md").write_text(text)


def body(prompt, url="https://tempfile.redpandaai.co/a.png"):
    return {"model": "google/gemini-omni-flash-1-1", "input": {"prompt": prompt + " No text.", "image_urls": [url], "aspect_ratio": "9:16"}}


def main():
    tmp = Path(tempfile.mkdtemp(prefix="gatelock_"))
    try:
        remote, work, job = make_repo(tmp)
        sys.path.insert(0, str(work / "grace"))
        gate = importlib.import_module("gate"); paid = importlib.import_module("paid")
        paid.FETCH_EVERY = 0
        os.environ.pop("GATE_REDO", None); os.environ.pop("GATE_NO_PUSH", None)

        # scripts-only: the script gate alone still passes, the book is information
        ok("scripts-only check passes without a book", gate.check(job) == [], str(gate.check(job)))
        r = subprocess.run([sys.executable, str(work / "grace/gate.py"), str(job)], capture_output=True, text=True)
        ok("CLI: GATE OK + BOOK line, exit 0", r.returncode == 0 and "GATE OK" in r.stdout and "BOOK: not ready" in r.stdout, r.stdout + r.stderr)

        # 1. Production Book
        e, m = exits(gate.require, job); ok("paid call refused with no BOOK.md", e and "no Production Book" in m, m)
        subprocess.run([sys.executable, str(work / "grace/gate.py"), str(job), "--book-init"], check=True, capture_output=True)
        e, m = exits(gate.require, job); ok("unfilled template refused (blanks)", e and "blanks" in m, m)
        fill_book(job, "0.70")
        e, m = exits(gate.require, job); ok("filled but unapproved book refused", e and "not approved" in m, m)
        e, m = exits(gate.approve_extra, job, 0.1, "yes", "x"); ok("extra refused before the book is approved", e, m)
        e, m = exits(gate.approve_book, job, "Approved, go"); ok("approve-book records Ralph's OK", not e, m)
        c = json.loads((job / "checklist.json").read_text())["book_ok"]
        ok("approval stores total + text hash + quote", c["total"] == 0.70 and len(c["sha256"]) == 64 and c["quote"] == "Approved, go", str(c))
        e, m = exits(gate.require, job); ok("require passes after approval", not e, m)
        (job / "BOOK.md").write_text((job / "BOOK.md").read_text() + "\nS9 added later\n")
        e, m = exits(gate.require, job); ok("editing BOOK.md after approval voids it", e and "changed after Ralph approved" in m, m)
        exits(gate.approve_book, job, "OK v2")
        ok("re-approval keeps the earlier OK in book_history",
           len(json.loads((job / "checklist.json").read_text()).get("book_history", [])) == 1)

        # 4. prompt check (Ralph 2026-10-25): unread or broken prompts are refused before anything is claimed
        pc = importlib.import_module("prompt_check")
        e, m = exits(gate.start_task, job, body("S1 hand lifts the bottle"), "S1")
        ok("unmarked prompt refused + saved for reading", e and "PROMPT CHECK" in m and "not marked" in m
           and any((job / "proof/pending_prompts").glob("*.txt")), m)
        ok("refused prompt claims nothing", not (job / "paid_tasks.json").exists() or json.loads((job / "paid_tasks.json").read_text()) == [])
        bad = "Recreate image 3 exactly, she walks in her sneakers. No text."
        ok("lint: image number past the refs sent", any("image [3]" in x for x in pc.lint(bad, 1)), str(pc.lint(bad, 1)))
        ok("lint: shoes on a person with no toe direction", any("toe direction" in x for x in pc.lint(bad, 3)))
        ok("lint: chest vs knees framing conflict", any("framing conflict" in x for x in pc.lint(
            "Her face is never in frame: the frame cuts at her chest. Nothing above her knees is in the frame. No text.", 0)))
        ok("lint: negated sparkle is fine, plain sparkle is not",
           pc.lint("A shoe. No added sparkles or glints. No text.") == [] and pc.lint("Sparkle on the shoe. No text.") != [])
        e, m = exits(gate.start_task, job, body(bad), "SX"); ok("lint failure refused even if never marked", e and "lint:" in m, m)
        ok("mark refuses a prompt that fails lint", pc.mark(job, [("SX", bad, 1)]) != [])
        test_prompts = ["S1 hand lifts the bottle", "S2 bottle on the counter", "S3 close-up of the cap", "S5 tablet drops in"]
        ok("mark records clean prompts", pc.mark(job, [(p, p + " No text.", 1) for p in test_prompts]) == [])

        # 3. ledger: saved + pushed at start
        e, m = exits(gate.start_task, job, body("S1 hand lifts the bottle"), "S1"); ok("first paid task allowed", not e, m)
        led = json.loads((job / "paid_tasks.json").read_text())
        ok("claim saved with status started + price $0.315", led[-1]["status"] == "started" and led[-1]["usd"] == 0.315, str(led))
        pushed = subprocess.run(["git", "--git-dir", str(remote), "show", "session-a:ugc/demo/paid_tasks.json"], capture_output=True, text=True)
        ok("claim committed and pushed to the session branch", pushed.returncode == 0 and '"started"' in pushed.stdout, pushed.stderr)
        e, m = exits(gate.start_task, job, body("S1 hand lifts the bottle", url="https://tempfile.redpandaai.co/NEW.png"), "S1")
        ok("same request (new upload URL) refused as a duplicate", e and "already started or paid" in m, m)
        key = led[-1]["key"]
        gate.task_submitted(job, key, "task_S1")
        ok("task_submitted stores the taskId", json.loads((job / "paid_tasks.json").read_text())[-1]["taskId"] == "task_S1")
        e, m = exits(gate.start_task, job, body("S1 hand lifts the bottle"), "S1")
        ok("refusal names the taskId to reuse", e and "GATE_REDO=task_S1" in m, m)

        # 2. budget lock (0.70 allowed): S1 in flight 0.315
        os.environ["GATE_REDO"] = "task_S1"
        e, m = exits(gate.start_task, job, body("S1 hand lifts the bottle"), "S1 redo"); ok("GATE_REDO lets the named redo through", not e, m)
        os.environ.pop("GATE_REDO")
        e, m = exits(gate.start_task, job, body("S2 bottle on the counter"), "S2")
        ok("budget lock refuses a call past the approved total (in-flight counted)", e and "BUDGET LOCK" in m and "$0.95 of the $0.70" in m, m)
        exits(gate.approve_extra, job, 0.30, "ok do S2", "S2")
        e, m = exits(gate.start_task, job, body("S2 bottle on the counter"), "S2"); ok("recorded extra lets it through", not e, m)

        # finished task counted once, not twice (ledger claim + kie_log entry)
        (job / "kie_log.json").write_text(json.dumps([{"t": "x", "request": body("S1 hand lifts the bottle"), "taskId": "task_S1",
                                                       "result": {}, "usd": 0.315}]))
        spent = paid.job_spend(paid.entries(job))
        ok("finished task counted once (0.315 x3 claims, one finished)", abs(spent - 0.945) < 1e-6, str(spent))
        e, m = exits(gate.require, job); ok("vo.py-style require(usd=0) still passes at the limit", not e, m)

        # a new book starts from what was already spent; old extras do not carry over
        (job / "BOOK.md").write_text((job / "BOOK.md").read_text().replace("TOTAL: $0.70", "TOTAL: $0.40"))
        exits(gate.approve_book, job, "redo round OK")
        c = json.loads((job / "checklist.json").read_text())
        ok("new approval records spend so far as its baseline", abs(c["book_ok"]["spent_at_approval"] - 0.945) < 1e-6, str(c["book_ok"]))
        ok("extras of the old book do not count for the new one", abs(gate.allowance(c)[0] - 0.40) < 1e-6, str(gate.allowance(c)))
        e, m = exits(gate.start_task, job, body("S3 close-up of the cap"), "S3"); ok("new round runs inside its own total", not e, m)

        # Vicks: another session (clone B, own branch) already paid for S5; this session must see it
        b = tmp / "b"; sh(tmp, "git", "clone", "-q", "-b", "main", str(remote), str(b))
        for w in ("user.name", "user.email"):
            sh(b, "git", "config", w, "test@example.com")
        sh(b, "git", "checkout", "-qb", "session-b")
        (b / "ugc/demo/kie_log.json").write_text(json.dumps([{"t": "2026-10-01 23:40:00", "request": body("S5 tablet drops in"),
                                                             "taskId": "task_B5", "result": {}}]))
        sh(b, "git", "add", "-A"); sh(b, "git", "commit", "-qm", "B clips"); sh(b, "git", "push", "-q", "origin", "session-b")
        e, m = exits(gate.start_task, job, body("S5 tablet drops in"), "S5")
        ok("request already paid on another session's branch is refused", e and "origin/session-b" in m and "task_B5" in m, m)

        # Kie input fields: a misnamed image field is refused before anything is claimed or sent
        n_before = len(json.loads((job / "paid_tasks.json").read_text()))
        wrong = {"model": "nano-banana-pro", "input": {"prompt": "S6 still", "image_urls": ["https://x/1.png"], "resolution": "1K"}}
        e, m = exits(gate.start_task, job, wrong, "S6")
        ok("nano-banana-pro with image_urls (its field is image_input) refused", e and "KIE FIELDS" in m and "image_input" in m, m)
        ok("refused field check claims nothing", len(json.loads((job / "paid_tasks.json").read_text())) == n_before)
        ok("documented fields pass the field check",
           importlib.import_module("kie_fields").check({**wrong, "input": {"prompt": "S6", "image_input": ["https://x/1.png"]}}) == [])

        # the key ignores hosted URLs anywhere (nano-banana image_input, Omni video_list) but not the prompt
        nb = lambda pr, u: {"model": "nano-banana-pro", "input": {"prompt": pr, "image_input": [u, u], "resolution": "1K"}}
        ok("same still request with new upload URLs has the same key",
           paid.task_key(nb("S1 still", "https://x/1.png")) == paid.task_key(nb("S1 still", "https://y/2.png")))
        ok("a different prompt or setting gets a different key",
           paid.task_key(nb("S1 still", "https://x/1.png")) != paid.task_key(nb("S2 still", "https://x/1.png"))
           and paid.task_key(body("S9")) != paid.task_key({**body("S9"), "input": {**body("S9")["input"], "duration": "6"}}))

        # the copy in this repo is the one under test
        ok("tested copies match grace/", all((work / "grace" / f).read_text() == (HERE / "grace" / f).read_text()
                                             for f in ("gate.py", "paid.py", "spend.py", "billed.py", "kie_fields.py", "kie_fields.json", "prompt_check.py")))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    failed = [n for n, c in results if not c]
    print(f"ALL CHECKS PASSED ({len(results)})" if not failed else f"{len(failed)} of {len(results)} FAILED: {failed}")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
