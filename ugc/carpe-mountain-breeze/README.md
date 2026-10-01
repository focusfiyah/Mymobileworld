# Carpe Mountain Breeze (v2): Grace on camera, tips ad

**Client: Grace** (Ralph, 2026-10-01). v2 of `../carpe-vanilla-peach/` (same research, facts and house rules; read
that README for why this format). Grace's changes: the Mountain Breeze product (`refs/mountain_breeze.jpg`, her
asset), a normal video of a person demonstrating every step instead of hands only, same Grace B voice.

Ralph's answers (2026-10-01): AI version of Grace from `refs/grace.jpg` with her real long almond French-tip nails;
bathroom setting; Grace B voiceover over her demo (no lip sync); keep both claims (front label "…for all-day fresh" + Target listing "100HR Sweat & Odor Control"; Ralph dropped
the word "wicking" 2026-10-01); name the scent and mention other scents, no smell claim.

Status: **voiceover v2 done (34.8s): Ralph's notes 2026-10-01 → only the label line re-recorded and spliced in
("The label says all-day fresh…", "wicking" dropped; old take kept as `vo/voiceover_wicking.mp3`). S1 is now a
close-up of the stick that pulls back to Grace (S1a still = first frame, S1 still = last frame, Seedance
`last_frame_url`); S1a's background blur and crop were done free in PIL (`preview/S1a_raw.png` = the raw still).
S1 clip done ($0.21): continuous move from the close-up down to chest height, background comes into focus
(`preview/S1_with_vo.mp4`). Stills S2–S10 done ($0.81, `preview/stills_sheet.png`); notes: S3 starts with a little cream already
showing, S6/S8 look alike (fix free in the cut: warm/dim night grade on S6, bright morning grade on S8).
Next: Ralph OKs stills → clips S2–S10 ($1.68) → free cut. Spent $1.20 Kie (239 credits) + ~730 ElevenLabs characters. Plan total ≈ $2.88 Kie. Ask before every paid generation.**

## Script (times from `vo/stt.json`)

| Time | Shot | Grace B says | Grace does |
|---|---|---|---|
| 0.0–4.7 | S1 | Okay, if you just bought Carpe, or you're about to, watch this first. | one continuous natural handheld move. It opens on the Mountain Breeze stick held very close to the lens, sharp, with her face and the bathroom soft and blurred behind it. The camera eases back smoothly, like someone stepping back with a phone, while focus shifts from the stick to her face, ending on her holding the stick at chest height with her eyebrows raised, exactly as in the last frame. Slight real handheld sway, no zoom pump, no cuts. |
| 4.7–7.9 | S2 | When it's new, it looks empty. It's not. | she tilts the open stick toward the lens to show the empty slots, gives a small shrug, then turns it back upright. |
| 7.9–11.3 | S3 | Just keep twisting. It takes a bunch of turns the first time, | her fingers turn the knob again and again, five quick turns; on the last turns small ribbons of white cream rise up through the slots. |
| 11.3–14.8 | S4 | and you need way less than you think, like, a pea. | her fingertip points at the small amount of cream, circles it once in the air, then she pulls the stick back a little. |
| 14.8–18.6 | S5 | Too much is how you get that white crusty stuff people post about. | she wipes the extra cream off the slotted top with the tissue in one stroke, leaving only a little in the slots. |
| 18.6–20.3 | S6 | Put it on dry skin at night, | she pats her underarm dry with the towel once, then glides the stick up and down twice, a light thin layer, and lowers her arm. |
| 20.3–22.4 | S7 | and let it dry before your shirt goes on, | she waits a beat, arms slightly out, with a little impatient look. Shot 2 (2-4s): she pulls the black t-shirt on over her head. |
| 22.4–23.8 | S8 | then again in the morning. | she glides the stick under her arm once, a quick light swipe, then lowers her arm and caps it. |
| 23.8–31.0 | S9 | The label says all-day fresh, and it's clinically tested for up to a hundred hours, but that's when you use it like this. | her fingernail taps the round badge once and she holds it steady. Shot 2 (4-8s): she tips the stick side to side a little, a casual 'eh, use it right' gesture with a small head tilt, then holds it still. |
| 31.0–35.0 | S10 | This one's Mountain Breeze. There are other scents too. It's linked below. | she holds the Mountain Breeze label to the lens and gives a small smile. Shot 2 (3-5s): she lowers the stick and points down toward the bottom of the frame, then holds. |

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
