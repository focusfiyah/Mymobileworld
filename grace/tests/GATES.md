# Gates: gate.py gets the three Video Factory ideas (Ralph 2026-10-22: "Build those three ideas into gate.py")

OWNS: grace/gate.py, grace/paid.py, grace/spend.py, grace/tests/**, .claude/skills/ugc-product-ad/**, ugc/youtheory-collagen/kie.py, CLAUDE.md, grace/PLAYBOOK.md, handoff/**

Scope: (1) Production Book: no paid call until BOOK.md is filled and Ralph's OK is recorded against its exact text;
(2) budget lock: spend since that OK can never pass the approved total plus recorded extras, in-flight tasks included;
(3) paid-task ledger: each paid task is saved and pushed when it starts, and a task already paid in this folder or on
any session branch is refused until it is named in GATE_REDO.

- [ ] G1: every scenario in the test suite passes (book missing/blank/changed, approval, budget lock incl. in-flight, extras, local duplicate, duplicate on another session branch (the Vicks case), GATE_REDO, push of the claim, scripts-only check unchanged)
  CHECK: python3 grace/tests/test_gate_lock.py
  EXPECT: ALL CHECKS PASSED
  EVIDENCE: pending

- [ ] G2: the script-gate output of 4 real jobs (plan + cut stage) is identical to the baseline taken before the change
  CHECK: python3 grace/tests/regress.py /tmp/claude-0/-home-user/2f03326b-4f99-5fdd-b899-985dbe957ce4/scratchpad/base
  EXPECT: REGRESSION OK 8/8
  EVIDENCE: pending

- [ ] G3: the runners new jobs copy (omni_clip.py, youtheory-collagen kie.py) call start_task before createTask and task_submitted after it
  CHECK: python3 grace/tests/wired.py
  EXPECT: WIRED OK
  EVIDENCE: pending

- [ ] G4: the rule is written where sessions read it (CLAUDE.md, PLAYBOOK, ugc-product-ad SKILL.md + plan template, the four handoff memory files, MEMORY_SHORT <= 2000 chars)
  CHECK: python3 grace/tests/docs.py
  EXPECT: DOCS OK
  EVIDENCE: pending

- [ ] G5: the job branch is merged into main and pushed (Mymobileworld and claude-skills)
  CHECK: python3 grace/tests/merged.py
  EXPECT: MERGED OK
  EVIDENCE: pending

- [ ] G6: live rules Google Doc refreshed and the skill zip rebuilt for Ralph's upload
  EVIDENCE: pending
