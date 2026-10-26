"""One GPT Image 2 still (2K, 9:16) from prompt.txt. Field check, prompt check, monthly cap and paid-task ledger first.
  cd ugc/_tests/gpt-image-2-pov && python3 run.py
"""
import json, sys, time
from pathlib import Path
import requests
JOB = Path(__file__).resolve().parent
sys.path.insert(0, str(JOB.parents[2] / "grace"))
import kie_fields, prompt_check, paid, spend, billed

body = {"model": "gpt-image-2-text-to-image",
        "input": {"prompt": (JOB / "prompt.txt").read_text().strip(), "aspect_ratio": "9:16", "resolution": "2K"}}
errs = kie_fields.check(body) + spend.budget_errors(JOB)
if errs:
    sys.exit("refused: " + "; ".join(errs))
prompt_check.require(JOB, body)
key = paid.claim(JOB, body, 0.05, label="gpt-image-2 pov test")
r = requests.post("https://api.kie.ai/api/v1/jobs/createTask", json=body, timeout=60).json()
tid = (r.get("data") or {}).get("taskId")
paid.submitted(JOB, key, tid)
log = JOB / "kie_log.json"; L = json.loads(log.read_text()) if log.exists() else []
if not tid:
    L.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "response": r}); log.write_text(json.dumps(L, indent=1))
    sys.exit(f"createTask failed: {r}")
print("submitted", tid, flush=True)
L.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), "submitted": tid}); log.write_text(json.dumps(L, indent=1))
for _ in range(100):
    d = (requests.get("https://api.kie.ai/api/v1/jobs/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
    if d.get("state") in ("success", "fail"):
        break
    time.sleep(6)
credits = d.get("creditsConsumed")
e = {"t": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "taskId": tid, "costTime": d.get("costTime"),
     **({"credits": credits, "usd": round(float(credits) * 0.005, 4)} if credits is not None else {})}
if d.get("state") != "success":
    e["fail"] = [d.get("failCode"), d.get("failMsg") or d.get("state")]
    L.append(e); log.write_text(json.dumps(L, indent=1)); sys.exit(f"failed: {e['fail']}")
rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) else (rj or {})
e["result"] = rj; L.append(e); log.write_text(json.dumps(L, indent=1))
url = (rj.get("resultUrls") or [None])[0]
(JOB / "still.png").write_bytes(requests.get(url, timeout=120).content)
billed.refresh(quiet=True)
print(f"OK still.png  billed {credits} credits = ${float(credits or 0) * 0.005:.3f}")
