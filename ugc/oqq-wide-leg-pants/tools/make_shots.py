"""Builds shots.json (still + clip prompts, prompt-master 'Ralph's stack') from shared blocks, so a look change is one edit."""
import json
PANTS = {
 "black": "TRUE BLACK",
 "brown": "DARK CHOCOLATE BROWN (exactly the brown in images 1 and 2)",
}
def pants(c):
    return (f"THE PANTS must match images 1 and 2 exactly, colour for colour: the real OQQ high-waisted wide-leg pants in {PANTS[c]}. "
            "Smooth matte stretch jersey, solid and opaque (never sheer, nothing shows through), no shine. A wide plain high waistband about a hand wide "
            "sitting at her natural waist, no drawstring, no buttons, no belt loops, no fly. One thin stitched seam line runs down the front of each leg "
            "from the waistband to the hem. Fitted over the hip and thigh, then wide and straight from the knee down to a full-length hem that covers the "
            "top of the shoe and brushes the floor. A hidden tonal pocket sits on the outer side of the hip just under the waistband (image 2). "
            "Only the small white round OQQ circle mark at the centre back under the waistband (image 3) when the back shows; no other logos, no ® or ™, no text.")
SHOES = ("ON HER FEET, both feet: the real Vans Premium Authentic low-top in sequin checkerboard (images 4 and 5): large black squares covered in black sequins, "
         "large off-white squares plain canvas (black and OFF-WHITE only, never brown, tan or beige checks), black laces through black eyelets (no gold or metal eyelets), "
         "the same checkerboard all the way round the heel (no solid black heel panel), a small BLACK woven side tab with white VANS letters (image 5), off-white rubber sidewall, gum sole. "
         "The hem covers most of each shoe so only the front half and toe cap show. Exactly two shoes, one on each foot, worn the right way round: the toe of each shoe points where her knees and the front of her body point, the heel at the back under the hem. "
         "The sequins look like real sequins in daylight: no added sparkles, glints, stars or light effects.")
HER = ("HER: Grace, exactly the body in image 6: slim build, medium-deep brown skin exactly like image 6 on every bit of skin, long almond nails with white "
       "nude polish. Her face is NEVER in frame: the top edge of the frame cuts at her chest.")
TOP = {"black": "A white ribbed cropped square-neck tank that ends at the top of the waistband, a strip of bare waist showing between them.",
       "brown": "A cream boxy cropped long-sleeve top with full puffed sleeves that ends just above the waistband."}
ROOM = {"black": "PLACE: the real kitchen in image 7: sage-green kitchen island with a white marble top, black round bar stools, warm oak floor.",
        "brown": "PLACE: the real kitchen in image 7: grey upholstered bar stools with wooden legs, white cabinets, dark island, grey wood floor."}
LIGHT = ("LIGHT: bright daylight, soft and even, neutral white balance: true black stays black, the brown stays chocolate, no yellow, orange or golden cast, "
         "no dark or moody grade. A real phone photo, casual and realistic, vertical 9:16. No text, no captions, no watermark anywhere.")
REF_DESC = {"refs/product_sheet.png": "the real pants from every side (listing photos, black and dark brown)", "refs/real_pocket.jpg": "the real hidden side pocket with a phone in it",
            "refs/real_back_logo.jpg": "the real centre-back OQQ circle mark", "refs/vans_product_sheet.png": "the real shoe from every side", "refs/real_vans_tab.jpg": "the real woven VANS side tab (small black tab, white VANS letters)",
            "refs/grace_body_sheet.jpg": "her real body and skin tone (ignore its clothes and room)", "refs/room.jpg": "the real room", "refs/room_b.jpg": "the real room", "refs/vans_real_heel_label.jpg": "the real Vans heel label (small WHITE OFF THE WALL label, black print)"}
LEGS = {"S2", "S5", "S7"}   # knees-to-floor shots: no top, no hands, no back mark (2026-10-25: chest framing in the body block won over "knees to floor" and S7 turned into a back view)
OLD_REFS_HEAD = ("Image 1 = the real pants from every side (listing photos, black and dark brown). Image 2 = the real hidden side pocket with a phone in it. "
             "Image 3 = the real centre-back OQQ circle mark. Image 4 = the real shoe from every side. Image 5 = the real woven VANS side tab. "
             "Image 6 = her real body and skin tone (ignore its clothes and room). Image 7 = the real room.")
