"""Paid-task ledger (Ralph 2026-10-22, from Video Factory: "every paid task is saved the moment it starts").
Why: Vicks (2026-10-01) paid for its 6 clips twice ($1.07) because a second session never saw the first one's takes.

Runners do not call this directly: grace/gate.py start_task() / task_submitted() wrap it (script gate + book + budget
lock first). For each paid Kie request:
  1. claim(): refuse when the same request (model + prompt + settings; hosted image URLs are ignored because every
     upload gets a new one) was already started or paid in this job folder or in the job's folder on ANY session
     branch (paid_tasks.json and kie_log.json), unless GATE_REDO names that task (Ralph's redo OK comes first).
     Then save {key, model, label, usd, status: started} to JOB/paid_tasks.json and commit + push that one file
     so every other session sees it.
  2. submitted(): add the Kie taskId (or status not_submitted when createTask failed; Kie charged nothing).
GATE_NO_PUSH=1 keeps the claim local (tests, offline work). A failed fetch or push is printed, never silent.
"""
import datetime, hashlib, json, os, subprocess, sys, time, uuid
from contextlib import contextmanager
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from spend import entry_usd

LEDGER = "paid_tasks.json"
LOGS = ("kie_log.json", "omni_log.json")
FETCH_EVERY = 60          # seconds; parallel clips in one run share one fetch
BRANCH_DAYS = 45          # session branches older than this are not scanned
_fetched = [0.0]


def _no_urls(v):
    """Hosted files get a new URL on every upload, so URLs are left out of the key (their count stays in)."""
    if isinstance(v, str):
        return "<url>" if v.startswith(("http://", "https://")) else v
    if isinstance(v, list):
        return [_no_urls(x) for x in v]
    if isinstance(v, dict):
        return {k: _no_urls(x) for k, x in v.items() if k != "callBackUrl"}
    return v


def task_key(body):
    return hashlib.sha1(json.dumps({"model": body.get("model"), **_no_urls(body.get("input") or {})},
                                   sort_keys=True).encode()).hexdigest()[:16]


def _git(repo, *a):
    return subprocess.run(["git", "-C", str(repo), *a], capture_output=True, text=True, timeout=120)


def _repo(job):
    r = _git(job, "rev-parse", "--show-toplevel")
    return Path(r.stdout.strip()) if r.returncode == 0 else None


def _read(f):
    try:
        data = json.loads(Path(f).read_text())
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []


