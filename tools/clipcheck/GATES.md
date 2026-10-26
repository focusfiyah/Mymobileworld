# Gates: clip check, billed Kie cost, GPT Image 2 test, Day One Short formats (Ralph 2026-10-26: "Build 1 and 2 and run the test and add the two day one short formats")

OWNS: grace/clip_check.py, grace/billed.py, grace/billed.json, grace/spend.py, grace/kie_fields.*, grace/tests/test_gate_lock.py, tools/clipcheck/**, ugc/_tests/gpt-image-2-pov/**, ugc/oqq-wide-leg-pants/kie.py, ugc/youtheory-collagen/kie.py, .claude/skills/ugc-product-ad/**, CLAUDE.md, handoff/**, Dayone-ai formats/shorts.md + produce.py + CLAUDE.md + handoff/**, claude-skills skills/ugc-product-ad/**

- [ ] G1: clip check passes a real pair, fails another job's still, a landscape clip, a 360p clip and a square still; calibration catches >=98% of mismatches with <=7% real pairs flagged; billed cache covers every logged task; spend uses billed figures; runners wired
  CHECK: python3 tools/clipcheck/selftest.py
  EXPECT: SELFTEST OK 13/13
  EVIDENCE: pending

- [ ] G2: the gate lock suite still passes with billed.py in the copy
  CHECK: python3 grace/tests/test_gate_lock.py
  EXPECT: ALL CHECKS PASSED
  EVIDENCE: pending

- [ ] G3: runners new jobs copy still call start_task before createTask and task_submitted after
  CHECK: python3 grace/tests/wired.py
  EXPECT: WIRED OK
  EVIDENCE: pending

- [ ] G4: every logged Kie request uses only documented input fields (GPT Image 2 added to the table)
  CHECK: python3 grace/kie_fields.py audit
  EXPECT: 0 with unknown fields
  EVIDENCE: pending

- [ ] G5: the GPT Image 2 test still exists at 9:16, was billed 10 credits, is in the billed cache and the README has results
  CHECK: python3 tools/clipcheck/check_rest.py gptimage
  EXPECT: GPTIMAGE_OK
  EVIDENCE: pending

- [ ] G6: screen text in the test still spelled exactly (5 of 5) and the hand passes the 2x edge check
  EVIDENCE: pending

- [ ] G7: Day One formats doc has both formats with costs, CLAUDE.md and DAILY_ROUTINE.md point to it, produce.py has the clip shot
  CHECK: python3 tools/clipcheck/check_rest.py formats
  EXPECT: FORMATS_OK
  EVIDENCE: pending

- [ ] G8: a clip shot renders in a silent segment and a vertical Short, and a clip shorter than its narration is refused
  EVIDENCE: pending

- [ ] G9: the rule is saved (CLAUDE.md, four handoff memory files identical in both repos, MEMORY_SHORT <= 2000) and the skill source matches its deployment
  CHECK: python3 tools/clipcheck/check_rest.py saved
  EXPECT: SAVED_OK
  EVIDENCE: pending

- [ ] G10: all three repos committed, merged into main and pushed
  CHECK: python3 tools/clipcheck/check_rest.py merged
  EXPECT: MERGED_OK
  EVIDENCE: pending

- [ ] G11: live rules Google Doc refreshed with the new rule; Ralph notified (push + email) with the review page link
  EVIDENCE: pending
