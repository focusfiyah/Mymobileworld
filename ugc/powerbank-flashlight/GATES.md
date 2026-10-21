# Power bank flashlight (Grace), phase 2: stills -> clips -> VO -> cut (Ralph approved 2026-10-21)

Ralph 2026-10-21: "OK, dusk is fine, same hand rings. Use this product reference sheet." Quote: Kie $2.00, Kling ~128 cr, ~600 EL chars.
Phase 1 ledger (research, script, sheet, plan): all 6 met, see git history.

- [ ] G1: Ralph's product sheet is the product reference in every product still/clip
  CHECK: python3 -c "import json;j=json.load(open('shots.json'));print('REF_OK' if j['refs']['product']==['refs/front_crop_ralph.png','refs/product_sheet.png'] and 'gunmetal' in j['product_block'] else 'NO')"
  EXPECT: REF_OK
- [ ] G2: 9 stills exist, S4 test still approved by me at full size before the rest (manual QC: grip, product parts, rings, edges 2x)
- [ ] G3: 9 clips exist (all Seedance, no Kling per Ralph 2026-10-21), every clip QC'd (product unchanged, hand edges 2x, no text)
  CHECK: python3 -c "import pathlib;n=[p for p in ['S1','S2','S3','S4','S5','S6','S7','S8','S9'] if not pathlib.Path(f'clips/{p}.mp4').exists()];print('CLIPS_OK' if not n else 'MISSING '+' '.join(n))"
  EXPECT: CLIPS_OK
- [ ] G4: Grace C voiceover, loudnorm -16 LUFS, STT shows no stutter or dropped word
- [ ] G5: cut is 9:16, no text drawn, AI finish applied, compare vs @zin5bamu done, gate --stage cut OK
  CHECK: cd ../.. && python3 grace/gate.py ugc/powerbank-flashlight --stage cut
  EXPECT: GATE OK
- [ ] G6: running total reported vs the $2.00 quote at each paid step; cut on the review page + push + email (manual)
