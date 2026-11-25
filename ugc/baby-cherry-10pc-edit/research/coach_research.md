# Coach research (tiktok-shop-coach, run 2026-11-25 in this session)

Output files: research/coach/ (shop-*.json, viral-2026-11-25.json, viral_run.log, videos/<id>/meta.json + transcript + hook.png + sheet.png). Media files (video.mp4) stay out of git.

## What ran and what came back (test outputs, not assumptions)
- `shop "baby clothes"` and `shop "baby pajamas"`: OK, 20 products each (shop-baby-clothes.json, shop-baby-pajamas.json). Closest to ours: SoftHug Kids "6-Piece Baby Girl Spring Fall Set, Long Sleeve Pants" (644 lifetime sold, 4.8 stars, 58 reviews) and "6-Piece Baby Girl Set, Heart Striped ... Cozy Pajamas" (190 sold, 4.3); JY.COZY 10 Pack onesie set (208 sold, 5.0); POSHTO bamboo pajamas (686 sold, 4.8). Multi-piece baby sets sell in the hundreds, not tens of thousands: a mid-size niche.
- `shop` on "baby girl clothes set", "10 piece baby girl set", "baby girl cherry set", "baby girl floral set", "baby girl pajamas set": "No products returned ... (no results, or TikTok served a captcha)". Exact listing NOT found.
- WebSearch for the exact title ("10-Piece Baby Girl Floral Cherry Print Long Sleeve Set" tiktok shop): no TikTok Shop page found (Walmart/buybuy BABY only, different products). So product facts = listing title only.
- `tag babygirlclothes / babyclothes / babypajamas --days 60`: "kept 0 of 0 videos ... No videos returned" for all three.
- `viral --days 30 --category fashion --add-tags babyclothes,babygirlclothes,babypajamas,babyclothesfinds,toddlerclothes`: every hashtag page returned 0 videos ("0 videos scanned"), see viral_run.log. Hashtag pages were empty this session.
- Discover pages: curl to tiktok.com/discover/baby-girl-clothes-set (and 4 other slugs) = 301 to the home page (no such page); WebSearch `site:tiktok.com/discover baby girl clothes set` found none.
- Fallback that worked: baby/toddler clothing SHOP videos already ranked on earlier viral boards in this repo (ugc/*/research/viral/viral-2026-10-*.json, coach output from 2026-10-07 to 2026-10-21), re-fetched today with `video` (fresh stats below).

## `video` on the top shop videos (fresh stats 2026-11-25)
| Video | Product | Views | Saves | Length | Hook (0-3 s) | Format | CTA |
|---|---|---|---|---|---|---|---|
| @oneclassybitchh 7698948291261697310 | Baby girl long-sleeve pumpkin flower footie romper | 7,915 | 8 | 13 s | Product laid flat on a table at frame 0, hand lifts the ruffle; spoken "I'm putting this in my niece's boo basket" (occasion + who it's for) | hands-only, flat lay, one take, voice over | none spoken (shop link) |
| @chubbycheeksedits 7688739264028347678 | Toddler girl 2-piece sweatsuit (3 prints) | 5,284 | 14 (best save rate, 0.26%) | 15 s | All three sets on screen at once, text "Cute outfits for every little moment"; spoken "why are all three of these so cute?" | AI faceless VO, all looks shown together, one use per look ("for playdates", "every day", "fun days") | "Tap the orange cart and pick your favorite." |
| @kadfinds 7699075511162522911 | Kids bamboo pajama set "Soft Breathable Stretchy" | 985 | 0 | 14 s | Pajama top held up to camera at frame 0, text "so many cute prints"; spoken occasion call-out ("Christmas is gonna be extra cute this year") | talking head holding the set | "snag them down below" + price talk (we never say price) |
| @j0rdan_jdr 7697354843316342047 | Toddler corduroy overalls romper | 2,733 | 3 | 20 s | Toddler walking in the outfit at a pumpkin patch, text "Fall outfit for son"; no captions | in-use, music only | none |
| @itstay.alyssa 7692178245868965134 | Baby girl 2-piece ruffle set | 985 | 1 | 102 s | Talking haul, long and slow | haul | "linked on the screen" |

## Patterns to copy (format, never words)
1. Product on screen at frame 0, laid flat or held up, hands touching it (all top 3). Our hook shot: her hands lay out / fan out all 10 pieces.
2. Short: 13-15 s for the three best; our script runs ~19-21 s.
3. Each look/feature gets a use ("for playdates", "for every day"): matches Grace's "features tied to use".
4. Show the whole set together once (chubbycheeks: all three outfits at once got the best save rate).
5. Tactile proof: hand squeezes/lifts the fabric (oneclassybitchh), "so soft, super stretchy" said over a stretch (kadfinds).
6. Occasion close (boo basket, Christmas): ours = holidays + Black Friday (real date).
7. What we drop: price talk (kadfinds), "so cute"/"obsessed" words (banned for Grace), long haul format.
