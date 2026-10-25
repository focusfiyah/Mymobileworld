"""One virtual try-on image per model on fal (FASHN v1.6, Kling Kolors). Ralph pre-approved <= $0.50 for this test
(2026-10-22, "run the test"). Refuses to re-run a model already in tryon_log.json (no silent retries)."""
import base64, hashlib, json, os, sys, time, urllib.request, concurrent.futures as cf
from pathlib import Path
HERE = Path(__file__).parent; LOG = HERE / "tryon_log.json"; JOB = HERE.parent
sys.path.insert(0, str(HERE.parents[2] / "grace")); from gate import require, start_task, task_submitted
def uri(p): return "data:image/jpeg;base64," + base64.b64encode((HERE / p).read_bytes()).decode()
JOBS = {
  "fashn": ("fal-ai/fashn/tryon/v1.6", 0.075, {"model_image": uri("person.jpg"), "garment_image": uri("garment_front.jpg"),
            "category": "bottoms", "mode": "quality", "garment_photo_type": "flat-lay", "num_samples": 1, "output_format": "png"}),
  "fashn_real": ("fal-ai/fashn/tryon/v1.6", 0.075, {"model_image": uri("person_real.jpg"), "garment_image": uri("garment_front.jpg"),
            "category": "bottoms", "mode": "quality", "garment_photo_type": "flat-lay", "num_samples": 1, "output_format": "png"}),
  "fashn_real_seg": ("fal-ai/fashn/tryon/v1.6", 0.075, {"model_image": uri("person_real.jpg"), "garment_image": uri("garment_front.jpg"),
            "category": "bottoms", "mode": "quality", "garment_photo_type": "flat-lay", "num_samples": 1, "output_format": "png",
            "segmentation_free": False}),
  "fashn_shorts": ("fal-ai/fashn/tryon/v1.6", 0.075, {"model_image": uri("person_shorts.jpg"), "garment_image": uri("garment_front.jpg"),
            "category": "bottoms", "mode": "quality", "garment_photo_type": "flat-lay", "num_samples": 1, "output_format": "png"}),
  "kolors_shorts": ("fal-ai/kling/v1-5/kolors-virtual-try-on", 0.07, {"human_image_url": uri("person_shorts.jpg"), "garment_image_url": uri("garment_front.jpg")}),
  "kolors": ("fal-ai/kling/v1-5/kolors-virtual-try-on", 0.07, {"human_image_url": uri("person.jpg"), "garment_image_url": uri("garment_front.jpg")}),
}
def req(url, body=None):
    r = urllib.request.Request(url, data=json.dumps(body).encode() if body else None, headers={"content-type": "application/json", "Authorization": "Key " + os.environ["fal_key"]})
    return json.loads(urllib.request.urlopen(r, timeout=120).read())
# v2 (2026-10-25): any look as NAME=PERSON,GARMENT (paths under tryon/), Kolors. Wired into grace/gate.py: book + budget
# lock + paid-task ledger, usd passed explicitly (fal is not a Kie model). The ledger body names files by sha256, not base64.
KOLORS = ("fal-ai/kling/v1-5/kolors-virtual-try-on", 0.07)
for a in sys.argv[1:]:
    if "=" in a:
        n, pg = a.split("=", 1); per, gar = pg.split(",")
        JOBS[n] = (KOLORS[0], KOLORS[1], {"human_image_url": uri(per), "garment_image_url": uri(gar)})
def sha(v): return hashlib.sha256(v.encode()).hexdigest()[:16] if isinstance(v, str) and v.startswith("data:") else v
def run(name):
    ep, usd, body = JOBS[name]
    key = start_task(JOB, {"model": ep, "input": {k: sha(v) for k, v in body.items()}}, label=name, usd=usd)
    try:
        sub = req(f"https://queue.fal.run/{ep}", body); rid = sub["request_id"]
    except Exception:
        task_submitted(JOB, key, None); raise
    task_submitted(JOB, key, rid); print(name, "submitted", rid, flush=True)
    while req(sub["status_url"])["status"] != "COMPLETED": time.sleep(4)
    res = req(sub["response_url"]); url = (res.get("images") or [res.get("image")])[0]["url"]
    out = HERE / f"{name}.png"; out.write_bytes(urllib.request.urlopen(url, timeout=120).read())
    return {"model": name, "endpoint": ep, "usd": usd, "request_id": rid, "out": str(out.relative_to(HERE.parents[2])), "url": url}
log = json.loads(LOG.read_text()) if LOG.exists() else []
names = [a.split("=", 1)[0] for a in sys.argv[1:]]
require(JOB)   # script gate + cap + approved BOOK.md before anything is sent
todo = [n for n in names if n not in {e["model"] for e in log}]
with cf.ThreadPoolExecutor(2) as ex:
    for e in ex.map(run, todo): log.append(e); LOG.write_text(json.dumps(log, indent=1)); print(e["model"], "->", e["out"])
