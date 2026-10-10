"""Kie runner for the ThunderFit December ring ad (copied from ugc/lgxnds-creatine). Each paid step writes a preview to approve before the next one.

  python3 kie.py stills [ID ...]   Nano Banana Pro stills ($0.09 each) -> stills/<ID>.png + preview/stills_sheet.png
  python3 kie.py clips  [ID ...]   Seedance 2.0 Mini, audio off ($0.041/s) -> clips/<ID>.mp4 + preview/clips_sheet.png

Key: KIE_API_KEY env var, or none if the environment proxy injects it for api.kie.ai. Every request and
response goes to kie_log.json. Failed Kie tasks cost $0.
"""
import hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path
import requests


def _gate():  # SCRIPT GATE (grace/gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven
    import sys as _s, pathlib as _p; _h = _p.Path(__file__).resolve()
    _s.path.insert(0, str(_h.parents[2] / "grace")); from gate import require; require(_h.parent)



API = "https://api.kie.ai/api/v1/jobs"
UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
J = json.loads(Path("shots.json").read_text())
SHOTS = {s["id"]: s for s in J["shots"]}
MAIN = [s["id"] for s in J["shots"]]
HAND_NOBLUE = ["refs/hand_noblue.jpg"]  # Grace's hand, crown set + heart ring, blue ring cropped out
HAND_BLUE = ["refs/grace_palm_rings.jpg"]  # palm with the real blue ring
PROD = "refs/real_ring_packshot.jpg"  # Grace's real December band


def blocks(sid):
    s = SHOTS[sid]
    return " ".join(([J["identity_bare"] if s.get("bare") else J["identity_block"]] if s["hand"] else []) + ([J["crown_block"]] if s["crown"] else [])
                    + ([J["ring_block"]] if s["ring"] else []))
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
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if k in cache:
        return cache[k]
    for attempt in range(4):
        r = requests.post(UPLOAD, headers=HDR, files={"file": (p.name, p.read_bytes())},
                          data={"uploadPath": "thunderfit-ring"}, timeout=120)
        if r.ok and (r.json().get("data") or {}).get("downloadUrl"):
            break
        time.sleep(2 ** attempt)
    url = r.json()["data"]["downloadUrl"]
    # pre-flight: the hosted file must be byte-identical to the local one
    if hashlib.sha256(requests.get(url, timeout=60).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs from the local file; not submitting")
    cache[k] = url; CACHE.write_text(json.dumps(cache, indent=1))
    return url


def run_task(body):
    for attempt in range(4):  # Kie answers 500 "server is busy" under load; an immediate retry works
        _gate()
        r = requests.post(f"{API}/createTask", headers=HDR, json=body, timeout=60)
        resp = r.json() if r.headers.get("content-type", "").startswith("application/json") else {"raw": r.text[:300]}
        tid = (resp.get("data") or {}).get("taskId")
        if tid:
            break
        print("createTask", r.status_code, json.dumps(resp)[:300]); time.sleep(3)
    else:
        log({"request": body, "response": resp}); sys.exit("createTask failed")
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


def stills(ids):
    for sid in ids:
        s = SHOTS[sid]
        refs = ([upload("refs/hand_dorsal.png")] if s.get("bare") else [upload(p) for p in (HAND_BLUE + HAND_NOBLUE if s["ring"] else HAND_NOBLUE)] if s["hand"] else []) \
            + ([upload(PROD)] if s["ring"] else [])
        prompt = (f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {s['still']} "
                  f"{blocks(sid)} {J['scene_block']}" + ("" if s["ring"] else " There is no blue ring anywhere in this image."))
        url = run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs,
                                                              "aspect_ratio": "9:16", "resolution": "1K"}})
        if url:
            fetch(url, f"stills/{sid}.png"); print("still", sid, "ok")
    sheet("stills", ".png")


def clips(ids):
    from concurrent.futures import ThreadPoolExecutor
    for sid in ids:  # upload first frames up front (cached), then render all clips in parallel
        upload(SHOTS[sid].get("first_frame", f"stills/{sid}.png"))
    with ThreadPoolExecutor(len(ids)) as ex:
        list(ex.map(clip, ids))
    sheet("clips", ".mp4")


def clip(sid):
    s = SHOTS[sid]
    first = upload(s.get("first_frame", f"stills/{sid}.png"))
    prompt = f"{s['video']} {blocks(sid)} {J['video_suffix']}"
    url = run_task({"model": "bytedance/seedance-2-mini", "input": {
        "prompt": prompt, "first_frame_url": first, "generate_audio": False,
        "resolution": "720p", "aspect_ratio": "9:16", "duration": s.get("dur", 4)}})
    if url:
        fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


def sheet(kind, ext):
    """One labelled preview image: every still, or 4 frames per clip (one row per clip)."""
    files = sorted(Path(kind).glob(f"*{ext}"), key=lambda p: (MAIN + list(SHOTS)).index(p.stem))
    Path("preview").mkdir(exist_ok=True)
    if kind == "stills":
        inputs = sum([["-i", str(f)] for f in files], [])
        lab = "".join(f"[{i}]scale=270:480,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                      f"text='{f.stem}':x=10:y=10:fontsize=28:fontcolor=white:box=1:boxcolor=black@0.6[v{i}];"
                      for i, f in enumerate(files))
        cols = min(len(files), 5); rows = -(-len(files) // cols)
        pad = "".join(f"color=black:270x480:d=1[p{j}];" for j in range(cols * rows - len(files)))
        cells = "".join(f"[v{i}]" for i in range(len(files))) + "".join(f"[p{j}]" for j in range(cols * rows - len(files)))
        lay = "|".join(f"{(i % cols) * 270}_{(i // cols) * 480}" for i in range(cols * rows))
        subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex",
                        f"{lab}{pad}{cells}xstack=inputs={cols * rows}:layout={lay}" if cols * rows > 1 else lab.rstrip(";").replace("[v0]", ""), "-frames:v", "1",
                        "preview/stills_sheet.png"], check=True)
    else:
        rows = []
        for f in files:
            row = f"preview/_{f.stem}.png"
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(f), "-vf",
                            "fps=1,scale=180:-2,tile=5x1,drawtext=fontfile=/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf:"
                            f"text='{f.stem}':x=6:y=6:fontsize=22:fontcolor=white:box=1:boxcolor=black@0.6",
                            "-frames:v", "1", row], check=True)
            rows.append(row)
        subprocess.run(["ffmpeg", "-v", "error", "-y", *sum([["-i", r] for r in rows], []), "-filter_complex",
                        f"{''.join(f'[{i}]' for i in range(len(rows)))}vstack={len(rows)}" if len(rows) > 1 else "null",
                        "-frames:v", "1", "preview/clips_sheet.png"], check=True)
    print("preview:", f"preview/{kind}_sheet.png")


if __name__ == "__main__":
    os.chdir(Path(__file__).parent)
    cmd, ids = sys.argv[1], sys.argv[2:] or MAIN
    {"stills": stills, "clips": clips}[cmd](ids)
