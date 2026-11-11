"""Builds shots.json for Vans sequin V18-V37 (Grace), 2026-11-11: 20 music-only videos of 16 s, 5 shots each (3.2 s).
Ask (Ralph 2026-11-11): 3 videos from each of Grace's 6 links (same beats, new look) + 2 mixing the best beats.
Written with prompt-master (Ralph's stack): view, framing and toe direction first; numbered refs named by what they ARE;
a real close-up for every logo the frame shows; who wears/holds which shoe; one grip, no turn; no effect words, no text.
Shared truth blocks reuse ugc/vans-vo5 (product_truth.json facts, real photos) plus every REMOVED.md lesson.
  python3 tools/make_shots.py   -> shots.json + prompts/<ID>_sd.txt (Seedance first-frame clip prompts)"""
import json, re
from pathlib import Path

J = Path(__file__).resolve().parent.parent

R = {"SHEET": ("refs/product_sheet.png", "the real shoe from every side (product sheet: pair, side, top with red insole, gum waffle sole, back, sequin close-up)"),
     "SEQ": ("refs/shoe_closeup.jpg", "the real sequin squares, side tab and laces up close"),
     "TAB": ("refs/real_vans_tab.jpg", "the real woven side tab: a small BLACK tab with white VANS letters, sewn flat on the outer side"),
     "HEEL": ("refs/real_heel_label.jpg", "the real back of the shoe: the vertical BLACK heel stripe with white stitching and the small WHITE 'OFF THE WALL' skateboard label with black print on the off-white sidewall"),
     "INSOLE": ("refs/real_insole_logo.jpg", "the real insole: deep RED with a WHITE rectangle holding the red VANS skateboard-tail logo"),
     "SOLE": ("refs/real_top_sole.jpg", "the real outsole: gum-brown waffle pattern"),
     "SKIN": ("refs/grace/f_23.5.jpg", "Grace's real ankles in the shoes: her exact medium-deep brown skin tone and thin gold anklet (ignore the pavement and her pants)"),
     "HAND": ("refs/grace/f_11.5.jpg", "Grace's real hand holding the shoe: her exact medium-deep brown skin tone, nails, rings and bracelets (ignore the street)")}

PLACE = {"street": ("refs/places/street.jpg", "a stone-paved sidewalk outside a cafe with small round tables, slatted chairs in pale blue and honey wood, potted plants and a chalkboard (like the place photo)"),
         "bedroom": ("refs/places/roomL_wide.jpg", "Grace's bright cream bedroom: cream upholstered bed, white nightstands, a curved cream bench, cream marble floor with a soft cream rug, pleated cream curtains (like the place photo)"),
         "car": ("refs/places/car.jpg", "inside a car with cream-white quilted leather seats, a black dashboard and door panels, daylight through the windows (like the place photo)"),
         "living": ("refs/places/living.jpg", "a bright living room: a round light-wood coffee table with a clear glass mug, a small jar candle and a vase of white and yellow daffodils, a grey sofa with cream cushions, sheer white curtains (like the place photo)"),
         "curb": ("refs/places/car.jpg", "a parked car with its door open onto a stone-paved cafe sidewalk: cream-white quilted leather seats, a black door sill, the sidewalk and cafe chairs outside (like the place photo)")}

SHOE = ("THE SHOE must match the product sheet and every close-up exactly, letter for letter and colour for colour: the real "
        "Vans Premium Authentic low-top lace-up sneaker in sequin checkerboard. A black and off-white checkerboard where ONLY the "
        "black squares are covered in raised black sequins and the off-white squares are plain woven canvas; black leather binding "
        "round the collar with white stitching; a black tongue; natural tan canvas lining; flat black cotton laces through four pairs "
        "of black eyelets; a small BLACK woven tab with white VANS letters on the outer side; a vertical black heel stripe; a chunky "
        "smooth off-white rubber sidewall with a small WHITE 'OFF THE WALL' label at the back; a deep RED insole with a WHITE "
        "rectangle holding the red VANS logo; a gum-brown waffle sole. The toe box is the same checkerboard as the rest of the upper, "
        "never a solid black toe or panel: every black square is its own square with off-white canvas squares between, the sequins never merge into a solid black area at the toe, heel or sides. The sidewall is OFF-WHITE all the way round; gum brown shows ONLY on the bottom tread, never on the side. The laces are BLACK. True size: an adult women's sneaker about 25 cm long, exactly the length of her own foot. "
        "No other logos, no added marks, no extra text.")
