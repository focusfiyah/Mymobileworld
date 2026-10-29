"""Builds shots.json for PRITECH V5-V9 (5 videos on Grace's own VO from https://www.tiktok.com/t/ZPLDRXhd4, 20.9 s).
Ralph 2026-10-29: "Use the VO from the link all 5 videos match visuals with VO however different visuals for each video."
Same 9 VO beats in every video; every shot idea is used once across V5-V9 (and none copies V1-V4 or Grace's posted cut).
Shared product/hand blocks copied from the approved V2-V4 prompts (ugc/pritech-15s/make_shots.py), written with prompt-master.
Run: python3 make_shots.py"""
import json

SIZE = "SIZE FIRST: a slim wand, as long as her hand from wrist crease to fingertip and only about two fingers wide; her fingers look big next to it, never the other way round."
SIZE_FREE = "SIZE FIRST: a slim wand, about as long as an adult hand and only about two fingers wide."
BRUSH = ("the real PRITECH face scrubber, BLACK: one SLIM matte black curved wand, about 15-16 cm long and only about two fingers wide, about 5 times as long as it is wide; "
         "its head is a forward-tilted oval paddle that flows straight out of the handle, barely wider than the handle (no neck, no round disc, no bulb), covered in short black silicone nubs in rings, "
         "three small moulded buttons on the front of the handle top to bottom (a vibration icon ((•)), a circle O, a °C sign), a short shiny silver chrome band at the bottom end, flush with the handle and exactly as wide as it. "
         "It never glows and has no lights. There is NO word, logo or print anywhere on the brush itself: its handle is plain matte black apart from the three moulded buttons (the grey word PRITECH exists only on the separate stand). No ® or ™.")
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch, the whole wrist visible, "
        "the hand enters from the frame edge and GRIPS the handle with the fingers wrapped around it.")
HANDS_NP = ("Grace's hands (medium-brown skin, short squared French-tip nails, the silver crown ring stack and small gold heart ring on one hand, blue thumb band, bare wrists, whole wrists)")
METALEND = ("The silver end is a short shiny chrome band flush with the handle, exactly as wide as the handle, ending in a flat round end face; it is NOT a disc, NOT a pedestal, NOT a blade, NOT wider than the handle.")
ANGLE = "Show the brush from a three-quarter side angle so its gentle curve and the forward tilt of the head show, exactly like the big photo in image 1."
NOFACE = "Only her cheek and jaw are in frame; her eyes and mouth are never in frame."
END = "Vertical 9:16 phone photo, {light}, true colours, realistic skin texture, no text, no captions, no watermark."
LIGHT = {"V5": "bright neutral daylight", "V6": "bright cool daylight, crisp and clean", "V7": "bright even vanity light, neutral white balance",
         "V8": "bright neutral hotel bathroom light", "V9": "bright soft window daylight, neutral white balance"}
NOHAND = "No hand, no fingers, no people."
CLIPEND = "No music, no voice, no captions, no on-screen text."
KEEP = "The hand keeps one grip and the brush never turns, flips or changes shape."
NOPRINT = "No word, logo or print appears on the brush handle at any time."
OMNI_FREE = ("Recreate image 1 exactly as the first frame: keep its room, light and framing exactly. {refs} keep this exact slim matte black shape, no lights, no glow, no added marks. ")
OMNI_HAND = ("Recreate image 1 exactly as the first frame: keep its room, light, framing and hand exactly. {refs} keep this exact slim matte black shape, no lights, no glow, no added marks. ")
SEED = "Recreate reference image 1 exactly as the first frame, then "
NOBRUSH = "No brush, no product, no face at any time."

