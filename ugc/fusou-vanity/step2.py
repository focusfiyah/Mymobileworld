"""Plan v2 step 2 (Ralph OK 2026-10-03): stills M2 M3 M4 M5 B1, $0.09 each = $0.45 (M6 = free crop of the cleaned real photo).

  python3 step2.py M2 M3 ...   -> stills/<ID>_raw.png + stills/<ID>.png (pasted back onto refs/base_<ID>.png; B1 has no product, no paste-back)
Hands like Ralph's example (@sdbby88): ONLY the hand enters from a frame edge, wrist at the edge, no forearm.
"""
import subprocess, sys
from concurrent.futures import ThreadPoolExecutor
import kie
J = kie.J
KEEP = ("Edit the FIRST reference image, a real photo of a white vanity. KEEP EVERYTHING IN IT EXACTLY AS IT IS: do not redraw, move, resize, "
        "sharpen or recolour anything; every drawer, knob, shelf item, lipstick, wall and floor plank stays exactly the same, same framing. Only ADD ONE HAND: ")
ONLY_HAND = (" ONLY THE HAND enters the frame, from the {edge} edge: the wrist sits right at the frame edge, NO forearm and no arm visible. The hand is "
             "natural size for its distance from the camera and covers only a small part of the furniture. ")
POSE = {
 "M2": ("LEFT", "the index finger is extended and its fingertip points at, almost touching, the two USB ports on the white power plate; the other fingers "
        "are loosely curled; the hand stays below the hair dryer and does not cover the outlets."),
 "M3": ("RIGHT", "at the height of the glass desk top, the thumb and index finger lift one lipstick from the small lipstick tray on the glass top, holding "
        "it a few centimetres above the glass; the other fingers are relaxed."),
 "M4": ("RIGHT", "at the height of the stool's top drawer, the fingertips hold the small crystal knob of the stool's top drawer, as if about to pull it open."),
 "M5": ("LEFT", "at mid-height, the fingertips curl around the left edge of the tall mirror door, as if about to pull it open; the hand stays small."),
}
B1 = ("Vertical 9:16 photo, a single frame from a phone-shot UGC video. Looking down at a small, cluttered bathroom counter beside a white sink: a messy "
      "jumble of lipsticks, compacts, makeup brushes, skincare bottles, hair ties and cotton pads piled on top of each other. Two hands enter from the "
      "bottom edge, ONLY THE HANDS: the wrists sit right at the frame edge, NO forearms visible; palms down, fingers spread, about to sweep the items "
      "together. Soft daylight. " + J["blocks"]["hand"] + " The first two reference images are the hands. " + J["blocks"]["phone"])


def still(sid):
    if sid == "B1":
        body = {"prompt": B1, "image_input": [kie.upload(p) for p in kie.HAND_REFS]}
    else:
        edge, pose = POSE[sid]
        body = {"prompt": KEEP + pose + ONLY_HAND.format(edge=edge) + J["blocks"]["hand"] + " The second and third reference images show the hands. "
                + J["blocks"]["phone"], "image_input": [kie.upload(p) for p in [f"refs/base_{sid}.png"] + kie.HAND_REFS]}
    url = kie.run_task({"model": "nano-banana-pro", "input": {**body, "aspect_ratio": "9:16", "resolution": "1K"}})
    if not url: return print(sid, "FAILED (failed Kie tasks cost $0)")
    kie.fetch(url, f"stills/{sid}_raw.png")
    if sid == "B1":
        subprocess.run(["cp", "stills/B1_raw.png", "stills/B1.png"])
    else:
        subprocess.run(["python3", "pasteback.py", "still", f"refs/base_{sid}.png", f"stills/{sid}_raw.png", f"stills/{sid}.png"], check=True)
    print(sid, "ok", flush=True)


if __name__ == "__main__":
    ids = sys.argv[1:]
    if not ids: sys.exit("name the shot ids (ask Ralph before any paid call)")
    with ThreadPoolExecutor(len(ids)) as ex: list(ex.map(still, ids))
