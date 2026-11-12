# Production Book: Vans Plaid Old Skool, 2 shot-for-shot recreations (Grace), 2026-11-12

Sent to Ralph: https://claude.ai/artifact/HA6jd224NhhkLGc4FtZb6o (2026-11-12)

## 1. Job
- Client: Grace  Product: Vans Unisex Old Skool Low Top, Tartan Oil Green (TikTok Shop 1732738096900837416)  Route: ugc-product-ad hands + feet, product lock: stills on Kie (nano-banana-pro) from the real product sheet + logo close-ups, clips Wan 3.0 720P + free upscale (Ralph tapped "Wan 3.0 on Kie" 2026-11-12), `.claude/skills/ugc-product-ad/references/product-lock.md`
- Job folder: `ugc/vans-plaid-recreate/`  Target length: V1 7.4 s (one take), V2 8.0 s (4 shots)  Shots: 5
- Ask (Ralph 2026-11-12): "recreating these videos shot for shot, and the only thing we're replacing is Grace's complexion" ("We are just using grace for these"). Refs: https://www.tiktok.com/t/ZPLWoWj2h/ (@girlypopshopfinds 7695839213635259678) and https://www.tiktok.com/t/ZPLWopx22/ (@herstyledcloset 7696342911218142494). His taps: Wan 3.0 on Kie, no text, keep settings exactly, free track Grace swaps.

## 2. Gate result (`python3 grace/gate.py ugc/vans-plaid-recreate`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (video on both refs; tag/discover/viral returned 0 = captcha, tested 3x) | proof/coach_research.md | OK |
| Daily viral board | research/coach/viral-2026-11-12.json | ran, 0 videos (captcha) |
| Product facts (source) | research/product_facts.md, product_truth.json (listing photos) | OK |
| Hooks modeled on named winners | research/hooks.md (Grace library H130, H055) | OK |
| Humanizer | proof/humanizer.md | no tells |
| Readability (grade) | proof/readability.txt | 2.8 / 2.8 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized)
Music only, no voice, no on-screen text. The words are the TikTok post captions (scripts.md):
- V1: This is going to matter once the holiday parties start. Dark green plaid with the white Vans stripe goes with every red I own. It's in the orange cart.
- V2: I already know exactly who would love this. The friend who puts her tree up in November and wants her shoes to match it. It's in the orange cart.
Source of each line: research/line_sources.md. Music: a free licensed track per video (free-assets), Grace can swap in a trending sound in TikTok.

## 4. Shot list
| # | Window (s) | VO words | On screen | Face? | VO or lip sync | Prompt notes |
|---|---|---|---|---|---|---|
| V1S1 | 0.00-7.42 | none (music) | overhead POV on asphalt; left hand holds the right shoe top-down (insole up, toe pointing up), turns it to a side view, back to top-down and pushes it toward the lens (HAND) | no face | music only | refs: refs/inspo/A_layout.png, refs/product_sheet.png, refs/insole_closeup.png, refs/side_closeup.png, refs/grace_hand.png, refs/grace_feet.png; clip 8 s Wan 720P |
| V2S1 | 0.00-2.10 | none (music) | hand holds one shoe in 3/4 side view in front of a lit Christmas tree, small turn toward the front (HAND) | no face | music only | refs: refs/inspo/B1_layout.png, refs/product_sheet.png, refs/side_closeup.png, refs/grace_hand.png; clip 3 s Wan 720P |
| V2S2 | 2.10-3.47 | none (music) | POV seated, legs crossed in light jeans, both shoes on, on a cream and red striped rug; her hand rests on her knee and slides a little (HAND) | no face | music only | refs: refs/inspo/B2_layout.png, refs/product_sheet.png, refs/side_closeup.png, refs/grace_hand.png, refs/grace_feet.png; clip 2 s Wan 720P |
| V2S3 | 3.47-5.57 | none (music) | low view from behind of both heels on a cream carpet, frayed jeans hems; the left heel is lifted showing the gum sole, it lowers and the right heel lifts (HAND-FREE) | no face | music only | refs: refs/inspo/B3_layout.png, refs/product_sheet.png, refs/heel_closeup.png, refs/grace_feet.png; clip 3 s Wan 720P |
| V2S4 | 5.57-7.97 | none (music) | hand holds one shoe front-on (laces to camera, toe down) in front of the tree, then turns it to a 3/4 side view (HAND) | no face | music only | refs: refs/inspo/B4_layout.png, refs/product_sheet.png, refs/side_closeup.png, refs/grace_hand.png; clip 3 s Wan 720P |
Outfit: as the originals (V1 red knit sweater with rhinestone brooch sleeve patches, black leggings, silver bow ring, nude almond nails, white pedicure, silver anklet; V2 cream cable-knit sleeve, diamond rings, nude almond nails, light frayed jeans)  Setting: as the originals (V1 asphalt + burgundy studded mini bag; V2 lit Christmas tree, cream/red striped rug on wood, cream carpet)  Person: Grace's real warm medium-deep brown skin on every hand and foot (refs/grace_hand.png, refs/grace_feet.png from her own post) = the only change  Real product confirmed: listing photos refs/real/listing_2-5.png, sheet refs/product_sheet.png, close-ups insole / heel / side

