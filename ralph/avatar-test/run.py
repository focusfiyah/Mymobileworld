"""Ralph AI avatar test (2026-10-26, Ralph: "My face, test OK"): his real photo + his cloned voice line on
fal MiniMax H3 Max lip sync (768P) and Kie Kling AI Avatar Standard, side by side. Approved $1.80 in chat.

  python3 run.py prep <photo>   upright jpg in in/photo.jpg (EXIF rotation applied, long side <= 2048)
  python3 run.py go             upload, submit both at once, wait, download to out/
The Kie task goes through grace/paid.py (ledger, repeat guard); the fal spend is added to grace/spend.json other.
The Grace script gate (TikTok Shop research proofs) does not apply to this personal test.
"""
import datetime, hashlib, json, os, subprocess, sys, threading, time
from pathlib import Path
import requests

HERE = Path(__file__).resolve().parent; ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "grace")); import paid  # noqa: E402
KIE = "https://api.kie.ai/api/v1/jobs"; UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
FAL = "https://queue.fal.run/minimax/h3-max/lip-sync/image-to-video"
LOG = HERE / "run_log.json"; _L = threading.Lock()


def log(e):
    with _L:
        d = json.loads(LOG.read_text()) if LOG.exists() else []
        d.append({"t": time.strftime("%Y-%m-%d %H:%M:%S"), **e}); LOG.write_text(json.dumps(d, indent=1))


def upload(p):
    p = Path(p)
    r = requests.post(UPLOAD, files={"file": (p.name, p.read_bytes())}, data={"uploadPath": "ralph-avatar-test"}, timeout=120)
    url = r.json()["data"]["downloadUrl"]
    if hashlib.sha256(requests.get(url, timeout=60).content).digest() != hashlib.sha256(p.read_bytes()).digest():
        sys.exit(f"hosted copy of {p} differs; not submitting")
    return url


VO = HERE / os.environ.get("VO", "vo/line_cbx.wav")   # free Chatterbox voice (default, 2026-10-29); VO=vo/line.mp3 = ElevenLabs


def audio_s():
    return float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(VO)]))


def kie(img, aud):
    body = {"model": "kling/ai-avatar-standard",
            "input": {"image_url": img, "audio_url": aud, "prompt": (HERE / "kling_prompt.txt").read_text().strip()}}
    usd = round(audio_s() * 0.04, 3)
    key = paid.claim(HERE, body, usd, "kling avatar test")
    r = requests.post(f"{KIE}/createTask", json=body, timeout=60).json(); tid = (r.get("data") or {}).get("taskId")
    paid.submitted(HERE, key, tid); log({"kie_request": body, "kie_response": r})
    if not tid: print("KIE createTask failed", r); return
    while True:
        time.sleep(10)
        d = (requests.get(f"{KIE}/recordInfo", params={"taskId": tid}, timeout=30).json() or {}).get("data") or {}
        if d.get("state") in ("success", "fail"): break
    log({"kie_result": d})
    if d.get("state") != "success": print("KIE failed", d.get("failMsg")); return
    url = json.loads(d["resultJson"])["resultUrls"][0]
    (HERE / "out/kling_avatar.mp4").write_bytes(requests.get(url, timeout=300).content); print("KIE OK", tid)


def fal(img, aud):
    body = {"image_url": img, "audio_url": aud, "resolution": "768P"}
    r = requests.post(FAL, json=body, timeout=60).json(); log({"fal_request": body, "fal_response": r})
    if "status_url" not in r: print("FAL submit failed", r); return
    usd = round(audio_s() * 0.08 * (1.2 if audio_s() > 15 else 1), 3)
    sp = ROOT / "grace/spend.json"
    with _L:
        s = json.loads(sp.read_text())
        s["other"].append({"date": datetime.date.today().isoformat(), "job": "ralph/avatar-test", "service": "fal.ai",
                           "what": f"MiniMax H3 Max lip sync 768P, {audio_s():.1f} s, request {r['request_id']}", "usd": usd,
                           "ok": "Ralph 2026-10-26 \"My face, test OK\" (plan $1.80 in chat)"})
        sp.write_text(json.dumps(s, indent=1) + "\n")
    while True:
        time.sleep(10)
        st = requests.get(r["status_url"], timeout=30).json()
        if st.get("status") == "COMPLETED": break
        if st.get("status") not in ("IN_QUEUE", "IN_PROGRESS"): print("FAL status", st); return
    res = requests.get(r["response_url"], timeout=60).json(); log({"fal_result": res})
    url = (res.get("video") or {}).get("url")
    if not url: print("FAL no video", res); return
    (HERE / "out/h3max.mp4").write_bytes(requests.get(url, timeout=300).content); print("FAL OK", r["request_id"])


if __name__ == "__main__":
    if sys.argv[1] == "prep":
        from PIL import Image, ImageOps
        im = ImageOps.exif_transpose(Image.open(sys.argv[2])).convert("RGB"); im.thumbnail((2048, 2048))
        im.save(HERE / "in/photo.jpg", quality=95); print("in/photo.jpg", im.size, round(im.size[0] / im.size[1], 2))
    elif sys.argv[1] == "go":
        img, aud = upload(HERE / "in/photo.jpg"), upload(VO); print(img, aud)
        ts = [threading.Thread(target=f, args=(img, aud)) for f in (kie, fal)]
        [t.start() for t in ts]; [t.join() for t in ts]
