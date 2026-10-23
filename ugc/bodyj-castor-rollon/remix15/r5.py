"""Round 5 (2026-10-23, Ralph: "v1 it shows a head missing" + "her hands do not stay true to Grace's skin tone").
Every shot where Grace's skin shows is remade with HER real hand sheet as a reference (grace/ref/hand-sheets), and no
shot shows a body without a head. Prompts written with prompt-master (Ralph's stack): hard rules first, every image named.

  python3 r5.py prompts --sheet with|without      write r5/prompts/<sheet>/<ID>_still.txt + <ID>_clip.txt (free)
  python3 r5.py stills --sheet S ID [ID ...]      Kie nano-banana-pro, $0.09 each -> r5/stills/ID.png
  python3 r5.py clip --sheet S ID [--dry]         product in frame: Omni 1.1 Flash on Kie 4 s $0.315 (omni_clip.py);
                                                  no product (V1b, V2a): Seedance 2.0 Mini 4 s $0.164
Paid runs go through grace/gate.py (script gate, approved BOOK.md, paid-task ledger).
"""
import argparse, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent
import redo                                     # chdirs to the parent job; kie.py + gate hook
from redo import kie, SHEET, FRONT, BOX, ROOM, PROD, SIZE, BOXSIZE, BRIGHT, LOOK

ROOT = H.parents[2]
HANDS = {"without": str(ROOT / "grace/ref/hand-sheets/without_bracelet.jpg"),
         "with": str(ROOT / "grace/ref/hand-sheets/with_bracelet.jpg")}
FACE = str(ROOT / "grace/ref/grace_reference_sheet.png")
WRIST = {"without": "Bare wrists: no bracelet, no watch.",
         "with": ("On her left wrist, exactly as on the hand sheet: a FLAT gold bracelet of rectangular links like a watch band "
                  "(NO watch face, not a rope chain) and a thin gold chain with small pearls and a gold leaf charm.")}


def grace(sheet, n):
    """Grace's hands, from her real hand sheet (reference image n). Tone first: Ralph's note was the skin tone."""
    return (f"HER HANDS (MUST): they are Grace's real hands from reference image {n} (her hand sheet). Copy the skin tone "
            f"EXACTLY from image {n}: warm medium-brown, the same tone on the back of the hand, the knuckles and the arm, "
            f"in every frame; never lighter, darker, pinker or more golden. Long nude-pink nails with white French tips. "
            f"Rings exactly as image {n}: a silver crown-shaped ring stack on the left ring finger, a gold ring with a "
            f"clear heart-shaped stone on the left index finger, a bright blue silicone band on the left thumb. "
            f"{WRIST[sheet]} Dusty mauve cotton t-shirt sleeve. Five fingers per hand, whole wrists, hands enter from the "
            f"frame edge and grip what they hold.")


NOHEAD = ("FRAMING (MUST): never a body without its head. No shoulders, chest or neck in frame unless her face from the "
          "eyebrows up is also in frame; crop tight to the hands and the named body part only.")
NOHAND = "No hands, fingers, arms or people appear anywhere in the frame at any time."
NEVER = ("Never: an oversized bottle, a second roll-on, extra hands or fingers, text, captions, watermarks, "
         "added effects, a dark or yellow look, a visible mouth.")

