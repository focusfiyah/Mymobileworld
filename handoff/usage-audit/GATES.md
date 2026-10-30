# Gates: Claude Code usage audit (TikTok @ccstrategic.io tips applied to our setup)

OWNS: handoff/usage-audit/**, CLAUDE.md, handoff/history/**, .claude/settings.json

Scope: cut the always-loaded rule files and add safe settings from the video's tips, without losing one rule.

- [ ] G1: Both CLAUDE.md files are at least 30% smaller than before
  CHECK: python3 handoff/usage-audit/verify.py size
  EXPECT: SIZE_OK
  EVIDENCE: pending

- [ ] G2: Every line removed from a CLAUDE.md exists word for word in a history file
  CHECK: python3 handoff/usage-audit/verify.py lossless
  EXPECT: LOSSLESS_OK
  EVIDENCE: pending

- [ ] G3: Standing rules and accounts stayed in CLAUDE.md and pointers resolve to non-empty files
  CHECK: python3 handoff/usage-audit/verify.py keep
  EXPECT: KEEP_OK
  EVIDENCE: pending

- [ ] G4: Settings are valid JSON in both repos, with deny rules and the bash output cap, hooks untouched
  CHECK: python3 handoff/usage-audit/verify.py settings
  EXPECT: SETTINGS_OK
  EVIDENCE: pending

- [ ] G5: Tips skipped because they collide with Ralph's rules are listed in the report (Opus-only Day One sessions, long video contexts, loops)
  EVIDENCE: pending
