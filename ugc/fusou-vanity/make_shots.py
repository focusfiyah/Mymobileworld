"""Builds shots.json for the FUSOU vanity job (6 hands-only videos). Edit here, re-run, never hand-edit shots.json."""
import json

VANITY = (
 "THE VANITY (must match the product reference photos exactly, same piece in every shot): the FUSOU 2-in-1 vanity, "
 "matte WHITE engineered wood, flat slab drawer fronts with thin shadow gaps, every drawer and door with the same small "
 "round faceted CLEAR CRYSTAL knob on a short chrome stem. About 71 inches wide and 63 inches tall overall. "
 "DESK: a long white desk with a knee opening in the middle. Directly under the desk top is ONE row of exactly 4 shallow "
 "drawers side by side. Below that row, a LEFT drawer tower with exactly 4 drawers stacked and a RIGHT drawer tower with "
 "exactly 4 drawers stacked (12 drawers in total, all the same white). The knee opening between the towers is open, no "
 "drawers there. GLASS TOP: the desk top has 4 clear tempered-glass panes set flush into a white border, one over each "
 "top drawer, so the makeup inside the top drawers (in small divider trays) shows through the glass. "
 "HUTCH on the back of the desk: a top row of exactly 4 equal open cubbies running the width of the hutch; below it a "
 "left column of 3 open shelves and a right column of 3 open shelves; between the two columns, sitting on the desk, a "
 "large FRAMELESS LANDSCAPE makeup mirror that is clearly WIDER than it is tall (about 5 wide to 4 tall, NOT portrait, "
 "NOT square), filling the whole gap between the two shelf columns and resting directly on the desk's glass top, with a "
 "thin LED light line inset about an inch from its edge shaped as a rounded rectangle, and a small round touch button on "
 "the glass at its lower left. The hutch is exactly as wide as the desk top, no gaps, no mirror set into a recess. "
"SIDE CABINET on the RIGHT end: a tall narrow cabinet as tall as the hutch, its whole front is ONE full-length mirror "
 "door (frameless mirror, with its own tall thin rounded-rectangle LED line inset from the edge); the door is hinged on "
 "its outer right edge and opens outward to reveal 5 white shelves inside. "
 "LEFT SIDE PANEL of the desk: a built-in white power strip plate (one AC outlet at the top, two USB ports in the "
 "middle, one AC outlet at the bottom) and, next to it, a small white metal hair-dryer holder ring. "
 "STOOL: a white cube storage stool with a padded white faux-leather seat cushion and 2 drawers in front, each with the "
 "same crystal knob; it tucks into the knee opening. "
 "Never add or remove drawers, shelves, knobs or mirrors; never change the mirror shapes, the white colour or the "
 "knob style; no logos, no text on the furniture.")

HAND = (
 "The hands are the ONLY person in the video: Grace's real hands, exactly as in the first two reference images "
 "(match them as closely as possible): medium-dark brown skin with natural knuckle creases and visible veins on the "
 "back of the hand, slim fingers, LONG ALMOND-shaped nails extending well past the fingertips, glossy dusty mauve-pink "
 "gel polish with a thin crisp white French tip on every nail, the same nail length and shape on every finger. "
 "Ignore the annotation text and leader lines in those images. No rings, no bracelets. No face, no arms above the "
 "forearm, no other people.")

ROOM = (
 "Setting: the real product-photo bedroom, matched to reference A: a calm, tidy room with a warm greige-olive painted "
 "wall behind the vanity, a light natural-oak plank floor with soft patches of sunlight on it from a window on the "
 "LEFT, sheer white curtains reflected in the mirrors, a leafy green plant in a pot at the far right edge. The vanity "
 "styling is exactly as in reference A: perfume and skincare bottles and a reed diffuser on the hutch shelves, beige "
 "storage boxes and one tan leather handbag in the top cubbies, a short row of makeup on the desk top, a small cream "
 "vase. Inside the side cabinet (seen only when its mirror door is open), always as in reference C: a tan leather "
 "handbag and beige storage boxes on the upper shelves, folded plaid throw blankets and woven baskets in the middle, a "
 "mint-green storage box low down. The hair dryer is always the same pale teal-green dryer in the left holder. "
 "Clean, airy, a little expensive-looking, nothing cluttered.")

