"""Nello Superfocus shots.json (2026-11-03). Prompts written with prompt-master (Ralph's stack). Run: python3 tools_make_shots.py"""
import json
HAND = ("HER HAND: Grace's real hand exactly as the hand reference: medium-brown skin with lighter palms, medium-length "
        "squoval nails with mauve-pink polish and white French tips, NO rings, NO bracelet, NO watch. The hand enters "
        "from the frame edge, the whole wrist shows, nothing of the background shows through the hand.")
LOOK = ("Vertical 9:16 phone photo, bright neutral daylight from a window, true colours, no yellow or golden cast, "
        "realistic skin. No text, no captions, no logos, no readable words on any screen or paper.")
LOOK_P = ("Vertical 9:16 phone photo, bright neutral daylight from a window, true colours, no yellow or golden cast, "
          "realistic skin. No captions and no text or logos anywhere except the real print on the tub; no readable "
          "words on any screen or paper.")
ROOM = ("the home office in the room reference (warm light-wood desk, white shelves with teal and blue books, bright "
        "window light), softly out of focus")
SIZE = ("SIZE FIRST: the tub is small and squat, about 10 cm across and 8 cm tall, a little wider than it is tall, "
        "about the size of a coffee mug and never bigger than her open hand.")
TUB = ("THE TUB: the real Nello Superfocus Fruit Punch tub from the product sheet and the logo close-up. A bright white "
       "screw lid with fine vertical ribs around its side, about a third of the tub's height. Below it a coral-red label "
       "with soft darker-red and orange wave bands wraps the body. Front print, all white: 'nello' in rounded lowercase "
       "with a small (R), then 'Focus Drink Mix' in thin italic; below it 'SUPER' in tall bold capitals right beside "
       "'FOCUS' in thin italic capitals with a small TM; lower left a small pale-pink rounded badge 'FRUIT PUNCH' in "
       "white bold capitals with a tiny drawing of fruit above it and 'FLAVORED' under it; lower right three small "
       "white lines '30 Servings', 'Dietary Supplement', 'Net Wt. 155.4g (5.48oz)'. The print matches the logo close-up "
       "letter for letter and colour for colour. No blue badge, no '+ CAFFEINE' tag, no caffeine badge, no fruit, no "
       "pouch or packets, no extra marks.")
DRINK = "a tall clear glass of ice water turned clear bright fruit-punch red, ice cubes, a clear glass straw"

