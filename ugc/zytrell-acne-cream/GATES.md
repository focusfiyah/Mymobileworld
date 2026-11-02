# GATES: ZYTRELL round 1 (plan + scripts)

- [x] G1: Script gate passes
  CHECK: cd ../.. && python3 grace/gate.py ugc/zytrell-acne-cream 2>&1 | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=03168cf902b975c2ac21ca919f514b2c8b635852b9670a91f3f0dc93bf56fda5; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G2: Both scripts read at grade 6 or lower
  CHECK: python3 -c "import re;t=open('research/readability.txt').read();g=[float(x) for x in re.findall(r'Grade level \(Flesch-Kincaid\): ([0-9.]+)',t)];print('READ_OK' if len(g)>=3 and max(g)<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=cd8c03ecf56c6bd29a2859ee7521f082f9fd2b2c78230a0096e4801d939ab8fb; exit=0; EXPECT=matched; output-sha256=11d87cbabaadd62346b73d15820a1b3a06f11255158bcbe1bb83f5d2c69f6aa3; output-bytes=24; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G3: Each script is <=41 words (fits ~12 s at 3.3 w/s)
  CHECK: python3 -c "L=open('research/v1_script.txt').read().split(chr(10));n=[len(l.split()) for l in L if l.strip()];print('LEN_OK' if n and max(n)<=41 else 'LEN_FAIL',n)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ca9a67aad7ea735c68c038921d2d0fe43aa978eb2d9fdf7d05fee6f321403e01; exit=0; EXPECT=matched; output-sha256=6759ac6bd38227373cc681ab00fdf054beeee816f44ae6b0d021f4a6b25beaeb; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G4: Book has the sent link and a TOTAL
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/artifact/' in t and '1.887' in t.split('TOTAL:')[-1] else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e29da0b5ea34478eaeede41f9053587fe4c74c2639b6fb331703fc704ff4bc0b; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G5: Close line and no banned words in scripts
  CHECK: python3 -c "t=open('scripts.md').read().lower();bad=[w for w in ['order it now','reviewer','the label says','$'] if w in t];print('WORDS_OK' if not bad and t.count(\"it's in the orange cart\")==2 else ('WORDS_FAIL',bad))"
  EXPECT: WORDS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=71614b2701ded256d71d2abd5560bef4d2d26c594d97a72af648a792ef1dcf6f; exit=0; EXPECT=matched; output-sha256=98ccd398ae5865a23676830a5587ef144b4d896b43e8cff818ec99c2b9eb6c98; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
