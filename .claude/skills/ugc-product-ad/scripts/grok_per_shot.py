"""One Grok Imagine Video 1.5 clip PER SHOT (Kie REST), then verify each.

Reference implementation from the Seller AI OS 30s tech UGC ad (2026-09-16). Adapt W, SHOTS and the
LOOK/AUDIO blocks; keep the structure. $0.0225/s at 720p, ~35s per shot, speech is lip-synced even
though Kie's schema lists no audio field.

Usage: python grok_per_shot.py s1 s3      (generate + verify the named shots)
Each shot animates from its OWN approved still. Never ask for counting gestures; state hand/prop
constraints as hard negatives (see SKILL.md "Prompt rules that each cost a retry here").
"""
import json, os, sys, time, subprocess, requests, concurrent.futures as cf
from pathlib import Path


def _gate():  # SCRIPT GATE (gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven; job dir = $UGC_JOB or cwd
    import os as _o, sys as _s, pathlib as _p; _s.path.insert(0, str(_p.Path(__file__).resolve().parent))
    from gate import require; require(_o.environ.get("UGC_JOB") or _o.getcwd())



W = Path("C:/dev/OpenMontage/projects/seller_ai_tech_ugc"); S = W / "stills"; O = W / "shots"; O.mkdir(exist_ok=True)
KEY = json.loads(Path(os.path.expanduser("~/.claude.json")).read_text(encoding="utf-8"))["mcpServers"]["kie-ai"]["env"]["KIE_AI_API_KEY"]
H = {"Authorization": f"Bearer {KEY}"}; API = "https://api.kie.ai/api/v1/jobs"
FFB = "C:/Users/ralph/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/"

LOOK = ("Realistic vertical 9:16 TikTok phone video continuing from the image: the same man, same face, full beard, thin black "
        "glasses, light blue oxford shirt with rolled sleeves and navy chinos, in his bright home office. Static phone camera "
        "propped on a shelf, natural daylight, authentic creator footage. ")
AUDIO = ("Audio: he says in a natural American male voice, energetic but with crisp articulation, every word pronounced fully "
         "and separately, short breath between sentences, just once: \"{line}\" Quiet room tone. No background music. "
         "No other dialogue. No on-screen text or captions. No logos.")

SHOTS = {
    "s1": {"still": "sb_couch_nologo.png", "duration": 5,
           "line": "Twelve products boxed up. Zero listings. Yeah, that was me.",
           "action": "He is slouched on the grey couch scrolling his phone, then looks up into the lens with a guilty half-smile "
                     "and waves one hand toward the stacked shipping boxes beside him, then shrugs."},
    "s3": {"still": "sb_desk_nologo.png", "duration": 6,
           "line": "Step one: fill in my shop setup once, so everything sounds like my brand.",
           "action": "He sits at the desk, types quickly on the laptop keyboard for a moment, then looks up into the lens and "
                     "talks while one hand makes a small explaining gesture, then goes back to typing."},
    "s4": {"still": "sb_desk_nologo.png", "duration": 6,
           "line": "Step two: paste the listing prompt. Title, tags, full description. Done.",
           "action": "THE LAPTOP STAYS FLAT ON THE DESK AT ALL TIMES: he never lifts it, never picks it up, never tilts or turns "
                     "it, and never shows its screen to the camera. His hands stay down at desk level near the keyboard. "
                     "He taps the trackpad as if pasting, glances down at the screen and nods once, then looks up into the "
                     "lens and talks with a small relaxed hand movement at desk height, finishing with a satisfied nod. "
                     "He never counts on his fingers and never holds up individual fingers."},
    "s5": {"still": "sb_desk_nologo.png", "duration": 5,
           "line": "Step three: run the SEO checklist so buyers can actually find it.",
           "action": "He leans toward the laptop and clicks a few times like ticking boxes, then sweeps an open flat palm toward "
                     "the screen and looks up into the lens with a confident smile and a small approving nod. He never counts "
                     "on his fingers and never holds up individual fingers."},
    "s6": {"still": "sb_desk_nologo.png", "duration": 4,
           "line": "Twelve listings up before my coffee got cold.",
           "action": "He leans back in his chair, picks up the white coffee mug, raises it slightly toward the lens with a proud "
                     "grin and takes a small sip at the end."},
    "s7": {"still": "sb_desk_nologo.png", "duration": 5,
           "line": "It's the Seller... A-I Operating System. Link in my bio.",
           "action": "He leans in toward the lens, friendly and direct, and on the words link in my bio points up with one "
                     "finger toward the top of the frame, holding the point with a smile."},
}


