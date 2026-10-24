"""PRITECH black face scrubber (Grace) runner, 2026-10-23. Script gate + BOOK lock run before every paid call (kie.run_task).
  python3 run.py stills S1 ...     Gemini 3 Pro Image on Kie (nano-banana-pro, $0.09 each) -> stills/<ID>.png
  python3 run.py prompt S1         print the still prompt and refs (free)
Prompts follow prompt-master (Ralph's stack): size first, numbered references named in the prompt, print matched, no text."""
import json, sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
import kie

S = {s["id"]: s for s in json.loads(Path("shots.json").read_text())}
SHEET, HEAD, BTN, LOGO = "refs/product_sheet_v2.png", "refs/closeup_head.png", "refs/closeup_buttons.png", "refs/closeup_stand_logo.png"
HANDREF = "../../grace/ref/hand-sheets/without_bracelet.jpg"
BUTTONS = {"S1", "S5", "S6", "S7"}      # buttons can be in frame
STAND = {"S4", "S8", "S9"}              # the stand with its PRITECH print is in frame


def still_refs(s):
    r, names = [], []
    def add(p, what): r.append(p); names.append(f"image {len(r)} = {what}")
    if s["product"]:
        add(SHEET, "the product sheet, real photos only: the big left photo is the real black brush, copy its slim shape and proportions exactly")
        add(HEAD, "a real close-up of the black bristle head")
        if s["id"] in BUTTONS: add(BTN, "a real close-up of the three moulded buttons, black on black: ((•)) on top, O in the middle, °C at the bottom")
        if s["id"] in STAND: add(LOGO, "a real close-up of the grey 'PRITECH' print on the black stand")
    add(f"rooms/room_{s['room']}.jpg", "the real bathroom to use as the background (same tiles, colours and light)")
    if s["hand"]: add(HANDREF, "Grace's real hand sheet (skin tone, nails, rings, bare wrist)")
    note = "Reference images: " + "; ".join(names) + "."
    if s["product"]: note += " The brush must match images 1 and 2 exactly in shape, size and matte black colour; any print matches its close-up letter for letter and colour for colour."
    return r, note


def still_prompt(s):
    refs, note = still_refs(s)
    return refs, "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + s["still"] + " " + note


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
