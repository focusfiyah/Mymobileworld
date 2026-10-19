# Coach research (2026-10-16)
Commands: `tiktok.py shop "toddler bathtub"` (shop_toddler.txt), `shop "toddler bath tub"` (shop_run.txt, returned adult tubs), `shop "shnuggle"` (no results / captcha),
`tag toddlerbath`, `tag toddlerbathtub` (tag_run.txt, 163 + 172 videos), `viral` board (viral/), `video` on the top shop videos.
`tiktok.py video` returned "no video data" 4/4 this session (headless browser); a 1-request plain-HTTPS test of the same page worked, so
tools/tt_fetch.py pulled meta + video + TikTok captions + hook/sheet frames the same way (research/videos/<id>/).

## TikTok Shop listing (US)
ShnuggleUSA "Shnuggle Toddler Bath Tub 1-3 years + Grip Feet", 389 lifetime units, rating 5 (21), https://shop.tiktok.com/us/pdp/shnuggle-tub-contoured-base-foam-backrest/1731321029096214627
Category leaders by units: MoreFeel collapsible tub 11,040; MOREFEEL bath seat 6M+ 10,406; Jool Fold 'n Store 6,556; frida 4-in-1 Grow-With-Me 885.

## Top shop videos broken down (`video` equivalent)
| Video | Views / saves | Hook (first line) | Format | CTA |
|---|---|---|---|---|
| @silv_rlv MOREFEEL bath seat https://www.tiktok.com/@silv_rlv/video/7683209043116133662 | 914.9K / 3,630 | caption "we just switched to a bath seat and i can't believe how big my baby is getting" | 15s, baby in use at frame 0, milestone emotion, no VO | none spoken |
| @itskristaadams Jool tub https://www.tiktok.com/@itskristaadams/video/7683397629056699679 | 526K / 7,833 (1.5% saves) | "If you don't have a lot of room in your house and you've got a baby coming, you need to see this." | 34s, hands demo: opens, thermometer, drain, folds into cabinet | "I'm gonna leave this link down below" |
| @shewiththeglow (Grace) Shnuggle https://www.tiktok.com/@shewiththeglow/video/7692132082188946719 | 81K / 319 | "Never have I ever seen a true toddler size bathtub until now." | 37s, unbox + toddler in tub, features one by one (bump, foam backrest, non slip, plug) | "link below in the orange cart" |
| @momfindsbyjeni Shnuggle https://www.tiktok.com/@momfindsbyjeni/video/7611366378741845262 | 35.7K / 53 | "If you are looking for a toddler bath, you have found the perfect one." | 45s, toddler in tub on the sink, contour bump, depth, drain over the sink | "I'm linking it below" |

## Patterns that apply here
- Product in use at frame 0 and scale shown (tub vs child, tub on sink): our hook shots open on the tub itself, already in place, with a hand acting.
- Features named one by one with the part on screen (bump, backrest, drain): our feature line gets one shot per feature.
- Drain shown in action (Jool: "there is a drain, so I'm not trying to dump the entire bathtub"): plug-pull shot with water draining.
- The comments on Grace's video ARE the brief: "over priced" (top comment, 13 likes) and "this looks like just the right size for a toddler." Both videos are TikTok comment replies, so the comment bubble comes from TikTok's own reply feature when Grace posts, not from us.
