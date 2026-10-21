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
        "product reference sheet exactly (the big front view is the real label); keep it upright and the label facing camera.")
LOOK = "Bright, clean, neutral daylight, true colours, no yellow or golden tint, no dark or moody look. No text, no logos other than the product label."
S = {
 "R1": {"refs": [SHEET, FRONT, BATH], "p": f"Close shot of the castor oil roll-on standing on the white marble counter of the sage-green tiled bathroom from the last reference image, soft morning sun from the window. One fat clear golden drop of castor oil sits on top of the rose quartz roller ball and catches the light like liquid gold. No hands. {PROD}"},
 "R2": {"refs": [SHEET, FRONT, BED], "p": f"A small round mirrored vanity tray on the wooden nightstand of the bedroom from the last reference image. On the tray, left: a pretty faceted glass perfume bottle with pale pink perfume and a round glass cap, no brand, no writing. Right, a little apart: the castor oil roll-on. No hands. {PROD}"},
 "R3": {"refs": ["stills/S5.png"], "p": "Seen from above and behind, no face. EXACTLY TWO HANDS in the whole frame, both hers: an older Black grandmother's hands (brown skin with fine wrinkles, short natural unpainted nails, a thin gold wedding band) part her short grey coily hair and work plain golden castor oil into the scalp at the part with her fingertips. In her other hand, an old unbranded clear glass bottle of golden oil with no label. Lavender cardigan sleeve at the wrist. Soft bright bedroom light, same framing and light as the reference image, but grey hair and older hands. Her right hand works the oil in at the part; her left hand holds the bottle low in the frame. No third hand, no hand on top of the head. Whole wrists, both coming from the bottom edge of the frame."},
 "R4": {"refs": [SHEET, FRONT, BATH], "p": f"A white bathroom shelf in the sage-green tiled bathroom from the last reference image. Left: a big old messy unbranded plastic bottle of castor oil, thick golden oil dripped down its side and a sticky oily ring under it on the shelf, no label text. Right, a little apart: the clean castor oil roll-on. No hands. {PROD}"},
}

ROOM = {1: "redo/rooms/room1_spa_tub.jpg", 2: "redo/rooms/room2_grey_marble.jpg", 3: "redo/rooms/room3_cream_double.jpg", 4: "redo/rooms/room4_navy_vanity.jpg"}
HAND = "stills/S4.png"; BOX = "refs/ralph_sheet_box.jpg"
BRIGHT = ("The room from the room reference image (Ralph's pick for this video), shown in bright natural daylight from the window, "
          "warm lamps and candles off, clean neutral white balance, airy and light.")
PERSON = ("Her hands: medium-brown skin, short natural nude nails, no rings, a dusty mauve cotton t-shirt sleeve, exactly like the hand in the hand "
          "reference image. Only her hands, arm or the named body part are in frame; never her mouth or full face.")
def shot(room, p, v, hand=True, product=True, box=False):
    refs = ([SHEET, FRONT] if product else []) + ([BOX] if box else []) + ([HAND] if hand else []) + [str(H / ROOM[room])]
    return {"refs": refs, "p": p + " " + BRIGHT + (" " + PERSON if hand else " No hands.") + (" " + PROD if product else "") +
            (" Next to it, its real retail box exactly as in the box reference image." if box else ""), "v": v, "product": product}
V1 = {
 "V1a": shot(1, "Close shot: the castor oil roll-on stands on the round wooden stool beside the freestanding white bathtub, a plant behind it. One fat clear golden drop of oil sits on top of the rose quartz roller ball and catches the sunlight like liquid gold.", "the camera slowly pushes in toward the roll-on; the golden drop glistens and slowly slides down the roller ball.", hand=False),
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
