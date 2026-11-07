"""V3 shots + prompts (song-only, Grace's text on screen), written with prompt-master (Ralph's stack), 2026-11-07.
Writes shots_v3.json. Constants (label words, bottle, hand, size) come from make_shots.py so V1/V2/V3 describe the
product the same way. Product clips: Wan 3.0 720P on Kie (Ralph tapped "All on Kie"), names Image1, Image2 ...
One room (A) for every shot. Text is burned in by the cut, never by a model: every prompt says no text."""
import json, re
src = open("make_shots.py").read()
exec(src[:src.index("def refs_text")])   # R, NAME, PRINT, BOTTLE, SIZE, SIZE_FREE, HAND, END, CLIPEND, NOHAND, SEED

T = [(0.0, 2.0), (2.0, 4.0), (4.0, 6.0), (6.0, 8.0), (8.0, 10.0), (10.0, 12.0)]
ROOM = ("The whole shot is inside the room of image 1 and nowhere else: the same red velvet armchair, green-and-red plaid pillow, "
        "red-and-cream striped tree-shaped pillow, white fluffy throw, the small decorated artificial Christmas tree with silver tinsel and a gold star, "
        "and the thin red-and-white striped wall.")
FRAME_TXT = "Keep the top half of the frame calm and uncluttered (wall, tree, armchair back), the product in the lower half."


def refs_text(keys, first=1, wan=False):
    return " ".join((f"Image{i + first}" if wan else f"Image {i + first}") + f" is {NAME[k]}." for i, k in enumerate(keys))


def shot(n, hand, product, still_keys, still, clip_keys, motion, secs):
    s = {"id": f"S{n}", "t": T[n - 1], "hand": hand, "product": product, "room": "A", "secs": secs,
         "still_refs": [R[k] for k in still_keys], "still": refs_text(still_keys) + " " + ROOM + " " + still + " " + (FRAME_TXT if product else "Keep the top half of the frame calm and uncluttered.") + " " + END}
    if product:
        head = "Recreate Image1 exactly as the first frame: keep its room, light" + (", framing and hand" if hand else " and framing") + " exactly. "
        s["clip_refs"] = [f"stills/v3_S{n}.png"] + [R[k] for k in clip_keys]
        s["clip"] = head + refs_text(clip_keys, first=2, wan=True) + " " + PRINT[0].upper() + PRINT[1:] + \
            "; the product keeps its exact small size and shape, no added marks, no extra bottles. Motion: " + motion + " " + \
            (HOLD.get(n, "The hand keeps one grip and nothing turns, flips or changes shape.") if hand else NOHAND) + " " + CLIPEND
        s["model"] = f"Wan 3.0 720P on Kie, {secs} s ${0.08 * secs:.2f} + free upscale"
    else:
        s["clip_refs"] = [f"stills/v3_S{n}.png"]
        s["clip"] = SEED + motion + " No bottles, no box, no product at any time. " + NOHAND + " " + CLIPEND
        s["model"] = f"Seedance 2.0 Mini on Kie, {secs} s $0.164"
    return s


