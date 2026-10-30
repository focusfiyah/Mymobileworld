"""Builds shots.json + prompts/ for NovaTabz V1 (Grace cloned v5 VO, ~30 s), written with prompt-master (loaded 2026-10-30).
Product facts come only from product_truth.json (Ralph's 3 photos + the Amazon listing). Run: python3 make_shots.py"""
import json, os

JAR = ("the real NovaTabz jar: a short wide CLEAR GLASS jar, 2.17 inches wide and 1.65 inches tall (fits in a palm, smaller than a coffee mug), "
       "with a threaded glass neck and glass visible above and below a turquoise paper label that wraps its middle. Label front, exactly as image 2, letter for letter and colour for colour: "
       "a white rectangle with turquoise capitals TOOTHPASTE TABLETS; below it NOVA over TABZ in big white serif capitals; PEPPERMINT in spaced white capitals; "
       "62 / TABLETS in white on the left; NET WT / 23G / (0.8 OZ) in white on the right. No other words, no ® or ™.")
LID = "a brushed SILVER metal screw lid with a finely ridged side edge and a plain flat top (image 3)"
TABS = "plain WHITE round flat tablets with rounded edges, each about the size of an aspirin, no print, no colour, no stripes"
SIZE = "SIZE FIRST: the jar is small, about as wide as a woman's palm; her fingers look normal next to it, the jar never looks bigger than her hand."
HAND = ("Grace's hand exactly as on the hand sheet: medium-brown skin, short squared French-tip nails (pale pink with white tips), a silver crown ring stack on the ring finger, "
        "a small gold ring with a heart-shaped stone on the middle finger, a blue silicone band on the thumb, bare wrist with no bracelet and no watch, the whole wrist visible, "
        "the hand enters from the frame edge.")
NOHAND = "No hand, no fingers, no people."
END = "Bright neutral daylight, true colours, clean and fresh, not dark, not yellow. No text, no captions, no watermark."
CLIPEND = "No music, no voice, no captions, no on-screen text."
OMNI = "Recreate image 1 exactly as the first frame: keep its room, light, framing{h} exactly. Image 2 is the real NovaTabz label: the label print matches it letter for letter and colour for colour. Image 3 is the real silver lid. Image 4 is the product sheet: keep this exact clear glass jar, turquoise label and white tablets; no added marks. "
SEED = "Recreate reference image 1 exactly as the first frame, then "

def s(id, words, hand, product, room, still, motion):
    if product:
        clip = OMNI.format(h=" and hand" if hand else "") + "Motion: " + motion + (" The hand keeps one grip and the jar never turns, flips or changes shape." if hand else " No hand, fingers or people appear at any time.") + " The jar does not change size. " + CLIPEND
    else:
        clip = SEED + motion + " No NovaTabz jar appears at any time. " + CLIPEND
    return {"id": id, "words": words, "hand": hand, "product": product, "room": room, "still": still + " " + END, "clip": clip}

