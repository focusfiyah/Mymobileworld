# Mini Bag Charm (Grace), 2026-10-26, phase 1: research + script gate + plan (no paid calls)

- [ ] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/mini-bag-charm
  EXPECT: GATE OK
- [ ] G2: readability grade of the script is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
- [ ] G3: product sheet built from real pixels and product_truth.json lists photos, facts and forbid
  CHECK: python3 -c "import json,os;from PIL import Image;t=json.load(open('product_truth.json'));ok=all(os.path.exists(f) for f in t['photos']) and len(t['facts'])>=6 and len(t['forbid'])>=5;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1000 else 'NO',im.size)"
  EXPECT: SHEET_OK
- [ ] G4: shots mark HAND / HAND-FREE with a third to half hand-free, every spoken line has a shot, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and all(x.get('words') for x in s) and 'kling' not in open('shots.json').read().lower();print('MIX_OK' if ok else 'BAD',round(f,2),len(s))"
  EXPECT: MIX_OK
- [ ] G5: every still prompt passes the prompt lint and is marked checked
  CHECK: cd ../.. && python3 grace/prompt_check.py mark ugc/mini-bag-charm ugc/mini-bag-charm/prompts/still_S1.txt ugc/mini-bag-charm/prompts/still_S2.txt ugc/mini-bag-charm/prompts/still_S3.txt ugc/mini-bag-charm/prompts/still_S5.txt ugc/mini-bag-charm/prompts/still_S6.txt ugc/mini-bag-charm/prompts/still_S7.txt ugc/mini-bag-charm/prompts/still_S8.txt ugc/mini-bag-charm/prompts/still_S9.txt
  EXPECT: MARKED_OK
- [ ] G6: REMOVED.md carries the standing removals and this job's ones
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','price','other colours','golden']) else 'NO')"
  EXPECT: REMOVED_OK
- [ ] G7: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
- [x] G8: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
  EVIDENCE: 2026-10-26 page https://claude.ai/artifact/Uns9WGWdYcjDBsdbbeCezb v1; Gmail GMAIL_SEND_EMAIL (gmail_correa-comus) id 1a17a90f5781e696; PushNotification "Mobile push requested."

# Phase 2 (2026-10-26, after Ralph's OK): stills
- [ ] G9: all 9 stills exist at 9:16
  CHECK: python3 -c "from PIL import Image;import os;ok=[i for i in range(1,10) if os.path.exists(f'stills/S{i}.png') and abs(Image.open(f'stills/S{i}.png').size[0]/Image.open(f'stills/S{i}.png').size[1]-9/16)<0.02];print('STILLS_OK' if len(ok)==9 else 'MISSING',ok)"
  EXPECT: STILLS_OK
- [ ] G10: job spend stays within the approved book
  CHECK: cd ../.. && python3 grace/gate.py ugc/mini-bag-charm
  EXPECT: \$3.90 allowed
- [ ] G11: every still QC'd at 2x (product details, grip, hand jewellery, key ring, no text, REMOVED.md) with a verdict in qc/stills_r1.md (manual)
- [ ] G12: storyboard on the review page + push + email (manual)

# Phase 3 (2026-10-27): clips + cut
- [ ] G13: cut QC passes (length, loudness, no black/flash frames, 1080x1920)
  CHECK: python3 qc/check_cut.py out/minibag_v1.mp4
  EXPECT: CUT_QC_OK
- [ ] G14: cut-stage gate passes (compare proof, no text in the cut script)
  CHECK: cd ../.. \&\& python3 grace/gate.py ugc/mini-bag-charm --stage cut
  EXPECT: GATE OK
- [x] G15: cut on the review page + push + email (manual)
  EVIDENCE: page v4; Gmail 1a17ad7078c5f660; push requested
- [x] G16: delivered to Drive (manual)
  EVIDENCE: 2026-10-27 folder 1sTBKhYHwoJdWXRzf_ZNvrmLhY1i83Tm8; video 14Qxy7HO6dXsunGqSJhbmPaXc-FMTi2S0 size 69197662 = local; doc 1qyVnUEJ3-j0-7u8MR52LIfRf--RTdD_tP73RFR68EyQ read back via Composio, emoji intact
- [x] G17: v2 delivered (manual)
  EVIDENCE: 2026-10-27 CURRENT - Mini Bag Charm V2.mp4 id 1t3yUupoX5v2iYCUH78pWsQetVMR67CGC size 69270724 = local; v1 renamed "v1 (2026-10-27) - Mini Bag Charm.mp4" into Older versions 1WU3NcV_PpN-AzP925TsQ5IKBtHoY1wf7
- [x] G18: v3 delivered (manual)
  EVIDENCE: 2026-10-27 CURRENT - Mini Bag Charm V3.mp4 id 1rJ12UqgxNpHEssdUSUOyex7B7XOMKM-Z size 69222464 = local; v2 renamed "v2 (2026-10-27) - Mini Bag Charm.mp4" into Older versions

# Phase 6 (2026-10-28, Grace: "she can tell it was pasted"; Ralph picked the free re-composite)
- [x] G30: the pasted charm keeps Grace's burgundy (listing hue ~352 deg) in S4, S7, S8, S9 of the new cut
  CHECK: python3 tools/hue_check.py
  EXPECT: HUE_OK
