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

## Phase 11: v13 Flow kit from Grace's real photos (Ralph 2026-10-29 "Flow kit")
- [x] G51 Four 9:16 start frames (1080x1920) cut from Grace's own photos, plus padlock, scarf and sheet refs from her photos
  CHECK: python3 -c "from PIL import Image;import sys;ok=all(Image.open(f'kit_v13/F{i}-1_start.jpg').size==(1080,1920) for i in (1,2,3,4)) and all(__import__('os').path.exists('kit_v13/'+f) for f in ('ref_padlock.jpg','ref_scarf.jpg','ref_sheet_grace.jpg'));print('G51_OK' if ok else 'G51_FAIL')"
  EXPECT: G51_OK
- [x] G52 Four prompts lint clean, name images 1-4, say first frame and no hand, and are marked checked
  CHECK: python3 -c "import re;t=[open(f'prompts/flow_F{i}.txt').read() for i in (1,2,3,4)];ok=all('first frame' in x and 'No hand' in x and all(f'mage {n}' in x or f'images 2 to 4' in x for n in (1,2,3,4)) for x in t);print('G52_OK' if ok else 'G52_FAIL')" && for i in 1 2 3 4; do python3 ../../grace/prompt_check.py lint prompts/flow_F$i.txt --refs 4; done
  EXPECT: G52_OK[\s\S]*PROMPT_LINT_OK[\s\S]*PROMPT_LINT_OK[\s\S]*PROMPT_LINT_OK[\s\S]*PROMPT_LINT_OK
- [x] G53 Review page carries 4 kit cards (16 Save buttons, 4 prompts) and the downloads script; published v18 with kit13 files (manual: Artifact list shows 7 kit13 files)
  CHECK: python3 -c "s=open('review/index.html').read();print('G53_OK' if s.count('class=\"sv\"')==16 and all(f'id=\"pF{i}\"' in s for i in (1,2,3,4)) and 'claude.use(\"downloads\")' in s else 'G53_FAIL')"
  EXPECT: G53_OK
- [x] G54 No Kie spend for this phase (kie_log.json unchanged since v12: no new task after 2026-10-28)
  CHECK: python3 -c "import json;L=json.load(open('kie_log.json'));d=[str(x.get('t','')) for x in (L if isinstance(L,list) else L.get('tasks',[]))];print('G54_OK' if not any('2026-10-29' in x for x in d) else 'G54_FAIL')"
  EXPECT: G54_OK

## Phase 12: cut v13 from Ralph's Flow takes (2026-10-29)
- [x] G55 Four Flow takes in clips/flow13 matched to their cards by first-frame distance (F1 e8ca, F2 a2af, F3 cc03, F4 4195), 1080x1920, every frame checked at 4-12 fps zoom
  CHECK: python3 -c "import os;print('G55_OK' if all(os.path.exists(f'clips/flow13/F{i}_flow.mp4') for i in (1,2,3,4)) else 'G55_FAIL')"
  EXPECT: G55_OK
- [x] G56 v13 passes the cut QC (length, last word, loudness, levels)
  CHECK: python3 qc/check_cut.py out/minibag_v13.mp4 --words vo/words_v13.json
  EXPECT: CUT_QC_OK
- [x] G57 Review page v19 shows cut v13, its sheet and the 4 takes
  CHECK: python3 -c "s=open('review/index.html').read();print('G57_OK' if all(x in s for x in ('cut_v13.mp4','cut_sheet_v13.jpg','F1_flow.mp4','F4_flow.mp4')) else 'G57_FAIL')"
  EXPECT: G57_OK

## Phase 13: v13 approved, Drive (2026-10-29, Ralph "Approved")
- [x] G58 Drive folder holds CURRENT - Mini Bag Charm V13.mp4 (47,309,792 bytes = local) + CURRENT script V13 doc (read back); V12 video + doc renamed "(2026-10-28)" in Older versions (manual: Drive API results this session)
  CHECK: python3 -c "import os;print('G58_LOCAL_OK' if os.path.getsize('out/minibag_v13.mp4')==47309792 else 'G58_FAIL')"
  EXPECT: G58_LOCAL_OK
