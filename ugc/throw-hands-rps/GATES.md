# Gates: Throw Hands RPS card game (Grace)

OWNS: ugc/throw-hands-rps/**

Scope: one AI Grace ad for the Throw Hands Rock Paper Scissors card game, matched to the format of Ralph's 3 example TikToks, delivered to Drive.

- [x] G1: Script gate passes
  CWD: ../..
  CHECK: python3 grace/gate.py ugc/throw-hands-rps
  EXPECT: GATE OK
  EVIDENCE: 2026-10-13 gate.py printed GATE OK on script v2

- [ ] G2: Plan with research proof, storyboard and one total cost sent and approved by Ralph before any paid call
  EVIDENCE: pending

- [ ] G3: Stills QC'd at full size (real box/cards unchanged, whole wrists, hands from frame edge, 2x edge zoom) before any clip
  EVIDENCE: pending

- [ ] G4: Riskiest clip tested and QC'd before the other clips
  EVIDENCE: pending

- [ ] G5: Cut QC (no text overlay, REMOVED.md, every VO word matches its shot, coach compare, gate --stage cut, ai_finish applied)
  EVIDENCE: pending

- [ ] G6: Kie spend at or under the approved cap, reported at every paid step
  EVIDENCE: pending

- [ ] G7: Final in Drive "Grace Tiktok assets/Throw Hands Card Game (Grace)" with CURRENT- prefix; README Status current
  EVIDENCE: pending

## Model test (Ralph 2026-10-14: Seedance 2.0/Fast, Vidu Q3 Turbo, Hailuo 02 Pro/2.3 Std on this ad)
- [x] G8: Kie price + model id found for every requested model, or a tested reason it is not on Kie
  CWD: .
  CHECK: python3 -c "t=open('MODEL_TEST.md').read();m=['Seedance 2.0 Fast','Seedance 2.0 |','Hailuo 2.3 Standard','Hailuo 02 Pro','Vidu Q3 Turbo'];print('ALL_MODELS' if all(x in t for x in m) else [x for x in m if x not in t])"
  EXPECT: ALL_MODELS
  EVIDENCE: 2026-10-14 Kie pricing API rows + docs.kie.ai; Vidu Q3 Turbo not on Kie, vidu/replicate APIs 400/401 without a key
- [ ] G9: Test cost approved by Ralph before any paid call
  EVIDENCE: pending (asked 2026-10-14, $2.375)
- [ ] G10: S4 still QC'd at full size, then one clip per approved model, sheet + per-model score table to Ralph
  EVIDENCE: pending
- [ ] G11: Kie spend at or under the approved test total
  EVIDENCE: pending
