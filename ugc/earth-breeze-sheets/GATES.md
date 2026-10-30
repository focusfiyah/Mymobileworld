# Earth Breeze Laundry Detergent Sheets (Grace), 2026-10-30, phase 1: research + script gate + plan (no paid calls)

Ralph's choices (2026-10-30): my script + Grace cloned v5 voice, 1 video 15-20 s, Kie only (no Flow), product facts and sheet from the 8 listing images.

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/earth-breeze-sheets
  EXPECT: GATE OK
- [x] G2: readability grade of the script is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
- [x] G3: script is 38-60 spoken words (15-20 s at Grace's pace) and closes in the orange cart
  CHECK: python3 -c "import re;t=open('scripts.md').read();s=t.split('## Spoken')[1].split('##')[0];w=len(re.findall(r\"[A-Za-z0-9']+\",s));print('LEN_OK' if 38<=w<=60 and 'orange cart' in s.lower() else 'BAD',w)"
  EXPECT: LEN_OK
- [x] G4: product sheet built from the listing photos (>= 1500 px) and product_truth.json has photos, facts and forbid
  CHECK: python3 -c "import json;from PIL import Image;t=json.load(open('product_truth.json'));im=Image.open('refs/product_sheet.png');print('SHEET_OK' if t.get('photos') and t.get('facts') and t.get('forbid') and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
- [x] G5: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and not any(x['model']=='kling' for x in s);print('MIX_OK' if ok else 'BAD',f)"
  EXPECT: MIX_OK
- [x] G6: every still and clip prompt passes the prompt lint (product truth included)
  CHECK: cd ../.. && python3 -c "import json,subprocess,glob;r=json.load(open('ugc/earth-breeze-sheets/prompts/refs.json'));bad=[f for f in sorted(glob.glob('ugc/earth-breeze-sheets/prompts/*.txt')) if 'PROMPT_LINT_OK' not in subprocess.run(['python3','grace/prompt_check.py','lint',f,'--refs',str(r[f.split('/')[-1]])],capture_output=True,text=True).stdout];print('LINT_ALL_OK' if not bad else bad)"
  EXPECT: LINT_ALL_OK
- [x] G7: REMOVED.md carries the standing removals
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','price','box picture']) else 'NO')"
  EXPECT: REMOVED_OK
- [x] G8: BOOK.md written with one TOTAL line
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 else 'NO')"
  EXPECT: BOOK_OK
- [x] G9: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
  EVIDENCE: https://claude.ai/artifact/Atwr5b9T6LruEECtf5T7Zr v1; push requested; Gmail id 1a18b370ef105dd8. G1-G8 run by hand 2026-10-30 (CHECK lines not approved in unlazy, per Ralph): all 8 MET

# Phase 2: production (stills, clips, VO, cut v1 + HofR)
- [x] G10: cut-stage gate passes (coach compare, text only in the HofR cut with Ralph's words)
  EVIDENCE: `python3 grace/gate.py ugc/earth-breeze-sheets --stage cut` -> GATE OK (2026-10-30)
- [x] G11: final 1080x1920, 15-20 s, audio -16 +/- 1 LUFS, no freeze or black
  EVIDENCE: out/earth_breeze_v1.mp4 1080x1920, 17.17 s, -17.0 LUFS, freezedetect/blackdetect none
- [x] G12: voice echo <= 150 ms
  EVIDENCE: grace/voice/echo.py vo/voiceover_paced.mp3 rt60_est_ms=150
- [x] G13: every cut on its line (scene cuts within 0.1 s of the shot starts)
  EVIDENCE: cuts 2.77 5.27 6.8 9.0 9.83 10.8 12.9 15.5 vs 2.74 5.26 6.78 8.98 9.78 10.72 12.82 15.44: SYNC_OK
- [x] G14: HofR hook readable from frame 0, held 2 s, in the safe zone
  EVIDENCE: tools/hookcheck/hook_check.py out/earth_breeze_hor_v1.mp4 --hook 250,410,580,210 -> HOOK_OK
- [x] G15: REMOVED.md + 2x QC (hands, edges, first second, prints) (manual)
  EVIDENCE: qc/ strips; S8 small-print slip flagged to Ralph, not fixed (no spend); washer logos cropped/blurred free
- [ ] G16: Ralph approves cut v1 (manual)
- [ ] G17: final + script doc in Drive "Grace Tiktok assets/Earth Breeze ... (Grace)" as CURRENT (manual)
