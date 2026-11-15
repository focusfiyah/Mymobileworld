# Weekly content batch (Ralph's own: @azariah2244 / Instagram)

Status: 2026-11-15: week 1 built (2 twin Flow kits, 2 faceless videos, 2 carousels), review https://claude.ai/artifact/XzVZhtyLPHpXUafNt2VBdj ; waiting on Ralph's 8 Flow clips and his OK. $0.

Ralph 2026-11-15: 2 AI twin videos a week, all 3 formats as one weekly batch, first batch mixes kit promos + AI tips. Twin style B (cinematic cards + pop-out words + subtitles) for combined and singles.

Steps per week (WEEK = folder, e.g. week1):
1. Write WEEK/scripts.json (twin shots with room query + angle; faceless lines with bg query + card; carousel slides). Humanizer voice, grade <= 6, no price, CTA "DM me KIT" for kit pieces.
2. `python3 checks.py scripts WEEK` -> SCRIPTS_OK (no 6-word run or close hook vs Grace's private material).
3. Twin: `python3 batch.py rooms WEEK` -> look at contact sheets, pick rooms with no people and no brand text (inpaint logos), write WEEK/rooms/picks.json -> `python3 batch.py kit WEEK` -> KITS_OK. Ralph makes the clips in Flow; then finish with ralph/twin-shorts (ElevenLabs STS to his clone, edit.py --plan, motion2 cards, ai_finish).
4. Faceless: `python3 batch.py bg WEEK` -> pick videos (WEEK/bg/picks.json, download) -> `faceless.py vo` (cbx venv) -> `faceless.py render` (musetalk venv) -> HOOK_OK + FACELESS_OK.
5. Carousels: `carousel.py WEEK` (musetalk venv) -> CAROUSELS_OK.
6. One review page per week; post only on Ralph's OK (TikTok via Zernio).
Media stays out of git (Drive via tools/media).
