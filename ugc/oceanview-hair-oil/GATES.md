# Gates: Ocean View hair oil, plan stage (2026-11-02)

- [x] G1: Script gate passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/oceanview-hair-oil 2>/dev/null | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b9f691e73d43f170ede2ee257e851e21da02a951ba58edb80fbf34e3e9d2c0a4; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G2: Every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/oceanview-hair-oil/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=63ba5a95050093c70f2e2d25641af277cf10d3ec3bbca6507245c707d738ca7a; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G3: VO script reads at grade 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Kincaid\): ([0-9.]+)',open('research/readability_v1.txt').read()).group(1));print('READ_OK' if g<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=eca855186a56ad7acfe2745e43621f1b7fdf84cb183a68ec2572667b2d5fc288; exit=0; EXPECT=matched; output-sha256=614ee3f2a82e15070b283b907d301650a68c9dd332fae9e14c9d29e7790f94ea; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G4: 7 shots, 3 hand-free, orange cart close, no banned words
  CHECK: python3 -c "t=open('scripts.md').read();n=t.count('| HAND-FREE |');s=t.count('| HAND |')+n;b=[w for w in ['order it now','order now','reviewer','the label says','\$','grows hair','—','heads up'] if w in t.split('## Product truth')[0].lower()];print('SHOTS_OK' if s==7 and n==3 and \"It's in the orange cart.\" in t and not b else 'SHOTS_FAIL',n,s,b)"
  EXPECT: SHOTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b604e80374e2f066d83a85e9f8405a9f38525bbcfb339db530e160c3f76bf22b; exit=0; EXPECT=matched; output-sha256=f2098d24249bc3631150f6e112a4a99a1c634a4b138d921868dc009a253a2208; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G5: Production Book has the Sent to Ralph line and one TOTAL
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/artifact/' in t and t.count('TOTAL: \$')==1 else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3ce9514d46962aba74a0765818b7b61ff6ff52361a5c5e0415d8b5b1465ae9a5; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G6: Drive product folder linked in README
  CHECK: python3 -c "print('DRIVE_OK' if 'drive.google.com/drive/folders/1UcHmH5IGzz-9Awtd-eh04Mjaahtwa1gO' in open('README.md').read() else 'NO_LINK')"
  EXPECT: DRIVE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0039b9902f2fb054879b004e2ae2f0967ce2bbe063d12d744960471540d9f5ad; exit=0; EXPECT=matched; output-sha256=62a8cc81c5586654847b20aa63a41bcd22762cf8047cad8b83169ca469393e94; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G7: Job media packed to Drive, none in git
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check 2>&1 | tail -1
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8b9331d7941d07cafa9ffcedf9d561dcc8860509350068ce0d571402a5c6c2a2; exit=0; EXPECT=matched; output-sha256=8083bc5e3d38fc4812679011f657b4c749435c73ae3358ae5426effe963edf5b; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G8: Final cut is 10-12 s, 1080x1920, with audio
  CHECK: python3 -c "import subprocess,json;d=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration:stream=codec_type,width,height','-of','json','cuts/v2.mp4'],capture_output=True,text=True).stdout);s=d['streams'];t=float(d['format']['duration']);v=[x for x in s if x['codec_type']=='video'][0];print('CUT_OK' if 10<=t<=12 and v['width']==1080 and v['height']==1920 and any(x['codec_type']=='audio' for x in s) else 'CUT_FAIL',t)"
  EXPECT: CUT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3d93ca2031e34aad9ceba1b4a66f4d9c05f31344801402c940cd43ac72d9ad64; exit=0; EXPECT=matched; output-sha256=5850d7bd3f651d6ac8f082eb237f9d6dd2224eac4686707f307ad126e7a2c4b6; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G9: Cut-stage gate passes (compare proof, no text overlay)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/oceanview-hair-oil --stage cut 2>/dev/null | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=637f0ed0ae71efc3344f666f34e1e2bef45bea3c706dc6dda318ed91acd36c8d; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G10: Job spend is within the approved allowance ($3.90)
  CHECK: cd /home/user/Mymobileworld && python3 grace/spend.py 2>/dev/null | python3 -c "import sys,re;m=re.search(r'oceanview-hair-oil\s+\\$\s*([0-9.]+)',sys.stdin.read());v=float(m.group(1));print('SPEND_OK' if v<=3.90 else 'SPEND_OVER',v)"
  EXPECT: SPEND_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=19f18562afe3478e502ef1d6b3246e28b0590815d0d801884091a6c1a6f66925; exit=0; EXPECT=matched; output-sha256=7abdd26035cb8193a2ff6e58597dac4b803d7cf61614dc30d6c2df40787953ed; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
- [x] G11: Final cut in the Drive product folder (Ralph approved v2; Drive file 1Ug1BA3ikFa6vUEb4DvjSPxPlvTiR7I1d, 67208902 bytes, matches local)
  CHECK: python3 -c "import os;print('DRIVE_SIZE_OK' if os.path.getsize('cuts/v2.mp4')==67208902 and 'CURRENT - Juice Boost Oil V2.mp4' in open('README.md').read() else 'FAIL')"
  EXPECT: DRIVE_SIZE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0751ae676240f9c2d9538d39db89cdcfa1877cb8e7c54c7feb520cfa46bd2884; exit=0; EXPECT=matched; output-sha256=6b6b4213fd3cf2fae49bc836f97e01b7784799ec3be4943c17baf5191251ac50; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/oceanview-hair-oil; path=7f4fb4b02918/15 entries
