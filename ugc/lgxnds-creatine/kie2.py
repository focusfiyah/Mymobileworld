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
BRACELET, ROOM = "refs/v2/bracelet_crop.png", "refs/v2/kitchen_ralph.jpg"
TUB = ["refs/v2/product_sheet.png", "refs/crop_tub_hi.png"]   # product reference sheet (Ralph 2026-10-19) + real front label
LOOK = "stills_v2/look_ref.png"   # copy of the approved test still


def text(s):
    parts = [s["still"], V["identity_block"] if s["hand"] else "No hand and no people anywhere in the frame."]
    if s["tub"]: parts.append(V["tub_block"])
    if s["powder"]: parts.append(V["powder_block"])
    parts.append(V["scene_block"])
    return " ".join(parts)


def still(sid):
    s = S[sid]
    refs = ([kie.upload(p) for p in HAND] + [kie.upload(BRACELET)] if s["hand"] else []) + ([kie.upload(p) for p in TUB] if s["tub"] else []) + [kie.upload(ROOM)]
    note = " Reference images: hand photos (skin, nails), the gold bracelet, " + ("the LGXNDS product reference sheet (the big front view is the real label; small views = side, top, bottom shape), a close-up of the real front label, " if s["tub"] else "") + "and the kitchen (match it)."
    if Path(LOOK).exists():
        refs.append(kie.upload(LOOK)); note += " The last reference image is an approved frame from this same video: match its light, kitchen, hand and bracelet exactly."
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text(s) + note
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        kie.fetch(url, f"stills_v2/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    s = S[sid]; RAW = "--raw" in sys.argv   # 2026-10-19 (Ralph: the pasted label looks fake): start from the clean Google still, no paste
    first = kie.upload(f"stills_v2/{sid}_label.png" if s["tub"] and not RAW else f"stills_v2/{sid}.png")
    prompt = f"{s['video']} {V['video_suffix']}"
    if s["model"] == "kling":
        body = {"model": "kling-3.0-omni/image-to-video", "input": {"prompt": prompt, "image_urls": [first, first] if s.get("last_frame_same") else [first],
                "duration": s["dur"], "resolution": "720p", "aspect_ratio": "auto", "audio": False}}
    else:
        body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "first_frame_url": first, "generate_audio": False,
                "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
        if s.get("last_frame_same"): body["input"]["last_frame_url"] = first
        if "--refs" in sys.argv:   # 2026-10-19 (Ralph's pick): reference mode instead of a first frame (Mini can't take both),
            # so Seedance sees the real print while it draws: image 1 = the clean still, 2 = real front label, 3 = reference sheet
            for k in ("first_frame_url", "last_frame_url"): body["input"].pop(k, None)
            body["input"]["reference_image_urls"] = [first, kie.upload(TUB[1]), kie.upload(TUB[0])]
            body["input"]["prompt"] = ("Recreate reference image 1 exactly (same kitchen, framing, hand, bracelet, tub) as the first frame, then: "
                + prompt + " The tub's front label must match reference image 2 exactly, letter for letter, including the teal band "
                "'100% PURE MICRONIZED' and the '5G CREATINE PER SCOOP' badge; reference image 3 shows the tub's shape from every side.")
    url = kie.run_task(body)
    if url:
        kie.fetch(url, f"clips_v2/{sid}{'_refs' if '--refs' in sys.argv else '_raw' if RAW else ''}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    for d in ("stills_v2", "clips_v2"): Path(d).mkdir(exist_ok=True)
    fn = still if kind == "stills" else clip
    with ThreadPoolExecutor(max(1, len(ids))) as ex:
        list(ex.map(fn, ids))
