# Gates: repo media to Google Drive (Ralph 2026-10-29)

- [ ] G1: Mymobileworld: no media tracked, every media file recorded in Drive with a verified sha256
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check
  EXPECT: MEDIA_OK
- [ ] G2: Dayone-ai: same
  CHECK: cd /home/user/Dayone-ai && python3 /home/user/Mymobileworld/tools/media/media.py check
  EXPECT: MEDIA_OK
- [ ] G3: New media can't be committed by accident (ignore rule works on a fresh path)
  CHECK: cd /home/user/Mymobileworld && git check-ignore -q ugc/newjob/out/x.mp4 && git check-ignore -q grace/voice/y.wav && ! git check-ignore -q .claude/skills/a/b.png && echo IGNORE_OK
  EXPECT: IGNORE_OK
- [x] G4: A restore from Drive works: one unit downloaded, every file's sha256 matches (manual: output of media.py get)
- [ ] G5: Disk freed: at least 12 GB free in this session
  CHECK: python3 -c "import shutil;f=shutil.disk_usage('/').free/1e9;print('FREE_OK' if f>=12 else f)"
  EXPECT: FREE_OK
- [ ] G6: Rule saved in the rule files and handoff memory (both repos)
  CHECK: cd /home/user && grep -l "media.py" Mymobileworld/CLAUDE.md Dayone-ai/CLAUDE.md Mymobileworld/handoff/GLOBAL_MEMORY.md Mymobileworld/handoff/MEMORY_SHORT.txt Mymobileworld/handoff/CLAUDE_PREFERENCES.txt Mymobileworld/handoff/REMEMBER_ME.txt Dayone-ai/handoff/GLOBAL_MEMORY.md | wc -l
  EXPECT: ^7$
- [ ] G7: Both repos' main carry the change
  CHECK: cd /home/user/Mymobileworld && git fetch -q origin main && git ls-tree origin/main media-in-drive/config.json tools/media/media.py | wc -l
  EXPECT: ^2$
- [x] G8: Live rules doc refreshed (manual: live_rules.py output)
- [ ] G9: Brain updated
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "media in drive,Repo media"
  EXPECT: BRAIN_OK

## Evidence
- G4 2026-10-29: `media.py get ralph/dfy-service links.json` -> "ralph/dfy-service: 18 files restored and checked" (each part and file sha256 matched).
- G8 2026-10-29: new doc 1JcU19geIHkqcv7dkRqj0rFaIpfGDcMhkYmC_5i0PavM read back: 24,943 chars, contains "Media in Drive, not git". The old doc 1zfT... could not be trashed (declined), so two docs share the title.
