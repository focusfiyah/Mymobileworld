"""Vans sequin runner (plan B, Ralph 2026-10-21: all Kie). Script gate runs before every paid call (kie.run_task).
  python3 run.py stills V1S1 ...   nano-banana-pro 1K ($0.09) -> stills/<id>.png
  python3 run.py clips V1S1 ...    Seedance 2.0 Mini REFERENCE mode ($0.041/s) -> clips/<id>.mp4
Refs on every product still/clip: product sheet + real 3/4 pair + real top/sole (no pasted labels, PLAYBOOK §6).
Once stills/look_<video>.png exists (approved still of that video), later stills of the same video use it as the look ref."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

V = json.loads(Path("shots.json").read_text())
S = {s["id"]: s for s in V["shots"]}
HAND = ["refs/hand_dorsal_bracelet.png", "refs/hand_side_bracelet.png"]
SHOE = ["refs/product_sheet.png", "refs/shoe_pair_3q.jpg", "refs/shoe_top_sole.jpg"]
TEST = "stills/look_test.png"   # the approved test still: hand, nails, jewellery, polish, shoe look for every other still


def text(s):
    p = [s["still"]]
    if s["hand"]: p.append(V["hand_block"])
    else: p.append("No hands or arms anywhere in the frame.")
    if s["feet"]: p.append(V["feet_block"])
    if s["anklet"]: p.append(f"She wears {s['anklet']}.")
    p += [V["shoe_block"], V["scene_suffix"]]
    return " ".join(p)


def still(sid):
    s = S[sid]
    refs = [kie.upload(p) for p in SHOE]; note = " Reference images: 1 = the product reference sheet (the real shoe from every side), 2 = the real pair at 3/4, 3 = the real top view with the red insole and the waffle sole"
    if s["hand"]:
        refs += [kie.upload(p) for p in HAND]; note += ", 4 and 5 = Grace's real hand (skin, nails, rings, bracelet: match exactly, ignore their grey background)"
    look = Path(f"stills/look_{s['video']}.png")
    for extra, why in ((TEST, "an approved frame from this ad: match its skin tone, nails, toenail polish and jewellery"), (str(look), "an approved frame from this same video: match its setting, light and outfit")):
        if Path(extra).exists() and Path(extra).resolve() != Path(f"stills/{sid}.png").resolve():
            refs.append(kie.upload(extra)); note += f", {len(refs)} = {why}"
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text(s) + note + "."
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": refs, "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    s = S[sid]
    first = Path(f"stills/{sid}_clean.png"); first = first if first.exists() else Path(f"stills/{sid}.png")
    refs = [kie.upload(str(first)), kie.upload(SHOE[0]), kie.upload(SHOE[1])]
    prompt = (f"Recreate reference image 1 exactly (same framing, setting, light, people, jewellery and shoe) as the first frame, then {s['move']}. "
              "The shoe must match reference image 2 (the real product from every side) and reference image 3 exactly: sequins only on the black squares, "
              f"black collar binding, black laces, marshmallow sole. {V['video_suffix']}")
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
            "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
    url = kie.run_task(body)
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__" and sys.argv[1] in ("stills", "clips"):
    kind, ids = sys.argv[1], sys.argv[2:]
    for d in ("stills", "clips"): Path(d).mkdir(exist_ok=True)
    with ThreadPoolExecutor(max(1, min(4, len(ids)))) as ex:
        list(ex.map(still if kind == "stills" else clip, ids))


def edit(sid):
    """Paid edit of an existing still (nano-banana-pro, $0.09): only the change in shots.json 'edit'. Keeps the original as <id>_orig.png."""
    s = S[sid]; src = Path(f"stills/{sid}.png"); base = Path(s.get("edit_src", src))
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": s["edit"], "image_input": [kie.upload(str(base))], "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        (src.rename(f"stills/{sid}_orig.png") if src.exists() else None); kie.fetch(url, str(src)); print("edit", sid, "ok", flush=True)


if __name__ == "__main__" and sys.argv[1] == "edit":
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(edit, sys.argv[2:]))
