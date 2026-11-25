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

## CORRECTION 2026-11-25 (main session, after Ralph questioned "no TikTok info")
The tag/viral/shop zeros above were a BLOCKED scraper, not empty pages (coach `tag babyclothes` re-run: still 0). camofox read the same #babygirlclothes page: 137 videos (research/coach/camofox/urls.txt + v/*/meta.json, stats via `tiktok.py video --no-media`, 134 fetched): 35 are shop videos. #babypajamas shows "Page not available" on TikTok itself. TikTok Shop search = puzzle captcha in camofox (exact listing still not found; ask Grace for the link).

Top shop videos on #babygirlclothes (views / saves / save% / length / posted):
| Video | Product | Views | Saves | Len | What it does |
|---|---|---|---|---|---|
| @madelyn_fitness 7705179545657281805 | Velvet Santa romper tutu dress | 2,600,000 | 19,088 (0.73%) | 14 s | Baby WEARING it, walking by the Christmas tree, music only, no talking, no text hook |
| @patriciamarie479 7702455763309956365 | "Made with love" bodysuit | 343,900 | 1,142 | 8 s | worn, funny print, music |
| @madelyn_fitness 7698928493400231182 | Toddler Baby Girl CHERRY BOW pajama set, pink gingham | 239,600 | 1,597 (0.67%) | 13 s | closest product to ours: baby wearing the cherry set on a white couch, sitting, waving, lying down; music only |
| @brooke_neil 7686471729371270430 | Leopard denim overalls | 207,400 | 2,279 (1.1%) | 9 s | worn |
| @mrs.kayrenee 7703302386244177182 / 7706248813362547998 | Newborn Christmas outfits | 112,800 / 106,900 | 1,419 / 1,123 (1.26% / 1.05%) | 12-14 s | worn, holiday occasion, "click the orange shopping bag" in caption |
| @chubbycheeksedits 7695841886182837534 | Girls 2-piece streetwear set | 103,900 | 185 | 15 s | all pieces shown, AI VO |
| @sodie.cakes 7697435412549225758 | 【Black Friday】3-Piece Baby Girls' Winter Outfit Set | 73,700 | 623 (0.85%) | 13 s | spoken: "Calling all girl mommies. Stop! What you doing? If you want your daughter to be standing out this winter, check this out. This is a three piece outfit. You will get the pants, the jacket, and the shirt. I'm gonna go ahead and leave a link..." |

What it changes:
1. Silent version (V1): the winners are 8-14 s, music only, product on the baby/in motion from frame 0. Grace's V1 (7-20 s, she adds music) matches; aim ~12-14 s.
2. Worn beats flat lay on views: if Grace has any shot of a baby wearing a piece, it opens both cuts. Ask her if she can film one (for next time if not in this upload).
3. VO script: the Black Friday set seller (73.7K) uses an identity call-out + "you will get the pants, the jacket and the shirt" (count what's in the set). Our script already counts ("With ten pieces"); added hook option (NEW, needs Ralph's OK): "Calling all baby girl moms, this one's ten pieces." The current script and its gate stay as they are.
