"""Writes shots.json (the one source for stills, clips and the cut). Edit SHOTS here, run it, then python3 qc/gates_check.py shots."""
import json
HAND = ("Grace's hand only (no face, no body): medium-brown skin, medium-length pink French-tip nails, a chunky gold LINK BRACELET (a bracelet only: NO watch, no watch face, no dial) "
        "plus a thin gold chain with small pearls and a gold leaf charm on the wrist, a solid sky-blue silicone band ring on the ring finger, exactly as in the hand "
        "reference photos. Only the hand and wrist enter from the frame edge, no forearm, the hand small next to the heater; it grips what it touches.")
HEATER = ("The space heater exactly as in the product reference sheet: a small matte-black cylinder, 8.7 in tall and 6.2 in wide (height about 1.4 x "
          "width), fine hexagon-hole black mesh all around, a rectangular heater window with vertical bars behind the mesh on the lower-middle front, "
          "a plain dark base band, and on top a round glossy black touch panel with a white '73' display, small white outlined buttons and one red "
          "power button, ringed by short vent slots. No knobs, no front handle, no logo or text on the body, no orange glow, no heat streaks.")
SCENE = ("Bright neutral daylight, true colours, no golden or yellow tint, no dark corners. Phone-camera photo, real room, keep the room from the "
         "room reference photo. The heater stands on the floor or a hard surface with clear space around it, nothing touching it. Nothing at any "
         "edge of the frame, no people, no text, no watermark, no date stamp.")
