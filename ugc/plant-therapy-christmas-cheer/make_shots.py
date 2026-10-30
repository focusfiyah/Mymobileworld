"""Shots + prompts for Plant Therapy Christmas Cheer (Grace, 15 s). Written with prompt-master (Ralph's stack), 2026-10-30.
Writes shots.json. Windows are estimates (3.6 words/s) until the voiceover's word times."""
import json
R = {"ROOM_A": "rooms/pick/A_armchair_tree.jpg", "ROOM_B": "rooms/pick/B_gift_table.jpg", "ROOM_C": "rooms/pick/C_coat_closet.jpg",
     "TREE": "refs/closeup_tree.png", "PLUM": "refs/closeup_plum.png", "VAN": "refs/closeup_vanilla.png", "BOX": "refs/closeup_box.png",
     "NECK": "refs/real_neck_capoff.jpg", "SHEET": "refs/product_sheet.png", "HAND": "grace/ref/hand-sheets/without_bracelet.jpg"}
NAME = {"ROOM_A": "the real room photo (red velvet armchair, plaid pillow, striped tree pillow, a decorated artificial Christmas tree with silver tinsel, red and white striped wall)",
        "ROOM_B": "the real room photo (gift-wrapping table with pink and gold wrapped gifts, a pink-lit Christmas tree behind)",
        "ROOM_C": "the real room photo (coat closet with colourful coats on hangers, wooden hangers, white wire baskets)",
        "TREE": "the real Christmas Tree bottle: hot pink label, chartreuse yellow-green tree with a yellow star and pale aqua dots, dark green 'Plant Therapy', 'Christmas Tree', 'ESSENTIAL OIL BLEND', white 'KidSafe' pill, '1/3 FL. OZ. (10 mL)'",
        "PLUM": "the real Sugar Plum Fairy bottle: soft lavender label, big cream-peach blob, small purple stars, dark green 'Plant Therapy', 'Sugar Plum Fairy', 'ESSENTIAL OIL BLEND', white 'KidSafe' pill, '1/3 FL. OZ. (10 mL)'",
        "VAN": "the real Vanilla Spice bottle: cream label, big taupe-brown circle, dark plum vanilla pod, olive leaves, a cinnamon stick, dark green 'Plant Therapy', 'Vanilla Spice', 'ESSENTIAL OIL BLEND', no KidSafe pill, '1/3 FL. OZ. (10 mL)'",
        "BOX": "the real Christmas Cheer box: white carton with small pink, orange, purple and green stars and a thin line ornament, dark text 'Plant Therapy', 'Christmas Cheer', 'Essential Oil Blend Set', 'Christmas Tree, Sugar Plum Fairy, & Vanilla Spice'",
        "NECK": "a real photo of the open bottle neck: a black ring stays on the neck and a small clear-white plastic dropper insert sits in the opening",
        "SHEET": "the product sheet made from real photos (front, back, box, cap off)",
        "HAND": "Grace's hand sheet"}
PRINT = "every label and print matches its image letter for letter and colour for colour"
BOTTLE = ("small amber glass bottle, round with straight sides and a rounded shoulder, a black ribbed screw cap with a smooth black band under the ribs, "
          "the label wrapped round the middle with bare amber glass above it and a dark band of glass below it; no dropper bulb, no pump, no roller ball")
SIZE = "SIZE FIRST: each bottle is small, about 6 cm tall with its cap and 2.5 cm wide, about as tall as an adult thumb; the hand looks big next to it."
SIZE_FREE = "SIZE FIRST: each bottle is small, about 6 cm tall with its cap and 2.5 cm wide, about as tall as a lipstick."
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch, the whole wrist visible; "
        "the hand enters from the frame edge")
HANDS = HAND.replace("Grace's hand exactly", "Grace's two hands exactly").replace("the whole wrist visible", "both whole wrists visible").replace("the hand enters from the frame edge", "the hands enter from the frame edge")
END = "Vertical 9:16 phone photo, bright neutral daylight, true colours, realistic textures, no text, no captions, no watermark, no logos other than the real labels."
CLIPEND = "Bright neutral daylight. No music, no voice, no captions, no on-screen text."
NOHAND = "No hand, fingers or people appear at any time."
SEED = "Recreate reference image 1 exactly as the first frame, then "
LINES = ["You know that moment when the fake tree's up,", "but the house doesn't smell like Christmas?", "Ours smelled like the storage box.",
         "A few drops of Christmas Tree in my diffuser,", "and now people ask where the real tree is.", "Get one to gift too before Christmas.", "It's in the orange cart."]
T = [(0.0, 2.5), (2.5, 4.4), (4.4, 6.1), (6.1, 8.6), (8.6, 11.0), (11.0, 13.1), (13.1, 14.8)]


def refs_text(keys, first=1):
    return " ".join(f"Image {i + first} is {NAME[k]}." for i, k in enumerate(keys))


def shot(n, hand, product, room, still_keys, still, clip_keys, motion):
    s = {"id": f"S{n}", "t": T[n - 1], "line": LINES[n - 1], "hand": hand, "product": product, "room": room,
         "still_refs": [R[k] for k in still_keys], "still": refs_text(still_keys) + " " + still + " " + END}
    if product:   # Omni on Kie / Flow: image 1 = approved still, then the real close-ups, then the sheet
        head = "Recreate image 1 exactly as the first frame: keep its room, light" + (", framing and hand" if hand else " and framing") + " exactly. "
        s["clip_refs"] = [f"stills/S{n}.png"] + [R[k] for k in clip_keys]
        s["clip"] = head + refs_text(clip_keys, first=2) + " " + PRINT[0].upper() + PRINT[1:] + "; the product keeps its exact small size and shape, no added marks. Motion: " + motion + " " + \
            ("The hand keeps one grip and nothing turns, flips or changes shape." if hand else NOHAND) + " " + CLIPEND
        s["model"] = "Omni 1.1 Flash (Flow $0 / Kie $0.315)"
    else:
        s["clip_refs"] = [f"stills/S{n}.png"]
        s["clip"] = SEED + motion + " No bottles, no box, no product at any time. " + ("" if hand else NOHAND + " ") + CLIPEND
        s["model"] = "Seedance 2.0 Mini on Kie ($0.164)"
    return s