- [x] G31: the charm is no sharper than the footage around it (edge steepness charm/surround <= 1.1; v7 S7 measured 1.22)
  CHECK: python3 tools/hue_check.py --sharp
  EXPECT: SHARP_OK
- [x] G32: S4 charm swings with the hand's moves; S7/S9 sway gently (looked at in the drift strips, manual)
  EVIDENCE: qc/track_S4.json sway -5.9..3.6 deg; S7/S9 +-0.8; strips qc/strip_S4/S7.jpg looked at
- [x] G33: 2x strips of S4/S7/S8/S9 looked at: room light on it, contact shadow, tissue not glowing, no halo, attached, no slide (manual)
  EVIDENCE: 2x crops v7 vs v8 (review/v8_compare.jpg); fixed on the way: warp fringe, S8 ghost above handle + left sliver, S9 bag-edge smear, S9 over-blur
- [x] G34: cut QC passes on v8
  CHECK: python3 qc/check_cut.py out/minibag_v8.mp4
  EXPECT: CUT_QC_OK
- [x] G35: v8 on the review page with v7 beside it + push + email (manual)
  EVIDENCE: artifact Uns9WGWdYcjDBsdbbeCezb version 13

# Phase 7 (2026-10-28, Ralph on v8: "6-9s the bag does something weird", "Drift in at these points" (S7 0:17), "wanted to see the motion of putting into stocking stuffer"; OK $0.49 for the S8 clip)
- [x] G36: S4 charm hangs from the AI's own ring and chain (no jump, no drawn chain toward the hand) (manual)
  EVIDENCE: qc/v9_strip_S4.jpg looked at; ring followed frame to frame (FOLLOW_RING)
- [x] G37: S7 handle, rim and curtain clean at 0:15-0:18, charm on the AI clasp (manual)
  EVIDENCE: qc/v9_strip_S7.jpg + 2x crops frames 5/30/55/74
- [x] G38: S8 shows the hand lowering the charm into the stocking, fingers in front, cuff hides it inside, no ghosts (manual)
  EVIDENCE: qc/v9_strip_S8.jpg; Seedance task a3ef23d1ab9c87a72c2435794f8bedcd $0.16
- [x] G39: hue and sharpness hold on all four pasted shots
  CHECK: python3 tools/hue_check.py && python3 tools/hue_check.py --sharp
  EXPECT: SHARP_OK
- [x] G40: cut QC passes on v9
  CHECK: python3 qc/check_cut.py out/minibag_v9.mp4
  EXPECT: CUT_QC_OK
- [x] G41: v9 on the review page + push + email (manual)
  EVIDENCE: artifact Uns9WGWdYcjDBsdbbeCezb version 14

# Phase 8 (2026-10-28, Ralph on v9: "Still have drift or misalignment" at S4, S7, S8)
- [x] G42: every frame of S4, S7, S8 in the final cut looked at (15 fps / 10 fps strips), no patch blotch, bag shape change, AI leftover or gap under the fingers (manual)
  EVIDENCE: review/v10_S4.jpg, v10_S7.jpg, v10_S8.jpg
- [x] G43: hue, sharpness, cut QC on v10
  CHECK: python3 tools/hue_check.py && python3 tools/hue_check.py --sharp && python3 qc/check_cut.py out/minibag_v10.mp4
  EXPECT: CUT_QC_OK
- [x] G44: v10 on the review page + push + email (manual)
  EVIDENCE: artifact Uns9WGWdYcjDBsdbbeCezb version 15

# Phase 9 (2026-10-28, Ralph: drift still at 7-8 s and 16-18 s; OK up to $0.64, "This is the last expense")
- [x] G45: S4 and S7 remade from charm-free start frames, no AI charm in the clips (manual)
  EVIDENCE: Seedance tasks 02dc4e93d996e0df8c8f46af481ff167 (S4N), 0054bada50be8ed360d770a4a5d3529a (S7N), $0.32, no redo
- [x] G46: every frame of S4/S7 in the final cut: charm on its ring, nothing patched, no AI leftovers (manual)
  EVIDENCE: review/v11_S4.jpg, review/v11_S7.jpg
- [x] G47: hue, sharpness, cut QC on v11
  CHECK: python3 tools/hue_check.py && python3 tools/hue_check.py --sharp && python3 qc/check_cut.py out/minibag_v11.mp4
  EXPECT: CUT_QC_OK

# Phase 10 (2026-10-28, Ralph on v11: "It is not good" -> "Free re-cut, no pasted shots", script "Yes, cut it")
- [x] G48: cut QC on the 18 s re-cut with the trimmed word list
  CHECK: python3 qc/check_cut.py out/minibag_v12.mp4 --words vo/words_v12.json
  EXPECT: CUT_QC_OK
- [x] G49: both voice joins clean (silence, then a whole word); S1 key-ring stub cut out; every frame of S1 looked at (manual)
  EVIDENCE: RMS at both joins; S1 opening stops at 1.45 s
- [x] G50: v12 on the review page + push + email (manual)
  EVIDENCE: artifact version 17
