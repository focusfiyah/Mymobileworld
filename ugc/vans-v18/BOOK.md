# Production Book: Vans sequin V18-V37, 20 music-only videos (Grace), 2026-11-11

Sent to Ralph: https://claude.ai/artifact/Hvvw2NxP4JCwL7bVLFidvT, 2026-11-11

## 1. Job
- Client: Grace  Product: Vans Premium Authentic low top, sequin checkerboard (same shoe as V1-V17)  Route: hands + feet AI from stills (Gemini 3 Pro Image on Kie) + Seedance 2.0 Mini first-frame clips on Kie (Ralph tapped "Seedance Mini, ~$30.50 (Recommended)" 2026-11-11, as V13-V17), `.claude/skills/ugc-product-ad`
- Job folder: `ugc/vans-v18/`  Length: 16 s each  Shots: 5 per video (3.2 s), 100 in all (50 hand-free)
- Ask (Ralph 2026-11-11): about 20 videos of the Vans, 3 from each of the 6 links Grace sent, matching the scenes; made on Kie; 16 s. Answers he tapped: sequin shoe, 20 videos (18 + 2 that mix the best beats), music only, same beats new look, Kie for all and OK over the cap, free music he can swap in TikTok. Hypit: breakdown only (Ralph tapped "Breakdown only, Kie makes it").
- Links: 1 https://www.tiktok.com/t/ZPLnjUU3p/ (V18-V20) · 2 https://www.tiktok.com/t/ZPLnjhxGh/ (V21-V23) · 3 https://www.tiktok.com/t/ZPLnj2pMc/ (V24-V26) · 4 https://www.tiktok.com/t/ZPLnjFctx/ (V27-V29) · 5 https://www.tiktok.com/t/ZPLnjkDyF/ (V30-V32) · 6 https://www.tiktok.com/t/ZPLn2wKg5/ (V33-V35) · mixes V36 (Links 6+5+3), V37 (Links 2+4+1)

