# Grace's voice (ElevenLabs, Starter plan = instant clones only; professional clone not allowed, tested 2026-10-18)

**Status 2026-10-20 round 2, WAITING ON GRACE'S PICK:** Grace says the voice below sounds too American (she is Haitian; old C
didn't have her accent either). Accent clone "Grace accent test" `Rh3oAQMqRVf78UIVpBoQ` = Ralph's 2026-10-19 video of Grace +
the 10 TikToks that sound most like it (accent_rank.json). Tests C (eleven_v4) / E (eleven_multilingual_v2) are on the review
page. Lesson: picking clone audio for low echo alone gave clips far from her natural voice (0.807 vs 0.93+ closeness); rank by
closeness to a known-good sample of her real accent first, then by echo. On the pick: it becomes "Grace", the others get deleted.

**"Grace" `gjmt5xZqVE6mjSY4NfQM` is Grace's ONE voice for now** (Ralph 2026-10-20: "Keep"; grace.json). Use it for every Grace
voiceover and skit line. Settings: eleven_v4, stability 0.4, similarity 0.8, style 0. Level every voiceover to -16 LUFS
(`loudnorm=I=-16:TP=-1.5`) before the cut and in any preview.

## How it was made (2026-10-20)
- Source: Grace's own TikToks on @shewiththeglow (display name GraceWithTheGlow). Only videos posted before 2026-09-25,
  because our AI voiceovers on her account start 2026-10-01 and must never feed the clone.
- `pick.py <dir>` ranked all 1,109 of them: driest first (`echo.py`), with quiet gaps between words (no music bed).
  7 clips where she talks to camera were kept (sources.json), each speaker-checked with resemblyzer against her other
  on-camera clips (>= 0.87; a different woman scored 0.846, so it is a rough filter, the on-camera check matters).
- Trimmed to 172 s of speech (silenceremove), levelled to -18 LUFS, uploaded as an instant clone (no character cost).
- Result on the same line: echo at pauses 52 ms vs 110 ms for the old Grace C (`echo.py`, lower = drier).
  A/B: `grace_voice_AB_2026-10-20.mp3` (real Grace, old C, new). Review page https://claude.ai/artifact/ERywTwEf9dwoxqgtH8jqyH.
- Gates: GATES.md (`check.py sources|train|clone|account|refs`).

## To rebuild it
Re-download with `yt-dlp --impersonate chrome` (needs `pip install curl_cffi`), run `pick.py`, look at the frames, keep
clips where Grace talks to camera, trim, clone, then A/B against the current voice before swapping ids. Ask Ralph first;
delete the old voice only on his OK.

## Retired (deleted from ElevenLabs 2026-10-20)
- Grace C `P8OUGBCvq8OBS4xlb65A`: cloned from her Wag Bag takes, which have room echo (baked into the clone).
- Grace B `bGrsdLmwBbYUgHRuMFOI`: 1-sample clone; Grace said it didn't sound like her.
- Old Seedance skit clone `3dmagVYZFvrGkBbWWmGC`: already gone from the account (API 400 on 2026-10-20).
Job notes that name these voices are history. `test_B.mp3` / `test_C.mp3` stay as the echo meter's control.
