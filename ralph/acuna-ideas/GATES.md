# Gates: Acuna idea 1, comment-to-DM on Instagram

OWNS: ralph/acuna-ideas/**

Scope: the free comment-to-DM bot on @realgoodhustles is proven on a real comment, its username bug is fixed in the repo and the workbench, and the 7-idea tracker exists.

- [x] G1: Dayone-ai main has the fixed script (reads the commenter from `from`, own-comment check uses it, parses)
  CHECK: python3 ralph/acuna-ideas/verify.py repo
  EXPECT: REPO_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=058008a532bd463b8fd59242dee96b5d7010ccc5b9e0ded70de43a98d029ffe0; exit=0; EXPECT=matched; output-sha256=5a3b8b74d8926000027259edc16a5910de92a7e5b0795cc921fb161020879e0e; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G2: the workbench copy the scheduled task runs is byte-identical to the repo copy
  EVIDENCE: 2026-10-28 06:4x UTC: repo sha256 f99a92015a9f6763..., /mnt/files/ig_comment_dm.py sha256 f99a92015a9f6763... (measured inside the Composio workbench), dry run after the copy: sent [] skipped 3 total_done 1.

- [x] G3: a real AUTOPILOT comment got the DM and the public reply
  EVIDENCE: 2026-10-28: comment 18111565625184788 by azariahlife; POST /me/messages returned recipient_id 1150692771243394 + a message_id; public reply 18121323754946713 "Sent! Check your DMs" read back from /replies; state file done count 1.

- [x] G4: running again sends nothing twice
  EVIDENCE: 2026-10-28: second live run printed sent [] failed [] skipped 3 total_done 1.

- [x] G5: Ralph confirms the DM arrived in @azariahlife's inbox (may sit in Message requests)
  EVIDENCE: 2026-10-28 Ralph: "I checked the Zarya Life. The message was there, and it was good to go." (voice typing for @azariahlife)

- [x] G6: the tracker lists all 7 ideas with item 1 marked done
  CHECK: python3 ralph/acuna-ideas/verify.py tracker
  EXPECT: TRACKER_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=46aad085f083d6e94bd06271f9a98162cafaf28d77854483612b5ede82a03ef3; exit=0; EXPECT=matched; output-sha256=4cba7042338c9e0f33e20bedc24b5443822bc6a35411a4fccb143443873daa45; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G7: brain notes pass the recall check
  CHECK: python3 tools/brain/check.py --terms "Acuna Ideas Tracker,comment_id,azariahlife,carousels"
  EXPECT: BRAIN_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=c3add1f7a19910e47ce9a64ec292ba63d703017ac4fdf11ee3ddcce9ae82a0c0; exit=0; EXPECT=matched; output-sha256=d3ef19b2291cd7f32eab317c0b25452845389183bea3bbc9b04f47e89122b1c1; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries
