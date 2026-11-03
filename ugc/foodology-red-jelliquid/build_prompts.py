"""Build every still and clip prompt from shots.json (free). prompt-master (loaded 2026-11-03), Ralph's stack: size first,
numbered references named in the prompt and matched letter for letter, one motion, no text.
  python3 build_prompts.py -> prompts/still_<ID>.txt, prompts/<ID>.txt (Wan 3.0, Image1..), prompts/flow_<ID>.txt (Flow, image 1..),
  prompts/<ID>_seedance.txt (no product), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]; SH = D["videos"][0]["shots"]
SHEET = "refs/product_sheet.png"
HAND = "../../grace/ref/hand-sheets/no_jewelry.jpg"
REF = {  # item -> (close-up refs with what each is)
 "acv_stick": [("refs/closeup_acv_stick.png", "a close-up of the real ACV Apple Jelly stick print"),
               ("refs/closeup_acv_jelly_hand.png", "a real photo of the opened ACV stick in a hand: the pale yellow jelly out of the top and the stick's true size")],
 "cj_stick":  [("refs/closeup_cj_stick.png", "a close-up of the real Coleology Cutting Jelly stick with its ruby chia jelly in the top"),
               ("refs/closeup_cj_jelly.png", "real pieces of the ruby-red chia seed jelly (texture and colour)")],
 "dm_stick":  [("refs/closeup_dm_stick.png", "a close-up of the real Coleology Drink Mix PRO stick"),
               ("refs/closeup_dm_pour.png", "a real photo of the pink-red powder pouring into water and turning it pink (the bottle in it is NOT used: our glass is plain)")],
 "dm_box":    [("refs/closeup_dm_box.png", "a close-up of the real Coleology Drink Mix PRO box front")],
 "boxes":     [("refs/closeup_cj_box.png", "the real Coleology Cutting Jelly box front"), ("refs/closeup_dm_box.png", "the real Coleology Drink Mix PRO box front"),
               ("refs/closeup_acv_box.png", "the real ACV Apple Jelly box front (sharp print, seen at a slight angle)")],
}
BLOCK = {"acv_stick": "acv_stick", "cj_stick": "cj_stick", "dm_stick": "dm_stick", "boxes": "boxes"}
SIZE = {"acv_stick": "size_stick", "cj_stick": "size_stick", "dm_stick": "size_stick", "boxes": "size_boxes", "dm_box": None}


def still(s):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    if s["items"]: add(SHEET, "the product reference sheet built from FOODOLOGY's real photos")
    for it in s["items"]:
        for p, w in REF[it]: add(p, w)
    if s.get("jelly"): add("refs/closeup_cj_jelly.png", "real pieces of the ruby-red chia seed jelly (texture, colour, size)")
    add(s["room"], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's no-jewellery hand reference sheet (skin, nails; no rings, no bracelet)")
    parts = ["Vertical 9:16 photo, a single frame from a phone-shot UGC video."]
    for it in s["items"]:
        if SIZE.get(it): parts.append(B[SIZE[it]])
    if "dm_stick" in s["items"]: parts.append(B["size_glass"])
    parts += [s["still"], B["hand_block"] if s["hand"] else B["no_hand"]]
    for it in s["items"]:
        if it in BLOCK: parts.append(B[BLOCK[it]])
    parts.append(B["scene_suffix"] if s["items"] else B["scene_suffix_nopack"])
    tail = "Reference images: " + "; ".join(n) + "."
    if s["items"]: tail += f" Every FOODOLOGY print must match images 1 to {1 + sum(len(REF[i]) for i in s['items'])} letter for letter and colour for colour, flat on its stick or box and inside its edges."
    else: tail += " No sticks, boxes or packaging of any kind appear in this frame."
    return r, " ".join(parts + [tail])


def clip(s, flow=False):
    I = (lambda k: f"image {k}") if flow else (lambda k: f"Image{k}")
    if s["model"] == "seedance":
        return [f"stills/{s['id']}.png"], (f"Animate this exact first frame: keep its room, light, framing and the jelly pieces exactly. {s['motion']} "
                f"{B['no_hand']} No sticks, boxes or packaging appear. {B['clip_tail']}")
    r = [f"stills/{s['id']}.png"]; ex = []
    head = f"Recreate {I(1)} exactly as the first frame: keep its room, light, framing" + (", hand and nails" if s["hand"] else "") + " exactly."
    for it in s["items"]:
        for p, w in REF[it]:
            r.append(p); ex.append(f"{I(len(r))} is {w}.")
    r.append(SHEET); ex.append(f"{I(len(r))} is the product reference sheet. Every FOODOLOGY print stays on the product the whole clip and matches {I(2)} to {I(len(r))} letter for letter and colour for colour; no extra text, no added marks.")
    if s["hand"]:
        r.append(HAND); ex.append(f"{I(len(r))} is Grace's hand sheet: the hand stays exactly as in {I(1)} and {I(len(r))}, mauve-pink French-tip nails, no rings, no bracelet, no watch; it keeps ONE grip the whole clip. No second hand appears.")
    else: ex.append("No hand, fingers or people appear at any time.")
    return r, f"{head} {' '.join(ex)} Motion: {s['motion']} {B['clip_tail']}"


if __name__ == "__main__":
    Path("prompts").mkdir(exist_ok=True); refs = {}
    for s in SH:
        r1, p1 = still(s); r2, p2 = clip(s)
        Path(f"prompts/still_{s['id']}.txt").write_text(p1 + "\n")
        if s["model"] == "seedance": Path(f"prompts/{s['id']}_seedance.txt").write_text(p2 + "\n")
        else:
            Path(f"prompts/{s['id']}.txt").write_text(p2 + "\n"); Path(f"prompts/flow_{s['id']}.txt").write_text(clip(s, True)[1] + "\n")
        refs[s["id"]] = {"still_refs": r1, "clip_refs": r2, "model": s["model"]}
        assert len(r1) <= 8, (s["id"], len(r1))
    Path("prompts/refs.json").write_text(json.dumps(refs, indent=1)); print("built", len(SH), "shots")
