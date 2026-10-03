"""Submit a Restlex skit clip to Kie Seedance 2.0 Mini via REST, download, and verify.

Kie's MCP tool only exposes Seedance 2.5, so Mini goes through the REST API.
Usage: python kie_seedance_mini.py clip2 v1            (submit)
       python kie_seedance_mini.py clip2 v1 <taskId>   (resume polling an existing task)
"""
import json
import os
import subprocess
import sys
import time
from pathlib import Path

import requests


def _gate():  # SCRIPT GATE (gate.py, Ralph 2026-10-03): no paid call until the PLAYBOOK §4 checklist is proven; job dir = $UGC_JOB or cwd
    import os as _o, sys as _s, pathlib as _p; _s.path.insert(0, str(_p.Path(__file__).resolve().parent))
    from gate import require; require(_o.environ.get("UGC_JOB") or _o.getcwd())



P = Path("C:/dev/OpenMontage/projects/restlex-couple-skit")
R = P / "renders"
API = "https://api.kie.ai/api/v1/jobs"
URLS = json.loads((P / "assets" / "video_refs" / "hosted_urls.json").read_text())
REFS = [URLS["scene_bottle"], URLS["az"], URLS["wife"], URLS["product"]]

PROMPTS = {
    "clip2": (
        "Vertical 9:16 family-friendly sitcom-style comedy sketch, filmed like a realistic TikTok phone video, late at night. "
        "A married couple, both fully dressed in sleepwear, lying in bed. "
        "Reference image 1 shows the exact bedroom, both people, the lighting and how the Restlex bottle looks when she holds it: "
        "dark espresso-brown wooden headboard, dusty mauve pillows, brown-grey checked duvet, window with sheer curtains and a "
        "streetlight outside, warm bedside-lamp light, faces clearly lit. The husband is on the LEFT side of the bed and the wife "
        "on the RIGHT, the whole time. "
        "Reference image 2 is the husband, Az: keep his face, shoulder-length locs, beard and navy t-shirt. "
        "Reference image 3 is the wife: keep her face, long box braids and cream knit sweater. "
        "Reference image 4 is the product: a white Approved Science RESTLEX +BIOPERINE supplement bottle with a white ribbed cap "
        "and navy-striped label; it looks like a real bottle about the size of her hand, lit by the room, label readable. "
        "THE RESTLESS LEG MUST BE CLEARLY VISIBLE: Az's bare lower leg and foot stick out from under the edge of the duvet on his "
        "side, and the viewer plainly sees the leg jerking and kicking on its own. "
        "At the start the bottle stands on the wife's nightstand. "
        "Shot 1 (0-2s): close-up of Az's bare foot and lower leg kicking out from under the edge of the duvet, clearly visible. "
        "Shot 2 (2-4s): medium close-up of the wife propped on one elbow, looking at her husband, tired and fed up. "
        "She says: \"Then take your leg pill!\" "
        "Shot 3 (4-6.5s): two-shot from beside the bed. She picks up the Restlex bottle from her nightstand and holds it up next "
        "to his face, label facing the camera. He takes it and says: \"Okay, okay...\" "
        "Shot 4 (6.5-10s): wide shot from the foot of the bed. She says: \"Because I'm not losing sleep over your legs tonight.\" "
        "She turns over, facing away from him, and pulls the blanket up over her head. He lies there holding the bottle, label "
        "toward the camera, with an apologetic look, while his foot still twitches at the edge of the duvet. "
        "Audio: only those spoken lines, in natural American English with light comedic timing - the wife tired and exasperated "
        "in a female voice, the husband sleepy and apologetic in a male voice. Quiet room tone and blanket rustle when the leg "
        "kicks. No background music. No other dialogue. No on-screen text or captions."
    ),
}


