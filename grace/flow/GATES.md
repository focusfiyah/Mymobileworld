# Gates: Google Flow trial set up for the next job (Ralph 2026-10-23)

OWNS: grace/flow/**, CLAUDE.md, grace/PLAYBOOK.md, handoff/**

Scope: the next ad job runs its riskiest product clip in Ralph's Google Flow app ($0, his Pro credits) beside the Kie Omni take, and every session knows it.

- [ ] G1: CLAUDE.md carries the Flow trial rule with Ralph's words
  CHECK: grep -c 'Yes, set it up for the next job' CLAUDE.md grace/flow/README.md | grep -c ':1$' | grep -qx 2 && echo G1_OK
  EXPECT: G1_OK
  EVIDENCE: manual run 2026-10-23 (CHECK lines not approved in the checker, Ralph's rule): printed its G*_OK token

- [ ] G2: the Flow kit template covers refs, prompt, credits before/after, resolution check and the side-by-side compare
  CHECK: for w in 'Ingredients' 'credits before' 'ffprobe' 'side by side' 'prompt-master' 'REMOVED.md'; do grep -q "$w" grace/flow/README.md || exit 1; done && echo G2_OK
  EXPECT: G2_OK
  EVIDENCE: manual run 2026-10-23 (CHECK lines not approved in the checker, Ralph's rule): printed its G*_OK token

- [ ] G3: PLAYBOOK §6 $0 route line names the Flow app
  CHECK: grep -n 'Google Flow' grace/PLAYBOOK.md | grep -q 'grace/flow' && echo G3_OK
  EXPECT: G3_OK
  EVIDENCE: manual run 2026-10-23 (CHECK lines not approved in the checker, Ralph's rule): printed its G*_OK token

- [ ] G4: all five handoff memory files name Flow, are identical in both repos, paste copy = REMEMBER_ME, MEMORY_SHORT <= 2000 chars
  CHECK: for f in REMEMBER_ME.txt REMEMBER_ME_paste.txt GLOBAL_MEMORY.md CLAUDE_PREFERENCES.txt MEMORY_SHORT.txt; do grep -q 'Flow' handoff/$f && cmp -s handoff/$f ../Dayone-ai/handoff/$f || exit 1; done; cmp -s handoff/REMEMBER_ME.txt handoff/REMEMBER_ME_paste.txt && [ $(wc -c < handoff/MEMORY_SHORT.txt) -le 2000 ] && echo G4_OK
  EXPECT: G4_OK
  EVIDENCE: manual run 2026-10-23 (CHECK lines not approved in the checker, Ralph's rule): printed its G*_OK token

- [ ] G5: origin/main in Mymobileworld and Dayone-ai carries the change
  CHECK: git fetch -q origin main && git show origin/main:CLAUDE.md | grep -q 'Yes, set it up for the next job' && git -C ../Dayone-ai fetch -q origin main && git -C ../Dayone-ai show origin/main:handoff/MEMORY_SHORT.txt | grep -q Flow && echo G5_OK
  EXPECT: G5_OK
  EVIDENCE: manual run 2026-10-23 (CHECK lines not approved in the checker, Ralph's rule): printed its G*_OK token

- [x] G6: live Google Doc "Ralph standing rules (live)" refreshed: one doc with that title, it contains the Flow rule, LIVE_DOC.txt has its id
  EVIDENCE: manual: new doc 1dFNU_5CxYUZ5URaL4uZrUXQxKOEMng1FrkC7-AV1CmM read back, contains 'Google Flow trial (2026-10-23)'; old 1auqm... trashed; LIVE_DOC.txt updated in both repos

- [x] G7: Obsidian brain has a session log for this change on origin/main
  EVIDENCE: manual: obsidian-vault origin/main f972b73 adds Brain/Sessions/2026-10-23 Google Flow trial.md + Index link + Tools row
