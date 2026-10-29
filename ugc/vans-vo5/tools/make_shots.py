"""Builds shots.json for Vans V13-V17 (5 videos x 11 shots on Grace's own VO), 2026-10-29.
Written with prompt-master (Ralph's stack): framing + toe direction first, numbered refs named by what they ARE, every
logo the frame shows passed as a real close-up, who wears/holds what stated, no effect words, no text.
  python3 tools/make_shots.py   -> shots.json (+ prints a count)
Shared truth blocks come from product_truth.json facts (real photos); shot specs are the SPEC table below."""
import json, re
from pathlib import Path

J = Path(__file__).resolve().parent.parent

# Grace's VO, line windows from TikTok's own timed transcript (ref/transcript_timed.txt); C/D and F/G split mid-line.
WIN = {"A": (0.0, 2.8), "B": (2.8, 5.3), "C": (5.3, 8.7), "D": (8.7, 10.8), "E": (10.8, 14.1), "F": (14.1, 15.2),
       "G": (15.2, 16.3), "H": (16.3, 19.8), "I": (19.8, 22.0), "J": (22.0, 25.3), "K": (25.3, 27.6)}
LINE = {"A": "Who told Vans to come out with these sparkly low tops?",
        "B": "Because whoever made that decision deserves a raise.",
        "C": "These are the Premium Authentic, and they really took the classic Vans look",
        "D": "and gave it a major upgrade.",
        "E": "The sequins add just the right amount of shine without being over the top,",
        "F": "so you can dress it up", "G": "or keep it casual.",
        "H": "And they're actually so comfortable, so you're getting the style and the comfort.",
        "I": "These are new, but I wouldn't wait too long to grab them,",
        "J": "because when the shiny girlies find these, they're going to sell them out fast.",
        "K": "Tap that orange cart and get your size before they're gone."}

R = {"SHEET": ("refs/product_sheet.png", "the real shoe from every side (product sheet: pair, side, top with red insole, gum waffle sole, back, sequin close-up)"),
     "SEQ": ("refs/shoe_closeup.jpg", "the real sequin squares, side tab and laces up close"),
     "TAB": ("refs/real_vans_tab.jpg", "the real woven side tab: a small BLACK tab with white VANS letters, sewn flat on the outer side"),
     "HEEL": ("refs/real_heel_label.jpg", "the real back of the shoe: the vertical BLACK heel stripe with white stitching and the small WHITE 'OFF THE WALL' skateboard label with black print on the off-white sidewall"),
     "INSOLE": ("refs/real_insole_logo.jpg", "the real insole: deep RED with a WHITE rectangle holding the red VANS skateboard-tail logo"),
     "SKIN": ("refs/ref5_skin_toes.png", "her skin tone only (ignore its outfit, pose and place)"),
     "HAND": ("refs/ref6_hand.png", "her real hand")}

SHOE = ("THE SHOE must match the product sheet and every close-up exactly, letter for letter and colour for colour: the real "
        "Vans Premium Authentic low-top lace-up sneaker in sequin checkerboard. A black and off-white checkerboard where ONLY the "
        "black squares are covered in raised black sequins (a few loose at the edges) and the off-white squares are plain woven "
        "canvas; black leather binding round the collar with white stitching; a black tongue; natural tan canvas lining; flat "
        "black cotton laces through four pairs of black eyelets; a small BLACK woven tab with white VANS letters on the outer side; "
        "a vertical black heel stripe; a chunky smooth off-white rubber sidewall with a small WHITE 'OFF THE WALL' label at the "
        "back; a deep RED insole with a WHITE rectangle holding the red VANS logo; a gum-brown waffle sole. True size: an adult "
        "women's sneaker about 25 cm long, exactly the length of her own foot. No other logos, no ® or ™ added, no extra text.")
