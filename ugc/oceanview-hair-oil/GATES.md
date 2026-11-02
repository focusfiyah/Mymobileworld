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
