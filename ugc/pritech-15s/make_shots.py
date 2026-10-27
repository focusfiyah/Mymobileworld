"""Builds shots.json for V2-V4 (3 x 15-20 s). Shared blocks are copied from the approved V1 prompts (ugc/pritech-cleansing-brush/shots.json).
Run: python3 make_shots.py"""
import json

SIZE = "SIZE FIRST: a slim wand, as long as her hand from wrist crease to fingertip and only about two fingers wide; her fingers look big next to it, never the other way round."
SIZE_FREE = "SIZE FIRST: a slim wand, about as long as an adult hand and only about two fingers wide."
BRUSH = ("the real PRITECH face scrubber, BLACK: one SLIM matte black curved wand, about 15-16 cm long and only about two fingers wide, about 5 times as long as it is wide; "
         "its head is a forward-tilted oval paddle that flows straight out of the handle, barely wider than the handle (no neck, no round disc, no bulb), covered in short black silicone nubs in rings, "
         "three small moulded buttons on the front of the handle top to bottom (a vibration icon ((•)), a circle O, a °C sign), a wide flat silver chrome band at the bottom end. "
         "It never glows and has no lights, no added marks, no ® or ™, no other text.")
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch, the whole wrist visible, "
        "the hand enters from the frame edge and GRIPS the handle with the fingers wrapped around it.")
ANGLE = "Show the brush from a three-quarter side angle so its gentle curve and the forward tilt of the head show, exactly like the big photo in image 1."
NOFACE = "Only her cheek and jaw are in frame; her eyes and mouth are never in frame."
END = "Vertical 9:16 phone photo, {light}, true colours, realistic skin texture, no text, no captions, no watermark."
LIGHT = {"V2": "bright neutral daylight", "V3": "bright cool daylight, crisp and clean", "V4": "bright clean morning light, neutral white balance"}
NOHAND = "No hand, no fingers, no people."
CLIPEND = "No music, no voice, no captions, no on-screen text."
KEEP = "The hand keeps one grip and the brush never turns, flips or changes shape."

def s(id, hand, product, room, line, still, clip, refs=(), btn=False, stand=False, face=False):
    v = id[:2]
    return {"id": id, "video": v, "hand": hand, "product": product, "face": face, "room": room, "line": line,
            "buttons": btn, "stand": stand, "still": still + " " + END.format(light=LIGHT[v]), "clip": clip, "clip_refs": list(refs)}

