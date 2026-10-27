# Production Book: HEVEBLUE Black Yuja Bean Lifting Auto Eye Cream (Grace), 2026-10-27

Sent to Ralph: https://claude.ai/artifact/Tc331r1KmPWRDFzm7d9p4K (2026-10-27)

## 1. Job
- Client: Grace  Product: "HEVEBLUE Black Yuja Bean Lifting Auto Eye Cream" (15 ml, auto-vibrating chrome tip)  Route: hands + hand-free AI over Grace's voice, product lock, Flow first (`.claude/skills/ugc-product-ad/references/product-lock.md`, `grace/flow/README.md`)
- Job folder: `ugc/heveblue-eye-cream/`  Target length: ~34 s  Shots: 10 (6 HAND / 4 HAND-FREE; 3 face crops: under-eye x2, neck)
- Your video idea: @momfindsbyfaith 730K https://www.tiktok.com/@momfindsbyfaith/video/7680831216869821710 (same product). Also modeled on @maddybeautyfinds 1.8M https://www.tiktok.com/@maddybeautyfinds/video/7690713735131909407 and @alexandraryoo 629K. Two of the three open on the tip touching a glass of water so the rings show the buzz: that is our opener.

## 2. Gate result (`python3 grace/gate.py ugc/heveblue-eye-cream`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read (+ live rules doc) | proof/playbook.md | OK |
| Audience research | research/audience.md (2,595 phrases, 456 TikTok comments, retailer reviews; Reddit 403 this session) | OK: "80-90% of them are just moisturizer repackaged", "Can I wear concealer over it without it rolling or peeling?", "So which ones work??" (658 likes) |
| Coach research (shop + tag x2 + discover + video x7) | research/coach_research.md | OK: same product at 1.8M / 730K / 629K views |
| Daily viral board | research/coach/viral-2026-10-27.json | OK (36 beauty shop videos today) |
| Product facts (source) | research/product_facts.md, product_truth.json | OK, size is an estimate (question 4) |
| Hooks modeled on named winners | research/hooks.md | A H094 (script), B H077, C H099 |
| Humanizer | proof/humanizer.md | OK, Grace's posted voice |
| Readability (grade) | research/readability_v1.txt | 2.6 |
| Banned-phrase check | gate.py | OK |

## 3. Script (Grace cloned voice, ~34 s, 121 words)
V1, recommended:
1. Okay, watch what happens when I touch the tip of this eye cream.
2. Hear that? It turns on by itself. Twelve thousand vibrations a minute.
3. Let's be for real, most eye cream is just lotion that ends up on your finger.
4. Then your concealer still creases by lunch.
5. This one has the massage tip built in, so a tiny dot gets worked right in.
6. It's yuja water, black bean and collagen for dry skin.
7. It goes on smile lines and your neck too.
8. People say that cool metal tip makes plain eye cream feel boring.
9. Cold weather dries out under eyes, so grab one for you and one for your mom's stocking.
10. I linked it in the orange cart for you.
Why: hook proves itself on screen in second 1 (water rings + the buzz sound); pain in their words (lotion on your finger, concealer creases); how it works, what's in it, where it goes; the honest line is what people say (Grace hasn't used it); real season (cold, holiday stockings) and two units; her orange-cart close.
Caption: "Hear that? It turns on by itself 👀 Yuja water, black bean and collagen, with a massage tip built in. #ad #heveblue #eyecream #kbeauty #koreanskincare #tiktokshopfinds"
Source of each line: research/line_sources.md. No on-screen text unless you say yes (option: "does your eye cream do this?").
Flag: the listing says to keep the tip away from water when cleaning it. The two top videos (1.8M, 730K) and the brand's own photo 1 show it in water anyway (question 2).

