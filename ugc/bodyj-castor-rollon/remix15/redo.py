"""Redo r3 (2026-10-21, REDO_PLAN.md): 4 new shots for lines whose picture didn't match the words.
  python3 redo.py stills [R1 ...]    nano-banana-pro (Gemini 3 Pro Image) on Kie, $0.09 each -> redo/stills/R*.png
  python3 redo.py clip R3            Seedance 2.0 Mini, 5 s, $0.205 (hand shot); R1 R2 R4 go to Kling (MCP)"""
import sys
from pathlib import Path
H = Path(__file__).resolve().parent; P = H.parent
sys.path.insert(0, str(P)); sys.path.insert(0, str(H.parents[2] / "grace"))
import os; os.chdir(P)          # kie.py logs + upload cache live in the parent job
import kie
from gate import require
kie._gate = lambda: require(H)  # this job's own script gate (remix15/checklist.json)
SHEET, FRONT = "refs/ralph_sheet_bottle.jpg", "refs/bottle_front.png"
BATH, BED = "stills/S8.png", "stills/S9.png"
PROD = ("The BodyJ4You castor oil roll-on: a short squat amber-brown glass bottle, white plastic collar, a pink rose quartz "
        "roller ball on top, white label with a plum band, plum serif 'CASTOR OIL', green USDA ORGANIC seal. It must match the "
        "product reference sheet exactly (the big front view is the real label); the label faces the camera wherever it is visible.")
LOOK = "Bright, clean, neutral daylight, true colours, no yellow or golden tint, no dark or moody look. No text, no logos other than the product label."
S = {
 "R1": {"refs": [SHEET, FRONT, BATH], "p": f"Close shot of the castor oil roll-on standing on the white marble counter of the sage-green tiled bathroom from the last reference image, soft morning sun from the window. One fat clear golden drop of castor oil sits on top of the rose quartz roller ball and catches the light like liquid gold. No hands. {PROD}"},
 "R2": {"refs": [SHEET, FRONT, BED], "p": f"A small round mirrored vanity tray on the wooden nightstand of the bedroom from the last reference image. On the tray, left: a pretty faceted glass perfume bottle with pale pink perfume and a round glass cap, no brand, no writing. Right, a little apart: the castor oil roll-on. No hands. {PROD}"},
 "R3": {"refs": ["stills/S5.png"], "p": "Seen from above and behind, no face. EXACTLY TWO HANDS in the whole frame, both hers: an older Black grandmother's hands (brown skin with fine wrinkles, short natural unpainted nails, a thin gold wedding band) part her short grey coily hair and work plain golden castor oil into the scalp at the part with her fingertips. In her other hand, an old unbranded clear glass bottle of golden oil with no label. Lavender cardigan sleeve at the wrist. Soft bright bedroom light, same framing and light as the reference image, but grey hair and older hands. Her right hand works the oil in at the part; her left hand holds the bottle low in the frame. No third hand, no hand on top of the head. Whole wrists, both coming from the bottom edge of the frame."},
 "R4": {"refs": [SHEET, FRONT, BATH], "p": f"A white bathroom shelf in the sage-green tiled bathroom from the last reference image. Left: a big old messy unbranded plastic bottle of castor oil, thick golden oil dripped down its side and a sticky oily ring under it on the shelf, no label text. Right, a little apart: the clean castor oil roll-on. No hands. {PROD}"},
}

ROOM = {1: "redo/rooms/room1_spa_tub.jpg", 2: "redo/rooms/room2_grey_marble.jpg", 3: "redo/rooms/room3_cream_double.jpg", 4: "redo/rooms/room4_navy_vanity.jpg"}
HAND = str(H / "redo/hand_ref.png"); BOX = "refs/ralph_sheet_box.jpg"
BRIGHT = ("The room from the room reference image (Ralph's pick for this video), shown in bright natural daylight from the window, "
          "warm lamps and candles off, clean neutral white balance, airy and light.")
PERSON = ("Her hands: medium-brown skin, short natural nude nails, no rings, a dusty mauve cotton t-shirt sleeve, exactly like the hand in the hand "
          "reference image. Only her hands, arm or the named body part are in frame; never her mouth or full face.")
def shot(room, p, v, hand=True, product=True, box=False):
    refs = ([SHEET, FRONT] if product else []) + ([BOX] if box else []) + ([HAND] if hand else []) + [str(H / ROOM[room])]
    return {"refs": refs, "p": p + " " + BRIGHT + (" " + PERSON if hand else " No hands.") + (" " + PROD if product else "") +
            (" Next to it, its real retail box exactly as in the box reference image." if box else ""), "v": v, "product": product}
