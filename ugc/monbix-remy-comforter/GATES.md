# Monbix Remy comforter set (Grace), 2026-10-26, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/monbix-remy-comforter
  EXPECT: GATE OK
- [ ] G2: readability grade of V1 is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
- [ ] G3: product sheet built from real pixels (>= 1500 px) and every real close-up exists
  CHECK: python3 -c "import os;from PIL import Image;ok=all(os.path.exists(f) for f in ['refs/real/pocket_real_tori2.png','refs/real/stripe_real_niki.png','refs/real/comforter_texture_tori.png','rooms/roomA_olive_bedroom.jpg']);im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
- [ ] G4: shots mark HAND / HAND-FREE with a third to half hand-free, pockets in the VO and on screen, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['videos'][0]['shots'];f=sum(1 for x in s if not x['hand'])/len(s);p=sum(1 for x in s if x['pocket']);t=open('scripts.md').read();ok=1/3-0.01<=f<=0.51 and p>=2 and 'pocket on both sides' in t and 'kling' not in open('shots.json').read().lower();print('MIX_OK' if ok else 'BAD',round(f,2),p)"
  EXPECT: MIX_OK
- [ ] G5: every still and clip prompt passes the prompt lint and is marked checked
  CHECK: cd ../.. && python3 grace/prompt_check.py mark ugc/monbix-remy-comforter ugc/monbix-remy-comforter/prompts/still_S1.txt ugc/monbix-remy-comforter/prompts/still_S2.txt ugc/monbix-remy-comforter/prompts/still_S3.txt ugc/monbix-remy-comforter/prompts/still_S4.txt ugc/monbix-remy-comforter/prompts/still_S5.txt ugc/monbix-remy-comforter/prompts/still_S6.txt ugc/monbix-remy-comforter/prompts/still_S7.txt ugc/monbix-remy-comforter/prompts/still_S8.txt ugc/monbix-remy-comforter/prompts/still_S9.txt ugc/monbix-remy-comforter/prompts/still_S10.txt ugc/monbix-remy-comforter/prompts/still_S11.txt
  EXPECT: MARKED_OK
- [ ] G6: REMOVED.md carries the standing removals and this job's ones
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','striped comforter','throw','breathable']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G7: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
- [ ] G8: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
