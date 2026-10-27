# PRITECH 15-20 s x3 (V2-V4, Grace), 2026-10-27, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/pritech-15s
  EXPECT: GATE OK
- [ ] G2: each script is 15-20 s at Grace's measured 3.53 words/sec and reads at grade 6 or lower
  CHECK: python3 -c "import re;t=open('scripts.md').read();r=[];[r.append((v,len(re.search(r'## '+v+r':.*\n(.+)',t).group(1).split())/3.53,float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_'+v.lower()+'.txt').read()).group(1)))) for v in ['V2','V3','V4']];print('LEN_OK' if all(15<=s<=20 and g<=6 for _,s,g in r) else 'BAD',r)"
  EXPECT: LEN_OK
- [ ] G3: every shot prompt passes the prompt lint (refs counted per shot)
  CHECK: cd ../.. && python3 grace/prompt_check.py lint ugc/pritech-15s/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G4: each video has a third to half hand-free shots and every spoken line has a shot
  CHECK: python3 -c "import json,re;s=json.load(open('shots.json'));t=open('scripts.md').read();ok=True;exec(\"for v in ['V2','V3','V4']:\n x=[a for a in s if a['video']==v];f=sum(not a['hand'] for a in x)/len(x);ok=ok and 1/3-0.01<=f<=0.51 and ' '.join(a['line'] for a in x)==re.search(r'## '+v+r':.*\\\\n(.+)',t).group(1).strip()\");print('MIX_OK' if ok else 'BAD')"
  EXPECT: MIX_OK
- [ ] G5: 6 new real rooms with sources, none reused from V1
  CHECK: python3 -c "import os;a=open('rooms/SOURCES.md').read();b=open('../pritech-cleansing-brush/rooms/SOURCES.md').read();import re;ids=re.findall(r'= (p[xb]_\d+)',a);print('ROOMS_OK' if len(ids)==6 and all(os.path.exists(f'rooms/room_{k}.jpg') for k in 'DEFGHI') and not any(i in b for i in ids) else 'NO',ids)"
  EXPECT: ROOMS_OK
- [ ] G6: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
- [ ] G7: review page published with scripts, shot lists, rooms and the total; push + email sent (manual)
  EVIDENCE: pending

# Phase 2+ (after Ralph's OK): stills -> storyboard -> Flow kit / clips -> VO -> cuts
- [ ] G8: 20 stills exist at 9:16 and pass 2x QC (product shape, buttons, rings, no face beyond cheek/jaw) (manual + size check)
  EVIDENCE: pending
- [ ] G9: 3 cuts, each 15-20 s, AI finish applied, echo <= 150 ms, verify_fix clean, compare vs @joshjshowcase run (manual)
  EVIDENCE: pending
- [ ] G10: Drive folder has CURRENT V2-V4 + script doc; brain check BRAIN_OK (manual)
  EVIDENCE: pending
