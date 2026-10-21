# Gates: Synthetic Wig voiceover scripts (Grace), 2026-10-21

OWNS: ugc/synthetic-wig/**

Scope: Grace gets voiceover scripts for her own footage (Drive "SyntheticWig.MOV", 59 s, highlight brown wig).
Each script fits that footage with a shot map, uses a library hook word for word, passes the Grace script gate, and
lands in a Claude doc plus the product's Drive folder. Ralph is notified by push and email.

- [x] G1: footage beats mapped with timestamps (what is on screen each second range, where her mouth is visible)
  CHECK: python3 -I check_scripts.py beats
  EXPECT: beats OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=a0408665f3287a241f2469e1670f7c3702ad7caf79dc9793c76367fb228cc1e8; exit=0; EXPECT=matched; output-sha256=92142f0110b0b19cad430278f40556153107cb35be1c2191322c59dafb1b9ac1; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/synthetic-wig; path=7f4fb4b02918/15 entries

- [x] G2: Grace script gate passes (playbook, coach, viral board, facts, audience, hooks, humanizer, readability, line sources)
  CHECK: python3 -I ../../grace/gate.py . 2>&1 | tail -1
  EXPECT: GATE OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=626bb17569cc7293692d35bf9b90f7f79865893b333caf2889a8ffdb538c87ea; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/synthetic-wig; path=7f4fb4b02918/15 entries

- [x] G3: every script: hook is a library hook word for word, ends with "It's in the orange cart.", 70-95 words, no price, no "reviewer", no "the label says", no hook id reused, every shot-map range inside the 59 s clip
  CHECK: python3 -I check_scripts.py scripts
  EXPECT: scripts OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=6424c594e1bea98f994275f00ea0414ada3b9708a88ebf71d4e31b6f0cd7d155; exit=0; EXPECT=matched; output-sha256=7768ddc63865b943c3a1e509675c3d4860d32a04bb2d6871fdf0421292369179; output-bytes=155; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/synthetic-wig; path=7f4fb4b02918/15 entries

- [x] G4: each script reads at grade 6 or lower (measured by the coach, per video)
  CHECK: python3 -I check_scripts.py grades
  EXPECT: grades OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=5165370e1376af6c943c1ad5bc382a1439e297aab5acc2fe14c2b3701d9a484c; exit=0; EXPECT=matched; output-sha256=17936f106cec756cd25b8fa5bd23b2cd1d8d582b02a5f3b799c903c9c34571e3; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/synthetic-wig; path=7f4fb4b02918/15 entries

- [x] G5: Claude doc published with all 3 scripts + shot maps + alt hooks + captions (link in README)
  EVIDENCE: https://claude.ai/artifact/V3eXJK4CgP753knpiWK6wd rev 7: How to use, V1, V2, V3 (each table of beat/line/clip seconds + alt hooks + text options + caption), Why these angles, Product facts; all 6 pending blocks resolved (pending_ended on each fill); link in README.md

- [x] G6: Drive "Grace Tiktok assets" has ONE "Synthetic Wig (Grace)" folder with "CURRENT - " scripts doc, nothing new loose
  EVIDENCE: search for wig folders in Grace Tiktok assets returned none, then created folder 1vgVOitKBvgZbnqKNWmVAlVxN8Ns8LX7y; doc 'CURRENT - Synthetic Wig voiceover scripts v1 (2026-10-21)' 14UmV3UZKpEwiV-qbm4Rg5xHdeBvzH9v6WNu6VZEaabc inside it, read back in full (all 3 scripts). Grace's own SyntheticWig.MOV was already loose there (her upload, left in place, flagged to Ralph)

- [ ] G7: README status line, CLAUDE.md job entry, playbook results line committed and pushed
  CHECK: test -z "$(git status --porcelain .)" && git fetch -q origin ccr-e66acd3b-4c4fj1 && git diff --quiet HEAD origin/ccr-e66acd3b-4c4fj1 && echo pushed-clean
  EXPECT: pushed-clean
  CWD: .

- [x] G8: Ralph notified (phone push + email) with the doc and folder links
  EVIDENCE: PushNotification 'Mobile push requested.'; Gmail GMAIL_SEND_EMAIL (gmail_correa-comus) id 1a15d171bb30c945 to life22watch@gmail.com with both links
