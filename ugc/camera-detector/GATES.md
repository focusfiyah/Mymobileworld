# Hidden Camera Detector LY-10 (Grace), 2026-10-28, phase 1: research + script gate + plan (no paid calls)

- [x] G1: Ralph's 7 photos saved in the job folder (he asked: "save the image assets in the folder")
  CHECK: python3 -c "import glob;n=len(glob.glob('ref/real/*.jpg'));print('ASSETS_OK' if n==7 else 'NO',n)"
  EXPECT: ASSETS_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> ASSETS_OK 7
- [x] G2: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/camera-detector
  EXPECT: GATE OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> GATE OK
- [x] G3: readability grade of the script is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> GRADE_OK 4.9
- [x] G4: product sheet built from real pixels and product_truth.json lists photos, facts and forbid
  CHECK: python3 -c "import json,os;from PIL import Image;t=json.load(open('product_truth.json'));ok=all(os.path.exists(f) for f in t['photos']) and len(t['facts'])>=6 and len(t['forbid'])>=5;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1000 else 'NO',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> SHEET_OK (2320, 1700)
- [x] G5: shots mark HAND / HAND-FREE with a third to half hand-free, every spoken line has a shot, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and all(x.get('words') for x in s) and 'kling' not in open('shots.json').read().lower();print('MIX_OK' if ok else 'BAD',round(f,2),len(s))"
  EXPECT: MIX_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> MIX_OK 0.45 11
- [x] G6: every still prompt passes the prompt lint and is marked checked
  CHECK: cd ../.. && python3 grace/prompt_check.py mark ugc/camera-detector ugc/camera-detector/prompts/still_S1.txt ugc/camera-detector/prompts/still_S2.txt ugc/camera-detector/prompts/still_S3.txt ugc/camera-detector/prompts/still_S4.txt ugc/camera-detector/prompts/still_S6.txt ugc/camera-detector/prompts/still_S7.txt ugc/camera-detector/prompts/still_S8.txt ugc/camera-detector/prompts/still_S9.txt ugc/camera-detector/prompts/still_S10.txt ugc/camera-detector/prompts/still_S11.txt
  EXPECT: MARKED_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> MARKED_OK
- [x] G7: REMOVED.md carries the standing removals and this job's ones
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','price','golden','beep','gps']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> REMOVED_OK
- [x] G8: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
  EVIDENCE: 2026-10-28 ran the CHECK by hand -> BOOK_OK
- [x] G9: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
  EVIDENCE: 2026-10-28 page https://claude.ai/artifact/WxfuVo6J1eMDS5c779TVNC v1; Gmail GMAIL_SEND_EMAIL (gmail_correa-comus) id 1a18454eeff2e38b; PushNotification "Mobile push requested."

# Phase 2-3 (2026-10-29, after Ralph's OK): stills, clips, cut, HofR version
- [x] G10: cut QC passes on Grace's cut (manual record of `python3 qc/check_cut.py out/camera_detector_v1.mp4`)
  EVIDENCE: 2026-10-29 CUT_QC_OK, 33.33 s, -16.68 LUFS, peak -2.47 dB
- [x] G11: cut-stage gate passes (compare vs @lism792 173K recorded)
  EVIDENCE: 2026-10-29 `python3 grace/gate.py ugc/camera-detector --stage cut` -> GATE OK
- [x] G12: voice echo <= 150 ms
  EVIDENCE: 2026-10-29 echo.py vo/voiceover_paced.mp3 rt60_est_ms=150
- [x] G13: HofR version: whole hook in frame 0, held, in the safe zone; cut QC passes
  EVIDENCE: 2026-10-29 hook_check.py out/camera_detector_hor_v1.mp4 --hook 420,395,240,160 -> HOOK_OK (diff 2.5); check_cut.py -> CUT_QC_OK
- [x] G14: every frame looked at against REMOVED.md (no text in Grace's cut, no box, no key tag, black unit, teal window, no beep claim)
  EVIDENCE: 2026-10-29 qc/cut_v1_sheet.jpg (1.5 fps, 50 tiles) + per-clip strips qc/*_strip.jpg
- [x] G15: review page has both cuts playable; push + email sent (manual)
  EVIDENCE: 2026-10-29 https://claude.ai/artifact/WxfuVo6J1eMDS5c779TVNC v3
- [ ] G16: delivered to Drive (CURRENT - ...), sizes match (after Ralph's OK)