STILL_REFS = {"black": ["refs/product_sheet.png", "refs/real_pocket.jpg", "refs/real_back_logo.jpg", "refs/vans_product_sheet.png",
                        "refs/real_vans_tab.jpg", "refs/grace_body_sheet.jpg", "refs/room.jpg"],
              "brown": ["refs/product_sheet.png", "refs/real_pocket.jpg", "refs/real_back_logo.jpg", "refs/vans_product_sheet.png",
                        "refs/real_vans_tab.jpg", "refs/grace_body_sheet.jpg", "refs/room_b.jpg"]}
FEET = {
 "S1": "She faces away from the camera toward the island: both toes point AWAY from the camera, the backs of both heels face the camera.",
 "S2": "she is mid-step walking toward the LEFT edge of the frame: BOTH shoes point the same way, toes to the LEFT edge and heels to the right edge; her left foot is ahead (further left) flat on the floor, her right foot behind with its heel just lifting; the two shoes are parallel and never point opposite ways.",
 "S3": "She faces the camera, turned a little to her left: both toes point toward the camera and slightly to the left edge, the heels behind.",
 "S5": "FRONT VIEW: she stands facing the camera, feet side by side about hip-width apart and parallel: both toe caps point AT the lens, the heels are hidden behind; both soles stay flat on the floor; we see the front of her shins with the front seam line of each leg, never the back of her legs or her heels.",
 "S6": "She faces the camera, turned a little to her left: both toes point toward the camera and slightly to the LEFT edge, the heels hidden behind; both soles flat on the floor.",
 "S7": "FRONT VIEW: she walks straight TOWARD the camera: both toe caps point AT the lens and are the closest thing to the camera, the heels are hidden behind; we see the front of her shins with the front seam line of each leg, never the back of her legs or her heels; both soles stay flat on the floor in a short, calm step, so the bottoms of the shoes never show.",
 "S8": "She faces the RIGHT edge of the frame: her knees and both toes point to the RIGHT edge, both heels point to the left edge.",
}
SHOTS = [
 ("S1", "HAND", "black", [0.0, 2.6], "Okay, y'all keep asking what the back of these looks like.",
  "SCENE: mirror-style photo from behind and a little to her right, chest to floor: she stands with her back three-quarters to the camera next to the island, weight on her left leg; her right hand rests flat on the back of her right hip, fingers together, whole wrist visible. The white circle mark shows at the centre back under the waistband.",
  "she shifts her weight slowly from foot to foot and her right hand slides down over the back of her hip and thigh; the wide legs sway and the hem stays on the floor; slight handheld camera, no cut", ["refs/real_back_logo.jpg", "refs/product_sheet.png"]),
 ("S2", "HAND-FREE", "black", [2.6, 5.0], "If wide-leg pants always stop at your ankles, look at this length.",
  "low camera at knee height, SIDE view of her lower legs on the oak floor: the black wide hems fall over her shoes and brush the floor, only the front half of each sequin Vans shows.",
  "she takes two slow steps across the frame from right to left, the hems swing and settle back over the shoes; the camera stays low and pans with her; no hand appears at any time", ["refs/real_vans_tab.jpg", "refs/product_sheet.png"]),
 ("S3", "HAND", "black", [5.0, 8.0], "I'm [height], wearing a [size] in the [Regular or Longer], and they go all the way down over my sneakers.",
  "SCENE (the inspo's shot): mirror-style photo of her right side, chest to floor, standing beside a black bar stool; her left hand rests on the stool's back with a relaxed grip, whole wrist visible; her right hand at her side. The full leg from waistband to floor is in frame.",
  "she shifts her weight from foot to foot and sways her hips gently, the wide legs sway and the hems stay on the floor over her shoes; her right hand stays resting on the marble counter edge, her left hand relaxed at her side; the phone stays tucked in the side pocket with only its top showing; slight handheld camera", ["refs/product_sheet.png"]),
 ("S4", "HAND", "black", [8.0, 10.6], "The waist sits up high, and there's a hidden pocket right here for my phone.",
  "SCENE: close-up of her right hip from the front-side, from the bottom of the tank to mid-thigh: the high waistband and the hidden pocket under it. Her right hand holds a plain phone in a light grey case with no logo, upright, its bottom edge just inside the pocket opening, thumb on the front, whole wrist visible.",
  "her right hand slides the phone straight down into the hidden pocket until only its top edge shows, then smooths the fabric over it and lets go; one grip, the phone never turns or flips; the pocket stays tonal black", ["refs/real_pocket.jpg", "refs/product_sheet.png"]),
 ("S5", "HAND-FREE", "black", [10.6, 12.8], "I've got them in black,",
  "camera low at shin height IN FRONT of her, FRONT view of her lower legs standing on the oak floor: the black wide hems pool over the shoes and only the toe caps of both sequin Vans show.",
  "she rocks gently from heel to toe and back twice and shifts her weight from foot to foot, the wide hems sway and settle over the toe caps; both feet stay facing the camera and never turn; no hand appears at any time", ["refs/real_vans_tab.jpg", "refs/product_sheet.png"]),
 ("S6", "HAND", "brown", [12.8, 15.8], "and in brown too, because when I find something I like, I get more than one.",
  "mirror-style photo of her FRONT, turned slightly to her left, chest to floor, standing beside a grey upholstered bar stool: her left hand rests on the top of the stool's back with a relaxed grip, whole wrist visible; her right hand rests on her right hip. We see the front of the pants: the wide waistband, the front seam line down each leg and the full length to the floor.",
  "she sways her hips gently and shifts her weight from foot to foot, the wide brown legs sway and the hems stay on the floor over her shoes; her left hand stays on the stool; slight handheld camera", ["refs/product_sheet.png"]),
 ("S7", "HAND-FREE", "brown", [15.8, 18.2], "Black and brown go with everything for fall, so grab both.",
  "camera low on the floor IN FRONT of her, FRONT view of her lower legs as she walks toward the camera on the grey wood floor: the brown wide hems swing forward and the toe caps of both sequin Vans show under them.",
  "she walks toward the camera, three relaxed steps, both feet pointing forward, the hems swing over the shoes; she stops just before the lens; no hand appears at any time", ["refs/real_vans_tab.jpg", "refs/product_sheet.png"]),
 ("S8", "HAND", "brown", [18.2, 20.5], "I linked them in the orange cart for you.",
  "SCENE: mirror-style photo of her right side, chest to floor, in the middle of the kitchen; her right hand on her right hip, fingers forward, whole wrist visible.",
  "she holds the phone still up by her face at the top edge of the frame (her face never shows) and her other hand slides down over her hip; she shifts her weight and sways gently, the wide brown legs swing and settle over the shoes; slight handheld camera", ["refs/product_sheet.png"]),
]
def refs_for(sid, c):
    if sid in LEGS:
        r = ["refs/product_sheet.png", "refs/vans_product_sheet.png", "refs/real_vans_tab.jpg", "refs/room.jpg" if c == "black" else "refs/room_b.jpg", "refs/grace_body_sheet.jpg"]
    else:
        r = list(STILL_REFS[c])
        if sid != "S1":
            r.remove("refs/real_back_logo.jpg")   # back mark only where the back shows
        if sid == "S4":
            r = [x for x in r if "vans" not in x]  # feet out of frame
    return r


