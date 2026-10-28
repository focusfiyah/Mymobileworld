# How Grace re-edited the PRITECH video that sold (studied 2026-10-28)

Ralph 2026-10-28: "Learn from the video style she used on that to have a better understanding of what she wants."
Three videos compared, same script and same voice (Grace's own recording of her storyboard script):
- **Oct 23** https://www.tiktok.com/t/ZPLAonsjU/ : her first post. 13 shots, all her own real footage (her hand, the
  real black brush on a clear acrylic box, LED lights, a pink box picture, the real box at the end). 1,327 views, no
  sale reported.
- **Our V1** (`ugc/pritech-cleansing-brush`, approved 2026-10-24): 9 AI clips of 4 s, one per line, our order
  S1 cheek lather (hook) → S2 tap → S3 towel → S4 bristles → S5 vibration button → S6 heat button → S7 warm end on
  cheek → S8 counter dolly → S9 brush in stand.
- **Oct 25, the one that sold** https://www.tiktok.com/t/ZPLAEVuMv : Grace mixed the two. 1 sale on 1,022 views.

## Shot map of the selling edit (cuts measured with ffmpeg scene detection)

| # | Time (s) | Words over it | Source |
|---|---|---|---|
| 1 | 0.0-3.6 | "If you're not washing your face with a cleansing brush, what are you doing?" | Grace real: brush in her hand, LED goes red to green, acrylic box, + her text line |
| 2 | 3.6-4.9 | "Because using your hands leaves makeup and oil behind" | our V1 S2 (hands under the tap) |
| 3 | 4.9-7.9 | "and towels just transfer bacteria right back into your skin" | our V1 S3 (makeup towel) |
| 4 | 7.9-10.0 | "This one has soft silicone bristles" | our V1 S4 (bristle push-in, brush in stand) |
| 5 | 10.0-11.3 | "five vibration settings" | our V1 S5 (hand holds it, button side) |
| 6 | 11.3-12.5 | "and a warming feature that heats up to 104 degrees" | our V1 S6 (heat button, metal end) |
| 7 | 12.5-15.5 | "so you can get that little extra spa feel" | our V1 S1 (lather on the cheek), moved from the hook to here |
| 8 | 15.5-15.8 | "And for something you do every single day" | Grace real: brush going into its stand |
| 9 | 15.8-16.1 | (same line) | Grace real: brush in stand on the acrylic box |
| 10 | 16.1-16.7 | (same line) | Grace real: hand lifts it |
| 11 | 16.7-16.9 | "you might as well do it the right way" | Grace real: brush in stand, wide |
| 12 | 16.9-18.6 | (same line) | Grace real: LED green, in hand |
| 13 | 18.6-19.3 | "Go grab yours in an orange cart" | Grace real: in hand, metal end |
| 14 | 19.3-20.7 | "before you forget about this" | Grace real: the real PRITECH box |

Dropped from our V1: S7 (warm end on the cheek), S8 (counter dolly), S9 (end shot in the stand).
Dropped from her Oct 23: the pink box picture (wrong colour) and the slow product-only shots over the pain lines.

## What she wants, built into OUR videos (Ralph 2026-10-28)
Ralph 2026-10-28: "I don't want to mix her real videos with ours. We just need to adopt the style to the videos we
produce." So we never cut her real footage into our videos; we copy how her edit works, with our own AI clips.
1. **Open on the product working in a hand, from frame 0.** Her hook shot is the brush held up with its light
   switching on: our hook clip does the same (product in hand, a visible "it's on" moment: a light, a click, a pump,
   steam), not a face or a room.
2. **Show the pain, then each feature as it is said.** The middle is one clip per phrase: the pain lines get the pain
   (hands under the tap, the dirty towel), then each feature on its own words. Her Oct 23 post had product-only shots
   over the pain lines and did not sell.
3. **Cut on the first word of each phrase.** Middle shots 1.2-3 s (average 1.5 s; our V1 clips ran 4 s), then very fast
   cuts (0.2-0.6 s) over the CTA lines.
4. **The face-use shot goes on the payoff line** ("that little extra spa feel"), not the hook.
5. **Close on a fast run of product-in-hand shots**, all moving (pick up, set in the stand, light on), ending on the
   product. No still-life endings: she cut our counter dolly and end shot. (She ended on the real box; our rule is no
   pictures of boxes, so a box end shot only on Ralph's word.)
6. **Her own text line on the first frame** is hers to type in TikTok; we burn in nothing unless Ralph says yes.
7. **Her own voice:** she records the VO herself; the clone is being rebuilt from those recordings (`grace/voice/README.md` round 5).

## Black Friday PRITECH video (NOT made yet, Ralph 2026-10-28: "not right now")
When Ralph says go: our own AI clips cut in this style (rules 1-5), a gift / Black Friday deadline and a CTA that asks
for two (the sold video has no deadline and asks for one). Hook from the hook library (Gift or Time Pressure), Grace
records the VO. New shots, framing and room (not V1-V4 footage again), no real footage of Grace's. Plan + cost to Ralph first.
