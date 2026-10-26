# GATES: Ralph AI avatar test (2026-10-26)

Request: Ralph's face (his real photo) + his cloned voice, one ~15 s test on fal H3 Max 768p and Kie Kling AI Avatar Standard, $1.80 approved ("My face, test OK").

- [ ] G1: the voice line is Ralph's clone, 5 to 15 s long
  CHECK: python3 -c "import subprocess as s;d=float(s.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0','vo/line.mp3']));print('VO_OK' if 5<=d<=15 else 'VO_BAD',d)"
  EXPECT: VO_OK
- [ ] G2: Ralph's photo is in in/ and is a real photo he sent (manual: his upload, not generated)
- [ ] G3: both test videos exist, each within 0.5 s of the voice length and with an audio track
  CHECK: python3 check.py
  EXPECT: CLIPS_OK
- [ ] G4: QC at 2x on face edges + first second, mouth moves on every spoken frame (manual, contact sheet in out/)
- [ ] G5: AI finish applied to both review copies (out/*_final.mp4)
  CHECK: python3 -c "import glob;f=glob.glob('out/*_final.mp4');print('FINISH_OK' if len(f)==2 else 'FINISH_MISSING',f)"
  EXPECT: FINISH_OK
- [ ] G6: spend measured and at or under $1.80 + nothing posted anywhere (manual: spend.json other + Kie billed)
- [ ] G7: review page with both videos playable sent to Ralph + push + email
