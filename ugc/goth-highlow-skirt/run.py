"""Goth High-Low Skirt (Grace) runner, 2026-10-22. Script gate runs before every paid call (kie.run_task / omni_clip.py).
  python3 run.py prompt S2          print the still prompt (free)
  python3 run.py stills S2 [S1 ..]   Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png, in parallel
  python3 run.py omni S2 [--dry]     Google Omni 1.1 Flash on Kie, 4 s $0.315 (product lock; the skirt is in every shot)
  python3 run.py edit SRC OUT PROMPT nano-banana-pro edit of an approved still ($0.09): image 1 = SRC, 2 = sheet, 3 = tie
  python3 run.py omnifl S2 FIRST LAST [--dry]  Omni first+last frame mode, 4 s $0.315 (Ralph 2026-10-22: the hem must rise
                                     from the top of the knee to mid-thigh like the inspo; reference mode only moved it a little)
Prompts written with prompt-master (Ralph's stack): numbered real references named in the prompt, colour matched, one motion, no text."""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

SHEET, TIE, RUCH, HAND, LOOK = "refs/product_sheet.png", "refs/closeup_tie.png", "refs/closeup_ruching.png", "../../grace/ref/hand-sheets/with_bracelet.jpg", "stills/S2.png"
HANDS = {"S2"}
ROOM = "refs/room.jpg"
OMNI = "../../.claude/skills/ugc-product-ad/scripts/omni_clip.py"


def still_prompt(sid):
    look = Path("prompts/look.txt").read_text().strip()
    p = Path(f"prompts/{sid}_still.txt").read_text().replace("<<LOOK>>", look)
    refs = [SHEET, TIE, RUCH] + ([HAND] if sid in HANDS else [LOOK]) + [ROOM]
    return refs, "Vertical 9:16 photo, a single frame from a phone-shot mirror video. " + p


def still(sid):
    refs, prompt = still_prompt(sid)
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def omni(sid, dry=False):
    refs = [TIE, RUCH, SHEET] + ([HAND] if sid in HANDS else [])  # S4 starts from the S3 still (free route, Ralph 2026-10-22)
    cmd = ["python3", OMNI, ".", sid, "--prompt-file", f"prompts/{sid}_clip.txt", "--still", f"stills/{sid}.png", "--seconds", "4"]
    for r in refs: cmd += ["--ref", r]
    subprocess.run(cmd + (["--dry"] if dry else []), check=False)


LEN = {"ONELEG2": "refs/inspo_len/len_one_leg.png", "FULL2": "refs/inspo_len/len_top_of_knee.png", "FULL": "refs/inspo_len/len_top_of_knee.png", "TOP": "refs/inspo_len/len_top_of_knee.png", "ONELEG": "refs/inspo_len/len_one_leg.png", "SHORT": "refs/inspo_len/len_shortest.png"}


def len_still(sid):
    """Fresh still for one skirt length (Ralph 2026-10-22: all 5 inspo looks). Edits did not change the length, so the
    inspo frame (caption painted out) goes in as a length-only guide."""
    import json
    shot = json.loads(Path("prompts/len_shots.json").read_text())[sid]
    look = Path("prompts/look.txt").read_text().strip()
    if sid in ("FULL", "FULL2", "ONELEG2"):   # Kling motion control needs a whole person: drop the waist-down framing line for this one still
        look = "\n".join(l for l in look.splitlines() if not l.startswith("LOOK:")) + "\nLOOK: vertical 9:16 phone photo in a mirror, full body head to boots. Bright, neutral, natural colour, no yellow or golden tint. No text, no watermark."
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot mirror video. " + Path("prompts/len_still.txt").read_text().replace("<<LOOK>>", look).replace("<<SHOT>>", shot)
    if sid in ("FULL", "FULL2", "ONELEG2"): prompt = prompt.replace("the light and the framing MUST match image 3 exactly", "the light MUST match image 3 (framing here is full body)")
    refs = (SHEET, TIE, LOOK, LEN[sid])
    if sid == "ONELEG2":   # keyframe for the Kling keyframe take: same framing as FULL2 / K4 (Ralph 2026-10-22)
        refs = (SHEET, TIE, "stills/FULL2.png", LEN[sid], "../../grace/ref/grace_reference_sheet.png")
        prompt += (" Image 3 is the approved frame of the SAME woman in the SAME framing: keep everything in it except the skirt length on one side. "
                   "Image 5 is Grace's reference sheet: her face, skin and braids MUST match it. No phone anywhere.")
    if sid == "FULL2":   # r1 drew a stranger: give Grace's own sheet + the full-body still of her in Ralph's bedroom
        refs = (SHEET, TIE, "stills/FULL.png", LEN[sid], "../../grace/ref/grace_reference_sheet.png")
        prompt += (" Image 3 here is a full-body frame of the SAME woman in the SAME bedroom: match her body, skin, braids, outfit, boots, room and light. "
                   "Image 5 is Grace's reference sheet: her face, medium-dark brown skin and long dark boho braids MUST match it; she is Grace, not anyone else. "
                   "Her hands hold ONLY the two skirt ties; there is no phone in her hands or anywhere in the picture.")
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def seed(sid, first, last=None, secs=4):
    """Seedance 2.0 Mini on Kie ($0.041/s), first frame (+ optional last frame). Ralph 2026-10-22: Omni ignored the end
    frame twice, so the pulls are filmed as the skirt dropping and played reversed in the cut (reverse route)."""
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": Path(f"prompts/{sid}_seed.txt").read_text().strip(),
            "first_frame_url": kie.upload(first), "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": secs}}
    if last: body["input"]["last_frame_url"] = kie.upload(last)
    url = kie.run_task(body)
    if url:
        Path("clips").mkdir(exist_ok=True); n = len(list(Path("clips").glob(f"{sid}_seed_*.mp4"))) + 1
        kie.fetch(url, f"clips/{sid}_seed_{n}.mp4"); print("OK", f"clips/{sid}_seed_{n}.mp4", flush=True)