## 2. Gate result (`python3 grace/gate.py ugc/vans-v18`): GATE OK
| Proof | File | Result |
|---|---|---|
| Playbook rules read | proof/playbook.md | OK |
| Coach research (ref video x6 + tag) | proof/coach_research.md | OK: top ref 367.8K views (Link 6); today's tag/viral pages returned 0 (TikTok captcha), Oct 29 tag data stands |
| Daily viral board | research/coach/viral-2026-11-11.json | ran today, 0 videos returned (captcha) |
| Product facts (source) | research/product_facts.md + product_truth.json | OK (Vans' real photos) |
| Hooks modeled on named winners | research/hooks.md | 20 different Grace library hooks, word for word |
| Humanizer | proof/humanizer.md | OK, 3 captions reworded |
| Readability (grade) | proof/readability.txt | 1.8 |
| Banned-phrase check | gate.py | OK |

## 3. Script
Music only: no voice, no on-screen text (Ralph 2026-11-11; Creator Pathway decision 4). The words are the TikTok post captions:
- V18: Link 1 | cafe sidewalk | caption: This looks completely different once you actually see it on. Only the black squares have sequins, so they shine without being too much. It's in the orange cart.
- V19: Link 1 | cafe sidewalk | caption: I needed to know how this looked from the side. Same classic Vans shape, just with sequins on the black squares. It's in the orange cart.
- V20: Link 1 | cafe sidewalk | caption: This is the part I wanted to see before I bought it. Red insole with the white Vans box inside. It's in the orange cart.
- V21: Link 2 | Grace's saved cream bedroom | caption: I keep reaching for this more than I expected. They go with my comfy clothes and my going out clothes. It's in the orange cart.
- V22: Link 2 | Grace's saved cream bedroom | caption: This just makes everything feel a little more put together. Sweats and sequin Vans, done. It's in the orange cart.
- V23: Link 2 | Grace's saved cream bedroom | caption: I was not expecting to care this much about a pair of Vans. The sequins catch the light every time I move. It's in the orange cart.
- V24: Link 3 | car interior (cream seats) | caption: Before you buy this, look at the sequins up close. Raised black sequins on the black squares, plain canvas on the white. It's in the orange cart.
- V25: Link 3 | car interior (cream seats) | caption: Okay, but what does the back actually look like? Black heel stripe and the Off The Wall label, same as the classic. It's in the orange cart.
- V26: Link 3 | car interior (cream seats) | caption: The listing did not really show me this part. Up close, the sequins are on the black squares only. It's in the orange cart.
- V27: Link 4 | bright living room, coffee table | caption: This is one of those details you do not notice until you use it. The red insole shows every time I slip them on. It's in the orange cart.
- V28: Link 4 | bright living room, coffee table | caption: This is the part I actually care about. Sequins on the classic Vans shape I already love. It's in the orange cart.
- V29: Link 4 | bright living room, coffee table | caption: I am very particular about my sneakers. These are the classic Authentic with sequins on the black squares. It's in the orange cart.
- V30: Link 5 | car door open onto the cafe sidewalk | caption: Here is what I would want someone to show me before I ordered this. The pair side by side, inside and out. It's in the orange cart.
- V31: Link 5 | car door open onto the cafe sidewalk | caption: The thing that sold me was not even the obvious feature. It was the red insole with the white Vans box. It's in the orange cart.
- V32: Link 5 | car door open onto the cafe sidewalk | caption: Apparently I have very strong opinions about sparkly sneakers. These have just the right amount. It's in the orange cart.
- V33: Link 6 | car door open onto the cafe sidewalk | caption: This is one of those things I keep reaching for without thinking about it. I wear them with jeans and with sweats. It's in the orange cart.
- V34: Link 6 | car door open onto the cafe sidewalk | caption: This is the thing I grab when I want my outfit to look done. I put these on and I'm out the door. It's in the orange cart.
- V35: Link 6 | car door open onto the cafe sidewalk | caption: I know this is minor, but I really do care about the bottom of my shoes. Gum waffle sole, just like the classic. It's in the orange cart.
- V36: Link 3, Link 5, Link 6 | car door open onto the cafe sidewalk | caption: I save this specifically for days I want a little sparkle. Lately that is most days. It's in the orange cart.
- V37: Link 1, Link 2, Link 4 | Grace's saved cream bedroom | caption: Here is the part that made me stop scrolling. Sequins on the black squares only, so they still look like Vans. It's in the orange cart.
Source of each line: research/line_sources.md (library hook id + product_truth fact). Music: a free licensed track per video (free-assets: Mixkit/Pixabay), each video its own track; Grace can swap in a trending sound in TikTok.

## 4. Shot list
| # | Window (s) | Shot | Kind | Setting | On screen | Face? | VO or lip sync |
|---|---|---|---|---|---|---|---|
| V18S1 | 0.0-3.2 | hand lifts the held shoe over her legs, side tab (beat 1a) | HAND | cafe sidewalk | none | no face | music only |
| V18S2 | 3.2-6.4 | held shoe top view, laces (beat 1b) | HAND | cafe sidewalk | none | no face | music only |
| V18S3 | 6.4-9.6 | feet crossed on the ground, foot bounce (beat 1d) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V18S4 | 9.6-12.8 | held shoe tilted, red insole (beat 1c) | HAND | cafe sidewalk | none | no face | music only |
| V18S5 | 12.8-16.0 | one shoe on the ground, push-in (beat 1e) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V19S1 | 0.0-3.2 | feet crossed on the ground, foot bounce (beat 1d) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V19S2 | 3.2-6.4 | held shoe tilted, red insole (beat 1c) | HAND | cafe sidewalk | none | no face | music only |
| V19S3 | 6.4-9.6 | hand lifts the held shoe over her legs, side tab (beat 1a) | HAND | cafe sidewalk | none | no face | music only |
| V19S4 | 9.6-12.8 | one shoe on the ground, push-in (beat 1e) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V19S5 | 12.8-16.0 | held shoe top view, laces (beat 1b) | HAND | cafe sidewalk | none | no face | music only |
| V20S1 | 0.0-3.2 | one shoe on the ground, push-in (beat 1e) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V20S2 | 3.2-6.4 | hand lifts the held shoe over her legs, side tab (beat 1a) | HAND | cafe sidewalk | none | no face | music only |
| V20S3 | 6.4-9.6 | held shoe tilted, red insole (beat 1c) | HAND | cafe sidewalk | none | no face | music only |
| V20S4 | 9.6-12.8 | held shoe top view, laces (beat 1b) | HAND | cafe sidewalk | none | no face | music only |
| V20S5 | 12.8-16.0 | feet crossed on the ground, foot bounce (beat 1d) | HAND-FREE | cafe sidewalk | none | no face | music only |
| V21S1 | 0.0-3.2 | finger taps the side tab on her worn shoe (beat 2a) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V21S2 | 3.2-6.4 | heel lift shows the gum sole (beat 2b) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V21S3 | 6.4-9.6 | hand pulls the worn shoe's bow tight (beat 2d) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V21S4 | 9.6-12.8 | seated wide, toes tap together (beat 2c) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V21S5 | 12.8-16.0 | the pair side by side, dolly in (beat 2e) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V22S1 | 0.0-3.2 | seated wide, toes tap together (beat 2c) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V22S2 | 3.2-6.4 | finger taps the side tab on her worn shoe (beat 2a) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V22S3 | 6.4-9.6 | the pair side by side, dolly in (beat 2e) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V22S4 | 9.6-12.8 | heel lift shows the gum sole (beat 2b) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V22S5 | 12.8-16.0 | hand pulls the worn shoe's bow tight (beat 2d) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V23S1 | 0.0-3.2 | the pair side by side, dolly in (beat 2e) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V23S2 | 3.2-6.4 | hand pulls the worn shoe's bow tight (beat 2d) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V23S3 | 6.4-9.6 | finger taps the side tab on her worn shoe (beat 2a) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V23S4 | 9.6-12.8 | seated wide, toes tap together (beat 2c) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V23S5 | 12.8-16.0 | heel lift shows the gum sole (beat 2b) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V24S1 | 0.0-3.2 | held shoe in front of the dash, side tab (beat 3a) | HAND | car interior (cream seats) | none | no face | music only |
| V24S2 | 3.2-6.4 | held shoe toe at the lens (beat 3b) | HAND | car interior (cream seats) | none | no face | music only |
| V24S3 | 6.4-9.6 | held shoe back view, heel label (beat 3c) | HAND | car interior (cream seats) | none | no face | music only |
| V24S4 | 9.6-12.8 | feet up on the dash, crossed, sway (beat 3d) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V24S5 | 12.8-16.0 | one shoe on the cream seat, push-in (beat 3e) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V25S1 | 0.0-3.2 | feet up on the dash, crossed, sway (beat 3d) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V25S2 | 3.2-6.4 | held shoe in front of the dash, side tab (beat 3a) | HAND | car interior (cream seats) | none | no face | music only |
| V25S3 | 6.4-9.6 | one shoe on the cream seat, push-in (beat 3e) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V25S4 | 9.6-12.8 | held shoe back view, heel label (beat 3c) | HAND | car interior (cream seats) | none | no face | music only |
| V25S5 | 12.8-16.0 | held shoe toe at the lens (beat 3b) | HAND | car interior (cream seats) | none | no face | music only |
| V26S1 | 0.0-3.2 | one shoe on the cream seat, push-in (beat 3e) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V26S2 | 3.2-6.4 | held shoe back view, heel label (beat 3c) | HAND | car interior (cream seats) | none | no face | music only |
| V26S3 | 6.4-9.6 | held shoe toe at the lens (beat 3b) | HAND | car interior (cream seats) | none | no face | music only |
| V26S4 | 9.6-12.8 | held shoe in front of the dash, side tab (beat 3a) | HAND | car interior (cream seats) | none | no face | music only |
| V26S5 | 12.8-16.0 | feet up on the dash, crossed, sway (beat 3d) | HAND-FREE | car interior (cream seats) | none | no face | music only |
| V27S1 | 0.0-3.2 | sequin macro slide (beat 4b) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V27S2 | 3.2-6.4 | held shoe over the coffee table, side tab (beat 4a) | HAND | bright living room, coffee table | none | no face | music only |
| V27S3 | 6.4-9.6 | held shoe tilted, red insole (beat 4c) | HAND | bright living room, coffee table | none | no face | music only |
| V27S4 | 9.6-12.8 | one shoe on the table by the mug, push-in (beat 4d) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V27S5 | 12.8-16.0 | feet by the table, ankle cross (beat 4e) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V28S1 | 0.0-3.2 | held shoe over the coffee table, side tab (beat 4a) | HAND | bright living room, coffee table | none | no face | music only |
| V28S2 | 3.2-6.4 | one shoe on the table by the mug, push-in (beat 4d) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V28S3 | 6.4-9.6 | sequin macro slide (beat 4b) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V28S4 | 9.6-12.8 | feet by the table, ankle cross (beat 4e) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V28S5 | 12.8-16.0 | held shoe tilted, red insole (beat 4c) | HAND | bright living room, coffee table | none | no face | music only |
| V29S1 | 0.0-3.2 | feet by the table, ankle cross (beat 4e) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V29S2 | 3.2-6.4 | held shoe tilted, red insole (beat 4c) | HAND | bright living room, coffee table | none | no face | music only |
| V29S3 | 6.4-9.6 | one shoe on the table by the mug, push-in (beat 4d) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V29S4 | 9.6-12.8 | sequin macro slide (beat 4b) | HAND-FREE | bright living room, coffee table | none | no face | music only |
| V29S5 | 12.8-16.0 | held shoe over the coffee table, side tab (beat 4a) | HAND | bright living room, coffee table | none | no face | music only |
| V30S1 | 0.0-3.2 | held shoe beside her worn foot on the door sill (beat 5a) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V30S2 | 3.2-6.4 | held shoe insole over the sill (beat 5b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V30S3 | 6.4-9.6 | held shoe top view over her foot (beat 5c) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V30S4 | 9.6-12.8 | both feet on the sill, toe tap (beat 5d) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V30S5 | 12.8-16.0 | she steps out onto the sidewalk (beat 5e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V31S1 | 0.0-3.2 | both feet on the sill, toe tap (beat 5d) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V31S2 | 3.2-6.4 | held shoe beside her worn foot on the door sill (beat 5a) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V31S3 | 6.4-9.6 | she steps out onto the sidewalk (beat 5e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V31S4 | 9.6-12.8 | held shoe top view over her foot (beat 5c) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V31S5 | 12.8-16.0 | held shoe insole over the sill (beat 5b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V32S1 | 0.0-3.2 | held shoe top view over her foot (beat 5c) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V32S2 | 3.2-6.4 | she steps out onto the sidewalk (beat 5e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V32S3 | 6.4-9.6 | held shoe insole over the sill (beat 5b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V32S4 | 9.6-12.8 | held shoe beside her worn foot on the door sill (beat 5a) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V32S5 | 12.8-16.0 | both feet on the sill, toe tap (beat 5d) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V33S1 | 0.0-3.2 | legs swing out of the car, feet land (beat 6a) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V33S2 | 3.2-6.4 | held shoe against the door panel (beat 6b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V33S3 | 6.4-9.6 | walks toward the camera (beat 6c) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V33S4 | 9.6-12.8 | held shoe sole to the lens, gum waffle (beat 6d) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V33S5 | 12.8-16.0 | standing by the car, heel lift (beat 6e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V34S1 | 0.0-3.2 | walks toward the camera (beat 6c) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V34S2 | 3.2-6.4 | legs swing out of the car, feet land (beat 6a) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V34S3 | 6.4-9.6 | standing by the car, heel lift (beat 6e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V34S4 | 9.6-12.8 | held shoe against the door panel (beat 6b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V34S5 | 12.8-16.0 | held shoe sole to the lens, gum waffle (beat 6d) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V35S1 | 0.0-3.2 | held shoe against the door panel (beat 6b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V35S2 | 3.2-6.4 | standing by the car, heel lift (beat 6e) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V35S3 | 6.4-9.6 | legs swing out of the car, feet land (beat 6a) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V35S4 | 9.6-12.8 | held shoe sole to the lens, gum waffle (beat 6d) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V35S5 | 12.8-16.0 | walks toward the camera (beat 6c) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V36S1 | 0.0-3.2 | legs swing out of the car, feet land (beat 6a) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V36S2 | 3.2-6.4 | held shoe beside her worn foot on the door sill (beat 5a) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V36S3 | 6.4-9.6 | held shoe toe at the lens (beat 3b) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V36S4 | 9.6-12.8 | walks toward the camera (beat 6c) | HAND-FREE | car door open onto the cafe sidewalk | none | no face | music only |
| V36S5 | 12.8-16.0 | held shoe sole to the lens, gum waffle (beat 6d) | HAND | car door open onto the cafe sidewalk | none | no face | music only |
| V37S1 | 0.0-3.2 | finger taps the side tab on her worn shoe (beat 2a) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V37S2 | 3.2-6.4 | sequin macro slide (beat 4b) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V37S3 | 6.4-9.6 | held shoe tilted, red insole (beat 1c) | HAND | Grace's saved cream bedroom | none | no face | music only |
| V37S4 | 9.6-12.8 | the pair side by side, dolly in (beat 2e) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
| V37S5 | 12.8-16.0 | seated wide, toes tap together (beat 2c) | HAND-FREE | Grace's saved cream bedroom | none | no face | music only |
Outfit: its own per video (tools/make_shots.py OUT, 10 looks rotating, never the same look twice in a link's 3 videos)  Setting: one per video (Grace's one-room rule; saved bedroom reused; car, sidewalk and living room picked today from free real photos, rooms/SOURCES.md)  Nails / person details: GRACE'S REAL COMPLEXION on every hand, ankle and leg (Ralph 2026-11-11: "make sure it's Grace's complexion that's being used"): refs are frames of her own Vans post (@shewiththeglow 7699252578239925535): refs/grace/f_11.5.jpg (her hand: medium-deep brown, pink French tips, blue band, heart ring, gold link bracelet) and refs/grace/f_23.5.jpg (her ankles, gold anklet); the older AI hand image is no longer used  Real product confirmed: same shoe as V1-V17, product_truth.json (black side tab with white VANS, red insole with white box, checkerboard toe, gum sole)

## 5. Order of work
1. All 100 stills at once (parallel, $9.00), QC at 2x (Grace's complexion on every hand and ankle, side tab, toe, which shoe), storyboard of all 20 videos on the review page. STOP for your look.
2. Example videos, one per link (Ralph 2026-11-11: "give me an example of one video from each link"): V18 (Link 1), V21 (Link 2), V24 (Link 3), V27 (Link 4), V30 (Link 5), V33 (Link 6). ONE test clip first, the riskiest: V30S1 (held shoe beside the worn one in the car door). Then the other 29 example clips ($4.92 for all 30), cut, QC, AI finish, on the review page. STOP for your look.
3. Only after your OK on the examples: the other 14 videos (70 clips, $11.48), cuts, QC, review page.
Free fixes planned: trim each clip to the cleanest 3.2 s window, crop, grade per video (bright neutral), mirror where a frame needs the other side.
Time: stills ~15 min, test clip ~5 min, clips ~20 min, cuts + QC ~40 min (machine time, plus your review stops).

## 6. Cost (one total)
| Item | Qty x unit | $ |
|---|---|---|
| Stills, Gemini 3 Pro Image (nano-banana-pro 1K) | 100 x $0.09 | 9.00 |
| Clips, Seedance 2.0 Mini 4 s 720p first-frame | 100 x $0.164 | 16.40 |
| Redo allowance (hard cap: the job never passes $30.00), each redo asked first with its cost | about 18 stills or 28 clips | 4.60 |
| Music (free licensed tracks) | 20 x $0 | 0.00 |
Total Kie: $30.00  ElevenLabs: 0 chars  Contingency redos: inside the total, each one still asked with its cost
Month so far (`python3 grace/spend.py`): $39.90 of the $100 cap; this job takes it to about $69.90 (you OK'd going over; it stays under)

TOTAL: $30.00

**Approve?**

## 7. Questions (all of them, now)
1. Answered 2026-11-11: budget $25 min, $30 max; storyboard for all; one example video per link before the rest; Grace's complexion.

## 8. Prompts (final, written with prompt-master; every reference named)
| Item | Model | Prompt file / text |
|---|---|---|
| 100 stills | nano-banana-pro | shots.json "still" + "still_refs" (tools/make_shots.py) |
| 100 clips | bytedance/seedance-2-mini first-frame | prompts/<ID>_sd.txt |
Lint: `python3 grace/prompt_check.py lint ugc/vans-v18/shots.json` = PROMPT_LINT_OK; every prompt read end to end (2 clashes fixed: clip look lines now name only the logos in frame; no "same grip" on the finger-tap shot).
