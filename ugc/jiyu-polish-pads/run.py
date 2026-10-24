"""JIYU Cleansing Polish Pads (Grace) runner, 2026-10-24 (from ugc/pritech-cleansing-brush/run.py). Script gate + BOOK lock run
before every paid call (kie.run_task).
  python3 run.py prompt S1         print the still prompt and refs (free)
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
Prompts follow prompt-master (Ralph's stack): size first, numbered references named in the prompt, print matched, no text."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())}
SHEET, FRONT, LID, PAD, ORIG = ("refs/product_sheet.png", "refs/closeup_jiyu_front.png", "refs/closeup_lid_top.png",
                                "refs/closeup_pad_texture.png", "refs/original_sheet.png")
HANDREF = "../../grace/ref/hand-sheets/without_bracelet.jpg"


def still_refs(s):
    r, names = [], []
    def add(p, what): r.append(p); names.append(f"image {len(r)} = {what}")
    p = s["product"]
    if p == "original":
        add("refs/closeup_orig_front.png", "the LETTER close-up: the real original jar front, giant blocky dark-green JIYU letters on peach-coral")
        add(ORIG, "JIYU's ORIGINAL toner pads jar, real photos: peach-coral jar, lime-green lid, dark-green JIYU letters")
    if p == "new" or s["id"] == "S5":
        add(FRONT, "the LETTER close-up: the real jar front, giant blocky cobalt-blue JIYU letters on frosted mint-aqua")
        add(SHEET, "the product sheet, real photos only: the big left photo is the real jar, copy its squat shape, size and colours exactly")
        add(LID, "a real close-up of the pastel pink lid top with the small cobalt-blue JIYU")
    if p in ("new", "pad", "pad-face"):
        add(PAD, "a real close-up of one JIYU pad: white, fine dimpled quilt texture (copy only the pad; ignore the hand and nail polish in that photo)")
    add(f"rooms/room_{s['room']}.jpg", "the real bathroom to use as the background (same tiles, colours and light)")
    if s["hand"]: add(HANDREF, "Grace's real hand sheet (skin tone, nails, rings, bare wrist)")
    note = "Reference images: " + "; ".join(names) + "."
    if p in ("new", "original"):
        note += " The jar must match its reference photos exactly in shape, size and colours; every JIYU letter matches its close-up letter for letter and colour for colour; no lavender or purple anywhere."
    return r, note


def still_prompt(s):
    refs, note = still_refs(s)
    # map the shot's generic "image 2/3/4" wording to the real numbering by naming refs explicitly
    text = s["still"].replace("exactly as image 2 (real photo) and the product sheet", "exactly as its reference photos") \
                     .replace("exactly as image 3", "exactly as its reference photos").replace("exactly as image 4", "exactly as its pad close-up") \
                     .replace("exactly as image 2", "exactly as its reference photos")
    return refs, "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + text + " " + note


def still(sid):
    refs, prompt = still_prompt(S[sid])
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(p) for p in refs],
                        "aspect_ratio": "9:16", "resolution": "1K"}}, label=f"still {sid}")
    if url: kie.fetch(url, f"stills/{sid}.png"); print("still", sid, "ok", flush=True)


if __name__ == "__main__":
    kind, ids = sys.argv[1], sys.argv[2:]
    Path("stills").mkdir(exist_ok=True); Path("clips").mkdir(exist_ok=True)
    if kind == "prompt":
        for i in ids: print(still_prompt(S[i]))
    elif kind == "stills":
        with ThreadPoolExecutor(max(1, len(ids))) as ex: list(ex.map(still, ids))
