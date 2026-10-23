# Production Book: Goth High-Low Skirt v2 (try-on route), 2026-10-23

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
| L2 HAND-FREE | 3-6 | none | 3/4 side turn, long ruffled back tiers swing | yes | n/a: music-only | Omni: no hand touches the skirt |
| L3 HAND | 6-9 | none | one side up, one leg out to JUST above the knee | yes | n/a: music-only | Omni: she shifts her weight onto that leg |
| L4 HAND | 9-12 | none | shortest: both sides up, back still long | yes | n/a: music-only | Omni: hands at the waist strings, small sway |
| L5 HAND-FREE | 12-15 | none | shortest, steps toward camera, crosses one leg | yes | n/a: music-only | Omni: no hand touches the skirt |
Outfit: black shapewear top/cincher (from Grace's frame) + the real brown skirt, bare legs, frame ends mid-shin  Setting: Grace's own white room from her TikTok (@shewiththeglow 7684001442977352991)  Nails / person details: Grace's own, unchanged by try-on  Real product confirmed (top, cap, label): drawstrings at the FRONT waistband, solid dark chocolate brown, long ruffled back (research/inspo_beats.md product truths)

Stills (Kling Kolors try-on, fal): person frame + real listing photo per look
| Look | Grace frame | Real listing photo |
|---|---|---|
| L1 knee | tryon/poses/P_waist.jpg (hands at the waist) | 07 (on model, front at the knee) |
| L2 side | tryon/poses/P_side.jpg | 29 (product, side view) |
| L3 one leg | tryon/poses/P_front.jpg | 06 (on model, one side up to the knee) |
| L4 shortest | tryon/poses/P_waist.jpg | 01 (on model, front up to the upper thigh) |
| L5 step | the L4 still (same look) | n/a: reuses the L4 still |

## 5. Order of work
Still storyboard first: the riskiest still (L4 shortest, does try-on keep a pulled-up length?) first as the ONE test still, then the other three, every still checked at 2x against the product truths, then the storyboard to Ralph. Clips: L1 first as the ONE test clip, then the batch after his OK.
Free fixes planned: colour shift toward the real chocolate brown (round 26 read a little khaki); crop to the same framing on every look; AI finish last.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Kolors try-on stills (fal) | 4 x $0.07 | 0.28 |
| Omni clips 4 s (Kie) | 5 x $0.315 | 1.575 |
Total Kie: $1.575  fal: $0.28  ElevenLabs: 0 chars (music-only)  Contingency redos (each asked separately): up to $0.50 (redo cap for this job)
Month so far (`python3 grace/spend.py`): $151.67 (no cap in October)

TOTAL: $1.86

**Approve?**

## 7. Questions (all of them, now)
1. Back view: no back frame of Grace exists in this room, so L2 is a 3/4 side turn. OK, or will Grace film 3 s of her back in that room ($0)?
2. Boots: Grace's frame ends mid-shin, so no boots show. OK?
3. The black shapewear band shows above the skirt (it reads as a black corset top). OK?

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| L1-L4 stills | Kling Kolors try-on (fal) | no text prompt: human_image_url = Grace frame, garment_image_url = real listing photo (table above) |
| L1-L5 clips | Omni on Kie (omni_clip.py) | prompts/v2_L1..L5.txt: ref 1 = the approved still (first frame), ref 2 = real front close-up refs/closeup_ruching.png, ref 3 = refs/product_sheet.png; "the skirt must match reference 2 and 3 fold for fold and colour for colour; drawstrings only at the front waistband; no hand lifts the hem; solid fabric, legs never show through" + the move from section 4 |
