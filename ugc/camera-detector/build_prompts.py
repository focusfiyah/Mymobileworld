"""Build every still and clip prompt from shots.json (free), Hidden Camera Detector (2026-10-28). prompt-master, Ralph's
stack: size first, numbered references named in the prompt, the real face of the detector matched exactly, one motion,
no text.   python3 build_prompts.py -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json
Shots with "free": true are made in the edit (no prompt)."""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["shots"]
SHEET = "refs/product_sheet.png"
FACE = {"back": "refs/real/closeup_back_buttons.jpg", "front": "refs/real/closeup_front_leds.jpg"}
HAND = "../../grace/ref/hand-sheets/without_bracelet.jpg"
LED = {"off": "leds_off", "red": "leds_red", "flash": "flash_on"}
NIGHT = "Night light: the room is in soft cool blue night shade, still easy to see, neutral colours, never yellow or golden."


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    prod = not s.get("no_product")
    if prod:
        add(SHEET, "the product reference sheet built from real photos of this exact camera detector")
        add(FACE[s["face"]], f"a real close-up of the detector's {s['face'].upper()} face")
    for er in s.get("extra_refs", []): add(er[0], er[1])
    add(s["room"], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bare wrist)")
    two = "TWO identical camera detectors, both exactly as described; no third one." if s.get("two") else "Only ONE camera detector in the frame."
    parts = [B["size_first"] if prod else "", s["still"], B["hand_block"] if s["hand"] else B["no_hand"],
             " ".join([B["product_block"], B["face_" + s["face"]], B["leds_red_back"] if (s["leds"] == "red" and s["face"] == "back") else B[LED[s["leds"]]], two]) if prod else "No camera detector, gadget or product appears anywhere in this frame.",
             f"Other props: {s['props']}, plain and unbranded." if s["props"] else "",
             NIGHT if s.get("leds") == "flash" else B["light"], B["suffix"],
             "Reference images: " + "; ".join(n) + "." + (" The detector must match images 1 and 2 exactly in shape, colour, buttons, holes and LEDs." if prod else "")]
    return r, " ".join(p for p in parts if p)


def clip(s):
    if s.get("no_product"):  # Seedance 2.0 Mini, first frame = the still
        return [f"stills/{s['id']}.png"], (f"Animate this image as the first frame. {s['motion']} No gadget or product appears. "
                "No hand, fingers or people appear at any time. Bright neutral light that never changes. "
                "No music, no voice, no captions, no on-screen text.")
    r = [f"stills/{s['id']}.png", FACE[s["face"]], SHEET]; sheet_n = len(r)
    who = ", hand and rings" if s["hand"] else ""
    head = B["omni_head"].replace("{who}", who).replace("{sheet}", str(sheet_n))
    extra = f" Image 2 is the real {s['face']} face, image 3 the product sheet. " + (B["leds_red_back"] if (s["leds"] == "red" and s["face"] == "back") else B[LED[s["leds"]]])
    if s.get("two"): extra += " There are exactly two detectors at the start, never three."
    if s["hand"]:
        r.append(HAND); extra += (f" Image {len(r)} is Grace's hand sheet: the French-tip nails and rings stay exactly, the wrist stays bare, as in images 1 and {len(r)};"
                                  " the hand keeps one grip and enters and leaves from the frame edge; no second hand and no other jewellery appear.")
    else:
        extra += " No hand, fingers or people appear at any time."
    tail = B["omni_tail"].replace("4 seconds", f"{s.get('seconds', 4)} seconds").replace("light that never changes", "night light that never changes" if s["leds"] == "flash" else "bright neutral light that never changes")
    if s.get("two"): tail = tail.replace("no second detector appears", "no third detector appears")
    if "locked off" in s["motion"]: tail = tail.replace("One continuous handheld phone shot", "One continuous phone shot from a tripod")
    return r, f"{head}{extra} Motion: {s['motion']} {tail}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        if s.get("free"): continue
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n"); Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2}
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(refs), "shots")


def seedance(s):
    """Product clips on Seedance 2.0 Mini first-frame when Omni on Kie gives 500s (BOOK.md 7b, Ralph 2026-10-29)."""
    keep = ("The camera detector stays exactly as in the first frame the whole time: the same small matte black rounded oval body, "
            "the same tall teal-green window in its glossy black bezel, the same buttons, holes and LEDs on the same face, the same short "
            "black teardrop loop; it never turns, flips, grows, shrinks or changes shape, and no "
            + ("third detector appears." if s.get("two") else "second detector appears."))
    hand = (" The hand keeps its French-tip nails, rings and bare wrist and one grip; no second hand appears."
            if s["hand"] else " No hand, fingers or people appear at any time.")
    light = "Soft cool night light that never changes." if s.get("leds") == "flash" else "Bright neutral light that never changes."
    return (f"Animate this image as the first frame, keeping its room, light and framing. Motion: {s['motion']} {keep}{hand} "
            f"{light} No music, no voice, no captions, no on-screen text.")


if __name__ == "__main__":
    for s in SH:
        if s.get("free") or s.get("no_product"): continue
        Path(f"prompts/{s['id']}_seedance.txt").write_text(seedance(s) + "\n")
    print("seedance prompts ok")