HAND = ("HER HAND is Grace's real hand, exactly like the hand reference: the same medium-deep brown skin tone, slim fingers, "
        "medium-length pink nails with white French tips, a thin blue silicone RING on one finger (a ring, never a wristband: nothing blue on her wrist), a silver heart ring, a chunky gold "
        "watch-style link bracelet and thin gold chain bracelets. Never lighter or darker skin than the reference. {sleeve} at the "
        "wrist. The hand enters from the frame edge, whole wrist visible, five fingers, and it GRIPS the shoe: thumb on one side, "
        "fingers curled round the other.")
LIGHT = ("LIGHT: bright soft daylight, neutral white balance: the off-white squares stay off-white, no yellow, orange or golden cast, "
         "no dark or moody grade.")
END = ("The sequins look like real sequins in daylight, nothing more: no added sparkles, glints or light streaks. A real phone "
       "photo, casual and realistic. Vertical 9:16 photo. No text, no captions, no watermark anywhere.")
WORN = ("She wears the pair: the left shoe on her left foot, the right shoe on her right foot, both feet fully inside the laced "
        "shoes so her feet hide the insoles; these are the only two shoes in the scene. Her face is never in the frame: the frame stops below her chest.")
HOLD = ("Her LEFT foot wears the LEFT shoe, fully inside it; her RIGHT hand holds the RIGHT shoe of the pair, empty; these are the "
        "only two shoes in the scene.")
PAIR = "The pair stands side by side, empty, laced; these are the only two shoes in the scene; no feet, no hands, no people."
ONE = "This one empty shoe is the only shoe in the scene; no feet, no hands, no people."

LOOK = {"TAB": ", the black side tab with white VANS letters", "SEQ": ", plain off-white canvas squares",
        "HEEL": ", the black heel stripe and the white OFF THE WALL label with black print",
        "INSOLE": ", the deep red insole with its white VANS rectangle", "SOLE": ", the gum-brown waffle sole"}

# Outfit per video: legs + sleeve cuff (each video its own look, hard rule 6)
OUT = ["light-wash skinny jeans with ripped knees, cropped at the ankle|A cream chunky-knit sweater cuff",
       "black leggings|An oatmeal sweatshirt cuff",
       "cream wide-leg trousers cropped just above the ankle|A white ribbed knit cuff",
       "dark-wash straight jeans cropped at the ankle|A heather-grey hoodie cuff",
       "a black satin midi skirt, bare ankles|A black fine-knit cardigan cuff",
       "olive cargo pants cuffed above the ankle|A white long-sleeve tee cuff",
       "light grey joggers cuffed above the ankle|A soft pink sweatshirt cuff",
       "light-blue mom jeans cuffed above the ankle|A camel sweater cuff",
       "black wide-leg trousers cropped at the ankle|A cream blazer cuff",
       "white straight jeans cropped at the ankle|A navy striped shirt cuff"]