# id: (room, product?, box?, kind, still text, motion).  kind: hand | face | free
SHOTS = {
 "V1b": (1, False, False, "hand", "Close shot over the rim of the white freestanding tub: her two cupped hands hold thick golden castor oil "
         "that runs between her fingers and drips in long sticky strings onto the tub rim; an old unbranded clear glass bottle of oil "
         "lies tipped on the rim, no label. Only hands and forearms in frame.",
         "the thick oil keeps oozing through her fingers and drips in slow sticky strings onto the tub rim."),
 "V1c": (1, True, False, "hand", "Close shot by the white freestanding tub: her right hand grips the small castor oil roll-on at the "
         "bottom of the frame, label facing camera; only the hand, wrist and a little forearm in frame, the tub and plants behind.",
         "she lifts the roll-on a little toward the camera and holds it there, label facing camera, one steady grip."),
 "V1d": (1, True, False, "hand", "Close shot: her left hand rests on the tub rim, back of the hand up; her right hand grips the "
         "castor oil roll-on and presses the pink ball on the back of the left hand. Fingertips clean and dry.",
         "she rolls the pink ball across the back of her left hand in one smooth stroke, leaving a thin shiny line."),
 "V1e": (1, True, False, "face", "Extreme close shot of one eyebrow and closed eye, frame bottom at the bridge of the nose (no mouth, "
         "no nose tip): her fingertips hold the small castor oil roll-on, mostly hidden in her fingers, the pink ball on the inner "
         "end of the eyebrow.", "she rolls the ball slowly along the eyebrow to the tail; the eye stays closed."),
 "V1f": (1, True, False, "hand", "Close shot: her left hand rests flat on a folded white towel on the tub rim; her right hand grips "
         "the castor oil roll-on and presses the pink ball on the cuticle of the left index finger.",
         "she rolls the ball over each cuticle, index to ring finger, one after another."),
 "V1g": (1, True, False, "hand", "Tight close shot of her bent left elbow and forearm only, filling the frame from the side (no "
         "shoulder, no chest, no t-shirt body in frame), the tub softly out of focus behind; her right hand grips the castor oil "
         "roll-on and presses the pink ball on the elbow.", "she rolls the ball in small circles over the elbow; the skin turns softly shiny."),
 "V1h": (1, True, False, "hand", "Tight close shot of the ends of her long dark hair held across her left palm (no shoulder, neck, "
         "chest or t-shirt body in frame), the bathroom softly out of focus behind; her right hand grips the castor oil roll-on and "
         "presses the pink ball on the hair ends.", "she rolls the ball down the hair ends; the ends turn smooth and glossy."),
 "V2a": (2, False, False, "hand", "Close shot over the grey marble vanity with the white vessel sink: her right hand tips an old "
         "unbranded clear glass bottle and pours very thick golden castor oil onto a metal spoon held in her left hand; the oil "
         "overflows the spoon and drips onto the marble. Only hands and forearms in frame.",
         "the thick oil keeps oozing over the spoon edge and drips in heavy sticky strings onto the marble."),
 "V2c": (2, True, False, "hand", "Close shot at the grey marble vanity beside the white vessel sink: her right hand grips the small "
         "castor oil roll-on just above the counter, label facing camera; only the hand, wrist and a little forearm in frame.",
         "she lifts the roll-on up a little and holds it there, label facing camera, one steady grip."),
 "V2d": (2, True, False, "hand", "Close shot: her left wrist turned up above the grey marble counter, inner wrist facing camera; her "
         "right hand grips the castor oil roll-on and presses the pink ball on one spot of the inner wrist. Only hands and forearms in frame.",
         "she rolls the ball back and forth on that one small spot, precise and neat."),
 "V2e": (2, True, False, "face", "Extreme close shot from the eyebrow up only (frame bottom at the bridge of the nose, no mouth): "
         "her fingertips hold the small castor oil roll-on, mostly hidden in her fingers, the pink ball on one eyebrow, the hairline "
         "above; eye closed.", "she rolls the ball along the eyebrow and then up into the hairline at the roots."),
 "V2f": (2, True, False, "hand", "Close shot: her left hand resting on a grey hand towel on the marble counter; her right hand grips "
         "the castor oil roll-on and presses the pink ball on the cuticle of the left middle finger.",
         "she rolls the ball over the cuticles, then across the knuckles, leaving a soft sheen."),
 "V3c": (3, True, False, "hand", "Close shot: her left hand flat on the white quartz vanity counter; her right hand grips the castor "
         "oil roll-on and presses the pink ball on the nail of the left index finger.",
         "she rolls the ball over each nail and cuticle, then across the back of the hand."),
 "V3d": (3, True, True, "hand", "Close shot on the white quartz double vanity with a black faucet: both her hands hold the roll-on's "
         "small retail box at chest height, top flap open; only hands and forearms in frame.",
         "she pulls the roll-on out of the open box with her right hand and lifts it toward the camera, label facing camera."),
 "V3e": (3, True, False, "hand", "Close shot over the white quartz double vanity: her left forearm held up, inner side out; her "
         "right hand grips the castor oil roll-on and presses the pink ball on the inner forearm. Only hands and forearms in frame.",
         "she rolls the ball in one smooth line up the inner forearm; her left fingers open to show they are clean and dry."),
 "V3f": (3, True, False, "hand", "Tight close shot of the back of her left hand and wrist resting on the white quartz counter; her "
         "right hand grips the castor oil roll-on and presses the pink ball on the wrist bone.",
         "she rolls the ball across the wrist and up the forearm, right where she needs it."),
 "V4c": (4, True, False, "hand", "Close shot above the navy vanity: her left forearm held out; her right hand grips the castor oil "
         "roll-on and presses the pink ball on the top of the forearm. Only hands and forearms in frame.",
         "she glides the ball in one long easy stroke along the forearm."),
 "V4d1": (4, True, False, "face", "Extreme close shot of one eyebrow, eye closed, from the eyebrow up only (no mouth, no nose): her "
          "fingertips hold the small castor oil roll-on, the pink ball at the inner end of the brow; navy and white bathroom behind.",
          "she rolls the ball along the eyebrow to the tail."),
 "V4d2": (4, True, False, "hand", "Close shot: her left hand resting on the white quartz top of the navy vanity; her right hand grips "
          "the castor oil roll-on and presses the pink ball on the cuticle of the left thumb, just beside the blue band.",
          "she rolls the ball over the thumb and index finger cuticles."),
 "V4d3": (4, True, False, "hand", "Tight close shot of her bent left elbow and forearm only (no shoulder, no chest), the navy vanity "
          "softly out of focus behind; her right hand grips the castor oil roll-on and presses the pink ball on the rough elbow.",
          "she rolls the ball in small circles over the elbow, which turns soft and shiny."),
 "V4d4": (4, True, False, "hand", "Tight close shot of the ends of her long dark hair held across her left palm in front of the glass "
          "shower (no shoulder, neck or chest in frame); her right hand grips the castor oil roll-on and presses the pink ball on the hair ends.",
          "she rolls the ball down the hair ends, which turn smooth and glossy."),
 "V4e": (4, True, False, "hand", "Close shot above the clean white quartz top of the navy vanity: her right hand holds the capped "
         "castor oil roll-on, her left hand open beside it, palm and fingertips clean and dry; the counter is spotless.",
         "she turns her open left hand slowly to show the clean dry fingertips, then sets the roll-on down on the counter."),
}
CLIP_ONLY = {   # hand-free stills from round 4 are right; Seedance added a hand nobody asked for
 "V2b": "the camera slowly arcs a little around the roll-on standing alone on the counter.",
 "V2h": "the camera slowly pushes in a little on the roll-on and its box.",
 "V4b": "the camera slowly pushes in toward the label until the USDA ORGANIC seal is large in frame.",
}


