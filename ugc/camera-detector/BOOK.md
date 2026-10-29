# Production Book: Hidden Camera Detector LY-10, black (Grace), 2026-10-28

Sent to Ralph: https://claude.ai/artifact/WxfuVo6J1eMDS5c779TVNC (2026-10-28)

## 1. Job
- Client: Grace (assumed, question 1)  Product: "Multi-Functional Camera Detector" model LY-10, black (Grace's own unit, Ralph's 7 photos in `ref/real/`), TikTok Shop listing 1732588237020435357 (the product both your examples link to)  Route: hands + hand-free AI over Grace's voice, product lock, Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Job folder: `ugc/camera-detector/`  Target length: ~34 s  Shots: 11 (6 HAND / 5 HAND-FREE), no face
- Your examples: @user6191215178177 191.5K https://www.tiktok.com/@user6191215178177/video/7680943338752609549 and @liuxing1238 15.9K https://www.tiktok.com/@liuxing1238/video/7693104034340818207 (same product). Also modeled on @lism792 173K and @liuxing1238 78K (same product), @camrynpicks 1.2M and @evaneramagic 677K (the niche's biggest).

## 2. Gate result (`python3 grace/gate.py ugc/camera-detector`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read (+ live rules doc) | proof/playbook.md | OK |
| Audience research | research/audience.md (958 phrases, 50 TikTok comments, 407 listing reviews read) | OK: top search "do hidden camera detectors work"; 1-star "merely a flashing red light that you self activate"; comment "why does mine not beep? when finding cameras?" |
| Coach research (shop + tag x2 + discover + video x8) | research/coach_research.md | OK: every winner shows the red through-the-window view + the door handle |
| Daily viral board | research/coach/viral-2026-10-28.json | OK (42 home/travel shop videos; no detector moving this week, angle open) |
| Product facts (source) | research/product_facts.md, product_truth.json | OK; 2 claims we do NOT make (see flag) |
| Hooks modeled on named winners | research/hooks.md | A H105 (script), B H028, C H132 |
| Humanizer | proof/humanizer.md | OK, Grace's posted voice |
| Readability (grade) | research/readability_v1.txt | 4.9 |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace cloned v5 voice, ~34 s, 131 words)
1. Listen, y'all have seen these camera finders everywhere, but nobody shows you the part that matters.
2. Let's be for real, a tiny lens can hide in a smoke detector, or even the shower head.
3. So turn it on, the red lights flash, and you look through this little window.
4. A hidden lens shines right back at you as a bright red dot.
5. At night, hang it on the door handle, and if anybody moves that door, it goes off.
6. It even has a flashlight for when you get up in the dark.
7. Once you have it, you'll be checking every bathroom you walk into.
8. Holiday trips are coming up, so grab two, one for you and one for your bestie.
9. I linked it in the orange cart for you.
Why: the hook promises the one thing none of the winners show (how to use it), the pain names real hiding spots (listing + the 677K shower-head video), lines 3-4 are the how-to and the proof (answers "do these work" and the "just a flashing red light" reviews), then the door alarm and flashlight, a brag-style honest line, real holiday-travel timing with two units, her orange-cart close.
Caption: "Nobody shows you this part 👀 Look through the little window and a hidden lens shines back red. Then hang it on the door at night. #ad #cameradetector #travelsafety #hotelsafety #airbnb #tiktokshopfinds"
Source of each line: research/line_sources.md. No on-screen text unless you say yes (option: "check your hotel room like this").
Flag: both your examples (and 3 top videos) say it "beeps / blasts an alarm the second it finds a camera". Nothing on the box or listing backs that, and a buyer asks "why does mine not beep?". Our script never says it; the alarm is the door alarm.