DARK = (
 "The vanity looks exactly like the reference photos, only darker. Lighting: evening, all room lights OFF, the room is dark and moody; the only real light comes from the vanity's LED "
 "mirror light lines, which glow and light the desk top and the hands. The window behind the curtains is deep dusk blue.")

BATH = (
 "Setting: a small, real-looking bathroom: a white sink counter crowded with makeup, skincare bottles, a hairbrush, "
 "perfume bottles and lipsticks all jumbled together; plain white wall, a little cramped, ordinary overhead light. "
 "NO vanity furniture in this shot.")

PHONE = (
 "Shot on a phone, vertical, natural light, realistic unretouched skin texture with visible knuckle creases, casual and "
 "real like a creator filmed it, no cinematic grading. No on-screen text or captions. No visible brand names.")

SUFFIX = (
 "Camera: handheld phone, gentle natural shake, no zoom unless stated. Fingers move naturally and stay anatomically "
 "correct (five fingers per hand). The vanity stays exactly the same piece the whole clip: same drawer count, same "
 "knobs, same mirror shapes, nothing appears or disappears. No sound. No on-screen text.")

# refs letters -> refs/vanity_*.jpg ; M = the approved master still
REFS = {"A": "refs/vanity_front.jpg", "B": "refs/vanity_open.jpg", "C": "refs/vanity_cabinet_open.jpg",
        "D": "refs/vanity_glass_top.jpg", "E": "refs/vanity_power_strip.jpg", "F": "refs/vanity_lit_room.jpg",
        "M": "refs/vanity_front.jpg"}  # M = the real listing photo A (Ralph chose it as the master, 2026-10-02)

def S(id, t, vo, still, video, refs, blocks=("hand", "vanity", "room"), dur=4):
    return dict(id=id, t=t, dur=dur, vo=vo, refs=refs, blocks=list(blocks), still=still, video=video)

