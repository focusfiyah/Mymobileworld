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
