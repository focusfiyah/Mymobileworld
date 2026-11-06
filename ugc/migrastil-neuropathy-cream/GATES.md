# Gates: Migrastil Neuropathy Cream, plan stage (2026-11-06)

Ask (Grace, Telegram group 2026-11-06; Ralph tapped music only + VO script): a 12-15 s music-only AI product video for Grace (no VO, she adds music) + a standard-length
(~30 s) VO script she can record later. Plan only: no paid call before Ralph approves BOOK.md.

- [x] G1: Script gate passes (audience, RESEARCH.md, coach, viral, facts, hooks, humanizer, readability, line sources)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/migrastil-neuropathy-cream 2>/dev/null | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=eb1a97856b71b2a7285cef4f175781a2267b33a1ae51c62650bb3a45042ee706; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G2: product_truth.json lists real photos + forbid, and the free product reference sheet exists
  CHECK: python3 -c "import json,os;d=json.load(open('product_truth.json'));print('TRUTH_OK' if len(d.get('photos',[]))>=2 and len(d.get('forbid',[]))>=3 and os.path.getsize('refs/product_sheet.png')>50000 else 'TRUTH_FAIL')"
  EXPECT: TRUTH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=bcfb0be4c221118cac2f374a50900d397c8d2978573321de3069a4ef040708d6; exit=0; EXPECT=matched; output-sha256=be3a515e39e9388a549ac4fdfd9834edfef39a978001a2cbcd008c643382692e; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G3: Every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/migrastil-neuropathy-cream/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=920e3d4c956d9790f52c5d58e2864820576a4d5967747a122105aca1ca22909c; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G4: VO script reads at grade 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Kincaid\): ([0-9.]+)',open('research/readability_v1.txt').read()).group(1));print('READ_OK' if g<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=eca855186a56ad7acfe2745e43621f1b7fdf84cb183a68ec2572667b2d5fc288; exit=0; EXPECT=matched; output-sha256=e0a3d4619a331a789985d4ce0110f024a925903eb38d1985e993804aa9f34373; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G5: Script closes in the orange cart, no banned words, 25-40 s of words at 3.0-3.6 w/s
  CHECK: python3 -c "import re;t=open('scripts.md').read().split('## VO script')[1].split(chr(10)*2)[0].split(chr(10),1)[1];b=[w for w in ['order it now','order now','reviewer','the label says','$','heads up','cure','obsessed','game changer','neuropathy cure','heals nerve'] if w in t.lower()];n=len(re.findall(r\"[A-Za-z']+\",t));print('SCRIPT_OK' if not b and 'orange cart' in t and 75<=n<=125 else 'SCRIPT_FAIL',n,b)"
  EXPECT: SCRIPT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=48bfb98cab753f19ab123e030b4cf9312b9c9b538de5d88630f4523e2a7bd95a; exit=0; EXPECT=matched; output-sha256=bed9a898d2d7268bc24867cd6bd005b2dda1fea72c5b4fc3f479d4e26176235f; output-bytes=17; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G6: 12-15 s shot list, a third to half hand-free
  CHECK: python3 -c "import json;s=list(json.load(open('shots.json')).values());d=sum(x['dur'] for x in s);h=sum(1 for x in s if x['hand']=='HAND-FREE');print('SHOTS_OK' if 12<=d<=15 and len(s)/3<=h<=len(s)/2 else 'SHOTS_FAIL',d,h,len(s))"
  EXPECT: SHOTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3eafd615a9ae4da63415d21092bff64b642166aae86fb01636a0aaf3ae1a7abe; exit=0; EXPECT=matched; output-sha256=7043d1fe9ba6eef1dc74b41cade9f97caaa01fdd75c8d41bf90012900a09d5f1; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [x] G7: Production Book has the Sent to Ralph line and one TOTAL
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/' in t and t.count('TOTAL: $')==1 else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=bd68027b885e853cf19fb9bcdedac0a6948d5f8098f647016414e89ab0ff75c1; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/migrastil-neuropathy-cream; path=7f4fb4b02918/15 entries
- [ ] G8: Job media in Drive, none in git
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check 2>&1 | tail -1
  EXPECT: MEDIA_OK
- [ ] G9: Ralph notified (push + email) and asked with tappable options: manual, evidence = tool results in this session