shots = [
 # V1 Lights On (dark)
 S("V1S1", [0, 2], "Tap it once. Again. Now hold it.",
   "Tight close-up of the lower left corner of the makeup mirror and the glass desk top in a dark room; an index "
   "fingertip rests on the small round touch button on the mirror glass; the mirror's LED line glows cool white.",
   "The fingertip taps the button: the LED line switches from cool white to warm white, taps again: warm yellow, then "
   "the finger presses and holds and the light slowly dims down and back up.",
   ["M", "A"], ("hand", "vanity", "dark")),
 S("V1S2", [2, 6], "Bathroom light makes your makeup look fine, until you step outside.",
   "Medium shot in the dark room: the whole lit makeup mirror (glowing warm white rounded-rectangle LED line), the hutch "
   "shelves on both sides softly lit, the glass desk top below. No hands.",
   "Slow, smooth pull back from the mirror until the hutch shelves on both sides come into frame. Nothing else moves.",
   ["M", "F"], ("vanity", "dark")),
 S("V1S3", [6, 11], "This mirror has three light colors and it dims, so you can match wherever you're going.",
   "Close-up looking down at the desk top in the dark room, warm light from the mirror above; a hand holds the crystal "
   "knob of one of the 4 top drawers, the drawer just starting to open; through the glass pane you see makeup in "
   "divider trays inside.",
   "The hand slowly pulls the top drawer open toward the camera; the warm mirror light falls on the lipsticks and "
   "palettes inside.", ["M", "D"], ("hand", "vanity", "dark")),
 S("V1S4", [11, 14], "Heads up, it's almost six feet wide. Measure your wall first.",
   "Low three-quarter angle along the front edge of the desk in the dark room, the row of 4 top drawers with crystal "
   "knobs receding to the right, warm mirror glow above; a hand's fingertips rest on the left end of the desk edge.",
   "The fingertips glide slowly along the front edge of the desk from left to right, past the crystal knobs.",
   ["M", "A"], ("hand", "vanity", "dark")),
 S("V1S5", [14, 20], "It ships in three boxes, so if you want it up before the holidays, order it now.",
   "Medium-close shot of the makeup mirror in the dark room, LED line glowing warm white, a fingertip on the touch "
   "button at the lower left of the mirror.",
   "The fingertip taps: the LED line goes dark for a moment, taps again: it glows warm white again. Hold on the glow.",
   ["M", "A"], ("hand", "vanity", "dark"), dur=5),
 # V2 Drawer by Drawer (daylight)
 S("V2S1", [0, 3], "Every drawer on this thing has a job.",
   "Top-down shot straight through the clear glass desk top: under the glass, a top drawer with neat divider trays of "
   "lipsticks and palettes; a hand's fingers on the crystal knob of that drawer at the front edge.",
   "The hand slides the top drawer open underneath the glass, the trays moving out toward the camera.",
   ["M", "D"]),
 S("V2S2", [3, 7], "If your makeup lives in a bag under the sink, you dig for everything.",
   "Close-up of an open top drawer with white divider trays holding lipsticks in a neat row; a hand's fingers above it.",
   "The fingers lift one lipstick out of its slot and turn it slightly toward the camera.", ["M", "B"]),
 S("V2S3", [7, 11], "Twelve drawers, plus two in the stool.",
   "Three-quarter view of the LEFT drawer tower (4 stacked drawers under the top row) and the stool; a hand on the "
   "crystal knob of the second drawer of the tower.",
   "The hand pulls the tower drawer open, lets go, then pulls the top drawer of the stool open. Smooth, quick, satisfying.",
   ["M", "B"]),
 S("V2S4", [11, 13], "The top is glass, so you see your makeup before you open anything.",
   "Close-up looking down at the glass desk top: through the clear panes, organised makeup in divider trays; a "
   "fingertip touching the glass.",
   "The fingertip taps the glass twice above a palette, then slides across the pane.", ["M", "D"]),
 S("V2S5", [13, 17], "Plan an afternoon to build it. It's a lot of parts.",
   "Close-up of one open hutch shelf on the right column with two perfume bottles; a hand holding a third perfume "
   "bottle just in front of the shelf.",
   "The hand sets the perfume bottle down on the shelf next to the others and lets go.", ["M", "A"]),
 S("V2S6", [17, 21], "Holiday shipping gets slow, and it comes in three boxes. Order it now.",
   "Close-up of the RIGHT drawer tower with one drawer half open; an index finger touching the drawer front.",
   "The single finger pushes the drawer shut; it closes softly. Hold still for one second.", ["M", "B"]),
 # V3 Count With Me
 S("V3S1", [0, 3], "This is one piece of furniture. Count with me.",
   "Wide shot of the whole vanity, lights on warm white; in the foreground, slightly out of focus, a hand holds up one "
   "index finger.", "The hand holds the one finger up and gives it a small shake, vanity sharp behind it.", ["M", "A"]),
 S("V3S2", [3, 6], "No room for a mirror, a dresser and a shelf?",
   "Medium shot of the bare beige wall and floor just LEFT of the vanity, the left edge of the vanity at the right of "
   "the frame; a hand open, palm out, in front of the empty wall.",
   "The open hand sweeps slowly across the empty wall toward the vanity.", ["M"]),
 S("V3S3", [6, 7.5], "One, a lit makeup mirror.",
   "Close-up of the lower left corner of the makeup mirror, LED line off; a fingertip on the round touch button.",
   "The fingertip taps and the LED line lights up warm white.", ["M", "A"], dur=4),
 S("V3S4", [7.5, 9], "Two, a full-length mirror.",
   "Medium shot of the tall full-length mirror door on the right end, its LED line glowing; a hand with fingertips "
   "resting flat on the mirror surface near its edge.",
   "The fingertips slide down the mirror edge a little.", ["M", "A"]),
 S("V3S5", [9, 10.5], "Three, a hidden cabinet.",
   "Medium shot of the full-length mirror door, opened a few inches; a hand on its edge.",
   "The hand swings the mirror door open, revealing the cabinet shelves with the tan handbag, the beige storage boxes and the folded plaid blankets.",
   ["M", "C"]),
 S("V3S6", [10.5, 12], "Four, outlets for hair tools.",
   "Close-up of the left side panel of the desk: the white power strip plate (outlet, two USB ports, outlet) and the "
   "white dryer holder ring; a hand holding the pale teal-green hair dryer's plug near the top outlet.",
   "The hand pushes the plug into the top outlet.", ["M", "E"]),
 S("V3S7", [12, 13.5], "Five, a stool with drawers.",
   "Close-up of the white storage stool in front of the desk, its padded seat and 2 drawers with crystal knobs; a hand "
   "on the top drawer knob.", "The hand slides the stool's top drawer open.", ["M", "B"]),
 S("V3S8", [13.5, 16], "It needs about six feet of wall.",
   "Low three-quarter angle along the front edge of the desk, the 4 top drawers receding; fingertips on the left end of "
   "the edge.", "The fingertips glide along the desk edge from left to right.", ["M", "A"]),
 S("V3S9", [16, 20], "Five things, one order. It ships in three boxes, so get it before the holidays.",
   "Medium shot of the lit makeup mirror; in front of it a hand holds up all five fingers, open palm facing the camera.",
   "The hand holds the five fingers up and gives a small wave, mirror glowing behind.", ["M", "A"]),
 # V4 The Mirror Is a Door
 S("V4S1", [0, 2], "Nobody notices this mirror is a door.",
   "Tight vertical shot of the full-length mirror door, closed, reflecting the bedroom; a hand resting lightly on its "
   "outer edge. The mirror fills most of the frame so it is not obvious it is a door.",
   "The hand rests, then the fingertips curl around the door edge.", ["M", "A"]),
 S("V4S2", [2, 7], "Bags and shoes end up on the floor when there's nowhere to put them.",
   "Same angle, the hand's fingertips curled around the outer edge of the closed mirror door.",
   "The hand slowly pulls the mirror door open outward, revealing the 5 white shelves inside with the tan handbag, the beige "
   "storage boxes and the folded plaid blankets.", ["M", "C"]),
 S("V4S3", [7, 12], "Behind it, shelves for bags, shoes and perfume. Close it, and you've got a full-length mirror again.",
   "Medium shot into the open side cabinet: the beige storage boxes, plaid blankets and baskets on their shelves, "
   "the second shelf empty; a hand holding the tan leather handbag by its handle in front of that empty shelf.",
   "The hand sets the handbag on the empty shelf, then swings the mirror door shut.", ["M", "C"]),
 S("V4S4", [12, 15], "Just know it's big, about six feet wide.",
   "Wide shot of the whole vanity, lights on warm white, from the left end.",
   "Slow pan from the left drawer tower across the mirror to the full-length mirror door. No hands.", ["M", "A"],
   ("vanity", "room")),
 S("V4S5", [15, 20], "It comes in three boxes, so order now if you want it done before the holidays.",
   "Medium-close shot of the makeup mirror, LED line off; a fingertip on the touch button at its lower left.",
   "The fingertip taps and the LED line glows warm white. Hold on the glow.", ["M", "A"], dur=5),
 # V5 Get Ready Hands
 S("V5S1", [0, 3], "The best part of this vanity is the outlet.",
   "Close-up of the left side panel of the desk: the white power strip plate and the dryer holder ring; a hand holding "
   "the plug of a pale teal-green hair dryer next to the top outlet.",
   "The hand pushes the plug into the top outlet.", ["M", "E"]),
 S("V5S2", [3, 6], "No more dryer cord stretched across the room.",
   "Close-up of the left side panel: a hand holding a pale teal-green hair dryer by the handle just above the white holder ring.",
   "The hand lowers the dryer nozzle-down into the holder ring and lets go; the dryer hangs there.", ["M", "E"]),
 S("V5S3", [6, 12], "Two outlets, two USB ports, and a holder for your dryer. Your phone charges while you do your face.",
   "Close-up of the glass desk top in front of the lit makeup mirror: a phone lying on the desk with its cable going to "
   "the side; a hand reaching into an open top drawer for a makeup brush.",
   "The hand picks a makeup brush out of the drawer and lifts it toward the mirror; the mirror light shifts to warm "
   "yellow.", ["M", "D"]),
 S("V5S4", [12, 15], "Only two outlets, so it's your dryer plus one more tool.",
   "Close-up of the white power strip plate on the left side panel, the dryer plugged into the top outlet, the bottom "
   "outlet empty; an index finger pointing at the bottom outlet.",
   "The finger points at the top outlet, then the bottom one.", ["M", "E"]),
 S("V5S5", [15, 19], "Holiday get-ready season is close, and it ships in three boxes. Order it now.",
   "Medium-close shot in front of the lit makeup mirror: a hand holding a glass perfume bottle above the desk.",
   "The hand gives one spray toward the mirror (fine mist), then sets the bottle on the nearest hutch shelf.",
   ["M", "A"]),
 # V6 Clear the Counter
 S("V6S1", [0, 2], "Watch where all of this goes.",
   "Close-up of a crowded bathroom sink counter, makeup, skincare and perfume bottles jumbled; a hand at the edge.",
   "The hand sweeps the jumble of products together into one pile.", [], ("hand", "bath")),
 S("V6S2", [2, 6], "Makeup on the sink, skincare on the dresser, perfume on the windowsill.",
   "Close-up of the same crowded bathroom counter, a woven basket at the front edge; two hands gathering products.",
   "Both hands scoop the products into the basket.", [], ("hand", "bath")),
 S("V6S3", [6, 12], "Lipsticks go in the drawers, under the glass. Perfume on the shelves. Hair tools plug in on the side.",
   "Close-up looking down at an open top drawer of the vanity under the glass desk top, divider trays half empty; a "
   "hand holding three lipsticks above it.",
   "Fast, satisfying: the hand drops the lipsticks into the tray slots one after another, then slides the drawer shut.",
   ["M", "D"]),
 S("V6S4", [12, 14], "Give yourself an afternoon to build it.",
   "Close-up of a hutch shelf with an empty spot; a hand holding a perfume bottle.",
   "The hand sets the perfume bottle on the shelf, lined up with the others.", ["M", "A"]),
 S("V6S5", [14, 20], "If someone in your house keeps asking for a vanity, this one ships in three boxes. Order early for Christmas.",
   "Medium shot of the finished, tidy vanity with the mirror lit warm white, from close in.",
   "Slow pull back until the whole vanity, stool and mirror door are in frame. No hands.", ["M", "F"],
   ("vanity", "room"), dur=5),
]

