# Gates: HofR Black Friday, silent videos A (Mirror, Body Butter, Ear Cam, Coloring Book, Meat Sticks), 2026-11-12

Done = five HofR cuts with Ralph's free Chatterbox VO, each checked, on one review page, Ralph notified. Drive upload and the
hub message happen only after Ralph's OK (gates G9-G10 stay open until then).

- [ ] G1: all five Grace source cuts are silent (no audio stream), confirmed before use
  CHECK: python3 -c "import subprocess,sys;fs=['mirror','butter','ear','coloring','meat'];r=[subprocess.run(['ffprobe','-v','error','-select_streams','a','-show_entries','stream=index','-of','csv=p=0','/tmp/claude-0/src/'+f+'.mp4'],capture_output=True,text=True) for f in fs];sys.exit(0 if all(x.returncode==0 and x.stdout.strip()=='' for x in r) else 1)" && echo SOURCES_SILENT
  EXPECT: SOURCES_SILENT
- [ ] G2: Body Butter cut passes every check (length, size, loudness, HOOK_OK, VO read back, script rules, hook word for word, b-roll logged)
  CHECK: python3 check.py ../bf-butter
  EXPECT: CHECK_OK butter
- [ ] G3: Mirror cut passes every check
  CHECK: python3 check.py ../bf-mirror
  EXPECT: CHECK_OK mirror
- [ ] G4: Ear Camera cut passes every check
  CHECK: python3 check.py ../bf-ear
  EXPECT: CHECK_OK ear
- [ ] G5: Coloring Book cut passes every check
  CHECK: python3 check.py ../bf-coloring
  EXPECT: CHECK_OK coloring
- [ ] G6: Meat Sticks cut passes every check
  CHECK: python3 check.py ../bf-meat
  EXPECT: CHECK_OK meat
- [ ] G7: I looked at a frame sheet of every final cut (4 fps) and the 2x first second; notes in QC.md, one line per post
  MANUAL: QC.md lists each post with what was seen
- [ ] G8: one review page with all five videos stacked full width + script under each; push + email sent to Ralph
  MANUAL: page link + push result + Gmail message id in README.md
- [ ] G9: after Ralph's OK, each approved cut is in its product's Drive folder as "HofR - <Product> BF.mp4", Drive size = local size
  MANUAL: file ids + sizes in README.md
- [ ] G10: hub session told one line per approved product; Brain note + session log pushed; Active work line removed; BRAIN_OK
  MANUAL: send_message result + brain check output