SHOTS = [
 s("S1", "At first I thought these were breath mints.", True, True, "B",
   SIZE + " Close-up on a white counter in a pink-tile bathroom: " + JAR + " It stands open, its lid (" + LID + ") lying beside it, full of " + TABS + ". " + HAND +
   " Her thumb and index finger pinch ONE white tablet just above the open jar. Only one jar.",
   "the fingers lift the one tablet slowly up toward the lens; the jar stays still on the counter."),
 s("S2", "Nope, it's toothpaste.", False, True, "A",
   SIZE.replace("her fingers look normal next to it, the jar never looks bigger than her hand", "it is shorter than the toothbrush cup beside it") + " On a long grey bathroom vanity next to a white vessel sink, leaf-print wallpaper soft behind (room reference): " + JAR +
   " Open, full of " + TABS + ", its lid (" + LID + ") leaning against it, a clear glass cup with one bamboo toothbrush beside it. Only one jar. " + NOHAND,
   "only the camera moves, a slow push-in toward the open jar; nothing else moves."),
 s("S3", "No more dried paste in the sink", False, False, "A",
   "Close-up into a white vessel sink on a grey vanity, leaf-print wallpaper soft behind (room reference): dried white and pale blue toothpaste globs stuck around the drain and the rim, "
   "a squeezed, plain white unbranded toothpaste tube with a crusty cap lying on the counter edge. No words on the tube. " + NOHAND,
   "the camera slowly pushes in toward the dried toothpaste globs around the drain; nothing moves. No person or hand appears at any time."),
 s("S4", "or a tube leaking in your bag.", True, False, "D",
   "Close-up on top of a cream suitcase in a bright cream living room (room reference): " + HAND.replace("the hand enters", "both hands enter") +
   " Her hands hold open a clear zip toiletry pouch; inside, a squeezed plain white unbranded tube has leaked white toothpaste smeared over a little bottle and the inside of the pouch. No words on anything.",
   "the hands pull the pouch open a little wider to show the toothpaste smear; the smear does not move. Only these two hands appear, whole wrists, the same rings as reference image 2."),
 s("S5", "Chew one,", True, False, "C",
   "Close-up beside a wooden bathroom vanity with a small green plant and a concrete wall (room reference): " + HAND + " She holds ONE plain white round flat tablet, about the size of an aspirin, between thumb and index finger, held up in front of the plant. No jar.",
   "the hand slowly lifts the tablet up and out of the top of the frame. Only this hand appears, whole wrist, the same rings as reference image 2. No face appears."),
 s("S6", "brush with a wet toothbrush,", True, False, "C",
   "Close-up over a wooden bathroom vanity with a matte black tap and a small plant (room reference): " + HAND + " She grips a bamboo toothbrush by the handle and holds its clean white bristles under the running tap. No paste on the brush.",
   "clear water runs over the bristles and the hand turns the brush a little under the stream. Only this hand appears, whole wrist, the same rings as reference image 2."),
 s("S7", "and it foams like regular paste.", False, False, "A",
   "Macro close-up: a bamboo toothbrush lies across the rim of a white vessel sink, its bristles covered in fluffy white foam, leaf-print wallpaper soft behind (room reference). " + NOHAND,
   "tiny bubbles in the white foam slowly pop and settle while the camera slowly pushes in. No person or hand appears at any time."),
 s("S8", "Nano hydroxyapatite, no fluoride, and a glass jar instead of a tube.", False, True, "A",
   SIZE.replace("her fingers look normal next to it, the jar never looks bigger than her hand", "it is about as tall as a coffee mug is wide") + " Eye-level close-up on a long grey bathroom vanity, leaf-print wallpaper soft behind (room reference): " + JAR + " Closed with its lid (" + LID + ")" + ", white tablets visible through the clear glass above and below the label. Only one jar. " + NOHAND,
   "only the camera moves, a slow arc a little to the right around the closed jar; the jar does not move."),
 s("S9", "People say it leaves a nice tingly, minty clean.", True, True, "B",
   SIZE + " Close-up on a white counter in a pink-tile bathroom, a small fresh mint sprig beside the jar: " + JAR + " Closed with its lid (" + LID + ")" + ". " + HAND +
   " Her fingers GRIP the ridged edge of the silver lid from above, the thumb on one side and the fingers on the other. Only one jar.",
   "the fingers twist the silver lid and lift it straight up off the jar, showing the white tablets inside."),
 s("S10", "The only downside? Nobody has an excuse for a messy sink now.", False, True, "A",
   SIZE.replace("her fingers look normal next to it, the jar never looks bigger than her hand", "it is shorter than the toothbrush cup beside it") + " A spotless, shiny white vessel sink on a long grey vanity, leaf-print wallpaper behind (room reference); " + JAR +
   " Closed with its lid (" + LID + ")" + ", standing beside a clear glass cup with a bamboo toothbrush. Clean counter. Only one jar. " + NOHAND,
   "only the camera moves, a slow sideways slide along the clean vanity toward the jar; nothing moves."),
 s("S11", "With holiday trips coming, they're not a liquid, so they fly through security.", True, True, "D",
   SIZE + " Close-up into an open cream suitcase in a bright cream living room (room reference), folded clothes and a clear zip toiletry pouch inside: " + HAND + " She GRIPS " + JAR + " Closed with its lid (" + LID + ")" + ", the thumb on one side and the fingers wrapped around the other. Only one jar.",
   "the hand lowers the jar and sets it into the clear toiletry pouch, then lets go."),
 s("S12", "Sixty-two is about a month, so grab one for home and one for your carry-on. It's in the orange cart.", False, True, "B",
   SIZE.replace("her fingers look normal next to it, the jar never looks bigger than her hand", "it fills only the middle third of the frame") + " A white counter in a pink-tile bathroom with a green leaf print behind (room reference): " + JAR + " Closed with its lid (" + LID + ")" + ". Only one jar. " + NOHAND,
   "only the camera moves, a slow push-in toward the jar's label; nothing moves."),
]
P = {"SHEET": "refs/product_sheet.png", "LABEL": "refs/real/closeup_label.png", "LID": "refs/real/closeup_lid.png"}
HANDREF = "../../grace/ref/hand-sheets/without_bracelet.jpg"
os.makedirs("prompts", exist_ok=True)
for x in SHOTS:
    r, names = [], []
    def add(p, what): r.append(p); names.append(f"image {len(r)} = {what}")
    if x["product"]:
        add(P["SHEET"], "the product sheet from real photos: copy the clear glass jar, turquoise label, silver lid and white tablets exactly")
        add(P["LABEL"], "a real close-up of the label print")
        add(P["LID"], "a real photo of the silver lid")
    add(f"rooms/room_{x['room']}.jpg", "the real room to use as the background (same colours and light)")
    if x["hand"]: add(HANDREF, "Grace's real hand sheet (skin tone, nails, rings, bare wrist)")
    note = "Reference images: " + "; ".join(names) + "."
    if x["product"]: note += " The jar must match images 1, 2 and 3 exactly in shape, size and colour; the label print matches image 2 letter for letter and colour for colour."
    x["still"] = "Vertical 9:16 photo, a single frame from a phone-shot UGC video. " + x["still"] + " " + note
    x["still_refs"] = r
    st = f"stills/{x['id']}.png"
    x["clip_refs"] = [st, P["LABEL"], P["LID"], P["SHEET"]] if x["product"] else [st] + ([HANDREF] if x["hand"] else [])
    x["clip_model"] = "omni (Flow first)" if x["product"] else "seedance-2-mini"
    open(f"prompts/still_{x['id']}.txt", "w").write(x["still"]); open(f"prompts/clip_{x['id']}.txt", "w").write(x["clip"])