V1 = {
 "V1a": shot(1, "Close shot: the castor oil roll-on stands on the round wooden stool beside the freestanding white bathtub, a plant behind it. The roll-on is complete and unchanged: amber glass bottle, white collar, pink rose quartz ball on top. Beside it, a small shallow glass dish holds a pool of clear golden castor oil that glows in the sunlight like liquid gold.", "the camera slowly pushes in toward the roll-on and the glowing golden oil in the dish; sunlight shimmers on the oil.", hand=False),
 "V1b": shot(1, "Close shot over the rim of the white freestanding tub: her cupped hands hold thick golden castor oil that runs between her fingers and drips in long sticky strings onto the tub rim. An old unbranded clear glass bottle of oil lies tipped on the rim, no label.", "the thick oil keeps oozing through her fingers and dripping in slow sticky strings onto the tub rim; her fingers spread a little, showing the mess.", product=False),
 "V1c": shot(1, "Her hand grips the castor oil roll-on, lifting it off the wooden wall shelf with rolled towels, label facing camera.", "her hand lifts the roll-on toward the camera and holds it up, label facing camera, steady and proud."),
 "V1d": shot(1, "Close shot: her right hand grips the castor oil roll-on and presses the rose quartz ball on the back of her left hand, resting on the tub rim; her fingertips are clean and dry.", "she rolls the rose quartz ball across the back of her left hand in one smooth stroke, leaving a thin shiny line; both hands stay clean and dry."),
 "V1e": shot(1, "Extreme close shot of one eyebrow and closed eye, from the brow up to the hairline only (no mouth, no nose tip): her hand holds the castor oil roll-on and presses the rose quartz ball at the inner end of the eyebrow.", "she rolls the ball slowly along the eyebrow from the inner end to the tail; the eye stays closed."),
 "V1f": shot(1, "Close shot: her left hand rests flat on a folded white towel on the tub rim; her right hand grips the castor oil roll-on and presses the rose quartz ball on the cuticle of the index finger.", "she rolls the ball over each cuticle, index to ring finger, one after another."),
 "V1g": shot(1, "Close shot: her left arm bent, elbow toward the camera; her right hand grips the castor oil roll-on and presses the rose quartz ball on the elbow.", "she rolls the ball in small circles over the elbow skin, which turns softly shiny."),
 "V1h": shot(1, "Close shot: long dark hair over her shoulder against the mauve t-shirt; her right hand grips the castor oil roll-on and presses the rose quartz ball on the hair ends.", "she rolls the ball down the hair ends; the ends turn smooth and glossy in the light."),
 "V1i": shot(1, "The castor oil roll-on standing next to its retail box on the round wooden stool beside the freestanding white bathtub, a small plant and a folded towel.", "the camera slowly pushes in on the roll-on and its box.", hand=False, box=True),
}
S.update(V1)

