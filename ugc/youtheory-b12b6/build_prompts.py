"""Build every still and Omni clip prompt from shots.json (free). prompt-master, Ralph's stack: size first, numbered
references named in the prompt and matched letter for letter, straw in every frame, one motion, no text.
  python3 build_prompts.py      -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["videos"][0]["shots"]
SHEET, LOGO, WORD = "refs/product_sheet.png", "refs/closeup_F.png", "refs/closeup_G.png"
TORN = "refs/closeup_I_torn_straw.png"
REAL = "refs/real/grace_pouch_front_flat.jpg"
BOX, BOXC, HAND = "refs/real/grace_box_front_open.jpg", "refs/closeup_box.png", "../../grace/ref/hand-sheets/with_bracelet.jpg"


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    add(SHEET, "the product reference sheet built from real photos (A = the real pouch front)")
    add(LOGO, "a close-up of the real 'youtheory' logo and magenta dot circle")
    add(WORD, "a close-up of the real 'B12B6 liquid' wordmark, claim lines and 'raspberry flavor' bar")
    if s["straw"] and s["id"] != "S5": add("stills/S5.png", "an approved frame from this video: copy its pouch top exactly (the neck and square shoulders whole, the torn tab edge at the top of the neck, the white paper straw standing in the opening)")
    elif s["straw"]: add(TORN, "the real pouch with its tear-off tab torn off and the white paper straw in the opening: the exact top to draw")
    else: add(REAL, "a real photo of Grace's unopened pouch, tab on")
    box = ""
    if s.get("box"):
        add(BOX, "a real photo of the display carton, torn open, with pouches inside")
        add(BOXC, "a close-up of the real carton front print below the tear")
        box = B["box_block"].replace("images 5 and 6", f"images {len(r) - 1} and {len(r)}").replace("exactly as image 6", f"exactly as image {len(r)}")
    add(s["room"], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bracelets)")
    parts = ["Vertical 9:16 photo, a single frame from a phone-shot UGC video.", B["size_first"], s["still"],
             B["hand_block"] if s["hand"] else B["no_hand"], B["pouch_block"], (B["straw_block"].replace("The torn-off tab is not in the frame.", "The half-torn tab still hangs from one side of the top, exactly as in image 4, because it was just opened.").replace("has been torn off;", "has been torn open;").replace("in this frame it is torn off", "in this frame it is torn open") if s["id"] != "S5" else B["straw_block"]) if s["straw"] else B["intact_block"], box, B["scene_suffix"],
             "Reference images: " + "; ".join(n) + ". The pouch print must match images 1 to 3 letter for letter and colour for colour, and its top must look exactly like image 4."]
    return r, " ".join(p for p in parts if p)


def clip(s):
    r = [f"stills/{s['id']}.png", LOGO, WORD, SHEET, TORN if s["straw"] else REAL]
    head = B["omni_head"].replace("{hand}", ", hand, rings and bracelets" if s["hand"] else "")
    if s["straw"]:
        extra = " Image 5 is the real torn-open top with the straw: the top of the pouch looks exactly like image 5 in every frame."
    else:
        head = head.replace(" and the white paper straw standing in the pouch", "").replace(" The straw stays upright in the torn-open top of the pouch in every frame; the pouch has a flat tear-off top, no screw cap and no spout.", " The pouch is unopened: its flat magenta tear-off tab stays on top in every frame; no straw, no screw cap, no spout.")
        extra = " Image 5 is a real photo of the unopened pouch: its top looks exactly like image 5 in every frame."
    if s["hand"]:
        r.append(HAND); extra += f" Image {len(r)} is Grace's hand sheet: the French-tip nails, rings and bracelets stay exactly as in images 1 and {len(r)}; no other jewellery appears."
    if s.get("box"):
        r.append(BOXC); extra += f" Image {len(r)} is the real carton front print: it matches image {len(r)} letter for letter and never changes."
    if not s["hand"]: extra += " No hand, fingers or people appear at any time."
    return r, f"{head}{extra} Motion: {s['motion']} {B['omni_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n"); Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
