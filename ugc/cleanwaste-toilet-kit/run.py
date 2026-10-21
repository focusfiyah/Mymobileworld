"""Cleanwaste toilet kit (Grace) V1 runner, Kie only (Ralph 2026-10-21).
  python3 run.py stills V1S4            Gemini 3 Pro Image (Kie nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py clips V1S4             Seedance 2.0 Mini reference mode, 5 s ($0.205 each) -> clips/<ID>.mp4
Prompts follow the prompt-master rules for Ralph's stack: one shot, one motion, the real product from the reference sheet,
hand text only (short French tips, no rings; no hand photo passed, its nails are longer), no text in frame.
Once stills/look_ref.png exists (copy of the approved test still) it is passed on every later still for the hand, light and look."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

D = json.loads(Path("shots.json").read_text()); B = D["blocks"]
S = {s["id"]: s for s in D["videos"][0]["shots"]}
SHEET, BOX, POUCH, BAGS, CONTENTS, LOOK = ("refs/product_sheet.png", "refs/crop_box_front.png", "refs/crop_pouch_front.png",
                                           "refs/crop_bags.png", "refs/crop_contents.png", "stills/look_ref.png")


def refs_for(s):
    """(paths, sentence naming each reference image by its number)"""
    r, names = [], []
    def add(p, what): r.append(p); names.append(f"reference image {len(r)} = {what}")
    if s["box"]: add(SHEET, "the Cleanwaste product reference sheet (big top view = the real box front)"); add(BOX, "a tight crop of the real box front print")
    if s["pouch"]: add(POUCH, "the real kit pouch")
    if s.get("seat_ref"): add("refs/crop_bag_on_seat.png", "the real bag draped over a toilet seat")
    if s["bag"]: add(BAGS, "the real blue-grey waste bag and zip-close bag")
    if s["contents"] or s.get("powder"): add(CONTENTS, "the real kit contents (bags, powder, toilet paper packet, wipe packet, pouch)")
    if Path(LOOK).exists() and s["hand"] and s["id"] != "V1S4": add(LOOK, "a frame from this same video: match its light, hand, skin tone and short French-tip nails exactly (NOT its forearm: only hand and wrist)")
    return r, ("Reference images: " + "; ".join(names) + ".") if names else ""


def text(s):
    parts = [s["still"], B["hand_block"] if s["hand"] else B["no_hand"]]
    if s["box"]: parts.append(B["box_block"])
    if s["pouch"]: parts.append(B["pouch_block"])
    if s["bag"]: parts.append(B["bag_block"])
    if s["contents"]: parts.append(B["contents_block"])
    if s.get("powder"): parts.append(B["powder_block"])
    parts.append(B["scene_suffix"])
    return " ".join(parts)


def still(sid):
    s = S[sid]; paths, note = refs_for(s)
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text(s) + " " + note
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in paths],
                                                              "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


def clip(sid):
    s = S[sid]; paths, _ = refs_for(s)
    first = f"stills/{sid}_fix.png" if Path(f"stills/{sid}_fix.png").exists() else f"stills/{sid}.png"
    refs = [first] + [p for p in paths if p != LOOK][:3]
    prompt = (f"Recreate reference image 1 exactly (same room, framing, light, objects{', hand' if s['hand'] else ''}) as the first frame, then: "
              + s["motion"] + " " + (B["hand_block"] if s["hand"] else B["no_hand"]) + " " + B["video_suffix"])
    if s["box"]: prompt += " The box print must match reference image 3 exactly, letter for letter ('The Original WAG BAG', '12-PACK', 'CLEANWASTE'); reference image 2 shows the real box."
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": [kie.upload(p) for p in refs],
                        "generate_audio": False, "resolution": "720p", "aspect_ratio": "9:16", "duration": 5}})
    if url: kie.fetch(url, f"clips/{sid}.mp4"); print("clip", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], [a for a in sys.argv[2:] if not a.startswith("--")]
    if "--dry" in sys.argv:
        for i in ids: p, n = refs_for(S[i]); print(i, p, "\n", (text(S[i]) + " " + n) if kind == "stills" else S[i]["motion"], "\n")
        sys.exit()
    for d in ("stills", "clips"): Path(d).mkdir(exist_ok=True)
    with ThreadPoolExecutor(max(1, min(4, len(ids)))) as ex: list(ex.map(still if kind == "stills" else clip, ids))