V234 = {
 # V2: room 2 (grey marble, wood vanity, white vessel sink)
 "V2a": shot(2, "Close shot over the grey marble vanity counter with the white vessel sink and wood-slat wall: her hand tips an old unbranded clear glass bottle and pours very thick golden castor oil onto a metal spoon held in her other hand; the oil overflows the spoon and drips onto the marble.", "the thick oil keeps oozing slowly over the spoon edge and drips in heavy sticky strings onto the marble counter.", product=False),
 "V2b": shot(2, "The castor oil roll-on standing alone on the grey marble vanity counter next to the white vessel sink, warm sunlight across the counter making the amber glass glow like liquid gold.", "the camera slowly arcs a little around the roll-on; light glints on the amber glass and the rose quartz ball.", hand=False),
 "V2c": shot(2, "Her hand grips the castor oil roll-on just above the grey marble counter beside the white vessel sink, label facing camera.", "her hand lifts the roll-on up toward the camera with a little flourish and holds it there, label facing camera."),
 "V2d": shot(2, "Close shot: her left wrist turned up, inner wrist facing camera, above the grey marble counter; her right hand grips the castor oil roll-on and presses the rose quartz ball on one spot of the inner wrist.", "she rolls the ball back and forth on that one small spot of the inner wrist, precise and neat."),
 "V2e": shot(2, "Extreme close shot of one eyebrow and the hairline above it, eye closed, only from the eyebrow up (no mouth, no nose): her hand holds the castor oil roll-on with the rose quartz ball on the eyebrow.", "she rolls the ball along the eyebrow, then up past the brow into the hairline and the roots of her hair."),
 "V2f": shot(2, "Close shot: her left hand resting on a grey hand towel on the marble counter; her right hand grips the castor oil roll-on and presses the rose quartz ball on the cuticle of the middle finger.", "she rolls the ball over the cuticles, then up across the dry knuckles on the back of the hand, leaving a soft sheen."),
 "V2h": shot(2, "The castor oil roll-on standing next to its retail box on the grey marble vanity counter beside the white vessel sink and a small plant.", "the camera slowly pushes in on the roll-on and its box.", hand=False, box=True),
 # V3: room 3 (cream double vanity, black fixtures)
 "V3a": shot(3, "On the white quartz double vanity counter between the two sinks: a pretty faceted glass perfume bottle with pale pink perfume and a round glass cap (no brand, no writing) on a small mirrored tray, and a little apart the castor oil roll-on.", "the camera slowly slides from the perfume bottle across to the castor oil roll-on and settles on it.", hand=False),
 "V3c": shot(3, "Close shot: her left hand flat on the white quartz vanity counter; her right hand grips the castor oil roll-on and presses the rose quartz ball on the nail of the index finger.", "she rolls the ball over each nail and cuticle, then across the skin on the back of her hand."),
 "V3d": shot(3, "Close shot on the white quartz double vanity counter with a black faucet and white cabinets with black handles: both her hands hold the castor oil roll-on's retail box, the top flap open.", "she pulls the roll-on out of the open box with one hand and lifts it up toward the camera, label facing camera, excited.", box=True),
 "V3e": shot(3, "Close shot over the white quartz double vanity with the black faucet: her right hand grips the castor oil roll-on and presses the rose quartz ball on the inside of her left forearm, held up and turned out; the fingertips of both hands are clean and dry.", "she rolls the ball in one smooth line up the inner forearm; her other hand opens its fingers to show they are clean and dry."),
 "V3f": shot(3, "Close shot of her neck and collarbone above the mauve t-shirt neckline, from the chin down only (no mouth): her hand grips the castor oil roll-on and presses the rose quartz ball on the collarbone.", "she rolls the ball along the collarbone and up the side of the neck."),
 "V3g": shot(3, "The castor oil roll-on standing next to its retail box on the white quartz double vanity counter by the black faucet and a small vase of greenery.", "the camera slowly pushes in on the roll-on and its box.", hand=False, box=True),
 # V4: room 4 (navy vanity, wooden shelves, glass shower)
 "V4a": shot(4, "The wooden wall shelf above the toilet in this bathroom: on the left a big old greasy unbranded plastic bottle of castor oil, its outside smeared and sticky with thick golden oil, a thick oil drip running down its side onto the shelf and a wide greasy oily ring and puddle under it, a used oily paper towel beside it (no label text); on the right, a little apart, the clean castor oil roll-on.", "the camera slowly slides right along the shelf from the messy bottle and stops on the castor oil roll-on.", hand=False),
 "V4b": shot(4, "Close shot: the castor oil roll-on standing on the white quartz top of the navy blue vanity, life-size and in scale with the counter and the faucet beside it, the label and the green USDA ORGANIC seal sharp. It sits naturally on the counter with a soft real shadow.", "the camera slowly pushes in toward the label until the USDA ORGANIC seal and the words CASTOR OIL fill the frame.", hand=False),
 "V4c": shot(4, "Close shot above the navy vanity: her left forearm held out; her right hand grips the castor oil roll-on and presses the rose quartz ball on the top of the forearm.", "she glides the ball in one long easy stroke along the forearm, quick and effortless."),
 "V4d1": shot(4, "Extreme close shot of one eyebrow, eye closed, from the eyebrow up only (no mouth, no nose): her hand holds the castor oil roll-on with the rose quartz ball at the inner end of the brow. Navy and white bathroom behind.", "she rolls the ball along the eyebrow to the tail."),
 "V4d2": shot(4, "Close shot: her left hand resting on the white quartz top of the navy vanity; her right hand grips the castor oil roll-on and presses the rose quartz ball on a dry cuticle of the thumb.", "she rolls the ball over the thumb and index finger cuticles."),
 "V4d3": shot(4, "Close shot: her bent left elbow with rough dry skin toward the camera, the navy vanity behind; her right hand grips the castor oil roll-on and presses the rose quartz ball on the elbow.", "she rolls the ball in small circles over the rough elbow, which turns soft and shiny."),
 "V4d4": shot(4, "Close shot: the ends of long dark hair held in her left hand in front of the striped towel by the glass shower; her right hand grips the castor oil roll-on and presses the rose quartz ball on the hair ends.", "she rolls the ball down the hair ends, which turn smooth and glossy."),
 "V4e": shot(4, "Close shot above the clean white quartz top of the navy vanity: her hand holds the capped castor oil roll-on, her other hand open next to it, palm and fingertips completely clean and dry; the counter is spotless.", "she turns her open hand slowly to show the clean dry fingertips and sets the roll-on down on the spotless counter."),
 "V4f": shot(4, "The castor oil roll-on standing next to its retail box on the white quartz top of the navy blue vanity, small plant and wooden shelf behind.", "the camera slowly pushes in on the roll-on and its box.", hand=False, box=True),
}
S.update(V234)

