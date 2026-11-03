"""Wan 3.0 vs Omni test (Ralph 2026-11-03 tapped "One test vs Omni (Recommended)", $0.40).
One wan/3-0-video clip, reference mode, 720P 9:16 5 s, same shot and refs as ZYTRELL S3's Omni take.
Field check, monthly cap, prompt check and paid-task ledger run first; clip_check after.
  cd ugc/_tests/wan3-vs-omni && python3 run.py
"""
import json, subprocess, sys, time
from pathlib import Path
import requests
JOB = Path(__file__).resolve().parent
ROOT = JOB.parents[2]
SRC = ROOT / "ugc/zytrell-acne-cream"
sys.path.insert(0, str(ROOT / "grace")); sys.path.insert(0, str(SRC))
import kie_fields, prompt_check, paid, spend, billed
from kie import upload   # ZYTRELL job's Kie file host helper (cached)

USD = 0.40   # 5 s x 16 credits/s x $0.005 (720P, kie.ai/wan3.0-video, checked 2026-11-03)
refs = [SRC / "stills/S3.png", SRC / "refs/logo_closeup.png", SRC / "refs/product_sheet.png"]
body = {"model": "wan/3-0-video",
        "input": {"prompt": (JOB / "prompt.txt").read_text().strip(),
                  "reference_image_urls": [upload(p) for p in refs],
                  "resolution": "720P", "aspect_ratio": "9:16", "duration": 5, "audio": False}}
errs = kie_fields.check(body) + spend.budget_errors(JOB)
if errs:
    sys.exit("refused: " + "; ".join(errs))
prompt_check.require(JOB, body)
key = paid.claim(JOB, body, USD, label="wan3 S3 test")
r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=body, timeout=60).json()
tid = (r.get("data") or {}).get("taskId")
paid.submitted(JOB, key, tid)
log = JOB / "kie_log.json"; L = json.loads(log.read_text()) if log.exists() else []
if not tid:
    L.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "response": r}); log.write_text(json.dumps(L, indent=1))
    sys.exit(f"createTask failed: {r}")
print("submitted", tid, flush=True)
L.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "submitted": tid}); log.write_text(json.dumps(L, indent=1))
t0 = time.time()
while time.time() - t0 < 1500:
    d = (requests.get("https://api.kie.ai/api/v1/jobs/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
    if d.get("state") in ("success", "fail"):
        break
    time.sleep(10)
credits = d.get("creditsConsumed")
e = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "taskId": tid, "costTime": d.get("costTime"), "state": d.get("state"),
     **({"credits": credits, "usd": round(float(credits) * 0.005, 4)} if credits is not None else {})}
if d.get("state") != "success":
    e["fail"] = [d.get("failCode"), d.get("failMsg") or d.get("state")]
    L.append(e); log.write_text(json.dumps(L, indent=1)); sys.exit(f"not done: {e.get('fail')} (fetch task {tid} again before any redo)")
rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) else (rj or {})
e["result"] = rj; L.append(e); log.write_text(json.dumps(L, indent=1))
url = (rj.get("resultUrls") or [None])[0]
out = JOB / "S3_wan3.mp4"; out.write_bytes(requests.get(url, timeout=300).content)
billed.refresh(quiet=True)
print(f"OK {out}  billed {credits} credits = ${float(credits or 0) * 0.005:.3f}")
subprocess.run([sys.executable, str(ROOT / "grace/clip_check.py"), str(refs[0]), str(out)])
