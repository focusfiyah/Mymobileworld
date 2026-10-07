# Gates: Carpe Mountain Breeze 15s (Grace)

- [ ] G1: Script gate passes (plan stage)
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK
- [ ] G2: Final cut is 14.5-16.5s, 1080x1920
  CHECK: ffprobe -v error -show_entries format=duration -of csv=p=0 out/carpe_mb_15s.mp4 | python3 -c "import sys;d=float(sys.stdin.read());print('LEN_OK' if 14.5<=d<=16.5 else d)"
  EXPECT: LEN_OK
- [ ] G3: Cut-stage gate passes (compare vs @deals.with.dreamer, no text overlay)
  CHECK: python3 ../../grace/gate.py . --stage cut
  EXPECT: GATE OK
- [ ] G4: QC report written: real label unchanged, no shimmer/flicker, no background through hands, whole wrists, hands from frame edge, no face, 2x edge zoom, first second checked
  EVIDENCE: pending
- [ ] G5: Storyboard approved by Ralph before any video spend
  EVIDENCE: pending
- [ ] G6: Drive: CURRENT - file in the Carpe Mountain Breeze folder, link in README
  EVIDENCE: pending
