# Weekly content batch (Ralph's own: @azariah2244 / Instagram)
Audience (Ralph 2026-11-16, tapped "Sellers first, 70/30"): from week 2, about 70% of posts for TikTok Shop affiliates and online sellers (their problems, product videos), about 30% broader AI-for-creators tips that still lead to the AI Product Video Kit. Scripts start from the affiliate research (Dayone-ai research/audience-tiktok-affiliates-2026-11-16/REPORT.md).

Status: 2026-11-16: week 1 DONE. All 6 approved and in Drive "Content batch week 1 (2026-11-16)" https://drive.google.com/drive/folders/1BxC6wgvkfPysQbD2a9qims6aaa_nFTC8 : T1 + T2 twin (Flow Veo 3.1 Lite, ElevenLabs STS, cards, lo-fi music Mixkit 738 + whooshes), F1 + F2 faceless, C1 + C2 carousels. No singles (Ralph). Cost $0 + 80 Flow credits. Next: week 2 batch; posting only on his OK.

Ralph 2026-11-15: 2 AI twin videos a week, all 3 formats as one weekly batch, first batch mixes kit promos + AI tips. Twin style B (cinematic cards + pop-out words + subtitles) for combined and singles.

Steps per week (WEEK = folder, e.g. week1):
1. Write WEEK/scripts.json (twin shots with room query + angle; faceless lines with bg query + card; carousel slides). Humanizer voice, grade <= 6, no price, CTA "DM me KIT" for kit pieces.
2. `python3 checks.py scripts WEEK` -> SCRIPTS_OK (no 6-word run or close hook vs Grace's private material).
3. Twin: `python3 batch.py rooms WEEK` -> look at contact sheets, pick rooms with no people and no brand text (inpaint logos), write WEEK/rooms/picks.json -> `python3 batch.py kit WEEK` -> KITS_OK. Ralph makes the clips in Flow; then finish with ralph/twin-shorts (ElevenLabs STS to his clone, edit.py --plan, motion2 cards, ai_finish).
4. Faceless: `python3 batch.py bg WEEK` -> pick videos (WEEK/bg/picks.json, download) -> `faceless.py vo` (cbx venv) -> `faceless.py render` (musetalk venv) -> HOOK_OK + FACELESS_OK.
5. Carousels: `carousel.py WEEK` (musetalk venv) -> CAROUSELS_OK.
6. One review page per week; post only on Ralph's OK (TikTok via Zernio).
Media stays out of git (Drive via tools/media).

## Week 3 on: format change (Ralph 2026-11-22, tapped "Twin + you-decide stories", from the IG growth session session_01Y1Pt3p5PxcufXxpzcjg8Ee)
From week 3, the @realgoodhustles reels are AI-twin "you decide" stories. Each one shows a real money spot in an AI side hustle (mostly AI product videos for TikTok Shop) and asks "comment A or B". The next reel shows what happened and leads to the kit. Same audience and the same 70/30 sellers plan; only the format changes. Scripts: the daily task "RGH IG growth: daily" writes 3 every Monday in JOB/remakes/ (Dayone-ai products/ai-on-autopilot/research/ig-growth-2026-11-22/). Use those, or our own in the same format. Rule: Dayone-ai rules/rgh-posts.md. Why: choice stories got a median of 143 views and 20 s watch; twin tip reels got 4-21 views and about 2 s watch.