# VO beats (Grace's VO, faster-whisper word times): cut windows used by cut.py
BEATS = [(0.00, 2.95), (2.95, 5.35), (5.35, 7.95), (7.95, 9.65), (9.65, 11.00), (11.00, 13.30), (13.30, 15.35), (15.35, 18.30), (18.30, 20.95)]
LINES = ["If you're not washing your face with a cleansing brush, what are you doing?",
         "Because using your hands leaves makeup and oil behind",
         "and towels just transfer bacteria right back into your skin.",
         "This one has soft silicone bristles,",
         "five vibration settings,",
         "and a warming feature that heats up to 104 degrees",
         "so you can get that little extra spa feel.",
         "And for something you do every single day, you might as well do it the right way.",
         "Go grab yours in the orange cart before you forget about this."]
R = {"SHEET": "image {n} is the product sheet:", "HEAD": "image {n} is the real black bristle head;", "BTN": "image {n} is the real three buttons ((•)) / O / °C, moulded black on black, matching it exactly;",
     "METAL": "image {n} is the real silver end, a short chrome band flush with the handle;", "LOGO": "image {n} is the real grey PRITECH print on the black stand, letter for letter;"}


def omni_refs(keys):
    """'Image 2 is ...; image 3 is the product sheet:' numbered in the order the clip_refs are sent (image 1 = the still)."""
    parts = [R[k].format(n=i + 2) for i, k in enumerate(keys)]
    t = " ".join(parts); return t[0].upper() + t[1:]


def s(id, beat, hand, product, room, still, motion, refs=(), btn=False, stand=False, face=False, metal=False):
    v = id[:2]
    if product:
        head = (OMNI_HAND if hand else OMNI_FREE).format(refs=omni_refs(refs))
        tail = (" " + KEEP if hand else " No hand, fingers or people appear at any time.") + f" {LIGHT[v].capitalize()}. " + NOPRINT + " " + CLIPEND
        clip = head + "Motion: " + motion + tail
    else:
        clip = (motion if motion.startswith(SEED) else SEED + motion) + f" {LIGHT[v].capitalize()}. " + CLIPEND
    return {"id": id, "video": v, "beat": beat, "t": BEATS[beat - 1], "line": LINES[beat - 1], "hand": hand, "product": product, "face": face, "room": room,
            "buttons": btn, "stand": stand, "metal": metal, "still": still + " " + END.format(light=LIGHT[v]), "clip": clip, "clip_refs": list(refs)}


