# Production Book: ZYTRELL Acne Cream (Grace), 2026-11-02

Sent to Ralph: https://claude.ai/artifact/FcqgjVn31wJ9zR8YMzh6uJ, 2026-11-02

## 1. Job
- Client: Grace  Product: ZYTRELL Acne Treatment Cream, 2% salicylic acid, 0.35 oz / 10 g tube  Route: ugc-product-ad hands route + product lock (`references/product-lock.md`): product clips are Omni (your Flow app first), clips without the product are Seedance 2.0 Mini
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
| Readability (grade) | research/readability.txt | A 2.6, B 2.4, caption 1.6 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized; for a later VO, ~31-34 words = ~10-11 s)
A (H062): You know that moment when a pimple shows up before plans? Concealer won't hide it, so I dab this on. Two percent salicylic acid. Grab two before holiday pics. It's in the orange cart.
B (H112): I was worried this would dry out my skin. Most pimple creams burn mine. This one's two percent salicylic acid, plus aloe. Grab two before holiday pics. It's in the orange cart.
Source of each line: research/line_sources.md (hooks word for word from HOOKS.md; 2% salicylic acid + aloe from the FDA label; "grab two before holiday pics" = CTA sells more units + real season).

## 4. Shot list (beat every ~2-2.5 s, modeled on the 9-13 s music-only winners)
| # | Window (s) | Script beat | On screen | HAND / HAND-FREE | Face? | Model |
|---|---|---|---|---|---|---|
| S1 | 0-2.2 | hook | Slow push-in on her lower face in a bright bathroom mirror: one small red pimple on the chin. No product | HAND-FREE | lower face only (no eyes) | Seedance 2.0 Mini 4 s |
| S2 | 2.2-4.2 | pain | Fingertip dabs concealer on the spot; the bump still shows | HAND | lower face | Seedance 2.0 Mini 4 s |
| S3 | 4.2-6.8 | solution | Hand picks the green ZYTRELL tube off the counter and squeezes a small dot of white cream onto the index fingertip (RISKIEST, test clip) | HAND | no | Omni: Flow first |
| S4 | 6.8-8.8 | "dab this on" | Fingertip pats a thin layer over the spot. No tube in frame | HAND | lower face | Seedance 2.0 Mini 4 s |
| S5 | 8.8-11.2 | "grab two" + close | Tube standing on the vanity beside an open makeup bag, slow dolly-in, no hand | HAND-FREE | no | Omni: Flow first |
Outfit: plain soft top, neckline only (asked, Q2). Setting: one real bright, neutral bathroom from Pexels/Pixabay (rooms.py), not white-on-white, not dark. Nails / person details: asked (Q2). Real product confirmed (top, cap, label): deep-green tube, green screw cap at the bottom, crimped top, white vertical "zytrell" logo; real photos asked (Q1). No box, no orange slices (listing props).
Every clip moves (push-in or a hand doing something); no photos, no freezes, no text, bright neutral grade, AI finish last.

## 5. Order of work
Product reference sheet (free) → 5 still storyboard on the review page (your OK, still free to change) → S3 test clip first (riskiest) → the other 4 → cut → QC (2x edges, drift strip on product shots, REMOVED.md) → AI finish → Drive.
Free fixes planned: crop/retime/blur in ffmpeg before any reroll; a drifted Omni take gets one edit turn (asked) before a new take.
Time: ~35-40 min machine time after your OK, plus your Flow takes (2 clips) and review stops.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie ($0 if you make them in your Gemini app) | 5 x $0.09 | 0.45 |
| Clips without the product, Seedance 2.0 Mini 4 s ($0.041/s) | 3 x $0.164 | 0.492 |
| Product clips S3, S5: Flow on your phone first (12 credits each) | 2 x $0 | 0.00 |
| ...same 2 on Kie Omni only if Flow fails or you can't (asked first) | 2 x $0.315 | 0.63 |
| One likely redo (S3 squeeze on Kie Omni, asked first) | 1 x $0.315 | 0.315 |
Total Kie: up to $1.887  ElevenLabs: 0 chars (no VO)  Contingency redos: included above, each asked separately
Expected spend with Flow: $0.94 ($0.49 if you also make the stills in Gemini).
Month so far (`python3 grace/spend.py`): $1.32 of the $100 November cap.

TOTAL: $1.887

**Approve?**

## 7. Questions (all of them, now)
1. Real product photos: can Grace send 2-3 photos of the tube itself (front, back, cap)? I only have listing image 1/7, a brand render. Photos win over the render (2026-10-26 rule).
2. Her skin: which skin tone, age range and nails (length, colour) for the hands and lower face? Or should it read as Grace?
3. Script B says "Most pimple creams burn mine." Is that true for Grace? If not, I use Script A.
4. Stills: Kie ($0.45) or your Gemini app ($0)?

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| S1-S5 stills, S1/S2/S4 Seedance, S3/S5 Omni | see §4 | written after your answers to §7 (skin, nails, real photos change every prompt), with prompt-master loaded, checked by grace/prompt_check.py, and this book re-sent for your OK before any spend |
