"""Kie runner for the space heater ad (copied from ugc/lgxnds-creatine). Stills: Gemini 3 Pro Image (nano-banana-pro). Hand clips: Seedance 2.0 Mini reference mode.

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
HAND = ["refs/hand/hand_french_bare.png", "refs/hand/bracelet_wrist.png", "refs/hand/blue_ring_real.jpg"]  # bare French-tip hand + her bracelet (sheet crop, no rings) + real blue ring
PROD = ["refs/product_sheet.png", "refs/ralph_sheet.jpg"]  # my real-pixel sheet (the product) + Ralph's AI sheet (shape only)


def blocks(sid):
    s = SHOTS[sid]
    return " ".join(([J["hand_block"]] if s["hand"] else ["No hand, no arm and no people anywhere in the frame."]) + ([J["heater_block"]] if s.get("heater", True) else []))
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
                          data={"uploadPath": "space-heater-ptc"}, timeout=120)
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



def still(sid):
    s = SHOTS[sid]; refs, names = [], []
    if s["hand"]:
        refs += [upload(p) for p in HAND]; names += ["Grace's bare hand (skin tone, nail shape, pink French tips: copy exactly)", "her gold watch-link bracelet with the pearl chain and leaf charm (on the wrist)", "the real sky-blue silicone ring (on the ring finger; no other rings)"]
    if s.get("heater", True) and s.get("panel"):   # top-panel close-up: real pixels only (Ralph's AI sheet added an X button, V1S8 r1)
        refs += [upload(PROD[0]), upload("refs/top_panel.png")]; names += ["the heater's reference sheet: REAL photos, copy the product exactly", "the REAL top panel close up: copy its buttons and display exactly"]
    elif s.get("heater", True):
        refs += [upload(p) for p in PROD]; names += ["the heater's reference sheet: these are REAL photos, copy the product exactly (shape, mesh, heater window, top panel)", "extra angles of the same heater, for its shape only (ignore its top-panel buttons)"]
    refs.append(upload(s["room"])); names.append("the room: keep this room, its furniture and its light, made neutral daylight")
    look = "stills/look_ref.png"
    if Path(look).exists() and sid != "V1S7":   # look_ref = approved V1S7 r2 (flat bracelet, French tips)
        refs.append(upload(look)); names.append("an approved frame from this same video: copy its hand, its FLAT gold link bracelet, its pearl chain with leaf, its single blue ring and its white French-tip nails exactly")
    prompt = ("Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + s["still"] + " " + blocks(sid) + " " + J["scene_block"]
              + " Reference images in order: " + "; ".join(f"{i+1}) {n}" for i, n in enumerate(names)) + ".")
    url = run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def stills(ids):
    from concurrent.futures import ThreadPoolExecutor
    for p in HAND + PROD: upload(p)
    with ThreadPoolExecutor(len(ids)) as ex:   # all at once (Ralph 2026-10-19: speed)
        list(ex.map(still, ids))
    sheet("stills", ".png")

def clip(sid):
    """Seedance 2.0 Mini, REFERENCE mode (no first frame; Ralph 2026-10-19 LGXNDS method): ref 1 = the approved still, 2 = my real-pixel
    sheet, 3 = the hand refs collage is not passed (the still already carries the hand). --free = the hand-free comparison clip."""
    s = SHOTS[sid]
    refs = [upload(f"stills/{sid}.png")] + ([upload(PROD[0])] if s.get("heater", True) else [])
    prompt = ("Recreate reference image 1 exactly (same room, framing, light" + (", hand, gold bracelet, blue ring" if s["hand"] else "")
              + (", heater" if s.get("heater", True) else "") + ") as the first frame, then: " + s["motion"] + " " + J["video_suffix"]
              + (" The heater must match reference image 2 exactly: matte-black mesh cylinder, the rectangular heater window, the round "
                 "black top panel with the white display and red power button; it never changes shape or size." if s.get("heater", True) else "")
              + (" Only the hand and wrist enter from the frame edge, no forearm; skin tone and short pink French-tip nails stay the same "
                 "in every frame; the hand grips what it touches." if s["hand"] else " No hands and no people ever enter the frame."))
    url = run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
                    "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}})
    if url:
        fetch(url, f"clips/{sid}{'_seed' if not s['hand'] else ''}.mp4"); print("clip", sid, "ok", flush=True)


def clips(ids):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(len(ids)) as ex:
        list(ex.map(clip, ids))

EDITS = {   # targeted edits of an otherwise-good still (PLAYBOOK §6, BodyJ lesson: an edit fixes one item where fresh stills keep failing)
    "V1S3": ("stills/r2/V1S3.png", ["stills/look_ref.png", "refs/hand/bracelet_wrist.png"],
             "Edit image 1. Change ONLY the jewellery on the wrist: replace the rope-chain bracelet with the FLAT gold bracelet of flat rectangular links "
             "(like a watch band, no watch face) plus the thin gold chain with small pearls and a gold leaf charm, exactly as worn in image 2 and shown in "
             "image 3. Keep everything else identical: the hand, its grip on the rim, the blue ring, the nails, the heater, the room, the light, the framing."),
    "V1S5": ("stills/r3/V1S5.png", ["stills/look_ref.png"],
             "Edit image 1. Change ONLY the blue silicone ring: take it off the thumb and put it on the RING finger (the fourth finger), so the thumb has "
             "no ring and there is exactly one blue ring. Keep everything else identical: the hand, its grip on the mug, the bracelets, the nails, the "
             "mug, the heater, the room, the light, the framing."),
    "V1S4": ("stills/r1b/V1S4.png", ["refs/product_sheet.png"],   # Ralph 2026-10-19: heater looks too big
             "Edit image 1. Change ONLY the size of the black heater: make it much smaller, its true size of 8.7 inches tall, so its top reaches "
             "only about a third of the way up to the nightstand's glass top, standing on the floor in the same spot. Fill the space it no longer "
             "covers with the same floor, nightstand legs, cable and wall. Keep the heater's look exactly (image 2) and everything else identical."),
    "V1S9": ("stills/r1b/V1S9.png", ["refs/product_sheet.png"],   # Ralph 2026-10-19: heater looks too big
             "Edit image 1. Change ONLY the size of the black heater: make it much smaller, its true size of 8.7 inches tall, so its top reaches "
             "only about halfway up the sofa seat's front, standing on the rug a little in front of the sofa. Fill the space it no longer covers "
             "with the same rug, sofa and throw. Keep the heater's look exactly (image 2) and everything else identical."),
    "V1S8": ("stills/fix/V1S8_icons.png", ["refs/front_cutout.png"],   # icons already fixed free (tools/free_fix.py S8); only the window left
             "Edit image 1. Change ONLY the heater's front window: the rectangular heater window with vertical bars must sit BEHIND the black "
             "hexagon-hole mesh, exactly like the real heater in image 2: the mesh continues across the window, the bars show faintly through the "
             "holes, there is no raised frame or bezel around it. Keep everything else identical: the hand and every finger, the blue ring, the "
             "nails, the bracelets, the top panel and its buttons and display, the table, the room, the light and the framing."),
}


def edit(sid):
    src, extra, text = EDITS[sid]
    url = run_task({"model": "nano-banana-pro", "input": {"prompt": text, "image_input": [upload(src)] + [upload(p) for p in extra],
                                                          "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        fetch(url, f"stills/{sid}.png"); print("edit", sid, "ok", flush=True)


def edits(ids):
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(len(ids)) as ex:
        list(ex.map(edit, ids))


def sheet(kind, ext):
    """One labelled preview image: every still, or 4 frames per clip (one row per clip)."""
    files = sorted([f for f in Path(kind).glob(f"*{ext}") if f.stem in SHOTS], key=lambda p: (MAIN + list(SHOTS)).index(p.stem))
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
    cmd, ids = sys.argv[1], sys.argv[2:] or [s for s in MAIN if s.startswith("V1")]
    {"stills": stills, "clips": clips, "edits": edits}[cmd](ids)
