# Production Book: Dr. Nice's Kids' Boo-Boo Gel (1 fl oz) for Grace, V1 music-only + V2 script

Sent to Ralph: https://claude.ai/code/artifact/9873bd52-a6f3-40b1-af7b-ac7a2c567791 (2026-11-03)

## 1. Job
- Client: Grace. Product: Dr. Nice's Boo-Boo Gel for Kids, 1 fl oz (30 ml) silver airless pump. Route: product lock, `ugc-product-ad` references/product-lock.md: product clips = Flow takes in your app first ($0), Wan 3.0 720P on Kie + our free upscale only if a Flow take fails or you can't make it; Seedance 2.0 Mini for the 2 clips without the product.
- Job folder: `ugc/dr-nice-boo-boo-gel/`  Target length: 12 s (Ralph 2026-11-03: "10-12s timeframe for current video")  Shots: 6 (3 HAND, 3 HAND-FREE). Music only, no VO; Grace adds music. Script V1 sits on the shots (she can caption or voice it); script V2 is the standard ~30 s for her own VO later.

## 2. Gate result (`python3 grace/gate.py ugc/dr-nice-boo-boo-gel`): GATE OK (2026-11-03)
| Proof | File | Result |
|---|---|---|
| Playbook rules read | research/playbook.md | done |
| Coach research (tag/shop/discover + video x3) | research/coach.md, shop/, discover/ (48 videos), videos/ x4 | done; 4 of 5 shop searches and all 5 hashtags returned 0 (tried, logged); "bug bite relief" gave 15 listings |
| Daily viral board | research/viral/viral-2026-11-03.json | 61 videos, 1 new shop video (bite relief is a summer niche) |
| Product facts (source) | research/product_facts.md, product_listing.md (brand site + Amazon) | done |
| Audience + Grace research workflow | research/audience.md, RESEARCH.md (7 sections, 4 roles) | done |
| Hooks modeled on named winners | research/hooks.md (H122, H040, H006, H041) | done |
| Humanizer | research/humanizer.md, captions.md | done |
| Readability (grade) | research/readability_v1.txt | V1 1.6, V2 2.0 |
| Banned-phrase check | gate.py | GATE OK |

