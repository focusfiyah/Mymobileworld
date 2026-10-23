# Production Book: Power Bank Flashlight V2 (Grace), 2026-10-22

## 1. Job
- Client / own content: Grace  Product: TINEKO clip-on COB power bank flashlight (SMILING SHARK print, Grace's real unit)  Route: hands-only AI + product lock (`.claude/skills/ugc-product-ad/references/product-lock.md`)
- Job folder: `ugc/powerbank-flashlight-v2/`  Target length: ~28 s (Ralph's script reads 34 s at 150 wpm; Grace's pace is quicker)  Shots: 9 (5 HAND / 4 HAND-FREE)

## 2. Gate result (`python3 grace/gate.py ugc/powerbank-flashlight-v2`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | grace/PLAYBOOK.md, checklist.json rules_applied | OK |
| Coach research (tag/shop/discover + video x3) | research/coach_research.md, shop_flashlight.txt, tag_powerbankflashlight.txt, videos/ (3 transcripts) | OK |
| Daily viral board | research/viral/viral-2026-10-22.json | OK |
| Product facts (source) | research/product_facts.md, research/size.md (Grace's box) | OK |
| Hooks modeled on named winners | research/hooks.md | OK (Ralph's own hook, verbatim override) |
| Humanizer | research/humanizer_report.md | OK (his words kept) |
| Readability (grade) | research/readability.txt | grade 4.5 |
| Banned-phrase check | gate.py | OK |

## 3. Script (final, Humanized)
Ralph's script word for word (override in checklist.json; "flickering" = his fix):
> Who in the world made this??? Because what do you mean I can charge my phone with this, hang it up in my tent for hands-free lighting, AND use it as a regular flashlight with a focused beam? And it has a flickering mode, too, for emergencies! This is the kind of gadget that makes sense to keep with your camping gear or emergency kit. And it costs less than a McDonald's Happy Meal! I'm linking it in the orange cart for you!

Source of each line: Ralph (research/line_sources.md). Product facts behind it: charges a phone (USB-A under the cap), hangs by its clip, focused zoom beam, flashing mode (Grace's box). "Less than a Happy Meal" = no price number spoken; McDonald's never on screen.

## 4. Shot list
| # | Window (s) | VO words | On screen | Face? | VO or lip sync | Prompt notes |
|---|---|---|---|---|---|---|
| S1 | 0-2.5 | Who in the world made this??? | HAND holds it up, panel lit, clip on top | no | VO | Ralph's Gemini still; Omni, lift + push-in |
| S2 | 2.5-6 | ...charge my phone with this | HAND-FREE on table, cap pulled, cable to phone | no | VO | Ralph's still; Omni, push-in, no hand |
| S3 | 6-9 | hang it up in my tent for hands-free lighting | HAND-FREE hanging in tent, panel lit | no | VO | Ralph's still; Omni, gentle sway |
| S4 | 9-12.5 | AND use it as a regular flashlight with a focused beam? | HAND POV beam down trail | no | VO | Ralph's still; Omni, walk; riskiest = TEST CLIP |
| S5 | 12.5-15.5 | flickering mode, too, for emergencies! | HAND-FREE on rock, FRONT lens flickers, panel off | no | VO | Kie still; Omni; flicker added free in the edit if Omni won't blink |
| S6 | 15.5-18.5 | the kind of gadget... camping gear | HAND-FREE clipped on backpack at camp | no | VO | Kie still; Omni, dolly past |
| S7 | 18.5-21 | or emergency kit | HAND lowers it into a plain pouch | no | VO | Kie still; Omni |
| S8 | 21-24.5 | costs less than a McDonald's Happy Meal! | HAND stands it on picnic table, clip on top (no food, no box) | no | VO | Kie still; Omni |
| S9 | 24.5-28 | I'm linking it in the orange cart for you! | HAND clips it to backpack strap | no | VO | Kie still; Omni |
Outfit: n/a (hands only, no sleeve beyond the wrist)  Setting: one pine-forest campsite at dusk, sky darkened closer to night while the campsite stays visible (Ralph 2026-10-22: "the dusk sky darkened closer to night while keeping the campsite visible"; in every still and clip prompt), tent, picnic table, mountains  Nails / person details: Grace's hand: French tips, blue band, gold solitaire, crown ring, gold watch-link bracelet, pearl chain with leaf charm (matches Ralph's S1/S4)  Real product confirmed (top, cap, label): Ralph's photos of Grace's unit (refs/real/, refs/product_sheet_real.png): clip on top, light blue-grey body, frosted panel, orange power button, dark grey end cap with SMILING SHARK, lens at the cap tip, ports under the cap.

QC of Ralph's 4 stills (2x crops): S1, S3, S4 product order, button, logo, rings and nails all match. S2: part order right, cap pulled with the cable in the port; the table wood looks over-sharpened (AI texture) and there is a small orange blob at the far left edge: free fix (soft blur on the wood + crop the edge) before its clip. Sky: S1-S4 skies are still a lighter dusk blue; in the grade I darken only the sky toward night (free) so they match S5-S9, campsite left as is.

## 5. Order of work
Kie stills S5-S9 at once (same Gemini-kit prompts + refs, plus Ralph's S1 as the hand/look reference and S2 as the campsite reference so all 9 match) → QC 2x → storyboard of all 9 on the review page (free to review) → ONE test clip, S4 (beam must come from the lens and land where it points) → the other 8 clips at once → VO (Grace cloned, echo gate) made while clips render → cut (reuses ugc/powerbank-flashlight/cut.py) → AI finish → gate --stage cut → review page + push + email.
Free fixes planned: S2 wood blur + edge crop; sky-only darken on S1-S4 to match; S5 flicker made in the edit (lens light keyed on/off) if Omni won't blink; trims to the clean window of each take.

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| S1-S4 stills (Ralph's Gemini app) | 4 x $0 | 0.00 |
| S5-S9 stills, Kie nano-banana-pro | 5 x $0.09 | 0.45 |
| Product-lock clips, Omni 1.1 Flash on Kie, 4 s | 9 x $0.315 | 2.835 |
| One likely redo (one still + one clip) | $0.09 + $0.315 | 0.405 |
Total Kie: $3.69  ElevenLabs: ~430 chars (subscription)  Contingency redos (each asked separately): beyond the one above, $0.09 per still, $0.315 per clip, $0.84 per Omni edit
Month so far (`python3 grace/spend.py`): $151.23 Kie (no cap in October)

TOTAL: $3.69

**Approve?**

## 7. Questions (all of them, now)
1. OK to use your S1 (hand/look) and S2 (campsite) as extra references on the Kie stills so all 9 shots match? (free, same price)
2. Anything in your 4 stills you want changed before they become clips? (S2's over-sharp wood I fix free unless you say leave it)

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| S5-S9 stills | Kie nano-banana-pro (Gemini 3 Pro Image) | gemini_app/prompt_S5.txt ... prompt_S9.txt + refs each names (ref1 sheet, ref2 true shape, ref3 lens / ref4 hand, ref6 logo) + stills/S1.png look ref + stills/S2.png place ref |
| S1-S9 clips | Kie google/gemini-omni-flash-1-1, 4 s, 1080p | prompts/clip_S1.txt ... clip_S9.txt (image 1 = the still, 2 = SMILING SHARK cap close-up, then lens/port close-up where seen, the product sheet, Grace's hand on hand shots) |