PROMPTS["clip1"] = (
    "Vertical 9:16 family-friendly sitcom-style comedy sketch, filmed like a realistic TikTok phone video, late at night. "
    "A married couple, both fully dressed in sleepwear, asleep in bed. "
    "Reference image 1 shows the exact bedroom, both people and the lighting: dark espresso-brown wooden headboard, dusty "
    "mauve pillows, brown-grey checked duvet, window with sheer curtains and a streetlight outside, warm bedside-lamp light, "
    "faces clearly lit, and a white supplement bottle standing on the wife's nightstand. They lie a little apart, not "
    "cuddling. The husband is on the LEFT side of the bed and the wife on the RIGHT, the whole time. "
    "Reference image 2 is the husband, Az: keep his face, shoulder-length locs, beard and navy t-shirt. "
    "Reference image 3 is the wife: keep her face, long box braids and cream knit sweater. "
    "The bottle stays on the nightstand; nobody holds it in this clip. "
    "THE RESTLESS LEG MUST BE CLEARLY VISIBLE AND IT IS THE WHOLE LEG: Az's lower leg sticks out from under the edge of the "
    "duvet; the knee bends and straightens and the calf kicks out in sudden jerks, the duvet over his knee jumping - not "
    "just the foot. "
    "Shot 1 (0-2s): close-up of Az's leg at the edge of the bed kicking in sudden jerks, the whole leg moving from the knee. "
    "Shot 2 (2-6s): close-up of the wife jolting awake on her pillow, eyes snapping open, annoyed, turning toward him. "
    "She says loudly: \"Az! What the heck?! I hate when your legs start shaking like that!\" "
    "Shot 3 (6-10s): close-up of Az, groggy and apologetic, eyes half open. He says: "
    "\"I know, baby. I'm sorry. I can't help it.\" "
    "Audio: only those spoken lines, in natural American English with light comedic timing - the wife exasperated in a "
    "female voice, the husband sleepy and apologetic in a male voice. Quiet room tone. No background music. No other "
    "dialogue. No on-screen text or captions."
)

# Per-clip reference sets; clip 1 uses the asleep wide shot so the bottle stays on the nightstand.
CLIP_REFS = {"clip1": ["wide_asleep", "az", "wife"]}


# Short inserts animate from a first frame (mutually exclusive with reference images on Mini).
INSERTS = {
    "leg_insert": {
        "first_frame": "leg_first_frame",
        "duration": 4,
        "prompt": (
            "Realistic close-up phone footage at night, continuing exactly from the first frame: a man's bare leg "
            "sticking out from under a brown-grey checked duvet at the edge of the bed, warm bedside-lamp light. "
            "Restless legs: his WHOLE LEG moves, not just the foot. The thigh under the duvet lurches, the knee bends "
            "and straightens, and the calf and foot kick out sharply several times in sudden uncontrollable jerks, "
            "the duvet over his thigh visibly jumping with each kick; a brief pause, then another hard jerk of the "
            "whole leg. The foot itself stays mostly relaxed; the movement comes from the knee and hip. "
            "Static camera, same framing, same bed, same lighting as the first frame. Only this one leg in shot, no "
            "faces. Audio: blanket rustle and soft thumps of the kicks, quiet room tone. No music, no dialogue, "
            "no on-screen text."
        ),
    },
}


INSERTS["leg_insert_ref"] = {
    "refs": ["leg_first_frame", "scene_bottle"],
    "duration": 4,
    "prompt": (
        "Reference image 1 shows the exact close-up framing: the husband's lower leg and foot at the edge of the bed "
        "under a brown-grey checked duvet, warm bedside-lamp light at night. Reference image 2 shows the same bedroom. "
        "Family-friendly sitcom insert shot; the husband is fully dressed in sleepwear. His restless leg acts up: the "
        "whole leg jerks, the knee bends and straightens and the calf kicks out several times, the duvet over his knee "
        "visibly jumping with each jerk, then a brief pause and one more hard jerk. The foot stays mostly relaxed; the "
        "motion comes from the knee, not the ankle. Static camera, same framing and lighting as reference image 1. "
        "No faces in shot. Audio: blanket rustle and soft thumps of the kicks, quiet room tone. No music, no "
        "dialogue, no on-screen text."
    ),
}


def kie_key() -> str:
    """Read the Kie key from the user-scope MCP config. Never print it."""
    cfg = json.loads(Path(os.path.expanduser("~/.claude.json")).read_text(encoding="utf-8"))
    return cfg["mcpServers"]["kie-ai"]["env"]["KIE_AI_API_KEY"]


def submit(clip: str, headers: dict, record: dict) -> str:
    if clip in INSERTS:
        spec = INSERTS[clip]
        if "first_frame" in spec:
            media = {"first_frame_url": URLS[spec["first_frame"]]}
        else:  # reference mode passed Kie compliance where first-frame mode was rejected
            media = {"reference_image_urls": [URLS[k] for k in spec["refs"]]}
        prompt, duration = spec["prompt"], spec["duration"]
    else:
        media = {"reference_image_urls": [URLS[k] for k in CLIP_REFS[clip]] if clip in CLIP_REFS else REFS}
        prompt, duration = PROMPTS[clip], 10
    body = {
        "model": "bytedance/seedance-2-mini",
        "input": {
            "prompt": prompt,
            **media,
            # Inserts are spliced under the main clip's audio; their own audio tripped Kie's copyright audit twice.
            "generate_audio": clip not in INSERTS,
            "resolution": "720p",
            "aspect_ratio": "9:16",
            "duration": duration,
        },
    }
    _gate()
    r = requests.post(f"{API}/createTask", headers=headers, json=body, timeout=60)
    try:
        resp = r.json()
    except ValueError:
        resp = {"raw": r.text[:500]}
    print("createTask HTTP", r.status_code, json.dumps(resp)[:400])
    record.update({"submitted_at": time.strftime("%Y-%m-%d %H:%M:%S"), "request": body, "create_response": resp})
    return (resp.get("data") or {}).get("taskId")


