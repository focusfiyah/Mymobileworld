# Gates: Goth High-Low Skirt v2 (try-on route), plan step (session 2026-10-25)

OWNS: ugc/goth-highlow-skirt/**

Scope: replicate the inspo (@jaquelineee809) with the real skirt on Grace; THIS session's step = a revised BOOK.md (bare legs + boots, neck down) on the review page, Ralph notified, no spend before his OK.

- [ ] G1: Script gate passes on the current script
  CHECK: python3 grace/gate.py ugc/goth-highlow-skirt
  EXPECT: GATE OK
  CWD: ../..

- [ ] G2: BOOK.md has the bare-legs + boots step, neck-down framing and one TOTAL line, and no tights left in the plan
  CHECK: python3 -c "t=open('BOOK.md').read();ok=t.count('TOTAL: $')==1 and 'BARE LEGS' in t and 'NECK DOWN' in t and 'Step A' in t and 'black sheer tights' not in t;print('BOOK_OK' if ok else 'BAD')"
  EXPECT: BOOK_OK

- [ ] G3: Every v2 clip and base-edit prompt (prompt-master) names bare legs + boots and none says tights
  CHECK: python3 -c "import glob;fs=sorted(glob.glob('prompts/v2_*.txt'));ok=len(fs)==7 and all('boots' in open(f).read() and 'sheer black tights.' not in open(f).read().replace('remove the sheer black tights.','') for f in fs);print('PROMPTS_OK' if ok else 'BAD',len(fs))"
  EXPECT: PROMPTS_OK

- [ ] G4: Try-on runner refuses without an approved book (gate wired)
  CHECK: python3 tryon/run_tryon.py gatecheck=person.jpg,garment_front.jpg 2>&1 | head -3
  EXPECT: BOOK.md is not approved

- [ ] G5: Review page has round 30 on top (newest first) and is republished to 3JRHDgMib5grRRR9ybu1QA
  CHECK: python3 -c "t=open('review/index.html').read();i=t.find('Round 30');print('PAGE_OK' if 0<i<t.find('Round 29') else 'BAD')"
  EXPECT: PAGE_OK

- [ ] G6: Ralph notified (phone push attempted + email sent), result recorded here
- [ ] G7: Nothing paid this session (no new fal/Kie entries before his OK)
  CHECK: python3 -c "import json;d=json.load(open('tryon/tryon_log.json'));print('NOSPEND_OK' if len(d)==6 else 'BAD',len(d))"
  EXPECT: NOSPEND_OK
