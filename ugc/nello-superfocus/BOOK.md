# Production Book: Nello Superfocus tub (Grace), 2026-11-03

Sent to Ralph: https://claude.ai/code/artifact/ba19b895-a976-46e2-8404-413ec9044288, 2026-11-03

## 1. Job
- Client: Grace  Product: Nello Superfocus Nootropic Drink Mix, 30 Serving Tub, Fruit Punch (TikTok Shop listing 1732403145881784760, 7.2K sold, 4.5 stars)  Route: ugc-product-ad hands route + product lock (`references/product-lock.md`): product clips are a $0 Flow take first, else Wan 3.0 720P on Kie + our free upscale; clips without the product are Seedance 2.0 Mini on Kie
- Job folder: `ugc/nello-superfocus/`  Target length: 10-12 s (Ralph: "10-12s timeframe for current video")  Shots: 6
- Sound: NO voiceover, no lip sync, no on-screen text; Grace adds music (Ralph: "No VO needed, she will add music for it"). The ~30 s scripts below are for a VO Grace records later (Ralph: "Make the script the standard timeframe").

## 2. Gate result (`python3 grace/gate.py ugc/nello-superfocus`: GATE OK)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | grace/PLAYBOOK.md | OK |
| Audience research | research/audience.md (+ 3,005 search phrases, 309 TikTok comments, VOC) | OK |
| Grace research workflow | research/RESEARCH.md (7 sections, verdict, 4 roles) | OK |
| Coach research (shop + discover + video x5) | research/coach_research.md | OK. viral/tag pages return 0 videos to this container (tested); shop, discover on real Nello pages and video worked |
| Daily viral board | research/viral-2026-11-03.json | ran, 0 videos (same block) |
| Product facts (source) | research/product_facts.md | OK: listing, Supplement Facts image, brand site |
| Hooks modeled on named winners | research/hooks.md | OK, H062 / H019 / H075 |
| Humanizer | research/humanizer_report.md | OK |
| Readability (grade) | research/readability.txt | A 4.4, B 3.9, caption 3.3 |
| Banned-phrase check | gate.py | OK |

