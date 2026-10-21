"""Kie runner for the Shnuggle "next bath" video (adapted from ugc/shnuggle-response/kie.py + ugc/lgxnds-creatine/kie2.py). Gate-protected.

  python3 kie.py stills [ID ...]   Nano Banana Pro stills ($0.09 each) -> stills/<ID>.png + preview/stills_sheet.png
  python3 kie.py clips  [ID ...]   Seedance 2.0 Mini, audio off ($0.041/s), REFERENCE mode for hand+tub shots -> clips/<ID>.mp4 + preview/clips_sheet.png
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
MAIN = list(SHOTS)
HAND = J["hand_refs"]  # Grace's hands with the birthstone ring (ThunderFit stills) + real ring packshot
TUB = J["tub_refs"]    # product lock (Ralph 2026-10-19): real-photo product sheet + real front 3/4 cut-out
LOOK = "stills/look_ref.png"  # copy of the approved test still (S8): room, light, hand, rings
KEY = os.environ.get("KIE_API_KEY")
HDR = {"Authorization": f"Bearer {KEY}"} if KEY else {}
LOG = Path("kie_log.json"); CACHE = Path("upload_cache.json"); _LOCK = threading.Lock()



def log(entry):
    with _LOCK:
        data = json.loads(LOG.read_text()) if LOG.exists() else []
        data.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **entry}); LOG.write_text(json.dumps(data, indent=1))


def upload(path):
    p = Path(path); st = p.stat(); k = f"{p}|{st.st_size}|{st.st_mtime_ns}"
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    if k in cache: return cache[k]
    for attempt in range(4):
        r = requests.post(UPLOAD, headers=HDR, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": "shnuggle-next-bath"}, timeout=120)
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



def text(sid):
    s = SHOTS[sid]
    parts = [s["still"], J["hand_block"] if s["hand"] else J["no_hand"]]
    if s["tub"]: parts.append(J["tub_block"])
    if s.get("infant"): parts.append(J["infant_block"])
    return " ".join(parts + [J["scene_block"]])


def fetch(url, out):
    Path(out).parent.mkdir(exist_ok=True); Path(out).write_bytes(requests.get(url, timeout=180).content)



def one_still(sid):
    s = SHOTS[sid]
    refs = ([upload(p) for p in HAND] if s["hand"] else []) + ([upload(p) for p in TUB] if s["tub"] else [])
    note = " Reference images: " + ("the hand photos (skin, nails, the two rings; ignore their backgrounds), " if s["hand"] else "") + \
           ("the Shnuggle product reference sheet and the real front 3/4 photo (copy the tub exactly from these), " if s["tub"] else "")
    if Path(LOOK).exists() and sid != "S8":
        refs.append(upload(LOOK)); note += "and the last image, an approved frame from this same video: match its bathroom, tiles, light" + (", hand and rings" if s["hand"] else "") + " exactly, but follow this prompt for framing and for what is in the shot."
    prompt = f"Vertical 9:16 photo, a single frame from a phone-shot UGC video. {text(sid)}{note}"
    url = run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)
    else: print("still", sid, "FAILED", flush=True)


def stills(ids):
    from concurrent.futures import ThreadPoolExecutor
    for p in HAND + TUB: upload(p)
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(one_still, ids))
    sheet("stills", ".png")


def clip(sid):
    s = SHOTS[sid]; assert s["model"].startswith("seedance"), f"{sid} is a Kling shot (Kling MCP, Ralph's account)"
    clean = f"stills/{sid}_clean.png"; first = upload(clean if Path(clean).exists() else f"stills/{sid}.png")
    prompt = f"{s['video']} {J['video_suffix']}"
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": first, "generate_audio": False,
            "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
    if s["model"] == "seedance_ref":   # LGXNDS v5 route (Ralph 2026-10-19): reference mode, no first frame, real tub refs in the loop
        body["input"].pop("first_frame_url")
        body["input"]["reference_image_urls"] = [first, upload(TUB[1]), upload(TUB[0])]
        body["input"]["prompt"] = ("Recreate reference image 1 exactly (same bathroom, framing, hand, rings, tub, water and toys) as the first frame, then: "
            + prompt + " The toddler tub must match reference image 2 exactly: white glossy tub, light-grey foam backrest, grey oval 'shnuggle' badge; "
            "reference image 3 shows the tub's shape from every side.")
    url = run_task(body)
    if url: fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)
    else: print("clip", sid, "FAILED", flush=True)


def clips(ids):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(clip, ids))
    sheet("clips", ".mp4")


def sheet(kind, ext):
    files = sorted([p for p in Path(kind).glob(f"*{ext}") if p.stem in MAIN], key=lambda p: MAIN.index(p.stem)); Path("preview").mkdir(exist_ok=True)
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
    os.chdir(Path(__file__).parent); cmd, ids = sys.argv[1], sys.argv[2:]
    if not ids: sys.exit("name the shot ids: one test first, then the rest (Ralph's rule)")
    {"stills": stills, "clips": clips}[cmd](ids)
