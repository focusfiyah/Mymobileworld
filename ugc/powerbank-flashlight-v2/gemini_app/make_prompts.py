"""Flashlight V2 Gemini-app kit (Ralph 2026-10-22: "Let's go with Gemini"). Writes prompt_<shot>.txt + KIT.md.
python3 gemini_app/make_prompts.py A|B   (A = orange button next to the clip, B = button below the panel, near the lens end)
Prompts follow prompt-master (Ralph's stack): size first, numbered references named by what they are, the product matched
part for part and colour for colour, one moment per photo, no text, no light-effect words."""
import sys
from pathlib import Path

ORDER = sys.argv[1].upper()
D = Path(__file__).resolve().parent

REF = {
    "sheet": ("ref1_product_sheet.png", "real photos of the flashlight: front, back, a close-up of its logo, its USB-A port, and its end cap pulled off showing the USB-C port"),
    "shape": ("ref2_true_shape.png", "a real photo of the flashlight standing upright with its carabiner clip on top: its true slim proportions and the order of its parts"),
    "lens": ("ref3_lens_closeup.png", "two real close-ups of the lens end: a rounded-square dark grey metal bezel around a clear domed zoom lens with a small square LED chip in the centre"),
    "hand": ("ref4_grace_hand.jpg", "her real hand: skin tone, nails, rings and bracelets"),
    "port": ("ref5_port_closeup.png", "a real close-up of the USB-A port, revealed when the dark end cap is pulled a little away from the body"),
    "logo": ("ref6_logo_closeup.png", "a real close-up of the print on the dark end cap: a white shark logo and the words SMILING SHARK"),
}

PARTS = {
    "B": "from the clip end: a light blue-grey plastic carabiner clip with a thin silver wire gate; the light blue-grey matte body with a long rounded-rectangle frosted pale light panel; then ONE square orange button with an embossed power symbol; then a darker grey brushed-metal end cap (about a quarter of the length) whose tip is the lens: a rounded-square dark grey bezel around a clear domed zoom lens with a small square LED chip in its centre (no silver reflector)",
}[ORDER]

SIZE = ("SIZE FIRST: the flashlight is 15.7 cm long including its clip and 2.95 cm square, about 5 times as long as it is wide, "
        "90 g. It is about as long as a phone and as wide as two fingers. Slim, never stubby, never a big torch.")

PRODUCT = ("THE FLASHLIGHT must match the real photos exactly, part for part and colour for colour: a slim square bar with "
           f"rounded corners, and its parts in this order {PARTS}. The only print on it: on the front of the dark end cap a white "
           "shark logo with the words SMILING SHARK in white bold letters, exactly as in the logo close-up, letter for letter; on the "
           "back of the cap a few lines of tiny white spec text; on the back of the body one small round hole near the clip. No other "
           "text, no stickers, no extra buttons, no screen, no second light. Only one flashlight in the photo.")

HAND = ("HER HAND (the only person in the photo): exactly the hand in the hand image: medium-brown skin, slim fingers, natural pink "
        "nails with crisp white French tips, a silver crown-shaped stack ring, a thin gold solitaire ring and a blue silicone band, "
        "a chunky gold watch-link bracelet and a thin gold chain with small pearls and a gold leaf charm on the wrist. The hand "
        "enters from the edge of the frame with the whole wrist visible; the fingers truly grip what they hold.")

NOHAND = "No hands, fingers or people anywhere in the photo."

PLACE = ("PLACE: one campsite in a pine forest at blue hour, just after sunset: the sky is still bright blue with a soft pale glow at "
         "the horizon, the scene is evenly and clearly lit, true neutral colours, no orange, yellow or golden cast, not dark or moody. "
         "A sage-green dome tent, a weathered wooden picnic table, pine trees and distant mountains.")

STYLE = ("Real photo taken on a phone, casual and realistic, like a real person took it. Vertical 9:16. No text, no captions, no "
         "watermark, no other logos or brand names anywhere, no lens flare, no sparkles, no light streaks.")