def refs_for(sid, sheet):
    room, product, box, kind, *_ = SHOTS[sid]
    refs = ([SHEET, FRONT] if product else []) + ([BOX] if box else []) + [HANDS[sheet]] + ([FACE] if kind == "face" else []) \
        + [str(H / ROOM[room])]
    return refs


def still_prompt(sid, sheet):
    room, product, box, kind, txt, _ = SHOTS[sid]
    refs = refs_for(sid, sheet); n = {r: i + 1 for i, r in enumerate(refs)}
    named = []
    if product: named.append(f"Image {n[SHEET]} is the product reference sheet and image {n[FRONT]} the real front label: the roll-on matches them letter for letter and colour for colour.")
    if box: named.append(f"Image {n[BOX]} is its real retail box.")
    if kind == "face": named.append(f"Image {n[FACE]} is Grace: her face skin and brows match it, same tone as her hands.")
    named.append(f"Image {n[str(H / ROOM[room])]} is the room.")
    return ("Vertical 9:16 photo, one frame from a phone-shot UGC video. " + grace(sheet, n[HANDS[sheet]]) + " " + NOHEAD + " " +
            ((SIZE + " " + PROD + " ") if product else "") + ((BOXSIZE + " ") if box else "") + " ".join(named) +
            " SHOT: " + txt + " " + BRIGHT + " " + NEVER + " " + LOOK)


