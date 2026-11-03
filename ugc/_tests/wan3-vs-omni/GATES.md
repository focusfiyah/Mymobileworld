# Gates: Wan 3.0 vs Omni test (ZYTRELL S3), 2026-11-03

- [ ] G1: one Wan 3.0 clip downloaded, 9:16, at least 4.5 s
  CHECK: python3 -c "import subprocess as s;o=s.run(['ffprobe','-v','error','-show_entries','stream=width,height:format=duration','-of','csv=p=0','S3_wan3.mp4'],capture_output=True,text=True).stdout.split();w,h=map(int,o[0].split(','));d=float(o[1]);print('CLIP_OK' if abs(w/h-9/16)<0.02 and d>=4.5 else 'BAD')"
  EXPECT: CLIP_OK
- [ ] G2: Kie billed no more than the $0.40 Ralph OK'd
  CHECK: python3 -c "import json;L=json.load(open('kie_log.json'));u=[e['usd'] for e in L if 'usd' in e];print('COST_OK' if u and sum(u)<=0.40 else 'OVER')"
  EXPECT: COST_OK
- [ ] G3: side-by-side sheet (still, Omni, Wan at the same times) and 2x label crops exist
  CHECK: python3 -c "import os;print('SHEET_OK' if all(os.path.getsize(f)>10000 for f in ['compare.png','label_2x.png']) else 'NO')"
  EXPECT: SHEET_OK
- [x] G4: review page published with both clips playable and the verdict
  MANUAL: Artifact URL in README.md
  EVIDENCE: https://claude.ai/artifact/BqEPDXFux8jH7489HiA525 published v2 2026-11-03, both clips play (mp4 files in the publish)
- [x] G5: I looked at every frame (strip) of the Wan clip at 2x for label, grip, flip, hand edges; findings in README.md
  MANUAL: README.md "QC" section filled
  EVIDENCE: all_frames.png (30 frames at 6 fps), edges_2x.png, label_2x.png read 2026-11-03; findings in README.md QC
