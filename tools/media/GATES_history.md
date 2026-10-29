# Gates: Mymobileworld git history cleanup (Ralph 2026-10-29: "Go ahead with the cleanup")

- [ ] H1: Every media version that lived only in git history is in Drive with a verified sha256
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py check
  EXPECT: HISTORY_STORED
- [ ] H2: A fresh clone from GitHub carries no job media in any branch's history and is under 1 GB
  CHECK: python3 /home/user/Mymobileworld/tools/media/history.py fresh-clone-check
  EXPECT: FRESH_CLONE_OK
- [ ] H3: Main's files after the cleanup equal main's files before it, media aside
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py same-files
  EXPECT: SAME_FILES_OK
- [ ] H4: Every branch on GitHub before the cleanup is still there afterwards with the same non-media files
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/history.py branches-kept
  EXPECT: BRANCHES_KEPT
- [ ] H5: branch_sync.py refuses to merge a branch that still carries the old history
  CHECK: cd /home/user/Mymobileworld && python3 handoff/tests/test_old_history.py
  EXPECT: OLD_HISTORY_GUARD_OK
- [ ] H6: This session's disk has at least 20 GB free afterwards
  CHECK: python3 -c "import shutil;f=shutil.disk_usage('/').free/1e9;print('FREE20_OK' if f>=20 else f)"
  EXPECT: FREE20_OK
- [ ] H7: Brain updated
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "history cleanup,Repo media"
  EXPECT: BRAIN_OK
