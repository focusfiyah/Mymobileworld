"""Bare Anatomy Rosemary & Rice Water spray, 3-pack (Grace, 2026-11-02): writes shots.json + prompts/*.txt + prompts/refs.json.
Copied from earth-breeze-sheets/make_shots.py. Prompts written with prompt-master (Ralph's stack): size first, numbered references,
print matched letter for letter. Product facts only from product_truth.json (listing photos L2/L4/L6 + Grace's screenshots).
Final shot script: scripts.md (11.4 s, 7 shots, music only, no text). S7 is three 0.6 s cuts (S7a/b/c)."""
import json
from pathlib import Path

J = Path(__file__).parent
SIZE = ("SIZE FIRST: the bottle is a 200 ml bottle, about 17 cm tall including the sprayer (about as tall as an adult hand from wrist to fingertip) "
        "and about 5 cm wide; an adult hand wraps all the way around its body. It is NEVER bigger than a hand, NEVER a tall salon bottle.")
BOTTLE = ("The real Bare Anatomy Rosemary & Rice Water Hair Spray bottle, exactly as on the product sheet: a CLEAR round see-through plastic bottle "
          "with rounded shoulders, filled with CLEAR colourless liquid (never orange, yellow or tinted), a tall glossy BLACK collar and a BLACK curved trigger sprayer "
          "with a long nozzle. The front label is printed straight on the clear bottle: 'BARE ANATOMY' in black spaced serif capitals with a small TM, "
          "'NATURE x SCIENCE' in small black capitals, a pale-blue water splash with a green rosemary sprig and a yellow sprig, 'Rosemary & Rice Water' in bold purple, "
          "'HAIR SPRAY' in dark purple capitals between thin grey lines, two small round purple line icons reading 'ALCOHOL FREE' and 'SULPHATE FREE', "
          "then small black text 'Helps Hair Appear Fuller & Voluminous', 'Water-Based Formula', '200 ml | 6.76 fl oz'. "
          "No other words, no badges, no stickers, no box.")
HAIR = ("Her hair is Grace's real hair exactly as in the hair reference: long jet-black knotless boho braids, thin and neat, with loose curly ends, the braids parted into small square sections so straight lines of scalp show between them. Medium-dark brown skin on the scalp. No loose straight hair, no wig, no head wrap.")
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch; "
        "the hand enters from the frame edge, the whole wrist visible, and GRIPS what it holds.")
NOHAND = "No hand, no fingers, no people, no face."
END = ("Vertical 9:16 phone photo, a single frame from a phone-shot UGC video, bright neutral daylight, true colours, realistic texture, "
       "no face, no text, no captions, no watermark, no logos other than the real bottle print.")
CLIPEND = "Bright neutral daylight. No music, no voice, no captions, no on-screen text."

REFDESC = {
    "sheet": "the product sheet, real photos only: the big left photo is the real bottle front, copy its shape, proportions, black sprayer and print exactly; top right is the real back; bottom right shows the three real bottles of the 3-pack",
    "front": "a real close-up of the front label, which must match letter for letter and colour for colour",
    "sprayer": "a real close-up of the black collar and black trigger sprayer, copy its exact shape",
    "hand": "Grace's hand sheet (her real hands, rings and nails)",
    "hair": "Grace's real hair (long black knotless boho braids with curly ends), copy this exact hair",
    "A": "the real room to use as the soft background (same green tiles, colours and light)",
    "B": "the real room to use as the background (same dark counter, green mosaic tiles, plants, colours and light)",
    "C": "the real room to use as the background (same kitchen, gas stove, tiles, plants, colours and light)",
    "D": "the real room to use as the background (same shower with tropical leaf tiles, colours and light)",
    "E": "the real room to use as the background (same wood table, plants, shelves, colours and light)",
    "F": "the real room to use as the background (same bright kitchen with plants on the shelf, colours and light)",
}
FILES = {"sheet": "refs/product_sheet.png", "front": "refs/closeup_front.png", "sprayer": "refs/closeup_sprayer.png",
         "hand": "../../grace/ref/hand-sheets/without_bracelet.jpg", "hair": "refs/grace_hair.jpg",
         **{k: f"rooms/room_{k}.jpg" for k in "ABCDEF"}}


def refs_text(keys):
    return "Reference images: " + "; ".join(f"image {i} = {REFDESC[k]}" for i, k in enumerate(keys, 1)) + "."


def s(id, t, beat, hand, bottle, room, model, still, motion, refs, hair=False):
    keys = list(refs) + ([room] if room else [])
    lead = still if still.startswith("FRAMING FIRST") else ""
    still_txt = " ".join(x for x in [
        lead,
        (SIZE + " " + BOTTLE) if bottle else "",
        HAIR if hair else "",
        "" if lead else still,
        HAND if hand else NOHAND,
        END, refs_text(keys)] if x)
    if model == "omni":
        crefs = ["still"] + [k for k in refs if k in ("front", "sprayer")] + ["sheet"]
        names = {"front": "the real front label, which must match letter for letter and colour for colour",
                 "sprayer": "the real black collar and trigger sprayer, keep its exact shape",
                 "sheet": "the product sheet: keep this exact clear bottle, black sprayer, size and print"}
        r = "; ".join(f"image {i} is {names[k]}" for i, k in enumerate(crefs, 1) if k != "still")
        clip = (f"Recreate image 1 exactly as the first frame: keep its room, light, framing{' and hand' if hand else ''} exactly. "
                + r + ". "
                + f"Motion: {motion} "
                + ("The hand keeps one grip; the bottle never turns, flips, grows or changes shape; the liquid stays clear; the print never changes. " if hand else
                   "The bottles never move, grow or change; the liquid stays clear; the print never changes. ")
                + ("" if hand else "No hand, fingers or people appear at any time. ")
                + CLIPEND)
        clip_refs = [f"stills/{id}.png"] + [FILES[k] for k in crefs[1:]]
    else:
        clip = (f"Recreate reference image 1 exactly as the first frame, then: {motion} "
                + ("" if hand else "No hand, fingers or people appear at any time. ")
                + "No spray bottle and no hair product appears at any time. " + CLIPEND)
        clip_refs = [f"stills/{id}.png"] + ([FILES["hand"]] if hand else [])
    return {"id": id, "t": t, "beat": beat, "hand": hand, "product": bottle, "room": room, "model": model,
            "still": still_txt, "clip": clip, "still_refs": [FILES[k] for k in keys], "clip_refs": clip_refs}