# (id, line, room, hand?, still, motion)   hand=True -> Seedance 2.0 Mini (Kie, reference mode); False -> Kling 3.0 (Ralph's account)
SHOTS = {
 "V1": [
  ("V1S1", "I know I cannot be the only one who has that one room that never warms up.", "V1_window_nook_armchair", False,
   "Wide view of the window nook: the heater stands on the bare wood FLOOR about two feet in front of the sofa, never on the sofa or any cushion, nothing touching it, soft daylight from the window.",
   "Slow walk-in dolly from the doorway toward the heater, slight handheld feel. Only the camera moves."),
  ("V1S2", "You turn the heat up for the whole house, and that room is still cold.", "V1_breakfast_table", True,
   "A plain white digital wall thermostat on the wall beside the breakfast table; the index finger presses its up arrow. No heater in this shot.",
   "The finger presses the thermostat up arrow twice, then the hand leaves the frame to the right. The camera holds steady."),
  ("V1S3", "So this little heater just goes wherever you are.", "V1_bedroom_desk_sun", True,
   "One hand comes in from the top edge of the frame and carries the heater by its top rim: thumb on one side, fingers curled around and under the rim on the other side, a real grip; the heater hangs a few inches above the bedroom floor. Only the hand and wrist are in frame, no arm.",
   "The hand carries the heater slowly to the right, keeping it upright and at the same distance from the camera; the camera pans with it."),
  ("V1S4", "Bedroom in the morning,", "V1_nightstand_gold", False,
   "The heater stands on the wood floor next to the gold nightstand, morning light.",
   "Slow low arc around the heater from left to right. Only the camera moves; the room stays still."),
  ("V1S5", "your desk during the day,", "V1_office_yellow_chair", True,
   "The heater stands on the floor beside the desk and the yellow chair. It is SHORT: 8.7 inches tall, about twice the height of a coffee mug, a squat cylinder, NOT a tall tower. On the desk, the hand sets down a white coffee mug, index and middle fingers through the mug handle and the thumb on top of it.",
   "The hand puts the mug down and slides out of frame; the camera slowly pushes in toward the heater."),
  ("V1S6", "the couch at night.", "V1_living_cream_sofa", False,
   "The heater stands on the rug in front of the cream sofa, a knit throw on the sofa arm, soft lamp light plus daylight (still bright).",
   "Slow sideways truck past the sofa toward the heater. Only the camera moves; the rug and sofa stay still."),
  ("V1S7", "It's fifteen hundred watts and heats up fast. And it's quiet.", "V1_breakfast_table", True,
   "The heater stands on the breakfast table; both hands come in from the bottom edge, palms open toward the heater a few inches from the mesh, not touching it; only hands and wrists in frame, the hands no bigger than the heater.",
   "The hands rub together slowly, then hold open toward the heater again. The heater and the table do not move."),
  ("V1S8", "You set the exact temperature right on top or with the remote, and there's an ECO mode.", "V1_office_yellow_chair", True,
   "Close top-down view of the heater's touch panel on the desk, exactly the REAL panel in reference image 5: a white '73' display in the centre, six small white-outlined round buttons in an arc on the left and lower edge, and one red power button on the right; no X button, no snowflake button. The index fingertip touches one outlined button on the lower edge.",
   "The fingertip taps the plus button twice, the display stays lit, the finger lifts away. Camera fixed, very slight push-in."),
  ("V1S9", "The only problem? Whoever gets it first is not giving it back.", "V1_living_cream_sofa", False,
   "Closer view from a low angle: the heater on the rug, the cream sofa and knit throw behind it.",
   "Slow push-in on the heater. Only the camera moves."),
  ("V1S10", "Grab one for the bedroom and one for your desk before the cold really hits. It's in the orange cart.", "V1_bedroom_desk_sun", False,
   "ONE heater on the bedroom floor in the sun patch near the bed, the desk and window behind.",
   "Slow pull-back and slight rise, ending on a calm wide view. Only the camera moves."),
 ],
 "V2": [
  ("V2S1", "Before you buy this, look at what happens when it tips over.", "V2_living_grey_sofa", True,
   "The heater lies on its side on the wooden floor in front of the grey sofa, its top panel dark; the hand grips the top rim, about to stand it up.",
   "The hand stands the heater upright in one smooth move and lets go; the heater keeps its exact shape. Camera steady, slight push-in."),
  ("V2S2", "If you have kids or a dog running around, the last thing you want is a heater falling over and staying on.", "V2_living_navy_sofa", False,
   "Low view across the rug: the heater stands on the floor near the navy sofa, a rope dog toy and a small toy block on the rug in front.",
   "Low slow dolly along the rug toward the heater. Only the camera moves; the toys and rug stay still."),
  ("V2S3", "This one has a tip-over sensor, so if it gets knocked over, it shuts itself off.", "V2_reading_window_seat", False,
   "The heater lies on its side on the floor below the window seat, its top panel dark (off).",
   "Slow push-in toward the dark top panel. Only the camera moves; nothing in the room moves."),
  ("V2S4", "It has overheat protection too.", "V2_reading_window_seat", False,
   "The heater stands upright on the floor beside the window seat, bright daylight.",
   "Slow arc around the heater from right to left. Only the camera moves."),
  ("V2S5", "And there's a child lock, so little fingers can't change the settings.", "V2_nightstand_white_x", True,
   "Close top-down view of the heater's touch panel beside the white nightstand; the index fingertip presses and holds the small lock button.",
   "The fingertip holds the lock button, then lifts away. Camera fixed, very slight push-in."),
  ("V2S6", "You pick the exact temperature and it warms the room fast. It's quiet, too.", "V2_desk_laptop_mug", True,
   "The heater stands on the white desk next to the laptop and the mug; the fingertip touches the plus button on its top panel.",
   "The finger taps the plus button once and moves away; the camera drifts slowly right."),
  ("V2S7", "Honestly, the remote is what makes you lazy. You change the heat without leaving the couch.", "V2_living_navy_sofa", True,
   "Over the sofa arm: the hand holds the small black remote (as in the reference sheet), thumb on a button, the heater on the floor ahead, a little soft.",
   "The thumb presses the button twice; the hand stays relaxed. Slight handheld drift."),
  ("V2S8", "Get one for the living room and one for the bedroom before it gets really cold.", "V2_bedroom_big_window", False,
   "ONE heater on the floor at the foot of the bed by the big window, morning sun.",
   "Slow walk-in dolly toward the heater. Only the camera moves."),
  ("V2S9", "It's in the orange cart.", "V2_bedroom_big_window", True,
   "Both hands warm themselves a few inches in front of the heater's mesh beside the bed, palms open, not touching it.",
   "The hands rub together once and open toward the heater again. The heater does not move."),
 ],
 "V3": [
  ("V3S1", "I am apparently at the age where this excites me.", "V3_nightstand_drawers", True,
   "Close top-down view of the heater's touch panel next to the white drawer nightstand; the panel is dark (off); the index fingertip touches the red power button.",
   "The finger taps the red power button, the white '73' display lights up, the finger lifts away. Camera fixed, slight push-in."),
  ("V3S2", "It's six in the morning, the floor is freezing, and I am not heating the whole house just to get dressed.", "V3_bed_curtains", False,
   "View through the sheer curtains to the bed; the heater stands on the floor at the side of the bed.",
   "Slow walk-in through the gap in the curtains toward the heater; the curtains stay still. Only the camera moves."),
  ("V3S3", "This little heater sits right by the bed.", "V3_bed_lamp_sun", False,
   "Low view along the floor: the heater by the bed, the brass lamp above, a stripe of sun on the wall.",
   "Low slow slide along the floor toward the heater. Only the camera moves."),
  ("V3S4", "Tap the top, pick the exact temperature, and it holds the room right there.", "V3_desk_white", True,
   "The heater stands on the white desk beside the laptop; the fingertip taps the plus button on its top panel, display lit.",
   "The finger taps the plus button twice and moves away; the camera pushes in slightly."),
  ("V3S5", "ECO mode is there when you want to save energy.", "V3_living_round_table", False,
   "The heater stands on the round wooden coffee table in the white living room, sofa behind.",
   "Slow arc around the heater from left to right. Only the camera moves."),
  ("V3S6", "There's a timer up to twenty-four hours, so it turns off on its own.", "V3_living_white_mirror", True,
   "The hand holds the small black remote (as in the reference sheet), thumb on the clock button; the heater on the floor by the white sofa ahead, a little soft.",
   "The thumb presses the button once; slight handheld drift."),
  ("V3S7", "People say it's bigger than they expected, but it's still easy to carry room to room.", "V3_living_round_table", True,
   "The hand holds the heater by its top rim from above, fingers curled under the rim, carrying it past the round table.",
   "The hand carries the heater slowly left to right, upright and at the same distance; the camera follows."),
  ("V3S8", "And it's quiet.", "V3_living_white_mirror", False,
   "The heater stands on the light rug in front of the white sofa, the gold mirror and plants behind.",
   "Slow push-in from a low angle. Only the camera moves."),
  ("V3S9", "With the cold coming, grab two, one for your bedroom and one for wherever you sit all day. It's in the orange cart.", "V3_bed_lamp_sun", True,
   "ONE heater on the floor by the bed; both hands warm themselves a few inches in front of the mesh, palms open, not touching it.",
   "The hands rub together slowly and open toward the heater again. The heater does not move."),
 ],
}
out = {"hand_block": HAND, "heater_block": HEATER, "scene_block": SCENE,
       "video_suffix": "Real phone video, natural motion, the heater keeps its exact shape, size and top panel in every frame, no text.",
       "shots": [{"id": i, "video": v, "line": l, "room": f"rooms/{r}.jpg", "hand": h, "kind": "HAND" if h else "HAND-FREE",
                  "model": "seedance-mini-refs" if h else "kling-3.0", "dur": 5, "still": s, "motion": m}
                 for v, lst in SHOTS.items() for (i, l, r, h, s, m) in lst]}
for s in out["shots"]:
    s["heater"] = s["id"] != "V1S2"   # the thermostat shot shows no heater
    s["panel"] = s["id"] in ("V1S8",)   # top-panel close-ups
json.dump(out, open("shots.json", "w"), indent=1)
for v in SHOTS: print(v, sum(not x[3] for x in SHOTS[v]), "hand-free of", len(SHOTS[v]))