HAND = ("HER HAND exactly like the hand reference: medium brown skin, slim fingers, long soft pink nails with white French tips, "
        "a silver ring stack, a gold ring with one clear trillion stone, a blue silicone band on the thumb, a flat gold bracelet of "
        "rectangular links like a watch band (no watch face) and a thin pearl chain with a gold leaf. {sleeve} at the wrist. The "
        "hand enters from the frame edge, whole wrist visible, five fingers, and it GRIPS what it holds: thumb on one side, "
        "fingers curled round the other.")
LIGHT_IN = ("LIGHT: bright soft window daylight, neutral white balance: the off-white squares stay off-white, the walls keep "
            "their true colour, no yellow, orange or golden cast, no dark or moody grade.")
LIGHT_OUT = ("LIGHT: bright clear daylight, neutral white balance: the off-white squares stay off-white, no yellow, orange or "
             "golden cast, no dark or moody grade.")
END = ("The sequins look like real sequins in daylight, nothing more: no added sparkles, glints, stars or light streaks. A real "
       "phone photo, casual and realistic. Vertical 9:16 photo. No text, no captions, no watermark anywhere.")

VID = {
 "V13": {"name": "Cafe", "in": "a cosy cafe: honey wood floor, green velvet armchairs, small round wooden tables, potted plants, framed pictures (like the place photo)",
         "out": "a stone-paved city sidewalk with small round bistro tables and woven chairs outside a cafe (like the place photo)",
         "main": "light-wash straight-leg jeans cropped just above the ankle bone", "sleeve": "A cream chunky-knit sweater cuff",
         "dress": "a black satin slip midi skirt with a soft sheen, hem at mid-calf", "anklet": "a thin gold chain anklet on her right ankle"},
 "V14": {"name": "Bedroom", "in": "a bedroom with sage-green walls, a honey wood floor, a white textured rug, a bed with a grey blanket (like the place photo)",
         "out": "a sunny park with a smooth grey asphalt path through bright green grass and trees (like the place photo)",
         "main": "soft grey cotton joggers cuffed just above the ankle bone", "sleeve": "An oatmeal sweatshirt cuff",
         "dress": "a cream pleated satin midi skirt, hem at mid-calf", "anklet": "a thin gold beaded anklet on her left ankle"},
 "V15": {"name": "Living room", "in": "a living room with a teal velvet sofa, a round wooden coffee table, a cream shaggy rug and a plant (like the place photo)",
         "out": "a narrow cobblestone alley between pastel old-town houses (like the place photo)",
         "main": "chocolate-brown corduroy straight pants cropped just above the ankle bone", "sleeve": "A camel sweater cuff",
         "dress": "a red and black plaid pleated mini skirt, bare legs", "anklet": "a thin gold chain anklet on her right ankle"},
 "V16": {"name": "Loft", "in": "a colourful loft with a red brick wall, a patchwork rug in reds, blues and greens, a white sofa with a pink throw and a mint-green pendant lamp (like the place photo)",
         "out": "a staircase with each step painted a different bright colour, red, orange, yellow, green, blue, purple (like the place photo)",
         "main": "olive cargo pants cuffed just above the ankle bone", "sleeve": "A black ribbed long-sleeve cuff",
         "dress": "white wide-leg linen trousers cropped at the ankle", "anklet": "a thin gold chain anklet on her left ankle"},
 "V17": {"name": "Kitchen", "in": "a bright kitchen with a mint-green wooden table, wicker chairs, a black and white geometric rug, white cabinets and a vase of pink flowers (like the place photo)",
         "out": "a wooden boardwalk through bright green grass under a blue sky (like the place photo)",
         "main": "cream wide-leg sweatpants cropped just above the ankle bone", "sleeve": "A light-blue denim shirt cuff",
         "dress": "a pastel floral midi dress, small pink and blue flowers on cream, hem at mid-calf", "anklet": "a thin gold beaded anklet on her right ankle"},
}

WORN = "She wears the pair: the left shoe on her left foot, the right shoe on her right foot; these are the only two shoes in the scene."
ONE = "Her feet are out of frame; this one shoe is the only shoe in the scene."
PAIR = "No person's feet in frame; the pair are the only two shoes in the scene."

