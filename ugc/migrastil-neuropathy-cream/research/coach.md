# Coach research (2026-11-06)
Setup this session: `import playwright` failed (ModuleNotFoundError), fixed with `pip install playwright==1.56.0`; shop.log first run shows the error, rerun OK.

Commands (logs in research/*.log):
- `shop "migrastil"` 25 products -> shop/shop-migrastil.json; `shop "neuropathy cream"` 10 products -> shop/shop-neuropathy-cream.json; `shop "neuropathy relief"`, `"foot cream neuropathy"`, `"nerve pain cream"`: "No products returned ... (no results, or TikTok served a captcha)" (shop.log).
- `discover` neuropathy-cream, neuropathy-relief, nerve-pain-cream, tingling-feet: "No discover page"; `discover migrastil-neuropathy-cream` (found by WebSearch): 15 videos -> discover/discover-migrastil-neuropathy-cream.json (discover.log).
- `tag --days 60` migrastil, neuropathy, neuropathycream, neuropathyrelief, nervepain, tinglingfeet: 0 videos each ("no such tag, nothing recent, or TikTok served a captcha"; tag.log), same as earlier jobs.
- `video` on 6 (videos/<id>/, videos.log). `viral --days 30 --category beauty --add-tags neuropathy,neuropathycream,neuropathyrelief,nervepain,footcare --discover .../migrastil-neuropathy-cream .../migrastil-neuropathy-cream-tiktok-shop`: hashtag pages 0, discover pages 16+16, 11 shop videos -> viral/viral-2026-11-06.json (viral.log).

## TikTok Shop
- "migrastil": the cream leads the shop at 109,295 sold, $32.49, 4.3, 7,075 reviews; 3-pack 441 sold ($70.20); cream + PainBlock roll-on bundle 789. Shop total 283.9K sold (listing).
- "neuropathy cream": Hrvsta "with Menthol" 7,953; Hrvsta Summervibes 3,109; Earth Essentials "High Menthol ... Camphor" 1,820; Raitera "Menthol" 1,741. Migrastil outsells all of them by 13x+, and it is the one without menthol.

## Videos watched (`video`, hook.png + sheet.png read)
| Video | Views | Len | What it does / what we take |
|---|---|---|---|
| @aunteeknows https://www.tiktok.com/@aunteeknows/video/7548818541793905950 | 1.3M | 57 s | Talking testimony, jar in hand at frame 0, text box "Living proof this cream WORKS! Neuropathy pain? Tingling? Burning?". Spoken hook: "this message is for chronic pain suffers if you suffer from neuropathy your feet your hands the constant burning and tingling". Winner line: "normally I'm up back and forth all night ... I slept like a baby". Take: the night/sleep angle and the "I tried every cream" story. Skip "living proof it works". |
| @jeff_el_colombiano https://www.tiktok.com/@jeff_el_colombiano/video/7503661052182236458 | 1.2M | 37 s | Spanish, in the car, reply to a comment, texture shown ("miren ustedes la textura"), "it absorbs super quickly with just a little bit". Take: texture close-up, comment-reply format. Skip "in thirty minutes or less" (not on listing). |
| @amazingaffiliate https://www.tiktok.com/@amazingaffiliate/video/7437977443283242286 | 1.2M | 57 s | POV legs and bare feet at frame 0, text "calling all diabetics with neuropathy pain". Lines: "no menthol or other irritating ingredient and it doesn't smell funky", "I put it on my feet especially at night ... sometimes I'll put socks on". Take: feet in frame at frame 0, bedtime + socks, no-menthol. Skip "gets to the root" and coupon urgency (comments mock it). |
| @spongebobprodsz https://www.tiktok.com/@spongebobprodsz/video/7605789234355571998 | 103.6K | 13 s | AI-looking stills of 2-4 jars in holiday rooms + "TRIPLE DISCOUNT ENDS TODAY" text, VO "last day". Shows a short no-person jar video can reach 100K. Skip the false-scarcity text. |
| @lylhealth https://www.tiktok.com/@lylhealth/video/7699489967113915662 | 28.3K (top of the 30-day viral board, 1.9K/day) | 14 s | Hands only: jar label to camera, back label, scoop, rub on the back of the hand, jar at end; music "Rock Road Rush" + short VO. Our model for the 12-15 s music cut. |
| @leslypocasangre https://www.tiktok.com/@leslypocasangre/video/7689983530222308638 | 25.3K | 11 s | Hands only, open jar at frame 0, swipe, rub on wrist, label to camera; "Epic Music" + Spanish VO "esa sensación como de toques eléctricos que no te dejan dormir en la noche ... Échate esta crema antes de dormir". |

## Viral board, last 30 days (viral/viral-2026-11-06.json)
11 shop videos, all for Migrastil, top: @lylhealth 1.9K views/day (14 s, hands only, music). Most recent posts are low (under 5K): the product is well known, so fresh-looking creative is the gap, not awareness.

## Lessons used
- Product or feet working in frame 0 (all three 1M+ winners).
- The night is the pain moment in every winner ("up all night", "no te dejan dormir en la noche").
- "No menthol / doesn't burn" is a named reason in the winner and the reason Migrastil differs from the competitors.
- Short winners are hands-only: scoop, rub in, label to camera, music.
- Hype and fake urgency get punished in the comments; we use none.