## 4. Shot list
| # | ~Window (s) | Words | On screen | HAND? | Clip |
|---|---|---|---|---|---|
| S1 | 0.0-3.3 | Okay, watch what happens when I touch the tip of this eye cream. | Hand holds the tube tip-down; the chrome tip touches the water in a glass coupe on a bathroom counter, rings spread (riskiest, made first) | HAND | Flow first (Omni) |
| S2 | 3.3-7.4 | Hear that? It turns on by itself. Twelve thousand vibrations a minute. | Top-down macro into the glass: fine rings pulse out from the tip | HAND | Flow first (Omni) |
| S3 | 7.4-11.6 | Let's be for real, most eye cream is just lotion that ends up on your finger, | Fingertip with leftover eye cream, thumb rubs it around (no product) | HAND | Seedance 2.0 Mini (Kie) |
| S4 | 11.6-13.8 | Then your concealer still creases by lunch. | Under-eye close-up, concealer settled into fine creases, slow push-in, she blinks (no mouth) | HAND-FREE + face crop | Seedance 2.0 Mini (Kie) |
| S5 | 13.8-18.4 | This one has the massage tip built in, so a tiny dot gets worked right in. | Chrome tip glides under her eye spreading a small dot of cream (no mouth) | HAND + face crop | Flow first (Omni) |
| S6 | 18.4-21.3 | It's yuja water, black bean and collagen for dry skin. | Tube, cap on, lying in a stone bowl of black beans, a cut yuja beside it, slow push-in | HAND-FREE | Flow first (Omni) |
| S7 | 21.3-23.9 | It goes on smile lines and your neck too. | Tip glides up the side of her neck toward the jaw (no mouth) | HAND | Flow first (Omni) |
| S8 | 23.9-27.3 | People say that cool metal tip makes plain eye cream feel boring. | Tube standing tip-up in a small glass tumbler on a bedroom vanity, slow camera arc | HAND-FREE | Flow first (Omni) |
| S9 | 27.3-31.6 | Cold weather dries out under eyes, so grab one for you and one for your mom's stocking. | Hand drops ONE capped tube into a red Christmas stocking on the fireplace | HAND | Flow first (Omni) |
| S10 | 31.6-34.5 | I linked it in the orange cart for you. | End: ONE tube on a small white dish on a vanity by a teal wall, slow push-in | HAND-FREE | Flow first (Omni) |
Rooms: 6 real photos (rooms/SOURCES.md): sage tile bathroom, pink tile bathroom, bright bedroom vanity (all Pexels), fireplace with red stockings, marble counter, teal wall vanity. Bright neutral grade.
Hand: Grace's hand sheet (question 1: with or without the bracelet), French tips, her rings, cream knit sleeve.
Face crops (S4, S5, S7): Grace's skin, brows and eye from her own photos (grace/ref), cropped eyebrow-to-cheek or jaw-to-collarbone, NO mouth on screen while her voice talks.
Sound: the winners lean on the buzz ("can you hear that?"); AI clips are silent, so I add a free real buzz sound effect under S1-S2 (question 7).

Real product (refs/product_sheet.png, real listing pixels only): one slim tube about 8 times as long as wide; top 60% matte white with a flat crimped white end; black serif print "BLACK YUJA BEAN / LIFTING AUTO / EYE CREAM", a thin black oval with the black "HB" monogram and tiny "HEVE" / "BLUE", seven ingredient lines, "15ml / 0.50 FL. OZ."; bottom 40% polished chrome: a smooth cylinder with a thin seam, one thin black ring, then a short chrome spool-shaped tip with a flat round end and one tiny hole. Matte black cap over the tip when stored (S6, S9 cap on; the rest cap off). No button, no light, no box. Size ~16 x 2 cm is MY ESTIMATE (no maker dimensions online).

