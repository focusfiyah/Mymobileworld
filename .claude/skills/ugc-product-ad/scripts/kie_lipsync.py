"""Re-drive each shot's mouth from a cloned-voice track: Kie `volcengine/video-to-video-lip-sync`.

Reference implementation from the Seller AI OS tech UGC ad (2026-09-16). Adapt W, VO and PAIRS.

$0.04/s, mode "lite", `align_audio: true`. Output length follows the AUDIO, so keep each VO shorter
than its clip. Use this only when ONE cloned voice must carry every cut; keeping each clip's own
generated audio is free and its mouth already matches.

AFTERWARDS, always mux the original mp3 back on:
    ffmpeg -i sN_vo.mp4 -i lineN.mp3 -map 0:v -map 1:a -c:v copy -c:a aac -shortest out.mp4
The lip-sync step re-encodes the audio and degrades it ("Seller" came back as "Cellar" on BOTH
whisper models). The mouth still matches, because that same audio drove it.

Kie returns 500 "The server is busy" under parallel load; failed tasks cost $0, so just retry.
"""
import json, os, time, subprocess, requests, concurrent.futures as cf
from pathlib import Path
W = Path("C:/dev/OpenMontage/projects/seller_ai_tech_ugc"); O = W / "lipsync"; O.mkdir(exist_ok=True)
VO = Path("C:/Users/ralph/Desktop/Ralph UGC assets/vo_lines")
KEY = json.loads(Path(os.path.expanduser("~/.claude.json")).read_text(encoding="utf-8"))["mcpServers"]["kie-ai"]["env"]["KIE_AI_API_KEY"]
H = {"Authorization": f"Bearer {KEY}"}; API = "https://api.kie.ai/api/v1/jobs"
FFB = "C:/Users/ralph/AppData/Local/Microsoft/WinGet/Packages/Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe/ffmpeg-8.1.2-full_build/bin/"
PAIRS = {f"s{i}": f"line{i}.mp3" for i in range(1, 8)}
LINES = {
 "s1": "Twelve products boxed up. Zero listings. Yeah, that was me.",
 "s2": "Okay. Let's actually get these listed.",
 "s3": "Step one: fill in my shop setup once, so everything sounds like my brand.",
 "s4": "Step two: paste the listing prompt. Title, tags, full description. Done.",
 "s5": "Step three: run the SEO checklist so buyers can actually find it.",
 "s6": "Twelve listings live before my coffee got cold.",
 "s7": "It's the Seller AI Operating System. Link in my bio.",
}
def upload(p: Path) -> str:
    with open(p, "rb") as f:
        r = requests.post("https://kieai.redpandaai.co/api/file-stream-upload", headers=H,
                          files={"file": (p.name, f)}, data={"uploadPath": "seller-ai-ugc", "fileName": p.name}, timeout=180)
    return r.json()["data"]["downloadUrl"]
def run(shot):
    vid = upload(W / "shots" / f"{shot}.mp4"); aud = upload(VO / PAIRS[shot])
    body = {"model": "volcengine/video-to-video-lip-sync",
            "input": {"mode": "lite", "video_url": vid, "audio_url": aud, "align_audio": True}}
    _gate()
    r = requests.post(f"{API}/createTask", headers=H, json=body, timeout=60).json()
    tid = (r.get("data") or {}).get("taskId")
    if not tid: return shot, f"SUBMIT FAIL {r}"
    t0 = time.time()
    while time.time() - t0 < 540:
        d = (requests.get(f"{API}/recordInfo", headers=H, params={"taskId": tid}, timeout=30).json().get("data") or {})
        if d.get("state") == "success":
            rj = json.loads(d["resultJson"]) if isinstance(d.get("resultJson"), str) else d.get("resultJson")
            (O / f"{shot}_vo.mp4").write_bytes(requests.get(rj["resultUrls"][0], timeout=180).content)
            return shot, f"OK {int(time.time()-t0)}s"
        if d.get("state") == "fail": return shot, f"FAIL {d.get('failCode')} {d.get('failMsg')}"
        time.sleep(8)
    return shot, f"TIMEOUT task={tid}"
with cf.ThreadPoolExecutor(7) as ex:
    for s, m in sorted(ex.map(run, PAIRS)): print(s, m)
from tools.tool_registry import registry


def _gate():  # SCRIPT GATE (gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven; job dir = $UGC_JOB or cwd
    import os as _o, sys as _s, pathlib as _p; _s.path.insert(0, str(_p.Path(__file__).resolve().parent))
    from gate import require; require(_o.environ.get("UGC_JOB") or _o.getcwd())


registry.discover()
for s in PAIRS:
    f = O / f"{s}_vo.mp4"
    if not f.exists(): continue
    dur = subprocess.run([FFB+"ffprobe.exe","-v","error","-show_entries","format=duration","-of","csv=p=0",str(f)],capture_output=True,text=True).stdout.strip()
    vol = subprocess.run([FFB+"ffmpeg.exe","-hide_banner","-i",str(f),"-af","volumedetect","-f","null","-"],capture_output=True,text=True,errors="replace").stderr
    mean = next((l.split("]")[-1].strip() for l in vol.splitlines() if "mean_volume" in l), "?")
    tr = registry._tools["transcriber"].execute({"input_path": str(f), "model_size": "small", "language": "en"})
    txt = " ".join(x["text"].strip() for x in (tr.data or {}).get("segments", []))
    print(f"{s} dur={dur} {mean} | {txt}")
    print(f"   want: {LINES[s]}")
