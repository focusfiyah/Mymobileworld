# Production Book: Goth High-Low Skirt v2 (try-on route), 2026-10-23, rev 4 2026-10-25 (bare legs + boots, neck down; step A in Ralph's Gemini app)

## 1. Job
- Client / own content: Grace  Product: dark brown goth high-low drawstring skirt (TikTok Shop listing, research/listing/)  Route: one base edit per Grace body photo (black long-sleeve top + bare legs + black knee-high boots; Ralph's Gemini app $0 first, else Kie nano-banana-pro) -> real skirt put on by virtual try-on (Kling Kolors on fal) -> clips Flow first ($0), Google Omni on Kie only when Flow can't (ugc-product-ad references/product-lock.md), tug-cut edit
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
Outfit: black fitted long-sleeve top (Ralph 2026-10-25, the cut 1 top) + the real brown skirt + BARE LEGS + black knee-high boots, flat lug sole, the cut 1 boots (refs/boots_cut1.png) (Ralph 2026-10-25: "No, wanted her legs to show with the boots"); every shot cropped from the NECK DOWN (Ralph 2026-10-25: "Neck down"), feet in frame  Setting: Grace's own room from her 4 body photos (sun mirror, fiddle-leaf plant, blue curtain, oak floor; grace/ref/body/)  Nails / person details: Grace's own, unchanged by try-on  Real product confirmed (top, cap, label): drawstrings at the FRONT waistband, solid dark chocolate brown, long ruffled back (research/inspo_beats.md product truths)

Stills, two steps per look:
- Step A, base edit (3 photos, L1 and L4 share front.jpg): top + bare legs + boots in ONE edit, prompts/v2_base_front.txt and v2_base_back.txt (written with prompt-master), refs: image 1 = Grace photo, image 2 = tryon/garment_top_black_ls.jpg (the cut 1 top), image 3 = refs/boots_cut1.png (the cut 1 boots). Ralph 2026-10-25: "Gemini": he runs the 3 edits in his Gemini app ($0) from the kit I send (flow_kit-style folder tryon/gemini_kit/), sends the results back, I QC them at 2x (bare legs match his arms, boots right foot/left foot, top, nothing else changed). A failed edit gets a second Gemini try, not a paid one; Kie only on his word with the cost.
- Step B, skirt try-on (Kolors, fal, no text prompt): human_image_url = the step A result, garment_image_url = the real listing photo below. Then free fixes: colour shift to the real chocolate brown (70,51,46), neck-down crop, same framing on every look.
| Look | Grace photo (grace/ref/body/) | Real listing photo (skirt) |
|---|---|---|
| L1 knee | front.jpg | 07 (on model, front at the knee) |
| L2 back | back.jpg | 30 (product, back view) |
| L3 one leg | front_face.jpg | 06 (on model, one side up to the knee) |
| L4 shortest | front.jpg | 01 (on model, front up to the upper thigh) |
| L5 step | the L4 still (same look) | n/a: reuses the L4 still |

## 5. Order of work
Still storyboard first: base edit of front.jpg first (it feeds L1 and L4), then the riskiest still (L4 shortest, does try-on keep a pulled-up length over bare legs + boots?) as the ONE test still, then the other three, every still checked at 2x against the product truths, then the storyboard to Ralph. Clips: Flow first ($0): I send Ralph the kit per clip (approved still, ruching close-up, product sheet, boots close-up, the prompt) in the chat and on the review page; L1 first as the ONE test take, then the rest after his OK. Kie Omni ($0.315) only for a clip Flow can't make or that fails QC, asked first with the cost.
Free fixes planned: colour shift toward the real chocolate brown (round 26 read a little khaki); crop to the same framing on every look; AI finish last.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Step A base edit: Ralph's Gemini app (Ralph 2026-10-25 "Gemini") | 3 x $0 | 0 |
| Step B Kolors skirt try-on (fal) | 4 x $0.07 | 0.28 |
| Clips: Ralph's Flow app ($0 first); paid fallback Omni 4 s on Kie | 5 x $0.315 | 1.575 |
Expected spend if Flow works: **$0.28** (fal only). Ceiling if every clip falls back to Kie Omni: Kie $1.575 + fal $0.28.
Dropped from rev 2: the separate Kolors top pass (4 x $0.07): the base edit puts the top on in the same step.
Contingency redos (each asked separately with its cost): up to $0.50 (redo cap for this job); the likely one is a Kolors skirt redo on L4 ($0.07).
ElevenLabs: 0 chars (music-only). Month so far (`python3 grace/spend.py`): $162.79 (no cap in October; from November $100/month).

TOTAL: $1.86

**Approve?** (TOTAL is the ceiling with every paid fallback; nothing paid runs where the $0 route works.)

## 7. Questions (all of them, now)
Answered by Ralph 2026-10-25: (1) "Neck down"; (2) "No, wanted her legs to show with the boots" (bare legs + black knee-high boots, no tights). Both are in this book (step A + neck-down crop).

Answered by Ralph 2026-10-25: "Gemini, ok": (1) step A in his Gemini app; (2) short black fitted shorts under the skirt OK.

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| Step A base edits | Gemini app ($0) / Kie nano-banana-pro | prompts/v2_base_front.txt (front.jpg, front_face.jpg), prompts/v2_base_back.txt (back.jpg); image 1 = Grace photo, image 2 = top, image 3 = boots |
| L1-L4 stills | Kling Kolors try-on (fal) | no text prompt: human_image_url = step A result, garment_image_url = real listing photo (table above) |
| L1-L5 clips | Flow app ($0) / Omni on Kie (omni_clip.py) | prompts/v2_L1..L5.txt (rewritten with prompt-master 2026-10-25): image 1 = the approved still (first frame), image 2 = refs/closeup_ruching.png, image 3 = refs/product_sheet.png, image 4 = refs/boots_cut1.png; neck-down framing, bare legs + boots, drawstrings only at the front waistband, hands never below the hips, solid fabric, no music/voice + the move from section 4 |