SHOTS = [
    ("S1", "Who in the world made this???", ["sheet", "shape", "logo", "hand"], True,
     "Close-up at chest height: her hand grips only the dark metal end cap at the bottom of the flashlight and holds it upright, so the orange button and the whole light panel stay uncovered in front of the pine trees, "
     "the side panel switched on with soft white light, the orange button facing the camera, and the whole carabiner clip visible "
     "above her fingers. The flashlight fills about a third of the frame height; the tent is soft in the background."),
    ("S2", "Because what do you mean I can charge my phone with this,", ["sheet", "shape", "port"], False,
     "On the wooden picnic table, the flashlight lies on its front, light off, its dark end cap pulled about 1 cm away from the body "
     "so the USB-A port shows on the back, exactly as in image 3. A white USB cable is plugged into that port and runs to a black "
     "smartphone lying face up next to it. The phone screen is dark except for one small green "
     "battery symbol in the middle, no words or numbers. Camera low and close along the table."),
    ("S3", "hang it up in my tent for hands-free lighting,", ["sheet", "shape"], False,
     "Inside the sage-green dome tent at blue hour: the flashlight hangs by its carabiner clip from the small fabric loop at the top "
     "of the tent, side panel on, lighting the tent walls with soft white light. A rolled sleeping bag and a pillow below. The "
     "flashlight is small in the frame, the whole tent interior visible."),
    ("S4", "AND use it as a regular flashlight with a focused beam?", ["sheet", "shape", "lens", "hand"], True,
     "First-person view down a narrow dirt trail between pine trees: her hand at the bottom centre of the frame holds the flashlight "
     "pointing straight ahead and away from the camera, its lens end facing down the trail, side panel off. A focused white "
     "beam runs straight ahead from the torch head and makes a bright round pool of light on the trail exactly where it points; no "
     "light anywhere else."),
    ("S5", "And it has a flickering mode, too, for emergencies!", ["sheet", "shape", "logo", "lens"], False,
     "The flashlight stands on a flat rock at the edge of the campsite, turned three-quarters so the lens at the tip of the dark end cap faces "
     "the camera at an angle, side panel OFF and dark. The lens is switched on with a bright white light shining toward the "
     "trees; nothing else is lit by it. Camera low, close to the rock."),
    ("S6", "This is the kind of gadget that makes sense to keep with your camping gear", ["sheet", "shape", "logo"], False,
     "A dark-grey hiking backpack stands on the ground; the flashlight hangs from its shoulder strap by the carabiner clip, side panel on. "
     "The strap is 5 cm wide and the flashlight is about three times as tall as the strap is wide. The tent and the mountains are soft "
     "behind it."),
    ("S7", "or emergency kit.", ["sheet", "shape", "hand"], True,
     "Top-down close-up: an open plain dark-blue zip pouch on the picnic table with bandages, a small water bottle and a roll of tape "
     "inside. Her hand grips the flashlight by its dark metal end cap and is lowering it into the pouch, light off, the orange button visible. The pouch has no cross, no "
     "logo and no writing."),
    ("S8", "And it costs less than a McDonald's Happy Meal!", ["sheet", "shape", "logo", "hand"], True,
     "Her hand stands the flashlight upright on the picnic table, torch head down on the wood and the carabiner clip on top, side "
     "panel on; her fingers grip only the dark metal end cap at the bottom, the orange button and the light panel uncovered. The whole clip is visible. Only the flashlight and her hand on the table, "
     "the campsite soft behind. No food, no packaging, no other products."),
    ("S9", "I'm linking it in the orange cart for you!", ["sheet", "shape", "logo", "hand"], True,
     "Close-up: her hand clips the flashlight's carabiner onto the shoulder strap of the dark-grey backpack, thumb pressing the "
     "silver wire gate open, the orange button facing the camera, side panel on. The mountains are soft behind."),
]


def prompt(sid, line, refs, hand, scene):
    names = "; ".join(f"Image {i} = {REF[r][1]}" for i, r in enumerate(refs, 1))
    p = [f"I am uploading {len(refs)} reference images. {names}.",
         f"Make one photo (shot {sid} of a 9-photo video series). {SIZE}",
         f"SCENE: {scene}", HAND if hand else NOHAND, PRODUCT, PLACE, STYLE]
    return "\n\n".join(p), [REF[r][0] for r in refs]


kit = ["# Flashlight V2: Gemini app kit", "",
       "For each shot: open a NEW Gemini chat, upload the listed images in this order, paste the prompt, send the image back.", ""]
for sid, line, refs, hand, scene in SHOTS:
    text, files = prompt(sid, line, refs, hand, scene)
    (D / f"prompt_{sid}.txt").write_text(text + "\n")
    kit += [f"## {sid} ({'HAND' if hand else 'HAND-FREE'}): \"{line}\"", "Upload: " + ", ".join(files), "", "```", text, "```", ""]
(D / "KIT.md").write_text("\n".join(kit))
print("wrote", len(SHOTS), "prompts, order", ORDER)