SHOTS = [
    s("S1", [0.0, 2.0], "Hook", True, True, "A", "omni",
      "FRAMING FIRST: close shot from behind her, slightly to her right side. The back and side of her head with her long braids fill the LEFT two-thirds of the frame, "
      "from the top of her head down to her shoulders. Her hand comes in from the RIGHT edge and GRIPS the ONE bottle around its body beside her head, index finger on the black trigger; "
      "the nozzle points LEFT, straight at the braids near the roots, its tip only a hand's width from the braids, so the braids are directly in front of the nozzle. "
      "The front label faces the camera and is EXACTLY image 2: printed straight onto the CLEAR plastic so the clear liquid shows through it, "
      "NO white label panel, NO green box or green band; 'HAIR SPRAY' is dark purple letters on clear plastic between thin grey lines. "
      "Green tiles soft and out of focus behind on the right. Only one bottle.",
      "her index finger squeezes the trigger twice; each time a fine clear mist shoots LEFT from the nozzle and lands on the braids right in front of it. "
      "The liquid clearly stays in the hair: after the first spray, many tiny clear water droplets sit on the braids in a patch where the mist landed and that patch of braids looks damp and darker; "
      "after the second spray the wet patch is bigger with more droplets. The droplets stay on the braids until the end. "
      "No mist goes past her head or across the frame. The hand stays in place. Camera steady.",
      ["sheet", "front", "sprayer", "hand", "hair"], hair=True),
    s("S2", [2.0, 3.4], "Pain", False, False, "C", "seedance",
      "Close shot on the gas stove: a small steel pot of water with a few green rosemary sprigs floating in it, gently simmering, steam rising; "
      "the tiled wall and plants soft behind. Only the pot, no other products.",
      "the camera slowly dollies in toward the pot while the water simmers and steam curls up.",
      []),
    s("S3", [3.4, 5.0], "Solution", False, True, "B", "omni",
      "EXACTLY THREE identical bottles stand in a row on the dark counter, fronts facing the camera, a small fresh rosemary sprig and a small wooden bowl of white rice beside them; "
      "green mosaic tiles and plants behind. The three bottles are the same size and print, each matching image 2 letter for letter. No other products.",
      "only the camera moves, a small slow slide from left to right, the three bottles always facing the camera; nothing in the room moves.",
      ["sheet", "front"]),
    s("S4", [5.0, 6.6], "How to use", True, False, "A", "seedance",
      "Close shot from just above: her fingertips rest on the scalp along one braid part, ready to rub in small circles. No bottle in the frame. Green tiles soft behind.",
      "her fingertips rub the scalp along the braid part in small slow circles, the braids moving a little. Camera steady.",
      ["hand", "hair"], hair=True),
    s("S5", [6.6, 8.0], "Selling point", True, False, "A", "seedance",
      "Close shot from behind her shoulder: her hand holds a few of her long braids near the top between her thumb and fingers, the curly ends hanging below. No bottle, no comb in the frame. Green tiles soft behind.",
      "her fingers slide slowly down the braids from top to the curly ends, the braids soft and light, and let them fall. Camera steady.",
      ["hand", "hair"], hair=True),
    s("S6", [8.0, 9.4], "Urgency", False, True, None, "omni",
      "ONE bottle stands on a white wooden windowsill, front facing the camera; behind it the window glass has soft white frost in the corners and a snowy garden outside, "
      "bright cold daylight. Only one bottle.",
      "only the camera moves, a slow push-in toward the bottle; nothing moves.",
      ["sheet", "front"]),
    s("S7a", [9.4, 10.0], "Close (3-pack)", True, True, "D", "omni",
      "Mid shot in the shower: her hand sets ONE bottle down on the shower ledge, front facing the camera, the tropical leaf tiles behind. Only one bottle.",
      "her hand sets the bottle down on the ledge and pulls away out of frame. Camera steady.",
      ["sheet", "front", "hand"]),
    s("S7b", [10.0, 10.6], "Close (3-pack)", True, True, "E", "omni",
      "Mid shot from above: an open plain black gym bag with no logo sits on the wood table; her hand holds ONE bottle by its body just above the open bag, front facing the camera. "
      "Plants and shelves soft behind. Only one bottle.",
      "her hand lowers the bottle into the open bag and lets go; it settles upright among a rolled towel. Camera steady.",
      ["sheet", "front", "hand"]),
    s("S7c", [10.6, 11.4], "Close (3-pack)", True, True, "F", "omni",
      "Mid close shot: her hand holds ONE bottle out toward the camera by its body, as if handing it to the viewer, the front label facing the camera and fully visible; "
      "the bright kitchen with plants soft behind. Only one bottle.",
      "the hand moves the bottle a little closer to the lens with one small steady move and holds it there.",
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
    print(len(SHOTS), "shots;", sum(not x["hand"] for x in SHOTS), "hand-free;", sum(x["model"] == "omni" for x in SHOTS), "omni")