## 4. Shot list
| # | ~Window (s) | Words | On screen | HAND? | Clip |
|---|---|---|---|---|---|
| S1 | 0.0-4.4 | Listen, y'all have seen these camera finders everywhere... | POV in a navy-tile hotel bathroom: her hand holds the black detector up (back face, buttons), camera walks toward the shower | HAND | Flow first (Omni) |
| S2 | 4.4-7.4 | Let's be for real, a tiny lens can hide in a smoke detector, | Push-in on a white ceiling smoke detector with one tiny black pinhole | HAND-FREE | Seedance 2.0 Mini (Kie) |
| S3 | 7.4-9.6 | or even the shower head. | Tilt up to a chrome rain shower head on navy tile | HAND-FREE | Seedance 2.0 Mini (Kie) |
| S4 | 9.6-13.5 | So turn it on, the red lights flash, and you look through this little window. | POV: thumb presses the power button, a red glow pulses on the wall ahead, the camera moves up to the window (riskiest product clip, made first) | HAND | Flow first (Omni) |
| S5 | 13.5-16.5 | A hidden lens shines right back at you as a bright red dot. | The view THROUGH the window: S2's smoke detector in red, framed by the window's shape, one small red pinpoint on the pinhole (question 3) | HAND-FREE | FREE edit of S2 |
| S6 | 16.5-19.3 | At night, hang it on the door handle, | Hand slips the black loop over a gold door lever, lets go | HAND | Flow first (Omni) |
| S7 | 19.3-21.2 | and if anybody moves that door, it goes off. | The lever dips by itself, the detector swings, its 4 LEDs flash red | HAND-FREE | Flow first (Omni) |
| S8 | 21.2-23.9 | It even has a flashlight for when you get up in the dark. | Night POV in a bedroom: the white beam lights one pool on the floor ahead (question 4) | HAND | Flow first (Omni) |
| S9 | 23.9-26.6 | Once you have it, you'll be checking every bathroom you walk into. | POV in a second hotel bathroom (vessel sinks): detector held up toward the mirror and ceiling vent, pan up | HAND | Flow first (Omni) |
| S10 | 26.6-30.6 | Holiday trips are coming up, so grab two, one for you and one for your bestie. | Open carry-on on the bed: two detectors on folded clothes, her hand takes one | HAND | Flow first (Omni) |
| S11 | 30.6-33.5 | I linked it in the orange cart for you. | End: ONE detector on a teal nightstand by red patterned wallpaper, slow push-in | HAND-FREE | Flow first (Omni) |
Rooms: 6 real photos (rooms/SOURCES.md, Pexels/Pixabay): colourful hotel room, navy-tile bathroom, gold-lever door, red-wallpaper + teal nightstand, colourful-pillow bedroom, vessel-sink bathroom. Bright neutral grade (S8 night: cool blue shade).
Hand: Grace's sheet without the bracelet (as HEVEBLUE; question 2), French tips, her rings, cream knit sleeve. No face, no lip sync.

Real product, from Grace's unit (refs/product_sheet.png, real pixels only; the listing renders are wrong on the window colour): one matte BLACK soft rounded oval, about 6 x 4 x 1.8 cm (about an AirPods case), 50 g, black silicone teardrop loop at the narrow end (~11 cm long overall). Tall rounded window through the middle in a glossy black bezel, filter glass glossy teal-green with a thin red edge (NOT purple). BACK face: 3 tiny speaker holes above the window, 2 pill buttons below (left circle = power, right sun = flashlight). FRONT face: small round black sensor top-left, square white flashlight LED top-right, 4 clear dome LEDs (2 each side of the window) that glow red. USB-C on the side. No logo or text on the device. Size from the listing (4.29 x 1.61 x 0.71 in with the loop).

