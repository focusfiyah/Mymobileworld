# Gates: Your Wish Is Your Command book, 3 Grace scripts

OWNS: ugc/your-wish-book/**, CLAUDE.md

Scope: three talking-head TikTok Shop scripts for Grace for the book, every Rule 0 proof saved, delivered as a Claude doc + Drive Google Doc in one product folder, Ralph notified.

- [x] G1: grace/gate.py passes for the job (all PLAYBOOK §4 proofs present, newer than the script, no banned phrase)
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=3050429bea3e20bd250d5cd2dc306f71998f919d598c1d1a5512aa32ffa68929; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/your-wish-book; path=7f4fb4b02918/15 entries

- [x] G2: exactly 3 scripts, each with HOOK, BODY, CTA and the "It's in the orange cart." close
  CHECK: node check.mjs structure
  EXPECT: STRUCTURE OK
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=013e633b7d2d4cc0cbccfd11f42a1a9ec70a281dfff747d12e53d33a59d3e94c; exit=0; EXPECT=matched; output-sha256=79ac66c1ec2e069e98131dfe11d6de8c911cf89b56292476e60d24f668b13491; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/your-wish-book; path=7f4fb4b02918/15 entries

- [x] G3: every hook (main + 2 alts per script) is a library hook said word for word, no id reused
  CHECK: node check.mjs hooks
  EXPECT: HOOKS VERBATIM OK 9
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=60031f8f1370518d0ad71f87a64a5cc9ef13258ab1d60526200b70863c8af032; exit=0; EXPECT=matched; output-sha256=41618b98d97304a62b0b9a6aaa5801aa47a927f4cb5abfc81c29d6f2c53937e1; output-bytes=20; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/your-wish-book; path=7f4fb4b02918/15 entries

- [x] G4: no price number, "reviewer", "the label says", dash or other banned phrase anywhere in scripts.md
  CHECK: node check.mjs banned
  EXPECT: BANNED CLEAN
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=1ebce14f03e84ae74452530727f139e88cb9cdb9a92abb0ee1e80bda98379a33; exit=0; EXPECT=matched; output-sha256=0ccb2d65f37a865eba5bb9757ee230600b5c78eddecbdcfcec433a946b7b429e; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/your-wish-book; path=7f4fb4b02918/15 entries

- [x] G5: every book claim in the scripts is backed in product_facts.md (no outcome promises for manifesting)
  EVIDENCE: product_facts.md maps every script claim to listing/Google Books/author video/review; money and control bullets listed under Not used (checked 2026-10-19)

- [x] G6: Claude doc published with all 3 scripts; Drive "Grace Tiktok assets" has ONE folder for the book with a "CURRENT - " Google Doc, nothing loose
  EVIDENCE: Claude doc https://claude.ai/code/artifact/05dbf55e-c6d4-4e6f-91a4-9f66bdd42b72 rev 6, all 3 scripts; Drive folder 1Oo1m8oiLuq2xE1131l0dh6Rs3K0z5B-u created in Grace Tiktok assets (no earlier folder found), CURRENT doc 1P8fxgyZti_7crMj4itv7E6tqzoyPxbbt8QHQL44efac, 4434 bytes, snippet checked

- [x] G7: Ralph notified: thread reply with links, phone push and email (or failure stated)
  EVIDENCE: Email sent (Gmail id 1a15579a39a2d65a). Phone push: ToolSearch select:PushNotification and a keyword search returned no such tool in this session; stated in the thread reply

- [x] G8: README Status line + CLAUDE.md Jobs line written and pushed to claude/project-thread-mx5xol
  CHECK: git -C ../.. log origin/claude/project-thread-mx5xol -1 --format=%s
  EXPECT: Your Wish
  CWD: .
  EVIDENCE: automatic-evidence=v1; definition-sha256=ff3ea7ae1cd3eb062fe6bf134591d2631cb7ded7eecd006bd383839d1d1bcd4d; exit=0; EXPECT=matched; output-sha256=268cbb5073737feb45fd7c95705f7550d39e8bee6e9903da3427661765674a30; output-bytes=67; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/your-wish-book; path=7f4fb4b02918/15 entries
