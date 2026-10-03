# Humanizer report: FUSOU V1-V6 final voiceovers, hooks and captions (2026-10-03)
Skill: .claude/skills/humanizer (blader/humanizer v3.1.0). Read as spoken UGC: short, concrete, casual.

| Video | Line | Tell | Change |
|---|---|---|---|
| V1 | "Heads up, it's almost six feet wide. Measure your wall first." | §4 staged run-up ("heads up") | "It's almost six feet wide, so measure your wall first." |
| V3 | "Five things, one order." | §2 slogan fragment | "That's five things in one order." |
| V6 | "Makeup on the sink, skincare on the dresser, perfume on the windowsill." then "Lipsticks go in the drawers... Perfume on the shelves. Hair tools plug in on the side." | §6 paired triads (weak here) | keep: the before/after IS the video and each sentence has its own shot |
| V1 | "Tap it once. Again. Now hold it." | §2 fragment row (weak: synced to the action) | keep (demo instruction); note: the clip shows one tap |
| all | hooks (18) and captions (6) | none found; caption emoji are TikTok convention | keep |
No dashes, no banned words (grace/gate.py scan), no "order it now".

## Re-check on the edited scripts.md (2026-10-03)
Re-read all 6 scripts after the two edits: no staged openers, slogans, contrasts, dashes or banned words left. New V1 line and new V3 line read naturally aloud.

## Re-run on the r2 script (2026-10-03, after Ralph removed "ships in three boxes" from all six)
Skill: .claude/skills/humanizer v3.1.0, read aloud as spoken UGC. Changed lines only plus the new joins.
| Video | Line now (spoken) | Tell | Decision |
|---|---|---|---|
| V1 | "If you want it up before the holidays, don't put it off. It's in the orange cart." | none (the stock closer "don't put it off" is Grace's usual, one use per video) | keep |
| V2 | "Holiday shipping gets slow, it's in the orange cart." | comma splice left by the cut; "holiday shipping gets slow" is a general claim nothing in the listing supports | FLAG to Ralph: replace with "If you want it up for the holidays, it's in the orange cart." (needs a re-voice, ElevenLabs credits, ask first) |
| V3 | "That's five things in one order. Don't put it off before the holidays. It's in the orange cart." | none | keep |
| V4 | "If you want it done before the holidays, don't put it off. It's in the orange cart." | none | keep |
| V5 | "Holiday get-ready season is close, it's in the orange cart." | comma splice left by the cut | FLAG: "Holiday get-ready season is close. It's in the orange cart." (re-voice, ask first) |
| V6 | "If someone in your house keeps asking for a vanity, it's in the orange cart." | none; reads as one sentence | keep |
No dashes, no banned phrases, no "order it now", no "three boxes" anywhere in the final voiceovers (checked `grep -i "boxes" vo/v*_final_words.json`: none).
