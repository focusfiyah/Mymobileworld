"""Build every still and Omni clip prompt from shots.json (free), Monbix Remy comforter (2026-10-26). prompt-master,
Ralph's stack: size first, numbered references named in the prompt and matched colour for colour, one motion, no text.
  python3 build_prompts.py      -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["videos"][0]["shots"]
SHEET, STRIPE, COMF, POCKET = "refs/product_sheet.png", "refs/real/stripe_real_niki.png", "refs/real/comforter_texture_tori.png", "refs/real/pocket_real_tori2.png"
ROOM, HAND = "rooms/roomA_olive_bedroom.jpg", "../../grace/ref/hand-sheets/with_bracelet.jpg"


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    add(SHEET, "the product reference sheet built from real photos of this exact set")
    add(STRIPE, "a real close-up of the sheet and pillowcase stripe (colour and stripe width)")
    add(COMF, "a real close-up of the solid terracotta comforter fabric")
    if s["pocket"]: add(POCKET, "a real close-up of the fitted sheet's striped side pocket")
    add(ROOM, "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bracelets)")
    parts = [B["size_first"] if (s["pocket"] or s["phone"] or s["id"] in ("S1", "S5", "S11")) else "", s["still"],
             B["hand_block"] if s["hand"] else s.get("no_hand_override", B["no_hand"]), B["bedding_block"], B["pocket_block"] if s["pocket"] else "",
             B["phone_block"] if s["phone"] else "", B["pillow_block"] if s["pillow"] else "", B["room_block"], B["suffix"],
             "Reference images: " + "; ".join(n) + ". The bedding must match images 1 to 3" + (" and the pocket image 4" if s["pocket"] else "") + " colour for colour and stripe width for stripe width."]
    return r, " ".join(p for p in parts if p)


def clip(s):
    r = [f"stills/{s['id']}.png", STRIPE, COMF]
    if s["pocket"]: r.append(POCKET)
    r.append(SHEET); sheet_n = len(r)
    head = B["omni_head"].replace("{hand}", ", hand, rings and bracelets" if s["hand"] else "").replace("{sheet}", str(sheet_n))
    extra = " Image 2 is the real stripe, image 3 the real comforter fabric"
    extra += (", image 4 the real side pocket: it stays sewn flat on the side of the mattress, open at the top" if s["pocket"] else "") + f", image {sheet_n} the product sheet."
    if s["phone"]: extra += " The phone stays a plain black phone with its screen off."
    if s["pillow"]: extra += " The cream pumpkin pillow stays the same shape and colour."
    if s["hand"]:
        r.append(HAND); extra += f" Image {len(r)} is Grace's hand sheet: the French-tip nails, rings and bracelets stay exactly as in images 1 and {len(r)}; the hand enters and leaves from the frame edge and grips what it touches; no other jewellery appears."
    else: extra += " No hand, fingers or skin appear at any time." if s.get("no_hand_override") else " No hand, fingers or people appear at any time."
    return r, f"{head}{extra} Motion: {s['motion']} {B['omni_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n"); Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