## 5. Order of work (machine time ~40 min + your stops; each Flow take ~2-3 min on your phone)
All 10 stills at once (S1 and S5 checked first) -> still storyboard on the review page (stop 1) -> S1 Flow kit first, the riskiest (water rings from the tip) (stop 2: you make it, I QC it) -> the other Flow kits + S3/S4 on Seedance -> VO (Grace cloned, echo check <= 150 ms) -> cut + QC (2x edges, first second, tube never changes, no mouth, REMOVED.md, verify_fix) + compare vs @maddybeautyfinds -> AI finish -> review page (stop 3) -> Drive "HEVEBLUE Eye Cream (Grace)" as CURRENT.
Free fixes first: trim to the clean window before any redo.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image on Kie (nano-banana-pro) | 10 x $0.09 | 0.90 |
| Two likely still redos (face crops are the risk) | 2 x $0.09 | 0.18 |
| S3 + S4 clips (no product), Seedance 2.0 Mini on Kie, 4 s | 2 x $0.164 | 0.328 |
| Product clips, Omni 1.1 Flash in your Flow app (12 credits each, 96 credits) | 8 x $0 | 0.00 |
| ...same 8 on Kie only if Flow fails or you can't (asked first) | 8 x $0.315 | 2.52 |
| One likely clip redo, asked before it runs | 1 x $0.315 | 0.315 |
Expected spend with Flow: $1.41. The total includes the Kie fallback so nothing surprises you. ElevenLabs: ~620 chars (Grace cloned).
Month so far (`python3 grace/spend.py`): $189.88 (no cap in October). Kie balance 1,477 credits (auto-refill).

TOTAL: $4.243

**Approve?**

## 7. Questions
1. Hand: Grace's sheet with the bracelet (default, as the last jobs) or without?
2. Water opener: keep the tip-in-a-glass-of-water opener like the 1.8M and 730K videos (default), or swap it for the tip buzzing a dot of cream on her fingertip (the listing says keep the tip away from water when cleaning)?
3. Face crops on S4, S5, S7 (Grace's under-eye and neck, no mouth) (default), or hands and product only, no face at all?
4. Size: does Grace have the sample? 3-4 phone photos (front, tip, in her hand) would replace my 16 cm estimate and the listing renders. Default: go with the estimate.
5. Stills on Kie ($0.90) or your Gemini app ($0, I send the kit)? Clips in Flow first (default) or straight to Kie?
6. On-screen text: none (default), or "does your eye cream do this?" on the opener?
7. Buzz sound: add a free real vibration sound under S1-S2 (default yes), or voice only?

## 7b. Ralph's answers (2026-10-27: "1. Without 2.keep 3. Under eye neck close 4. No 5.kie and Kie 6 none 7. First 2 shots")
1. Hand sheet WITHOUT the bracelet (bare wrist; rings as in the sheet: crown stack ring on the ring finger, gold heart ring on the middle finger, blue band on the thumb). 2. Water opener kept. 3. Face crops on S4, S5, S7 (under-eye and neck, no mouth). 4. No sample: go with the 16 x 2 cm estimate. 5. Stills on Kie, the 8 product clips on Kie (Omni 1.1 Flash, $0.315 each; Seedance first-frame if Omni gives 500s), no Flow kits. 6. No on-screen text. 7. Free buzz sound effect under S1 and S2 only.
Expected spend now: $3.76 (10 stills + 2 Seedance + 8 Omni on Kie) within the $4.243 TOTAL.

## 8. Prompts
Every still and clip prompt: prompts/still_<ID>.txt and prompts/<ID>.txt (built by build_prompts.py from shots.json, written with prompt-master, linted PROMPT_LINT_OK and marked checked). Still refs, numbered and named: 1 product sheet, 2 real print close-up, 3 real chrome tip close-up (or the black cap when it is on), 4 the room photo, 5 Grace's hand sheet, 6 Grace's face (face shots). Clip refs: 1 the approved still ("Recreate image 1 exactly as the first frame"), 2 print, 3 tip or cap, 4 sheet, 5 hand sheet. Every prompt: size first, the print matched letter for letter, chrome never gold, no button or light, one grip on the chrome, never turns or flips, no mouth in face crops, no sparkle words, no text, no music, no voice.
