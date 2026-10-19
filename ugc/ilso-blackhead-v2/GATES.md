# Gates: ilso Blackhead Remover Pore Care Bundle, 3 new Grace scripts (v2, 2026-10-19)

OWNS: ugc/ilso-blackhead-v2/**

Scope: 3 new humanized talking-head scripts (v1 from 2026-10-07 kept, none of its hooks reused), full PLAYBOOK §4 proofs incl. the viral board, Claude Doc, Drive folder updated (CURRENT v2, v1 to Older versions), email + push, $0.

- [x] G1: 3 spoken scripts exist and each closes with "It's in the orange cart."
  CHECK: node verify.mjs scripts
  EXPECT: SCRIPTS_OK 3
  EVIDENCE: automatic-evidence=v1; definition-sha256=89197f7197e7348138f4b792f8ff7b09258bc5dcac8e02cfd6ed9e1927f873c9; exit=0; EXPECT=matched; output-sha256=cc3e22f17a04a48aeb7085500e979c9f1e072e02fdf088ddc28161ba34356963; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G2: no banned phrase, dash, price, "label says", "reviewer" or cure claim in any script file
  CHECK: node verify.mjs banned
  EXPECT: BANNED_CLEAN 4
  EVIDENCE: automatic-evidence=v1; definition-sha256=ce28e2f0f76c0abb6d82dda224224d1b374f136993e0b42362f23cdbb8b4573a; exit=0; EXPECT=matched; output-sha256=0ed6aae7c431fb19c639f5561e64bd8204fb078f1be7c6e0b19e52b671f41c33; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G3: every script reads at grade 6 or lower and is 70 to 115 words
  CHECK: node verify.mjs readability
  EXPECT: READABILITY_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=494d083b1ef7c553c04cd4d3b2ac6f5eb51eb60466b6bde6a9efef037423fc63; exit=0; EXPECT=matched; output-sha256=ea570be0d1ebdbf0045606813d791ea86ddca04753cdc5036d8f96d115c4d09f; output-bytes=25; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G4: 9 library hooks said word for word, none repeated, none from v1, each script opens with its main hook
  CHECK: node verify.mjs hooks
  EXPECT: HOOKS_OK 9
  EVIDENCE: automatic-evidence=v1; definition-sha256=822ffd0781e0b0d5d02c77ecc7eb78113faf380d6ba7a0b0a90f3497965b8aac; exit=0; EXPECT=matched; output-sha256=00ae276d31947c7201ac23611ea20d61daf6717c366ac64df8a89c9639308b18; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G5: grace/gate.py passes all 9 steps, viral board included
  CHECK: node verify.mjs gate
  EXPECT: GATE_PASS
  EVIDENCE: automatic-evidence=v1; definition-sha256=36ec54ea5050535cf9d4b5e270adc934f97c7a16e0a5a84515e0d5154ddf336d; exit=0; EXPECT=matched; output-sha256=a7fce3ab74d19500972f24124fba79a3ac97616182ea0d8b3c4962814e38217f; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G6: README has a DONE ($0) Status line with the Drive folder and doc links
  CHECK: node verify.mjs readme
  EXPECT: README_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8cafbabfc528200636921b140ce017e2a1d0c7538920b26666a5f3bfaa2ab5eb; exit=0; EXPECT=matched; output-sha256=a6e1c515fbd233d568c0e37e0eb57e14266a79769d23d3ce522990def2691ae5; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ilso-blackhead-v2; path=7f4fb4b02918/15 entries

- [x] G7: Drive product folder holds a CURRENT v2 scripts Google Doc, the v1 doc renamed v1 (2026-10-07) inside Older versions, nothing loose
  EVIDENCE: Drive listing 2026-10-19 08:13Z: folder 1Y3C2TK7RR-Ns-BhhX8YOuN4gOZdPW_-Z holds "CURRENT - ilso Blackhead Remover Bundle scripts v2 (2026-10-19)" (143ZUmnY...) + "Older versions" (16XPl03R...) containing "v1 (2026-10-07) - ilso Blackhead Remover Bundle scripts"; two emoji-garbled test copies trashed

- [x] G8: phone-friendly Claude Doc with all 3 scripts, alt hooks, shot notes and product facts
  EVIDENCE: https://claude.ai/code/artifact/d91883d5-9b14-422d-b1e5-fb2761a7822f rev 1, all sections from scripts.md

- [ ] G9: email to life22watch@gmail.com and phone push sent
  EVIDENCE: email sent 2026-10-19 (Gmail id 1a1533975d875a4f). Push NOT sent: ToolSearch 'PushNotification' and 'push notification phone' returned no such tool in this session.
