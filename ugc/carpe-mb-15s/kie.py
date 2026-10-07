"""Kie runner for a Carpe MB 15s job (adapted from ugc/gtt-kn95/kie.py). Gate-protected.

  python3 kie.py stills [ID ...]   Nano Banana Pro stills ($0.09 each) -> stills/<ID>.png + preview/stills_sheet.png
  python3 kie.py clips  [ID ...]   Seedance 2.0 Mini, audio off ($0.041/s) -> clips/<ID>.mp4 + preview/clips_sheet.png
Every request/response goes to kie_log.json. Failed Kie tasks cost $0.
"""
import hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path
import requests


def _gate():
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)


API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
J = json.loads(Path(__file__).with_name("shots.json").read_text())
SHOTS = {s["id"]: s for s in J["shots"]}
MAIN = [s["id"] for s in J["shots"]]
HAND = []  # round 2: no hand refs (their long nails overrode the prompt)
KEY = os.environ.get("KIE_API_KEY")
HDR = {"Authorization": f"Bearer {KEY}"} if KEY else {}
LOG = Path("kie_log.json"); CACHE = Path("upload_cache.json"); _LOCK = threading.Lock()


def blocks(sid):
    s = SHOTS[sid]
    return " ".join(([J['hand_block']] if s.get('hand') else []) + ([J['prod_block']] if s.get('prod') else []))


def log(entry):
    with _LOCK:
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **entry}); LOG.write_text(json.dumps(data, indent=1))


def upload(path):
    p = Path(path); st = p.stat(); k = f"{p}|{st.st_size}|{st.st_mtime_ns}"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if k in cache: return cache[k]
    for attempt in range(4):
        r = requests.post(UPLOAD, headers=HDR, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": "carpe-mb-15s"}, timeout=120)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"): break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    if hashlib.sha256(requests.get(url, timeout=60).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs from the local file; not submitting")
    cache[k] = url; CACHE.write_text(json.dumps(cache, indent=1)); return url


def run_task(body):
    for attempt in range(4):
        _gate()
        r = requests.post(f"{API}/createTask", headers=HDR, json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid: break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        log({"request": body, "response": resp}); sys.exit("createTask failed")
    log({"submitted": tid, "prompt": body["input"].get("prompt", "")[:120]}); print("submitted", tid, flush=True)
    deadline = time.time() + 600
    while time.time() < deadline:
        d = (requests.get(f"{API}/recordInfo", headers=HDR, params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") == "success":
            rj = d.get("resultJson"); rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            log({"request": body, "taskId": tid, "result": rj, "costTime": d.get("costTime")}); return (rj.get("resultUrls") or [None])[0]
        if d.get("state") == "fail":
            log({"request": body, "taskId": tid, "fail": [d.get("failCode"), d.get("failMsg")]}); print("FAILED", d.get("failCode"), d.get("failMsg")); return None
        time.sleep(6)
    log({"request": body, "taskId": tid, "fail": "timeout"}); return None


def fetch(url, out):
    Path(out).parent.mkdir(exist_ok=True); Path(out).write_bytes(requests.get(url, timeout=180).content)


def one_still(sid):
    s = SHOTS[sid]
    refs = ([upload(p) for p in HAND] if s.get("hand") else []) + ([upload(p) for p in J["prod_refs"]] if s.get("prod") else [])
    prompt = f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} {blocks(sid)} {J['scene_block']}"
    url = run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)
    else: print("still", sid, "FAILED", flush=True)


def stills(ids):
    from concurrent.futures import ThreadPoolExecutor
    for p in HAND + J["prod_refs"]: upload(p)
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(one_still, ids))
    sheet("stills", ".png")


def clip(sid):
    s = SHOTS[sid]; first = upload(f"stills/{sid}.png")
    prompt = f"{s['video']} {blocks(sid)} {J['video_suffix']}"
    url = run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": first, "generate_audio": False,
                                                                   "resolution": "720p", "aspect_ratio": "9:16", "duration": s.get("dur", 4)}})
    if url: fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


def clips(ids):
    from concurrent.futures import ThreadPoolExecutor
    for sid in ids: upload(f"stills/{sid}.png")
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(clip, ids))
    sheet("clips", ".mp4")


def sheet(kind, ext):
    files = sorted(Path(kind).glob(f"*{ext}"), key=lambda p: MAIN.index(p.stem)); Path("preview").mkdir(exist_ok=True)
    F = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    if kind == "stills":
        from PIL import Image, ImageDraw
        W, H = 270, 480; im = Image.new("RGB", (W * len(files), H), "black")
        for i, f in enumerate(files):
            t = Image.open(f).convert("RGB").resize((W, H)); ImageDraw.Draw(t).text((8, 8), f.stem, fill="white"); im.paste(t, (i * W, 0))
        im.save("preview/stills_sheet.png")
    else:
        rows = []
        for f in files:
            row = f"preview/_{f.stem}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf", f"fps=1,scale=180:-2,tile=6x1,drawtext=fontfile={F}:text='{f.stem}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6", "-frames:v", "1", row], check=True); rows.append(row)
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", r] for r in rows], []), "-filter_complex", f"{''.join(f'[{i}]' for i in range(len(rows)))}vstack={len(rows)}" if len(rows) > 1 else "null", "-frames:v", "1", "preview/clips_sheet.png"], check=True)
    print("preview:", f"preview/{kind}_sheet.png")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent); cmd, ids = sys.argv[1], sys.argv[2:] or MAIN
    {"stills": stills, "clips": clips}[cmd](ids)