SHOTS = [
 # ---------------- V5: fresh mint morning (rooms V5A mint tile + wood stool vanity + stone bowl basin, V5B mint mosaic niche + tub). Sage towel headband, white tee.
 s("V5S1", 1, True, True, "V5A",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " She holds it up close to the camera, the oval bristle face turned toward the lens, buttons on the side facing the lens edge; wet drops on the nubs. "
   "Mint tile wall, round mirror and a stone bowl basin on a wooden stool vanity soft behind (room reference).",
   "the hand moves the brush slowly closer to the lens, bristle face toward the camera the whole time.", refs=("HEAD", "SHEET")),
 s("V5S2", 2, True, False, "V5A",
   "Close-up over a stone bowl basin on a wooden stool vanity: " + HANDS_NP + " held palms up toward the camera, just lifted from washing, dripping water; beige foundation smudges and an oily shine are still on the fingertips and palms. "
   "Mint tile soft behind (room reference). No brush, no product, no face.",
   SEED + "the fingers curl slightly and drops of water run off the fingertips; the beige foundation smudges and oily shine stay on the fingertips. Only these two hands appear, whole wrists, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V5S3", 3, False, False, "V5B",
   "A crumpled, damp, used plain white face towel tossed over the rim of a white tub under mint mosaic niche shelves; grey-beige makeup marks on the towel. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera slowly pushes in toward the makeup marks on the crumpled towel; the towel does not move. No person, hand, brush or product appears at any time."),
 s("V5S4", 4, True, True, "V5A",
   SIZE + " Macro close-up: " + HAND + " She holds " + BRUSH + " bristle face up, and the thumb of her other hand rests on the soft black silicone nubs. Mint tile soft behind (room reference). " + ANGLE,
   "the thumb presses gently into the nubs and they bend softly under it, then spring back as the thumb lifts.", refs=("HEAD", "SHEET")),
 s("V5S5", 5, True, True, "V5A",
   SIZE + " Close-up from the side: " + HAND + " She holds " + BRUSH + " with the bristle head just touching the still water in a round stone bowl basin. Mint tile soft behind (room reference). " + ANGLE,
   "the brush is switched on and the water around the bristle head trembles and spreads small fast rings outward.", refs=("HEAD", "SHEET")),
 s("V5S6", 6, True, True, "V5A",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " and presses its silver chrome end against the inside of her other wrist, like testing the warmth. " + METALEND +
   " Both wrists whole, no bracelet. Mint tile and wooden vanity soft behind (room reference).",
   "the silver end rests on the inside of the wrist and slides a little along it.", refs=("METAL", "SHEET"), metal=True),
 s("V5S7", 7, False, False, "V5B",
   "A white tub filled with clear warm water under mint mosaic niche shelves holding neatly rolled thick white towels and a small green plant; soft steam over the water. Bright, calm, not dark. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera slowly pushes in toward the niche shelves while soft steam drifts up from the tub. No person, hand, brush or product appears at any time."),
 s("V5S8", 8, True, True, "V5A",
   SIZE + " Close three-quarter view: " + NOFACE + " Her cheek is covered in white cleanser foam; a sage green towel headband at the top edge, white tee at the shoulder. " + HAND + " She presses the bristle head of " + BRUSH +
   " The bristle head lies flat on her foamy cheek. Mint tile soft behind (room reference). " + ANGLE,
   "the hand moves the brush in small slow circles on the foamy cheek; the foam spreads a little. Her eyes and mouth never come into frame. Camera locked-off.", refs=("HEAD", "SHEET"), face=True),
 s("V5S9", 9, False, True, "V5A",
   SIZE_FREE + " One " + BRUSH + " It lies on the wooden stool vanity top right beside the round stone bowl basin, bristle head away from the camera, buttons up. Only one brush, no stand. Mint tile and round mirror soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow low push-in along the wooden top toward the brush; nothing moves.", refs=("BTN", "SHEET"), btn=True),

 # ---------------- V6: after the gym, oily skin (rooms V6A oxblood red tile + white tub, V6B teal-blue tile bath + wood mirror). Grey sports tank, hair in a ponytail.
 s("V6S1", 1, False, True, "V6B",
   SIZE_FREE + " One " + BRUSH + " It lies across the front edge of a white sink, water running from the tap behind it, a few drops on the nubs. Only one brush. Teal-blue tile soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow low dolly in across the counter toward the brush; the water keeps running, the brush never moves.", refs=("HEAD", "SHEET")),
 s("V6S2", 2, True, False, "V6B",
   "Close side view: " + NOFACE + " Her cheek has a shiny, oily post-workout sheen; a grey sports tank strap at the shoulder, a dark ponytail behind. " + HANDS_NP.replace("hands", "right hand") +
   " rubs two fingertips on the cheek. Teal-blue tile soft behind (room reference). No brush, no product.",
   SEED + "the fingertips rub the oily cheek, pull away and show a greasy shine on the fingertips. Only this one hand appears, whole wrist, the same rings as reference image 2. Her eyes and mouth never come into frame. No brush, no product at any time. Camera locked-off."),
 s("V6S3", 3, True, False, "V6A",
   "Close side view: " + NOFACE + " " + HANDS_NP.replace("hands", "right hand") + " presses a small plain grey gym towel against her cheek; a grey sports tank strap at the shoulder. Oxblood red tile soft behind (room reference). No brush, no product.",
   SEED + "the hand rubs the grey towel across the cheek and pulls it away. Only this one hand appears, whole wrist, the same rings as reference image 2. Her eyes and mouth never come into frame. No brush, no product at any time. Camera locked-off."),
 s("V6S4", 4, True, True, "V6B",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " and rests its bristle head on the back of her other hand (whole wrist, blue thumb band visible). Teal-blue tile soft behind (room reference). " + ANGLE,
   "the bristle head sweeps slowly across the back of the other hand and the soft nubs bend as they drag over the skin.", refs=("HEAD", "SHEET")),
 s("V6S5", 5, True, True, "V6B",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " and presses the bristle head into the open palm of her other hand (whole wrist). Teal-blue tile soft behind (room reference). " + ANGLE,
   "the brush is switched on and the skin of the open palm jiggles fast under the vibrating nubs.", refs=("HEAD", "SHEET")),
 s("V6S6", 6, True, True, "V6A",
   SIZE + " Close side view of the side of her neck below the jaw: everything above her jawline is out of frame (no lips, no mouth, no eyes). A grey sports tank strap at the shoulder. " + HAND + " She holds " + BRUSH +
   " diagonally with the bristle head out of the bottom edge of the frame, and the silver chrome end rests on the side of her neck. " + METALEND + " The bristles never touch her skin. Oxblood red tile soft behind (room reference).",
   "the silver end glides slowly down the side of the neck toward the collarbone.", refs=("METAL", "SHEET"), face=True, metal=True),
 s("V6S7", 7, False, False, "V6A",
   "A bundle of fresh green eucalyptus hanging from a chrome shower head above a white tub with oxblood red tile walls; a folded white towel on the tub ledge. Bright, not dark. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera slowly pushes in toward the eucalyptus bundle, which sways very gently. No person, hand, brush or product appears at any time."),
 s("V6S8", 8, True, True, "V6B",
   SIZE + " " + HAND + " Her hand lowers " + BRUSH + " into its matte black stand (grey PRITECH on the stand front) on a white sink counter, the brush just above the stand, wet. Teal-blue tile soft behind (room reference). " + ANGLE,
   "the hand slowly lowers the brush straight down until it sits in the stand, fingers still around the handle; the stand stays still.", refs=("LOGO", "BTN", "SHEET"), btn=True, stand=True),
 s("V6S9", 9, False, True, "V6B",
   SIZE_FREE + " One " + BRUSH + " It sits in the open side pocket of a plain grey gym bag (no logo, no text) on a white counter, bristle head sticking up. Only one brush. Teal-blue tile soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow push-in toward the brush in the bag pocket; nothing moves.", refs=("HEAD", "SHEET")),

 # ---------------- V7: makeup removal at the vanity (rooms V7A pink terracotta tile + leaf print + white counter, V7B bulb makeup vanity). White satin robe.
 s("V7S1", 1, True, True, "V7B",
   SIZE + " " + HAND + " Her hand picks up " + BRUSH + " from a white makeup vanity table in front of a bulb-framed mirror, lifting it toward the camera. A few plain makeup brushes in a cup soft behind (no brand, no text) (room reference). " + ANGLE,
   "the hand lifts the brush up off the table and toward the camera.", refs=("HEAD", "SHEET")),
 s("V7S2", 2, True, False, "V7B",
   "Close side view: " + NOFACE + " Her cheek still has a light layer of beige foundation after a quick hand wash; a white satin robe collar at the shoulder. " + HANDS_NP.replace("hands", "right hand") +
   " runs one fingertip across the cheek. Bulb mirror soft behind (room reference). No brush, no product.",
   SEED + "the fingertip swipes across the cheek and turns toward the camera, showing a beige foundation smudge on it. Only this one hand appears, whole wrist, the same rings as reference image 2. Her eyes and mouth never come into frame. No brush, no product at any time. Camera locked-off."),
 s("V7S3", 3, True, False, "V7A",
   "A plain white face towel with beige makeup marks hanging from a chrome hook on a pink terracotta tile wall; " + HANDS_NP.replace("hands", "right hand") + " reaches in from the right edge and grips the towel. No brush, no product, no face (room reference).",
   SEED + "the hand pulls the towel down off the hook and out of the bottom of the frame, ready to reuse it. Only this one hand appears, whole wrist, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V7S4", 4, False, True, "V7A",
   SIZE_FREE + " One " + BRUSH + " It lies on a soft fluffy white towel on a white counter, the bristle face angled up toward the camera. Only one brush. Pink terracotta tile and a green leaf print soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow short arc to the right around the bristle face; the brush never moves.", refs=("HEAD", "SHEET")),
 s("V7S5", 5, False, True, "V7B",
   SIZE_FREE + " One " + BRUSH + " It lies on a small round mirrored vanity tray, a few water drops on the tray around the bristle head. Only one brush. Bulb mirror soft behind (room reference). " + NOHAND + " " + ANGLE,
   "the brush is switched on and buzzes in place, the water drops on the tray around the head jump and shiver; the brush does not slide.", refs=("HEAD", "SHEET")),
 s("V7S6", 6, True, True, "V7A",
   SIZE + " Close side view: " + HAND + " She holds " + BRUSH + " upright, buttons facing the camera, her thumb on the bottom °C button; the silver chrome end shows below her hand. " + METALEND + " Pink terracotta tile soft behind (room reference). " + ANGLE,
   "the thumb presses the bottom °C button once and lifts off.", refs=("BTN", "METAL", "SHEET"), btn=True, metal=True),
 s("V7S7", 7, True, False, "V7A",
   "Body close-up from the chest down to the waist, no face: " + HANDS_NP + " tie the belt of a white satin robe at the waist. Pink terracotta tile soft behind (room reference). No brush, no product.",
   SEED + "the hands pull the robe belt into a loose bow. Only these two hands appear, whole wrists, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V7S8", 8, True, True, "V7A",
   SIZE + " Close-up over a white counter: " + HAND + " She holds " + BRUSH + " bristle head down onto a small folded white cloth, patting it dry. Pink terracotta tile soft behind (room reference). " + ANGLE,
   "the hand pats the bristle head gently on the cloth twice.", refs=("HEAD", "SHEET")),
 s("V7S9", 9, False, True, "V7B",
   SIZE_FREE + " One " + BRUSH + " in its matte black stand (grey PRITECH on the stand front) on a white makeup vanity table in front of a bulb-framed mirror. Only one brush. " + NOHAND + " (room reference) " + ANGLE,
   "only the camera moves, a slow push-in toward the brush in its stand; nothing moves.", refs=("LOGO", "BTN", "SHEET"), btn=True, stand=True),

 # ---------------- V8: travel / hotel (rooms V8A navy tile hotel bath + white basin, V8B wood-plank wall + freestanding tub). White waffle hotel robe.
 s("V8S1", 1, True, True, "V8A",
   SIZE + " " + HAND + " Her hand pulls " + BRUSH + " half out of an open plain grey zip toiletry pouch (no logo, no text) on a white hotel bathroom counter. Navy tile and a white basin soft behind (room reference). " + ANGLE,
   "the hand pulls the brush the rest of the way out of the pouch and holds it up toward the camera.", refs=("HEAD", "SHEET")),
 s("V8S2", 2, True, False, "V8A",
   "Close-up over a white basin: " + HANDS_NP + " lather a plain white bar of hotel soap (no logo); beige foundation streaks still on the fingertips. Navy tile soft behind (room reference). No brush, no product, no face.",
   SEED + "the hands rub the soap into a thin lather; the beige streaks stay on the fingertips. Only these two hands appear, whole wrists, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V8S3", 3, False, False, "V8A",
   "A damp, used, limp white hand towel hanging on a chrome hotel towel bar on a navy tile wall, faint beige makeup marks on it. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera tilts slowly down the hanging towel toward its marked corner; the towel does not move. No person, hand, brush or product appears at any time."),
 s("V8S4", 4, True, True, "V8A",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " with the bristle head just lifted out of a white basin of water, water dripping off the nubs. Navy tile soft behind (room reference). " + ANGLE,
   "the hand lifts the bristle head a little higher and the water runs off the soft nubs in drips.", refs=("HEAD", "SHEET")),
 s("V8S5", 5, True, True, "V8A",
   SIZE + " Close-up from the front: " + HAND + " She holds " + BRUSH + " upright over a white basin, buttons facing the camera, her thumb on the top vibration button ((•)); wet nubs. Navy tile soft behind (room reference). " + ANGLE,
   "the thumb presses the top ((•)) button and fine water droplets spray off the vibrating nubs.", refs=("BTN", "HEAD", "SHEET"), btn=True),
 s("V8S6", 6, False, True, "V8B",
   SIZE_FREE + " One " + BRUSH + " It lies on the wide rim of a white freestanding tub, the silver chrome end nearest the camera. " + METALEND + " Only one brush. Wood-plank wall soft behind (room reference). " + NOHAND,
   "only the camera moves, a slow slide along the handle toward the silver chrome end; nothing moves.", refs=("METAL", "SHEET"), metal=True),
 s("V8S7", 7, False, False, "V8B",
   "A folded white waffle robe and a pair of white hotel slippers on a small wooden stool beside a white freestanding tub, wood-plank wall. Bright and calm, not dark. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera slowly pushes in toward the robe and slippers on the stool. No person, hand, brush or product appears at any time."),
 s("V8S8", 8, True, True, "V8A",
   SIZE + " Close-up on a white hotel counter: " + HAND + " Her hand lowers " + BRUSH + " into an open plain grey zip toiletry pouch (no logo, no text), the brush half inside. Navy tile soft behind (room reference). " + ANGLE,
   "the hand slowly slides the brush down into the open pouch, fingers still around the handle; the pouch stays open.", refs=("HEAD", "SHEET")),
 s("V8S9", 9, False, True, "V8A",
   SIZE_FREE + " One " + BRUSH + " in its matte black stand (grey PRITECH on the stand front) on a white hotel bathroom counter next to a plain white key card (no text). Only one brush. Navy tile soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow push-in toward the brush in its stand; nothing moves.", refs=("LOGO", "BTN", "SHEET"), btn=True, stand=True),

 # ---------------- V9: self-care Sunday (rooms V9A green tile + white square basin + pink floor, V9B wood cabin bath + big window). Cream knit sweater, hair in a claw clip.
 s("V9S1", 1, False, True, "V9A",
   SIZE_FREE + " Top-down view: one " + BRUSH + " It lies on the flat rim of a white square basin, a few water drops on the nubs. Only one brush. Green tile at the top edge (room reference). " + NOHAND,
   "only the camera moves, a slow descent straight down toward the brush; nothing moves.", refs=("HEAD", "SHEET")),
 s("V9S2", 2, True, False, "V9A",
   "Macro close-up in window light: " + HANDS_NP.replace("hands", "right hand") + " held up, thumb rubbing across the fingertips; the finger pads show beige foundation and an oily shine. Green tile soft behind (room reference). No brush, no product, no face.",
   SEED + "the thumb slowly rubs across the fingertips and the oily shine catches the light. Only this one hand appears, whole wrist, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V9S3", 3, True, False, "V9A",
   "Close-up over a white square basin: " + HANDS_NP + " grip a damp plain white face cloth with faint beige makeup marks. Green tile soft behind (room reference). No brush, no product, no face.",
   SEED + "the hands twist and wring out the face cloth and slightly beige water drips into the basin. Only these two hands appear, whole wrists, the same rings as reference image 2. " + NOBRUSH + " Camera locked-off."),
 s("V9S4", 4, False, True, "V9B",
   SIZE_FREE + " Macro close-up: one " + BRUSH + " It lies on a wooden bath caddy across a white tub by a big window, the bristle face up and nearest the camera. Only one brush. Wood walls and window light soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow macro slide across the soft black nubs; nothing moves.", refs=("HEAD", "SHEET")),
 s("V9S5", 5, True, True, "V9A",
   SIZE + " Close-up: " + HAND + " She holds " + BRUSH + " and presses the bristle head into a small white dish of white cleanser foam on the basin rim. Green tile soft behind (room reference). " + ANGLE,
   "the brush is switched on and the foam in the dish jiggles and ripples fast around the bristle head.", refs=("HEAD", "SHEET")),
 s("V9S6", 6, True, True, "V9B",
   SIZE + " Close side view: " + NOFACE + " Her cheek is rinsed clean and slightly damp; a cream knit sweater at the shoulder, hair up in a claw clip. " + HAND + " She holds " + BRUSH +
   " diagonally: the bristle head is out of the bottom edge of the frame, and the silver chrome end rests flat on her jaw near the ear. " + METALEND + " The bristles never touch her face. Window light and wood wall soft behind (room reference).",
   "the hand glides the silver end slowly along the jaw toward the ear. Her eyes and mouth never come into frame.", refs=("METAL", "SHEET"), face=True, metal=True),
 s("V9S7", 7, False, False, "V9B",
   "A folded cream knit blanket and a closed book with a plain cover (no text) on a wooden bench under a big bright window in a wooden cabin bathroom, a white tub soft behind. Bright, cozy, not dark. No person, no hand, no brush, no product (room reference).",
   SEED + "the camera makes a slow sideways dolly along the bench past the blanket and book. No person, hand, brush or product appears at any time."),
 s("V9S8", 8, True, True, "V9A",
   SIZE + " Close-up from the front: " + HAND + " She holds " + BRUSH + " upright, buttons facing the camera, her thumb on the middle circle O button; a cream knit sleeve at the wrist edge. Green tile soft behind (room reference). " + ANGLE,
   "the thumb presses the O button once and the hand lifts the brush up and out of the top of the frame.", refs=("BTN", "SHEET"), btn=True),
 s("V9S9", 9, False, True, "V9B",
   SIZE_FREE + " One " + BRUSH + " It lies on a wide wooden windowsill in bright morning light, bristle head toward the window, buttons up. Only one brush. Wood wall soft behind (room reference). " + NOHAND + " " + ANGLE,
   "only the camera moves, a slow push-in toward the brush on the sill; nothing moves.", refs=("BTN", "SHEET"), btn=True),
]

