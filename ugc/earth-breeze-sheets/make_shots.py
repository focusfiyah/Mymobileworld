"""Earth Breeze sheets V1 (Grace, 2026-10-30): writes shots.json + prompts/*.txt + prompts/refs.json.
Prompts written with prompt-master (Ralph's stack): size first, numbered references, print matched letter for letter.
Product facts only from product_truth.json (listing photos L1/L5/L7, Ralph 2026-10-30)."""
import json
from pathlib import Path

J = Path(__file__).parent
BOX_SIZE = ("SIZE FIRST: the box is a FLAT, SLIM portrait box about 25 cm tall, 16 cm wide and only about 1 cm thick, "
            "as big as a small tablet and as thin as a phone; an adult hand covers about half its width. It is NOT a carton, NOT a cube, NOT a tub.")
BOX = ("The real Earth Breeze Laundry Detergent Sheets box, Fresh Scent, exactly as the big photo on the product sheet: sky-blue to light aqua front with small bubbles; "
       "a green tab top-left reading 'FRESH SCENT' in white; top-right 'Lasts up to 60 LOADS' in white beside a clear bubble; white arc text 'powerful clean. safe ingredients.'; "
       "the 'earth breeze' logo in heavy dark navy lowercase letters with a light-blue and white swoosh ring behind it; a white paper banner reading 'laundry detergent sheets' in navy; "
       "a water line; a sea turtle bottom-left with a small heart reading 'No Mess, No Plastic Jug'; navy 'NO HARSH CHEMICAL RESIDUE'; a dark navy t-shirt split down the middle on the right; "
       "'30 SHEETS' along the bottom. No other words, no badges, no flags, no ® other than the one on the logo.")
SHEET = ("The sheet: ONE plain matte WHITE paper-thin rectangle, 14 x 11 cm (about the size of an adult palm), soft like thin paper, with NO print, NO colour, NO holes, NO perforation line.")
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch; "
        "the hand enters from the frame edge, the whole wrist visible, and GRIPS what it holds.")
NOHAND = "No hand, no fingers, no people."
END = ("Vertical 9:16 phone photo, a single frame from a phone-shot UGC video, bright neutral daylight, true colours, realistic skin texture, "
       "no text, no captions, no watermark, no logos other than the real box print.")
CLIPEND = "Bright neutral daylight. No music, no voice, no captions, no on-screen text."

REFDESC = {
    "sheet": "the product sheet, real photos only: the big left photo is the real box front, copy its shape, proportions and print exactly; the stack at right shows the plain white sheets",
    "front": "a real close-up of the box front print, which must match letter for letter and colour for colour",
    "sheetstack": "a real close-up of the plain white sheets (no print)",
    "hand": "Grace's hand sheet (her real hands, rings and nails)",
    "A": "the real room to use as the background (same laundry corner, washer, plant, colours and light)",
    "B": "the real room to use as the background (same green tiles, washer, colours and light)",
    "C": "the real room to use as the background (same blue patterned tiles, woven hamper, colours and light)",
    "D": "the real room to use as the background (same bright guest bedroom, floral pillows, rattan lamp, colours and light)",
}
FILES = {"sheet": "refs/product_sheet.png", "front": "refs/closeup_front.png", "sheetstack": "refs/closeup_sheet_stack.png",
         "hand": "../../grace/ref/hand-sheets/without_bracelet.jpg",
         "A": "rooms/room_A.jpg", "B": "rooms/room_B.jpg", "C": "rooms/room_C.jpg", "D": "rooms/room_D.jpg"}


def refs_text(keys):
    return "Reference images: " + "; ".join(f"image {i} = {REFDESC[k]}" for i, k in enumerate(keys, 1)) + "."


def s(id, t, line, hand, box, room, model, still, motion, refs):
    keys = list(refs) + ([room] if room else [])
    still_txt = " ".join(x for x in [
        (BOX_SIZE + " " + BOX) if box else "",
        still,
        HAND if hand else NOHAND,
        END, refs_text(keys)] if x)
    if model == "omni":
        crefs = ["still"] + [k for k in refs if k in ("front", "sheetstack")] + (["sheet"] if box else [])
        names = {"still": None, "front": "the real box front print, which must match letter for letter and colour for colour",
                 "sheetstack": "the real plain white sheets, no print", "sheet": "the product sheet: keep this exact flat slim box shape and print"}
        r = "; ".join(f"image {i} is {names[k]}" for i, k in enumerate(crefs, 1) if k != "still")
        clip = (f"Recreate image 1 exactly as the first frame: keep its room, light, framing{' and hand' if hand else ''} exactly. "
                + (r + ". " if r else "")
                + f"Motion: {motion} "
                + ("The hand keeps one grip and the box never turns, flips, grows or changes shape; the print never changes. " if hand and box else "")
                + ("The box never moves, grows or changes; the print never changes. " if box and not hand else "")
                + ("" if hand else "No hand, fingers or people appear at any time. ")
                + CLIPEND)
        clip_refs = [f"stills/{id}.png"] + [FILES[k] for k in crefs[1:]]
    else:
        clip = (f"Recreate reference image 1 exactly as the first frame, then: {motion} "
                + ("" if hand else "No hand, fingers or people appear at any time. ")
                + "No detergent box, no laundry sheet appears. " + CLIPEND)
        clip_refs = [f"stills/{id}.png"] + ([FILES["hand"]] if hand else [])
    return {"id": id, "t": t, "line": line, "hand": hand, "product": box or "sheet" in refs or "sheetstack" in refs,
            "box": box, "room": room, "model": model, "still": still_txt, "clip": clip,
            "still_refs": [FILES[k] for k in keys], "clip_refs": clip_refs}


