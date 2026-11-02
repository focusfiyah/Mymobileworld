"""CeraVe Winter Skin Bundle (Grace), 2026-11-02 v2: writes shots.json + prompts/<ID>_clip.txt.
Ralph 2026-11-02: "Not all the products on every shot. Use the green mostly however show the group shot when necessary
and towards the end." So S1-S3 show ONLY the green Hydrating Facial Cleanser (its refs only: no sheet of all four, so
the others are not drawn), S4-S5 show the group of four. Written with prompt-master (Ralph's stack): size + view first,
every reference named by number, print matched letter for letter, no effect words, no text."""
import json
from pathlib import Path

ROOM = "rooms/cand/px_6580366.jpg"
SHEET = "refs/product_sheet.png"
CLN = "refs/closeup_cleanser.png"
CL4 = [CLN, "refs/closeup_am50.png", "refs/closeup_cream_tube.png", "refs/closeup_lipbalm.png"]
HAND = "../../grace/ref/hand-sheets/without_bracelet.jpg"

CLEANSER = ("THE PRODUCT, exactly as image 2, letter for letter and colour for colour: ONE CeraVe Hydrating Facial Cleanser "
    "bottle, about as tall as an adult hand from wrist to fingertip with its pump: a white rounded bottle with a LIME-GREEN "
    "pump collar and a white pump with a long nozzle; label: navy 'CeraVe' with a green diagonal wedge on the right, small "
    "'DEVELOPED WITH DERMATOLOGISTS', 'Hydrating Facial Cleanser' in green, 'For Normal to Dry Skin', grey pill 'MOISTURE "
    "BALANCE', a small round navy seal bottom right. It is the only product in the frame: no other bottles, tubes, jars, "
    "boxes or products anywhere, no added marks, no ® or ™ beyond the real label. ")
SIZE4 = ("TRUE SIZES, exactly as in the product sheet: the green-pump cleanser bottle is the tallest, about as tall as an "
         "adult hand from wrist to fingertip; the AM lotion bottle is about 85% of the cleanser's height; the cream tube "
         "stands on its cap about the same height as the lotion; the lip balm is a slim tube about half the cleanser's "
         "height and as wide as a finger. ")
GROUP = (
    "The four products, each must match its close-up letter for letter and colour for colour: "
    "(a) Hydrating Facial Cleanser = image 3: white rounded bottle with a LIME-GREEN pump collar and a white pump with a "
    "long nozzle, navy 'CeraVe' with a green diagonal wedge on the right, 'Hydrating Facial Cleanser' in green, grey pill "
    "'MOISTURE BALANCE', small round navy seal bottom right; "
    "(b) AM Facial Moisturizing Lotion SPF 50 = image 4: white oval bottle, white pump on a BLUE collar, navy 'CeraVe' with "
    "a blue diagonal wedge on the right, small yellow-orange 'AM' pill, 'Facial Moisturizing Lotion' in blue with a "
    "yellow-orange '50', blue pill 'Broad Spectrum SPF 50'; "
    "(c) Intensive Moisturizing Cream = image 5 (it MUST show the small red 'NEW' tag top left and the NAVY '5% HYDRO-UREA' band with its round drop icon): a white squeeze TUBE standing upright on its BLUE flip cap, flat crimped end "
    "at the top, small red 'NEW' tag top left, navy 'CeraVe' with a blue diagonal wedge on the right, 'Intensive "
    "Moisturizing Cream' all in NAVY, a NAVY band '5% HYDRO-UREA', grey pill 'RICH TEXTURE'; "
    "(d) Healing Lip Balm = image 6: slim NAVY squeeze tube standing on a SILVER cap, white 'CeraVe' running up the tube, "
    "white 'Healing Lip Balm', grey pill 'LIP PROTECTANT'. "
    "No other products, no box, no extra bottles, no added marks, no ® or ™ beyond the real labels. ")
