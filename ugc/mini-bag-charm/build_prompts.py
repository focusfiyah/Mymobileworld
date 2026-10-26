"""Build every still and clip prompt from shots.json (free), Mini Bag Charm (2026-10-26). prompt-master, Ralph's stack:
size first, numbered references named in the prompt and matched colour for colour, one motion, no text.
  python3 build_prompts.py      -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["shots"]
SHEET, FRONT, LOCK, SCARF = "refs/product_sheet.png", "refs/real/closeup_front.png", "refs/real/closeup_lock.png", "refs/real/closeup_scarf.png"
HAND = "../../grace/ref/hand-sheets/with_bracelet.jpg"


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    prod = not s.get("no_product")
    if prod:
        add(SHEET, "the product reference sheet built from real photos of this exact bag charm")
        add(LOCK, "a real close-up of its gold buckle loop, grommet and padlock")
        add(SCARF, "a real close-up of its twilly scarf and right-hand handle")
    add(s["room"], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bracelets)")
    bag = "handbag" in s["still"].lower() or "tote" in s["still"].lower()
    size = B["size_first"].replace(" and it is empty: nothing sticks out of its open top except a little white tissue paper, as in image 1.", "; a white wireless earbuds case fits inside it with its top just showing.") if s.get("filled") else B["size_first"]
    parts = [size if prod else "", s["still"], B["hand_block"] if s["hand"] else B["no_hand"],
             B["product_block"] if prod else "No bag charm or mini bag appears anywhere in this frame.",
             B["handbag_block"] if bag and prod else "",
             f"Other props: {s['props']}, plain and unbranded." if s["props"] else "", B["light"], B["suffix"] if prod else B["suffix"].replace("sharp focus on the bag charm", "sharp focus on the hand and the bottom of the tote"),
             "Reference images: " + "; ".join(n) + "." + (" The bag charm must match images 1 to 3 colour for colour and detail for detail." if prod else "")]
    return r, " ".join(p for p in parts if p)


def clip(s):
    if s.get("no_product"):  # Seedance 2.0 Mini, first frame = the still
        return [f"stills/{s['id']}.png"], (f"Animate this image as the first frame. {s['motion']} No bag charm appears. "
                + ("The hand keeps its French-tip nails, rings and bracelets, " if s["hand"] else "")
                + "bright neutral daylight that never changes. No music, no voice, no captions, no on-screen text.")
    r = [f"stills/{s['id']}.png", LOCK, SCARF, SHEET]; sheet_n = len(r)
    head = B["omni_head"].replace("{hand}", ", hand, rings and bracelets" if s["hand"] else "").replace("{sheet}", str(sheet_n))
    extra = f" Image 2 is the real gold buckle and padlock, image 3 the real scarf and handle, image {sheet_n} the product sheet."
    if s["hand"]:
        r.append(HAND); extra += f" Image {len(r)} is Grace's hand sheet: the French-tip nails, rings and bracelets stay exactly as in images 1 and {len(r)}; the hand keeps one grip, enters and leaves from the frame edge; the charm never turns, flips or swings; no other jewellery appears."
    else: extra += " No hand, fingers or people appear at any time."
    return r, f"{head}{extra} Motion: {s['motion']} {B['omni_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n"); Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
