# Production Book: Migrastil Neuropathy Cream (Grace)

Sent to Ralph: https://claude.ai/artifact/DGT4x42YffAsWTvEfBz3oS (2026-11-06)

## 1. Job
- Client: Grace  Product: Migrastil Extra Strength Neuropathy Cream, 4 oz jar (TikTok Shop; 109,295 sold)  Route: hands + hand-free product ad, music only (references/hands-only-and-demo.md + product-lock.md)
- Job folder: `ugc/migrastil-neuropathy-cream/`  Target length: 13.5 s (Grace: 12-15 s)  Shots: 6 (3 hand-free)
- Ask: Grace, Telegram group 2026-11-06 ("Ai video needed for this", 12-15 s). Ralph tapped: music only (Grace adds music) + VO script; share the storyboard with Grace too.
- Photos: Grace's 2 real photos (front + back, lid on). Sheet: refs/product_sheet.png. The cream itself is not in any photo (question 3).

## 2. Gate result (`python3 grace/gate.py ugc/migrastil-neuropathy-cream`): GATE OK
| Proof | File | Result |
|---|---|---|
| Audience research | research/audience.md + audience/voc.md | OK |
| Grace research workflow | research/RESEARCH.md (7 sections, verdict, 4 roles) | OK |
| Playbook rules read | research/playbook.md | OK |
| Coach research (tag/shop/discover + video x3) | research/coach.md (top 3: @aunteeknows 1.3M, @jeff_el_colombiano 1.2M, @amazingaffiliate 1.2M) | OK (tag pages returned 0, logged) |
| Daily viral board | research/viral/viral-2026-11-06.json (top: @lylhealth 14 s hands-only) | OK |
| Product facts (source) | scripts.md, product_truth.json, research/product_facts.md | OK |
| Hooks modeled on named winners | research/hooks.md (H066 used; H005, H151 options) | OK |
| Humanizer | research/humanizer.md | OK |
| Readability (grade) | research/readability_v1.txt | 2.5 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized)
Music only in this cut. VO script for Grace to record later (112 words, about 34 s at her pace):
This is such a specific problem, but if you have it, you know. / The second I lie down, my feet start burning and tingling. / And most creams I tried made it burn even more. / Now I keep this Migrastil cream on my nightstand. / I rub a little on my feet before bed, and it sinks right in without feeling greasy. / There's no menthol in it, just a light smell from the oils. / People say they sleep like a baby now, and I get it. / The only problem? My mom wants her own jar. / Cold nights are coming, so grab one for you and one for your mom. / It's in the orange cart.
Hook H066 word for word. Source of each line: research/line_sources.md. Claims kept out: cure, heals nerves, restless legs, circulation, 2-4 weeks, any time promise.
Caption: "my feet start up the second I lie down #ad". On-screen hook text: none (options in research/hooks.md, only on your yes).

## 4. Shot list
| # | Window (s) | VO words | On screen | Face? | VO or lip sync | Prompt notes |
|---|---|---|---|---|---|---|
| S1 | 0.0-2.2 | (music only; VO later) | Bare feet at the bed edge, one rubs the other, toes curl (sage bedroom) | no | none | HAND-FREE, no product, Seedance 2.0 Mini on Kie |
| S2 | 2.2-4.4 | (music only; VO later) | Hand lifts the closed jar off the wooden nightstand, label to camera | no | none | HAND, product, Flow (Omni), else Wan 3.0 720P on Kie |
| S3 | 4.4-6.8 | (music only; VO later) | Fingertips rub a dab of cream into the top of a bare foot on the duvet | no | none | HAND, no product, Seedance 2.0 Mini on Kie |
| S4 | 6.8-8.8 | (music only; VO later) | Fingers rub the last of the cream into the back of a hand (yellow sofa) | no | none | HAND, no product, Seedance 2.0 Mini on Kie |
| S5 | 8.8-11.0 | (music only; VO later) | Relief: feet slide under the duvet, toes relax, push-in | no | none | HAND-FREE, no product, Seedance 2.0 Mini on Kie |
| S6 | 11.0-13.5 | (music only; VO later) | END: the jar alone on the white nightstand by the bright window, dolly-in | no | none | HAND-FREE, product, Flow (Omni), else Wan 3.0 720P on Kie |
Outfit: n/a (hands and bare feet only)  Setting: real Pexels rooms (rooms/SOURCES.md): sage bedroom (S1, S2, S3, S5), yellow-sofa living room (S4), bright window bedroom (S6)  Nails / person details: Grace's no-jewellery hand sheet (medium-brown skin, mauve-pink French tips, no rings/bracelet/watch); bare feet, short unpolished toenails  Real product confirmed (top, cap, label): from Grace's photos: dark cobalt-blue 4 oz jar, glossy black screw lid, navy label, green NON-BURNING RELIEF band, MIGRASTIL / Neuropathy Cream, USA shield. The jar stays closed in every shot (no open jar until the cream is confirmed).
Different from Grace's earlier videos: new product, new rooms, hook H066 not used on her recent jobs.

