"""CeraVe Winter Skin Bundle (Grace), 2026-11-02: writes shots.json + prompts/<ID>_clip.txt.
Written with prompt-master (Ralph's stack): size + view first, every reference named by number, print matched letter
for letter, no effect words, no text. Every shot shows ALL FOUR products together (Ralph 2026-11-02)."""
import json
from pathlib import Path

ROOM = "rooms/cand/px_6580366.jpg"
SHEET = "refs/product_sheet.png"
CL = ["refs/closeup_cleanser.png", "refs/closeup_am50.png", "refs/closeup_cream_tube.png", "refs/closeup_lipbalm.png"]
HAND = "../../grace/ref/hand-sheets/without_bracelet.jpg"

SIZE = ("TRUE SIZES, exactly as in the product sheet: the green-pump cleanser bottle is the tallest, about as tall as an "
        "adult hand from wrist to fingertip; the AM lotion bottle is about 85% of the cleanser's height; the cream tube "
        "stands on its cap about the same height as the lotion; the lip balm is a slim tube about half the cleanser's "
        "height and as wide as a finger. ")
PRODUCTS = (
    "The four products, each must match its close-up letter for letter and colour for colour: "
    "(a) Hydrating Facial Cleanser = image 3: white rounded bottle with a LIME-GREEN pump collar and a white pump with a "
    "long nozzle, navy 'CeraVe' with a green diagonal wedge on the right, 'Hydrating Facial Cleanser' in green, grey pill "
    "'MOISTURE BALANCE', small round navy seal bottom right; "
    "(b) AM Facial Moisturizing Lotion SPF 50 = image 4: white oval bottle, white pump on a BLUE collar, navy 'CeraVe' with "
    "a blue diagonal wedge on the right, small yellow-orange 'AM' pill, 'Facial Moisturizing Lotion' in blue with a "
    "yellow-orange '50', blue pill 'Broad Spectrum SPF 50'; "
    "(c) Intensive Moisturizing Cream = image 5: a white squeeze TUBE standing upright on its BLUE flip cap, flat crimped end "
    "at the top, small red 'NEW' tag top left, navy 'CeraVe' with a blue diagonal wedge on the right, 'Intensive "
    "Moisturizing Cream' all in NAVY, a NAVY band '5% HYDRO-UREA', grey pill 'RICH TEXTURE'; "
    "(d) Healing Lip Balm = image 6: slim NAVY squeeze tube standing on a SILVER cap, white 'CeraVe' running up the tube, "
    "white 'Healing Lip Balm', grey pill 'LIP PROTECTANT'. "
    "No other products, no box, no extra bottles, no added marks, no ® or ™ beyond the real labels. ")
ROOM_TXT = ("Setting = image 1, the real bathroom: light oak wood vanity top, sage-green rectangular wall tiles behind, the "
            "edge of a round mirror; bright soft neutral daylight, true colours, a clean counter with only a small folded "
            "white towel at the far edge. ")
TAIL = ("Vertical 9:16 phone photo, a single frame from a phone-shot UGC video, realistic, sharp focus on the labels, "
        "no text, no captions, no watermark, no logos other than the real labels.")
GRACE = ("Grace's hand (image 7: medium-brown skin, short squared French-tip nails with a pink base and white tips, the silver "
         "crown ring stack and the small gold heart ring, a blue band on the thumb), a soft cream knit sweater cuff on her forearm "
         "ending just above the wrist, entering from the frame edge with the whole wrist in frame. ")
REFS_TXT = ("Reference images: image 1 = the room; image 2 = the product sheet (shapes and true sizes); images 3-6 = the "
            "real fronts of the cleanser, AM lotion, cream tube and lip balm{hand}.")

def still(view, action, hand):
    return (view + SIZE + PRODUCTS + ROOM_TXT + (GRACE if hand else "No hand, fingers or people anywhere in the frame. ")
            + action + " " + TAIL + " " + REFS_TXT.format(hand="; image 7 = Grace's real hand sheet (skin, nails, rings)" if hand else ""))

CLIP_HEAD = ("Recreate image 1 exactly as the first frame: keep its room, light, framing{h} exactly. "
             "Images 2-5 are the real fronts of the four products (2 Hydrating Facial Cleanser with the lime-green pump, "
             "3 AM Facial Moisturizing Lotion SPF 50 with the blue collar, 4 Intensive Moisturizing Cream tube with navy text "
             "and a blue cap, 5 Healing Lip Balm navy tube with a silver cap): every label stays on its product the whole clip "
             "and matches its image letter for letter and colour for colour. Image 6 is the product sheet: keep these exact "
             "shapes, true sizes and colours, no added marks, no ® or ™, no extra text, no other products. ")
CLIP_TAIL = ("Vertical 9:16 phone footage, bright soft neutral daylight, true colours{skin}. "
             "No music, no voice, no captions, no on-screen text.")