def veo(sid, first, tier="veo3_fast", secs=6):
    """Google Veo 3.1 on Kie, first-frame image-to-video, 9:16 720p (veo3_fast 60 credits = $0.30; same call as
    ugc/throw-hands-rps/kie.py). Ralph 2026-10-22: test whether Veo can do the drawstring rise Omni/Seedance could not."""
    url = kie.run_task({"model": "veo-3-1", "input": {"model": tier, "generation_type": "FIRST_AND_LAST_FRAMES_2_VIDEO",
        "prompt": Path(f"prompts/{sid}_veo.txt").read_text().strip(), "image_urls": [kie.upload(first)],
        "aspect_ratio": "9:16", "duration": secs, "resolution": "720p"}})
    if url:
        Path("clips").mkdir(exist_ok=True); n = len(list(Path("clips").glob(f"{sid}_veo_*.mp4"))) + 1
        kie.fetch(url, f"clips/{sid}_veo_{n}.mp4"); print("OK", f"clips/{sid}_veo_{n}.mp4", flush=True)


def kie_kling(sid, first, secs=5):
    """Kling 3.0 Omni on Kie ($0.07/s; same call as ugc/lgxnds-creatine/kie2.py). Ralph 2026-10-22: continue V4 from its
    last frame so the shortest look (both legs) joins with no visible cut; his own Kling account had 8 credits left."""
    url = kie.run_task({"model": "kling-3.0-omni/image-to-video", "input": {"prompt": Path(f"prompts/{sid}_kie.txt").read_text().strip(),
                        "image_urls": [kie.upload(first)], "duration": secs, "resolution": "720p", "aspect_ratio": "auto", "audio": False}})
    if url:
        Path("clips").mkdir(exist_ok=True); kie.fetch(url, f"clips/{sid}_kie.mp4"); print("OK", f"clips/{sid}_kie.mp4", flush=True)


def edit(src, out, prompt_file):
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": Path(prompt_file).read_text().strip(),
                        "image_input": [kie.upload(r) for r in (src, SHEET, TIE)], "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, out); print("edit", out, "ok", flush=True)


def omnifl(sid, first, last, dry=False):
    """Omni on Kie, first_frame_url + last_frame_url (no reference images in this mode; both frames carry the real skirt)."""
    import json, requests
    prompt = Path(f"prompts/{sid}_fl_clip.txt").read_text().strip()
    print(f"{sid}: Kie google/gemini-omni-flash-1-1 first+last 4s 1080p 9:16 -> $0.315"); print(prompt)
    if dry: return
    body = {"model": "google/gemini-omni-flash-1-1", "input": {"prompt": prompt, "duration": "4", "aspect_ratio": "9:16",
            "resolution": "1080p", "first_frame_url": kie.upload(first), "last_frame_url": kie.upload(last)}}
    url = kie.run_task(body)
    if not url: return
    Path("clips").mkdir(exist_ok=True); n = len(list(Path("clips").glob(f"{sid}_omni_*.mp4"))) + 1
    raw = f"clips/{sid}_omni_{n}.mp4"; kie.fetch(url, raw)
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", raw, "-an", "-c:v", "copy", f"clips/{sid}.mp4"], check=True)


if __name__ == "__main__":
    cmd, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if cmd == "prompt":
        for i in ids: r, p = still_prompt(i); print(r); print(p)
    elif cmd == "stills":
        Path("stills").mkdir(exist_ok=True)
        with ThreadPoolExecutor(4) as ex: list(ex.map(still, ids))
    elif cmd == "len":
        with ThreadPoolExecutor(3) as ex: list(ex.map(len_still, ids))
    elif cmd == "seed":
        seed(ids[0], ids[1], ids[2] if len(ids) > 2 else None)
    elif cmd == "veo":
        veo(ids[0], ids[1])
    elif cmd == "kiekling":
        kie_kling(ids[0], ids[1])
    elif cmd == "edit":
        edit(*ids[:3])
    elif cmd == "omnifl":
        omnifl(ids[0], ids[1], ids[2], "--dry" in sys.argv)
    elif cmd == "omni":
        with ThreadPoolExecutor(4) as ex: list(ex.map(lambda i: omni(i, "--dry" in sys.argv), ids))
