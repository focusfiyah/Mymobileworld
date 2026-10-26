# Production Book: Mini Bag Charm, burgundy (Grace), 2026-10-26

## 1. Job
- Client: Grace  Product: "High-End PU Leather Basket Shape Bag Charm, 2026 Mini Keychain Charm ... Earphone Storage Bag, Christmas Pendant" (burgundy)  Route: hands + hand-free AI over Grace's voice, product lock, Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Job folder: `ugc/mini-bag-charm/`  Target length: ~26 s (storyboard 20-25 s)  Shots: 9 (5 HAND / 4 HAND-FREE)
- Model video: @the_little_beannn 331K https://www.tiktok.com/@the_little_beannn/video/7689843077464214814 (burgundy mini charm in hand at frame 0, packed with tiny things, clipped onto a bigger bag at the end)

## 2. Gate result (`python3 grace/gate.py ugc/mini-bag-charm`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read (+ live rules doc) | proof/playbook.md | OK |
| Audience research | research/audience.md (2,257 phrases, 452 TikTok comments, Reddit) | OK: worries = "Can you actually like use it?", "Did it fit??" (AirPods), "Cute but why are they $37 each?!" |
| Coach research (shop + tag + discover + video x6) | research/coach_research.md | OK: top 331K / 333K / 603K; multi-packs sell most (12,006 units) |
| Daily viral board | research/coach/viral-2026-10-26.json | OK (run today) |
| Product facts (source) | research/product_facts.md, product_truth.json | OK, 3 open items (questions 1-3) |
| Hooks modeled on named winners | research/hooks.md | A H061 (the script's), B H055, C @jessicadyfortt |
| Humanizer | proof/humanizer.md | OK, script kept, caption shortened |
| Readability (grade) | research/readability_v1.txt | 4.9 (as sent: 5.0) |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace cloned voice, ~26 s)
V1, recommended = your script + 2 small edits [+]:
1. For the person who loves anything mini…
2. How cute is this little purse?!
3. [+] You know how your earbuds always end up at the bottom of your bag?
4. It clips right onto your handbag, and you can stash your earbuds, lip balm, keys, or other tiny essentials inside.
5. The scarf and gold hardware make it look so much more expensive than a typical bag charm.
6. AND it makes the cutest little stocking stuffer!
7. Grab one for yourself [+] and one for a friend who loves all things mini.
8. It's linked in the orange cart!
Why: Grace's structure needs a pain beat (the sent script goes hook -> product), and the CTA must sell two, not one ("for yourself or a friend" = one unit). Word for word is fine too (question 4).
Caption: "For the girl who loves anything mini 🤏 It clips onto your bag and holds your earbuds and lip balm. Stocking stuffer done. #ad #bagcharm #minibag #stockingstuffer #giftideas #tiktokshopfinds"
Source of each line: research/line_sources.md. No on-screen text (the storyboard's script-font overlays are not used unless you say yes).

## 4. Shot list
| # | ~Window (s) | Words | On screen | HAND? | Clip |
|---|---|---|---|---|---|
| S1 | 0-2.5 | For the person who loves anything mini… | Hand holds the charm up by its two handles in front of a wooden table (pink candle soft behind) and brings it toward the lens | HAND | Flow (Omni) |
| S2 | 2.5-4.3 | How cute is this little purse?! | Charm standing on the table next to a white mug for scale, slow low push-in | HAND-FREE | Flow |
| S3 | 4.3-6.8 | You know how your earbuds... bottom of your bag? | Hand digs through a big brown tote, earbuds case lost under receipts and keys (no charm) | HAND | Seedance 2.0 Mini (Kie) |
| S4 | 6.8-8.6 | It clips right onto your handbag, | Hand slides the charm's gold key ring chain onto the brown handbag's handle (riskiest) | HAND | Flow |
| S5 | 8.6-12.2 | and you can stash your earbuds, lip balm, keys... inside. | Charm open on the table, lip balm inside, hand lowers an earbuds case in | HAND | Flow |
| S6 | 12.2-13.8 | The scarf and gold hardware | Macro push from the gold padlock up to the scarf knot | HAND-FREE | Flow |
| S7 | 13.8-16.6 | make it look so much more expensive than a typical bag charm. | Charm hanging on the brown handbag on a cream sofa by a bright window, slow arc | HAND-FREE | Flow |
| S8 | 16.6-19.2 | AND it makes the cutest little stocking stuffer! | Hand lowers the charm into a cream knit stocking at a fireplace, handles peek out | HAND | Flow |
| S9 | 19.2-26 | Grab one for yourself and one for a friend... orange cart! | End: ONE charm on the handbag in front of a green tree with white bows, slow pull-back | HAND-FREE | Flow |
Rooms: 4 real photos (rooms/SOURCES.md): wooden table with a pink candle (Pixabay), cream sofa by a window (Pixabay), fireplace with a tree (Pexels), green tree with white bows (Pexels). Bright neutral grade, not the storyboard's golden tone.
Hand: Grace's hand sheet WITH the bracelet (gold link bracelet + pearl chain; matches the gold hardware), French tips, her rings, cream knit sleeve.
Not used from the storyboard: the colours lineup (shot 2) and the other colours in the end shot, until I have real photos of them (question 2); the red bow; text overlays.

Real product (refs/product_sheet.png, from your listing photo 10/10): deep burgundy pebbled faux leather, bucket shape, open top (no zip, no flap); two rolled handles with darker painted edges; front strap through a small rectangular gold buckle; gold padlock (three engraved lines, no letters) on a gold ring + grommet; four gold feet; pink / light blue / white twilly scarf knotted on the right handle with a long frayed tail. No logo anywhere.

## 5. Order of work (machine time ~35 min + your stops; each Flow take ~2-3 min on your phone)
All 9 stills at once -> still storyboard on the review page (stop 1) -> S4 Flow kit first, the riskiest (hand + key ring on the handle) (stop 2: you make it, I QC it) -> Flow kits for the rest on the review page + S3 on Seedance -> VO (Grace cloned, echo check) -> cut + QC (2x edges, first second, charm never changes, REMOVED.md, verify_fix) + compare vs @the_little_beannn -> AI finish -> review page (stop 3) -> Drive "Mini Bag Charm (Grace)" as CURRENT.
Free fixes first: trim to the clean window before any redo.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 9 x $0.09 | 0.81 |
| One likely still redo | 1 x $0.09 | 0.09 |
| S3 clip (no product), Seedance 2.0 Mini on Kie, 4 s | 1 x $0.164 | 0.164 |
| Product clips, Omni 1.1 Flash in your Flow app (12 credits each, 96 credits) | 8 x $0 | 0.00 |
| ...same 8 on Kie only if Flow fails or you can't (asked first) | 8 x $0.315 | 2.52 |
| One likely clip redo, asked before it runs | 1 x $0.315 | 0.315 |
Expected spend with Flow: $1.06. The total includes the Kie fallback so nothing surprises you. ElevenLabs: ~450 chars (your plan).
Month so far (`python3 grace/spend.py`): $176.80 (no cap in October). Kie balance 255 credits (auto-refill).

TOTAL: $3.899

**Approve?**

Sent to Ralph: https://claude.ai/artifact/Uns9WGWdYcjDBsdbbeCezb (2026-10-26)

## 7. Questions
1. The clip: your listing photo doesn't show how it attaches (lobster clasp, key ring, chain?). Can you send the listing link or a screenshot of the clip, plus the size if it's listed? S4, S7, S9 wait on it; I won't invent one.
2. Colours: the storyboard shows black, white, pink, blue, tan and burgundy. Send the colour photos if you want the lineup; otherwise burgundy only (default).
3. Does an AirPods case really fit inside? The video shows earbuds going in; I'm assuming ~3 in tall x 2.5 in wide.
4. Script: V1 with my 2 edits (default), or word for word as you sent it?
5. Hand: Grace's sheet with the bracelet (default) or without?
6. On-screen text: none (default), or the storyboard's overlays?
7. Stills on Kie ($0.81) or your Gemini app ($0, I send the kit)? Clips in Flow first (default).

## 7b. Ralph's answers (2026-10-26: "1. Key ring chain 2. Burgundy only 3. Yes 4.Your version 5.with 6.none 7. Kie")
1. Attaches with a gold key ring on a short gold chain (in every prompt; placed at the left handle base). 2. Burgundy only, no lineup. 3. AirPods case fits. 4. Script V1 (with the 2 edits). 5. Hand sheet with the bracelet. 6. No on-screen text. 7. Stills on Kie ($0.81).

## 8. Prompts
Every still and clip prompt: prompts/still_<ID>.txt and prompts/<ID>.txt (built by build_prompts.py from shots.json, written with prompt-master, linted and marked checked; S4 re-marked once the clip is known). Still refs, numbered and named: 1 product sheet, 2 real padlock + buckle close-up, 3 real scarf + handle close-up, 4 the room photo, 5 Grace's hand sheet. Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), 2-3 the real close-ups, 4 the sheet, 5 the hand sheet. Every prompt: size first, the charm matched colour for colour, gold hardware never silver, no letters on the padlock, one grip, never turns or flips, no sparkle words, no text, no music, no voice.
