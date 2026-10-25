# Production Book: Goth High-Low Skirt v2 (try-on route), 2026-10-23, rev 2026-10-25

## 1. Job
- Client / own content: Grace  Product: dark brown goth high-low drawstring skirt (TikTok Shop listing, research/listing/)  Route: virtual try-on stills (Kling Kolors on fal) + Google Omni clips on Kie (ugc-product-ad references/product-lock.md), tug-cut edit
- Job folder: `ugc/goth-highlow-skirt/`  Target length: 15 s  Shots: 5

## 2. Gate result (`python3 grace/gate.py ugc/goth-highlow-skirt`)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (tag/shop/discover + video x3) | proof/coach_research.md | OK |
| Daily viral board | research/coach (viral board, 2026-10-22) | OK |
| Product facts (source) | research/product_facts.md | OK |
| Hooks modeled on named winners | research/hooks.md | OK (text only on Ralph's yes) |
| Humanizer | proof/humanizer.md | OK (re-checked 2026-10-23) |
| Readability (grade) | proof/readability_v1.txt | grade 1.1 |
| Banned-phrase check | gate.py | OK, GATE OK |

## 3. Script (final, Humanized)
Music-only, like the inspo (@jaquelineee809). No voice, no text unless Ralph says yes. Caption: "Pull the strings and pick your length. Long for the day, short with boots for Halloween night. It's in the orange cart. #ad ..." (scripts.md).
Source of each line: research/line_sources.md (v1 caption + v2 shots table)

## 4. Shot list
| # | Window (s) | VO words | On screen | Face? | VO or lip sync | Prompt notes |
|---|---|---|---|---|---|---|
| L1 HAND | 0-3 | none (music) | front, skirt just above the knee, both hands on the two front waist strings, one tug | yes, no lip sync (music) | n/a: music-only | Omni: one small tug up and out from the waist, the hem stays put |
| L2 HAND-FREE | 3-6 | none | back view, long ruffled back tiers swing, then a half turn to the side | no (back) | n/a: music-only | Omni: no hand touches the skirt |
| L3 HAND | 6-9 | none | one side up, one leg out to JUST above the knee | yes | n/a: music-only | Omni: she shifts her weight onto that leg |
| L4 HAND | 9-12 | none | shortest: both sides up, back still long | yes | n/a: music-only | Omni: hands at the waist strings, small sway |
| L5 HAND-FREE | 12-15 | none | shortest, steps toward camera, crosses one leg | yes | n/a: music-only | Omni: no hand touches the skirt |
Outfit: black fitted long-sleeve top (Ralph 2026-10-25, the cut 1 top, put on by try-on) + the real brown skirt, black sheer tights, feet in frame  Setting: Grace's own room from her 4 body photos (sun mirror, fiddle-leaf plant, blue curtain, oak floor; grace/ref/body/)  Nails / person details: Grace's own, unchanged by try-on  Real product confirmed (top, cap, label): drawstrings at the FRONT waistband, solid dark chocolate brown, long ruffled back (research/inspo_beats.md product truths)

Stills (Kling Kolors try-on, fal), two passes per look: pass 1 puts the black long-sleeve top on (garment tryon/garment_top_black_ls.jpg, cropped from the approved FULL2 still), pass 2 puts the real skirt on that result
| Look | Grace photo (grace/ref/body/) | Real listing photo (skirt) |
|---|---|---|
| L1 knee | front.jpg | 07 (on model, front at the knee) |
| L2 back | back.jpg | 30 (product, back view) |
| L3 one leg | front_face.jpg | 06 (on model, one side up to the knee) |
| L4 shortest | front.jpg | 01 (on model, front up to the upper thigh) |
| L5 step | the L4 still (same look) | n/a: reuses the L4 still |

## 5. Order of work
Still storyboard first: the riskiest still (L4 shortest, does try-on keep a pulled-up length?) first as the ONE test still, then the other three, every still checked at 2x against the product truths, then the storyboard to Ralph. Clips: L1 first as the ONE test clip, then the batch after his OK.
Free fixes planned: colour shift toward the real chocolate brown (round 26 read a little khaki); crop to the same framing on every look; AI finish last.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Kolors try-on, top pass (fal) | 4 x $0.07 | 0.28 |
| Kolors try-on, skirt pass (fal) | 4 x $0.07 | 0.28 |
| Omni clips 4 s (Kie) | 5 x $0.315 | 1.575 |
Total Kie: $1.575  fal: $0.56  ElevenLabs: 0 chars (music-only)  Contingency redos (each asked separately): up to $0.50 (redo cap for this job)
Month so far (`python3 grace/spend.py`): $151.67 (no cap in October)

TOTAL: $2.14

**Approve?**

## 7. Questions (all of them, now)
Answered by Ralph 2026-10-25: (1) "Neck down"; (2) "No, wanted her legs to show with the boots" (bare legs + black knee-high boots, no tights). Plan needs a new step + new total before approval.

1. Grace wears a pink satin head wrap in all 4 photos. Crop every shot from the neck down (like cut 1's waist-down framing), or keep her face in?
2. The body photos are sheer black tights, so her legs read as black tights under the skirt in the short looks. OK?

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| L1-L4 stills | Kling Kolors try-on (fal) | no text prompt: pass 1 human_image_url = Grace photo, garment_image_url = tryon/garment_top_black_ls.jpg; pass 2 human_image_url = pass 1 result, garment_image_url = real listing photo (table above) |
| L1-L5 clips | Omni on Kie (omni_clip.py) | prompts/v2_L1..L5.txt: ref 1 = the approved still (first frame), ref 2 = real front close-up refs/closeup_ruching.png, ref 3 = refs/product_sheet.png; "the skirt must match reference 2 and 3 fold for fold and colour for colour; drawstrings only at the front waistband; no hand lifts the hem; solid fabric, legs never show through" + the move from section 4 |
