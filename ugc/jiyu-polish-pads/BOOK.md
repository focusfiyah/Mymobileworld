# Production Book: JIYU Cleansing Polish Pads (Grace), 2026-10-24

## 1. Job
- Client: Grace  Product: JIYU Cleansing Polish Pads (dual-textured, 60 pads, 150 ml)  Route: hands-only AI + product lock, half face only (`.claude/skills/ugc-product-ad/references/product-lock.md`)
- Job folder: `ugc/jiyu-polish-pads/`  Target length: ~31 s (109 words at Grace's ~3.5 words/s)  Shots: 10 (6 HAND / 4 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/jiyu-polish-pads`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | OK, 3 flags below (kept as written) |
| Audience research | research/audience.md + audience/ (3,447 search phrases, 528 TikTok comments, JIYU reviews) | OK: "rough and bumpy", "how many times a week", break-out worry |
| Coach research (tag/shop + video x6) | research/coach.md, shop/, tag/, videos/ | OK: original pads 336,877 sold; Polish Pads 3,084 sold, 4.8 |
| Daily viral board | research/viral/viral-2026-10-24.json | OK |
| Product facts (source) | research/product_facts.md | OK, every claim on JIYU's own page |
| Hooks modeled on named winners | research/hooks.md | Grace's hook; same "they upgraded it?" pull as @illaalvarez 190K |
| Humanizer | research/humanizer.md, captions.md | OK, no words changed |
| Readability (grade) | research/readability_v1.txt | 8.3, override recorded: Ralph 2026-10-24 "Use script word for word" |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace's, word for word)
> I thought JIYU had already made the perfect toner pad… then they dropped THESE. This is what you grab when your skin needs more than hydration. These are their NEW Cleansing Polish Pads, with two different textures, one side exfoliates, the other smooths. The formula combines multiple exfoliating acids to help with rough texture, clogged pores and blemishes, plus niacinamide to help balance excess oil and improve the appearance of uneven skin tone. Use them up to three times a week at night when your skin needs that extra reset. Especially if your skin's been feeling rough and bumpy instead of baby-smooth, these are linked in the orange cart!

Only change: the long dash after "textures" is a comma (gate bans dashes; no word changed). Every claim is on JIYU's page (multi-acid AHA+BHA+PHA+LHA, niacinamide "balances oil and brightens tone", textured side + soft side, 2-3 times a week). Flags, kept as written: no brag-style confession line, no real-date urgency, the CTA doesn't push more units. Source of each line: research/line_sources.md.

## 4. Shot list
| # | VO words | On screen | HAND? | Face? | Clip | Room |
|---|---|---|---|---|---|---|
| S1 | "I thought JIYU had already made the perfect toner pad…" | Hand holds JIYU's ORIGINAL toner pads jar (peach, lime lid) to camera, small proud tilt | HAND | no | Omni 4 s | B mint tile + wood |
| S2 | "then they dropped THESE." | The NEW jar alone on the vanity, quick push-in | HAND-FREE | no | Omni 4 s | B |
| S3 | "This is what you grab when your skin needs more than hydration." | Hand wraps round the new jar and lifts it | HAND | no | Omni 4 s | B |
| S4 | "These are their NEW Cleansing Polish Pads," | Lid open, pad stack + clear tweezers in the lid, slow orbit | HAND-FREE | no | Omni 4 s | C grey marble + yellow flowers |
| S5 | "with two different textures, one side exfoliates, the other smooths." | Fingers pinch one pad, dimpled side to lens, turn it to the smooth side (RISKIEST: texture + turn) | HAND | no | Omni 4 s | C |
| S6 | "The formula combines multiple exfoliating acids ... blemishes," | Pad in small circles on the cheek near the nose | HAND | half face: cheek/nose side, no eyes, no mouth | Seedance 4 s (pad has no print) | A pink tile |
| S7 | "plus niacinamide ... uneven skin tone." | Smooth even cheek and jaw turning into the light | HAND-FREE | half face, no eyes, no mouth | Seedance 4 s | A |
| S8 | "Use them up to three times a week at night ..." | Evening, bright vanity lights, tweezers lift a pad out of the jar | HAND | no | Omni 4 s | A (night) |
| S9 | "Especially if your skin's been feeling rough and bumpy instead of baby-smooth," | Fingertips glide along a smooth jaw | HAND | half face, no eyes, no mouth | Seedance 4 s | C |
| S10 | "these are linked in the orange cart!" | ONE jar on the marble counter, slow push-in | HAND-FREE | no | Omni 4 s | C |

Face: half face only (Ralph: "don't want ai whole face reveal"), so no eyes and no mouth in any shot: lips on screen during the voiceover would have to move (hard rule 3), so no lip sync needed.
Setting: real Pexels rooms (rooms/SOURCES.md): A pink tile bath, B mint tile + wood vanity, C grey marble + yellow flowers. Bright neutral grade, no text.
Hand: Grace's hand sheet WITHOUT bracelet as on PRITECH (short squared French tips, silver crown ring stack, gold heart-stone ring, blue thumb band) unless you say otherwise.
Real product (refs/product_sheet.png, JIYU's own photos): frosted MINT-AQUA jar, PASTEL PINK flip lid with thumb tab, giant COBALT-BLUE "JIYU" letters, small blue JIYU on the lid, clear tweezers clip in the lid; white round pads, fine dimpled side + flat soft side; 150 ml, 60 pads, ~8.5 cm wide (estimate: no maker dimensions; palm-sized in JIYU's photos). Original toner pads: PEACH jar, LIME-GREEN lid, dark-green JIYU (refs/original_sheet.png). The storyboard's LAVENDER jar and white "100 Pads" jar do not exist; the cut uses the real ones.

## 5. Order of work (machine time ~35-40 min + your review stops)
Stills (all 10 at once) -> still storyboard on the review page (stop 1) -> S5 test clip both ways: Flow kit to you + nothing on Kie unless Flow fails (stop 2) -> the rest at once (Flow kits for S1-S4, S8, S10; Seedance S6, S7, S9 on Kie) while the Grace voice renders (echo gate <=150 ms) -> cut + QC (2x edges, first second, REMOVED.md, verify_fix) + compare vs @illaalvarez -> AI finish -> review page (stop 3) -> Drive.
Free fixes first: crop/retime before any reroll.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 10 x $0.09 | 0.90 |
| Product clips, Omni 1.1 Flash: Flow first on your phone (12 credits each, 84 credits) | 7 x $0 | 0.00 |
| ...same 7 on Kie only if Flow fails or you can't (asked first) | 7 x $0.315 | 2.205 |
| No-product clips, Seedance 2.0 Mini 4 s | 3 x $0.164 | 0.492 |
| One likely redo, asked before it runs | 1 x $0.315 | 0.315 |
Expected spend with Flow: $1.71 ($0.81 if you also make the stills in your Gemini app). Cap below includes the Kie fallback so nothing surprises you. ElevenLabs: ~650 chars (Grace cloned).
Month so far (`python3 grace/spend.py`): $158.70 (no cap in October).

TOTAL: $3.91

## 7. Questions
1. Real jar (pink lid, mint jar, blue JIYU) instead of the storyboard's lavender one? Does Grace have it (a photo of hers helps)?
2. S1 shows JIYU's original toner pads jar (same brand) for "the perfect toner pad": OK?
3. Half face = cheek/jaw/nose side, no eyes, no mouth: OK?
4. Hand sheet without bracelet, French tips (as PRITECH): OK?
5. Stills on Kie ($0.90) or your Gemini app ($0)?
6. On-screen text: the storyboard has captions. Default is none; want any?

## 7b. Ralph's answers (2026-10-24: "Yes, use real jar from question 1, ok, ok, Kie, no captions.")
1. Real jar (pink lid, mint, blue JIYU). 2. S1 original jar OK. 3. Half face (no eyes, no mouth) OK. 4. Not answered: hand sheet without bracelet, French tips, as stated above. 5. Stills on Kie ($0.90, in the TOTAL). 6. No captions, no on-screen text.

## 8. Prompts
Every still and clip prompt is in shots.json (`still`, `clip`), written with prompt-master (Ralph's stack): refs = room photo + hand sheet + refs/closeup_jiyu_front.png + refs/closeup_lid_top.png + refs/product_sheet.png (+ refs/original_sheet.png on S1, refs/closeup_pad_texture.png on S5/S6). Size first (8.5 cm, sits in one palm), true colours in words, one grip, never flips, no ® or ™, hand-free shots say no hand appears at any time.
