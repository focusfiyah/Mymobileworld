"""Build every still and clip prompt from shots.json (free), HEVEBLUE eye cream (2026-10-27). prompt-master, Ralph's stack:
size first, numbered references named in the prompt and matched letter for letter, one motion, no text.
  python3 build_prompts.py      -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["shots"]
SHEET, PRINT, TIP, CAP = "refs/product_sheet.png", "refs/real/closeup_print.png", "refs/real/closeup_tip.png", "refs/real/closeup_cap.png"
HAND = "../../grace/ref/hand-sheets/without_bracelet.jpg"
FACE = "refs/grace_face.jpg"


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    prod = not s.get("no_product")
    if prod:
        add(SHEET, "the product reference sheet built from real photos of this exact eye cream")
        add(PRINT, "a real close-up of the print on the white tube")
        add(CAP if s["cap"] == "on" else TIP, "a real close-up of the black cap on the tube" if s["cap"] == "on" else "a real close-up of the chrome applicator, black ring and flared tip")
    for er in s.get("extra_refs", []): add(er[0], er[1])
    add(s["room"], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bare wrist)")
    if s["face"]: add(FACE, "Grace's face, for her skin tone, brows and eyes only")
    hb = B["hand_block"].replace("Whole wrist visible, a little forearm in a soft cream knit sleeve may show,", "The wrist runs off the bottom frame edge,") if s["face"] else B["hand_block"]
    parts = [B["size_first"] if prod else "", s["still"], hb if s["hand"] else B["no_hand"],
             B["face_block"] if s["face"] else "",
             (B["product_block"] + " " + (B["cap_on"] if s["cap"] == "on" else B["cap_off"])) if prod else "No eye cream tube, no product and no packaging appears anywhere in this frame.",
             f"Other props: {s['props']}, plain and unbranded." if s["props"] else "", B["light"], B["suffix"],
             "Reference images: " + "; ".join(n) + "." + (" The eye cream must match images 1 to 3 letter for letter, colour for colour and shape for shape." if prod else "")]
    if not s["hand"]: parts[2] = B["no_hand"] if not s["face"] else "No hand, fingers or arm anywhere in the frame."
    return r, " ".join(p for p in parts if p)


def clip(s):
    if s.get("no_product"):  # Seedance 2.0 Mini, first frame = the still
        return [f"stills/{s['id']}.png"], (f"Animate this image as the first frame. {s['motion']} No eye cream tube or product appears. "
                + ("The hand keeps its French-tip nails and rings and a bare wrist with no bracelet; no second hand appears. " if s["hand"] else "No hand or fingers appear at any time. ")
                + ("Her face keeps the same skin, eye and brows; no mouth comes into the frame. " if s["face"] else "")
                + "Bright neutral daylight that never changes. No music, no voice, no captions, no on-screen text.")
    r = [f"stills/{s['id']}.png", PRINT, CAP if s["cap"] == "on" else TIP, SHEET]; sheet_n = len(r)
    who = (", hand and rings" if s["hand"] else "") + (", face and skin" if s["face"] else "")
    head = B["omni_head"].replace("{who}", who).replace("{sheet}", str(sheet_n))
    extra = (f" Image 2 is the real print, image 3 the real {'black cap' if s['cap'] == 'on' else 'chrome tip and black ring'}, image {sheet_n} the product sheet."
             + (" The cap stays on the whole time." if s["cap"] == "on" else " The cap is off and never appears."))
    if s["hand"]:
        r.append(HAND); extra += f" Image {len(r)} is Grace's hand sheet: the French-tip nails and rings stay exactly, the wrist stays bare, as in images 1 and {len(r)}; the hand keeps one grip on the chrome and enters and leaves from the frame edge; no second hand and no other jewellery appear."
    else: extra += " No hand, fingers or people appear at any time." if not s["face"] else ""
    if s["face"]: extra += " Her face stays exactly as in image 1; no mouth or lips come into the frame."
    return r, f"{head}{extra} Motion: {s['motion']} {B['omni_tail'].replace('4 seconds', str(s.get('seconds', 4)) + ' seconds')}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n"); Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