ROOM_TXT = ("Setting = image 1, the real bathroom: light oak wood vanity top, sage-green rectangular wall tiles behind, the "
            "edge of a round mirror; bright soft neutral daylight, true colours, a clean counter with only a small folded "
            "white towel at the far edge. ")
TAIL = ("Vertical 9:16 phone photo, a single frame from a phone-shot UGC video, realistic, sharp focus on the label, "
        "no text, no captions, no watermark, no logos other than the real label.")
GRACE = ("Grace's hand (image {n}: medium-brown skin, short squared French-tip nails with a pink base and white tips, the "
         "silver crown ring stack and the small gold heart ring, a blue band on the thumb), a soft cream knit sweater cuff "
         "on her forearm ending just above the wrist, entering from the frame edge with the whole wrist in frame. ")
NOHAND = "No hand, fingers or people anywhere in the frame. "

CLIP1 = ("Recreate image 1 exactly as the first frame: keep its room, light, framing{h} exactly. Image 2 is the real front "
         "of the CeraVe Hydrating Facial Cleanser: its label stays on the bottle the whole clip and matches image 2 letter "
         "for letter and colour for colour, the lime-green pump collar stays lime green. It is the only product in the "
         "clip: no other bottles, tubes or products appear, no added marks, no ® or ™, no extra text. ")
CLIP4 = ("Recreate image 1 exactly as the first frame: keep its room, light, framing{h} exactly. Image 2 is the real "
         "front of the Hydrating Facial Cleanser with the lime-green pump, image 3 the AM Facial Moisturizing Lotion SPF 50 "
         "with the blue collar, image 4 the Intensive Moisturizing Cream tube with navy text and a blue cap, image 5 the "
         "Healing Lip Balm navy tube with a silver cap: every label stays on its product the whole clip and matches its image "
         "letter for letter and colour for colour. Image 6 is the product sheet: keep these exact shapes, true sizes and "
         "colours, no added marks, no ® or ™, no extra text, no other products. ")
CLIP_TAIL = ("Vertical 9:16 phone footage, bright soft neutral daylight, true colours{skin}. "
             "No music, no voice, no captions, no on-screen text.")