def poll(task_id: str, headers: dict, record: dict) -> str | None:
    deadline, last_state = time.time() + 540, None
    while time.time() < deadline:
        q = requests.get(f"{API}/recordInfo", headers=headers, params={"taskId": task_id}, timeout=30)
        try:
            data = (q.json() or {}).get("data") or {}
        except ValueError:
            data = {}
        state = data.get("state")
        if state != last_state:
            print(time.strftime("%H:%M:%S"), "state:", state, "| HTTP", q.status_code)
            last_state = state
        if state == "success":
            rj = data.get("resultJson")
            rj = json.loads(rj) if isinstance(rj, str) and rj else (rj or {})
            urls = rj.get("resultUrls") or data.get("resultUrls") or []
            record["result"] = {"resultJson": rj, "costTime": data.get("costTime"), "completeTime": data.get("completeTime")}
            return urls[0] if urls else None
        if state == "fail":
            record["result"] = {"failCode": data.get("failCode"), "failMsg": data.get("failMsg")}
            print("FAILED:", data.get("failCode"), data.get("failMsg"))
            return None
        if q.status_code != 200 and not state:
            print("recordInfo unexpected:", q.status_code, q.text[:300])
        time.sleep(10)
    print("TIMEOUT waiting for task", task_id)
    return None


def verify(out: Path) -> None:
    probe = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration", "-show_entries",
         "stream=codec_type,width,height", "-of", "default=noprint_wrappers=1", str(out)],
        capture_output=True, text=True)
    print(probe.stdout.strip())
    vol = subprocess.run(["ffmpeg", "-hide_banner", "-i", str(out), "-af", "volumedetect", "-f", "null", "-"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace").stderr
    print("\n".join(line.strip() for line in vol.splitlines() if "mean_volume" in line or "max_volume" in line))
    sheet = out.with_name(out.stem + "_sheet.jpg")
    subprocess.run(["ffmpeg", "-hide_banner", "-v", "error", "-y", "-i", str(out), "-vf",
                    "fps=1,scale=200:-2,tile=5x2", "-frames:v", "1", str(sheet)])
    print("sheet", sheet, sheet.exists())

    from tools.tool_registry import registry
    registry.discover()
    tr = registry._tools["transcriber"].execute({"input_path": str(out), "model_size": "small", "language": "en"})
    for s in (tr.data or {}).get("segments", []):
        low = [f"{w.get('word', '').strip()}({w.get('probability', 1):.2f})" for w in (s.get("words") or [])
               if (w.get("probability") or 1) < 0.8]
        print(f"{s.get('start', 0):5.2f}-{s.get('end', 0):5.2f} {s.get('text', '').strip()}",
              ("LOW: " + " ".join(low)) if low else "")


def main() -> None:
    clip, version = sys.argv[1], sys.argv[2]
    resume_id = sys.argv[3] if len(sys.argv) > 3 else None
    headers = {"Authorization": f"Bearer {kie_key()}", "Content-Type": "application/json"}
    R.mkdir(exist_ok=True)
    rec_path = R / f"{clip}_mini_{version}.json"
    record = json.loads(rec_path.read_text()) if rec_path.exists() else {}

    task_id = resume_id or submit(clip, headers, record)
    rec_path.write_text(json.dumps(record, indent=2))
    if not task_id:
        sys.exit("no taskId returned - see create_response in " + str(rec_path))
    record["task_id"] = task_id
    rec_path.write_text(json.dumps(record, indent=2))
    print("taskId", task_id)

    video_url = poll(task_id, headers, record)
    rec_path.write_text(json.dumps(record, indent=2))
    if not video_url:
        sys.exit(f"no video; resume with: python kie_seedance_mini.py {clip} {version} {task_id}")

    out = R / f"{clip}_mini_{version}.mp4"
    out.write_bytes(requests.get(video_url, timeout=300).content)
    print("downloaded", out, round(out.stat().st_size / 1024), "KB")
    verify(out)


if __name__ == "__main__":
    main()
