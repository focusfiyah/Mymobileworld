# Production Book: ZYTRELL Acne Cream (Grace), 2026-11-02

Sent to Ralph: https://claude.ai/artifact/FcqgjVn31wJ9zR8YMzh6uJ, 2026-11-02

## 1. Job
- Client: Grace  Product: ZYTRELL Acne Treatment Cream, 2% salicylic acid, 0.35 oz / 10 g tube  Route: ugc-product-ad hands route + product lock (`references/product-lock.md`): product clips are Omni 1.1 Flash on Kie (Ralph 2026-11-02: "everything on Kie"), clips without the product are Seedance 2.0 Mini on Kie
- Job folder: `ugc/zytrell-acne-cream/`  Target length: 10-12 s (Ralph: "10-12s")  Shots: 5
- Sound: NO voiceover, no lip sync, no on-screen text; music is added later (Ralph). Spoken script kept for a VO Grace can record later.

## 2. Gate result (`python3 grace/gate.py ugc/zytrell-acne-cream`: GATE OK)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | grace/PLAYBOOK.md | OK |
| Coach research (shop + video x4) | research/coach_research.md | OK. TikTok tag/discover pages blocked from this container (tested); shop + video worked |
| Daily viral board | research/viral-2026-11-02.json | ran, 0 videos (same block); acne winners taken from saved Sept-Oct boards |
| Product facts (source) | research/product_facts.md | OK, FDA label + your listing photo |
| Hooks modeled on named winners | research/hooks.md | OK, H062 / H112 / H047 |
| Humanizer | research/humanizer_report.md | OK |
| Readability (grade) | research/readability.txt | A 3.7, caption 1.6 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized; for a later VO, 34 words = ~10-11 s)
Script A is final (Ralph 2026-11-02: Script B's "Most pimple creams burn mine" is not true for Grace, so B is dropped).
A (H062): You know that moment when a pimple shows up before plans? Concealer won't hide it, so I dab this on. Two percent salicylic acid. Grab two before holiday pics. It's in the orange cart.
Source of each line: research/line_sources.md (hooks word for word from HOOKS.md; 2% salicylic acid from the FDA label; "grab two before holiday pics" = CTA sells more units + real season).

## 4. Shot list (beat every ~2-2.5 s, modeled on the 9-13 s music-only winners)
| # | Window (s) | Script beat | On screen | HAND / HAND-FREE | Face? | Model |
|---|---|---|---|---|---|---|
| S1 | 0-2.2 | hook | Slow push-in on Grace's lower face (nose tip to collarbone) in the bathroom: one small raised pimple on the chin. No hand, no product | HAND-FREE | lower face only (no eyes) | Seedance 2.0 Mini 4 s |
| S2 | 2.2-4.2 | pain | Fingertip dabs concealer on the spot; the bump still shows | HAND | lower face | Seedance 2.0 Mini 4 s |
| S3 | 4.2-6.8 | solution | Grace's left hand holds the closed tube by its edges on the counter and lifts it toward the lens, print facing the camera (RISKIEST, test clip). No squeeze: the nozzle under the cap is in no photo, so it would be invented | HAND | no | Omni 1.1 Flash on Kie 4 s |
| S4 | 6.8-8.8 | "dab this on" | Her fingertip with a dot of white cream pats a thin layer over the spot. No tube in frame | HAND | lower face | Seedance 2.0 Mini 4 s |
| S5 | 8.8-11.2 | "grab two" + close | Tube standing on the counter beside an open plain blush-pink makeup bag, slow dolly-in, no hand | HAND-FREE | no | Omni 1.1 Flash on Kie 4 s |
Person: Grace's likeness (Ralph 2026-11-02): her face from grace/ref/body/front_face.jpg (refs/grace_face.jpg), medium-deep brown skin, lower face only. Outfit: soft pink ribbed tank (her own top in the reference). Hands: grace/ref/hand-sheets/without_bracelet.jpg (left hand: silver crown stack on the ring finger, gold heart ring on the index, blue thumb band, square pink French-tip nails); bracelet sheet only if you say so (Q1). Setting: real Pexels bathroom refs/room.jpg (px_29589451: white stone counter, light wood drawers, oval gold mirror; rooms/SOURCES.md). Real product (Ralph 2026-11-02: no real photos, use the listing): refs/product_sheet.png + refs/logo_closeup.png cut from listing image 1/7, props whited out; deep-green tube, green screw cap at the bottom, crimped top, white vertical "zytrell" logo. No box, no fruit (listing props).
Every clip moves (push-in or a hand doing something); no photos, no freezes, no text, bright neutral grade, AI finish last.

## 5. Order of work
Product reference sheet (free, done) → 5 still storyboard on the review page (your OK, still free to change) → S3 test clip first (riskiest) → the other 4 → cut → QC (2x edges, drift strip on product shots, REMOVED.md) → AI finish → Drive.
Free fixes planned: crop/retime/blur in ffmpeg before any reroll; a drifted Omni take gets one edit turn (asked) before a new take.
Time: ~35-40 min machine time after your OK, plus your review stops (stills, then the S3 test clip).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 5 x $0.09 | 0.45 |
| Clips without the product, Seedance 2.0 Mini 4 s ($0.041/s) | 3 x $0.164 | 0.492 |
| Product clips S3, S5, Omni 1.1 Flash on Kie 4 s | 2 x $0.315 | 0.63 |
| One likely redo (S3 hand + tube on Kie Omni, asked first) | 1 x $0.315 | 0.315 |
Total Kie: up to $1.887  ElevenLabs: 0 chars (no VO)  Contingency redos: included above, each asked separately
Expected spend without a redo: $1.572.
Month so far (`python3 grace/spend.py`): $1.32 of the $100 November cap.

TOTAL: $1.887

**Approve?**

## 7. Questions (all of them, now)
Answered 2026-11-02 (Ralph): no real tube photos, use the listing; Grace's likeness; Script B line not true (A is final); stills and everything on Kie.
1. Hands: Grace's hand sheet WITHOUT the bracelet (planned, cleaner for skincare) or WITH it (gold link bracelet + pearl chain)?

## 8. Prompts (final, written with prompt-master; every reference named)
All 10 prompts in `shots.json` (built by `tools_make_shots.py`), copies in `prompts/still_S*.txt` and `prompts/S*.txt`. `grace/prompt_check.py`: PROMPT_LINT_OK and MARKED_OK (2026-11-02).
| Item | Model | References (in order) |
|---|---|---|
| Stills S1 | nano-banana-pro 9:16 1K | grace_face, room |
| Stills S2, S4 | nano-banana-pro 9:16 1K | grace_face, grace_hands, room |
| Still S3 | nano-banana-pro 9:16 1K | product_sheet, logo_closeup, grace_hands, room |
| Still S5 | nano-banana-pro 9:16 1K | product_sheet, logo_closeup, room |
| Clips S1, S2, S4 | bytedance/seedance-2-mini 4 s 720p, reference mode, audio off (`run.py seedance`) | the approved still |
| Clips S3, S5 | google/gemini-omni-flash-1-1 4 s (`omni_clip.py`) | the approved still, logo_closeup, product_sheet |
