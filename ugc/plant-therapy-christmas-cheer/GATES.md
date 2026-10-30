# Gates: Plant Therapy Christmas Cheer, plan phase (2026-10-30)

- [ ] G1: Script gate passes (all 9 PLAYBOOK §4 proofs)
  CHECK: cd ../.. && python3 grace/gate.py ugc/plant-therapy-christmas-cheer
  EXPECT: GATE OK
- [ ] G2: Every still and clip prompt lints clean
  CHECK: cd ../.. && python3 grace/prompt_check.py lint ugc/plant-therapy-christmas-cheer/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G3: BOOK.md has one TOTAL and the Sent to Ralph link
  CHECK: python3 -c "import re;b=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'^TOTAL: \$',b,re.M))==1 and 'Sent to Ralph: https://claude.ai/artifact/' in b else 'BAD')"
  EXPECT: BOOK_OK
- [ ] G4: product_truth.json lists only existing photos and a forbid list
  CHECK: python3 -c "import json,os;t=json.load(open('product_truth.json'));print('TRUTH_OK' if all(os.path.exists(p) for p in t['photos']) and t['forbid'] else 'BAD')"
  EXPECT: TRUTH_OK
- [ ] G5: Ralph notified by phone push AND email (manual: tool results in the session)
- [ ] G6: Brain updated and check passes
  CHECK: cd ../.. && python3 tools/brain/check.py --terms "Christmas Cheer,Plant Therapy,fake tree"
  EXPECT: BRAIN_OK