## 3. Scripts (final, Humanized; ~30 s each for a later VO, ~95 words at Grace's ~3.2 words/s)
A (H062, leads with the HOOK role, recommended): You know that moment when it's three o'clock and you've read the same email four times? Forty tabs open and nothing done. Another coffee just makes you jittery. So this is what people are grabbing instead. Nello Superfocus. One scoop in cold water and it tastes like fruit punch. It has lion's mane, rhodiola and alpha GPC, and zero sugar. Honestly, now I have no excuse to push my to-do list to tomorrow. The tub has thirty servings, so grab two and keep one at your desk before the holidays get busy. It's in the orange cart.
B (H019, leads with the DESIRE role): I would rather drink this than spend another day rereading the same email. Three o'clock hits and the brain just stops. This is Nello Superfocus. One scoop, cold water, and it turns into fruit punch. People say it's the only thing that gets them through their list, and it has zero sugar. Inside there's lion's mane, rhodiola and alpha GPC. I hate how easy this is, now there's no excuse left. The tub has thirty servings, so grab one for home and one for work before the holidays. It's in the orange cart.
Caption: 3pm brain, meet fruit punch 🍒 One scoop. Zero sugar. #nello #focus #tiktokshop #ad
On-screen text options (yes/no only, default NO; HofR version keeps text): "3pm brain has entered the chat" / "my 3pm coffee got replaced" / "the tub nobody told you about".
Source of each line: research/line_sources.md (hooks word for word from HOOKS.md; facts from the Supplement Facts image: 1 scoop, 30 servings, 0 g sugar, lion's mane, rhodiola, alpha GPC). Not said: ADHD, Adderall, "no jitters" promises, caffeine amounts, prices, deals.

## 4. Shot list (10-12 s music video, a beat every ~2 s, modeled on the 12-16 s product-in-hand winners)
| # | Window (s) | Script A beat | On screen | HAND / HAND-FREE | Model |
|---|---|---|---|---|---|
| S1 | 0-2.0 | hook + pain | Desk at 3 pm: laptop with many tabs (nothing readable), half-full cold coffee mug, slow push-in. No product | HAND-FREE | Seedance 2.0 Mini 4 s |
| S2 | 2.0-4.0 | one scoop in cold water | Her hand tips the clear long-handled scoop: pale-pink powder pours into a glass of ice water. Tub not in frame | HAND | Seedance 2.0 Mini 4 s |
| S3 | 4.0-5.8 | tastes like fruit punch | Macro: the pink swirls dissolve into clear bright red with ice, slow push-in | HAND-FREE | Seedance 2.0 Mini 4 s |
| S4 | 5.8-8.0 | Nello Superfocus (RISKIEST, test clip first) | Her left hand closes around the tub on the desk and lifts it a hand's width toward the lens, label to camera, one grip | HAND | Flow take ($0) first, else Wan 3.0 720P 5 s |
| S5 | 8.0-10.0 | no excuse / to-do list | Her hand lifts the red drink up out of frame past a notebook list (unreadable). No face | HAND | Seedance 2.0 Mini 4 s |
| S6 | 10.0-12.0 | thirty servings + close | Tub alone standing on the desk beside the red drink, slow dolly-in (end shot shows ONE product) | HAND-FREE | Flow take ($0) first, else Wan 3.0 720P 5 s |
Hand-free: 3 of 6 (half). Person: Grace's hands only, no face. Hands: grace/ref/hand-sheets/no_jewelry.jpg (Q3). Setting: real Pixabay home office refs/room.jpg (pb_791184: warm wood desk, white shelves with teal books, window light; rooms/SOURCES.md).
Real product (from Ralph's photo = listing image 1; product_truth.json): squat round tub, about palm size (~10 cm across x ~8 cm tall, estimated from real tubs in a creator's hand; no maker dimensions published), white ribbed screw lid, coral-red wave label, white print "nello® Focus Drink Mix†" / "SUPER FOCUS™", pale-pink "FRUIT PUNCH FLAVORED" badge lower left, "30 Servings / Dietary Supplement / Net Wt. 155.4g (5.48oz)" lower right; clear long-handled scoop; pale-pink powder; clear red drink. NOT shown: the blue "30 Servings" badge, fruit and background from the listing photo (props), pouches/packets, the back of the tub (no photo of it).
Every clip moves (push-in, dolly or a hand doing something); no photos, no freezes, no text, bright neutral grade, AI finish last.

## 5. Order of work
Product sheet + room (free, done) -> 6 stills on the review page (your OK, still cheap to change) -> S4 test clip first (Flow kit to you, or Wan) -> the other 5 clips at once -> cut -> QC (2x edges, label check on every product frame, REMOVED.md) -> AI finish -> Drive "Grace Tiktok assets" / Nello Superfocus.
Free fixes first (crop, retime, blur) before any reroll.
Time: ~35-40 min machine time after your OK, plus your review stops (stills, then the S4 test clip). Flow takes add your phone time.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) ($0 if you make them in your Gemini app, Q2) | 6 x $0.09 | 0.54 |
| Clips without the product, Seedance 2.0 Mini 4 s ($0.041/s) | 4 x $0.164 | 0.656 |
| Product clips S4, S6: Flow first ($0); Wan 3.0 720P 5 s only if Flow fails or credits run out | 2 x $0.40 | 0.80 |
| One likely redo (S4 hand + tub on Wan, asked first) | 1 x $0.40 | 0.40 |
Total Kie: up to $2.396  ElevenLabs: 0 chars (no VO)
Expected: $1.196 if both Flow takes pass and no redo; $0.656 if you also make the stills in Gemini.
Month so far (`python3 grace/spend.py`): $16.12 of the $100 November cap ($83.88 left).

TOTAL: $2.396

**Approve?**

## 7. Questions (all of them, now)
Answered 2026-11-03 (Ralph, tapped): Tub, no caffeine; stills on Kie; no-jewellery hands; Script A.
1. Which product does Grace have: the tub, no caffeine (your photo), the tub + caffeine (adds a blue "+ CAFFEINE" pill and a "75mg caffeine" badge on the label), or the travel packets?
2. Stills: Kie ($0.54) or your Gemini app ($0, I send the kit)?
3. Hands: no jewellery (recommended, cleanest), without bracelet (rings), or with bracelet?
4. Script: A (3 o'clock hook) or B ("I would rather drink this")?

## 8. Prompts (final, written with prompt-master; every reference named)
All 12 prompts in `shots.json` (built by `tools_make_shots.py`), copies in `prompts/still_S*.txt` and `prompts/S*.txt`. `grace/prompt_check.py`: PROMPT_LINT_OK and MARKED_OK (2026-11-03).
| Item | Model | References (in order) |
|---|---|---|
| Stills S1 | nano-banana-pro 9:16 1K | room |
| Stills S2 | nano-banana-pro 9:16 1K | grace_hands, room |
| Still S3 | nano-banana-pro 9:16 1K | drink_glass, room |
| Still S4 | nano-banana-pro 9:16 1K | product_sheet, logo_closeup, grace_hands, room |
| Still S5 | nano-banana-pro 9:16 1K | drink_glass, grace_hands, room |
| Still S6 | nano-banana-pro 9:16 1K | product_sheet, logo_closeup, room |
| Clips S1, S2, S3, S5 | bytedance/seedance-2-mini 4 s 720p, reference mode, audio off | the approved still |
| Clips S4, S6 | Flow (Omni 1.1 Flash) kit, else wan/3-0-video 720P 5 s (`wan_clip.py`) | the approved still, logo_closeup, product_sheet |
