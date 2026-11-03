# Gates: Bite Toothpaste Bits, plan stage (2026-11-03)

Ask (Ralph, Telegram 2026-11-03): a 10-12 s music-only product video for Grace (no VO, she adds music) + a standard-length
(~30 s) VO script she can record later. Plan only: no paid call before Ralph approves BOOK.md.

- [ ] G1: Script gate passes (audience, RESEARCH.md, coach, viral, facts, hooks, humanizer, readability, line sources)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/bite-toothpaste-bits 2>/dev/null | head -1
  EXPECT: GATE OK
- [ ] G2: product_truth.json lists real photos + forbid, and the free product reference sheet exists
  CHECK: python3 -c "import json,os;d=json.load(open('product_truth.json'));print('TRUTH_OK' if len(d.get('photos',[]))>=3 and len(d.get('forbid',[]))>=3 and os.path.getsize('refs/product_sheet.png')>50000 else 'TRUTH_FAIL')"
  EXPECT: TRUTH_OK
- [ ] G3: Every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/bite-toothpaste-bits/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G4: VO script reads at grade 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Kincaid\): ([0-9.]+)',open('research/readability_v1.txt').read()).group(1));print('READ_OK' if g<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
- [ ] G5: Script closes in the orange cart, no banned words, 25-40 s of words at 3.0-3.6 w/s
  CHECK: python3 -c "import re;t=open('scripts.md').read().split('## VO script')[1].split(chr(10)*2)[0].split(chr(10),1)[1];b=[w for w in ['order it now','order now','reviewer','the label says','$','heads up','cure','obsessed','game changer'] if w in t.lower()];n=len(re.findall(r\"[A-Za-z']+\",t));print('SCRIPT_OK' if not b and 'orange cart' in t and 75<=n<=125 else 'SCRIPT_FAIL',n,b)"
  EXPECT: SCRIPT_OK
- [ ] G6: 10-12 s shot list, a third to half hand-free
  CHECK: python3 -c "import json;s=list(json.load(open('shots.json')).values());d=sum(x['dur'] for x in s);h=sum(1 for x in s if x['hand']=='HAND-FREE');print('SHOTS_OK' if 10<=d<=12 and len(s)/3<=h<=len(s)/2 else 'SHOTS_FAIL',d,h,len(s))"
  EXPECT: SHOTS_OK
- [ ] G7: Production Book has the Sent to Ralph line and one TOTAL
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/' in t and t.count('TOTAL: $')==1 else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
- [ ] G8: Job media in Drive, none in git
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check 2>&1 | tail -1
  EXPECT: MEDIA_OK
- [ ] G9: Ralph notified (push + email) and asked with tappable options: manual, evidence = tool results in this session