## 5. Order of work
5 stills = the storyboard (Ralph reviews, $0.45) → V1S1 clip first (riskiest: the big held-shoe turn) → the 4 V2 clips after his OK → cut on the original cut times, free music, AI finish, QC (2x edges, drift, REMOVED.md) → review page → Drive after his OK.
Free fixes planned: trim each clip to its window, crop, retime within 1.0x+, cut before any flip.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, nano-banana-pro 1K | 5 x $0.09 | $0.45 |
| V1S1 clip, Wan 720P | 8 s x $0.08 | $0.64 |
| V2 clips, Wan 720P | (3+2+3+3) s x $0.08 | $0.88 |
| Likely redo (one still + the V1 clip) | $0.09 + $0.64 | $0.73 |
Total Kie: $2.70  ElevenLabs: 0 chars  Contingency: inside TOTAL (each redo still asked)
Month so far (`python3 grace/spend.py`): $73.30 of $100 (left $26.70)

TOTAL: $2.70

**Approve?**

## 7. Questions (all of them, now)
1. The originals turn the held shoe (V1: top-down to side and back; V2: small turns). REMOVED.md has "any rotation of a held shoe" (Ralph 2026-10-21) because the models flipped it. Allow the turn for these shot-for-shot videos, with frame-by-frame checks and cuts before any flip? (asked after Ralph reads the page)

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| V1S1 still | nano-banana-pro (Gemini 3 Pro Image), Kie, 1K 9:16 | shots.json `V1S1.still` |
| V1S1 clip | Wan 3.0 720P + free upscale, Kie, 8 s | shots.json `V1S1.clip` (refs: stills/V1S1.png, refs/insole_closeup.png, refs/side_closeup.png, refs/product_sheet.png) |
| V2S1 still | nano-banana-pro (Gemini 3 Pro Image), Kie, 1K 9:16 | shots.json `V2S1.still` |
| V2S1 clip | Wan 3.0 720P + free upscale, Kie, 3 s | shots.json `V2S1.clip` (refs: stills/V2S1.png, refs/side_closeup.png, refs/product_sheet.png) |
| V2S2 still | nano-banana-pro (Gemini 3 Pro Image), Kie, 1K 9:16 | shots.json `V2S2.still` |
| V2S2 clip | Wan 3.0 720P + free upscale, Kie, 2 s | shots.json `V2S2.clip` (refs: stills/V2S2.png, refs/side_closeup.png, refs/product_sheet.png) |
| V2S3 still | nano-banana-pro (Gemini 3 Pro Image), Kie, 1K 9:16 | shots.json `V2S3.still` |
| V2S3 clip | Wan 3.0 720P + free upscale, Kie, 3 s | shots.json `V2S3.clip` (refs: stills/V2S3.png, refs/heel_closeup.png, refs/product_sheet.png) |
| V2S4 still | nano-banana-pro (Gemini 3 Pro Image), Kie, 1K 9:16 | shots.json `V2S4.still` |
| V2S4 clip | Wan 3.0 720P + free upscale, Kie, 3 s | shots.json `V2S4.clip` (refs: stills/V2S4.png, refs/side_closeup.png, refs/product_sheet.png) |
