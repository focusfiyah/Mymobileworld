# Gates: Mymobileworld git history cleanup (Ralph 2026-10-29: "Go ahead with the cleanup")

- [x] H1: Every media version that lived only in git history is in Drive with a verified sha256
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py check
  EXPECT: HISTORY_STORED
  EVIDENCE: automatic-evidence=v1; definition-sha256=b37f4b6b85d20f2eab5e4d67b6a11baca7d73fd91be3f3585a5f8a22bddf1fcf; exit=0; EXPECT=matched; output-sha256=711901f2df1ec8b422907e2e9645260a8d0fea6e1434a5aa9a986b242fc67de4; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H2: A fresh clone from GitHub carries no job media in any branch's history and is under 1 GB
  CHECK: python3 /home/user/Mymobileworld/tools/media/history.py fresh-clone-check
  EXPECT: FRESH_CLONE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f6e5b0969aa25f76a19d2312c43211b1ffbed6ba32fcd60ddbe11bb8626faeae; exit=0; EXPECT=matched; output-sha256=dbe00c6700b22cdd48e70aa0a55d0469185576f7ddba80d071510065cad20f4b; output-bytes=57; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H3: Main's files after the cleanup equal main's files before it, media aside
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py same-files
  EXPECT: SAME_FILES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5d60ba92d24b17894b166c7d55b1fa0902ce970a2adb85577aa6696c5b39aad4; exit=0; EXPECT=matched; output-sha256=f010a88d4496884e2f1db08c9b7f5107a1730a99b1903f250d3ce244d483cc3b; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H4: Every branch on GitHub before the cleanup is still there afterwards with the same non-media files
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py branches-kept
  EXPECT: BRANCHES_KEPT
  EVIDENCE: automatic-evidence=v1; definition-sha256=7afb94bacebdd8d4283b03ea59784e392720de9596c10707027e34d0c8c890e1; exit=0; EXPECT=matched; output-sha256=90b51de498956a803c7cfb1119602b919c3f79d028c8f1b56a739f60b17c9b29; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H5: branch_sync.py refuses to merge a branch that still carries the old history
  CHECK: cd /home/user/Mymobileworld && python3 handoff/tests/test_old_history.py
  EXPECT: OLD_HISTORY_GUARD_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5d144675a1640069f7104b9b64e6b5668a18626179a462b40be74a5529ad32fb; exit=0; EXPECT=matched; output-sha256=0f6d891805934e35ae6d64b689095cb095a1d26836da398b24284aaca2d8cb21; output-bytes=21; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H6: This session's disk has at least 20 GB free afterwards
  CHECK: python3 -c "import shutil;f=shutil.disk_usage('/').free/1e9;print('FREE20_OK' if f>=20 else f)"
  EXPECT: FREE20_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=298ba24818793756a2115a2b83f7f8af5613232c69f1c4265bbaf78e516212a4; exit=0; EXPECT=matched; output-sha256=00cb1343d5a23e80f14e75a1a7b29183340753fff46607a2a2d51d005e1e2b16; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] H7: Brain updated
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "history cleanup,Repo media"
  EXPECT: BRAIN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9ad50c38c8d010fac79d3fb63915e8c3d4185c1c81d80bfd88ea53d3db04f235; exit=0; EXPECT=matched; output-sha256=6ccf283c559cdacc72ddd15ea722d973e427203a1a5ac0530774fa97c97241e8; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