# Beat library: (kind, refs, who, scene, motion, camera)
B = {
 # Link 1: hand turns the held shoe over her legs, ground below (street)
 "1a": ("HAND", ["TAB"], HOLD, "Seated on the stone sidewalk: view from above of her legs stretched out on the pavement, her left foot in its shoe at the top-left; her right hand holds the RIGHT shoe above her shins in side view, the toe pointing to the TOP-LEFT corner, the black side tab facing the camera.", "her hand keeps the same grip on the heel collar and lifts the shoe slowly about 5 cm toward the lens; the shoe never turns or flips", "handheld, very slight drift"),
 "1b": ("HAND", ["TAB"], HOLD, "Seated on the sidewalk, view from above: her right hand holds the RIGHT shoe flat above her knees, top view, the laces and black tongue facing the camera, the toe pointing to the TOP edge of the frame; her left shoe on the pavement behind.", "her hand keeps one grip on the side of the shoe and brings it a little closer to the lens; the shoe never turns", "handheld, slow push-in"),
 "1c": ("HAND", ["INSOLE", "TAB"], HOLD, "Seated on the sidewalk, view from above: her right hand holds the RIGHT shoe tilted so the camera looks down into the collar at the deep red insole with its white VANS rectangle, the toe pointing to the TOP edge; her left shoe on the pavement behind.", "her hand keeps one grip on the heel and lifts the shoe slowly; the angle stays the same", "handheld, slight drift"),
 "1d": ("HAND-FREE", ["TAB"], WORN, "Seated on the sidewalk: view from above of her legs crossed at the ankles on the stone pavement, both shoes on, both toe caps pointing to the TOP-RIGHT corner, the side tabs facing the camera.", "she bounces her top foot gently twice; no hand appears at any time", "locked off"),
 "1e": ("HAND-FREE", ["TAB"], ONE, "Low close-up at pavement level: the RIGHT shoe standing on the stone sidewalk beside a cafe chair leg, side view, the toe pointing to the LEFT edge of the frame, the black side tab facing the camera.", "the shoe stays still; no hand appears at any time", "very slow push-in"),
 # Link 2: seated on the rug in the bedroom, one continuous wearing moment
 "2a": ("HAND", ["TAB"], WORN, "Seated on the cream rug: view from above of her right foot in front of her, the toe pointing to the lower-LEFT corner, the outer side with the black side tab facing the camera; her right index finger touches the side tab; her left foot behind.", "her index finger taps the side tab twice; the foot stays still", "handheld, very slight drift"),
 "2b": ("HAND-FREE", ["TAB", "SOLE"], WORN, "Seated on the cream rug: front three-quarter view of her right foot, the toe pointing to the lower-LEFT corner, her left foot beside it.", "she lifts her right heel and tilts the foot so the side of the gum waffle sole shows, then sets it down; no hand appears at any time", "locked off"),
 "2c": ("HAND-FREE", ["TAB"], WORN, "Wide view on the cream rug: she sits with knees bent, both feet flat in front of her, both toe caps pointing at the lens, the bed soft behind.", "she taps her two toes together once; no hand appears at any time", "slow push-in"),
 "2d": ("HAND", ["TAB"], WORN, "Seated on the cream rug: view from above of her right foot, toe pointing to the lower-LEFT corner; her right hand pinches the two loops of the tied black bow on that worn shoe.", "she pulls the bow loops gently tight with one grip; the shoe stays still", "handheld"),
 "2e": ("HAND-FREE", ["TAB"], PAIR, "Low view on the cream rug: the pair side by side, front three-quarter, both toe caps pointing to the lower-LEFT corner, the bed soft behind.", "the shoes stay still; no hand appears at any time", "slow dolly in at rug level"),
 # Link 3: in the car, the held shoe shown up close, foot on the dash
 "3a": ("HAND", ["TAB"], HOLD, "In the car passenger seat: her left leg rests up with the left shoe near the dashboard at the top of the frame; her right hand holds the RIGHT shoe in front of the black dashboard, side view, the toe pointing to the LEFT edge, the black side tab facing the camera.", "her hand keeps one grip on the heel collar and moves the shoe slowly closer to the lens; it never turns", "handheld, slight drift"),
 "3b": ("HAND", ["TAB"], HOLD, "In the car: close-up of the RIGHT shoe held in her right hand, front view, the toe cap pointing at the lens, the laces and tongue above, the cream seat soft behind.", "her hand keeps one grip and lifts the shoe slowly a few centimetres; it never turns", "handheld, slow push-in"),
 "3c": ("HAND", ["HEEL"], HOLD, "In the car: close-up of the RIGHT shoe held in her right hand, back view: the black heel stripe and the white OFF THE WALL label facing the camera, the toe pointing to the TOP edge, the black dashboard soft behind.", "her hand keeps one grip and lifts the shoe slowly; it never turns", "handheld"),
 "3d": ("HAND-FREE", ["TAB"], WORN, "In the car passenger seat: both feet up on the black dashboard, crossed at the ankles, both shoes on, both toe caps pointing to the TOP-RIGHT corner, the side tabs facing the camera, the windshield light behind.", "she sways her crossed feet gently once; no hand appears at any time", "locked off"),
 "3e": ("HAND-FREE", ["TAB"], ONE, "Close-up of the RIGHT shoe resting on the cream quilted leather seat, side view, the toe pointing to the RIGHT edge, the black side tab facing the camera.", "the shoe stays still; no hand appears at any time", "very slow push-in along the sidewall"),
 # Link 4: styled close-ups at the coffee table (kept bright)
 "4a": ("HAND", ["TAB"], HOLD, "At the coffee table: her right hand holds the RIGHT shoe above the light-wood table, side view, the toe pointing to the LEFT edge, the black side tab facing the camera; the daffodils and candle soft behind; her left foot in its shoe on the rug at the bottom edge.", "her hand keeps one grip on the heel collar and lifts the shoe slowly a few centimetres; it never turns", "handheld"),
 "4b": ("HAND-FREE", ["SEQ"], ONE, "Extreme close-up of the toe of one shoe resting on the light-wood coffee table: the sequin-covered black squares and plain off-white canvas squares fill the frame, the toe pointing to the lower-LEFT corner.", "the shoe stays still; no hand appears at any time", "very slow slide across the squares"),
 "4c": ("HAND", ["INSOLE"], HOLD, "At the coffee table: her right hand holds the RIGHT shoe tilted so the camera looks down into the collar at the deep red insole with its white VANS rectangle, the toe pointing to the TOP edge; the table soft below.", "her hand keeps one grip and lifts the shoe slowly; the angle stays the same", "handheld"),
 "4d": ("HAND-FREE", ["TAB"], ONE, "The RIGHT shoe standing on the light-wood coffee table beside the glass mug, side view, the toe pointing to the LEFT edge, the black side tab facing the camera, daffodils soft behind.", "the shoe stays still; no hand appears at any time", "slow push-in toward the side tab"),
 "4e": ("HAND-FREE", ["TAB"], WORN, "Seated on the sofa: low view of both feet resting on the rug beside the coffee table, both shoes on, both toe caps pointing to the lower-LEFT corner.", "she crosses her right ankle over her left slowly; no hand appears at any time", "locked off"),
 # Link 5: seated in the open car door, held shoe beside the worn one
 "5a": ("HAND", ["TAB"], HOLD, "Seated sideways in the open car door: her left foot in its shoe rests on the black door sill; her right hand holds the RIGHT shoe beside it, side view, both toes pointing to the LEFT edge, the black side tabs facing the camera.", "her hand keeps one grip on the heel collar and lifts the held shoe slowly a few centimetres; it never turns", "handheld"),
 "5b": ("HAND", ["INSOLE"], HOLD, "Seated in the open car door: view from above, her right hand holds the RIGHT shoe tilted so the camera looks into the collar at the deep red insole, the toe pointing to the TOP edge; her left foot in its shoe on the sill below.", "her hand keeps one grip and lifts the shoe slowly; the angle stays the same", "handheld"),
 "5c": ("HAND", ["TAB"], HOLD, "Seated in the open car door: view from above, her right hand holds the RIGHT shoe flat above her left foot, top view, the laces and black tongue facing the camera, the toe pointing to the TOP edge.", "her hand keeps one grip and moves the shoe slowly toward the lens; it never turns", "handheld"),
 "5d": ("HAND-FREE", ["TAB"], WORN, "Seated in the open car door: view from above of both feet on the black door sill, both shoes on, both toe caps pointing to the lower-LEFT corner, the sidewalk below.", "she taps her right toe twice on the sill; no hand appears at any time", "locked off"),
 "5e": ("HAND-FREE", ["TAB"], WORN, "Low view from the sidewalk: her feet step out of the open car door onto the stone pavement, both toe caps pointing at the lens.", "she sets her right foot down on the pavement, then her left, real weight; nothing slides; no hand appears at any time", "locked off, low"),
 # Link 6: car + sidewalk, walking
 "6a": ("HAND-FREE", ["TAB"], WORN, "Low view from the sidewalk: her legs swing out of the open car door, both shoes on, both toe caps pointing at the lens, the cream seat behind.", "she plants both feet on the stone pavement, one after the other; nothing slides; no hand appears at any time", "locked off, low"),
 "6b": ("HAND", ["TAB"], HOLD, "Standing at the open car door: her right hand holds the RIGHT shoe against the black door panel, side view, the toe pointing to the RIGHT edge, the black side tab facing the camera; her left shoe on her foot at the bottom edge.", "her hand keeps one grip and lifts the shoe slowly; it never turns", "handheld"),
 "6c": ("HAND-FREE", ["TAB"], WORN, "Low front view on the stone sidewalk: her feet walking toward the camera, both toe caps pointing at the lens, legs from the knee down, the car and cafe chairs soft behind.", "she walks toward the camera, three real steps; each heel lifts clearly off the pavement and each foot lands with weight; nothing slides; no hand appears at any time", "locked off, low"),
 "6d": ("HAND", ["SOLE"], HOLD, "Standing by the car: her right hand holds the RIGHT shoe sole-up toward the camera, the gum-brown waffle sole facing the lens, the toe pointing to the TOP edge; the sidewalk soft below.", "her hand keeps one grip on the heel and lifts the shoe slowly; it never turns or flips", "handheld"),
 "6e": ("HAND-FREE", ["TAB"], WORN, "Standing on the sidewalk beside the car: side view of both feet, her right foot crossed in front of her left, both toes pointing to the LEFT edge.", "she lifts her right heel and sets it down once; no hand appears at any time", "locked off"),
}