HOLD = {2: "The bottle itself never turns, tips, flips or changes shape; only the cap twists and lifts."}
TRAY = "a small round light-wood tray resting flat on the armchair seat in front of the plaid pillow"
SHOTS = [
 shot(1, False, True, ["ROOM_A", "TREE", "PLUM", "VAN", "SHEET"],
      f"Low camera at seat height, a little to the left. On {TRAY} stand exactly three bottles in a row, left to right: Christmas Tree (image 2), Sugar Plum Fairy (image 3), "
      f"Vanilla Spice (image 4), labels facing the camera, caps on. Each is a {BOTTLE}; {PRINT}; image 5 shows their true shape. {SIZE_FREE} "
      "The tinsel tree is soft behind them on the left. No hand, no fingers, no people, no diffuser, no box.",
      ["TREE", "PLUM", "VAN", "SHEET"], "only the camera moves, a slow sideways dolly from left to right along the three bottles at seat height; the bottles never move.", 5),
 shot(2, True, True, ["ROOM_A", "TREE", "NECK", "SHEET", "HAND"],
      "Close-up on the white fluffy throw draped over the armchair arm, the red velvet soft behind. One bottle stands upright on the throw: the Christmas Tree bottle of image 2, "
      f"a {BOTTLE}; {PRINT}; image 4 shows its true shape. Its black cap is still ON. {HAND} at the top right; the thumb and first two fingers GRIP the black ribbed cap from above, "
      f"ready to twist it, the pink label facing the camera. Image 3 shows what the open neck looks like (for the clip). {SIZE} No other bottles, no box, no diffuser.",
      ["TREE", "NECK", "SHEET"], "the fingers twist the black cap a quarter turn and lift it straight up off the bottle, showing the black ring on the neck and the small clear-white dropper insert of Image3; the bottle stays standing on the throw, label to the camera; the camera holds still.", 5),
 shot(3, False, False, ["ROOM_A"],
      "Low angle from the wooden floor beside the base of the decorated artificial Christmas tree: a matte white round ultrasonic diffuser stands on the floor by the tree, "
      "a soft ribbon of white mist rising from its top, the red armchair at the right edge. No bottles, no box, no product. No hand, no fingers, no people.",
      [], "the white mist rises in a slow soft ribbon while the camera slowly rises up past the tinsel toward the gold star at the top of the tree.", 4),
 shot(4, True, True, ["ROOM_A", "PLUM", "SHEET", "HAND"],
      f"Close-up of {TRAY}, a few small gold baubles lying on it. {HAND} on the right and GRIPS ONE bottle, the Sugar Plum Fairy bottle of image 2, upright, a {BOTTLE}; {PRINT}. "
      f"Its black cap is ON; thumb on the side of the label, fingers wrapped around the back; the bottle is held 3 cm above the tray, lavender label facing the camera. "
      f"Image 3 shows its true shape. {SIZE} No other bottles, no box, no diffuser, no fruit.",
      ["PLUM", "SHEET"], "the hand slowly sets the bottle down upright on the tray beside the gold baubles, lets go and slides out of the frame to the right; the bottle stays still; the camera holds.", 5),
 shot(5, True, True, ["ROOM_A", "VAN", "SHEET", "HAND"],
      f"Close-up on a small light-wood stool standing right beside the red armchair: on its round top a white ceramic mug of hot cocoa with one cinnamon stick standing in it, a thin wisp of steam. {HAND} on the left and GRIPS ONE bottle, "
      f"the Vanilla Spice bottle of image 2, upright beside the mug, a {BOTTLE}; {PRINT}. Its black cap is ON; thumb on the side of the label, fingers around the back; the cream label faces the camera. "
      f"Image 3 shows its true shape. {SIZE} No other bottles, no box, no diffuser.",
      ["VAN", "SHEET"], "the hand sets the bottle down upright next to the mug, lets go and slides out of the frame to the left; the thin steam keeps curling up from the cocoa; the camera holds.", 5),
 shot(6, False, True, ["ROOM_A", "BOX", "TREE", "PLUM", "VAN", "SHEET"],
      "On the red velvet armchair seat, in front of the striped tree-shaped pillow: the closed Christmas Cheer box of image 2 standing upright, front facing the camera, "
      f"and in front of it exactly three bottles in a row, left to right: Christmas Tree (image 3), Sugar Plum Fairy (image 4), Vanilla Spice (image 5), labels facing the camera, caps on. "
      f"Each is a {BOTTLE}; {PRINT}; image 6 shows their true shape. The box is a little taller than one bottle and about three bottles wide (as in image 6). {SIZE_FREE} No hand, no fingers, no people, no diffuser.",
      ["BOX", "TREE", "PLUM", "VAN", "SHEET"], "only the camera moves, a slow small arc from the right to the front of the box and bottles; nothing on the seat moves.", 5),
]
json.dump({"job": "plant-therapy-christmas-cheer", "video": "V3", "refs": R, "order": [s["id"] for s in SHOTS], "shots": SHOTS}, open("shots_v3.json", "w"), indent=1)
print("wrote shots_v3.json", len(SHOTS))
