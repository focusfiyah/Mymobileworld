"""Kie helpers for the Youtheory Collagen Liquid ad (copied from ugc/lgxnds-creatine): upload, run_task (script gate first), fetch. Each paid step writes a preview to approve before the next one.


Key: KIE_API_KEY env var, or none if the environment proxy injects it for api.kie.ai. Every request and
response goes to kie_log.json. Failed Kie tasks cost $0.
"""
import hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path
import requests


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); import gate; return gate, _h.parent



API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"


KEY = os.environ.get("KIE_API_KEY")
HDR = {"Authorization": f"Bearer {KEY}"} if KEY else {}
LOG = Path("kie_log.json")
CACHE = Path("upload_cache.json")


_LOCK = threading.Lock()


def log(entry):
    with _LOCK:  # clips run in parallel threads
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **entry})
        LOG.write_text(json.dumps(data, indent=1))


def upload(path):
    """Host a local file on Kie. Cache keyed on path+size+mtime so a regenerated still never reuses an old URL."""
    p = Path(path); st = p.stat()
    k = f"{p}|{st.st_size}|{st.st_mtime_ns}"
    with _LOCK:   # parallel clips read/write the cache at once (S7 crashed on a half-written file, 2026-10-21)
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if k in cache:
        return cache[k]
    for attempt in range(4):
        r = requests.post(UPLOAD, headers=HDR, files={"file": (p.name, p.read_bytes())},
                          data={"uploadPath": "youtheory-collagen"}, timeout=120)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"):
            break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    # pre-flight: the hosted file must be byte-identical to the local one
    if hashlib.sha256(requests.get(url, timeout=60).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs from the local file; not submitting")
    with _LOCK:
        cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
        cache[k] = url; CACHE.write_text(json.dumps(cache, indent=1))
    return url


def run_task(body, label=""):
    gate, job = _gate()   # script gate + cap + approved BOOK.md + budget lock + paid-task ledger (Ralph 2026-10-22)
    key = gate.start_task(job, body, label=label)
    for attempt in range(4):  # Kie answers 500 "server is busy" under load; an immediate retry works
        r = requests.post(f"{API}/createTask", headers=HDR, json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid:
            break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        gate.task_submitted(job, key, None)
        log({"request": body, "response": resp}); sys.exit("createTask failed")
    gate.task_submitted(job, key, tid)
    log({"submitted": tid, "prompt": body["input"].get("prompt", "")[:120]})  # recoverable via recordInfo if this run dies
    print("submitted", tid, flush=True)
    deadline = time.time() + 600
    while time.time() < deadline:
        d = (requests.get(f"{API}/recordInfo", headers=HDR, params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") == "success":
            rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            log({"request": body, "taskId": tid, "result": rj, "costTime": d.get("costTime")})
            return (rj.get("resultUrls") or [None])[0]
        if d.get("state") == "fail":
            log({"request": body, "taskId": tid, "fail": [d.get("failCode"), d.get("failMsg")]})
            print("FAILED", d.get("failCode"), d.get("failMsg")); return None
        time.sleep(6)
    log({"request": body, "taskId": tid, "fail": "timeout"}); return None


def fetch(url, out):
    Path(out).parent.mkdir(exist_ok=True)
    Path(out).write_bytes(requests.get(url, timeout=180).content)