## 5. Order of work
6 stills (storyboard, to you and Grace before any clip) -> riskiest clip first (S2, hand lifting the jar) as the ONE test clip -> rest in parallel -> free cut, no audio track for Grace's music -> ai_finish -> QC (2x edges, label at 2x, grip, cream ON the foot, drift) -> review page. Time: about 35-40 min machine time after your OK, plus your two review stops (stills, cut).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Nano Banana Pro on Kie | 6 x $0.09 | 0.54 |
| Product clips (S2, S6), Wan 3.0 720P 5 s on Kie + free upscale | 2 x $0.40 | 0.80 |
| No-product clips (S1, S3, S4, S5), Seedance 2.0 Mini 4 s | 4 x $0.164 | 0.66 |
| Likely redo: 1 still + 1 Wan clip (each asked first) | | 0.49 |
| Music | Grace adds her own | 0 |
Free routes instead: your Flow app for S2/S6 (2 x 12 = 24 credits) with Kie stills = $1.45; your Gemini app stills + Flow clips = Seedance only $0.66 + a likely redo $0.16 = $0.82.
Month so far (`python3 grace/spend.py`): $30.08 of $100 (left $69.92).

TOTAL: $2.49

**Approve?**

## 7. Questions (all of them, now)
1. Route: all on Kie ($2.49), Kie stills + your Flow clips ($1.45), or your Gemini + Flow kit ($0.82)?
2. Grace's hands: the no-jewellery sheet (prompts written for it), or with/without bracelet?
3. The cream colour: not in Grace's photos. Plain white cream (prompts written that way), or ask Grace for a photo of the open jar first?

