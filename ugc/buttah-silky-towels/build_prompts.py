"""Build every still and clip prompt from shots.json (free). prompt-master, Ralph's stack: size first, numbered references
named in the prompt and matched letter for letter, one motion, no text. Copied in shape from ../youtheory-b12b6.
  python3 build_prompts.py  -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json
HAND sheet path is set after Ralph picks with/without bracelet (grace/ref/hand-sheets/README.md)."""
import json, sys
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["videos"][0]["shots"]
SHEET, LOGO, BADGE, REAL = "refs/product_sheet.png", "refs/closeup_logo.png", "refs/closeup_badges.png", "refs/front_clean.png"
TOWEL = "refs/towel_ref.png"   # real opened towel + waffle texture, no pouch (for no-pouch shots)
HAND = "../../grace/ref/hand-sheets/" + (sys.argv[1] if len(sys.argv) > 1 else "with_bracelet.jpg")


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    if s["pouch"]: add(SHEET, "the product reference sheet built from the brand's real photos (its panels D, E, F, H are the towel references)")
    elif s["towel"]: add(TOWEL, "the towel reference: a real opened towel and its waffle texture")
    if s["pouch"]:
        add(LOGO, "a close-up of the real 'buttah.' logo and 'Silky Soft Towels' line")
        add(BADGE, "a close-up of the real window strip, three badges and white text lines")
        add(REAL, "the real pouch front")
    add(s["room"], "the real room photo to use as the setting")
    # Ralph 2026-11-02: Grace's hand with no rings and no bracelet -> no hand sheet image (its rings would be copied); hand in words only
    parts = ["Vertical 9:16 photo, a single frame from a phone-shot UGC video."]
    if s["pouch"]: parts.append(B["size_first"] + (" " + B["size_folded"] if s["towel"] else ""))
    elif s["towel"]: parts.append(B["size_towel"])
    parts += [s["still"], B["hand_block"] if s["hand"] else B["no_hand"]]
    if s["pouch"]: parts.append(B["pouch_block"])
    if s["towel"]: parts.append(B["towel_block"])
    parts.append(B["scene_suffix"] if s["pouch"] else B["scene_suffix_nopack"])
    tail = "Reference images: " + "; ".join(n) + "."
    if s["pouch"]: tail += " The pouch print must match images 2 to 4 letter for letter and colour for colour."
    if not s["pouch"]: tail += " No towel pack or packaging of any kind appears in this frame."
    return r, " ".join(parts + [tail])


def clip(s):
    if s["model"] == "seedance":
        return [f"stills/{s['id']}.png"], (f"Animate this exact first frame: keep its room, light and framing exactly. {s['motion']} "
                f"{B['no_hand']} No towel pack or product appears. {B['omni_tail']}")
    r = [f"stills/{s['id']}.png"]; ex = []
    head = "Recreate image 1 exactly as the first frame: keep its room, light, framing" + (", hand and nails" if s["hand"] else "") + " exactly."
    if s["pouch"]:
        r += [LOGO, BADGE]
        ex.append("Image 2 is the real 'buttah.' logo and 'Silky Soft Towels' line, image 3 the real window strip, three badges and white text lines: they stay on the pouch the whole clip and match images 2 and 3 letter for letter and colour for colour.")
    r.append(SHEET if s["pouch"] else TOWEL)
    ex.append(f"Image {len(r)} is the product sheet: keep this exact soft flat pouch shape, size and colours" + (" and the plain white waffle towels" if s["towel"] else "") + "; no added marks, no extra text." if s["pouch"]
              else f"Image {len(r)} is the real towel: it stays a plain white waffle towel with no print; no towel pack or packaging appears in this clip.")
    if s["pouch"]: ex.append("The pouch stays closed with no lid, flap or opening, and never bends, turns or flips.")
    if s["hand"]:
        ex.append("The hand stays exactly as in image 1: medium-brown skin, short French-tip nails, no rings, no bracelet, no watch, no jewellery appears at any time.")
    else: ex.append("No hand, fingers or people appear at any time.")
    return r, f"{head} {' '.join(ex)} Motion: {s['motion']} {B['omni_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n")
        Path(f"prompts/{s['id']}{'_seedance' if s['model'] == 'seedance' else ''}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2, "model": s["model"]}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