SHOTS = [
 # ---------------- V2: towel pain (rooms D blush basin, E walnut vanity), 6 shots
 s("V2S1", True, False, "D", "You know that moment you dry your face and the towel still comes up with makeup on it?",
   "Close side view of her cheek and jaw (medium-dark brown skin, damp, clean), " + NOFACE + " A blush pink towel headband just at the top edge, white tee strap at the shoulder. "
   "Grace's hand (medium-brown skin, short squared French-tip nails, silver crown ring stack, small gold heart ring, blue thumb band, bare wrist, whole wrist visible, entering from the frame edge) "
   "pulls a small plain white face towel away from her cheek; the towel faces the camera and shows clear beige foundation smears and a few black mascara marks. "
   "Blush pink basin, cream tiles and a gold tap soft behind (room reference). No brush, no product.",
   "Recreate reference image 1 exactly as the first frame, then the hand slowly pulls the white towel a little further away from the cheek and turns it a little toward the camera so the beige makeup smears read clearly. "
   "Only this one hand appears, whole wrist, the same rings as reference image 2. No brush, no product appears at any time. Her eyes and mouth never come into frame. Camera locked-off. Bright neutral daylight. " + CLIPEND, face=True),
 s("V2S2", True, False, "D", "Yeah, your hands are leaving it behind.",
   "Macro close-up of Grace's fingertips (medium-brown skin, short squared French-tip nails, the silver crown ring stack and small gold heart ring on one hand, blue thumb band, bare wrists, whole wrists) "
   "under a thin stream from a gold tap over a blush pink basin; beige foundation smudges and black mascara marks are still on the fingertips. Cream tile soft behind (room reference). No brush, no product, no face.",
   "Recreate reference image 1 exactly as the first frame, then the fingertips rub together slowly under the thin stream of water; the beige foundation and black mascara smudges stay on the fingertips. "
   "Only these two hands appear, whole wrists, the same rings as reference image 2. No brush, no product, no face at any time. Camera locked-off. Bright neutral daylight. " + CLIPEND),
 s("V2S3", True, True, "D", "This brush has soft silicone bristles",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " She holds it upright, bristle head toward the camera, and the index fingertip of her other hand presses into the black nubs so they bend softly. "
   "Water drops on the nubs. Blush pink basin and cream tile soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing and hands exactly. Image 2 is the real black bristle head; image 3 is the product sheet: keep this exact slim shape, size and matte black colour, no lights, no added marks. "
   "Motion: the fingertip presses into the nubs twice and they bend softly and spring back. " + KEEP + " Camera locked-off. Bright neutral daylight. " + CLIPEND, refs=("HEAD", "SHEET")),
 s("V2S4", True, True, "D", "and five speeds, so you get a real deep clean.",
   SIZE + " Close three-quarter view: " + NOFACE + " Her cheek is covered in white cleanser foam; blush pink towel headband at the top edge. " + HAND + " She presses the bristle head of " + BRUSH +
   " The bristle head lies flat on her foamy cheek, her thumb rests on the top vibration button ((•)). Blush pink basin and cream tile soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing, skin and hand exactly. Image 2 is the real bristle head; image 3 is the real three buttons ((•)) / O / °C, moulded black on black; image 4 is the product sheet, no added marks, no lights. "
   "Motion: the hand moves the brush in small slow circles on the foamy cheek; the foam spreads a little. " + KEEP + " Her eyes and mouth never come into frame. Camera locked-off. Bright neutral daylight. " + CLIPEND, refs=("HEAD", "BTN", "SHEET"), btn=True, face=True),
 s("V2S5", False, True, "E", "Only problem? Washing with your hands feels sad after this.",
   SIZE_FREE + " " + BRUSH + " It lies on its side on a folded white hand towel on a walnut vanity next to a round white vessel sink, the bristle head wet with water drops, the silver chrome end toward the camera. "
   "A small vase of pink flowers soft behind (room reference). " + NOHAND + " " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real bristle head and image 3 the product sheet: keep this exact slim black shape and the silver chrome end, no lights, no glow, no added marks. "
   "Motion: only the camera moves, a slow sideways dolly along the vanity; nothing in the room moves. No hand, fingers or people appear at any time. Bright neutral daylight. " + CLIPEND, refs=("HEAD", "SHEET")),
 s("V2S6", False, True, "E", "Grab one for you and one for your sister. It's in the orange cart.",
   SIZE_FREE + " One " + BRUSH + " It stands upright in its matte black stand, grey PRITECH readable on the stand front, on a walnut vanity top beside a round white vessel sink, seen from a slightly low angle. "
   "Only one brush. Round mirror and white tiles soft behind (room reference). " + NOHAND + " " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real grey PRITECH on the black stand, matching it letter for letter; image 3 is the product sheet, only one brush, no added marks, no lights. "
   "Motion: only the camera moves, a slow push-in toward the brush; nothing moves. No hand, fingers or people appear at any time. Bright neutral daylight. " + CLIPEND, refs=("LOGO", "SHEET"), stand=True),

 # ---------------- V3: the warm silver end (rooms F blue tile, G blue bath + window), 7 shots
 s("V3S1", True, True, "F", "This looked like a normal face brush until I noticed the silver end.",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " She holds it tilted toward the camera, the wide flat silver chrome end nearest the lens and the bristle head higher up, a little further away. "
   "Deep blue tile wall and a white tub soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly. Image 2 is the real three buttons ((•)) / O / °C; image 3 is the product sheet: keep this exact slim black shape and the wide flat silver chrome end, no lights, no glow, no added marks. "
   "Motion: the camera slowly pushes in toward the silver chrome end. " + KEEP + " Bright cool daylight. " + CLIPEND, refs=("BTN", "SHEET"), btn=True),
 s("V3S2", True, True, "F", "It warms up to a hundred and four degrees.",
   SIZE + " Close side view: " + HAND + " She holds " + BRUSH + " She holds it upright, buttons facing the camera, her thumb on the bottom °C button; the silver chrome end shows below her hand. "
   "Deep blue tile soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly. Image 2 is the real three buttons ((•)) / O / °C, moulded black on black, matching image 2 exactly; image 3 is the product sheet, no added marks, no lights. "
   "Motion: the thumb presses the bottom °C button once and lifts off. " + KEEP + " Camera locked-off. Bright cool daylight. " + CLIPEND, refs=("BTN", "SHEET"), btn=True),
 s("V3S3", False, False, "G", "Who has time or money for a facial every week?",
   "Spa corner of a bright blue-tiled bath: two neatly rolled thick white towels, a small eucalyptus sprig in a glass and an unlit white candle on the tub ledge, frosted window light. "
   "Calm and bright, not dark. No brush, no product, no hand, no people (room reference).",
   "Recreate reference image 1 exactly as the first frame, then the camera makes a slow sideways dolly along the tub ledge past the rolled towels; nothing in the room moves, the candle stays unlit. "
   "No brush, no product, no hand, fingers or people appear at any time. Bright cool daylight. " + CLIPEND),
 s("V3S4", True, True, "F", "Wash with the soft bristles,",
   SIZE + " Close side view: " + NOFACE + " Her cheek is covered in white cleanser foam; a light blue towel headband just at the top edge, white waffle robe at the shoulder. " + HAND + " She presses the bristle head of " + BRUSH +
   " The bristle head lies flat on her foamy cheek. Deep blue tile soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing, skin and hand exactly. Image 2 is the real bristle head; image 3 is the product sheet: keep this exact slim shape, size and black colour, no added marks, no lights. "
   "Motion: the hand moves the brush in small slow circles on the foamy cheek. " + KEEP + " Her eyes and mouth never come into frame. Camera locked-off. Bright cool daylight. " + CLIPEND, refs=("HEAD", "SHEET"), face=True),
 s("V3S5", True, True, "F", "then rub the warm end in little circles.",
   SIZE + " Close side view: " + NOFACE + " Her cheek is rinsed clean and slightly damp, no foam; light blue towel headband at the top edge, white waffle robe at the shoulder. " + HAND + " She holds " + BRUSH +
   " She holds it upside down so the wide flat silver chrome end touches her cheekbone and the bristle head points down out of the frame. Deep blue tile soft behind (room reference).",
   "Recreate image 1 exactly as the first frame: keep its room, light, framing, skin and hand exactly. Image 2 is the product sheet: keep this exact slim black shape and the wide flat silver chrome end, no lights, no glow, no steam, no added marks. "
   "Motion: the hand glides the silver end in small slow circles on the cheekbone. " + KEEP + " Her eyes and mouth never come into frame. Camera locked-off. Bright cool daylight. " + CLIPEND, refs=("SHEET",), face=True),
 s("V3S6", False, True, "F", "I hate how much I look forward to it.",
   SIZE_FREE + " " + BRUSH + " It lies on its side on a folded white waffle towel on the edge of a white tub, the wide flat silver chrome end toward the camera, water drops on the black nubs. "
   "Deep blue tile soft behind (room reference). " + NOHAND + " " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real bristle head and image 3 the product sheet: keep this exact slim black shape and the silver chrome end, no lights, no glow, no added marks. "
   "Motion: only the camera moves, a slow half-arc around the brush from the silver end toward its side; nothing moves. No hand, fingers or people appear at any time. Bright cool daylight. " + CLIPEND, refs=("HEAD", "SHEET")),
 s("V3S7", False, True, "G", "Cold weather's coming, so get one for your mom too. It's in the orange cart.",
   SIZE_FREE + " One " + BRUSH + " It stands upright in its matte black stand, grey PRITECH readable on the stand front, on the white tub ledge under a frosted window, blue tiles around. "
   "Only one brush. " + NOHAND + " (room reference) " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real grey PRITECH on the black stand, matching it letter for letter; image 3 is the product sheet, only one brush, no added marks, no lights. "
   "Motion: only the camera moves, a slow push-in toward the brush; nothing moves. No hand, fingers or people appear at any time. Bright cool daylight. " + CLIPEND, refs=("LOGO", "SHEET"), stand=True),

 # ---------------- V4: falls asleep in makeup (rooms H bedding, I marble vanity), 7 shots
 s("V4S1", False, False, "H", "This is for everybody who always falls asleep with their makeup on.",
   "Close-up of a rumpled light blue-grey pillowcase on an unmade bed in soft morning light; on the pillowcase a clear beige foundation smudge and two small black mascara marks, as if a face slept there in makeup. "
   "No person, no hand, no brush, no product (room reference).",
   "Recreate reference image 1 exactly as the first frame, then the camera slowly pushes in toward the makeup smudge on the pillowcase; the fabric does not move. "
   "No person, hand, brush or product appears at any time. Bright clean morning light. " + CLIPEND),
 s("V4S2", True, False, "I", "A quick splash with your hands leaves makeup behind.",
   "Close shot over a white marble vanity sink: Grace's two hands (medium-brown skin, short squared French-tip nails, the silver crown ring stack and small gold heart ring on the right hand, blue thumb band, bare wrists, whole wrists) "
   "cupped full of water just above the basin, the tap running; faint beige foundation marks on the fingertips. Grey vanity, marble wall and a green plant soft behind (room reference). No brush, no product, no face.",
   "Recreate reference image 1 exactly as the first frame, then the cupped hands lift the water quickly up and out of the top of the frame, and come back down wet. "
   "Only these two hands appear, whole wrists, the same rings as reference image 2. No brush, no product, no face at any time. Camera locked-off. Bright clean light. " + CLIPEND),
 s("V4S3", True, True, "I", "This brush does the work for you,",
   SIZE + " " + HAND + " Her hand lifts " + BRUSH + " up out of its matte black stand (grey PRITECH on the stand front) on a white marble vanity top, the brush just above the stand. "
   "Green plant and marble wall soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly. Image 2 is the real grey PRITECH on the black stand, letter for letter; image 3 is the real three buttons ((•)) / O / °C; image 4 is the product sheet, no added marks, no lights. "
   "Motion: the hand lifts the brush straight up out of the stand and a little toward the camera; the stand stays on the counter. " + KEEP + " Camera locked-off. Bright clean light. " + CLIPEND, refs=("LOGO", "BTN", "SHEET"), btn=True, stand=True),
 s("V4S4", True, True, "I", "with soft silicone bristles",
   SIZE + " Low angle close-up of her jawline and the side of her neck, seen from below; " + NOFACE + " White cleanser foam along the jaw, a grey tee at the shoulder. " + HAND + " She presses the bristle head of " + BRUSH +
   " The bristle head lies flat along her foamy jawline. Marble wall soft behind (room reference). " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light, framing, skin and hand exactly. Image 2 is the real bristle head; image 3 is the product sheet: keep this exact slim shape, size and black colour, no added marks, no lights. "
   "Motion: the hand moves the brush in small slow strokes along the foamy jawline. " + KEEP + " Her eyes and mouth never come into frame. Camera locked-off. Bright clean light. " + CLIPEND, refs=("HEAD", "SHEET"), face=True),
 s("V4S5", True, True, "I", "and five speeds.",
   SIZE + " Macro close-up from the front: " + HAND + " She holds " + BRUSH + " She holds it upright, buttons facing the camera, her thumb on the top vibration button ((•)); water drops sit on the black nubs. "
   "White marble and grey vanity soft behind (room reference).",
   "Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly. Image 2 is the real three buttons ((•)) / O / °C, moulded black on black, matching image 2 exactly; image 3 is the real bristle head; image 4 is the product sheet, no added marks, no lights. "
   "Motion: the thumb presses the top ((•)) button once; the water drops on the nubs shiver from the vibration. " + KEEP + " Camera locked-off. Bright clean light. " + CLIPEND, refs=("BTN", "HEAD", "SHEET"), btn=True),
 s("V4S6", False, True, "I", "I'm mad it makes washing this easy. Now I have no excuse.",
   SIZE_FREE + " " + BRUSH + " It stands upright in its matte black stand (grey PRITECH on the stand front) next to the white marble sink, wet with water drops, a small green plant beside it. "
   + NOHAND + " (room reference) " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real grey PRITECH on the black stand, letter for letter; image 3 is the product sheet, no added marks, no lights. "
   "Motion: only the camera moves, a slow arc around the brush from its side toward its front; nothing moves. No hand, fingers or people appear at any time. Bright clean light. " + CLIPEND, refs=("LOGO", "SHEET"), stand=True),
 s("V4S7", False, True, "I", "The holidays are coming, so grab one for your bestie too. It's in the orange cart.",
   SIZE_FREE + " One " + BRUSH + " It stands upright in its matte black stand, grey PRITECH readable on the stand front, on the white marble counter beside a small gift wrapped in plain white paper with a red ribbon (no tag, no text). "
   "Only one brush. " + NOHAND + " (room reference) " + ANGLE,
   "Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. Image 2 is the real grey PRITECH on the black stand, matching it letter for letter; image 3 is the product sheet, only one brush, no added marks, no lights. "
   "Motion: only the camera moves, a slow push-in toward the brush; nothing moves. No hand, fingers or people appear at any time. Bright clean light. " + CLIPEND, refs=("LOGO", "SHEET"), stand=True),
]