# id: (window, kind, place, outfit, logos, who, scene, motion, camera)
# kind HAND / HAND-FREE; place in/out; outfit main/dress/none; who WORN/ONE/PAIR
SPEC = {
 "V13": [
  ("A", "HAND", "in", None, ["TAB"], ONE, "Close-up at table height: her right hand lifts ONE shoe a few centimetres off a small round wooden cafe table, side view, the toe pointing to the LEFT edge of the frame, the black side tab facing the camera; a plain white cup with no logo soft in the background.", "her hand keeps the same grip on the heel collar and lifts the shoe slowly about 5 cm; the shoe stays side-on, it never turns or flips", "slow push-in"),
  ("B", "HAND-FREE", "in", "main", ["TAB"], WORN, "Low camera at floor level, front three-quarter view of both feet standing side by side on the wood floor beside a green velvet armchair, both toe caps pointing to the lower-LEFT corner, legs visible from the knee down.", "she rises slowly onto her toes and back down once; both feet stay side by side and parallel; no hand appears at any time", "locked off"),
  ("C", "HAND-FREE", "in", "main", ["TAB", "HEEL"], WORN, "Side view at floor level of her right foot standing flat on the wood floor, the toe pointing to the RIGHT edge of the frame, the heel at the left; her left foot behind it, mostly hidden; legs from mid-calf down.", "her feet stay still; no hand appears at any time", "the camera glides slowly along the shoe from the heel toward the toe"),
  ("D", "HAND-FREE", "out", "main", ["TAB"], WORN, "Extreme close-up from above of the toe and lace area of her right shoe on the stone pavement, the toe cap pointing to the lower-LEFT corner, the sequin squares filling most of the frame; only the hem of her jeans at the top edge.", "her foot stays still; no hand appears at any time", "very slow push-in"),
  ("E", "HAND-FREE", "out", "main", ["TAB"], WORN, "Seated at a bistro table outside: low front view under the table of both feet flat on the stone pavement, side by side, both toe caps pointing at the lens, legs from mid-shin down, daylight on the shoes.", "she lifts her right heel slowly and sets it down again; the toes stay planted and pointing at the lens; no hand appears at any time", "locked off"),
  ("F", "HAND-FREE", "out", "dress", ["TAB"], WORN, "Low front view on the stone sidewalk: her legs from mid-calf down in the black satin slip skirt, both toe caps pointing at the lens.", "she takes one small step toward the camera with her right foot; the satin hem moves; no hand appears at any time", "locked off"),
  ("G", "HAND-FREE", "in", "main", ["TAB"], WORN, "Front three-quarter view on the cafe wood floor of both feet side by side, both toe caps pointing to the lower-RIGHT corner, legs from mid-calf down in the jeans.", "she taps her right toe twice on the floor, heel down; no hand appears at any time", "locked off"),
  ("H", "HAND", "in", None, ["INSOLE"], ONE, "Close-up on the cafe table: her left hand holds ONE shoe upright by the outer side with the opening facing the camera, the toe pointing to the TOP edge, the red insole with the white VANS box clearly visible; her thumb rests inside on the red insole at the heel.", "her thumb presses down into the red insole twice and the cushion gives a little; the hand keeps its grip and the shoe never turns or flips", "locked off"),
  ("I", "HAND", "in", None, ["TAB"], ONE, "Side view at table height: her right hand sets ONE shoe down on the wooden cafe table next to a small white plate with a croissant, the toe pointing to the RIGHT edge, the black side tab facing the camera.", "the hand lowers the shoe the last 3 cm onto the table, lets go and rises out of the top of the frame; the shoe stays side-on", "locked off"),
  ("J", "HAND-FREE", "out", "main", ["TAB"], WORN, "Low front view on the stone sidewalk between the bistro chairs: her feet walking toward the camera, both toe caps pointing at the lens, legs from the knee down.", "she walks briskly toward the camera, three real steps, and passes out of the frame on the right; the pavement stays fixed; no hand appears at any time", "locked off, low"),
  ("K", "HAND", "in", None, ["HEEL"], ONE, "Close-up in the cafe: her right hand holds ONE shoe up at chest height by the toe, the heel facing the camera so the black heel stripe and the white OFF THE WALL label are clearly visible, the toe pointing away from the lens.", "the hand lifts the shoe about 5 cm toward the lens; same grip, the heel stays facing the camera, it never turns or flips", "slow push-in"),
 ],
 "V14": [
  ("A", "HAND-FREE", "in", "main", ["TAB"], WORN, "Low front view at rug height: both feet standing side by side on the white textured rug, both toe caps pointing at the lens, legs from mid-calf down in the grey joggers, the bed soft behind.", "her feet stay still and side by side; no hand appears at any time", "slow push-in toward the toes"),
  ("B", "HAND", "in", "main", ["TAB"], WORN, "Seated on the edge of the bed: view from above of her right foot on the rug, the toe pointing to the lower-LEFT corner; her right hand holds the two lace loops of the bow on that shoe, one loop between thumb and finger on each side.", "she pulls the two lace loops gently outward to tighten the bow, once; the foot stays still; the shoe never moves", "locked off"),
  ("C", "HAND", "in", None, ["TAB"], ONE, "Close-up: her right hand holds ONE shoe side-on at chest height in front of the sage-green wall, gripping it round the heel collar, the toe pointing to the RIGHT edge, the black side tab facing the camera.", "the hand keeps the same grip and lifts the shoe about 5 cm; the shoe stays side-on and never turns or flips", "slow push-in"),
  ("D", "HAND-FREE", "in", None, ["TAB"], "No person in frame; this one shoe stands alone on the rug and is the only shoe in the scene.", "Close-up at rug height of ONE shoe standing upright alone on the white textured rug, side view, the toe pointing to the LEFT edge, the sequin squares of the side filling the frame.", "the shoe stays still; no hand appears at any time", "the camera slides slowly along the side from the toe toward the heel"),
  ("E", "HAND-FREE", "in", None, ["TAB", "HEEL"], PAIR, "The pair stand side by side on the honey wood floor in a patch of soft window daylight, three-quarter view, both toes pointing to the LEFT edge, the bed soft behind.", "the shoes stay still; no hand or person appears at any time", "the camera arcs slowly a few degrees to the right"),
  ("F", "HAND-FREE", "in", "dress", ["TAB"], WORN, "Low front view on the wood floor: her legs from mid-calf down in the cream pleated satin skirt, both toe caps pointing at the lens.", "she takes one small step toward the camera; the pleats swing; no hand appears at any time", "locked off"),
  ("G", "HAND-FREE", "out", "main", ["TAB"], WORN, "Side view at path level in the park: her feet in the grey joggers stepping onto the grey asphalt path from the grass, both toes pointing to the RIGHT edge of the frame.", "she takes one step forward along the path; no hand appears at any time", "locked off"),
  ("H", "HAND-FREE", "out", "main", ["TAB"], WORN, "POV looking straight down from her own eyes at both feet on the grey asphalt park path, both toes pointing to the TOP edge of the frame, green grass on both sides.", "she walks forward at a relaxed pace, four real steps, the camera moves with her so the path clearly travels down and out of the bottom of the frame; both feet point forward the whole time; no hand appears at any time", "moves forward with her"),
  ("I", "HAND", "in", None, ["TAB", "HEEL"], ONE, "Low view beside the bed: her right hand picks ONE shoe up off the honey wood floor, gripping it by the heel collar, side view, the toe pointing to the LEFT edge, the black side tab facing the camera.", "the hand lifts the shoe straight up about 15 cm off the floor; same grip, it never turns or flips", "locked off"),
  ("J", "HAND-FREE", "out", "main", ["HEEL"], WORN, "Low view behind her on the park path: both heels facing the camera, both toes pointing to the TOP edge of the frame, the black heel stripes and white heel labels visible.", "she walks quickly away along the path, three real steps; the path stays fixed; no hand appears at any time", "locked off, low"),
  ("K", "HAND", "in", None, ["INSOLE"], ONE, "Close-up above the white rug: her right hand holds ONE shoe by the outer side with the opening tilted toward the camera, the toe pointing to the TOP edge, the red insole with the white VANS box clearly visible.", "the hand tilts the shoe about 10 degrees toward the lens and back; the insole faces the camera the whole time; it never turns or flips", "locked off"),
 ],
 "V15": [
  ("A", "HAND-FREE", "out", "main", ["TAB"], WORN, "Low front view on the cobblestones: her right foot coming down onto the stones in front of her left, both toe caps pointing at the lens, legs from the knee down in the brown corduroy pants.", "her right foot steps down onto the cobblestones toward the camera and plants; no hand appears at any time", "locked off, low"),
  ("B", "HAND", "in", None, ["TAB"], ONE, "Her right hand holds ONE shoe up toward a bright window beside the teal sofa, side-on, gripping it round the heel collar, the toe pointing to the LEFT edge, the black side tab facing the camera.", "the hand raises the shoe slowly about 10 cm, same grip; the shoe stays side-on and never turns or flips", "locked off"),
  ("C", "HAND-FREE", "in", None, ["TAB", "HEEL"], PAIR, "The pair stand side by side on the round wooden coffee table in front of the teal sofa, three-quarter view, both toes pointing to the RIGHT edge.", "the shoes stay still; no hand or person appears at any time", "the camera arcs slowly a few degrees to the left around them"),
  ("D", "HAND", "in", None, ["TAB"], ONE, "Extreme close-up of the toe of ONE shoe resting on the teal velvet sofa cushion, the toe pointing to the lower-LEFT corner; her right thumb and index finger pinch the edge of one raised black sequin.", "the fingers pinch the sequin lightly and let go; the hand moves only a few millimetres; the shoe stays still", "locked off"),
  ("E", "HAND-FREE", "out", "main", ["TAB"], WORN, "Side view at stone level in the cobblestone alley in sunshine: her right foot standing, the toe pointing to the RIGHT edge of the frame, her left foot just behind.", "she lifts her right heel slowly and sets it down; the toes stay on the stones; no hand appears at any time", "locked off"),
  ("F", "HAND-FREE", "out", "dress", ["TAB"], WORN, "Front view on the cobblestones: her bare legs from mid-thigh down under the red and black plaid mini skirt, both toe caps pointing at the lens.", "she shifts her weight from one foot to the other once; no hand appears at any time", "locked off"),
  ("G", "HAND-FREE", "in", "main", ["TAB"], WORN, "Seated on the teal sofa: low front view of both feet flat on the cream shaggy rug, both toe caps pointing at the lens, legs from the knee down in the brown corduroy pants.", "she slides her right foot forward on the rug a few centimetres; no hand appears at any time", "locked off"),
  ("H", "HAND-FREE", "out", "main", ["TAB"], WORN, "Side view at ankle height in the cobblestone alley: both feet walking, both toes pointing to the RIGHT edge of the frame.", "she walks at a relaxed pace, three real steps; the camera tracks beside her at the same speed so the cobblestones move past; no hand appears at any time", "tracks sideways with her"),
  ("I", "HAND", "in", None, ["TAB", "HEEL"], ONE, "Her right hand takes ONE shoe off a wooden bookshelf shelf, gripping it by the heel collar, side view, the toe pointing to the LEFT edge, the black side tab facing the camera; books beside it.", "the hand slides the shoe off the shelf toward the camera about 10 cm; same grip, it never turns or flips", "locked off"),
  ("J", "HAND-FREE", "out", "main", ["TAB"], WORN, "Low side view in the cobblestone alley: her feet in quick steps across the frame, both toes pointing to the LEFT edge.", "she hurries across the frame from right to left, three quick steps; the cobblestones stay fixed; no hand appears at any time", "locked off, low"),
  ("K", "HAND", "in", None, ["TAB"], ONE, "Close-up beside the teal sofa: her right hand holds ONE shoe near the lens, side-on, gripping it round the heel collar, the toe pointing to the RIGHT edge, the black side tab large in frame.", "the hand keeps the same grip and brings the shoe a little closer to the lens; it never turns or flips", "slow push-in"),
 ],
 "V16": [
  ("A", "HAND-FREE", "out", "main", ["TAB"], WORN, "Side view at step level on the painted rainbow staircase: her right foot on a yellow step, her left foot on the orange step below, both toes pointing to the LEFT edge of the frame, legs from the knee down in olive cargo pants.", "she steps up one step with her left foot; no hand appears at any time", "locked off"),
  ("B", "HAND", "in", None, ["HEEL"], "Her feet are out of frame; the two held shoes are the only shoes in the scene.", "In front of the red brick wall: her two hands each hold ONE shoe of the pair by the toe, the left shoe in her left hand and the right shoe in her right hand, side by side, both heels facing the camera so both black heel stripes and white OFF THE WALL labels are clearly visible, both toes pointing away from the lens.", "both hands raise the pair together about 10 cm, same grips; the heels keep facing the camera and the shoes never turn or flip", "locked off"),
  ("C", "HAND-FREE", "in", "main", ["TAB"], WORN, "High three-quarter view of both feet standing side by side on the patchwork rug, both toes pointing to the lower-RIGHT corner, legs from the knee down in olive cargo pants.", "her feet stay still; no hand appears at any time", "the camera cranes slowly down toward the shoes"),
  ("D", "HAND-FREE", "in", None, ["TAB"], "No person in frame; this one shoe stands alone on the rug and is the only shoe in the scene.", "Extreme close-up at rug height of ONE shoe standing alone on the patchwork rug, three-quarter view, the toe pointing to the lower-RIGHT corner, the sequin squares of the toe filling the frame.", "the shoe stays still; no hand appears at any time", "very slow push-in"),
  ("E", "HAND-FREE", "out", "main", ["TAB"], WORN, "Seated on the rainbow staircase: side view of both feet resting on the step below, a green step, both toes pointing to the LEFT edge, legs from mid-shin down.", "she lifts her right heel slowly and sets it down; no hand appears at any time", "locked off"),
  ("F", "HAND-FREE", "in", "dress", ["TAB"], WORN, "Low front view in front of the red brick wall: her legs from mid-shin down in white wide-leg linen trousers, both toe caps pointing at the lens.", "she takes one small step toward the camera; the linen moves; no hand appears at any time", "locked off"),
  ("G", "HAND-FREE", "in", "main", ["TAB"], WORN, "Front view of both feet on the patchwork rug, both toe caps pointing at the lens, legs from mid-calf down in olive cargo pants.", "she pivots her right foot on its heel a little to the right and back; no hand appears at any time", "locked off"),
  ("H", "HAND-FREE", "out", "main", ["TAB"], WORN, "Low view from the bottom of the rainbow staircase: her feet coming down the painted steps toward the camera, both toe caps pointing at the lens.", "she walks down two steps toward the camera at a relaxed pace; the steps stay fixed; no hand appears at any time", "locked off, low"),
  ("I", "HAND", "in", None, ["TAB"], ONE, "Her right hand picks ONE shoe up off the white sofa next to the pink throw, gripping it round the heel collar, side view, the toe pointing to the RIGHT edge, the black side tab facing the camera.", "the hand lifts the shoe straight up about 15 cm; same grip, it never turns or flips", "locked off"),
  ("J", "HAND-FREE", "out", "main", ["HEEL"], WORN, "Low view from behind on the rainbow staircase: both heels facing the camera, both toes pointing to the TOP edge of the frame, the black heel stripes and white heel labels visible.", "she runs quickly up three painted steps away from the camera; no hand appears at any time", "locked off, low"),
  ("K", "HAND", "in", None, ["INSOLE"], ONE, "Close-up in front of the red brick wall: her right hand holds ONE shoe by the outer side with the opening toward the camera, the toe pointing to the TOP edge, the red insole with the white VANS box clearly visible.", "the hand tilts the shoe about 10 degrees toward the lens and back; the insole faces the camera the whole time; it never turns or flips", "slow push-in"),
 ],
 "V17": [
  ("A", "HAND", "in", None, ["TAB"], ONE, "Close-up: her right hand holds ONE shoe very close to the lens, side-on, gripping it round the heel collar, the toe pointing to the LEFT edge, the black side tab large in frame, the bright kitchen soft behind.", "the hand moves the shoe slowly back away from the lens, revealing the kitchen; same grip, it never turns or flips", "locked off"),
  ("B", "HAND-FREE", "in", "main", ["TAB"], WORN, "Side view at floor level of both feet standing on the black and white geometric rug, both toes pointing to the LEFT edge of the frame, legs from mid-calf down in cream wide-leg sweatpants.", "she rises onto her toes and back down once; no hand appears at any time", "locked off"),
  ("C", "HAND-FREE", "out", "main", ["TAB"], WORN, "Low front view on the wooden boardwalk: her feet walking toward the camera, both toe caps pointing at the lens, legs from the knee down, green grass on both sides.", "she walks toward the camera at a relaxed pace, three real steps; the boards stay fixed; no hand appears at any time", "locked off, low"),
  ("D", "HAND", "in", None, ["TAB"], ONE, "Extreme close-up of the toe of ONE shoe standing on the mint-green table, the toe pointing to the lower-RIGHT corner; her right index fingertip points at the sequin squares about 2 cm above them, not touching.", "the fingertip holds still above the sequins, then pulls back slightly; it never touches or sweeps across the shoe", "very slow push-in"),
  ("E", "HAND-FREE", "in", None, ["TAB", "HEEL"], PAIR, "The pair stand side by side on the mint-green wooden table in bright window daylight next to the vase of pink flowers, three-quarter view, both toes pointing to the RIGHT edge.", "the shoes stay still; no hand or person appears at any time", "slow push-in"),
  ("F", "HAND-FREE", "out", "dress", ["TAB"], WORN, "Low front view on the boardwalk: her legs from mid-shin down under the pastel floral midi dress, both toe caps pointing at the lens.", "she takes one small step toward the camera; the hem moves; no hand appears at any time", "locked off"),
  ("G", "HAND-FREE", "in", "main", ["TAB"], WORN, "Front view of both feet on the geometric rug, both toe caps pointing at the lens, legs from mid-calf down in cream wide-leg sweatpants.", "she shifts her weight from foot to foot once; no hand appears at any time", "locked off"),
  ("H", "HAND-FREE", "out", "main", ["TAB"], WORN, "POV looking straight down from her own eyes at both feet on the wooden boardwalk, both toes pointing to the TOP edge of the frame.", "she walks forward at a relaxed pace, four real steps, the camera moves with her so the boards clearly travel down and out of the bottom of the frame; both feet point forward the whole time; no hand appears at any time", "moves forward with her"),
  ("I", "HAND", "in", None, ["TAB", "HEEL"], ONE, "Her right hand lifts ONE shoe off the seat of a wicker chair, gripping it by the heel collar, side view, the toe pointing to the RIGHT edge, the black side tab facing the camera.", "the hand lifts the shoe straight up about 15 cm; same grip, it never turns or flips", "locked off"),
  ("J", "HAND-FREE", "out", "main", ["HEEL"], WORN, "Low view behind her on the boardwalk: both heels facing the camera, both toes pointing to the TOP edge of the frame, the black heel stripes and white heel labels visible.", "she walks quickly away along the boards, three real steps; the boards stay fixed; no hand appears at any time", "locked off, low"),
  ("K", "HAND", "in", None, ["INSOLE"], ONE, "Close-up next to the mint-green table: her right hand holds ONE shoe by the outer side with the opening toward the camera, the toe pointing to the TOP edge, the red insole with the white VANS box clearly visible, the pink flowers soft behind.", "the hand tilts the shoe about 10 degrees toward the lens and back; the insole faces the camera the whole time; it never turns or flips", "locked off"),
 ],
}


