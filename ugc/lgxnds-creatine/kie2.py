"""v2 runner (2026-10-18). Reuses kie.py's upload/run_task (script gate runs before every paid call).
  python3 kie2.py stills S3          one still ($0.09) -> stills_v2/S3.png (then label.py paste-back, free)
  python3 kie2.py clips S2 ...       Kling 3.0 Omni ($0.07/s) or Seedance Mini ($0.041/s) per shots_v2.json -> clips_v2/
Stills use the APPROVED test still as an extra look reference once it exists (PLAYBOOK §6: one test still first)."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

V = json.loads(Path("shots_v2.json").read_text())
S = {s["id"]: s for s in V["shots"]}
HAND = ["refs/v2/hand_french_bare.png"]  # Grace bare hand, French tips (Ralph 2026-10-19)
BRACELET, TUB, ROOM = "refs/v2/bracelet_crop.png", "refs/crop_tub_hi.png", "refs/v2/kitchen_ralph.jpg"
LOOK = "stills_v2/look_ref.png"   # copy of the approved test still


def text(s):
    parts = [s["still"], V["identity_block"] if s["hand"] else "No hand and no people anywhere in the frame."]
    if s["tub"]: parts.append(V["tub_block"])
    if s["powder"]: parts.append(V["powder_block"])
    parts.append(V["scene_block"])
    return " ".join(parts)


def still(sid):
    s = S[sid]
    refs = ([kie.upload(p) for p in HAND] + [kie.upload(BRACELET)] if s["hand"] else []) + ([kie.upload(TUB)] if s["tub"] else []) + [kie.upload(ROOM)]
    note = " Reference images: hand photos (skin, nails), the gold bracelet, " + ("the real LGXNDS tub, " if s["tub"] else "") + "and the kitchen (match it)."
    if Path(LOOK).exists():
        refs.append(kie.upload(LOOK)); note += " The last reference image is an approved frame from this same video: match its light, kitchen, hand and bracelet exactly."
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text(s) + note
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills_v2/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    s = S[sid]; first = kie.upload(f"stills_v2/{sid}_label.png" if s["tub"] else f"stills_v2/{sid}.png")
    prompt = f"{s['video']} {V['video_suffix']}"
    if s["model"] == "kling":
        body = {"model": "kling-3.0-omni/image-to-video", "input": {"prompt": prompt, "image_urls": [first, first] if s.get("last_frame_same") else [first],
                "duration": s["dur"], "resolution": "720p", "aspect_ratio": "auto", "audio": False}}
    else:
        body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": first, "generate_audio": False,
                "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
    url = kie.run_task(body)
    if url:
        kie.fetch(url, f"clips_v2/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    for d in ("stills_v2", "clips_v2"): Path(d).mkdir(exist_ok=True)
    fn = still if kind == "stills" else clip
    with ThreadPoolExecutor(max(1, len(ids))) as ex:
        list(ex.map(fn, ids))