def clip_prompt(sid, sheet):
    if sid in CLIP_ONLY:
        return ("Recreate image 1 exactly as the first frame: keep its room, light and framing. Image 2 is the real front label: it "
                "matches image 2 letter for letter and colour for colour the whole clip. Image 3 is the product sheet: keep this exact "
                "small squat shape, size and colours, no added marks, no extra text. " + ("Image 4 is its real retail box. " if sid == "V2h" else "") + NOHAND + " Motion: " + CLIP_ONLY[sid] +
                " The bottle keeps the same small size in every frame. Vertical 9:16 phone footage, bright neutral daylight. "
                "No music, no voice, no captions, no on-screen text.")
    room, product, box, kind, txt, motion = SHOTS[sid]
    if not product:   # Seedance reference mode: image 1 still, image 2 hand sheet
        return ("Recreate reference image 1 exactly as the first frame (same room, framing, light, hands), then: " + motion +
                " The hands are Grace's from reference image 2: the same warm medium-brown skin tone, French-tip nails and rings "
                "in every frame, five fingers each, whole wrists, no new hands appear. Smooth real-time motion, steady camera with a "
                "slight handheld drift. Bright neutral light, no text.")
    k = 4 if box else 3
    return ("Recreate image 1 exactly as the first frame: keep its room, light, framing and hands exactly. Image 2 is the real "
            "front label of the roll-on: it stays on the bottle the whole clip and matches image 2 letter for letter and colour for "
            "colour. Image 3 is the product sheet: keep this exact small squat shape, size and colours, no added marks, no extra text. "
            + (f"Image 4 is its real retail box. " if box else "") +
            f"Image {k + 1} is Grace's real hand sheet: her skin tone, French-tip nails and rings match image {k + 1} in every frame, "
            "never lighter or more golden. Motion: " + motion + " The hand keeps one grip; the bottle never turns its back, flips or "
            "grows. Camera: steady, a slight handheld drift. " + NOHEAD + " Vertical 9:16 phone footage, bright neutral daylight, "
            "realistic skin. No music, no voice, no captions, no on-screen text.")


def write_prompts(sheet):
    d = H / "r5/prompts" / sheet; d.mkdir(parents=True, exist_ok=True)
    for sid in SHOTS:
        (d / f"{sid}_still.txt").write_text(still_prompt(sid, sheet) + "\nREFS: " + " | ".join(refs_for(sid, sheet)) + "\n")
    for sid in list(SHOTS) + list(CLIP_ONLY):
        (d / f"{sid}_clip.txt").write_text(clip_prompt(sid, sheet) + "\n")
    print("prompts", sheet, len(SHOTS), "stills,", len(SHOTS) + len(CLIP_ONLY), "clips")


def still(sid, sheet):
    prompt = still_prompt(sid, sheet)
    url = kie.run_task({"model": "nano-banana-pro", "input": {"prompt": prompt, "image_input": [kie.upload(r) for r in refs_for(sid, sheet)],
                                                              "aspect_ratio": "9:16", "resolution": "1K"}})
    if url:
        out = H / "r5/stills" / f"{sid}.png"; out.parent.mkdir(parents=True, exist_ok=True)
        kie.fetch(url, str(out)); print("still", sid, "ok", flush=True)


def clip(sid, sheet, dry=False):
    pf = H / "r5/prompts" / sheet / f"{sid}_clip.txt"
    still_png = H / ("redo/stills" if sid in CLIP_ONLY else "r5/stills") / f"{sid}.png"
    if sid in SHOTS and not SHOTS[sid][1]:          # no product in frame: Seedance 2.0 Mini
        if dry: print("DRY seedance", sid, "$0.164"); return
        refs = [kie.upload(str(still_png)), kie.upload(HANDS[sheet])]
        url = kie.run_task({"model": "bytedance/seedance-2-mini", "input": {"prompt": pf.read_text().strip(), "reference_image_urls": refs,
                            "generate_audio": False, "aspect_ratio": "9:16", "resolution": "720p", "duration": "4"}})
        if url:
            out = H / "r5/clips" / f"{sid}.mp4"; out.parent.mkdir(parents=True, exist_ok=True); kie.fetch(url, str(out))
        return
    box = sid in SHOTS and SHOTS[sid][2] or sid == "V2h"
    cmd = [sys.executable, str(ROOT / ".claude/skills/ugc-product-ad/scripts/omni_clip.py"), str(H / "r5"), sid, "--prompt-file", str(pf),
           "--still", str(still_png), "--ref", str(ROOT / "ugc/bodyj-castor-rollon" / FRONT), "--ref", str(ROOT / "ugc/bodyj-castor-rollon" / SHEET)]
    if box: cmd += ["--ref", str(ROOT / "ugc/bodyj-castor-rollon" / BOX)]
    if sid in SHOTS: cmd += ["--ref", HANDS[sheet]]
    cmd += ["--seconds", "4"] + (["--dry"] if dry else [])
    subprocess.run(cmd, check=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("ids", nargs="*")
    ap.add_argument("--sheet", choices=["with", "without"], required=True); ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    if a.cmd == "prompts": write_prompts(a.sheet)
    elif a.cmd == "stills": [still(i, a.sheet) for i in a.ids]
    elif a.cmd == "clip": [clip(i, a.sheet, a.dry) for i in a.ids]
