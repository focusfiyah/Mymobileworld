# Production Book: CeraVe Winter Skin Routine Bundle (Grace)

Sent to Ralph: https://claude.ai/artifact/MsGgDxqTuqxumSVXt4aH4m (v2, 2026-11-02)

## 1. Job
- Client / own content: Grace  Product: CeraVe Winter Skin Routine Bundle, TikTok Shop exclusive (Hydrating Facial Cleanser, AM Facial Moisturizing Lotion SPF 50, Intensive Moisturizing Cream tube, Healing Lip Balm)  Route: music-only product video, product lock (ugc-product-ad references/product-lock.md), Omni on Kie (Ralph 2026-11-02)
- Job folder: `ugc/cerave-winter-bundle/`  Target length: 10 s (Ralph)  Shots: 5 clips cut into 7 shots (2 hand-free)

## 2. Gate result (`python3 grace/gate.py ugc/cerave-winter-bundle`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (tag x5 + discover + video x6; shop search hit a captcha, listing data used) | proof/coach.md | OK |
| Daily viral board | research/coach/viral-2026-11-02.json (911 videos, 242 shop) | OK |
| Product facts (source) | proof/product_facts.md | OK |
| Hooks modeled on named winners | proof/hooks.md | OK (H005 picked) |
| Humanizer | proof/humanizer.md | OK |
| Readability (grade) | proof_readability.txt | 3.3 |
| Banned-phrase check | gate.py | OK |
| Audience research | research/audience.md + voc.md (25 real quotes) | OK |

## 3. Script (final, Humanized)
Video: no voiceover, music added later (Ralph). Spoken script for later (Grace or her clone), 35 words, about 12-14 s:
> One thing I cannot stand is my lips cracking every single winter. I already use the green one, and this set comes with all four. It's only on TikTok Shop. It's in the orange cart.
Source of each line: proof/line_sources.md (hook H005 + audience quotes / Grace owns the cleanser + 4 in the set / TikTok Shop exclusive badge / Grace close).

## 4. Shot list (green cleanser mostly; the group of four only where needed and at the end, Ralph 2026-11-02)
| # | Window (s) | VO words | On screen | Face? | VO or lip sync | Prompt notes |
|---|---|---|---|---|---|---|
| S1 | 0.0-2.0 | (music) | Hook: green cleanser pumped into her palm | No | none | HAND, green cleanser only, Omni 1.1 Flash on Kie, 4 s, 1080p |
| S2 | 2.0-3.5 | (music) | Hand-free push-in on the green cleanser | No | none | HAND-FREE, green cleanser only, Omni 1.1 Flash on Kie, 4 s, 1080p |
| S3 | 3.5-5.0 | (music) | Green cleanser lifted and held to camera | No | none | HAND, green cleanser only, Omni 1.1 Flash on Kie, 4 s, 1080p |
| S4 | 5.0-6.8 | (music) | Group: she sets the cleanser down beside the other three | No | none | HAND, all four, Omni 1.1 Flash on Kie, 4 s, 1080p |
| run | 6.8-8.0 | (music) | fast run, 0.6 s each from S1 and S3 spare windows ($0) | No | none | free re-use |
| S5 | 8.0-10.0 | (music) | End: slow arc on all four | No | none | HAND-FREE, all four, Omni 1.1 Flash on Kie, 4 s, 1080p |
Outfit: cream knit sweater cuff on her forearm (winter cue)  Setting: real Pexels bathroom, light oak vanity + sage-green tiles (rooms/SOURCES.md)  Nails / person details: Grace's hand sheet (medium-brown skin, short squared French tips, crown ring stack, gold heart ring, blue thumb band)  Real product confirmed: refs/product_sheet.png (cleanser green pump; AM lotion blue collar; cream TUBE navy text, blue flip cap; lip balm navy tube, silver cap)

## 5. Order of work
Still storyboard first (5 stills, QC at 2x: labels letter for letter, sizes, grip, hand edges) → S1 (two hands + pump, riskiest) as the ONE test clip → S2-S5 after S1 passes → cut 10 s silent (music later), AI finish, QC, review page.
Free fixes planned: trim to the clean window of each take; crop; no label paste-back.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills (nano-banana-pro) | 5 x 0.09 | 0.45 |
| Omni 1.1 Flash clips, 4 s 1080p | 5 x 0.315 | 1.58 |
| One likely redo (1 still + 1 clip) | 1 x 0.405 | 0.41 |
Total Kie: $2.43  ElevenLabs: 0 (no VO)  Contingency redos (each asked separately): beyond the one above
Month so far (`python3 grace/spend.py`): $1.32 of $100

TOTAL: $2.43

**Approve?**

## 7. Questions (answered by Ralph 2026-11-02)
1. Hand sheet: WITHOUT the bracelet.
2. "I already use the green one" is true.
3. On-screen text: none.
4. Change: "Not all the products on every shot. Use the green mostly however show the group shot when necessary and towards the end." Done: S1-S3 green cleanser only, S4-S5 the group of four.

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| S1 still | nano-banana-pro (Gemini 3 Pro Image) | shots.json `still` (refs: rooms/cand/px_6580366.jpg, refs/closeup_cleanser.png, ../../grace/ref/hand-sheets/without_bracelet.jpg) |
| S1 clip | Omni 1.1 Flash | prompts/S1_clip.txt (refs: stills/S1.png, refs/closeup_cleanser.png) |
| S2 still | nano-banana-pro (Gemini 3 Pro Image) | shots.json `still` (refs: rooms/cand/px_6580366.jpg, refs/closeup_cleanser.png) |
| S2 clip | Omni 1.1 Flash | prompts/S2_clip.txt (refs: stills/S2.png, refs/closeup_cleanser.png) |
| S3 still | nano-banana-pro (Gemini 3 Pro Image) | shots.json `still` (refs: rooms/cand/px_6580366.jpg, refs/closeup_cleanser.png, ../../grace/ref/hand-sheets/without_bracelet.jpg) |
| S3 clip | Omni 1.1 Flash | prompts/S3_clip.txt (refs: stills/S3.png, refs/closeup_cleanser.png) |
| S4 still | nano-banana-pro (Gemini 3 Pro Image) | shots.json `still` (refs: rooms/cand/px_6580366.jpg, refs/product_sheet.png, refs/closeup_cleanser.png, refs/closeup_am50.png, refs/closeup_cream_tube.png, refs/closeup_lipbalm.png, ../../grace/ref/hand-sheets/without_bracelet.jpg) |
| S4 clip | Omni 1.1 Flash | prompts/S4_clip.txt (refs: stills/S4.png, refs/closeup_cleanser.png, refs/closeup_am50.png, refs/closeup_cream_tube.png, refs/closeup_lipbalm.png, refs/product_sheet.png) |
| S5 still | nano-banana-pro (Gemini 3 Pro Image) | shots.json `still` (refs: rooms/cand/px_6580366.jpg, refs/product_sheet.png, refs/closeup_cleanser.png, refs/closeup_am50.png, refs/closeup_cream_tube.png, refs/closeup_lipbalm.png) |
| S5 clip | Omni 1.1 Flash | prompts/S5_clip.txt (refs: stills/S5.png, refs/closeup_cleanser.png, refs/closeup_am50.png, refs/closeup_cream_tube.png, refs/closeup_lipbalm.png, refs/product_sheet.png) |
