# Youtheory B12B6 Liquid (Grace), 2026-10-26, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-b12b6
  EXPECT: GATE OK
- [ ] G2: readability grade of V1 is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
- [ ] G3: product sheet built from the real photos (>= 1500 px) and every close-up exists
  CHECK: python3 -c "import os;from PIL import Image;ok=all(os.path.exists(f) for f in ['refs/closeup_F.png','refs/closeup_G.png','refs/closeup_box.png','refs/real/grace_pouch_front_flat.jpg']);im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
- [ ] G4: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every product shot on Omni, no Kling, straw block in every still prompt
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['videos'][0]['shots'];f=sum(1 for x in s if not x['hand'])/len(s);st=all('white paper straw' in open('prompts/still_'+x['id']+'.txt').read() for x in s);ok=1/3-0.01<=f<=0.51 and all((x['model']=='omni')==x['product'] for x in s) and not any(x['model']=='kling' for x in s) and st;print('MIX_OK' if ok else 'BAD',f)"
  EXPECT: MIX_OK
- [ ] G5: every still and clip prompt passes the prompt lint
  CHECK: cd ../.. && python3 -c "import json,subprocess,glob,os;r=json.load(open('ugc/youtheory-b12b6/prompts/refs.json'));bad=[];[bad.append(f) for f in sorted(glob.glob('ugc/youtheory-b12b6/prompts/*.txt')) if 'PROMPT_LINT_OK' not in subprocess.run(['python3','grace/prompt_check.py','lint',f,'--refs',str(len(r[os.path.basename(f)[:-4].replace('still_','')]['still_refs' if 'still_' in f else 'clip_refs']))],capture_output=True,text=True).stdout];print('LINT_ALL_OK' if not bad else bad)"
  EXPECT: LINT_ALL_OK
- [ ] G6: REMOVED.md carries the standing removals, the listing-only line and the straw rule
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','essential daily vitamins','straw']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G7: BOOK.md written with one TOTAL line
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: \$[0-9.]+',t))==1 else 'NO')"
  EXPECT: BOOK_OK
- [ ] G8: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