P = {"METAL": "refs/closeup_metal_end.png", "SHEET": "refs/product_sheet_v2.png", "HEAD": "refs/closeup_head.png", "BTN": "refs/closeup_buttons.png", "LOGO": "refs/closeup_stand_logo.png"}
HANDREF = "../../grace/ref/hand-sheets/without_bracelet.jpg"
for x in SHOTS:   # the exact text and images sent, so prompt_check reads what is paid for
    r, names = [], []
    def add(path, what): r.append(path); names.append(f"image {len(r)} = {what}")
    if x["product"]:
        add(P["SHEET"], "the product sheet, real photos only: the big left photo is the real black brush, copy its slim shape and proportions exactly")
        add(P["HEAD"], "a real close-up of the black bristle head")
        if x["buttons"]: add(P["BTN"], "a real close-up of the three moulded buttons, black on black: ((•)) on top, O in the middle, °C at the bottom")
        if x["stand"]: add(P["LOGO"], "a real close-up of the grey 'PRITECH' print on the black stand")
        if x["metal"]: add(P["METAL"], "a real photo of the black brush's silver end: a short chrome band flush with the handle, same width, flat round end face")
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
for v in "56789":
    vs = [x for x in SHOTS if x["video"] == "V" + v]
    print(f"V{v}: {len(vs)} shots, {sum(not x['hand'] for x in vs)} hand-free, {sum(x['product'] for x in vs)} product")