shots = [
 dict(id="S1", hand=True, group=False, t="0.0-2.0", label="Hook: green cleanser pumped into her palm",
  view=("Close-up from slightly above counter height, the camera 35 cm away. The cleanser bottle stands on the vanity in "
        "the centre of the frame, its front label facing the camera, the pump nozzle pointing to the LEFT, its tip above her cupped left palm. "),
  action=("Her RIGHT hand comes in from the right frame edge, fingertips on top of the white pump head; her LEFT hand comes "
          "in from the bottom frame edge, cupped palm up under the nozzle tip, a small dollop of white creamy cleanser in "
          "the palm. (S1 r3 = an edit of the r1 still that only turned the pump head: prompts/S1_edit.txt)"),
  motion=("Motion: her right fingertips press the lime-green-collared pump down two times and each time a small dollop of "
          "white creamy cleanser comes out of the nozzle tip, which points to the LEFT with its tip over her palm, and drops "
          "straight down into her cupped left palm; the bottle stays standing on the counter, never lifted, never turned. "
          "Both hands keep their grip, whole wrists in frame. Camera: handheld, almost still, no zoom.")),
 dict(id="S2", hand=False, group=False, t="2.0-3.5", label="Hand-free push-in on the green cleanser",
  view=("Low angle, the camera at counter height, 45 cm away. The cleanser bottle stands alone on the vanity, a little "
        "left of centre, its front label facing the camera. "),
  action="The bottle stands still on the clean counter.",
  motion=("Motion: none on the bottle: it stands perfectly still. Camera: a slow smooth push-in toward the bottle, ending "
          "with the whole bottle, pump included, still in frame and the label sharp. No hand, fingers or people appear at "
          "any time.")),
 dict(id="S3", hand=True, group=False, t="3.5-5.0", label="Green cleanser lifted and held to camera",
  view=("Close-up, camera at the bottle's height, 35 cm away, the vanity and tiles soft behind. "),
  action=("The bottle stands perfectly upright and straight-on to the camera, not tilted, its whole front label flat to "
          "the lens and large in the frame, 10 cm above the counter. Her RIGHT hand, from the right frame edge, grips it "
          "from BEHIND: the palm on the back of the bottle, the thumb along the right side edge, the four fingertips just "
          "showing on the left side edge; no finger crosses the front label, every word of the label is clear and "
          "exactly as image 2."),
  motion=("Motion: her right hand lifts the bottle 3 cm higher and holds it there, keeping exactly the starting angle and "
          "the same distance from the camera; the bottle keeps one grip, front label to the camera, never turns or flips. "
          "Whole wrist in frame. Camera: locked off, no zoom.")),
 dict(id="S4", hand=True, group=True, t="5.0-6.8", label="Group: she sets the cleanser down beside the other three",
  view=("Close-up from slightly above counter height, the camera 45 cm away. On the vanity the AM lotion, the cream tube "
        "and the lip balm stand in a row on the right, labels facing the camera; there is a gap on the left of the row. "),
  action=("Her RIGHT hand, from the top right frame edge, holds the green-pump cleanser upright by its middle, its base 2 cm "
          "above the counter in the gap at the left end of the row, front label facing the camera."),
  motion=("Motion: her right hand lowers the cleanser the last 2 cm onto the counter at the left end of the row, lets go and "
          "slides out of the frame to the right; the cleanser keeps its front label to the camera, never turns or flips. "
          "The other three products never move. Whole wrist in frame while it is visible. Camera: handheld, almost still, "
          "no zoom.")),
 dict(id="S5", hand=False, group=True, t="8.0-10.0", label="End: slow arc on all four",
  view=("Three-quarter view from the left at counter height, the camera 55 cm away. The four products stand together in a "
        "tight row on the vanity, left to right: cleanser, AM lotion, cream tube, lip balm, front labels facing slightly "
        "right of the camera, the cleanser nearest the lens. "),
  action="The products stand still on the clean counter.",
  motion=("Motion: none on the products. Camera: a slow smooth arc from the left toward the front, ending straight on with "
          "every front label facing the camera, all four products fully in frame the whole time. No hand, fingers or people "
          "appear at any time.")),
]

out = []
for s in shots:
    h, g = s["hand"], s["group"]
    if g:
        refs = [ROOM, SHEET] + CL4 + ([HAND] if h else [])
        body = SIZE4 + GROUP
        rtxt = ("Reference images: image 1 = the room; image 2 = the product sheet (shapes and true sizes); images 3-6 = the "
                "real fronts of the cleanser, AM lotion, cream tube and lip balm" + ("; image 7 = Grace's real hand sheet (skin, nails, rings)." if h else "."))
        hn = 7; clip_refs = [f"stills/{s['id']}.png"] + CL4 + [SHEET]; head = CLIP4
    else:
        refs = [ROOM, CLN] + ([HAND] if h else [])
        body = CLEANSER
        rtxt = ("Reference images: image 1 = the room; image 2 = the real front of the cleanser" + ("; image 3 = Grace's real hand sheet (skin, nails, rings)." if h else "."))
        hn = 3; clip_refs = [f"stills/{s['id']}.png", CLN]; head = CLIP1
    still = s["view"] + body + ROOM_TXT + (GRACE.format(n=hn) if h else NOHAND) + s["action"] + " " + TAIL + " " + rtxt
    clip = (head.format(h=", hands" if h else "") + s["motion"] + " "
            + CLIP_TAIL.format(skin=", realistic medium-brown skin, short squared French-tip nails in every frame" if h else ""))
    Path(f"prompts/{s['id']}_clip.txt").write_text(clip + "\n")
    out.append({"id": s["id"], "label": s["label"], "t": s["t"], "hand": h, "group": g, "product": True,
                "still": still, "still_refs": refs, "clip": clip, "clip_refs": clip_refs, "clip_model": "omni-1.1-flash"})
Path("shots.json").write_text(json.dumps(out, indent=1))
print("shots", len(out))
