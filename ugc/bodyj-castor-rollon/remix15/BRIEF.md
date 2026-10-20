# BodyJ castor roll-on: 4 x 15 s remixes of the selling video (Grace)

Status: 2026-10-20 BRIEF only. Waiting on Grace's 4 scripts (Ralph forwards them). Nothing made, $0 spent.

## What Ralph asked (2026-10-20, his words)
"Use the winning formula. Keep the visuals similar, similar script, change the hook as long as it makes sense. remix
the current video. Let's do 4 videos. 15s timeframe and she will send 4 scripts. Let's compare the scripts before you
make the videos."

## The winner (why we are building on it)
- https://www.tiktok.com/@shewiththeglow/video/7697844264050511135 (posted 2026-10-18, 31 s): 3 sales, 1,578 views
  = 526 views per sale on 2026-10-20, best of Grace's tracker (`grace/winners/winners.json`, `PATTERNS.md`).
- Reply to the comment "I think we all need castor oil" (@umi3728) on Grace's viral cradle-cap video; comment sticker on frame 1.
- **Voice: Grace's OWN voice, not ElevenLabs** (Ralph 2026-10-20). The new 4 are voiced by Grace too, unless Ralph says otherwise.
- Promoted by the brand (TikTok ad label).
- Script as posted (TikTok captions): "The only thing I hate about Castor oil is how thick and messy it is. And let's be
  for real, the smell isn't exactly something you want lingering all day. But if you know, you know, Castor oil is
  liquid gold. And this roll on. Freaking ingenious. No pouring, no oily fingers. Just roll it exactly where you want
  it. It's USDA organic, cold pressed and hexane free with a rose quartz roller. I'mma do y'all a favor and link it in
  the orange car[t]. If you want condition brows, softer cuticles, moisturize skin and hair, growing longer, smoother,
  and shinier, you know what to do."
- Footage: our v2g cut (`out/bodyj_castor_v2g_r1_final.mp4`, clips in `clips/` S1-S9 + N1-N4, in git), messy pour ->
  roll-on -> label close-ups -> scalp/hair -> box on nightstand. The posted file can be pulled with
  `tiktok.py video <link>` (has Grace's voice).

## The job
1. When Ralph sends Grace's 4 scripts: COMPARE them before making anything. For each: words + estimated length at
   her pace (~3 words/s, so ~45 words for 15 s), hook vs the winner's, structure vs the winner, readability grade,
   claims the listing can't back (the winner's "hair growing longer" is a growth claim: flag, never silently edit),
   banned phrases (`grace/gate.py`), and what it keeps from the winning formula (messy-vs-roll-on proof early, one
   objection killed, orange cart close). One table, then a recommendation. Use them word for word only on Ralph's say
   (per-video `overrides` in checklist.json).
2. Ask how the voice arrives: Grace records each script herself (default) and sends the audio, or Ralph decides otherwise.
3. Plan the remix (free first): 15 s each, built from the existing castor clips, visuals similar to the winner;
   Ralph explicitly asked to remix this video, so record that as his override of the "every video different" rule in
   checklist.json, and still vary order/crop/grade per video so TikTok doesn't see 4 identical uploads.
   Any new clip or still costs money: ask first with the exact cost.
4. Usual finish: QC (`qc/verify_fix.py`), AI finish (`ai_finish.sh`), REMOVED.md check, one Artifact review page,
   Drive (Grace Tiktok assets/BodyJ folder, CURRENT- names), email + push to Ralph.