def n(refs, key):
    return refs.index(key) + 1


out = {"shots": []}
for sid, kind, c, win, line, scene, motion, extra in SHOTS:
    refs = refs_for(sid, c)
    head = " ".join(f"Image {i+1} = {REF_DESC[r]}." for i, r in enumerate(refs))
    pants_txt = pants(c).replace("images 1 and 2", "image 1" + (f" and image {n(refs,'refs/real_pocket.jpg')}" if "refs/real_pocket.jpg" in refs else ""))
    pants_txt = pants_txt.replace("(image 2)", f"(image {n(refs,'refs/real_pocket.jpg')})" if "refs/real_pocket.jpg" in refs else "")
    if "refs/real_back_logo.jpg" in refs:
        pants_txt = pants_txt.replace("(image 3) when the back shows", f"(image {n(refs,'refs/real_back_logo.jpg')})")
    else:
        pants_txt = pants_txt.replace("Only the small white round OQQ circle mark at the centre back under the waistband (image 3) when the back shows; no other logos", "No logos")
    shoes_txt = SHOES.replace("(images 4 and 5)", f"(image {n(refs,'refs/vans_product_sheet.png')})").replace("(image 5)", f"(image {n(refs,'refs/real_vans_tab.jpg')})") if sid != "S4" else ""
    body_n = n(refs, "refs/grace_body_sheet.jpg")
    room_txt = ROOM[c].replace("image 7", f"image {n(refs, 'refs/room.jpg' if c == 'black' else 'refs/room_b.jpg')}")
    if sid in LEGS:
        first = ("SHOT: " + scene + " FRAMING: only her lower legs and feet, from just above the knees down to the floor; nothing above her knees is in the frame (no top, no waist, no hands, no arms). FEET: " + FEET[sid])
        herx = f"Any skin that shows (a glimpse of ankle) matches image {body_n}."
        pants_txt = (f"THE PANTS must match image 1 exactly, colour for colour: the {'BLACK' if c == 'black' else 'DARK BROWN'} pair of the real OQQ wide-leg pants. "
                     "Smooth matte stretch jersey, solid and opaque (never sheer, nothing shows through), no shine. One thin stitched seam line runs down the front of each leg. "
                     "Below the knee the legs are wide and straight (not flared, not tapered) down to a full-length hem that covers the top of the shoe and brushes the floor. No logos, no text.")
        body = [first, head, herx, pants_txt, shoes_txt, room_txt, LIGHT]
    else:
        first = "SHOT: " + scene + (" FEET: " + FEET[sid] if sid != "S4" else " Her feet are out of frame.")
        herx = HER.replace("image 6", f"image {body_n}")
        body = [first, head, herx, TOP[c], pants_txt, shoes_txt, room_txt, LIGHT]
    still = " ".join(x for x in body if x)
    if kind == "HAND-FREE" and sid not in LEGS:
        still += " No hands, arms or fingers anywhere in the frame."
    names = {"refs/real_back_logo.jpg": "the real centre-back OQQ circle mark: a small white round mark", "refs/real_pocket.jpg": "the real hidden side pocket (tonal, phone top showing)",
             "refs/real_vans_tab.jpg": "the real woven VANS side tab: small black tab, white VANS letters", "refs/product_sheet.png": "the pants product sheet", "refs/vans_real_heel_label.jpg": "the real Vans heel label: a small WHITE OFF THE WALL label with black print"}
    lines = [f"Image {i+2} is {names[r]}." for i, r in enumerate(extra)]
    keep = "her skin, top and pants exactly; her feet stay out of the frame" if sid == "S4" else "her skin, top, pants and shoes exactly"
    clip = (f"Recreate image 1 exactly as the first frame: keep its place, light, framing, {keep}. " + " ".join(lines) +
            f" The pants stay {PANTS[c].split(' (')[0].lower()}, smooth, matte and solid (never sheer), with the high plain waistband, the front seam line and a full-length wide straight leg; "
            f"they must match the product sheet colour for colour. Motion: {motion}. Her face never enters the frame. Hands keep five fingers and whole wrists. "
            + ("Exactly two shoes, worn the right way round; " + FEET[sid] + " " if sid != "S4" else "") + "No added marks, no \u00ae or \u2122, no text, no captions, no sparkle or light effects. No music, no voice. 4 seconds, 9:16.")
    out["shots"].append({"id": sid, "kind": kind, "colour": c, "window": win, "line": line, "still_refs": refs, "still": still,
                         "clip_refs": ["stills/%s.png" % sid] + extra, "motion": motion, "clip": clip})
json.dump(out, open("shots.json", "w"), indent=1)
print(len(out["shots"]), "shots;", sum(s["kind"] == "HAND-FREE" for s in out["shots"]), "hand-free; max still chars", max(len(s["still"]) for s in out["shots"]))