shots = [
 dict(id="S1", hand=True, label="Hook: pump of the green cleanser, all four in the row",
  view=("Close-up from slightly above counter height, the camera 40 cm away. The four products stand in one row on the "
        "vanity, left to right: cleanser, AM lotion, cream tube, lip balm, every front label facing the camera. "),
  action=("Her RIGHT hand comes in from the right frame edge and rests its palm on top of the cleanser's white pump head, "
          "fingers curled over it, pressing it halfway down; her LEFT hand comes in from the bottom frame edge, cupped palm "
          "up just under the nozzle tip, a small dollop of white creamy cleanser landing in the palm. The other three "
          "products stay standing in the row, untouched."),
  motion=("Motion: her right hand presses the green-collared cleanser pump down two times and a small dollop of white "
          "creamy cleanser lands in her cupped left palm; the cleanser bottle stays standing on the counter, never lifted, "
          "never turned. Both hands keep their grip, whole wrists in frame. The other three products never move. "
          "Camera: handheld, almost still, no zoom.")),
 dict(id="S2", hand=False, label="Hand-free push-in on all four",
  view=("Low angle, the camera at counter height, 50 cm away. The four products stand in one row on the vanity, left to "
        "right: cleanser, AM lotion, cream tube, lip balm, front labels facing the camera, the cleanser nearest the lens. "),
  action="The products stand still on the clean counter.",
  motion=("Motion: none on the products: they stand perfectly still. Camera: a slow smooth push-in toward the row, ending "
          "with all four products still fully in frame and the same size relative to each other. No hand, fingers or people "
          "appear at any time.")),
 dict(id="S3", hand=True, label="AM lotion SPF 50 pump onto fingertips",
  view=("Close-up from slightly above counter height, the camera 35 cm away. The four products stand in one row on the "
        "vanity, left to right: cleanser, AM lotion, cream tube, lip balm, every front label facing the camera. "),
  action=("Her RIGHT hand comes in from the right frame edge, index finger resting on top of the AM lotion's white pump "
          "head, pressing it down; her LEFT hand comes in from the bottom frame edge, two fingertips held just under the "
          "pump nozzle with a small pearl of white lotion on them. The other three products stay standing in the row."),
  motion=("Motion: her right index finger presses the blue-collared AM lotion pump down once and a small pearl of white "
          "lotion lands on her left fingertips; the lotion bottle stays standing on the counter, never lifted, never "
          "turned. Whole wrists in frame. The other three products never move. Camera: handheld, almost still, no zoom.")),
 dict(id="S4", hand=True, label="Cream tube squeeze, the other three behind",
  view=("Close-up, camera at chest height looking slightly down, 40 cm away. In the soft background on the vanity, the "
        "cleanser, AM lotion and lip balm stand in a row, labels facing the camera; in the foreground her hands hold the "
        "cream tube. "),
  action=("Her RIGHT hand, from the right frame edge, holds the Intensive Moisturizing Cream tube upright by its middle "
          "(thumb on the back, fingers wrapped round the front edge, the navy front label fully visible and facing the "
          "camera), blue flip cap down and open; her LEFT hand, from the bottom frame edge, is held palm down under the "
          "cap with a short line of thick white cream on the back of the hand."),
  motion=("Motion: her right hand gently squeezes the tube once and a short line of thick white cream comes out onto the "
          "back of her left hand; the tube keeps one grip, front label to the camera, never turns or flips. Whole wrists in "
          "frame. The three products in the background never move. Camera: handheld, almost still, no zoom.")),
 dict(id="S5", hand=True, label="Lip balm lifted from the row",
  view=("Close-up from counter height, the camera 35 cm away. The four products stand in one row on the vanity, left to "
        "right: cleanser, AM lotion, cream tube, lip balm, front labels facing the camera. "),
  action=("Her RIGHT hand, from the right frame edge, pinches the Healing Lip Balm tube between thumb and two fingers at "
          "its middle and holds it upright 3 cm above the counter, silver cap down, the white 'CeraVe' and 'Healing Lip Balm' "
          "facing the camera; the other three products stand in the row beside it."),
  motion=("Motion: her right hand lifts the lip balm 3 cm higher and holds it there, keeping exactly the starting angle and "
          "the same distance from the camera; the lip balm keeps one grip, front print to the camera, never turns or flips. "
          "Whole wrist in frame. The other three products never move. Camera: locked off, no zoom.")),
 dict(id="S6", hand=False, label="End: slow arc on all four",
  view=("Three-quarter view from the left at counter height, the camera 55 cm away. The four products stand together in a "
        "tight row on the vanity, left to right: cleanser, AM lotion, cream tube, lip balm, front labels facing slightly "
        "right of the camera. "),
  action="The products stand still on the clean counter.",
  motion=("Motion: none on the products. Camera: a slow smooth arc from the left toward the front, ending straight on with "
          "every front label facing the camera, all four products fully in frame the whole time. No hand, fingers or people "
          "appear at any time.")),
]

out = []
for s in shots:
    h = s["hand"]
    refs = [ROOM, SHEET] + CL + ([HAND] if h else [])
    clip = (CLIP_HEAD.format(h=", hands" if h else "") + s["motion"] + " "
            + CLIP_TAIL.format(skin=", realistic medium-brown skin, short squared French-tip nails in every frame" if h else ""))
    Path(f"prompts/{s['id']}_clip.txt").write_text(clip + "\n")
    out.append({"id": s["id"], "label": s["label"], "hand": h, "product": True,
                "still": still(s["view"], s["action"], h), "still_refs": refs,
                "clip": clip, "clip_refs": [f"stills/{s['id']}.png"] + CL + [SHEET], "clip_model": "omni-1.1-flash"})
Path("shots.json").write_text(json.dumps(out, indent=1))
print("shots", len(out))
