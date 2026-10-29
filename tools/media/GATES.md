# Gates: repo media to Google Drive (Ralph 2026-10-29)

- [x] G1: Mymobileworld: no media tracked, every media file recorded in Drive with a verified sha256
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a66385644360a15b9a16b370692a526fbf7beb23b8e8e7572560f8cd98ee8237; exit=0; EXPECT=matched; output-sha256=8083bc5e3d38fc4812679011f657b4c749435c73ae3358ae5426effe963edf5b; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G2: Dayone-ai: same
  CHECK: cd /home/user/Dayone-ai && python3 /home/user/Mymobileworld/tools/media/media.py check
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=11af4fe6b027417a2243acfe5c48d74e7b477da4f405d037abb59b4a1d6cb657; exit=0; EXPECT=matched; output-sha256=8083bc5e3d38fc4812679011f657b4c749435c73ae3358ae5426effe963edf5b; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G3: New media can't be committed by accident (ignore rule works on a fresh path)
  CHECK: cd /home/user/Mymobileworld && git check-ignore -q ugc/newjob/out/x.mp4 && git check-ignore -q grace/voice/y.wav && ! git check-ignore -q .claude/skills/a/b.png && echo IGNORE_OK
  EXPECT: IGNORE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8eca6c11e19cfd63669cbc916f7e66ef4dccd2550dead8095e45aaebbb8341ce; exit=0; EXPECT=matched; output-sha256=ebf3473580307752f02f0e46f927e0272d0ad023b493de0c629a9d99444a9ddc; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G4: A restore from Drive works: one unit downloaded, every file's sha256 matches (manual: output of media.py get)
  EVIDENCE: 2026-10-29 media.py get ralph/dfy-service -> "18 files restored and checked" (every part and file sha256 matched)
- [x] G5: Disk freed: at least 12 GB free in this session
  CHECK: python3 -c "import shutil;f=shutil.disk_usage('/').free/1e9;print('FREE_OK' if f>=12 else f)"
  EXPECT: FREE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9e40111fbfe38df7051cde76863d5d6059ef75f765ab0ee7010773fc0ebd34ef; exit=0; EXPECT=matched; output-sha256=f9a2d1b87d5e1cbb4c877e45c3bad8ecf7abe239d037c355c292475c359a2db7; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G6: Rule saved in the rule files and handoff memory (both repos)
  CHECK: cd /home/user && grep -l "media.py" Mymobileworld/CLAUDE.md Dayone-ai/CLAUDE.md Mymobileworld/handoff/GLOBAL_MEMORY.md Mymobileworld/handoff/MEMORY_SHORT.txt Mymobileworld/handoff/CLAUDE_PREFERENCES.txt Mymobileworld/handoff/REMEMBER_ME.txt Dayone-ai/handoff/GLOBAL_MEMORY.md | wc -l | sed 's/^7$/RULE_SAVED_7/'
  EXPECT: RULE_SAVED_7
  EVIDENCE: automatic-evidence=v1; definition-sha256=282f5d59fc34243561ae84336901665974882357c9b31ed115c28ae7747f21b3; exit=0; EXPECT=matched; output-sha256=78d69d9edb7a1a3620aec9723af3cc260b0d373544c7e35afda422132ae0be60; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G7: Both repos' main carry the change
  CHECK: cd /home/user/Mymobileworld && git fetch -q origin main && git ls-tree origin/main media-in-drive/config.json tools/media/media.py | wc -l | sed 's/^2$/MAIN_HAS_IT/'
  EXPECT: MAIN_HAS_IT
  EVIDENCE: automatic-evidence=v1; definition-sha256=aabeaa5dc063cb612fdeb69430e54845c3ffefd5bcfd7082622ca0e8c25ac7cd; exit=0; EXPECT=matched; output-sha256=436ee501470a978cfca5fb382acf6b5d51196cc76b0895e6f661a435ea04d330; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries
- [x] G8: Live rules doc refreshed (manual: live_rules.py output)
  EVIDENCE: 2026-10-29 new doc 1JcU19geIHkqcv7dkRqj0rFaIpfGDcMhkYmC_5i0PavM read back, 24,943 chars, contains "Media in Drive, not git"
- [x] G9: Brain updated
  CHECK: cd /home/user/Mymobileworld && python3 tools/brain/check.py --terms "media in drive,Repo media"
  EXPECT: BRAIN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9e500771f2849fd0654079e46a73cc2f7c2ff25565bd63ab7c4b5256e25de91a; exit=0; EXPECT=matched; output-sha256=b6f1c923554aa72c27ea1295cae77e512519b27e6b1dce71e23c881bab2d236c; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld/tools/media; path=7f4fb4b02918/15 entries

