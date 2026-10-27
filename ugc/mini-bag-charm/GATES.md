# Mini Bag Charm (Grace), 2026-10-26, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/mini-bag-charm
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
- [ ] G5: every still prompt passes the prompt lint and is marked checked
  CHECK: cd ../.. && python3 grace/prompt_check.py mark ugc/mini-bag-charm ugc/mini-bag-charm/prompts/still_S1.txt ugc/mini-bag-charm/prompts/still_S2.txt ugc/mini-bag-charm/prompts/still_S3.txt ugc/mini-bag-charm/prompts/still_S5.txt ugc/mini-bag-charm/prompts/still_S6.txt ugc/mini-bag-charm/prompts/still_S7.txt ugc/mini-bag-charm/prompts/still_S8.txt ugc/mini-bag-charm/prompts/still_S9.txt
  EXPECT: MARKED_OK
- [ ] G6: REMOVED.md carries the standing removals and this job's ones
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','price','other colours','golden']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G7: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
- [x] G8: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
  EVIDENCE: 2026-10-26 page https://claude.ai/artifact/Uns9WGWdYcjDBsdbbeCezb v1; Gmail GMAIL_SEND_EMAIL (gmail_correa-comus) id 1a17a90f5781e696; PushNotification "Mobile push requested."

# Phase 2 (2026-10-26, after Ralph's OK): stills
- [ ] G9: all 9 stills exist at 9:16
  CHECK: python3 -c "from PIL import Image;import os;ok=[i for i in range(1,10) if os.path.exists(f'stills/S{i}.png') and abs(Image.open(f'stills/S{i}.png').size[0]/Image.open(f'stills/S{i}.png').size[1]-9/16)<0.02];print('STILLS_OK' if len(ok)==9 else 'MISSING',ok)"
  EXPECT: STILLS_OK
- [ ] G10: job spend stays within the approved book
  CHECK: cd ../.. && python3 grace/gate.py ugc/mini-bag-charm
  EXPECT: \$3.90 allowed
- [ ] G11: every still QC'd at 2x (product details, grip, hand jewellery, key ring, no text, REMOVED.md) with a verdict in qc/stills_r1.md (manual)
- [ ] G12: storyboard on the review page + push + email (manual)

# Phase 3 (2026-10-27): clips + cut
- [ ] G13: cut QC passes (length, loudness, no black/flash frames, 1080x1920)
  CHECK: python3 qc/check_cut.py out/minibag_v1.mp4
  EXPECT: CUT_QC_OK
- [ ] G14: cut-stage gate passes (compare proof, no text in the cut script)
  CHECK: cd ../.. \&\& python3 grace/gate.py ugc/mini-bag-charm --stage cut
  EXPECT: GATE OK
- [x] G15: cut on the review page + push + email (manual)
  EVIDENCE: page v4; Gmail 1a17ad7078c5f660; push requested
- [x] G16: delivered to Drive (manual)
  EVIDENCE: 2026-10-27 folder 1sTBKhYHwoJdWXRzf_ZNvrmLhY1i83Tm8; video 14Qxy7HO6dXsunGqSJhbmPaXc-FMTi2S0 size 69197662 = local; doc 1qyVnUEJ3-j0-7u8MR52LIfRf--RTdD_tP73RFR68EyQ read back via Composio, emoji intact
