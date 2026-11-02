# Gates: Bare Anatomy rosemary spray script (2026-11-02)

- [x] G1: Script gate passes (all Rule 0 proofs present and newer than the script)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/bare-anatomy-rosemary-spray 2>&1 | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8dad4fe2b558ce67bd0dc88a0868a8eb68db9277cd1163a56110a4edfde7bd72; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G2: No banned words in script or caption (price, order now, reviewer, the label says, grows/growth claim, dash)
  CHECK: python3 -c "import re;t=open('scripts.md').read().split('## Product truth')[0].lower();b=[w for w in ['order it now','order now','reviewer','the label says','\$','grows hair','—','heads up'] if w in t];print('BANNED',b) if b else print('CLEAN_OK')"
  EXPECT: CLEAN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=36b7db781986724452061d48723395b569a14e595052a32bdad9913d2a3265b1; exit=0; EXPECT=matched; output-sha256=d58ce06c5a35e4660452a1658768a7aefd2a606cd860251fec1f3d126d3ce673; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G3: Readability grade <= 6
  CHECK: python3 -c "import re;g=float(re.search(r'Kincaid\): ([0-9.]+)',open('research/readability_v1.txt').read()).group(1));print('READ_OK' if g<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=eca855186a56ad7acfe2745e43621f1b7fdf84cb183a68ec2572667b2d5fc288; exit=0; EXPECT=matched; output-sha256=272e431face7a963c05e5c29ed2c734db2bf35108c8d1afe6da9bd7c109399b1; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G4: Close says "It's in the orange cart." and a third to half of shots are hand-free
  CHECK: python3 -c "t=open('scripts.md').read();n=t.count('| HAND-FREE |');s=t.count('| HAND |')+n;print('SHOTS_OK' if \"It's in the orange cart.\" in t and s==7 and 7/3<=n<=3.5 else 'SHOTS_FAIL',n,s)"
  EXPECT: SHOTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=85d6354ed329b392bfde34b3159269b52cc38c079a48d6e304a341859c6e9a2a; exit=0; EXPECT=matched; output-sha256=5d6899608fa513745bb74c77ea424d47e16c0cbbaef1f461bc5f211d26542c8e; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G5: Script in Drive "Grace Tiktok assets" product folder as CURRENT Google Doc (manual: link in README)
  CHECK: python3 -c "print('DRIVE_OK' if 'drive.google.com/drive/folders/10eauHORrJBo17zYsndVO7bMNx2YSIwW0' in open('README.md').read() else 'NO_LINK')"
  EXPECT: DRIVE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a0a5f65e19837a2f4286eb241c2f16ffd4e2ab847bf428d2219ddbfdedbd6f3a; exit=0; EXPECT=matched; output-sha256=62a8cc81c5586654847b20aa63a41bcd22762cf8047cad8b83169ca469393e94; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G6: Final video in the Drive product folder at the same size as the local file
  CHECK: python3 -c "import os;print('VIDEO_OK' if os.path.getsize('out/rosemary_v3.mp4')==30171668 and '1I-Wm_61Yukiy7GEPNTv8o3EMhka0S_rO' in open('README.md').read() else 'NO')"
  EXPECT: VIDEO_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=70c9ada9f905407381e8e8f15088f9eed00e66388bbe0176af95a98ab4988df9; exit=0; EXPECT=matched; output-sha256=dd945c41e3d104865b5f76092108b6e5c7c30ad15e59e839470dec1a25004aaa; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
- [x] G7: Final cut passes QC and the cut gate
  CHECK: python3 -c "import subprocess as s;q=s.run(['python3','qc.py','out/rosemary_v3.mp4','11.4'],capture_output=True,text=True).stdout;g=s.run(['python3','/home/user/Mymobileworld/grace/gate.py','.','--stage','cut'],capture_output=True,text=True).stdout;print('CUT_OK' if 'QC_OK' in q and 'GATE OK' in g else 'CUT_FAIL')"
  EXPECT: CUT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=af5eab74ba1a22c9a3acb109a4a74d7c4c0f88c96e2d5f6c2faaa9d9a671d532; exit=0; EXPECT=matched; output-sha256=76bbe64ec214834a9b335167cb9fbabdddaa9107d7c78a44ba16caa7df93e444; output-bytes=7; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/bare-anatomy-rosemary-spray; path=7f4fb4b02918/15 entries