shots = [
 {"id": "S1", "kind": "HAND-FREE", "model": "seedance", "window": [0, 2.0], "beat": "hook + pain: 3 o'clock, same email, forty tabs",
  "still_refs": ["refs/room.jpg"],
  "still": ("SHOT: eye-level close view across the desk at a laptop, its screen a soft blurred white page with many small "
            "browser tabs along the top, nothing readable. In front of the laptop: a white coffee mug half full of cold "
            "black coffee, a phone face down, a closed pen. Image 1 is the room reference. Setting: " + ROOM + ". No "
            "hands, no people, no tub, no product of any kind. " + LOOK),
  "clip_refs": ["stills/S1.png"],
  "clip": ("Recreate reference image 1 exactly as the first frame. The camera pushes in slowly toward the laptop screen; "
           "nothing on the desk moves. No hand, fingers or people appear at any time, no product appears. Bright "
           "neutral daylight, no text.")},
 {"id": "S2", "kind": "HAND", "model": "seedance", "window": [2.0, 4.0], "beat": "one scoop in cold water",
  "still_refs": ["refs/grace_hands.jpg", "refs/room.jpg"],
  "still": ("SHOT: close-up from above and slightly in front, at desk height. Her right hand holds a clear plastic scoop "
            "with a long flat handle by its handle, fingers wrapped around it, tipping it over a tall clear glass of "
            "ice water so soft pale-pink powder pours into the water. The glass stands on the desk in the centre. No "
            "tub, jar or packet in the frame. Image 1 is her hand reference. Image 2 is the room reference. " + HAND +
            " Setting: " + ROOM + ". " + LOOK),
  "clip_refs": ["stills/S2.png"],
  "clip": ("Recreate reference image 1 exactly as the first frame. Her hand keeps one grip on the scoop handle and "
           "tips it a little further; the pale-pink powder falls into the ice water and starts to cloud it pink-red. "
           "The camera stays locked off. Same bare hand the whole clip, no rings appear, no tub or packet appears. "
           "Bright neutral daylight, no text.")},
 {"id": "S3", "kind": "HAND-FREE", "model": "seedance", "window": [4.0, 5.8], "beat": "it tastes like fruit punch",
  "still_refs": ["refs/drink_glass.png", "refs/room.jpg"],
  "still": ("SHOT: close-up of " + DRINK + " on the desk, side view at glass height, filling the middle of the frame; "
            "faint pink swirls still drifting in the red water near the top. Image 1 shows the real drink colour. "
            "Image 2 is the room reference. Setting: " + ROOM + ". No hands, no people, no tub, no product. " + LOOK),
  "clip_refs": ["stills/S3.png"],
  "clip": ("Recreate reference image 1 exactly as the first frame. The last pink swirls dissolve and the drink settles "
           "to an even clear bright red; tiny bubbles rise, the ice turns slightly. The camera pushes in very slowly. "
           "No hand, fingers or people appear at any time, no product appears. Bright neutral daylight, no text.")},
 {"id": "S4", "kind": "HAND", "model": "flow/wan", "window": [5.8, 8.0], "beat": "Nello Superfocus: lion's mane, rhodiola, alpha GPC",
  "still_refs": ["refs/product_sheet.png", "refs/logo_closeup.png", "refs/grace_hands.jpg", "refs/room.jpg"],
  "still": (SIZE + " SHOT: close-up on the desk at chest height, front of the tub facing the camera. The tub stands on "
            "the desk and her left hand has just closed around its body to pick it up: fingers wrap behind the tub, "
            "thumb on its left side below the lid, 'nello', 'SUPER FOCUS' and the FRUIT PUNCH badge stay fully visible. "
            "The red drink glass stands behind it, softly out of focus. Image 1 is the product sheet. Image 2 is the "
            "real logo close-up. Image 3 is her hand reference. Image 4 is the room reference. " + TUB + " " + HAND +
            " Setting: " + ROOM + ". " + LOOK_P),
  "clip_refs": ["stills/S4.png", "refs/logo_closeup.png", "refs/product_sheet.png"],
  "clip": ("Recreate Image1 exactly as the first frame: keep its desk, light, framing and hand exactly. Image2 is the "
           "real 'nello Focus Drink Mix SUPER FOCUS' label print with the FRUIT PUNCH badge: it stays on the tub the "
           "whole clip and matches Image2 letter for letter and colour for colour. Image3 is the product sheet: keep "
           "this exact squat tub shape, small size, white ribbed lid and coral-red label, no added marks, no blue "
           "badge, no extra text. Motion: her hand keeps one grip and lifts the tub slowly about a hand's width off the "
           "desk toward the lens; the front stays facing the camera, the tub never turns, tilts away or flips. Camera: "
           "slow push-in. Vertical 9:16 phone footage, bright neutral daylight, realistic skin. No music, no voice, no "
           "captions, no on-screen text.")},
 {"id": "S5", "kind": "HAND", "model": "seedance", "window": [8.0, 10.0], "beat": "now I have no excuse (to-do list)",
  "still_refs": ["refs/drink_glass.png", "refs/grace_hands.jpg", "refs/room.jpg"],
  "still": ("SHOT: close-up at desk height. Her right hand grips " + DRINK + " around its middle, fingers wrapped around "
            "the glass, just lifting it off the desk. Behind it an open spiral notebook with a short handwritten list, "
            "the lines are soft and unreadable. No tub, jar or packet in the frame. Image 1 shows the real drink "
            "colour. Image 2 is her hand reference. Image 3 is the room reference. " + HAND + " Setting: " + ROOM +
            ". " + LOOK),
  "clip_refs": ["stills/S5.png"],
  "clip": ("Recreate reference image 1 exactly as the first frame. Her hand keeps one grip and lifts the glass of red "
           "drink smoothly up and out of the top of the frame; the notebook stays on the desk. The camera stays locked "
           "off. Same bare hand the whole clip, no rings appear, no face appears, no product appears. Bright neutral "
           "daylight, no text.")},
 {"id": "S6", "kind": "HAND-FREE", "model": "flow/wan", "window": [10.0, 12.0], "beat": "thirty servings, keep one at your desk",
  "still_refs": ["refs/product_sheet.png", "refs/logo_closeup.png", "refs/room.jpg"],
  "still": (SIZE + " SHOT: the desk at desk height, the tub standing upright in the centre, front facing the camera, "
            "lid closed, beside " + DRINK + " on its right and a closed laptop corner on its left. The tub is the only "
            "product in the frame. Image 1 is the product sheet. Image 2 is the real logo close-up. Image 3 is the room "
            "reference. " + TUB + " No hands or people. Setting: " + ROOM + ". " + LOOK_P),
  "clip_refs": ["stills/S6.png", "refs/logo_closeup.png", "refs/product_sheet.png"],
  "clip": ("Recreate Image1 exactly as the first frame: keep its desk, light, framing and objects exactly. Image2 is "
           "the real 'nello Focus Drink Mix SUPER FOCUS' label print with the FRUIT PUNCH badge: it stays on the tub the "
           "whole clip and matches Image2 letter for letter and colour for colour. Image3 is the product sheet: keep "
           "this exact squat tub shape, small size, white ribbed lid and coral-red label, no added marks, no blue "
           "badge, no extra text. Motion: the tub and glass stay still; no hand, fingers or people appear at any time. "
           "Camera: slow dolly-in toward the tub. Vertical 9:16 phone footage, bright neutral daylight. No music, no "
           "voice, no captions, no on-screen text.")},
]
json.dump({"shots": shots}, open("shots.json", "w"), indent=1)
for s in shots:
    open(f"prompts/still_{s['id']}.txt", "w").write(s["still"])
    open(f"prompts/{s['id']}.txt", "w").write(s["clip"])
print("ok", len(shots))
