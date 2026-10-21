# Gates: Vans sequin Authentic, 10 AI videos for Grace

OWNS: ugc/vans-sequin-authentic/**

Scope: 10 finished 7-15 s vertical AI videos of the real Vans Premium Authentic sequin checkerboard (8 = 4 recreations of each of Grace's two references, 2 gift/unboxing), Grace's hand jewellery + white-polish toes + anklets, approved by Ralph, delivered to Drive.

- [x] G1: Script gate passes on the current script (research, hooks, humanizer, readability, audience, sources)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic
  EXPECT: GATE OK
  EVIDENCE: run by hand 2026-10-21 after the last script edit: GATE OK

- [x] G2: Product reference sheet exists, built only from real Vans photos
  CHECK: python3 -c "from PIL import Image; im=Image.open('ugc/vans-sequin-authentic/refs/product_sheet.png'); print('SHEET_OK' if im.size==(1600,2400) else 'bad')"
  EXPECT: SHEET_OK
  EVIDENCE: run by hand 2026-10-21: SHEET_OK

- [x] G3: Ralph approved the one-message plan + total cost before any paid call (his words quoted in README)
  EVIDENCE: Ralph 2026-10-21 'Go with Kie all the way' (plan B, $7.73 Kie)

- [x] G4: Every still QC'd at full size + 2x edges (grip, real shoe details, sequins only on black squares, white polish, anklet, no forearm) before its clip is paid for; one test still and one test clip first
  EVIDENCE: 45 images QC'd full size + 2x; test still V1S1, test clip V1S1 (r0, then r1 with the real tab ref) before batches

- [x] G5: Ten finals exist, each 7-15 s, vertical, and no two share the same footage
  CHECK: python3 qc/finals_check.py
  EXPECT: FINALS_OK
  CWD: ugc/vans-sequin-authentic
  EVIDENCE: run by hand 2026-10-21: FINALS_OK (10 finals, 7.1-13.6 s, 1080x1920)

- [x] G6: Cut gate passes (coach compare vs the winners done, no text overlay unless Ralph said yes)
  CHECK: python3 grace/gate.py ugc/vans-sequin-authentic --stage cut
  EXPECT: GATE OK
  EVIDENCE: run by hand 2026-10-21: GATE OK (--stage cut, compare proofs V1/V5)

- [x] G7: Every final checked against REMOVED.md and frame-by-frame QC (no shimmer, shoe never changes, hands whole, no halo), ai_finish applied last
  EVIDENCE: REMOVED.md table checked against all 10 finals; clip_qc.py motion + 6fps frame review; clean windows in cut.py; finish applied in cut.py (ai_finish values, bitrate capped)

- [ ] G8: Cuts on the Artifact review page, Ralph emailed + pushed, Ralph approved
  EVIDENCE: review page round 10 (v16); Ralph in chat 2026-10-21 "Go ahead for v4. Add in drive when done"; emails sent 05:2x and after Drive. UNMET PART: phone push, PushNotification not loadable in this session (ToolSearch "PushNotification" = no match, 2026-10-21).

- [x] G9: Finals in Drive "Grace Tiktok assets" one product folder, CURRENT prefix, link in README; running Kie/Kling cost vs quote recorded
  EVIDENCE: https://drive.google.com/drive/folders/1sCPZmn3mSM_BazNZxNxVFibniSqUOE-_ "Vans sequin (Grace)": CURRENT - Vans V1..V10.mp4 (Drive sizes = local bytes, all 10) + CURRENT - Vans captions doc (read back OK); README Status: Kie $16.39 vs $7.73 plan, Kling 48 s on Kie.
