# Carpe Mountain Breeze (v2): Grace on camera, tips ad

**Client: Grace** (Ralph, 2026-10-01). v2 of `../carpe-vanilla-peach/` (same research, facts and house rules; read
that README for why this format). Grace's changes: the Mountain Breeze product (`refs/mountain_breeze.jpg`, her
asset), a normal video of a person demonstrating every step instead of hands only, same Grace B voice.

Ralph's answers (2026-10-01): AI version of Grace from `refs/grace.jpg` with her real long almond French-tip nails;
bathroom setting; Grace B voiceover over her demo (no lip sync); keep both claims (front label "…for all-day fresh" + Target listing "100HR Sweat & Odor Control"; Ralph dropped
the word "wicking" 2026-10-01); name the scent and mention other scents, no smell claim.

Status: **script v3 (Ralph 2026-10-01: curiosity hook → pain → solution → urgency CTA) recorded in Grace B, STT matches
word for word, pauses trimmed free → 35.0s (`vo/voiceover.mp3`; older takes kept: `voiceover_tips.mp3`, `voiceover_raw.mp3`).
Visuals: V1 walking selfie, V2 grey-tee sweat stain, whip-pan → S1 (made), S2–S4, V4 b-roll, V5 dry tee tug, S10.
Next: stills V1 V2 V4 V5 ($0.36) → clips for all but S1 (37s, $1.52) → free cut. Spent $1.20 Kie. Plan ≈ $3.08.
Ask before every paid generation.**

## Script (times from `vo/stt.json`)

| Time | Shot | Grace B says | Beat |
|---|---|---|---|
| 0.00–4.13 | V1 | You're probably putting your deodorant on at the wrong time. Here's why. | hook (curiosity loop) |
| 4.13–9.96 | V2 | Pit stains by lunch. Changing your shirt before a meeting. Keeping your arms down in every photo. | pain |
| 9.96–16.16 | S1 | This is Carpe, in Mountain Breeze. It's clinically tested for up to a hundred hours of sweat and odor control, | solution: product + claim (whip-pan in; clip made, slowed to fit) |
| 16.16–19.80 | S2 | but only if you use it right. When it's new, it looks empty, | caveat + looks empty |
| 19.80–21.23 | S3 | so just keep twisting. | keep twisting |
| 21.23–22.73 | S4 | You only need a pea. | a pea |
| 22.73–27.07 | V4 | Put it on at night, on dry skin, let it dry, then again in the morning. | how: night, dry skin (closes the hook) |
| 27.07–31.09 | V5 | Night is the step people miss. If sweat's never bothered you, scroll on. | result + detached CTA start |
| 31.09–35.03 | S10 | If it has, don't wait till holiday party photos. It's linked below. | urgency CTA |

Label text is garbled by the image model at small sizes: for the badge and the Mountain Breeze panel, cut in a
close-up of the real product photo (`refs/mb_front.png`) in `cut.py` (free), like v1's badge insert.

## Cost plan

| Step | Cost |
|---|---|
| Voiceover (610 chars + 120-char line fix, Grace B, eleven_v4) + STT checks | ElevenLabs credits |
| S1 + S1a stills | $0.18 (done) |
| S2–S10 stills | $0.81 |
| 10 clips, Seedance 2.0 Mini, 46s total | $1.89 |
| Cut (`python3 cut.py`, after adapting to 10 shots + label inserts) | free |
| **Total** | **≈ $2.88** + ~$0.25 per redone shot |
