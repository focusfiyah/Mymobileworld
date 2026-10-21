# GATES: TrendyQueen V-neck 3-pack, pause edit (Grace, 2026-10-21)

Job: Grace's own full video (Drive "TrendyQueenDeeoV-Neck.LS.Shirt.MOV", 45.5s), remove the awkward pauses only. $0.

- [x] G1: Final cut is 1080x1920 h264+aac, shorter than the 45.5s source but over 30s
  CHECK: python3 -I qc.py spec "out/TrendyQueen V-neck V1.mp4"
  EXPECT: spec OK
- [x] G2: No word Grace said is dropped (whisper on the cut vs the source transcript)
  CHECK: python3 -I qc.py words "out/TrendyQueen V-neck V1.mp4"
  EXPECT: words OK
- [x] G3: No pause longer than 0.5s remains (source had 1.9s / 0.9s / 0.5s gaps)
  CHECK: python3 -I qc.py pauses "out/TrendyQueen V-neck V1.mp4"
  EXPECT: pauses OK
- [x] G4: No black or blown flash frame at any cut
  CHECK: python3 -I qc.py flash "out/TrendyQueen V-neck V1.mp4"
  EXPECT: flash OK
- [x] G5: Loudness about -14 LUFS (not silent, not clipped)
  CHECK: python3 -I qc.py loud "out/TrendyQueen V-neck V1.mp4"
  EXPECT: loud OK
- [x] G6: Nothing added: no text, emoji, cards or grade (job.json has no overlays)
  CHECK: python3 -I -c "import json; j=json.load(open('job.json')); print('none OK' if not j.get('overlays') and not j['videos']['V1'].get('overlays') else 'HAS')"
  EXPECT: none OK
- [x] G7: Cuts watched on a contact sheet at every cut point: no mid-gesture jump that reads as a glitch (manual)
- [x] G8: Review page (Artifact) with the playable cut published, link in the reply (manual)
- [x] G9: In Drive "Grace Tiktok assets" product folder as "CURRENT - ...", Drive size == local size (manual)
- [x] G10: Ralph notified: push + email (manual)
- [x] G11: README Status line + REMOVED.md written, committed and pushed on ccr-5affdde5-zcaw2d (manual)