## 5. Order of work (machine time ~40 min + your stops; each Flow take ~2-3 min on your phone)
All 10 stills at once (S4 and S10 checked first) -> still storyboard on the review page (stop 1) -> S4 Flow kit first, the riskiest (button press + red glow + move to the eye) (stop 2: you make it, I QC it) -> the other 7 Flow kits + S2/S3 on Seedance -> S5 made free from S2 -> VO (Grace cloned v5, echo <= 150 ms) -> cut + QC (2x edges, first second, detector never changes, REMOVED.md, verify_fix) + compare vs @lism792 -> AI finish -> review page (stop 3) -> Drive "Camera Detector (Grace)" as CURRENT.
Free fixes first: trim to the clean window before any redo.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 10 x $0.09 | 0.90 |
| Two likely still redos (the held POV shots are the risk) | 2 x $0.09 | 0.18 |
| S2 + S3 clips (no product), Seedance 2.0 Mini on Kie, 4 s | 2 x $0.164 | 0.328 |
| S5 through-the-window shot (ffmpeg from S2) | 1 x $0 | 0.00 |
| Product clips, Omni 1.1 Flash in your Flow app (12 credits each, 96 credits) | 8 x $0 | 0.00 |
| ...same 8 on Kie only if Flow fails or you can't (asked first) | 8 x $0.315 | 2.52 |
| One likely clip redo, asked before it runs | 1 x $0.315 | 0.315 |
Expected spend with Flow: $1.41. The total includes the Kie fallback so nothing surprises you. (Ralph 2026-10-29: straight to Kie, so expected $3.75: 10 stills + 2 Seedance + 8 Omni.) ElevenLabs: ~700 chars (Grace cloned v5).
Month so far (`python3 grace/spend.py`): $198.55 (no cap in October; $100 cap starts in 4 days).

TOTAL: $4.243

**Approve?**

## 7. Questions
1. Client: this is for Grace (default), or House of Rameau / someone else?
2. Hand: Grace's sheet without the bracelet (default, as HEVEBLUE) or with it?
3. S5: the view through the window is red by nature (every winner shows it) with one small red pinpoint where the lens is, made free in the edit from S2. OK (default), even though it is a red shot and a light dot? Or skip S5 and stay on S4?
4. S8 flashlight: a night shot in cool blue shade so the beam shows (default, like Flashlight V2's dusk), or keep it bright and show the flashlight on in daylight?
5. Stills on Kie ($0.90) or your Gemini app ($0, I send the kit)? Clips in Flow first (default) or straight to Kie?
6. Two-pack: does Grace's shop link carry the 2-pack (the listing has Black-2PCS)? If not, line 8 becomes "grab two".
7. On-screen text: none (default), or "check your hotel room like this" on the opener?

## 7b. Ralph's answers (2026-10-29: "1. Yes 2. Yes 3. Yes ok ( that's does not have to be a hard rule, if needed then we do it 4. Yes 5. Straight to Kie 6. No 7. No")
1. Grace. 2. Hand sheet WITHOUT the bracelet. 3. S5 red through-the-window shot kept (product's own light effects are not a hard no when the product needs them). 4. S8 night flashlight in cool blue shade. 5. Stills on Kie, the 8 product clips straight to Kie (Omni 1.1 Flash, $0.315 each; Seedance first-frame if Omni gives 500s), no Flow kits. 6. Grace's link has no 2-pack: line 8 is "grab two" (as offered in question 6). 7. No on-screen text in Grace's version.
Expected spend now: $3.75 within the $4.243 TOTAL.

## 8. Prompts
Every still and clip prompt: prompts/still_<ID>.txt and prompts/<ID>.txt (built by build_prompts.py from shots.json, written with prompt-master, linted PROMPT_LINT_OK and marked checked). Still refs, numbered and named: 1 product sheet, 2 the real close-up of the face the camera sees (back or front), 3 the room photo, 4 Grace's hand sheet. Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), 2 the real face close-up, 3 sheet, 4 hand sheet. Every prompt: size first (AirPods case), teal-green window never purple, no logo or text on the device, LEDs only on the front face, one grip, never turns or flips, no sparkle words, no text, no music, no voice. S2/S3 (no product): Seedance first frame, no hand at any time.
