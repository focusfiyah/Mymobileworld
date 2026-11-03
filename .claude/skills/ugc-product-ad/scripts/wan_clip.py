"""Product clip on Wan 3.0 ON KIE at 720P, upscaled by us to 1080x1920 for $0 (Ralph 2026-11-03: "Make wan the default
with our upscale"; Flow stays first, Wan replaces Kie Omni, Seedance 2.0 Mini stays for clips without the product).
Kie model `wan/3-0-video`, docs https://docs.kie.ai/market/wan/3-0-video.md.

  python3 wan_clip.py JOB SHOT --prompt-file P.txt --still STILL.png --ref LOGO1.png [--ref SHEET.png ...] \
      [--seconds 5] [--dry]

- JOB is the job folder; grace/gate.py require() runs first (script gate, monthly cap, approved Production Book) and
  start_task() right before createTask (field check, prompt check, budget lock, paid-task ledger). --dry prints the
  cost and the prompt and spends nothing.
- Reference mode (first frame and reference images cannot be combined on Wan): the still is Image1, then one real
  close-up per logo/label in frame, then the product reference sheet (10 images at most). The prompt names each one
  ("Image1", "Image2", ...) and opens with "Recreate Image1 exactly as the first frame" (template:
  references/product-lock.md). Write it with the prompt-master skill.
- Price (kie.ai/wan3.0-video, checked 2026-11-03): 720P 16 credits/s = $0.08/s (5 s $0.40), the same per second as
  Omni. 1080P costs double and is not needed: the free upscale below kept the ZYTRELL label at 2x about as sharp as
  Omni's native 1080p (test: Mymobileworld ugc/_tests/wan3-vs-omni).
- Writes JOB/clips/SHOT_wan_N.mp4 (720p as delivered) and JOB/clips/SHOT.mp4 (1080x1920, lanczos + light unsharp, no
  audio); logs to JOB/kie_log.json in the format grace/spend.py counts.
"""
import argparse, hashlib, json, re, subprocess, sys, time
from pathlib import Path

import requests

API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
MODEL = "wan/3-0-video"
USD_PER_S = 0.08   # 720P
UPSCALE = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.6:5:5:0"


def find_up(start, rel):
    for p in [start, *start.parents]:
        if (p / rel).exists():
            return p / rel
    return None


def log(job, entry):
    f = job / "kie_log.json"; data = json.loads(f.read_text()) if f.exists() else []
    data.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **entry}); f.write_text(json.dumps(data, indent=1))


def upload(path, folder):
    p = Path(path)
    for attempt in range(4):
        r = requests.post(UPLOAD, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": folder}, timeout=180)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"):
            break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    if hashlib.sha256(requests.get(url, timeout=120).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs from the local file; not submitting")
    return url


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job"); ap.add_argument("shot")
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--still", required=True); ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--seconds", type=int, default=5)
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    job = Path(a.job).resolve(); prompt = Path(a.prompt_file).read_text().strip()
    if not 2 <= a.seconds <= 30:
        sys.exit("--seconds must be 2-30 (Wan 3.0)")
    n = 1 + len(a.ref)
    if n > 10:
        sys.exit("Wan 3.0 takes at most 10 reference images")
    for i in range(1, n + 1):
        if not re.search(rf"\bimage ?{i}\b", prompt, re.I):
            sys.exit(f"prompt does not name Image{i}: every reference must be named (references/product-lock.md)")
    if "first frame" not in prompt.lower():
        sys.exit("prompt must say to recreate Image1 as the first frame")
    usd = round(USD_PER_S * a.seconds, 3)
    print(f"{a.shot}: Kie {MODEL} {a.seconds}s 720P 9:16 -> ${usd} (+ free upscale to 1080x1920)")
    if a.dry:
        print(prompt); return
    gate = find_up(job, "grace/gate.py")
    if not gate:
        sys.exit("grace/gate.py not found above the job folder")
    sys.path.insert(0, str(gate.parent)); from gate import require, start_task, task_submitted; require(job)
    import clip_check   # grace/clip_check.py (Ralph 2026-10-26): wrong-shape still = cropped clip; checked before paying
    errs = clip_check.check_still(a.still, "9:16")
    if errs:
        sys.exit("CLIP_CHECK_FAIL before spending: " + "; ".join(errs))
    folder = job.name
    inp = {"prompt": prompt, "reference_image_urls": [upload(a.still, folder)] + [upload(r, folder) for r in a.ref],
           "resolution": "720P", "aspect_ratio": "9:16", "duration": a.seconds, "audio": False}
    body = {"model": MODEL, "input": inp}
    key = start_task(job, body, label=a.shot, usd=usd)   # saved + pushed before Kie is asked
    for attempt in range(4):  # Kie answers 500 "server is busy" under load
        r = requests.post(f"{API}/createTask", json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid:
            break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        task_submitted(job, key, None)
        log(job, {"request": body, "response": resp}); sys.exit("createTask failed")
    task_submitted(job, key, tid)
    log(job, {"submitted": tid, "prompt": prompt[:120]}); print("submitted", tid, flush=True)
    deadline = time.time() + 1500
    while time.time() < deadline:
        d = (requests.get(f"{API}/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") == "success":
            rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            billed = d.get("creditsConsumed")   # what Kie actually charged (1 credit = $0.005), else the list price
            log(job, {"request": body, "taskId": tid, "result": rj, "costTime": d.get("costTime"),
                      "usd": round(float(billed) * 0.005, 4) if billed is not None else usd,
                      **({"credits": billed} if billed is not None else {})})
            break
        if d.get("state") == "fail":
            log(job, {"request": body, "taskId": tid, "fail": [d.get("failCode"), d.get("failMsg")], "usd": 0})
            sys.exit(f"Wan failed (Kie does not charge failed tasks): {d.get('failCode')} {d.get('failMsg')}")
        time.sleep(10)
    else:
        log(job, {"request": body, "taskId": tid, "fail": "timeout"}); sys.exit("timed out; recover with recordInfo " + tid)
    (job / "clips").mkdir(exist_ok=True)
    takes = sorted((job / "clips").glob(f"{a.shot}_wan_*.mp4"))
    raw = job / "clips" / f"{a.shot}_wan_{len(takes) + 1}.mp4"
    raw.write_bytes(requests.get((rj.get("resultUrls") or [None])[0], timeout=300).content)
    out = job / "clips" / f"{a.shot}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-an", "-vf", UPSCALE, "-c:v", "libx264", "-crf", "16",
                    "-preset", "veryfast", "-threads", "4", "-pix_fmt", "yuv420p", str(out)], check=True)
    # Kie bills a clip that ignored the image: compare the opening second with the still
    ok, score = clip_check.report(a.still, out, aspect="9:16", seconds=a.seconds)
    log(job, {"clip_check": str(out), "still": a.still, "ok": ok, "score": score})
    if ok is False:
        sys.exit(f"{out} saved but FAILED the clip check: look at it before anyone else does")
    print(f"OK {out} (${usd}, upscaled from {raw.name}); QC the product at 2x on several frames before it goes anywhere")


if __name__ == "__main__":
    main()