def still_prompt(v, place, outfit, logos, who, scene, kind):
    refs = ["SHEET", "SEQ"] + logos
    legs = outfit is not None
    if legs: refs.append("SKIN")
    if kind == "HAND": refs.append("HAND")
    paths = [R[k][0] for k in refs] + [f"refs/places/{v}_{place}.jpg"]
    intro = " ".join(f"Image {i} = {R[k][1]}." for i, k in enumerate(refs, 1)) + f" Image {len(refs) + 1} = the real place."
    d = VID[v]
    parts = [intro, "SCENE: " + scene, who]
    side = re.search(r"toes? pointing to the (LEFT|RIGHT) edge", scene)
    if side and "side tab facing the camera" in scene and who == ONE:
        parts.append(f"The held shoe is the {side.group(1)} shoe of the pair, so its outer side with the black tab faces the camera.")
    elif side and who == PAIR:
        parts.append(f"The shoe nearer the camera is the {side.group(1)} shoe, so its outer side with the black tab faces the camera.")
    if legs:
        clothes = d["dress"] if outfit == "dress" else d["main"]
        parts.append(f"HER: medium brown skin exactly like the skin reference; {clothes}; bare ankles; {d['anklet']}.")
    if kind == "HAND":
        parts.append(HAND.format(sleeve=d["sleeve"]))
    else:
        parts.append("No hands, arms or fingers anywhere in the frame.")
    parts += [SHOE, "PLACE: " + d[place] + ".", LIGHT_IN if place == "in" else LIGHT_OUT, END]
    return " ".join(parts), paths