# Per video: setting, beat order (each of a link's 3 videos has its own order, outfit and framing note)
V = {
 "V18": ("street", ["1a", "1b", "1d", "1c", "1e"], "close and low, the cafe chairs at the left"),
 "V19": ("street", ["1d", "1c", "1a", "1e", "1b"], "a little wider, the potted plants at the right"),
 "V20": ("street", ["1e", "1a", "1c", "1b", "1d"], "high angle, the chalkboard soft behind"),
 "V21": ("bedroom", ["2a", "2b", "2d", "2c", "2e"], "on the rug at the foot of the bed"),
 "V22": ("bedroom", ["2c", "2a", "2e", "2b", "2d"], "on the rug beside the curved cream bench"),
 "V23": ("bedroom", ["2e", "2d", "2a", "2c", "2b"], "on the rug by the pleated curtains"),
 "V24": ("car", ["3a", "3b", "3c", "3d", "3e"], "passenger seat, dashboard side"),
 "V25": ("car", ["3d", "3a", "3e", "3c", "3b"], "passenger seat, window side"),
 "V26": ("car", ["3e", "3c", "3b", "3a", "3d"], "rear seat, seat-back side"),
 "V27": ("living", ["4b", "4a", "4c", "4d", "4e"], "the table by the window"),
 "V28": ("living", ["4a", "4d", "4b", "4e", "4c"], "the table in front of the sofa"),
 "V29": ("living", ["4e", "4c", "4d", "4b", "4a"], "the table by the flowers"),
 "V30": ("curb", ["5a", "5b", "5c", "5d", "5e"], "driver door"),
 "V31": ("curb", ["5d", "5a", "5e", "5c", "5b"], "passenger door"),
 "V32": ("curb", ["5c", "5e", "5b", "5a", "5d"], "rear door"),
 "V33": ("curb", ["6a", "6b", "6c", "6d", "6e"], "driver side, morning light"),
 "V34": ("curb", ["6c", "6a", "6e", "6b", "6d"], "passenger side, near the cafe tables"),
 "V35": ("curb", ["6b", "6e", "6a", "6d", "6c"], "back of the car, near the plants"),
 "V36": ("curb", ["6a", "5a", "3b", "6c", "6d"], "mix: L6 step-out + L5 door hold + L3 toe close-up + L6 walk"),
 "V37": ("bedroom", ["2a", "4b", "1c", "2e", "2c"], "mix: L2 tab tap + L4 sequin macro + L1 insole + L2 pair"),
}
# Beats re-used outside their own setting get the setting words swapped
SWAP = {"bedroom": [("light-wood coffee table", "cream rug"), ("stone sidewalk", "cream rug"), ("pavement", "rug"), ("sidewalk", "rug"), ("daffodils and candle", "bed")],
        "curb": [("In the car passenger seat", "Seated in the open car door"), ("in front of the black dashboard", "in front of the black door panel"), ("the cream seat soft behind", "the sidewalk soft behind"), ("In the car:", "At the open car door:")]}


