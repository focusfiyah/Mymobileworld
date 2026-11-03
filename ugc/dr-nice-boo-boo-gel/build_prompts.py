"""Build every still and clip prompt from shots.json (free). prompt-master, Ralph's stack: size first, numbered references
named in the prompt and matched letter for letter, one motion, no text. Shape copied from ../buttah-silky-towels.
  python3 build_prompts.py  -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json
Product clips: Flow kit first (Ralph's app, $0), else Wan 3.0 720P on Kie (Image1.. naming). No-product clips: Seedance 2.0 Mini."""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["videos"][0]["shots"]
SHEET, LABEL, LOGO, PUMP = "refs/product_sheet.png", "refs/closeup_label.png", "refs/closeup_logo.png", "refs/pump_open.png"
HAND = "../../grace/ref/hand-sheets/no_jewelry.jpg"
KID_LOOK = "stills/S1.png"   # approved S1 still = the child's skin/hand look for S3 (passed once S1 is approved)


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    if s["product"]:
        add(SHEET, "the product reference sheet built from the brand's real photos")
        add(LABEL, "a close-up of the real front label")
        add(LOGO, "a close-up of the real 'DR. NICE'S / NATURAL PRODUCTS / BOO-BOO GEL' lettering")
        if s.get("open"): add(PUMP, "the real bottle with its cap off, showing the silver pump head")
    add(s["room"], "the real photo to use as the setting")
    if s["hand"] == "grace": add(HAND, "Grace's no-jewellery hand reference sheet (skin, nails; no rings, no bracelet)")
    if s["hand"] == "kid" and s.get("kid_ref"): add(KID_LOOK, "the approved first shot: the same child's hand, skin and shorts")
    parts = ["Vertical 9:16 photo, a single frame from a phone-shot UGC video."]
    if s["product"]: parts.append(B["size_first"])
    parts += [s["still"], B["grace_hand"] if s["hand"] == "grace" else B["kid_hand"] if s["hand"] == "kid" else B["no_hand"]]
    if s["product"]:
        parts.append(B["product_block"]); parts.append(B["open_block"] if s.get("open") else B["cap_on"])
    if s.get("gel"): parts.append(B["gel_block"])
    parts.append(B["scene_suffix"] if s["product"] else B["scene_suffix_noproduct"])
    tail = "Reference images: " + "; ".join(n) + "."
    if s["product"]: tail += " The bottle print must match images 2 and 3 letter for letter and colour for colour."
    else: tail += " No bottle, tube, box or product of any kind appears in this frame."
    return r, " ".join(parts + [tail])


def clip(s):
    if s["model"] == "seedance":
        return [f"stills/{s['id']}.png"], (f"Animate this exact first frame: keep its setting, light and framing exactly. {s['motion']} "
                + ("The child's hand stays the same small hand with short natural nails; no adult hand appears. " if s["hand"] else B["no_hand"] + " ") + f"No bottle, tube, box or product appears at any time. {B['clip_tail']}")
    r = [f"stills/{s['id']}.png", LABEL, LOGO]; ex = []
    head = "Recreate Image1 exactly as the first frame: keep its setting, light, framing" + (", hand and nails" if s["hand"] else "") + " exactly."
    ex.append("Image2 is the real front label and Image3 the real 'DR. NICE'S / NATURAL PRODUCTS / BOO-BOO GEL' lettering: the label stays on the bottle the whole clip and matches Image2 and Image3 letter for letter and colour for colour, the blue monster with golden horns and the orange bandage unchanged.")
    if s.get("open"): r.append(PUMP); ex.append(f"Image{len(r)} is the real bottle with its cap off: the pump head stays silver with a small nozzle.")
    r.append(SHEET); ex.append(f"Image{len(r)} is the product sheet: keep this exact slim silver bottle shape, size and colours; no added marks, no ® or ™, no extra text.")
    ex.append("The bottle keeps one grip, never turns its back to the lens, never flips and never changes size.")
    if s["hand"] == "grace":
        r.append(HAND); ex.append(f"Image{len(r)} is Grace's hand sheet: the hand stays exactly as in Image1 and Image{len(r)}, mauve-pink French-tip nails, no rings, no bracelet, no watch; no jewellery appears at any time.")
    elif s["hand"] == "kid": ex.append("The child's hand stays exactly as in Image1: small, short natural nails, no polish, no jewellery; no adult hand appears.")
    else: ex.append("No hand, fingers or people appear at any time.")
    return r, f"{head} {' '.join(ex)} Motion: {s['motion']} {B['clip_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n")
        Path(f"prompts/{s['id']}{'_seedance' if s['model'] == 'seedance' else ''}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2, "model": s["model"]}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
