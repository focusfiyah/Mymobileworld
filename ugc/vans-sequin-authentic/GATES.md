# Gates: Vans sequin Authentic, 10 AI videos for Grace

OWNS: ugc/vans-sequin-authentic/**

Scope: 10 finished 7-15 s vertical AI videos of the real Vans Premium Authentic sequin checkerboard (8 = 4 recreations of each of Grace's two references, 2 gift/unboxing), Grace's hand jewellery + white-polish toes + anklets, approved by Ralph, delivered to Drive.

- [ ] G1: Script gate passes on the current script (research, hooks, humanizer, readability, audience, sources)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic
  EXPECT: GATE OK
  EVIDENCE: pending

- [ ] G2: Product reference sheet exists, built only from real Vans photos
  CHECK: python3 -c "from PIL import Image; im=Image.open('ugc/vans-sequin-authentic/refs/product_sheet.png'); print('SHEET_OK' if im.size==(1600,2400) else 'bad')"
  EXPECT: SHEET_OK
  EVIDENCE: pending

- [ ] G3: Ralph approved the one-message plan + total cost before any paid call (his words quoted in README)
  EVIDENCE: pending

- [ ] G4: Every still QC'd at full size + 2x edges (grip, real shoe details, sequins only on black squares, white polish, anklet, no forearm) before its clip is paid for; one test still and one test clip first
  EVIDENCE: pending

- [ ] G5: Ten finals exist, each 7-15 s, vertical, and no two share the same footage
  CHECK: python3 qc/finals_check.py
  EXPECT: FINALS_OK
  CWD: ugc/vans-sequin-authentic
  EVIDENCE: pending

- [ ] G6: Cut gate passes (coach compare vs the winners done, no text overlay unless Ralph said yes)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic --stage cut
  EXPECT: GATE OK
  EVIDENCE: pending

- [ ] G7: Every final checked against REMOVED.md and frame-by-frame QC (no shimmer, shoe never changes, hands whole, no halo), ai_finish applied last
  EVIDENCE: pending

- [ ] G8: Cuts on the Artifact review page, Ralph emailed + pushed, Ralph approved
  EVIDENCE: pending

- [ ] G9: Finals in Drive "Grace Tiktok assets" one product folder, CURRENT prefix, link in README; running Kie/Kling cost vs quote recorded
  EVIDENCE: pending