def still(sid, place, beat, outfit, note):
    kind, logos, who, scene, motion, cam = B[beat]
    for a, b in SWAP.get(place, []): scene = scene.replace(a, b)
    legs, sleeve = outfit.split("|")
    refs, lines, n = [], [], 0
    n += 1; refs.append(R["SHEET"][0]); lines.append(f"Image {n} = {R['SHEET'][1]}.")
    for k in logos:
        n += 1; refs.append(R[k][0]); lines.append(f"Image {n} = {R[k][1]}.")
    if kind == "HAND":
        n += 1; refs.append(R["HAND"][0]); lines.append(f"Image {n} = {R['HAND'][1]}.")
    if who in (WORN, HOLD):
        n += 1; refs.append(R["SKIN"][0]); lines.append(f"Image {n} = {R['SKIN'][1]}.")
    n += 1; refs.append(PLACE[place][0]); lines.append(f"Image {n} = the real place.")
    body = [f"VIEW AND FRAMING FIRST: {scene}", who, SHOE]
    if kind == "HAND": body.append(HAND.replace("{sleeve}", sleeve))
    if who in (WORN, HOLD): body.append(f"HER LEGS: {legs}; GRACE'S SKIN on every ankle, foot and hand: the exact medium-deep brown tone of the skin reference, never lighter or darker; a thin gold anklet.")
    body += [f"PLACE: {PLACE[place][1]}, {note}.", LIGHT, END]
    toes = re.findall(r"(?:both )?toe(?: caps?)?s? pointing (?:to|at) [^,;.]+", scene)
    toe = ("Toe direction stays exactly as in the first frame: " + "; ".join(dict.fromkeys(toes)) + ". ") if toes else ""
    clip = (f"{motion}. Camera: {cam}. {toe}The shoe keeps exactly the look of the first frame the whole clip: checkerboard with "
            "sequins only on the black squares" + "".join(LOOK[k] for k in logos) + "; it never turns, flips or changes shape. "
            + ("Her hand keeps the same grip the whole clip, five fingers, whole wrist; the blue band stays a ring on her finger. " if kind == "HAND" and "grip" in motion else "")
            + ("Her hand stays whole, five fingers, whole wrist. " if kind == "HAND" and "grip" not in motion else "")
            + ("The feet stay in the shoes; nothing slides. " if who == WORN else "")
            + ("Her skin stays the same medium-deep brown tone as the first frame. " if kind == "HAND" or who in (WORN, HOLD) else "") + "Bright neutral daylight, realistic phone footage, 9:16. No sparkle effects, no text, no captions, no music, no voice.")
    return {"kind": kind, "beat": beat, "place": place, "still": " ".join(lines + body), "still_refs": refs, "clip": clip}


def main():
    S = {}
    for vi, (vid, (place, beats, note)) in enumerate(V.items()):
        outfit = OUT[vi % len(OUT)]
        for si, beat in enumerate(beats):
            sid = f"{vid}S{si + 1}"
            S[sid] = {"video": vid, "window": [round(si * 3.2, 1), round(si * 3.2 + 3.2, 1)], **still(sid, place, beat, outfit, note)}
    (J / "shots.json").write_text(json.dumps(S, indent=1))
    P = J / "prompts"; P.mkdir(exist_ok=True)
    for sid, s in S.items(): (P / f"{sid}_sd.txt").write_text(s["clip"] + "\n")
    hf = sum(s["kind"] == "HAND-FREE" for s in S.values())
    print(len(S), "shots,", hf, "hand-free,", len(S) - hf, "hand; max refs", max(len(s["still_refs"]) for s in S.values()))


if __name__ == "__main__":
    main()
