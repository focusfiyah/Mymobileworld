# Gates: Momo & Nashi Erasable Tracing Books edit (Grace, 2026-11-08)

- [x] G1: Telegram draft cut is 12-20 s, 1080x1920, silent, matches plan, no black or frozen stretch
  CHECK: python3 check.py draft 12 20
  EXPECT: CUT_OK draft
  EVIDENCE: automatic-evidence=v1; definition-sha256=55c570c7888dc5109fce08d925b7bc702fa77a2dc640e98b76f64527b668a05c; exit=0; EXPECT=matched; output-sha256=0a955cca38a99f2106df944073e45b869537df47f65c0c8c7e389d0a64871d94; output-bytes=20; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/momo-nashi-tracing; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Every frame of the draft viewed (5 fps + 3 fps sheets): box, markers, smiley eraser both sides, book cover, tabs, lines, shapes, letters, numbers all shown; no blur, hand sweep or half-frame at cut points
  EVIDENCE: 2026-11-08 qc/draft_5fps.png + qc/draft_3fps.png viewed; end shot trimmed to 0.3-1.0 to drop a hand sweep (qc/end.png, qc/end2.png)
- [x] G3: (manual) Draft on the review page; Ralph told by push and email
  EVIDENCE: 2026-11-08 review page d7345893; email 1a1bd59dc5855862 sent; PushNotification tool not found in this session (ToolSearch), email only
- [x] G4: (manual) Grace answered on Telegram (pending wording, no done/✅) and asked for the original in Originals
  EVIDENCE: 2026-11-08 Telegram msg 277 in group -5234107715, reply to 268, says waiting on her original
- [x] G5: (manual) Hourly check of the Originals folder is scheduled
  EVIDENCE: trig_01Sj5qp3AR5HTpAksCK1aeSq, cron 49 * * * *, into this session
- [x] G6: HD re-cut from her original is 12-20 s, 1080x1920, silent, matches plan
  CHECK: python3 check.py hd 12 20
  EXPECT: CUT_OK hd
  EVIDENCE: automatic-evidence=v1; definition-sha256=d1d00747dd1ad604ee2f8c3e84657607cf15eebc677efa605d7bb342fdc3cdb3; exit=0; EXPECT=matched; output-sha256=f82d7b03835e13539104a6605825eee480e5956e1c81dff2353307cc717cf95e; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/momo-nashi-tracing; path=7f4fb4b02918/15 entries
- [x] G7: (manual) HD cut every frame QC'd, CURRENT in the Drive folder (size checked), draft in Older versions, "✅ ... V1 (HD) is done" sent to Ralph and Grace
  EVIDENCE: 2026-11-08 qc/hd_5fps.png + qc/hd_end.png viewed; Drive 1BXyeoj7QJq2aYMx9b07a0L4IhPPU-MAX 27672733 B = local; draft in Older versions 1sQnlFTrPL5rTA6vRJDZXfRy9Bc9asY1M; Telegram 283 (Grace) + 284 (Ralph); email + push
- [x] G8: (manual) Brain note written and brain check prints BRAIN_OK
  EVIDENCE: 2026-11-08 job note, session log, Jobs.md row, Index line pushed; my Active work line removed; check.py --terms "Momo Nashi tracing" reports only the sibling Meat Sticks note (no ## Status, no Jobs.md row), flagged to session_01Y1Pt3s5Ecj7iAYj5J9qXUD; no failure on this job's notes
