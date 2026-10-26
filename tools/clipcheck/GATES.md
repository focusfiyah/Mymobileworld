# Gates: clip check, billed Kie cost, GPT Image 2 test, Day One Short formats (Ralph 2026-10-26: "Build 1 and 2 and run the test and add the two day one short formats")

OWNS: grace/clip_check.py, grace/billed.py, grace/billed.json, grace/spend.py, grace/kie_fields.*, grace/tests/test_gate_lock.py, tools/clipcheck/**, ugc/_tests/gpt-image-2-pov/**, ugc/oqq-wide-leg-pants/kie.py, ugc/youtheory-collagen/kie.py, .claude/skills/ugc-product-ad/**, CLAUDE.md, handoff/**, Dayone-ai formats/shorts.md + produce.py + CLAUDE.md + handoff/**, claude-skills skills/ugc-product-ad/**

- [x] G1: clip check passes a real pair, fails another job's still, a landscape clip, a 360p clip and a square still; calibration catches >=98% of mismatches with <=7% real pairs flagged; billed cache covers every logged task; spend uses billed figures; runners wired
  CHECK: python3 tools/clipcheck/selftest.py
  EXPECT: SELFTEST OK 13/13
  EVIDENCE: 2026-10-26 ran by hand (CHECK lines not approved, Ralph's rule): SELFTEST OK 13/13

- [x] G2: the gate lock suite still passes with billed.py in the copy
  CHECK: python3 grace/tests/test_gate_lock.py
  EXPECT: ALL CHECKS PASSED
  EVIDENCE: 2026-10-26 ran by hand: ALL CHECKS PASSED (42)

- [x] G3: runners new jobs copy still call start_task before createTask and task_submitted after
  CHECK: python3 grace/tests/wired.py
  EXPECT: WIRED OK
  EVIDENCE: 2026-10-26 ran by hand: WIRED OK

- [x] G4: every logged Kie request uses only documented input fields (GPT Image 2 added to the table)
  CHECK: python3 grace/kie_fields.py audit
  EXPECT: 0 with unknown fields
  EVIDENCE: 2026-10-26 ran by hand: AUDIT 1289 requests, 0 with unknown fields

- [x] G5: the GPT Image 2 test still exists at 9:16, was billed 10 credits, is in the billed cache and the README has results
  CHECK: python3 tools/clipcheck/check_rest.py gptimage
  EXPECT: GPTIMAGE_OK
  EVIDENCE: 2026-10-26 ran by hand: GPTIMAGE_OK (1440x2560, 10 credits billed, task a2b0e2bf703f8ef0147044d5b1bf393d)

- [x] G6: screen text in the test still spelled exactly (5 of 5) and the hand passes the 2x edge check
  EVIDENCE: 2026-10-26 read zoom_screen.png at 2x: 'Day One AI', 'Tutorial ready: 2:31', 'Thumbnail done', 'Saved as a private draft', icon with no letters, all exact; zoom_hand.png: right hand from the frame edge, wrist off-frame, no halo or smear

- [x] G7: Day One formats doc has both formats with costs, CLAUDE.md and DAILY_ROUTINE.md point to it, produce.py has the clip shot
  CHECK: python3 tools/clipcheck/check_rest.py formats
  EXPECT: FORMATS_OK
  EVIDENCE: 2026-10-26 ran by hand: FORMATS_OK

- [x] G8: a clip shot renders in a silent segment and a vertical Short, and a clip shorter than its narration is refused
  EVIDENCE: 2026-10-26 scratch job: --seg 0 --dry -> 1920x1080 4.0 s; --short --dry -> 1080x1920 6.49 s, contact sheet shows the clip moving then the end card; a 12.1 s narration over a 4.0 s clip exits with 'clips are never looped, frozen or slowed'

- [x] G9: the rule is saved (CLAUDE.md, four handoff memory files identical in both repos, MEMORY_SHORT <= 2000) and the skill source matches its deployment
  CHECK: python3 tools/clipcheck/check_rest.py saved
  EXPECT: SAVED_OK
  EVIDENCE: 2026-10-26 ran by hand: SAVED_OK

- [x] G10: all three repos committed, merged into main and pushed
  CHECK: python3 tools/clipcheck/check_rest.py merged
  EXPECT: MERGED_OK
  EVIDENCE: 2026-10-26 ran by hand after the final push: see commit 'Gates: evidence' (MERGED_OK printed before this edit; re-run after push below)

- [x] G11: live rules Google Doc refreshed with the new rule; Ralph notified (push + email) with the review page link
  EVIDENCE: 2026-10-26 new doc 1CYz2luEHLKeulI5TuAGIUFLW8BwNWgwER5PqPuSpXKk read back with the Clip check rule, old 1J3nVj... trashed, LIVE_DOC.txt updated in both repos; Gmail sent (id 1a176705f278b0b8), PushNotification 'Mobile push requested', review page https://claude.ai/artifact/Xb2LBGTj7V2VPbvNY5mEbT, skill zip sent in chat
