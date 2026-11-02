# Coach research (2026-11-02)

## What ran, and what failed
- `tiktok.py tag` and `shop` with headless Chromium returned nothing this session: TikTok served its "Something went wrong" page on every hashtag page (item_list API answered 200 with an empty body) and the shop search returned no products (logs: research/coach/playwright_failed/). Tested once alone after the parallel run, same result.
- Workaround (free): hashtag pages loaded in camofox (anti-detection Firefox), video links read from the page (research/coach/raw_links/), then each video's stats pulled with tiktok.py's own `fetch_item`/`summarize`, same JSON format as `tag` (60 days): research/coach/tag_cerave, tag_ceravebundle, tag_ceravetiktokshop, tag_winterskincare, tag_dryskin (#dryskin: 49 videos in 60 days, 18 shop, none selling CeraVe; #winterskincare: 97, 7 shop, none CeraVe). The viral board ran the same way (research/coach/viral-2026-11-02.json).
- `discover` worked in headless Chromium: research/coach/discover/ (cerave-hydrating-facial-cleanser, cerave-moisturizing-cream; cerave-moisturizer-for-dry-skin has no page).
- `shop`: captcha in camofox too; web-index listing data instead in research/coach/shop_cerave/shop.md.
- `video` on 6 shop videos: research/videos/<id>/ (meta.json, transcripts, hook.png, sheet.png, video.mp4). Hook and sheet frames looked at. Cuts = ffmpeg scene detection (`select='gt(scene,0.3)'`).

## Top shop videos (TikTok's shop-video flag, product anchor = CeraVe)
| # | Video | Views / saves | Length, cuts | Hook (spoken / on-screen / first visual) | CTA | Format |
|---|---|---|---|---|---|---|
| 1 | @dailydoubledeals22 https://www.tiktok.com/@dailydoubledeals22/video/7685123953416785183 | 521,000 / 172 (0.03%), 5.1K followers | 29 s, 8 cuts (0.27/s) | "I have never seen a Cerave bundle this big before." / "HOLY CERAVE JACKPOT !!" + "CHECK YOUR COUPONS" / the products fanned in one hand, fall decor | "I'll drop a link... I would grab this so fast before this completely sells out." | faceless product-only footage + voiceover, deal angle (Ceramide Boost bundle) |
| 2 | @eldonoferton22 https://www.tiktok.com/@eldonoferton22/video/7689210935516400926 | 304,200 / 245 (0.08%), 10K followers | 15 s, 9 cuts (0.6/s) | "Look at the megacombo..." / no text / open white gift box, all products on shredded paper, finger points at each | "If you still get the discount, touch the cart" | faceless, one overhead shot of the open box + VO naming every item, "Epic Music" bed |
| 3 | @lordkierra https://www.tiktok.com/@lordkierra/video/7585784888108797239 | 199,600 / 350 (0.18%), 794K followers, posted 2025-12-20 | 15 s, 4 cuts | NO talking. Music: "Nutcracker: Dance of the Sugar Plum Fairy". On-screen (whole video): "The CeraVe Hydrating Facial Cleanser hasn't broken me out AND has been perfect for the dry winter weather... periodddd" / frame 0: cleanser pumped into the palm right at the lens | none spoken; ends holding the bottle to camera; caption "affordable, safe, and effective!" | MUSIC-ONLY routine demo (Hydrating Cleanser = our product), winter angle, paid partnership |
| 4 | @dusteerosexo https://www.tiktok.com/@dusteerosexo/video/7689297898550414605 | 111,500 / 39 (0.03%) | 33 s, 3 cuts | "Has to be a mistake." / "this can't be real" / face + arms full of CeraVe | "I'll link it on here. You better run before it's gone." | talking head, deal angle |

Music-only short winners worth copying (same products):
- @shakyra._ https://www.tiktok.com/@shakyra._/video/7594984451361361165 : 17,400 views on 8.8K followers, 67 saves (0.39%, the best save rate here), 11 s, 8 cuts (0.7 cuts/s), music "Cyclessss", caption "a must have for the winter". Beats: face with cream on > tub held to camera > lid off > cream texture in the open tub > apply on cheeks > tub held next to face. Title text "CERAVE INTENSIVE MOISTURIZING CREAM" all the way + small feature captions ("FOR DRY TO VERY DRY SKIN", "3 CERAMIDES, 5% HYDRO-UREA, & SHEA BUTTER"). NOTE: her Intensive Moisturizing Cream is a TUB with a blue lid; check Grace's real product photos before any still (the brief says tube).
- @drews_tts https://www.tiktok.com/@drews_tts/video/7640982874212027678 : 50,900 views on 2K followers, 11 s, 2 cuts, store-shelf pan of Moisturizing Cream tubs, text "Huge DISCOUNT / Limited Time Only" with a coupon voiceover (0.01% saves: deal hype gets views, not saves).

## Viral board (research/coach/viral-2026-11-02.json, beauty + skincareroutine, dryskincare, winterskincare, 30 days)
- 911 videos scanned, 242 shop videos. No CeraVe video on the 30-day board.
- Skincare leaders: @ofertasenlausa medicube PDRN Pink Glow Edit 553,600 views, 0.60% saves, 31 s, "Epic Music" bed (https://www.tiktok.com/@ofertasenlausa/video/7701377739655466253); @trendmart070 medicube sets 303,100 and 416,300 (sets/bundles keep winning).
- Very short videos travel: 6-9 s shop videos at 858K-2.6M views (@atnorah 6 s, @shopwithtaye 8 s, @alpha_finds1 9 s), so 10 s is a good length.
- Winter skincare sets are only starting (Kind Science 3-Piece Winter Hydration Set 557 views, Aquaphor Hydration Skincare Kit new): room for a winter bundle video now.

## Patterns
- The bundle sells on "how much you get": every bundle winner shows ALL products together in the first second (fanned in hand, open gift box, arms full). 53 of 90 #ceravebundle shop videos sell the Ceramide Boost bundle.
- Winter is stated, not acted: lordkierra's and shakyra's winners say "dry winter weather" / "a must have for the winter" in text or caption over a normal routine.
- Music-only works for this brand: the two music-only winners have the highest save rates in the set (0.18%, 0.39%) vs 0.03-0.08% for the deal voiceovers.
- Pace: short winners cut every 0.7-1.5 s (shakyra 0.7 cuts/s, eldonoferton 0.6/s); lordkierra holds longer handheld takes.

## What a 10 s music-only product video should copy
1. Frame 0: all four products together (open box or flat lay) so the bundle reads at once (winners 1, 2).
2. Then one quick shot per product in routine order, each with its texture or use: cleanser pumped into the palm (lordkierra frame 0), cream scooped from the open container (shakyra), balm on lips, SPF lotion pumped for morning; ~1 cut per 1-1.5 s (8-9 shots in 10 s).
3. Winter cues in frame (window frost, sweater, mug) instead of words; the "winter" line goes in the caption.
4. Seasonal music bed (lordkierra used holiday music in December); no talking.
5. End on all four held together / in the box (the shop link carries the CTA). On-screen text only on Ralph's yes (hard rule 6).
