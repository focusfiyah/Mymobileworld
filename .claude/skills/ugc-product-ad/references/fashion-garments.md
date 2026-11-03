# Fashion garments on a person (dress, skirt, mirror selfie)

Not every garment video is the same job. Decide the type first; the type decides the route and what can be promised.
Evidence is dated; what was only seen on someone else's video, not tested by us, is marked.

## Contents
1. Which type is it
2. Type A: the garment hangs and sways
3. Type B: the garment changes shape on camera
4. Mirror and room details that cost us rounds
5. Where the records are

## 1. Which type is it
- **A: hangs and sways** (a dress, a skirt, a sweater set; a mirror selfie or a standing shot; small weight shifts, a hand on the hair or hip).
- **B: changes shape on camera** (adjustable strings, wrap, convertible, length that changes).
Say the type in the plan before the first still. Type B is capped at two tests (Mymobileworld CLAUDE.md "Garments that change shape", Ralph 2026-11-03).

## 2. Type A: the garment hangs and sways
- What good ones look like (@ttsjourney1's two example clips, 2026-11-03, seen only, model and settings unknown): about 4 s, one camera, almost no motion, a bright real-looking room, print and hands steady. His cost was $0.90 to $1.25 per clip, more than our routes (Seedance Mini 5 s about $0.21, Flow $0). So the lever is the starting still, not the price per clip.
- Our route: a clean still from the real product photos (Gemini 3 Pro Image, or Ralph's Gemini app at $0) in a real room photo, then a short low-motion clip, Flow first (product lock, `references/product-lock.md`). Not yet tested by us on a dress; the Goth skirt knee shot below is the nearest pass.
- A neck-down 9:16 frame (no head) kept faces out of the drift on the goth job.

## 3. Type B: the garment changes shape on camera
What failed on the Goth High-Low Skirt (2026-10-22 to 10-25, $3.46 Kie + $0.21 fal + Kling and Flow credits, about 40 review rounds, stopped by Ralph):
- Kie: Omni reference + first/last frame, Seedance reverse + first/last, Veo: none shortened the skirt by its strings.
- Try-on (Kolors on fal): kept the real skirt design in one test, then copied the corset top and drew the hem below the knee; olive band on the shorts. FASHN only worked over separate bottoms.
- Flow Omni Flash: knee-length bedroom-mirror shot PASSED (strings and ruching kept, hands take the strings at the waistband, boots right). Back view: 0 to 2.2 s fine, then it added a turn, a phone and lighter hands; re-prompting "no turn, no phone" did not help, the free trim did. Nothing showed the strings pulling the skirt up.
What worked: the **tug-cut**: one moving clip per look (back, top of knee, mid-thigh, one leg, shortest), the length changing on a cut as her hand tugs. 11.7 s, approved, in Drive.
What real examples look like: every adjustable-length skirt video found on 2026-11-03 (the inspo @jaquelineee809, the top adjustable-skirt videos) is real footage. Grace's own two posts of the same skirt (@shewiththeglow 7702124355597176094 and 7702136461998574879) show the real pull on her in her bedroom.
Next time, in this order: (1) tug-cut as the plan; (2) if Ralph wants the pull itself, ONE test with frames of Grace's real pull as references (start, middle, pulled; not yet tried); (3) if that fails, stop and offer Grace filming that beat for real.

## 4. Mirror and room details that cost us rounds
- Keep the inspo's setting and camera: a bedroom with a full-length mirror, waist to floor, not Grace's plain room straight on (Ralph 2026-10-25). Pick a real room photo the Vans V12 way (`rooms.py`, different photo, same kind of place; goth v2 used Pexels 4993094).
- Skin tone: use Grace's real hand sheet `grace/ref/hand-sheets/` (no-jewellery sheet), not a description; Flow gave lighter hands in the turn (Ralph caught it).
- Phones: "mirror-style photo" makes the model add a phone at her face. If the shot has no phone, write "a friend films her from the side, her hands hold no phone" (OQQ pants 2026-10-26).
- Name the real details in words and pass a close-up: the exact top, the strings, the hem shape, the boots. The model copies whatever top is in the reference (a corset in the try-on test).
- Flow can start from a different pose than the still; trim, do not re-prompt (L2).

## 5. Where the records are
`ugc/goth-highlow-skirt/` (README Status, `tryon/QC.md`, `research/`, `prompts/`, `rooms/SOURCES.md`); Brain notes `Goth High-Low Skirt`, `Grace goth skirt own videos`, `ttsjourney1 cheap AI shop video`; `grace/PLAYBOOK.md` §6.
