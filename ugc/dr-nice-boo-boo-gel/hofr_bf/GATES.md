# Boo-Boo Gel HofR Black Friday cut (Ralph 2026-11-12): 15 s+, Chatterbox VO, extra real b-roll, $0

- [x] G1: Final cut is 15.0 s or longer (aim 16-18 s)
  CHECK: python3 -c "import subprocess;d=float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','out/bf_boo_boo.mp4'],capture_output=True,text=True).stdout);print('LEN_OK' if 15.0<=d<=19.0 else 'LEN_BAD',d)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7ae20bbc56b1a81a0cb749ae27ea1abd7123090d81aeb939977c5cea80950abc; exit=0; EXPECT=matched; output-sha256=4ddb68009f1a59ca20e1896ecff4de4832bb37aade2044848e3289b48f3bb2fb; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G2: Hook card whole in frame 0, held 2 s+, inside the safe zone
  CHECK: python3 ../../../tools/hookcheck/hook_check.py out/bf_boo_boo.mp4 --hook 170,420,740,190
  EXPECT: HOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f887d697b840708254c5963ff69c50955e8a4b57af5c184d6c7b1726b91f155d; exit=0; EXPECT=matched; output-sha256=67f89366a851021f69e5bad985872fa3d739a9721fdb0bf8d2ac267ea64e315a; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G3: 1080x1920, 30 fps, AAC audio present
  CHECK: python3 qc.py size out/bf_boo_boo.mp4
  EXPECT: SIZE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0b21b9b305dbb2107930ce26428ba55d7aad9a896df04aebad69dfc29a659140; exit=0; EXPECT=matched; output-sha256=b9388d79c6749b01567dbb7828a659c02a165ec76ee846b2928cf38d3b67fc5e; output-bytes=31; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G4: Loudness between -16 and -13.5 LUFS
  CHECK: python3 qc.py lufs out/bf_boo_boo.mp4
  EXPECT: LUFS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5466cd386268f8c18b0d5fc9c8f8ca43db198912532a35463bb8fc7a49571027; exit=0; EXPECT=matched; output-sha256=a99102f8db2674dfea8c47b572f601b65d3b06718f0e54658cd29f041b1cf731; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G5: Every VO line heard word for word by faster-whisper (no ElevenLabs used)
  CHECK: python3 qc.py words
  EXPECT: WORDS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=71332e58aa9d1780df5a09cb2bd12f1525792464ee3624d50d9113de7e46fe40; exit=0; EXPECT=matched; output-sha256=c597d68a9fd0df6cd740d4abb24068423ae0017e56e573fc5d7fe626758a225d; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G6: No frozen frames (no run of identical frames over 0.3 s)
  CHECK: python3 qc.py freeze out/bf_boo_boo.mp4
  EXPECT: FREEZE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2f9dc6809edb08bc6c4df76a63f18a5f19692a4953c44d33f738e125636dc639; exit=0; EXPECT=matched; output-sha256=c2f5d837bb34fcbf1504277035e53bc825642d02bd0b351e0e02eb990c448016; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G7: Every shot starts on its line's first word (within 0.15 s) and no clip is stretched (cut.py asserts)
  CHECK: python3 qc.py sync
  EXPECT: SYNC_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=89c3d951de435a4aa1d1958fc8d31517dbe5d1476fde315d7ea30d02ed3db73c; exit=0; EXPECT=matched; output-sha256=8a966c950c4950bf641ee0c455d3ac42cc1621832b7de309a7694b82976edf67; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G8: Every b-roll clip logged in broll/SOURCES.md with its Pexels page
  CHECK: python3 qc.py sources
  EXPECT: SOURCES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0a3f88cf4e75d13988e5e9c8c2cbe20e0655c7711507d160efced71ef45f8875; exit=0; EXPECT=matched; output-sha256=3a748049512382d6df3be04734b42d9760bdad48091382c2f71a86b53f0734d4; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/dr-nice-boo-boo-gel/hofr_bf; path=7f4fb4b02918/15 entries
- [x] G9: (manual) frame sheet looked at; 2x on hand/skin edges; gel lands ON the scrape; REMOVED.md (S3_seedance_r1 gel-beside-scrape take never used); bright neutral; no captions
  EVIDENCE: 2026-11-12 looked at 40-frame sheet (0.5 s steps) + 2x crops at 0.03/1.3/7.6 s: gel dot sits ON the scrape and is dabbed along it, finger and knee edges clean (no halo/smear); cut.py never loads S3_seedance_r1; bright daylight grade; hook card only in shot 1, no captions
- [ ] G10: (manual) review page published (video full width), push + email sent, then STOP for Ralph
- [ ] G11: (manual, after Ralph OK) Drive "HofR - Boo-Boo Gel BF.mp4" size = local, hub session messaged, code merged, Brain note + BRAIN_OK