P = {"SHEET": "refs/product_sheet_v2.png", "HEAD": "refs/closeup_head.png", "BTN": "refs/closeup_buttons.png", "LOGO": "refs/closeup_stand_logo.png"}
HANDREF = "../../grace/ref/hand-sheets/without_bracelet.jpg"
for x in SHOTS:   # the exact text and images sent (as in V1 run.py), so prompt_check reads what is paid for
    r, names = [], []
    def add(path, what): r.append(path); names.append(f"image {len(r)} = {what}")
    if x["product"]:
        add(P["SHEET"], "the product sheet, real photos only: the big left photo is the real black brush, copy its slim shape and proportions exactly")
        add(P["HEAD"], "a real close-up of the black bristle head")
        if x["buttons"]: add(P["BTN"], "a real close-up of the three moulded buttons, black on black: ((•)) on top, O in the middle, °C at the bottom")
        if x["stand"]: add(P["LOGO"], "a real close-up of the grey 'PRITECH' print on the black stand")
    add(f"rooms/room_{x['room']}.jpg", "the real room to use as the background (same tiles, colours and light)")
    if x["hand"]: add(HANDREF, "Grace's real hand sheet (skin tone, nails, rings, bare wrist)")
    note = "Reference images: " + "; ".join(names) + "."
    if x["product"]: note += " The brush must match images 1 and 2 exactly in shape, size and matte black colour; any print matches its close-up letter for letter and colour for colour."
    x["still"] = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + x["still"] + " " + note
    x["still_refs"] = r
    still = f"stills/{x['id']}.png"
    if x["product"]: x["clip_refs"] = [still] + [P[k] for k in x["clip_refs"]]          # Omni (Flow kit / Kie): image 1 = still
    else: x["clip_refs"] = [still] + ([HANDREF] if x["hand"] else [])                   # Seedance reference mode
    x["clip_model"] = "omni (Flow first)" if x["product"] else "seedance-2-mini"
json.dump(SHOTS, open("shots.json", "w"), indent=1, ensure_ascii=False)
print(len(SHOTS), "shots;", sum(x["product"] for x in SHOTS), "product clips;", sum(not x["product"] for x in SHOTS), "no-product clips;",
      sum(not x["hand"] for x in SHOTS), "hand-free")
