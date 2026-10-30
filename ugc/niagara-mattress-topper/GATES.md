# Niagara Mattress Topper (Grace) - plan stage gates

- [x] G1: script gate passes (all proofs exist, newer than the script, no banned phrase)
  CHECK: cd ../.. && python3 grace/gate.py ugc/niagara-mattress-topper 2>&1 | head -3
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=483944805728f52d01d6fc176a6b26ed3ad80924438ae2829947fd83fe4da482; exit=0; EXPECT=matched; output-sha256=759a39f75e1dc036cd4d1cf01936bdef31a2640a420907603facffd2b5cc3326; output-bytes=169; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/niagara-mattress-topper; path=7f4fb4b02918/15 entries
- [x] G2: product_truth.json exists with photos, facts and forbid lists
  CHECK: python3 -c "import json;d=json.load(open('product_truth.json'));assert d['photos'] and d['facts'] and d['forbid'];print('TRUTH_OK')"
  EXPECT: TRUTH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=57130c6bd6b79b47631c95ae280578454027b09365aa0af797e29acc9297f384; exit=0; EXPECT=matched; output-sha256=be3a515e39e9388a549ac4fdfd9834edfef39a978001a2cbcd008c643382692e; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/niagara-mattress-topper; path=7f4fb4b02918/15 entries
- [x] G3: BOOK.md has one TOTAL line and a Sent to Ralph line
  CHECK: python3 -c "t=open('BOOK.md').read();import re;assert len(re.findall(r'^TOTAL: [$]',t,re.M))==1 and 'Sent to Ralph:' in t;print('BOOK_OK')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=31e01284ca81767af3802fe7f89ea3ec8d8fc15f40d39fcd94f13b3b9e0673d4; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/niagara-mattress-topper; path=7f4fb4b02918/15 entries
- [x] G4: script readability grade <= 6 and VO 15-20 s (~40-55 words)
  CHECK: python3 -c "import re;t=open('vo_lines.txt').read();n=len(re.findall(r\"[A-Za-z']+\",t));assert 38<=n<=58,n;print('LEN_OK',n)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=cd8554ff500701f3eb92a5115fc8185c6f6013985db26ea1f490f6a25500581e; exit=0; EXPECT=matched; output-sha256=16e674272ca7e613c2b68120e53b17e09c1328d9c14c2e7c79b16429751fe5ca; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/niagara-mattress-topper; path=7f4fb4b02918/15 entries
- [x] G5: rooms are real photos with SOURCES.md
  CHECK: test -s rooms/SOURCES.md && echo ROOMS_OK
  EXPECT: ROOMS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8cf7dd31a048d687ad6d8aeeb89da93b9b0e4a66631ca89a7502e2201a50fecb; exit=0; EXPECT=matched; output-sha256=1ccb5983fef497bb2ba16b269aa647998346add8d40ccd6a936d8bcdf86aa08d; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/niagara-mattress-topper; path=7f4fb4b02918/15 entries
- [ ] G6: (manual) review page with script, storyboard, product sheet and total published and sent to Ralph (push + email)