## 8. Prompts (final, written with prompt-master; linted PROMPT_LINT_OK)
For product clips: image 1 the approved still, image 2 label close-up (refs/closeup_label.png), image 3 green band close-up (refs/closeup_band.png), image 4 the sheet.
| Item | Model | Prompt |
|---|---|---|
| S1 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: grace/ref/hand-sheets/no_jewelry.jpg, rooms/roomA_sage_bedroom.jpg. Image 1 is Grace's real hands (for skin tone), image 2 the room. Low close-up at floor level, camera beside the bed in the sage-green bedroom from image 2: two bare feet resting on the floor at the edge of the bed, the white duvet edge hanging just above them, the toes slightly curled. Feet: bare feet of a Black woman with medium-brown skin matching image 1, short natural toenails with no polish, no socks, no jewellery. No hands, no product, no jar, no other people. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S1 clip | Seedance 2.0 Mini on Kie | One bare foot slowly rubs the top of the other foot and the toes curl, then relax. Camera steady, slight handheld drift. No hands, fingers or product appear at any time. No music, no voice, no text. 4 seconds. |
| S2 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: refs/product_sheet.png, refs/closeup_label.png, refs/closeup_band.png, grace/ref/hand-sheets/no_jewelry.jpg, rooms/roomA_sage_bedroom.jpg. Image 1 is the product reference sheet, image 2 the real front label close-up, image 3 the real green band close-up, image 4 Grace's real hands, image 5 the room. Close-up, camera at nightstand height: the closed jar stands on the small wooden nightstand of the sage-green bedroom from image 5, label facing the camera, the white lamp soft behind it. One RIGHT hand comes in from the right edge and wraps around the jar, thumb on the near side and four fingers around the back, lifting it a few centimetres off the nightstand. The jar fills about the hand's palm. The product is the real Migrastil Extra Strength Neuropathy Cream 4 oz jar: a round jar with straight sides, about 7 cm wide and about as tall as it is wide with the lid on, small enough to hold in one palm. Glossy dark cobalt-blue jar with a wide glossy black screw lid with a smooth top. A navy label wraps the middle. At the top of the label a lime-green band with navy bold 'NON-BURNING RELIEF' on two lines and, to its right, a white hand icon on a blue square. Below it: 'MIGRASTIL' in white bold serif capitals, 'Extra Strength' in small white letters, 'Neuropathy' and 'Cream' in large lime-green rounded letters, 'Gentle, Non-Burning Relief' in small white letters, a thin lime-green line, 'NET WT 4 oz. (113 g)' in white; white curved arcs at the lower left and a red, white and blue USA shield with 'Made in the USA' at the lower right. The label print MUST match image 2 letter for letter and colour for colour, the green band MUST match image 3. The jar stays closed with its black lid on: no white jar, no clear jar, no tube, no pump, no box. Hands: Grace's real hands from image 4, copied exactly: medium-brown skin with lighter palms, medium-length squoval nails with mauve-pink polish and white French tips, no rings, no bracelet, no watch; each hand enters from the frame edge with the whole wrist visible. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S2 clip | Flow (Omni), else Wan 3.0 720P on Kie | Recreate image 1 exactly as the first frame. The hand lifts the jar slowly up and a little toward the camera in one small move, holding it the same way the whole time. The jar does not turn, tip or open; the label stays facing the camera. The label must match image 2 letter for letter and colour for colour, the green band must match image 3, the jar must match image 4 (the product reference sheet), the jar stays the same size in every frame. No music, no voice, no text. 5 seconds. |
| S3 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: grace/ref/hand-sheets/no_jewelry.jpg, rooms/roomA_sage_bedroom.jpg. Image 1 is Grace's real hands, image 2 the room. Close-up from above: one bare foot rests on the white duvet of the bed in the sage-green bedroom from image 2; the fingertips of one RIGHT hand rest on the top of the foot with a small dab of white cream on it, the cream sitting directly under the fingertips on the top of the foot. The cream is a small dab of smooth white cream. Feet: bare feet of a Black woman with medium-brown skin matching image 1, short natural toenails with no polish, no socks, no jewellery. Hands: Grace's real hands from image 1, copied exactly: medium-brown skin with lighter palms, medium-length squoval nails with mauve-pink polish and white French tips, no rings, no bracelet, no watch; each hand enters from the frame edge with the whole wrist visible. No jar, no product, no other people. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S3 clip | Seedance 2.0 Mini on Kie | The fingertips rub the cream into the top of the foot in slow small circles, the cream spreading on that spot and sinking in. Same hand position the whole time; the foot stays still. Camera steady. No jar or product appears at any time. No music, no voice, no text. 4 seconds. |
| S4 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: grace/ref/hand-sheets/no_jewelry.jpg, rooms/roomB_yellow_sofa.jpg. Image 1 is Grace's real hands, image 2 the room. Close-up of two hands in front of the yellow sofa from image 2, sofa soft and out of focus: the RIGHT hand's fingers rub a thin sheen of white cream into the back of the LEFT hand. Hands: Grace's real hands from image 1, copied exactly: medium-brown skin with lighter palms, medium-length squoval nails with mauve-pink polish and white French tips, no rings, no bracelet, no watch; each hand enters from the frame edge with the whole wrist visible. No jar, no product, no face, no other people. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S4 clip | Seedance 2.0 Mini on Kie | The right hand's fingers rub the cream into the back of the left hand in slow strokes until it sinks in. Same two hands, same positions. Camera steady, slight handheld drift. No jar or product appears at any time. No music, no voice, no text. 4 seconds. |
| S5 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: grace/ref/hand-sheets/no_jewelry.jpg, rooms/roomA_sage_bedroom.jpg. Image 1 is Grace's real hands (for skin tone), image 2 the room. Close-up at mattress height at the foot of the bed in the sage-green bedroom from image 2: two bare feet just tucked under the edge of the white duvet, only the toes and the tops of the feet showing, relaxed. Feet: bare feet of a Black woman with medium-brown skin matching image 1, short natural toenails with no polish, no socks, no jewellery. No hands, no product, no jar, no other people. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S5 clip | Seedance 2.0 Mini on Kie | Slow push-in as the feet slide a little further under the duvet and the toes relax. No hands, fingers or product appear at any time. No music, no voice, no text. 4 seconds. |
| S6 still | Nano Banana Pro on Kie (or your Gemini app, free) | refs: refs/product_sheet.png, refs/closeup_label.png, refs/closeup_band.png, rooms/roomC_bright_bedroom.jpg. Image 1 is the product reference sheet, image 2 the real front label close-up, image 3 the real green band close-up, image 4 the room. On top of the small white nightstand beside the bed by the bright window in the bedroom from image 4: ONE closed jar standing upright, label facing the camera, the white lamp beside it. The jar is small: about a third of the lamp's height. No hands, no people. The product is the real Migrastil Extra Strength Neuropathy Cream 4 oz jar: a round jar with straight sides, about 7 cm wide and about as tall as it is wide with the lid on, small enough to hold in one palm. Glossy dark cobalt-blue jar with a wide glossy black screw lid with a smooth top. A navy label wraps the middle. At the top of the label a lime-green band with navy bold 'NON-BURNING RELIEF' on two lines and, to its right, a white hand icon on a blue square. Below it: 'MIGRASTIL' in white bold serif capitals, 'Extra Strength' in small white letters, 'Neuropathy' and 'Cream' in large lime-green rounded letters, 'Gentle, Non-Burning Relief' in small white letters, a thin lime-green line, 'NET WT 4 oz. (113 g)' in white; white curved arcs at the lower left and a red, white and blue USA shield with 'Made in the USA' at the lower right. The label print MUST match image 2 letter for letter and colour for colour, the green band MUST match image 3. The jar stays closed with its black lid on: no white jar, no clear jar, no tube, no pump, no box. Bright neutral daylight, true colours, vertical 9:16 photo, realistic phone-camera look. No text, no captions, no logos other than the real label, no light effects. |
| S6 clip | Flow (Omni), else Wan 3.0 720P on Kie | Recreate image 1 exactly as the first frame. Slow dolly-in toward the jar on the nightstand. Nothing moves except the camera. No hands, fingers or people appear at any time. The label must match image 2 letter for letter and colour for colour, the green band must match image 3, the jar must match image 4 (the product reference sheet), the jar stays the same size in every frame. No music, no voice, no text. 5 seconds. |
