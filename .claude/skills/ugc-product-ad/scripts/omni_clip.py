"""Product-lock clip: Google Gemini Omni 1.1 Flash ON KIE (Ralph 2026-10-21: "product lock on all products ... Google
Omni"; 2026-10-22: "Use Omni on kie not thru the API key"). Kie model `google/gemini-omni-flash-1-1`, docs
https://docs.kie.ai/market/google/gemini-omni-flash-1-1.md.

  python3 omni_clip.py JOB SHOT --prompt-file P.txt --still STILL.png --ref LOGO1.png [--ref SHEET.png ...] \
      [--seconds 4|6|8|10] [--res 1080p] [--dry]
  python3 omni_clip.py JOB SHOT --edit --prompt-file FIX.txt [--dry]      # fix ONE detail of the shot's last take

- JOB is the job folder; grace/gate.py require() runs first (script gate + monthly cap). --dry prints the cost and the
  request and spends nothing.
- Reference mode (Kie: image_urls and first_frame_url cannot be combined, so refs win): the still is image 1, then one
  real close-up per logo/label in frame, then the product reference sheet (max 7 images). The prompt names each by
  number ("image 1" ...) and opens with "Recreate image 1 exactly as the first frame" (template:
  references/product-lock.md). Write it with the prompt-master skill.
- --edit sends the shot's last take back as video input (video_list, max 10 s) with a short prompt naming only the change
  and ending "Keep everything else the same."
- Kie list price (kie.ai/gemini-omni-1-1-flash, checked 2026-10-22), 360p/720p/1080p the same: 4 s $0.315, 6 s $0.42,
  8 s $0.525, 10 s $0.63; with video input (edit) $0.84 per generation; failed tasks cost $0.
- Writes JOB/clips/SHOT.mp4 (audio stripped) and logs to JOB/kie_log.json in the format grace/spend.py counts.
"""
import argparse, hashlib, json, os, subprocess, sys, time
from pathlib import Path

import requests

API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
MODEL = "google/gemini-omni-flash-1-1"
PRICE = {4: 0.315, 6: 0.42, 8: 0.525, 10: 0.63}
EDIT_PRICE = 0.84


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
    ap.add_argument("--still"); ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--seconds", type=int, default=4, choices=sorted(PRICE))
    ap.add_argument("--res", default="1080p", choices=["360p", "720p", "1080p"])
    ap.add_argument("--edit", action="store_true"); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    job = Path(a.job).resolve(); prompt = Path(a.prompt_file).read_text().strip()
    takes = sorted((job / "clips").glob(f"{a.shot}_omni_*.mp4")) if (job / "clips").exists() else []
    if a.edit:
        if not takes:
            sys.exit(f"--edit: no earlier Omni take of {a.shot} in {job / 'clips'}")
        if "Keep everything else the same" not in prompt:
            sys.exit("--edit prompt must end with 'Keep everything else the same.'")
        usd = EDIT_PRICE
    else:
        if not a.still:
            sys.exit("--still is required for a new take")
        n = 1 + len(a.ref)
        if n > 7:
            sys.exit("Kie Omni takes at most 7 images")
        for i in range(1, n + 1):
            if f"image {i}" not in prompt.lower():
                sys.exit(f"prompt does not name image {i}: every reference must be named (references/product-lock.md)")
        if "first frame" not in prompt.lower():
            sys.exit("prompt must say to recreate image 1 as the first frame")
        usd = PRICE[a.seconds]
    print(f"{a.shot}: Kie {MODEL} {'edit of ' + takes[-1].name if a.edit else f'{a.seconds}s'} {a.res} 9:16 -> ${usd}")
    if a.dry:
        print(prompt); return
    gate = find_up(job, "grace/gate.py")
    if not gate:
        sys.exit("grace/gate.py not found above the job folder")
    sys.path.insert(0, str(gate.parent)); from gate import require; require(job)
    folder = job.name
    inp = {"prompt": prompt, "aspect_ratio": "9:16", "resolution": a.res}
    if a.edit:
        dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                                    str(takes[-1])], capture_output=True, text=True).stdout or 4)
        inp["video_list"] = [{"url": upload(takes[-1], folder), "start": 0, "ends": round(min(dur, 10.0), 2)}]
    else:
        inp["duration"] = str(a.seconds)
        inp["image_urls"] = [upload(a.still, folder)] + [upload(r, folder) for r in a.ref]
    body = {"model": MODEL, "input": inp}
    for attempt in range(4):  # Kie answers 500 "server is busy" under load
        r = requests.post(f"{API}/createTask", json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid:
            break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        log(job, {"request": body, "response": resp}); sys.exit("createTask failed")
    log(job, {"submitted": tid, "prompt": prompt[:120]}); print("submitted", tid, flush=True)
    deadline = time.time() + 900
    while time.time() < deadline:
        d = (requests.get(f"{API}/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") == "success":
            rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            log(job, {"request": body, "taskId": tid, "result": rj, "costTime": d.get("costTime"), "usd": usd})
            break
        if d.get("state") == "fail":
            log(job, {"request": body, "taskId": tid, "fail": [d.get("failCode"), d.get("failMsg")], "usd": 0})
            sys.exit(f"Omni failed (Kie does not charge failed tasks): {d.get('failCode')} {d.get('failMsg')}")
        time.sleep(8)
    else:
        log(job, {"request": body, "taskId": tid, "fail": "timeout"}); sys.exit("timed out; recover with recordInfo " + tid)
    (job / "clips").mkdir(exist_ok=True)
    raw = job / "clips" / f"{a.shot}_omni_{len(takes) + 1}.mp4"
    raw.write_bytes(requests.get((rj.get("resultUrls") or [None])[0], timeout=300).content)
    out = job / "clips" / f"{a.shot}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-an", "-c:v", "copy", str(out)], check=True)
    print(f"OK {out} (${usd}); QC the product at 2x on several frames before it goes anywhere")


if __name__ == "__main__":
    main()
