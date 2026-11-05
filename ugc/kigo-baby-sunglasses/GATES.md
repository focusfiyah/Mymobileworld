# Gates: KIGO Baby Sunglasses scripts V1 (Grace, Telegram request 2026-11-05), scripts only

OWNS: ugc/kigo-baby-sunglasses/**

Scope: Rule 0 script gate, 5 different-angle scripts (about 30 s each, seasonal objection worked in), Claude doc + Google Doc in Drive. No paid generation, no video.

- [ ] G1: script gate passes (audience, coach, viral, facts, hooks, humanizer, readability, sources, research verdict, banned phrases)
  CHECK: python3 grace/gate.py ugc/kigo-baby-sunglasses
  EXPECT: GATE OK

- [ ] G2: five scripts exist, each with HOOK / BODY / CTA and 2 alternate hooks
  CHECK: python3 -c "t=open('ugc/kigo-baby-sunglasses/scripts.md').read(); import sys; print('FIVE_OK' if t.count('**HOOK**')==5 and t.count('**BODY**')==5 and t.count('**CTA**')==5 and t.count('Alternate hooks')==5 else 'BAD')"
  EXPECT: FIVE_OK

- [ ] G3: every script closes with "It's in the orange cart." and none says a price, "order it now", "reviewer" or "the label says"
  CHECK: python3 -c "import re;t=open('ugc/kigo-baby-sunglasses/scripts.md').read(); ok=t.count(\"It's in the orange cart.\")>=5 and not re.search(r'order it now|reviewer|label says|\\\$\\d',t,re.I); print('CLOSE_OK' if ok else 'BAD')"
  EXPECT: CLOSE_OK

- [ ] G4: seasonal work covers low winter sun, snow glare, gifts, warm-weather buyers, trips
  CHECK: python3 -c "t=open('ugc/kigo-baby-sunglasses/research/RESEARCH.md').read().lower(); print('SEASON_OK' if all(k in t for k in ['low','snow','gift','florida','trip','not summer']) else 'BAD')"
  EXPECT: SEASON_OK

- [ ] G5: claims the listing cannot back are flagged in product_facts (99.9%, certificates, BPA, food-grade, age split, foldable, strap)
  CHECK: python3 -c "t=open('ugc/kigo-baby-sunglasses/research/product_facts.md').read().lower(); print('FLAGS_OK' if all(k in t for k in ['99.9','certificate','bpa','food-grade','tr90','foldable','strap']) else 'BAD')"
  EXPECT: FLAGS_OK

- [ ] G6: Drive folder "KIGO Baby Sunglasses (Grace)" holds CURRENT - scripts Google Doc and Research verdict doc, no PDF
  EVIDENCE: pending (manual: Drive folder link)

- [ ] G7: Telegram message sent to group -5234107715 and chat 7628331161, phone push and email sent
  EVIDENCE: pending (manual)
