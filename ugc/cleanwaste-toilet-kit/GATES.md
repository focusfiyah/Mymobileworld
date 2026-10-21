# Cleanwaste Portable Toilet Bags (Grace), 2026-10-21, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/cleanwaste-toilet-kit
  EXPECT: GATE OK
- [ ] G2: every script readability file is grade <= 6
  CHECK: python3 -c "import re,glob;fs=sorted(glob.glob('research/readability_v*.txt'));g=[float(re.search(r'Kincaid\):\s*([0-9.]+)',open(f).read()).group(1)) for f in fs];print('GRADES_OK' if fs and max(g)<=6 else 'BAD',g)"
  EXPECT: GRADES_OK
- [ ] G3: Grace's script claims each have a source verdict in product_facts.md
  CHECK: python3 -c "t=open('research/product_facts.md').read().lower();ks=['gels','odor','toilet paper','wipe','zip','toilet that won']; m=[k for k in ks if k not in t];print('FACTS_OK' if not m else 'MISSING',m)"
  EXPECT: FACTS_OK
- [ ] G4: real product photos saved (box front at least 800 px wide)
  CHECK: python3 -c "import glob;from PIL import Image;fs=[f for f in glob.glob('refs/real/*') if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))];w=max([Image.open(f).size[0] for f in fs] or [0]);print('PHOTOS_OK' if len(fs)>=3 and w>=800 else 'NO',len(fs),w)"
  EXPECT: PHOTOS_OK
- [ ] G5: product reference sheet built from real pixels
  CHECK: python3 -c "from PIL import Image;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if min(im.size)>=900 else 'SMALL',im.size)"
  EXPECT: SHEET_OK
- [ ] G6: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every prompt passed through prompt-master rules
  CHECK: python3 -c "import json;d=json.load(open('shots.json'));r=[];[r.append((v['id'],sum(1 for s in v['shots'] if not s['hand'])/len(v['shots']))) for v in d['videos']];print('MIX_OK' if all(1/3-0.01<=x<=0.5+0.01 for _,x in r) else 'BAD',r)"
  EXPECT: MIX_OK
- [ ] G7: REMOVED.md exists and carries Ralph's standing removals (no text, no cards, no Ken Burns)
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G8: review page published with the script + reference sheet; plan sent to Ralph with one total cost; push + email sent (manual)
