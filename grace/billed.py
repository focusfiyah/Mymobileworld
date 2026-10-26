"""What Kie actually billed per task (Ralph 2026-10-26, from Sabrina Ramonov's /generate skill email: log the real
charge, not the quote). Kie's recordInfo returns creditsConsumed (1 credit = $0.005; 0 for failed tasks), back to our
first task (2026-10-01, tested 2026-10-26). grace/spend.py prefers these figures over its list prices, so the monthly
cap and every job's budget lock count real money.

  python3 grace/billed.py            fetch every logged task not yet in grace/billed.json
  python3 grace/billed.py --stats    billed vs list price per model (no network)

Cache grace/billed.json: {taskId: {"credits": x, "state": "success"|"fail", "model": m}}. Only finished tasks are
cached. SPEND_OFFLINE=1 skips the network (tests).
"""
import glob, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "grace" / "billed.json"
API = "https://api.kie.ai/api/v1/jobs/recordInfo"
LOGS = ("ugc/**/kie_log.json", "ugc/**/omni_log.json", "fungix/**/kie_log.json", "ugc/**/paid_tasks.json")
USD_PER_CREDIT = 0.005


def load():
    try:
        return json.loads(CACHE.read_text())
    except (OSError, ValueError):
        return {}


def usd(task_id, cache=None):
    """Billed USD for a task, or None when Kie's figure is not cached."""
    e = (cache if cache is not None else load()).get(task_id)
    return None if e is None else round(float(e.get("credits") or 0) * USD_PER_CREDIT, 4)


def logged_ids():
    ids = set()
    for pat in LOGS:
        for f in glob.glob(str(ROOT / pat), recursive=True):
            try:
                data = json.loads(Path(f).read_text())
            except (OSError, ValueError):
                continue
            for e in data if isinstance(data, list) else []:   # "submitted" = a task whose run died before logging it
                tid = isinstance(e, dict) and (e.get("taskId") or e.get("submitted"))
                if isinstance(tid, str) and tid:
                    ids.add(tid)
    return ids


def _fetch(tid):
    import requests
    for attempt in range(3):
        try:
            d = (requests.get(API, params={"taskId": tid}, timeout=20).json() or {}).get("data") or {}
            if d.get("state") in ("success", "fail") and d.get("creditsConsumed") is not None:
                return tid, {"credits": float(d["creditsConsumed"]), "state": d["state"], "model": d.get("model")}
            return tid, None              # still running, or no record
        except Exception:
            time.sleep(2 ** attempt)
    return tid, None


def refresh(limit_s=120, quiet=False):
    """Fetch uncached task ids (8 at a time). Returns how many were added. Never raises."""
    if os.environ.get("SPEND_OFFLINE"):
        return 0
    cache = load(); todo = sorted(logged_ids() - set(cache))
    if not todo:
        return 0
    added, t0 = 0, time.time()
    try:
        with ThreadPoolExecutor(8) as ex:
            for tid, e in ex.map(_fetch, todo):
                if e:
                    cache[tid] = e; added += 1
                if time.time() - t0 > limit_s:
                    break
    except Exception as e:   # no network: list prices stay in use
        print(f"BILLED: refresh failed ({e}); spend uses list prices for {len(todo)} task(s)", file=sys.stderr)
    if added:
        CACHE.write_text(json.dumps(cache, indent=0, sort_keys=True))
    if not quiet:
        print(f"BILLED: {added} new of {len(todo)} uncached task(s); cache holds {len(cache)}", file=sys.stderr)
    return added


def stats():
    sys.path.insert(0, str(ROOT / "grace")); from spend import price
    cache, rows = load(), {}
    for pat in LOGS:
        for f in glob.glob(str(ROOT / pat), recursive=True):
            for e in json.loads(Path(f).read_text()) if f else []:
                if isinstance(e, dict) and e.get("taskId") in cache and isinstance(e.get("request"), dict):
                    m = e["request"].get("model"); r = rows.setdefault(m, [0, 0.0, 0.0])
                    r[0] += 1; r[1] += usd(e["taskId"], cache); r[2] += 0 if e.get("fail") else price(e["request"])[1]
    for m, (n, b, l) in sorted(rows.items(), key=lambda x: -x[1][1]):
        print(f"  {m:40s} n={n:4d} billed ${b:8.2f}  list ${l:8.2f}")


if __name__ == "__main__":
    if "--stats" in sys.argv:
        stats()
    else:
        refresh(limit_s=600)