# Round 4 (2026-10-21, Ralph: "Shouldn't grandma be holding the one with the roller", "The size of the roller looks pretty big",
# "use your prompt master skill"): prompts rebuilt with the hard constraints FIRST (size, identity, hands), one action, NEVER list.
SIZE = ("PRODUCT SIZE AND SHAPE (MUST): the roll-on is a SMALL, SQUAT 50 ml (1.7 fl oz) round bottle, only about twice as tall as it is wide "
        "(about 9 cm tall with the ball, 4 cm wide), exactly the proportions of the product reference sheet, never a slim tube or a tall vial; "
        "it is about as tall as her index finger. The label wraps horizontally with CASTOR OIL reading across, exactly like the reference. In a hand, her fingers wrap around it and hide most of the label height; it is NEVER "
        "bigger than her hand and NEVER as tall as a faucet, a vase or a soap pump. Keep it in true scale with the counter, sink and faucet.")
BOXSIZE = "The retail box is small too: 4 x 4 x 11 cm, only a little taller than the bottle."
NEVER = ("NEVER: an oversized or giant bottle, a second roll-on, a roll-on still inside the box, extra hands or fingers, text, "
         "captions, watermarks, a dark or yellow look, a visible mouth.")
def pm(room, shot_txt, motion, hand=True, product=True, box=False, person=None):
    must = ((SIZE + " " + PROD + " ") if product else "") + ((BOXSIZE + " ") if box else "") + \
           (person or PERSON if hand else "No hands. ") + " " + BRIGHT
    d = shot(room, "", motion, hand=hand, product=product, box=box)
    d["p"] = must + " SHOT: " + shot_txt + (" Next to it, its real retail box exactly as in the box reference image, closed and standing." if box else "") + " " + NEVER
    d["v"] = motion + " The bottle keeps exactly the same small size in every frame; it never grows as it comes toward the camera."
    return d
GRANNY = ("Her hands: an older Black grandmother's hands, brown skin with fine wrinkles, short natural unpainted nails, a thin gold "
          "wedding band, lavender cardigan sleeves. Only her two hands and the top of her head are in frame, never her face.")