SHOTS = [
 shot(1, False, True, "A", ["ROOM_A", "TREE", "PLUM", "VAN", "SHEET"],
      "Show the room of image 1 exactly: the red velvet armchair with its pillows and the decorated artificial Christmas tree with silver tinsel. Add one small round light-wood side table in the lower left foreground. "
      f"On it stand exactly three bottles in a row, left to right: Christmas Tree (image 2), Sugar Plum Fairy (image 3), Vanilla Spice (image 4), labels facing the camera. Each is a {BOTTLE}; {PRINT}; image 5 shows their true shape. {SIZE_FREE} "
      "The bottles are sharp in the lower third, the tree and armchair behind them. No hand, no fingers, no people, no diffuser.",
      ["TREE", "PLUM", "VAN", "SHEET"], "only the camera moves, a slow push-in past the three bottles toward the Christmas tree; the bottles never move."),
 shot(2, True, False, "A", ["ROOM_A", "HAND"],
      "Close-up of the decorated artificial Christmas tree from image 1: plastic needle tips with silver tinsel, a gold bauble and a red bauble, the red armchair soft behind. "
      f"{HAND} on the right and pinches one plastic branch tip between thumb and fingers. No bottles, no box, no diffuser, no product.",
      [], "the fingers bend the plastic branch tip down and let it spring back up, the tinsel shivers; the camera holds still. No face at any time."),
 shot(3, True, False, "C", ["ROOM_C", "HAND"],
      "Show the coat closet of image 1 exactly. On its floor in the foreground sits a clear plastic storage tote with a grey snap lid, packed with folded green artificial tree branch sections and a few red and gold baubles. "
      + HANDS.replace("from the frame edge", "from the bottom frame edge") + "; both hands grip the two sides of the grey lid, lifting it a little. No bottles, no box, no product, no face.",
      [], "both hands lift the grey lid up and away out of the top of the frame, showing the folded branches inside; the camera tilts down a little into the tote. No face at any time."),
 shot(4, True, True, "A", ["ROOM_A", "TREE", "NECK", "SHEET", "HAND"],
      "On the small light-wood side table beside the red armchair of image 1 sits a matte white ceramic ultrasonic diffuser with its top cover off, its round tank half full of clear water. "
      f"{HAND} at the upper right and GRIPS ONE bottle, the Christmas Tree bottle of image 2 ({PRINT}): a {BOTTLE}. It is cap off, tilted down at 45 degrees over the open water tank with its label facing the camera: "
      "the open neck shows the black ring and the small clear-white plastic dropper insert of image 3. Thumb on the side of the label, fingers wrapped around the back. "
      f"Image 4 shows its true shape. {SIZE} One drop hangs from the dropper insert. No other bottles, no box.",
      ["TREE", "NECK", "SHEET"], "two drops fall one after the other from the dropper insert into the water and small ripples spread; the bottle stays tilted the same way."),
 shot(5, False, False, "A", ["ROOM_A"],
      "Show the room of image 1: in the foreground a matte white ceramic ultrasonic diffuser stands on a small round light-wood side table with soft white mist rising from its top; "
      "the decorated artificial Christmas tree with silver tinsel and the red armchair behind it. No bottles, no box, no product. No hand, no fingers, no people.",
      [], "the soft white mist keeps rising and curling up from the diffuser while the camera makes a slow small arc to the left around it."),
 shot(6, True, True, "B", ["ROOM_B", "BOX", "SHEET", "HAND"],
      f"At the gift-wrapping table of image 1 (pink-lit tree and pink and gold wrapped gifts kept). {HAND} on the right and GRIPS the closed Christmas Cheer box of image 2 "
      f"by its two sides (thumb on one side, fingers on the other), box front facing the camera, {PRINT}; image 3 shows the real box and bottles. "
      "The box is small, about as wide as three small bottles side by side and a little taller than one bottle; the hand looks big next to it. "
      "It is held just above an open plain kraft-paper gift bag with red tissue paper. One box only, no loose bottles.",
      ["BOX", "SHEET"], "the hand lowers the box straight down into the gift bag until half of it is inside; the red tissue paper rustles."),
 shot(7, False, True, "A", ["ROOM_A", "BOX", "TREE", "PLUM", "VAN", "SHEET"],
      "Low close view of the small round light-wood side table beside the red armchair of image 1, the tinsel tree soft behind. "
      f"On it the closed Christmas Cheer box of image 2 stands upright, and in front of it exactly three bottles in a row, left to right: Christmas Tree (image 3), Sugar Plum Fairy (image 4), Vanilla Spice (image 5), "
      f"labels facing the camera. Each is a {BOTTLE}; {PRINT}; image 6 shows their true shape. {SIZE_FREE} One set only. No hand, no fingers, no people, no diffuser.",
      ["BOX", "TREE", "PLUM", "VAN", "SHEET"], "only the camera moves, a slow push-in toward the box and the three bottles; nothing moves."),
]
json.dump({"job": "plant-therapy-christmas-cheer", "refs": R, "shots": SHOTS}, open("shots.json", "w"), indent=1)
print(len(SHOTS), "shots;", sum(not s["hand"] for s in SHOTS), "hand-free;", sum(s["product"] for s in SHOTS), "product clips")
