# Gates: Christmas Fridge Magnets, plan stage

OWNS: ugc/xmas-fridge-magnets/**

Scope: Grace's Christmas Fridge Magnets toddler-activity video, from plan to approved cut V2 in Drive, within the approved budget.

- [x] G1: script gate passes on the current script and proofs
  CHECK: python3 grace/gate.py ugc/xmas-fridge-magnets
  EXPECT: GATE OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=0280914e1a461c40c42cc82092a4762021955927ee5637bb2b6910e6d832c48f; exit=0; EXPECT=matched; output-sha256=548fbc3b6d084a6fe9ea222429ff96a13d3c940d9e91c7e4882fc2c0452f6fcb; output-bytes=86; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G2: every still and clip prompt lints clean
  CHECK: python3 grace/prompt_check.py lint ugc/xmas-fridge-magnets/shots.json
  EXPECT: PROMPT_LINT_OK
  CWD: ../..
  EVIDENCE: automatic-evidence=v1; definition-sha256=54b3157e9311e34635b27e10bfd7723cde19d56d032a4ca1ed954e321c4c4145; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld; path=7f4fb4b02918/15 entries

- [x] G3: BOOK.md names the review page it was sent on and one TOTAL line
  CHECK: python3 gates_check.py book
  EXPECT: BOOK_FIELDS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3420b88a24aab452630900d4d0828d3dbd2afae7c30873692487f81c2d1d81d2; exit=0; EXPECT=matched; output-sha256=3dc7ff65def97536618efa6c7ecbdc626d86b75f2bf08d7e9f21def7509d3a17; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/xmas-fridge-magnets; path=7f4fb4b02918/15 entries

- [x] G4: Kie spend on the job stays within the approved book total ($4.66)
  CHECK: python3 gates_check.py spend
  EXPECT: SPEND_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2e71bb4188b796aa1b30c6c5e205a8fdc3fb82e6577e32659c64c630fb920d97; exit=0; EXPECT=matched; output-sha256=82591f215d7e770e63e5d0b1697dcae92c675ce5776454cbec7c5298c9ace4e9; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/xmas-fridge-magnets; path=7f4fb4b02918/15 entries

- [x] G5: Ralph was notified (push + email) and asked with tap questions at every stop
  EVIDENCE: 2026-11-07 push + email (Gmail ids 1a1b750357e56309, 1a1b755ffd643d45, 1a1b764864db7a3b, 1a1b7722755ed5d3, 1a1b78c1f26760ce) and tap questions at every stop; the push tool loaded only after the restart, so the first two notices were email only

- [x] G6: Grace's Telegram photo is in Drive "Telegram Assets (Azariah)" with the same size and an index line
  EVIDENCE: 2026-11-07 Drive file 1qJ8UPV10P5SCWUVKIxhjEFpsXuwDm06V size 107787 = local 107787; README - asset index.txt updated

- [x] G7: approved cut V2 is in the product's Drive folder with the same size as the local delivery file, and Grace and Ralph were told on Telegram
  EVIDENCE: 2026-11-07 Drive 1Yzvqx0Lo3eK3qZPuptQlk29K-m03nsm0 size 20316162 = local cut/v2_deliver.mp4 20316162; Telegram group msg 222 (Grace), Ralph msg 223 with done + checkmark
