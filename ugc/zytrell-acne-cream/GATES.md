# GATES: ZYTRELL round 1 (plan + scripts)

- [x] G1: Script gate passes
  CHECK: cd ../.. && python3 grace/gate.py ugc/zytrell-acne-cream 2>&1 | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=03168cf902b975c2ac21ca919f514b2c8b635852b9670a91f3f0dc93bf56fda5; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G2: Both scripts read at grade 6 or lower
  CHECK: python3 -c "import re;t=open('research/readability.txt').read();g=[float(x) for x in re.findall(r'Grade level \(Flesch-Kincaid\): ([0-9.]+)',t)];print('READ_OK' if len(g)>=3 and max(g)<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=cd8c03ecf56c6bd29a2859ee7521f082f9fd2b2c78230a0096e4801d939ab8fb; exit=0; EXPECT=matched; output-sha256=11d87cbabaadd62346b73d15820a1b3a06f11255158bcbe1bb83f5d2c69f6aa3; output-bytes=24; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G3: Each script is <=34 words (fits 10-11 s at 3.3 w/s)
  CHECK: python3 -c "L=open('research/v1_script.txt').read().split(chr(10));n=[len(l.split()) for l in L if l.strip()];print('LEN_OK' if n and max(n)<=34 and len(n)==1 else 'LEN_FAIL',n)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=26c6d1cdbd036b3ae6bba6e46da18c11f7e24265a41741f191a563413a458ae9; exit=0; EXPECT=matched; output-sha256=8e5f601e6d16d11adfd523797cf8a0986b430fd69659c13897bcdabbdd1f4ae4; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G4: Book has the sent link and a TOTAL
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/artifact/' in t and '1.887' in t.split('TOTAL:')[-1] else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e29da0b5ea34478eaeede41f9053587fe4c74c2639b6fb331703fc704ff4bc0b; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G5: Close line and no banned words in scripts
  CHECK: python3 -c "t=open('scripts.md').read().lower();bad=[w for w in ['order it now','reviewer','the label says','$'] if w in t];print('WORDS_OK' if not bad and t.count(\"it's in the orange cart\")==2 else ('WORDS_FAIL',bad))"
  EXPECT: WORDS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=71614b2701ded256d71d2abd5560bef4d2d26c594d97a72af648a792ef1dcf6f; exit=0; EXPECT=matched; output-sha256=98ccd398ae5865a23676830a5587ef144b4d896b43e8cff818ec99c2b9eb6c98; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G6: All 10 prompts pass the prompt lint
  CHECK: python3 ../../grace/prompt_check.py lint shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=07a95a46b40cb6de9f4fef1fb408028b9367814cc51eed67b882e882415f04b7; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G7: Every reference the prompts name exists on disk
  CHECK: python3 -c "import json,os;s=json.load(open('shots.json'))['shots'];m=[r for x in s for r in x['still_refs'] if not os.path.exists(r)];print('REFS_OK' if len(s)==5 and not m else ('REFS_MISSING',m))"
  EXPECT: REFS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a5c3602e3ba72646f26e7ebe443318e7635c0bea4ae07d2f09f65e895c0f3bf9; exit=0; EXPECT=matched; output-sha256=2f575726671e2a7928635cea0175d39a9c81b723764725a004f68f3b1c05b071; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
- [x] G8: Book carries Kie-only clips, script A only, and the hand question
  CHECK: python3 -c "t=open('BOOK.md').read();ok='Flow' not in t.split('## 6.')[1].split('## 7.')[0] and 'B (H112)' not in t and 'WITHOUT the bracelet' in t;print('BOOK2_OK' if ok else 'BOOK2_FAIL')"
  EXPECT: BOOK2_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8d5adbba22a0ad667fbff72b2343a9bc4eb6cb8991b2687bef2f1562d3f443a9; exit=0; EXPECT=matched; output-sha256=a67d4f12940cc1cd973f0313681f81778cdf1962ab23154b2471b811532e0735; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/zytrell-acne-cream; path=7f4fb4b02918/15 entries
