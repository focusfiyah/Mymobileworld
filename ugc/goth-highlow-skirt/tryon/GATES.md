# Gates: virtual try-on test (Goth High-Low Skirt, 2026-10-22)

OWNS: ugc/goth-highlow-skirt/tryon/**, ugc/goth-highlow-skirt/review/**, ugc/goth-highlow-skirt/README.md, grace/spend.json

Scope: one try-on image each from FASHN v1.6 and Kling Kolors on fal (person FULL2, garment = real listing front), QC'd at 2x, on the review page, spend logged, Ralph notified; spend <= $0.50.

- [x] G1: Each model's price read from its own fal page this session (FASHN $0.075, Kolors $0.07)
  EVIDENCE: 2026-10-22 fal pages + api.fal.ai pricing: FASHN 0.075, Kolors 0.07

- [x] G2: Exactly one result image per model saved, no retries
  CHECK: python3 -c "import json,os;d=json.load(open('ugc/goth-highlow-skirt/tryon/tryon_log.json'));ok=len(d)==2 and all(os.path.getsize(e['out'])>10000 for e in d);print('TWO_OK' if ok else 'BAD',len(d))"
  EXPECT: TWO_OK
  EVIDENCE: 2026-10-22 TWO_OK 2

- [x] G3: Test spend logged in grace/spend.json other and total <= $0.50
  CHECK: python3 -c "import json;o=[x for x in json.load(open('grace/spend.json'))['other'] if 'try-on' in x.get('what','')];s=sum(float(x['usd']) for x in o);print('SPEND_OK' if o and s<=0.5 else 'BAD',s)"
  EXPECT: SPEND_OK
  EVIDENCE: 2026-10-22 SPEND_OK 0.145

- [x] G4: Both results QC'd at 2x against the product truths, verdict per model written in tryon/QC.md
  CHECK: python3 -c "t=open('ugc/goth-highlow-skirt/tryon/QC.md').read();print('QC_OK' if 'FASHN verdict:' in t and 'Kolors verdict:' in t else 'BAD')"
  EXPECT: QC_OK
  EVIDENCE: 2026-10-22 QC_OK

- [x] G5: Review page has the side-by-side (real photo, FULL2, FASHN, Kolors) on top and is republished to the same URL
  CHECK: python3 -c "t=open('ugc/goth-highlow-skirt/review/index.html').read();i=t.find('tryon_side_by_side.jpg');print('PAGE_OK' if 0<i<t.find('Round 21') else 'BAD')"
  EXPECT: PAGE_OK
  EVIDENCE: 2026-10-22 PAGE_OK, published v23 to 3JRHDgMib5grRRR9ybu1QA

- [x] G6: Committed and merged to main, pushed
  CHECK: bash -c "git fetch -q origin main && git merge-base --is-ancestor HEAD origin/main && echo MERGED_OK"
  EXPECT: MERGED_OK
  EVIDENCE: 2026-10-22 MERGED_OK (main b4b90934 + merges)

- [ ] G7: Ralph notified by phone push AND email with result + exact cost
  EVIDENCE: email sent 1a165e8c8be142fa; phone push NOT sent: PushNotification not offered by ToolSearch this session (select + keyword search tested)