def upload(p: Path) -> str:
    with open(p, "rb") as f:
        r = requests.post("https://kieai.redpandaai.co/api/file-stream-upload", headers=H,
                          files={"file": (p.name, f)}, data={"uploadPath": "seller-ai-ugc", "fileName": p.name}, timeout=120)
    return r.json()["data"]["downloadUrl"]


def run(name: str, urls: dict):
    sh = SHOTS[name]
    prompt = LOOK + sh["action"] + " " + AUDIO.format(line=sh["line"])
    body = {"model": "grok-imagine-video-1-5-preview",
            "input": {"prompt": prompt, "image_urls": [urls[sh["still"]]], "duration": sh["duration"],
                      "resolution": "720p", "aspect_ratio": "9:16"}}
    _gate()
    r = requests.post(f"{API}/createTask", headers=H, json=body, timeout=60).json()
    tid = (r.get("data") or {}).get("taskId")
    if not tid:
        return name, f"SUBMIT FAIL {r}"
    t0 = time.time()
    while time.time() - t0 < 540:
        d = (requests.get(f"{API}/recordInfo", headers=H, params={"taskId": tid}, timeout=30).json().get("data") or {})
        if d.get("state") == "success":
            rj = json.loads(d["resultJson"]) if isinstance(d.get("resultJson"), str) else d.get("resultJson")
            (O / f"{name}.mp4").write_bytes(requests.get(rj["resultUrls"][0], timeout=180).content)
            (O / f"{name}_request.json").write_text(json.dumps({"task": tid, **body}, indent=1), encoding="utf-8")
            return name, f"OK {int(time.time()-t0)}s task={tid}"
        if d.get("state") == "fail":
            return name, f"FAIL {d.get('failCode')} {d.get('failMsg')} task={tid}"
        time.sleep(6)
    return name, f"TIMEOUT task={tid}"


def verify(name: str):
    f = O / f"{name}.mp4"
    if not f.exists():
        return
    dur = subprocess.run([FFB + "ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)],
                         capture_output=True, text=True).stdout.strip()
    vol = subprocess.run([FFB + "ffmpeg.exe", "-hide_banner", "-i", str(f), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True, errors="replace").stderr
    print("==", name, "dur", dur, " ".join(l.split("]")[-1].strip() for l in vol.splitlines() if "mean_volume" in l or "max_volume" in l))
    subprocess.run([FFB + "ffmpeg.exe", "-hide_banner", "-v", "error", "-y", "-i", str(f), "-vf",
                    "fps=2,scale=144:-2,tile=12x1", "-frames:v", "1", str(O / f"{name}_sheet.jpg")])
    from tools.tool_registry import registry
    registry.discover()
    tr = registry._tools["transcriber"].execute({"input_path": str(f), "model_size": "small", "language": "en"})
    print("   script:", SHOTS[name]["line"])
    for s in (tr.data or {}).get("segments", []):
        low = [(w.get("word"), round(w.get("probability", 0), 2)) for w in s.get("words", []) if w.get("probability", 1) < 0.8]
        print("  ", round(s["start"], 2), round(s["end"], 2), s["text"], "LOW:", low)


if __name__ == "__main__":
    names = sys.argv[1:]
    cache = W / "hosted_urls.json"
    urls = json.loads(cache.read_text())
    for st in {SHOTS[n]["still"] for n in names}:
        if st not in urls:
            urls[st] = upload(S / st)
    cache.write_text(json.dumps(urls, indent=1))
    with cf.ThreadPoolExecutor(len(names)) as ex:
        for n, m in ex.map(lambda n: run(n, urls), names):
            print(n, m)
    for n in names:
        verify(n)
