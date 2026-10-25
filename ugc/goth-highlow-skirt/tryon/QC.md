# Try-on test QC (2026-10-22), 2x crops in tryon/qc_*_2x.jpg

Inputs: person = stills/FULL2.png (already wears the earlier AI skirt: fitted midi, see-through chiffon hem); garment = real listing front 28_x_13987564.webp. One image per model, no retries.

| Product truth | FASHN v1.6 ($0.075) | Kling Kolors ($0.07) |
|---|---|---|
| Real skirt shape (bustled ruching, side cascades, long back) | NO: kept FULL2's AI skirt (skirt area mean diff vs input 9.4, face 6.4 = unchanged) | YES: bustle ruching, cascading sides, dark centre panel like the real photo |
| Solid fabric, legs never visible | NO: the old see-through hem (legs show) | YES: legs not visible through it |
| Colour = dark chocolate brown (real mean RGB 70,51,46) | brown 55,39,34 (FULL2's colour) | greyer/olive 51,43,37 (free colour-match fixes it) |
| Two front waist strings | FULL2's two strings | not clear: channels show cords, no hanging tails; hands pinch fabric |
| Face, braids, skin unchanged | yes | yes |
| Boots unchanged | yes | shape yes; hem now covers the boot tops, ragged hem edge at 2x by the boots |

FASHN verdict: FAIL for this test. It returned the input almost untouched, so we learned nothing about the real skirt. Most likely cause: FULL2 already wears a similar brown skirt. A fair re-test needs a person photo wearing a different bottom (plain leggings or jeans) ($0.075, asked first).
Kolors verdict: PARTIAL PASS. First model to put the real skirt's structure on Grace without inventing a new design. Needs: a colour match (free), a cleaner hem by the boots, and the front waist strings are not readable. Worth using as the look-lock stills route, with a re-test on a neutral-bottom person photo.

## Re-test: FASHN v1.6 on Grace's real photo in plain brown wide-leg pants (Ralph's photo 3, $0.075)

| Product truth | FASHN on the real photo |
|---|---|
| Real skirt design | YES at the waist: the real bunched front and both drawstring channels, matching the listing photo at 2x |
| Two front waist strings | YES: both cords run down from the waistband (the first result that shows them) |
| Solid fabric, legs never visible | YES: dark centre panel, no legs show through |
| Colour (real 70,51,46) | 59,43,41, warmer and closer than Kolors (51,43,37) |
| Hem / silhouette | NO: the skirt kept the pants' shape. It's a narrow column pulled in at the ankles like a cuff, with no flared ruffle hem |
| Face, arms, shoes unchanged | yes (mean diff 2.0 / 6.6 / 3.5) |

FASHN re-test verdict: the best waist and front of any model so far; the hem fails because it copied the shape of the pants. A photo of Grace in shorts, bare legs or a short fitted dress should fix the shape (FASHN fills the area of the old garment). Usable now for waist-up and waist-to-knee framing.

## Re-test 2: FASHN, segmentation_free off (same photo 3, $0.075)
Worse on every count: colour washed to mauve (99,73,70 vs real 70,51,46); still a narrow column cuffed at the ankles; the plant pot was redrawn as a brown smear and the boots were redrawn. Verdict: FAIL. Keep the default (segmentation_free on). The shape needs a different input photo (shorts / bare legs), not a setting.

## Re-test 3: FASHN on Grace's own TikTok frame (black shapewear shorts, bare legs; @shewiththeglow 7684001442977352991 at 13 s), $0.075
FASHN returned the frame unchanged: no skirt at all, only a thin dark streak on one shin. Her outfit is a one-piece shapewear bodysuit, so FASHN finds no separate bottom garment to replace. Verdict: FAIL (no-op). FASHN needs a real separate bottom (pants worked, round 23); a bodysuit or bare legs gives it nothing to swap.

## Re-test 4: Kolors on the same TikTok shapewear frame, $0.07
Best overall so far. Silhouette right: full, flowing, long, wider at the hem (not a column), the dark centre panel low down, and solid fabric with no legs showing. Mean colour 70,50,40 vs real 70,51,46: brightness right, but the satin sheen reads a little khaki/olive (a little less blue); a free colour shift fixes that. Misses: the front ruching is softer and smoother than the real deep bunching; only the right drawstring channel shows its gathering clearly and the left is faint; no hanging string tails at the waist. Her face, arms, hands and room are unchanged; the black shapewear cincher still shows above the skirt (it reads as a black top). Verdict: PARTIAL PASS, the best base so far for look-lock stills.

## 2026-10-25 L4 shortest test (book rev 5): Kolors on Gemini A1 + listing 01 (full on-model photo), $0.07
FAIL. (1) Kolors took the whole outfit from the photo: the black long-sleeve top became the model's strapless pinstripe corset. (2) Length: the front hem fell below the knee with a ragged edge, not the upper thigh. (3) Output only 723x1296 (input 1536x2752). Lesson: give Kolors a skirt-only crop (tryon/g_01_skirt.jpg), never a full-outfit photo; Kolors does not hold a pulled-up length, so the short looks need another route.

## 2026-10-25 option 1: Kolors L1 knee (A1 + garment_front) and L2 back (A3 + garment_back), $0.14
FAIL, both. Kolors kept Grace's black shorts and drew only a short dark olive ruffle band below them (thigh to knee); no waistband, no front ruching, no drawstrings, no long back, wrong colour. On the Gemini bases (separate shorts) Kolors treats the shorts as the bottom and adds a hem under it. Kolors is dropped for this job: 3 tries on the new bases, 0 usable ($0.21).

## 2026-10-25 Gemini app skirt stills (Ralph, $0)
L1 knee PASS, L2 back PASS, L4 shortest PASS (two drawstrings, ruching, front at thigh, back long, solid). L3 one leg r1 FAIL: length right but the skirt became a single-drawstring wrap skirt with a diagonal ruffle; redo prompt keeps both channels + ruching close-up ref (prompts/v2_gem_L3.txt).
L3 one leg r2 PASS (both drawstrings + ruching kept, picture-left side up, one leg above the knee). All 4 stills approved for Flow; 9:16 neck-down start frames in flow_kit/still_L1..L4.jpg.
L1 Flow take (clips/L1_flow.mp4) PASS at 3 fps + 2x (0.0/1.8/3.5 s): both drawstrings, real ruching, fingers pinch the strings at the waistband and tug, whole wrists, no hand at the hem, boots unchanged, head never in frame.
2026-10-25 bedroom 2 (Ralph's pick) via Gemini app on the 4 approved stills: all PASS at 2x (skirt unchanged, hands whole, boots right). Waist-to-floor 9:16 crops right-aligned so the mirror frame shows (flow_kit/room_L1..L4.jpg). Clip prompts v2_L1..L5 updated: mirror, bedroom, tripod, fixed frame.
L1 bedroom Flow take (clips/L1_room_flow.mp4) PASS at 3 fps + 2x (0.6/1.0/1.2/2.6 s). Note: frame 0 already has her hands at the waist, so the cut uses the tug (about 0.8-3.0 s).
L2 bedroom Flow take (clips/L2_room_flow.mp4): 0-2.2 s PASS (back view, real tiers, no skin); 2.3-4 s FAIL (Ralph caught it: Flow turned her around, hands lighter than Grace's, a phone appears, front changes). Cut uses clips/L2_room_trim.mp4 (0-2.2 s). L2 prompt updated: no turn, no phone, no arm skin.
L2 r2 Flow take (clips/L2_room_flow_r2.mp4): failed per Ralph; L2 = clips/L2_room_trim.mp4 (r1 0-2.2 s), Ralph 2026-10-25 'just use previous'.
