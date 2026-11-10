# Gates: ili New York Double Flap Eyeglass Case edit (2026-11-10)

- [x] G1: Grace's original video is downloaded and its size equals the Drive file size
  CHECK: python3 -c "import os,json;m=json.load(open('orig/meta.json'));print('ORIG_OK' if os.path.getsize(m['path'])==int(m['drive_size']) else 'MISMATCH')"
  EXPECT: ORIG_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b4e3cb1fa4c4ae5ed4404edd600ba22924d370387f5a627004861049d5ee0472; exit=0; EXPECT=matched; output-sha256=8ccea134bbbbca09051ba578c55f5498532c0bba596cb0b81ea70cca7932bcb0; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ili-eyeglass-case; path=7f4fb4b02918/15 entries
- [x] G2: (manual) Frames of the whole original viewed (contact sheet); shot list picks the case open/closed, both flaps, sunglasses + eyeglasses in, closure, leather close-up, in-hand/in-bag angles
  EVIDENCE: 1 fps sheets of all 99.6 s + 4 fps windows (8-16, 17-29, 48-58, 80-99 s). Audio = background chat (Whisper base.en), cut silent.
- [x] G3: Cut is 7-20 s (Grace msg 351), 1080x1920, no black frames, within 0.15 s of plan
  CHECK: python3 check.py ili 7 20
  EXPECT: CUT_OK ili
  EVIDENCE: automatic-evidence=v1; definition-sha256=0dfcd8ed052d18a950d5f5352ad83a28d17bcdb5df929115d6dfb3b2382793ce; exit=0; EXPECT=matched; output-sha256=c48e6cf9dea81071e061b3682c0a6ef231e35f82c1232e08b0692241957d6776; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/ili-eyeglass-case; path=7f4fb4b02918/15 entries
- [x] G4: (manual) Every frame of the cut viewed (5-6 fps sheet) + 2x edges: no blur at cuts, nothing stretched (every clip >= 1.0x), bright neutral grade, no text, REMOVED.md checked
  EVIDENCE: 6 fps sheet of the 13.83 s cut, 10 fps on the close-up; blurry zoom-out after the leather close-up trimmed (95.65 s); 2x crops at 7 points clean; source is 1080x1920, so nothing scaled or stretched; mean Y 142.6; no text (REMOVED.md).
- [x] G5: (manual) Cut on the review page (video full column width); Ralph push + email; Grace told on Telegram with pending wording (no ✅, no "done")
  EVIDENCE: review https://claude.ai/artifact/PLLikevtSvqtUvoVECFDRo v1; push sent; email 1a1c382b47979bf6; Grace Telegram msg 361 (pending wording).
- [x] G6: (manual) After Ralph's OK on that exact cut: Drive "CURRENT - ili Case V1 (HD).mp4" size = local; nothing loose; "✅ ili New York Eyeglass Case V1 (HD) is done and in Drive: <folder link>" sent to Ralph and Grace; hourly check task deleted
  EVIDENCE: Ralph "Ok" 2026-11-10 on review v1; Drive 1RU5OG1YlSg50E_lxHcXeotxRb4HpXAoM size 25883667 = local; folder holds only Originals + CURRENT; ✅ Telegram msgs 380 (Ralph) + 381 (Grace group); hourly task trig_01JEm6h52NY5EN3woXAipuY8 deleted
- [ ] G7: (manual) Brain note Brain/Jobs + Active work line removed; tools/brain/check.py prints BRAIN_OK

