# Gates: record the 15 unmerged session branches as merged (Ralph 2026-10-23: "Go ahead")

OWNS: handoff/merge-2026-10-23/**, ugc/**, grace/**, CLAUDE.md, handoff/**

Scope: every branch branch_sync.py lists is merged into main, main's newer rules kept, any job note missing from main ported, nothing lost.

- [ ] G1: branch_sync.py prints SYNC_OK for Mymobileworld
  CHECK: python3 handoff/branch_sync.py
  EXPECT: SYNC_OK
  EVIDENCE: pending

- [ ] G2: every line a branch added that main lacks is listed in LOG.md with its decision (ported, or superseded by a named newer main rule)
  EVIDENCE: pending

- [ ] G3: Dayone-ai and claude-skills already clean
  CHECK: cd ../Dayone-ai && python3 ../Mymobileworld/handoff/branch_sync.py | tail -1 && cd ../claude-skills && python3 ../Mymobileworld/handoff/branch_sync.py | tail -1 | sed 's/SYNC_OK/BOTH_SYNC_OK/'
  EXPECT: BOTH_SYNC_OK
  EVIDENCE: pending

- [ ] G4: origin/main carries the merges (no branch-sync leftovers after push)
  CHECK: git fetch -q origin && git status -sb | head -1 && python3 handoff/branch_sync.py | tail -1 | sed 's/SYNC_OK/MAIN_SYNC_OK/'
  EXPECT: MAIN_SYNC_OK
  EVIDENCE: pending
