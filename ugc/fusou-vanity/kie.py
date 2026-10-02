"""Kie runner for the FUSOU vanity job. Prompts come from shots.json (built by make_shots.py).

  python3 kie.py stills ID [ID ...]   Nano Banana Pro, 1K 9:16, $0.09 each -> stills/<ID>.png
  python3 kie.py clips  ID [ID ...]   Seedance 2.0 Mini, audio off, $0.041/s -> clips/<ID>.mp4
Key comes from the environment proxy. Every submit/result goes to kie_log.json; failed Kie tasks cost $0.
"""
import hashlib, json, os, sys, threading, time
from pathlib import Path
import requests

os.chdir(Path(__file__).parent)
API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
J = json.loads(Path("shots.json").read_text())
SHOTS = {s["id"]: s for s in J["shots"]}
HAND_REFS = ["refs/hand_dorsal.png", "refs/hand_palm.png"]
LOG, CACHE, _LOCK = Path("kie_log.json"), Path("upload_cache.json"), threading.Lock()


def log(entry):
    with _LOCK:
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **entry}); LOG.write_text(json.dumps(data, indent=1))


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


def text_blocks(s):
    return " ".join(J["blocks"][b] for b in s["blocks"])


def ref_paths(s):
    paths = [J["refs"][r] for r in s["refs"]]
    if "hand" in s["blocks"]: paths = HAND_REFS + paths
    return paths


def still(sid):
    s = SHOTS[sid]; paths = ref_paths(s)
    prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} {text_blocks(s)} {J['blocks']['phone']}"
              + (" The reference images show the real product: reproduce it exactly (same drawers, knobs, mirrors, colour, proportions)."
                 if "vanity" in s["blocks"] else ""))
    if "hand" in s["blocks"]:
        prompt += " The first two reference images are the hands (skin tone, hand shape, nail look)."
    url = run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [upload(p) for p in paths],
                                                          "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    s = SHOTS[sid]
    prompt = f"{s['video']} {text_blocks(s)} {J['video_suffix']}"
    url = run_task({"model": "bytedance/seedance-2-mini", "input": {
        "prompt": prompt, "first_frame_url": upload(f"stills/{sid}.png"), "generate_audio": False,
        "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}})
    if url: fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    cmd, ids = sys.argv[1], sys.argv[2:]
    if not ids: sys.exit("name the shot ids (ask Ralph before any paid call)")
    from concurrent.futures import ThreadPoolExecutor  # parallel; Kie "server busy" is retried and failed tasks cost $0
    fn = {"stills": still, "clips": clip}[cmd]
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(fn, ids))