@contextmanager
def _lock(job):
    """One writer at a time per repo: parallel clips must not race on the ledger, the git index or the push."""
    repo = _repo(job)
    lf = Path(_git(repo, "rev-parse", "--absolute-git-dir").stdout.strip()) / "paid_tasks.lock" if repo else job / ".paid_tasks.lock"
    try:
        import fcntl
    except ImportError:       # Windows: no lock (paid runs happen in the cloud container)
        yield; return
    with open(lf, "w") as fh:
        fcntl.flock(fh, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(fh, fcntl.LOCK_UN)


def entries(job):
    """(where, entry) from the job's ledger and logs here and on every recent session branch."""
    job = Path(job).resolve(); out = []
    for name in (LEDGER, *LOGS):
        out += [("this folder", e) for e in _read(job / name)]
    repo = _repo(job)
    if not repo:
        return out
    if time.time() - _fetched[0] > FETCH_EVERY:
        f = _git(repo, "fetch", "-q", "origin")
        if f.returncode:
            print(f"PAID LEDGER: git fetch failed, checking the branches as last fetched: {f.stderr.strip()[:200]}", file=sys.stderr)
        _fetched[0] = time.time()
    rel = job.relative_to(repo).as_posix(); since = time.time() - BRANCH_DAYS * 86400
    for line in _git(repo, "for-each-ref", "--format=%(refname:short) %(committerdate:unix)", "refs/remotes/origin").stdout.splitlines():
        ref, _, ts = line.rpartition(" ")
        if ref in ("origin", "origin/HEAD") or not ts.isdigit() or int(ts) < since:
            continue
        for name in (LEDGER, *LOGS):
            r = _git(repo, "show", f"{ref}:{rel}/{name}")
            if r.returncode == 0:
                try:
                    data = json.loads(r.stdout)
                except ValueError:
                    continue
                out += [(ref, e) for e in data if isinstance(e, dict)] if isinstance(data, list) else []
    return out


def job_spend(ents):
    """USD this job has paid or has in flight, across sessions: finished tasks once each (by taskId) + ledger claims
    whose task has not finished yet."""
    done, finished = {}, set()
    for _, e in ents:
        tid = e.get("taskId")
        if tid and ("result" in e or "fail" in e or "usd" in e) and isinstance(e.get("request"), dict):
            finished.add(tid); done[tid] = entry_usd(e)
    seen, inflight = set(), 0.0
    for _, e in ents:
        if "key" not in e or e.get("status") == "not_submitted":
            continue
        ident = e.get("id") or (e["key"], e.get("t"))
        if ident in seen or (e.get("taskId") and e["taskId"] in finished):
            continue
        seen.add(ident); inflight += float(e.get("usd") or 0)
    return round(sum(done.values()) + inflight, 4)


def duplicates(ents, key):
    hits, seen = [], set()
    for where, e in ents:
        if e.get("key") == key and e.get("status") != "not_submitted":
            hit = {"where": where, "taskId": e.get("taskId"), "t": e.get("t"), "label": e.get("label", ""), "note": "claimed",
                   "id": e.get("id") or (key, e.get("t"))}
        elif isinstance(e.get("request"), dict) and e.get("taskId") and task_key(e["request"]) == key:
            hit = {"where": where, "taskId": e["taskId"], "t": e.get("t"), "label": "", "id": e["taskId"],
                   "note": "failed, $0" if e.get("fail") else "paid"}
        else:
            continue
        ident = hit["taskId"] or hit["id"]
        if ident not in seen:
            seen.add(ident); hits.append(hit)
    return hits


def _publish(job, msg):
    if os.environ.get("GATE_NO_PUSH"):
        return
    repo = _repo(job)
    if not repo:
        return
    path = (Path(job).resolve() / LEDGER).relative_to(repo).as_posix()
    branch = _git(repo, "rev-parse", "--abbrev-ref", "HEAD").stdout.strip()
    steps = [("add", "--", path), ("commit", "-q", "--only", "-m", msg, "--", path), ("push", "-q", "origin", f"HEAD:{branch}")]
    for step in steps:
        r = _git(repo, *step)
        if r.returncode:
            print(f"PAID LEDGER: git {step[0]} failed, other sessions will NOT see this claim: {(r.stderr or r.stdout).strip()[:200]}",
                  file=sys.stderr)
            return


def _save(job, update):
    f = Path(job) / LEDGER; data = _read(f); update(data)
    f.write_text(json.dumps(data, indent=1))


def claim(job, body, usd, label="", check=None):
    """Refuse a repeat, run check(spend_so_far) (the budget lock), then save + push the claim. Returns the key."""
    job = Path(job).resolve(); key = task_key(body)
    with _lock(job):
        ents = entries(job)
        redo = {x.strip() for x in os.environ.get("GATE_REDO", "").split(",") if x.strip()}
        hits = [h for h in duplicates(ents, key) if (h["taskId"] or key) not in redo]
        if hits:
            lines = [f"{h['note']} {h['t']} {h['label']} task {h['taskId'] or '(not submitted yet)'} in {h['where']}" for h in hits]
            name = hits[-1]["taskId"] or key
            sys.exit("PAID LEDGER: this exact request was already started or paid:\n  - " + "\n  - ".join(lines) +
                     f"\nFetch that result (recordInfo?taskId=...) instead of paying again. Only after Ralph OKs a redo"
                     f" with its cost: rerun with GATE_REDO={name}")
        errs = check(job_spend(ents)) if check else []
        if errs:
            sys.exit("BUDGET LOCK: paid call refused:\n  - " + "\n  - ".join(errs))
        t = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        _save(job, lambda d: d.append({"t": t, "id": uuid.uuid4().hex[:12], "key": key, "model": body.get("model"), "label": label, "usd": round(usd, 4),
                                       "status": "started", "session": os.environ.get("CLAUDE_CODE_SESSION_ID", "")}))
        _publish(job, f"paid task started: {job.name} {label or key} {body.get('model')} ${usd:.3f}")
    return key


def submitted(job, key, task_id):
    job = Path(job).resolve()

    def upd(data):
        for e in reversed(data):
            if e.get("key") == key and e.get("status") == "started":
                e.update({"taskId": task_id, "status": "submitted"} if task_id else {"status": "not_submitted"}); break
    with _lock(job):
        _save(job, upd)
        _publish(job, f"paid task {'submitted ' + task_id if task_id else 'not submitted'}: {job.name} {key}")
