"""Kie runner for the V1 A/B job (gated on v1ab/checklist.json, not the old FUSOU job). Same upload/submit/poll/fetch as ../kie.py. Logs to v1ab/kie_log.json."""
import hashlib, json, os, sys, time
from pathlib import Path
import requests
HERE = Path(__file__).resolve().parent; ROOT = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "grace")); from gate import require
os.chdir(ROOT)
API = "https://api.kie.ai/api/v1/jobs"; UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
LOG, CACHE = HERE / "kie_log.json", ROOT / "upload_cache.json"


def log(e):
    d = json.loads(LOG.read_text()) if LOG.exists() else []; d.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **e}); LOG.write_text(json.dumps(d, indent=1))


def upload(path):
    p = Path(path); st = p.stat(); k = f"{p}|{st.st_size}|{st.st_mtime_ns}"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if k in cache: return cache[k]
    for attempt in range(4):
        r = requests.post(UPLOAD, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": "fusou"}, timeout=120)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"): break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    if hashlib.sha256(requests.get(url, timeout=60).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs; not submitting")
    cache[k] = url; CACHE.write_text(json.dumps(cache, indent=1)); return url


def run_task(body):
    for attempt in range(4):
        require(HERE)
        r = requests.post(f"{API}/createTask", json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid: break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        log({"request": body, "response": resp}); sys.exit("createTask failed")
    log({"submitted": tid, "prompt": body["input"].get("prompt", "")[:120]}); print("submitted", tid, flush=True)
    deadline = time.time() + 900
    while time.time() < deadline:
        d = (requests.get(f"{API}/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") == "success":
            rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            log({"request": body, "taskId": tid, "result": rj, "costTime": d.get("costTime")})
            return (rj.get("resultUrls") or [None])[0]
        if d.get("state") == "fail":
            log({"request": body, "taskId": tid, "fail": [d.get("failCode"), d.get("failMsg")]}); print("FAILED", d.get("failCode"), d.get("failMsg")); return None
        time.sleep(6)
    log({"request": body, "taskId": tid, "fail": "timeout"}); return None


def fetch(url, out):
    Path(out).parent.mkdir(exist_ok=True); Path(out).write_bytes(requests.get(url, timeout=180).content)