R4 = {
 "R3": pm(3, "Seen from above and behind: her short grey coily hair with a neat part. Her left fingertips gently hold the hair open at the part; "
          "her right hand grips the small castor oil roll-on, ball down, and presses the pink rose quartz ball on the scalp at the part. "
          "Exactly two hands in the frame, both hers, coming from the bottom edge. Plain bright wall behind.",
          "she rolls the pink ball slowly along the part from front to back; a thin shiny line of oil follows the ball; her left hand stays still.",
          person=GRANNY),
 "V1c": pm(1, "Medium close shot by the white freestanding tub: her hand grips the small castor oil roll-on at chest height, label facing camera, "
           "the bottle fits in her fist with only the white collar and pink ball above her thumb.", "she lifts the roll-on a little and holds it up, proud, label facing camera."),
 "V1e": pm(1, "Extreme close shot from the eyebrow up only (frame bottom at the bridge of the nose, no mouth, no nose tip): her fingertips hold the small "
           "castor oil roll-on, mostly hidden in her fingers, the pink ball pressed on the inner end of one eyebrow; eye closed.", "she rolls the ball slowly along the eyebrow to the tail."),
 "V2c": pm(2, "Medium shot at the grey marble vanity beside the white vessel sink: her hand grips the small castor oil roll-on just above the counter, label facing camera, "
           "the bottle shorter than the sink's height and tiny next to the black faucet.", "she lifts the roll-on up to chest height and holds it there, label facing camera."),
 "V2e": pm(2, "Extreme close shot from the eyebrow up only (frame bottom at the bridge of the nose, no mouth): her fingertips hold the small castor oil roll-on, mostly hidden "
           "in her fingers, the pink ball pressed on one eyebrow; the hairline above; eye closed.", "she rolls the ball along the eyebrow and then up into the hairline at the roots."),
 "V2h": pm(2, "Wide-ish shot of the grey marble vanity counter beside the white vessel sink and a small plant: the small castor oil roll-on standing upright, its height about a third of the sink's height.",
           "the camera slowly pushes in a little on the roll-on and its box.", hand=False, box=True),
 "V3f": pm(3, "Close shot of her neck and collarbone above the mauve t-shirt neckline, frame top at the jaw line (no mouth): her fingers wrap around the small castor oil roll-on, "
           "the pink ball pressed on the collarbone.", "she rolls the ball along the collarbone and up the side of the neck."),
 "V3g": pm(3, "Shot of the white quartz double vanity counter by a black faucet and a small vase of greenery: the small castor oil roll-on standing upright, much shorter than the faucet.",
           "the camera slowly pushes in a little on the roll-on and its box.", hand=False, box=True),
 "V4a": pm(4, "The wooden wall shelf above the toilet: on the left a big old greasy unbranded 500 ml plastic bottle of castor oil, its outside smeared with thick golden oil, a drip running down "
           "its side and a greasy puddle under it, a used oily paper towel beside it (no label text); on the right, a little apart, the small clean castor oil roll-on, about a third of the big bottle's height.",
           "the camera slowly slides right along the shelf from the greasy bottle and stops on the small roll-on.", hand=False),
 "V4b": pm(4, "Close shot on the white quartz top of the navy vanity: the small castor oil roll-on standing upright beside the chrome faucet base, the label and green USDA ORGANIC seal sharp, a soft real shadow.",
           "the camera slowly pushes in toward the label until the USDA ORGANIC seal is large in frame.", hand=False),
 "V4f": pm(4, "Shot of the white quartz top of the navy vanity, small plant and wooden shelf behind: the small castor oil roll-on standing upright, its height about a third of the faucet's height.",
           "the camera slowly pushes in a little on the roll-on and its box.", hand=False, box=True),
}
S.update(R4)
S["R3"]["refs"] = [SHEET, FRONT, str(H / "redo/stills/R3_v2_glassbottle.png")]   # grandma look from the approved R3 still, no Grace hand ref
S["R3"]["p"] = S["R3"]["p"].replace("The room from the room reference image", "The grandmother, cardigan and light from the last reference image (but she now holds the roll-on, not a glass bottle)")

def still(sid):
    s = S[sid]
    prompt = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + s["p"] + " " + LOOK
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in s["refs"]], "aspect_ratio": "9:16", "resolution": "1K"}})
    if url: kie.fetch(url, str(H / f"redo/stills/{sid}.png")); print("still", sid, "ok", flush=True)
HANDRULE = ("The hands keep the same skin tone and nails for the whole clip, five fingers each, whole wrists, they grip what they hold. "
            "No new hands appear. Smooth, natural, real-time motion; the camera stays steady with a slight handheld drift. Bright neutral light, no text.")
PRODRULE = (" The roll-on bottle never changes shape; its front label must match reference image 2 letter for letter "
            "('Body4You', '100% Premium Quality', 'CASTOR OIL', the green USDA ORGANIC seal); reference image 3 shows the bottle from every side.")
def clip(sid, dur=4):
    s = S[sid]; first = kie.upload(str(H / f"redo/stills/{sid}.png"))
    refs = [first] + ([kie.upload(FRONT), kie.upload(SHEET)] if s.get("product", True) else [])
    prompt = "Recreate reference image 1 exactly (same room, framing, light and objects) as the first frame, then: " + s["v"] + " " + HANDRULE + (PRODRULE if s.get("product", True) else "")
    url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": prompt, "reference_image_urls": refs, "generate_audio": False,
                        "resolution": "720p", "aspect_ratio": "9:16", "duration": dur}})
    if url: (H / "redo/clips").mkdir(exist_ok=True); kie.fetch(url, str(H / f"redo/clips/{sid}.mp4")); print("clip", sid, "ok", flush=True)
S["R3"].update({"product": False, "v": "her right hand's fingertips slowly massage the golden oil into the scalp along the part in small circles, the oil glistening on the grey hair; her left hand stays low, holding the old glass bottle steady."})
if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for sid in sys.argv[2:] or list(S): still(sid)
    elif sys.argv[1] == "clip":
        for sid in sys.argv[2:]: clip(sid)