def clip_prompt(v, sid, logos, who, motion, camera, kind, place, outfit, scene):
    n = 2; lines = []
    d = VID[v]
    keep = "its place, light and framing"
    if outfit: keep += ", her skin, " + (d["dress"] if outfit == "dress" else d["main"]) + " and anklet"
    if kind == "HAND": keep += ", her hand, nails, rings, blue band and bracelets"
    lines.append(f"Recreate image 1 exactly as the first frame: keep {keep} exactly.")
    for k in logos:
        lines.append(f"Image {n} is {R[k][1]}: it stays on the shoe the whole clip and matches image {n} letter for letter and colour for colour.")
        n += 1
    lines.append(f"Image {n} is the product sheet: keep this exact shoe shape, size, checkerboard and colours; only the black squares carry sequins; no added marks, no extra text.")
    lines.append(who)
    toes = re.findall(r"(?:both )?toe(?: caps?)?s? pointing (?:to|at|away from) [^,;.]+", scene)
    if toes: lines.append("Toe direction stays as in image 1 the whole clip: " + "; ".join(dict.fromkeys(toes)) + ".")
    lines.append(f"Motion: {motion}.")
    lines.append(f"Camera: {camera}.")
    if kind == "HAND": lines.append("Exactly the hands in image 1, five fingers each, whole wrists.")
    lines.append(f"Vertical 9:16 phone footage, bright neutral {'window daylight' if place == 'in' else 'daylight'}, realistic. "
                 "No sparkle effects, no music, no voice, no captions, no on-screen text.")
    return " ".join(lines), [f"stills/{sid}.png"] + [R[k][0] for k in logos] + [R["SHEET"][0]]


def main():
    out = {}
    for v, rows in SPEC.items():
        for (w, kind, place, outfit, logos, who, scene, motion, camera) in rows:
            sid = f"{v}{w}"
            s, sr = still_prompt(v, place, outfit, logos, who, scene, kind)
            c, cr = clip_prompt(v, sid, logos, who, motion, camera, kind, place, outfit, scene)
            out[sid] = {"video": v, "beat": w, "window": list(WIN[w]), "line": LINE[w], "kind": kind,
                        "place": f"{v}_{place}", "outfit": outfit, "scene": scene, "motion": motion,
                        "still": s, "still_refs": sr, "clip": c, "clip_refs": cr, "model": "omni-4s"}
    (J / "shots.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    print(len(out), "shots")


if __name__ == "__main__":
    main()
