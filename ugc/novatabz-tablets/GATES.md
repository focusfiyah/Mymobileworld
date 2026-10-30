# NovaTabz Toothpaste Tablets (Grace), 2026-10-30, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/novatabz-tablets
  EXPECT: GATE OK
- [ ] G2: readability grade of the script is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
- [ ] G3: product sheet built from real pixels and product_truth.json lists photos, facts and forbid
  CHECK: python3 -c "import json,os;from PIL import Image;t=json.load(open('product_truth.json'));ok=all(os.path.exists(f) for f in t['photos']) and len(t['facts'])>=6 and len(t['forbid'])>=5;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1000 else 'NO',im.size)"
  EXPECT: SHEET_OK
- [ ] G4: shots mark HAND / HAND-FREE with a third to half hand-free, every spoken line has a shot, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and all(x.get('words') for x in s) and 'kling' not in open('shots.json').read().lower();print('MIX_OK' if ok else 'BAD',round(f,2),len(s))"
  EXPECT: MIX_OK
- [ ] G5: every still and clip prompt passes the prompt lint and is marked checked
  CHECK: cd ../.. && python3 grace/prompt_check.py mark ugc/novatabz-tablets ugc/novatabz-tablets/prompts/*.txt
  EXPECT: MARKED_OK
- [ ] G6: REMOVED.md carries the standing removals and this job's ones
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','price','golden','innuendo']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G7: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
- [x] G8: review page published with script, sheet, storyboard plan, prompts and the total; push + email sent (manual)
  EVIDENCE: 2026-10-30 page https://claude.ai/artifact/6A88QRQeyEJyNgZWrPwsRe v1; Gmail id 1a18b30ebd430ec8; PushNotification "Mobile push requested."
- [ ] G9: brain note + session log written and the brain check passes
  CHECK: cd ../.. && python3 tools/brain/check.py --terms "NovaTabz toothpaste tablets"
  EXPECT: BRAIN_OK

# Phase 2 (2026-10-30, after Ralph's OK): stills, clips, cut
- [x] G10: cut QC passes (manual record of `python3 qc/check_cut.py out/novatabz_v1.mp4`)
  EVIDENCE: 2026-10-30 CUT_QC_OK, 15.20 s, -17.32 LUFS, peak -2.09 dB
- [x] G11: cut-stage gate passes
  EVIDENCE: 2026-10-30 `python3 grace/gate.py ugc/novatabz-tablets --stage cut` -> GATE OK
- [x] G12: voice echo <= 150 ms
  EVIDENCE: 2026-10-30 echo.py vo/voiceover_paced.mp3 rt60_est_ms=150
- [ ] G13: delivered to Drive, sizes match (manual; after Ralph approves the cut)