## 3. Script (final, Humanized)
V1, the 12 s music cut (46 words, about 12-13 s at Grace's pace, grade 1.6):
1. Hook (H122): I didn't think much of this until a scraped knee.
2. Pain: Usually it's tears and a bandaid fight.
3. Solution: No sting, so they dab it on themselves.
4. Sell-side confession: Only problem? They want it on every bump.
5. Real urgency + more units: Grab one per bag before the next scrape.
6. Close: It's in the orange cart.

V2, standard length for Grace's VO (107 words, about 30-35 s, grade 2.0):
1. Hook (H040): This was supposed to be for the first aid kit. Then the kids found it.
2. Pain: One little scrape and it's tears, a bandaid fight, and a bandaid that peels off five minutes later.
3. Solution: This is Boo-Boo Gel. One pump is a pearl-size dot, and they dab it on themselves. No sting.
4. Selling points: It feels cool, dries clear and isn't greasy. Four ingredients, vegan, made in the USA.
5. Confession: Only downside? Now they want it on every tiny bump, even the ones I can't see.
6. Urgency + close: It's small enough for a backpack, so grab one for school and one for the car before the next scrape. It's in the orange cart.
No price, no "order it now", only our product, no medical words (no heals, antibacterial, infection, scars). On-screen text: none (options in research/hooks.md, only on your yes). Insect bites: only the TikTok Shop title says it; the brand site and Amazon say scrapes, minor cuts, burns, blisters, chafing, so the scripts leave bites out unless you say so.
Source of each line: research/line_sources.md (H122/H040; @laniedoesdeals 10.8M "melts down every time you clean a scrape"; parents' own words; listing "No sting, so kids can do it themselves", "One pearl-sized dot", "Sized for backpacks, diaper bags, and travel pouches"; PLAYBOOK confession pattern).

## 4. Shot list
| # | Window (s) | Words | Shot | HAND? | Model | Setting (real photo) |
|---|---|---|---|---|---|---|
| S1 | 0.0-2.4 | hook | Child's left hand holds the open bottle (silver pump), right fingertip with one clear gel dot pulls back from the nozzle | HAND (child) | Flow, else Wan 5 s | backyard lawn |
| S2 | 2.4-4.2 | tears + bandaid fight | Blue kick scooter tipped over on the lawn, wheel spinning down, dolly in | HAND-FREE | Seedance Mini 4 s | backyard lawn |
| S3 | 4.2-6.3 | no sting, dab | Child's fingertip dabs the clear gel on a small pink knee scrape, a clear film stays | HAND (child) | Seedance Mini 4 s (no bottle in frame) | backyard lawn |
| S4 | 6.3-8.4 | every bump | Bottle standing on the kitchen counter by a bowl of oranges, push-in | HAND-FREE | Flow, else Wan 5 s | white counter |
| S5 | 8.4-10.6 | one per bag | Grace's hand slides the bottle into the mesh side pocket of a plain navy kid's backpack | HAND (Grace) | Flow, else Wan 5 s | bright kitchen |
| S6 | 10.6-12.0 | orange cart | ONE bottle standing on a flat stone by the garden path, dolly in | HAND-FREE | Flow, else Wan 5 s | sunny garden |
No faces in any shot (no lip sync). Child: about six, small hands, short natural nails, light-medium skin, denim shorts (S3). Grace's hand: her no-jewellery hand sheet (grace/ref/hand-sheets/no_jewelry.jpg), mauve-pink French tips, no rings, bracelet or watch.
Real product (product_truth.json, refs/product_sheet.png, from the brand's photos = the ones you sent): slim silver cylinder about 11 cm tall and 3 cm across (box 1.37 x 1.37 x 4.75 in); brushed silver cap over the top third; thin chrome ring; sky-blue label: "DR. NICE'S" white with a tiny green leaf, "NATURAL PRODUCTS", "BOO-BOO GEL", smiling blue furry monster with golden horns and an orange bandage, "1 fl oz (30ml)"; silver base. Cap off: silver pump head (the brand's HOW TO USE photo; an older listing photo shows a white pump, not used). Clear gel, one pearl-size dot. Box: never shown.

## 5. Order of work
All 6 stills at once on Kie ($0.54), storyboard on the review page for your look (QC at 2x: every letter of the label, the monster, size vs the hand, grip, silver pump, whole wrists). Then the Flow kits for S1, S4, S5, S6 on the review page (one card each: still + label close-up + logo close-up + sheet + prompt); you make S1 first (riskiest: open pump, two child hands, the gel dot), I QC it, then the other 3. S2 and S3 run on Seedance at the same time. Cut to the line windows, QC (flash, levels, every frame of the label), AI finish last, silent master for the music.
Free fixes planned: crop, retime, colour match; trim to the clean window before any redo.
Time: about 35-40 min of machine time after your OK, plus your stops (storyboard, Flow takes, cut).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills (Gemini 3 Pro Image = nano-banana-pro on Kie) | 6 x 0.09 | 0.54 |
| Seedance 2.0 Mini 4 s (S2, S3: no product) | 2 x 0.164 | 0.33 |
| Product clips S1, S4, S5, S6: Flow takes in your app | 4 x 12 credits | 0.00 |
| Fallback: Wan 3.0 720P 5 s on Kie, only if a Flow take fails QC or you can't make it (each asked first) | up to 4 x 0.40 | 1.60 |
| One likely redo (1 still + 1 Wan clip), asked before it runs | 1 | 0.49 |
Expected with Flow: $0.96 Kie (stills, 2 Seedance, 1 still redo) + 48 Flow credits. Ceiling if every product clip falls back to Wan: $2.96. ElevenLabs: 0 chars (no VO).
Month so far (`python3 grace/spend.py`): $16.12 of the $100 November cap

TOTAL: $2.96

## 7. Questions (asked with tap answers)
1. Approve the plan (Flow first for the 4 product clips, ceiling $2.96)?
2. Insect bites: leave out (brand site + Amazon say scrapes, cuts, burns, blisters) or add one line as the TikTok Shop title says it?
3. House of Rameau version (free re-cut with on-screen hook text, no captions): now or later?

## 8. Prompts (final, written with prompt-master; all 12 pass grace/prompt_check.py lint)
| Item | Model | Prompt file |
|---|---|---|
| Stills S1-S6 | nano-banana-pro (Kie) | prompts/still_S1.txt ... still_S6.txt (full text on the review page) |
| Clips S1, S4, S5, S6 | Flow (Omni Flash) kit; fallback wan/3-0-video 720P (Kie) | prompts/S1.txt, S4.txt, S5.txt, S6.txt |
| Clips S2, S3 | bytedance/seedance-2-mini (Kie), first frame = approved still | prompts/S2_seedance.txt, S3_seedance.txt |
References per shot: prompts/refs.json (product sheet, front-label close-up, lettering close-up, cap-off pump photo for S1, real setting photo, Grace's hand sheet for S5; S3 also gets the approved S1 still for the child's hand).