SEE = {"S1": "Fingers pinch one white tablet up out of the open jar, pink-tile counter", "S2": "Open jar full of tablets beside a toothbrush cup on the grey vanity, push-in", "S3": "Dried toothpaste globs in the vessel sink, plain crusty unbranded tube, push-in", "S4": "Hands open a toiletry pouch on a suitcase: a plain tube leaked paste inside", "S5": "Hand holds one white tablet up, lifts it out of frame (toward the mouth, no face)", "S6": "Hand holds a bamboo toothbrush under the running tap", "S7": "Macro: white foam on the toothbrush resting on the sink rim, bubbles settle", "S8": "Closed jar on the vanity, slow arc around it, tablets through the glass", "S9": "Hand twists the silver lid off, mint sprig beside the jar", "S10": "Spotless sink, jar beside the toothbrush cup, slow side slide", "S11": "Hand sets the closed jar into a clear toiletry pouch in an open suitcase", "S12": "END: one closed jar on the pink-tile counter, push-in to the label"}
for x in SHOTS: x["see"] = SEE[x["id"]]
json.dump({"shots": SHOTS}, open("shots.json", "w"), indent=1, ensure_ascii=False)
print(len(SHOTS), "shots;", sum(x["product"] for x in SHOTS), "product;", sum(not x["hand"] for x in SHOTS), "hand-free")