SHOTS = [
    s("S1", [0.0, 2.6], "Okay, watch what happens when I drop this in water.", True, False, "A", "omni",
      SHEET + " Close shot from slightly above: her hand comes in from the top edge and pinches ONE plain white sheet by one corner, "
      "holding it flat just above a wide clear glass bowl full of water that sits on top of the front-loading washer. The water is clear and still. No box in the frame.",
      "her fingers let go and the white sheet drops flat onto the water and floats; its edges start to turn see-through. The camera holds steady.",
      ["sheetstack", "hand"]),
    s("S2", [2.6, 4.6], "That's a whole load, melting away.", False, False, "A", "omni",
      SHEET + " Top-down close-up into the wide clear glass bowl of water on top of the washer: the one white sheet floats flat on the water, "
      "its edges already soft and see-through, tiny bubbles around it. No box in the frame.",
      "the sheet softens, splits into soft pieces and melts into cloudy white water with a little light foam while the camera slowly pushes down toward the bowl.",
      ["sheetstack"]),
    s("S3", [4.6, 6.4], "No more hauling a heavy jug,", True, False, "A", "seedance",
      "Low side shot by the washer: her hand GRIPS the handle of a big heavy plain white plastic laundry jug with NO label, NO logo and NO words on it, "
      "lifting it off the floor; a thin blue drip runs down its side from under its cap. Only the jug, no other laundry product.",
      "her hand heaves the heavy jug up a few centimetres, it sways and pulls her wrist down, and the blue drip slides further down its side. Camera locked off.",
      ["hand"]),
    s("S4", [6.4, 8.3], "and it leaves no harsh chemical residue.", False, False, "B", "seedance",
      "Close shot: a clean dark navy cotton t-shirt, freshly washed, folded neatly on top of the washer in the green-tile bathroom; deep even colour, smooth soft fabric, "
      "no marks, no white streaks, no print on the shirt.",
      "the camera glides slowly along the folded navy shirt from its collar to its hem; nothing else moves.",
      []),
    s("S5", [8.3, 10.0], "Just pull one out", True, True, "C", "omni",
      "Mid shot like the real how-to photo: one hand holds the box upright by its lower half with the front facing the camera, "
      "and the other hand's fingers pinch ONE plain white sheet and pull it halfway up out of the slot along the box's TOP edge. " + SHEET +
      " Only one box. Blue patterned tile wall soft behind.",
      "the fingers slide the white sheet up and out of the top slot in one smooth pull while the other hand holds the box still.",
      ["sheet", "front", "hand"]),
    s("S6", [10.0, 11.6], "and toss it in.", True, False, "B", "omni",
      SHEET + " Close shot into the open front-loading washer: her hand holds one white sheet at the open door, above a pile of colourful clothes in the drum. No box in the frame.",
      "her hand tosses the white sheet into the drum; it lands flat on top of the clothes and the hand pulls back out of frame. Camera steady.",
      ["sheetstack", "hand"]),
    s("S7", [11.6, 13.6], "I'm kinda mad nobody told me sooner.", False, True, "A", "omni",
      "One box stands upright on top of the front-loading washer, front facing the camera, leaning lightly against the wall beside the potted plant and a small stack of folded towels. Only one box.",
      "only the camera moves, a slow push-in toward the box; nothing in the room moves.",
      ["sheet", "front"]),
    s("S8", [13.6, 16.4], "Grab a couple boxes before Thanksgiving guests show up.", False, True, "D", "omni",
      "Close, low camera at the foot of the made guest bed: EXACTLY TWO identical boxes lie flat side by side, fronts up and facing the camera, on a neat stack of fresh folded white towels; "
      "the two boxes fill the lower half of the frame so every word of their print is large and sharp, the bed, floral pillows and rattan lamp soft behind. "
      "Both boxes the same size and print, each matching image 2 letter for letter. No other products.",
      "only the camera moves, a slow dolly in along the bed toward the two boxes on the towels; nothing moves.",
      ["sheet", "front"]),
    s("S9", [16.4, 18.5], "It's in the orange cart.", True, True, "B", "omni",
      "Mid close shot: her hand holds ONE box upright toward the camera by its lower half, the front facing the camera and fully visible, thumb on the front's bottom corner only; the box front is EXACTLY the real design in image 2 (sea turtle, t-shirt panel, swoosh ring, arc text), never a simplified or redrawn design; "
      "the green-tile bathroom with the washer soft behind. Only one box.",
      "the hand brings the box a little closer to the lens with one small steady move and holds it there.",
      ["sheet", "front", "hand"]),
]

if __name__ == "__main__":
    (J / "prompts").mkdir(exist_ok=True)
    json.dump({"shots": SHOTS}, open(J / "shots.json", "w"), indent=1)
    refs = {}
    for x in SHOTS:
        (J / f"prompts/still_{x['id']}.txt").write_text(x["still"])
        (J / f"prompts/clip_{x['id']}.txt").write_text(x["clip"])
        refs[f"still_{x['id']}.txt"] = len(x["still_refs"])
        refs[f"clip_{x['id']}.txt"] = len(x["clip_refs"])
    json.dump(refs, open(J / "prompts/refs.json", "w"), indent=1)
    print(len(SHOTS), "shots;", sum(not x["hand"] for x in SHOTS), "hand-free")
