# Grace's voice (ElevenLabs, Starter plan = instant clones only; professional clone not allowed, tested 2026-10-18)

**"Grace" `Rh3oAQMqRVf78UIVpBoQ` is Grace's ONE voice** (Grace's pick, 2026-10-20; grace.json). Use it for every Grace
voiceover and skit line:
1. Render: eleven_v4, stability 0.4, similarity 0.8, style 0.
2. Pace (free, always): `python3 grace/voice/pace.py IN OUT --wps 3.5`. Caps pauses at 0.15 s and retimes to 3.5 words/s
   (Grace's natural pace in Ralph's video) with pitch and formants kept, then levels to -16 LUFS. The raw render runs
   2.9 words/s with long pauses, which Grace found too slow. Needs `pip install faster-whisper` (free local model).
3. Clean the echo (free, always): `python3 grace/voice/clean.py PACED OUT` (resemble-enhance, best of 3 runs that keep
   every word, about 8 minutes for 30 s). The clone carries some room echo from her accent clips; Ralph approved the
   cleaned sound 2026-10-20 ("It is good now"). Setup lines are at the top of clean.py.
4. Then the usual STT stutter check (PLAYBOOK §6).

## How it was made (2026-10-20, three rounds)
- Round 1 (echo): a clone from 7 of her TikToks picked for low echo alone. Grace: "too American". Those clips turned out
  far from her natural voice (closeness 0.807 to Ralph's video vs 0.93+ for her best clips). Deleted.
- Round 2 (accent): Ralph sent a video of Grace talking in her Haitian accent (VID-20261019-WA0017.mp4, not committed).
  Her @shewiththeglow TikToks (display name GraceWithTheGlow; only posted before 2026-09-25, before any AI voice on her
  account) were ranked by resemblyzer closeness to that video; the 10 closest that were not echoey, plus the video,
  make 173 s of speech (accent_rank.json). Whisper language ID could not rank accent (P(en) ~0.999 everywhere).
  Tests: same clone on eleven_v4 (C) 0.835, on multilingual_v2 (E) 0.839; round-1 voice on v2 or with a "[Haitian
  accent]" tag did not move (0.761 / 0.749). Grace liked C's sound with E's pace.
- Round 3 (pace): `pace.py` retimes C for free; G (3.5 words/s, closeness 0.844) picked over F (E's 4.1).
- Round 4 (echo): Ralph heard an echo in G (fast decay 171 ms vs 100 for the round-1 voice). WPE dereverb changed nothing
  (the echo is in the clone's voice, not a room); resemble-enhance at temperature 0.1 brings it to 100-150 ms and keeps
  every word (`clean.py`). The meter cannot judge accent after cleaning, so that was by ear.
- Review page: https://claude.ai/artifact/ERywTwEf9dwoxqgtH8jqyH. Gates: GATES.md (`check.py`).
- Cost: about 920 ElevenLabs characters over the three rounds (test lines only; cloning is free).

## To rebuild it
Get a fresh video of Grace talking naturally (her accent), re-download her TikToks (`yt-dlp --impersonate chrome`, needs
`pip install curl_cffi`), rank them by closeness to that video, look at the frames (Grace on camera, no reposts), drop
echoey ones (`echo.py`), trim (silenceremove), clone, then A/B against the current voice on the review page before
swapping ids. Ask Ralph first; delete the old voice only on his OK.

## Retired (deleted from ElevenLabs 2026-10-20)
- Round-1 "Grace" `gjmt5xZqVE6mjSY4NfQM`: low echo but American-sounding.
- Grace C `P8OUGBCvq8OBS4xlb65A`: cloned from her Wag Bag takes; room echo and no accent.
- Grace B `bGrsdLmwBbYUgHRuMFOI`: 1-sample clone; Grace said it didn't sound like her.
- Old Seedance skit clone `3dmagVYZFvrGkBbWWmGC`: already gone from the account (API 400 on 2026-10-20).
Job notes that name these voices are history. `test_B.mp3` / `test_C.mp3` stay as the echo meter's control.
