# Production Book: BodyJ castor 15 s videos, round 5 (Grace), 2026-10-23

## 1. Job
- Client: Grace  Product: BodyJ4You castor oil roll-on (50 ml)  Route: hands-only AI + product lock (Omni on Kie), round-4 rooms kept
- Job folder: `ugc/bodyj-castor-rollon/remix15/`  Videos: 4 (V1 15 s, V2 15 s, V3 19 s, V4 15.5 s), voices unchanged (approved E voices)
- Ralph's notes on round 4 (2026-10-23): "v1 it shows a head missing" + "her hands do not stay true to Graces skin tone, it looks like a different hand with a different skin tone"

## 2. Gate result
Script gate for the job: GATE OK (scripts unchanged since round 2; `python3 ../../../grace/gate.py .`). Free check of round 4: `qc/r5/FINDINGS.md`
(3 frames per shot next to Grace's real hand sheet, `qc/r5/r4_v1..4_shots.jpg`).
Root cause: round 4 used an old AI hand crop (`redo/hand_ref.png`) and a prompt that said "short natural nude nails, no rings", and the
clips got no hand reference at all. So no shot has Grace's French tips or rings, and the tone drifts shot to shot. Six hand-free shots
(V1i, V2b, V2h, V3g, V4b, V4f) came back with a pale white hand Seedance added on its own.

## 3. Script
Unchanged, Grace's 4 scripts word for word (`scripts.json`), voices `vo/v1..v4.mp3` (no new voice spend).

## 4. Shot list (only what changes; every other shot stays as in round 4)
| Shot | Words | New picture | HAND / FREE | Why |
|---|---|---|---|---|
| V1b | why is it so messy | oil through her cupped hands onto the tub rim | HAND | tone lighter/golden |
| V1c | this roll-on is genius | hand lifts the roll-on, only hand + wrist in frame | HAND | tone lighter |
| V1d | no pouring, no oily fingers | rolls the back of her hand (TEST CLIP) | HAND | nails, rings, tone |
| V1e | brows | brow only, Grace's face sheet as a ref | HAND | a different woman's face |
| V1f | cuticles | rolls cuticles on a towel | HAND | nails, rings |
| V1g | dry skin | elbow + forearm ONLY, no shoulder or chest | HAND | HEADLESS (arm up, torso, no head) |
| V1h | shine to your hair | hair ends across her palm ONLY, no shoulder | HAND | HEADLESS (hair over shoulder, no head) |
| V1i | orange cart | free fix: the clean 1.1 s before the white hand enters, played forward then back | FREE | pale hand at 1.15 s |
| V2a | thick and messy | oil over a spoon on the marble | HAND | tone lighter |
| V2b | liquid gold | clip only, round-4 still, "no hands at any time" | FREE | pale hand added |
| V2c | this roll-on | lifts the roll-on, hand + wrist only | HAND | nails, rings |
| V2d | targeted | one spot on the inner wrist | HAND | nails, rings |
| V2e | brows / hair | brow into the hairline, Grace's face sheet | HAND | lighter face, different woman |
| V2f | cuticles / dry skin | cuticles then knuckles | HAND | nails, rings |
| V2h | orange cart | clip only, round-4 still, "no hands at any time" | FREE | pale hand at 0.5 s |
| V3c | skin and nails | nails and cuticles on the counter | HAND | nails, rings |
| V3d | had to get it | pulls the roll-on out of the box | HAND | nails, rings |
| V3e | no oily fingers | inner forearm, fingers open clean | HAND | nails, rings |
| V3f | roll it where you need it | wrist and forearm (was neck/collarbone, cut at the jaw) | HAND | reads headless |
| V3g | orange cart | free fix: clean 1.65 s, forward then back | FREE | pale hand at 1.8 s |
| V4b | USDA organic... | clip only, round-4 still, "no hands at any time" | FREE | pale hands the whole shot |
| V4c | so much easier | long stroke on the forearm | HAND | nails, rings |
| V4d1 | brows | brow only, Grace's face sheet | HAND | different woman |
| V4d2 | dry cuticles | thumb + index cuticles | HAND | nails, rings |
| V4d3 | rough skin | elbow + forearm only | HAND | nails, rings, tight crop |
| V4d4 | hair ends | hair ends across her palm only | HAND | reads headless |
| V4e | without the oily mess | clean dry fingertips | HAND | nails, rings |
| V4f | orange cart | free fix: clean 1.85 s, forward then back | FREE | hand at 2.0 s |
Kept as is: V1a, V3a, R3 (grandma, meant to differ), V4a, V4a2. Hand shots: Grace's hand sheet (with or without bracelet, Ralph picks)
passed as a reference on every still AND every clip. Outfit: dusty mauve tee sleeve. Rooms: round-4 rooms (one per video).

## 5. Order of work
Free fixes done (V1i, V3g, V4f, preview on the review page) → 22 stills at once → QC 2x vs the hand sheet → still sheet on the review
page → ONE test clip (V1d, both hands + product) → the other 24 clips at once → cuts (`cut.py N --final`, only changed shots) →
qc.py, check.py cuts, gate --stage cut, REMOVED.md, 2x zooms, AI finish → review page, Drive, email. About 2 to 2.5 hours after the OK.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Kie nano-banana-pro 1K | 22 x $0.09 | 1.98 |
| Product clips, Omni 1.1 Flash on Kie, 4 s | 23 x $0.315 | 7.245 |
| No-product clips (V1b, V2a), Seedance 2.0 Mini 4 s | 2 x $0.164 | 0.328 |
| One likely redo (one still + one Omni clip) | $0.09 + $0.315 | 0.405 |
| Free fixes V1i, V3g, V4f | 3 x $0 | 0.00 |
Kie balance now 771 credits = $3.86: a top-up of about $6.10 is needed before the batch (the stills and the test clip fit).
Month so far (`python3 grace/spend.py`): $154.23 (no cap in October). This job so far: Kie ~$16.28 (round 3 ~$11.14 + round 4 ~$5.14).
Smaller option B (only the clearly wrong + headless shots: V1b V1c V1e V1g V1h V2a V2e + V2b V2h V4b clips): $3.88; nails and rings
would still not match in the other 15 hand shots.

TOTAL: $9.96

## 7. Questions (all of them, now)
1. Grace's hand sheet for these videos: with the bracelet or without?
2. Redo list: all 25 shots above (TOTAL $9.96), or option B ($3.88)?
3. Google Flow trial (your standing rule): I make the test clip V1d on Kie Omni, and you make the same clip free in Flow from a kit on the review page? (yes / skip this time)

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt files |
|---|---|---|
| 22 stills | Kie nano-banana-pro (Gemini 3 Pro Image), 9:16 1K | `r5/prompts/<with|without>/<ID>_still.txt` (refs listed on the last line: product sheet, real front label, box sheet where shown, Grace's hand sheet, Grace's face sheet on brow shots, the round-4 room) |
| 23 product clips | Kie google/gemini-omni-flash-1-1, 4 s (`r5.py clip`, via omni_clip.py) | `r5/prompts/<sheet>/<ID>_clip.txt`: image 1 still, 2 real front label, 3 product sheet, (4 box), last Grace's hand sheet |
| V1b, V2a clips | Kie bytedance/seedance-2-mini, 4 s | `r5/prompts/<sheet>/V1b_clip.txt`, `V2a_clip.txt`: image 1 still, image 2 Grace's hand sheet |
Generator: `r5.py` (`python3 r5.py prompts --sheet with|without`). Every hand prompt opens with Grace's skin tone copied from her sheet,
French tips, crown ring stack, heart-stone ring, blue thumb band; every one has the no-headless framing rule.
