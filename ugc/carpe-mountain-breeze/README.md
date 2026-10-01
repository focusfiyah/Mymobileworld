# Carpe Mountain Breeze (v2): Grace on camera, tips ad

**Client: Grace** (Ralph, 2026-10-01). v2 of `../carpe-vanilla-peach/` (same research, facts and house rules; read
that README for why this format). Grace's changes: the Mountain Breeze product (`refs/mountain_breeze.jpg`, her
asset), a normal video of a person demonstrating every step instead of hands only, same Grace B voice.

Ralph's answers (2026-10-01): AI version of Grace from `refs/grace.jpg` with her real long almond French-tip nails;
bathroom setting; Grace B voiceover over her demo (no lip sync); keep both claims (front label "…for all-day fresh" + Target listing "100HR Sweat & Odor Control"; Ralph dropped
the word "wicking" 2026-10-01); name the scent and mention other scents, no smell claim.

Status: **new visual plan (Ralph 2026-10-01, over the same voiceover): V1 walking selfie (voiceover only), whip-pan →
S1 close-up clip (made), S2–S4 tips (stills made), V2 grey tee sweat stain + eye-roll, V4 tight cap-off/swipe b-roll,
V5 crisp dry grey tee tug, S10 CTA. S6–S9 stills unused (`preview/unused/`). Next: stills V1 V2 V4 V5 ($0.36) →
clips for every shot but S1 (37s, $1.52) → free cut with whip-pan. Spent $1.20 Kie (239 credits). Plan total ≈ $3.08.
Ask before every paid generation.**

## Script (times from `vo/stt.json`)

| Time | Shot | Grace B says | Visual |
|---|---|---|---|
| 0.00–4.70 | V1 | Okay, if you just bought Carpe, or you're about to, watch this first. | hook (walking selfie) |
| 4.70–5.85 | S1 | Okay, if you just bought Carpe, or you're about to, watch this first. | whip-pan → stick at the lens (clip already made) |
| 5.85–7.90 | S2 | When it's new, it looks empty. It's not. | it looks empty |
| 7.90–11.30 | S3 | Just keep twisting. It takes a bunch of turns the first time, | keep twisting |
| 11.30–14.80 | S4 | and you need way less than you think, like, a pea. | a pea |
| 14.80–18.60 | V2 | Too much is how you get that white crusty stuff people post about. | pit stain, eye-roll |
| 18.60–23.80 | V4 | Put it on dry skin at night, and let it dry before your shirt goes on. Then again in the morning. | tight b-roll: cap off + swipe |
| 23.80–31.00 | V5 | The label says all-day fresh, and it's clinically tested for up to a hundred hours, but that's when you use it like this. | crisp dry grey tee, tug |
| 31.00–35.00 | S10 | This one's Mountain Breeze. There are other scents too. It's linked below. | scent + CTA |

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
