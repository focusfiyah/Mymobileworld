"""Build every still and clip prompt from shots.json (free), Niagara navy bamboo topper (2026-10-30). prompt-master,
Ralph's stack: size first, numbered references named in the prompt, matched letter for letter and colour for colour.
  python3 build_prompts.py -> prompts/still_<ID>.txt, prompts/<ID>.txt (clip), prompts/refs.json"""
import json
from pathlib import Path
D = json.loads(Path("shots.json").read_text()); B = D["blocks"]
SHEET, PRINT, TAG, EDGE = "refs/product_sheet.png", "refs/closeups/bamboo_print.png", "refs/closeups/niagara_tag.png", "refs/closeups/edge_skirt.png"
ROOM = {"A": "rooms/roomA_window_bedroom.jpg", "B": "rooms/roomB_guest_bedroom.jpg", "C": "rooms/roomC_laundry.jpg"}
HAND = "../../grace/ref/hand-sheets/without_bracelet.jpg"


def refs(s, first=None):
    r, n = [], []
    def add(p, what): r.append(p); n.append(f"image {len(r)} = {what}")
    if first: add(first, "the approved still, the first frame")
    if s["product"]:
        add(SHEET, "the product reference sheet built from real photos of this exact navy topper")
        add(PRINT, "a real close-up of the light-blue 'Bamboo' word and leaf print")
        if s.get("tag"): add(TAG, "a real close-up of the small light-blue Niagara tag")
        add(EDGE, "a real close-up of the puffy rolled border and the smooth navy skirt")
    if not first: add(ROOM[s["room"]], "the real room photo to use as the setting")
    if s["hand"]: add(HAND, "Grace's hand reference sheet (skin, French-tip nails, rings, bare wrist)")
    return r, n


def fix_numbers(text, s, first):
    # the blocks say image 1/2/3 for sheet/print/tag; shift when a first frame comes first
    if not s["product"]: return text
    off = 1 if first else 0
    m = {"image 1": f"image {1+off}", "image 2": f"image {2+off}", "image 3": f"image {3+off}"}
    for k in sorted(m, reverse=True): text = text.replace(k, m[k].upper().replace("IMAGE", "IMG#"))
    return text.replace("IMG#", "image")


def still(s):
    r, n = refs(s)
    t = [B["size_first"] if s["product"] or s["id"] in ("S1", "S2") else "", s["still"],
         B["hand_block"] if s["hand"] else B["no_hand"],
         fix_numbers(B["topper_block"], s, None) if s["product"] else "No topper on the bed: a plain white mattress and white bedding only.",
         fix_numbers(B["tag_block"], s, None) if s.get("tag") else "",
         B["room_" + s["room"]], B["suffix"], "Reference images: " + "; ".join(n) + "."]
    return r, " ".join(x for x in t if x)


def clip(s):
    first = f"stills/{s['id']}.png"
    r, n = refs(s, first)
    if s["product"]:
        head = B["omni_head"].replace("{hand}", " and the same hands, rings, bare wrist" if s["hand"] else "")
        head = head.replace("image 2", "image 3").replace("Recreate image 1", "Recreate image 1")
        body = f"{head} Motion: {s['motion']} {B['omni_tail']} References: " + "; ".join(n) + "."
    else:
        body = f"Recreate image 1 exactly as the first frame{', same hand, nails, rings, bare wrist as the hand sheet' if s['hand'] else ''}, then: {s['motion']} {B['omni_tail']} References: " + "; ".join(n) + "."
    return r, body


Path("prompts").mkdir(exist_ok=True); R = {}
for s in D["shots"]:
    a, p = still(s); Path(f"prompts/still_{s['id']}.txt").write_text(p)
    b, q = clip(s); Path(f"prompts/{s['id']}.txt").write_text(q)
    R[s["id"]] = {"still": a, "clip": b, "model": "omni" if s["product"] else "seedance"}
Path("prompts/refs.json").write_text(json.dumps(R, indent=1)); print("built", len(R))