job = dict(
 product="FUSOU 2-in-1 Vanity Desk (71\" white, 12 drawers + 2-drawer stool, LED makeup mirror + full-length LED mirror door, "
         "hidden side cabinet, power strip 2 AC + 2 USB, glass top) https://shop.tiktok.com/us/pdp/1732251413004981161",
 client="Grace", voice="Grace records her own voiceover (no ElevenLabs).",
 format=dict(aspect_ratio="9:16", resolution="720p"),
 still_model="nano-banana-pro on Kie, 1K, 9:16; image_input = hand refs (hand shots) + the real listing photos listed per shot (M = listing photo A)",
 video_model="bytedance/seedance-2-mini on Kie, first_frame_url = approved still, generate_audio false, 720p, 9:16",
 pending=["colour (white assumed)", "hand refs (same as Vicks assumed)", "bedroom room look"],
 blocks=dict(vanity=VANITY, hand=HAND, room=ROOM, dark=DARK, bath=BATH, phone=PHONE), video_suffix=SUFFIX, refs=REFS,
 rules=["Shots without the vanity (V6S1, V6S2) carry NO vanity text and NO vanity refs.",
        "Shots without hands (V1S2, V4S4, V6S5) carry NO hand text and NO hand refs.",
        "Dark shots (V1) use the dark block instead of the room daylight."],
 shots=shots)
json.dump(job, open("shots.json", "w"), indent=1, ensure_ascii=False)
stills = len(shots); clips = len(shots); secs = sum(s["dur"] for s in shots)
print(f"{stills} stills ${stills*0.09:.2f} + {clips} clips {secs}s ${secs*0.041:.2f} = ${stills*0.09+secs*0.041:.2f}")
