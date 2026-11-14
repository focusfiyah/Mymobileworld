# Gates: weekly workflow audit 2026-11-14

- [x] G1: Every repo with rule files has no unmerged branch
  CHECK: for r in Mymobileworld Dayone-ai jean-rameau claude-skills obsidian-vault OpenMontage; do (cd /home/user/$r && git fetch -q origin && python3 /home/user/Mymobileworld/handoff/branch_sync.py | tail -1); done | grep -c SYNC_OK | sed 's/^/SYNCED=/'
  EXPECT: SYNCED=6
  EVIDENCE: automatic-evidence=v1; definition-sha256=cc2381175d3d2d15c8ce65cf8b6755269d7778b4f0cee927c312414e2096103c; exit=0; EXPECT=matched; output-sha256=70937c84da93896bf9d39dba450756f3fee3600739f4db61900ab4374f8e14d0; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/audits/2026-11-14-weekly; path=7f4fb4b02918/15 entries
- [x] G2: Grace gate test suites all pass
  CHECK: cd /home/user/Mymobileworld && for t in grace/tests/test_*.py; do python3 $t | tail -1; done | grep -c -E "PASSED|_OK" | sed 's/^/SUITES=/'
  EXPECT: SUITES=5
  EVIDENCE: automatic-evidence=v1; definition-sha256=970662bb6d8c4045d25d6bfeba49f819f592db7efa132f1b3f36e39333e42592; exit=0; EXPECT=matched; output-sha256=16fbdc05e3c352e752ce55de84495a4279a932f9866619ce793448a403bbfe8a; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/audits/2026-11-14-weekly; path=7f4fb4b02918/15 entries
- [x] G3: Every job's media is in Drive
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check | tail -1
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f7d590d44e72c5ba80b41256aa8f911982cdd447d8dfac5e10a4ddc403da7a83; exit=0; EXPECT=matched; output-sha256=8083bc5e3d38fc4812679011f657b4c749435c73ae3358ae5426effe963edf5b; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/audits/2026-11-14-weekly; path=7f4fb4b02918/15 entries
- [x] G4: Skill home matches both deployments for every skill
  CHECK: cd /home/user/claude-skills && for s in $(ls skills); do for d in /home/user/Mymobileworld/.claude/skills /home/user/Dayone-ai/.claude/skills; do [ -d $d/$s ] && ! diff -rq skills/$s $d/$s >/dev/null && echo DRIFT; done; done | grep -c DRIFT | sed 's/^/DRIFTS=/'
  EXPECT: DRIFTS=0
  EVIDENCE: automatic-evidence=v1; definition-sha256=3adb6c098d73af9f50286012cc5a9a651ff136739f6400756ba327617e92ce08; exit=0; EXPECT=matched; output-sha256=aac6592f68be4c860b9ac89105092742189486533ff508c6aac7ceb39e142123; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/audits/2026-11-14-weekly; path=7f4fb4b02918/15 entries
- [x] G5: Brain check passes with the audit's recall terms and this session's Active work line removed
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "weekly audit, SessionStart hooks, KIGO set 2, prompt-master drift, budget" | tail -1
  EXPECT: BRAIN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a95eb8afc7653aa27d09c91f570220c56b1eb6e4d7a65d06a5d167ddd33d76f9; exit=0; EXPECT=matched; output-sha256=140d532321810ee7c86ec90aae74e74c056b945579c8dcd9198cb2ef6e57f7b1; output-bytes=51; shell=/bin/sh; cwd=/home/user/Mymobileworld/audits/2026-11-14-weekly; path=7f4fb4b02918/15 entries
- [x] G6: The audit doc has sections for what worked, what didn't, skills and tools, today's fixes and Ralph's decisions
  EVIDENCE: Claude Docs doc "Weekly Audit Nov 14" rev 2 written 2026-11-14 with sections 1-7 (numbers, worked, didn't work, skills and tools, fixed today, decisions, your steps)
