# Gates: HofR Black Friday, silent videos A (Mirror, Body Butter, Ear Cam, Coloring Book, Meat Sticks), 2026-11-12

Done = five HofR cuts with Ralph's free Chatterbox VO, each checked, on one review page, Ralph notified. Drive upload and the
hub message happen only after Ralph's OK (gates G9-G10 stay open until then).

- [x] G1: all five Grace source cuts are silent (no audio stream), confirmed before use
  CHECK: python3 -c "import subprocess,sys;fs=['mirror','butter','ear','coloring','meat'];r=[subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0','/tmp/claude-0/src/'+f+'.mp4'],capture_output=True,text=True) for f in fs];sys.exit(0 if all(x.returncode==0 and x.stdout.strip()=='' for x in r) else 1)" && echo SOURCES_SILENT
  EXPECT: SOURCES_SILENT
  EVIDENCE: automatic-evidence=v1; definition-sha256=efede6aa10b7bd3cb797517ba5ead70ce407b09322a840a51c4c5a0d92231b29; exit=0; EXPECT=matched; output-sha256=ad615d8d3598e509da39246843cf52f81c17f5ce40314910c6b0c7bc35f1a67b; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G2: Body Butter cut passes every check (length, size, loudness, HOOK_OK, VO read back, script rules, hook word for word, b-roll logged)
  CHECK: python3 check.py ../bf-butter
  EXPECT: CHECK_OK butter
  EVIDENCE: automatic-evidence=v1; definition-sha256=8e716c9d9710bf16f3423662f09a346438b5d1ccd8c43042d3ced66e2070a64b; exit=0; EXPECT=matched; output-sha256=b2403bb63f7d03b7c116b554ef23cf153f9f23102a40db9aeb5885672df8c76d; output-bytes=43; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G3: Mirror cut passes every check
  CHECK: python3 check.py ../bf-mirror
  EXPECT: CHECK_OK mirror
  EVIDENCE: automatic-evidence=v1; definition-sha256=19040667b36c33e2a468136b7628c71f2f7999e0f103816a6ea9b9b7ad9b5d94; exit=0; EXPECT=matched; output-sha256=bd9da506d5018a9fa07a5eee5715b48ccc03c023fb9b29f561aba695e68429ff; output-bytes=43; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G4: Ear Camera cut passes every check
  CHECK: python3 check.py ../bf-ear
  EXPECT: CHECK_OK ear
  EVIDENCE: automatic-evidence=v1; definition-sha256=f54cf7f6bbc14d70d9f7681b7fce374da032e4e1fe59a31c33bfda79adac2125; exit=0; EXPECT=matched; output-sha256=1f9968ee7bff02f48ae1fc55da3cab8caf29285b165f3d0614370a3654ec7159; output-bytes=37; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G5: Coloring Book cut passes every check
  CHECK: python3 check.py ../bf-coloring
  EXPECT: CHECK_OK coloring
  EVIDENCE: automatic-evidence=v1; definition-sha256=8646d62a5bedbdf8864f5855f3b5763776369e078ea356338c5e91617e91af57; exit=0; EXPECT=matched; output-sha256=6ee5fbfa91384a524ebd5881a4410632965a3940b28351ef3c90be756b645246; output-bytes=47; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G6: Meat Sticks cut passes every check
  CHECK: python3 check.py ../bf-meat
  EXPECT: CHECK_OK meat
  EVIDENCE: automatic-evidence=v1; definition-sha256=4fc2f95e663f6c718f0aafc0b197153f7dbd54474787076175ba8211cd152747; exit=0; EXPECT=matched; output-sha256=361b9134189cef8bfb6237d8c9aa8b5670c11ae2425a4b0554bfd70d669d44b4; output-bytes=39; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf-silent-a; path=7f4fb4b02918/15 entries
- [x] G7: I looked at a frame sheet of every final cut (4 fps) and the 2x first second; notes in QC.md, one line per post
  MANUAL: QC.md lists each post with what was seen
  EVIDENCE: QC.md, 5 lines (2026-11-12)
- [x] G8: one review page with all five videos stacked full width + script under each; push + email sent to Ralph
  MANUAL: page link + push result + Gmail message id in README.md
  EVIDENCE: https://claude.ai/code/artifact/62c62375-ddc3-41a2-b48c-3b93cbcd000f ; Gmail 1a1d1fb6b51cd5f6 ; push tool not in this session (ToolSearch found none)
- [ ] G9: after Ralph's OK, each approved cut is in its product's Drive folder as "HofR - <Product> BF.mp4", Drive size = local size
  MANUAL: file ids + sizes in README.md
- [ ] G10: hub session told one line per approved product; Brain note + session log pushed; Active work line removed; BRAIN_OK
  MANUAL: send_message result + brain check output
