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
TAB = "refs/real_vans_tab.jpg"   # real side-tab close-up (Vans 2026-10-21: the print the model sees is the print it draws)
TEST = "stills/look_test.png"   # the approved test still: hand, nails, jewellery, polish, shoe look for every other still


def text(s):
    p = [s["still"]]
    if s["hand"]: p.append(V["hand_block"])
    else: p.append("No hands or arms anywhere in the frame.")
    if s["feet"]: p.append(V["feet_block"])
    if s["anklet"]: p.append(f"She wears {s['anklet']}.")
    p += [V["shoe_block"], V["night_suffix"] if s.get("suffix") == "night" else V["scene_suffix"]]
    return " ".join(p)


def still(sid):
    s = S[sid]
    refs = [kie.upload(p) for p in SHOE] + [kie.upload(TAB)]; note = (" Reference images: 1 = the product reference sheet (the real shoe from every side), 2 = the real pair at 3/4, 3 = the real top view with the red insole and the waffle sole, "
        "4 = a close-up of the real side VANS tab: the shoe print MUST match images 1-4 letter for letter and colour for colour (black woven tab with white letters, sequins on the black squares only)")
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
    """LGXNDS v5 method in full (Ralph 2026-10-19, restated 2026-10-21 after the V1S1 tab read as a floating sticker):
    reference mode, refs = 1 the clean still, 2 a close-up of the REAL side VANS tab, 3 the product reference sheet."""
    s = S[sid]
    first = Path(f"stills/{sid}_clean.png"); first = first if first.exists() else Path(f"stills/{sid}.png")
    refs = [kie.upload(str(first)), kie.upload("refs/real_vans_tab.jpg"), kie.upload(SHOE[0])]
    prompt = (f"Recreate reference image 1 exactly (same framing, setting, light, people, hands, jewellery and shoe) as the first frame, then {s['move']}. "
              "The small woven VANS tab on the side of the shoe must match reference image 2 exactly, letter for letter: a BLACK woven label with white "
              "VANS letters and the registered mark, sewn flat into the canvas between the sequin squares, never white, blue or purple, never raised "
              "or floating. Reference image 3 shows the real shoe from every side: keep its sequins on the black squares only, the black collar binding, "
              f"the black laces and the marshmallow sole. {V['video_suffix']}")
    body = {"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
            "resolution": "720p", "aspect_ratio": "9:16", "duration": s["dur"]}}
    url = kie.run_task(body)
    if url:
        out = Path(f"clips/{sid}.mp4")
        if out.exists(): out.rename(f"clips/{sid}_r{len(list(Path('clips').glob(sid + '_r*.mp4')))}.mp4")
        kie.fetch(url, str(out)); print("clip", sid, "ok", flush=True)


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


def kling_clip(sid, prompt, hold=True):
    """Kling 3.0 Omni on Kie ($0.07/s) with the clean still as BOTH first and last frame (LGXNDS kie2.py last_frame_same):
    the clip must end where it starts, so a held shoe cannot flip or switch sides (Vans 2026-10-21, Seedance kept turning it)."""
    s = S[sid]
    first = Path(f"stills/{sid}_clean.png"); first = first if first.exists() else Path(f"stills/{sid}.png")
    u = kie.upload(str(first))
    body = {"model": "kling-3.0-omni/image-to-video", "input": {"prompt": prompt, "image_urls": [u, u] if hold else [u], "duration": s["dur"],
            "resolution": "720p", "aspect_ratio": "auto", "audio": False}}
    url = kie.run_task(body)
    if url:
        out = Path(f"clips/{sid}.mp4")
        if out.exists(): out.rename(f"clips/{sid}_r{len(list(Path('clips').glob(sid + '_r*.mp4')))}.mp4")
        kie.fetch(url, str(out)); print("kling clip", sid, "ok", flush=True)
