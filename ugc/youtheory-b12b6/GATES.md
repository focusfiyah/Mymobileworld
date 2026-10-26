# Youtheory B12B6 Liquid (Grace), 2026-10-26, phase 1: research + script gate + plan (no paid calls)

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-b12b6
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3c0e318b5161a7e15a05dd3a177c4485b3979154e048e82219cdee5d8fdf2639; exit=0; EXPECT=matched; output-sha256=86ce11b5c0da215cf6c1423bee611cdf124d00e87aa3a39db46cb5948ae86c0f; output-bytes=86; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G2: readability grade of V1 is 6 or lower
  CHECK: python3 -c "import re;g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('GRADE_OK' if g<=6 else 'BAD',g)"
  EXPECT: GRADE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=0db271c5c504dde6199a19befc349e83b7867670aa4d69b70e2e16bf5d82f4f8; exit=0; EXPECT=matched; output-sha256=7abe1e1f07d2bfd184649e2a5bb17226cff6fa6d85f86926d852edcfce16537e; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G3: product sheet built from the real photos (>= 1500 px) and every close-up exists
  CHECK: python3 -c "import os;from PIL import Image;ok=all(os.path.exists(f) for f in ['refs/closeup_F.png','refs/closeup_G.png','refs/closeup_box.png','refs/real/grace_pouch_front_flat.jpg']);im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a90371bdeab90eb4da4137ccab9335dd554f06f0cdcf19e0687496a48f8b657a; exit=0; EXPECT=matched; output-sha256=ee4334ff32a20f4ded64e842cf0fd5eb903364afd41a599874ad3e592aca5845; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G4: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, no Kling; straw prompts on straw shots and the as-sold block on the others (Ralph 2026-10-26)
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['videos'][0]['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and not any(x['model']=='kling' for x in s) and all(('white paper straw stands' in open('prompts/still_'+x['id']+'.txt').read())==x['straw'] and ('AS SOLD' in open('prompts/still_'+x['id']+'.txt').read())==(not x['straw']) for x in s);print('MIX_OK' if ok else 'BAD',f)"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=9e1b9c7fc97ce33bcee4fa5600261ce980a2b4a4a98580a05414e6cc2cc91f1b; exit=0; EXPECT=matched; output-sha256=c5af9ce895b459310b727e3c5b65c251d255ea2f047fb7849a06fc9b019940f2; output-bytes=26; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G5: every still, Omni and Seedance prompt passes the prompt lint (product truth included)
  CHECK: cd ../.. && python3 -c "import json,subprocess,glob,os;r=json.load(open('ugc/youtheory-b12b6/prompts/refs.json'));n=lambda f:1 if f.endswith('_seedance.txt') else len(r[os.path.basename(f)[:-4].replace('still_','')]['still_refs' if 'still_' in f else 'clip_refs']);bad=[f for f in sorted(glob.glob('ugc/youtheory-b12b6/prompts/*.txt')) if 'PROMPT_LINT_OK' not in subprocess.run(['python3','grace/prompt_check.py','lint',f,'--refs',str(n(f))],capture_output=True,text=True).stdout];print('LINT_ALL_OK' if not bad else bad)"
  EXPECT: LINT_ALL_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2f1e0e2cca29714e9df63754dc96b9afdce8d7af5940a53a78710aa0628415d8; exit=0; EXPECT=matched; output-sha256=e407c69457474654cebb392e7b6c48c0d96b954e80c965e88d5f074a7efd36b9; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G6: REMOVED.md carries the standing removals, the listing-only line and the straw rule
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','essential daily vitamins','straw']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=91cfaa28ca94aefa912e6d6e1a912f8ea87a90ca1d0ab0f8c4952948322a992b; exit=0; EXPECT=matched; output-sha256=fdd0ffce6701454c76a66b240abb2c3bf4ad8cf481d672c18ea787906a38db7a; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G7: BOOK.md written with one TOTAL line
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 else 'NO')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f03ea59c647acbbff7ea47cefe55fd670890949bf372b068a64b8d97c0f413a2; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G8: review page published with script, sheet, shot list, prompts and the total; push + email sent (manual)
  EVIDENCE: plan + storyboards + clips on review page https://claude.ai/artifact/LvrMBi3CNvBuXW4MCHv16j (v1-v9); push + email at every stop (Gmail ids 1a17618fc95ce856, 1a17636f71e4aaa7, 1a17642511911d49, 1a176578b6dd56b0, 1a1765aac64a93e7, 1a17665ec339f975, 1a1766a09bac9dc9, 1a1766ec4542b0f6, 1a17684ec7ccd3b4)

# Phase 2: production (stills r2-r8, Seedance first-frame clips, cut v1)

- [x] G9: cut-stage gate passes (coach compare, no text overlay)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-b12b6 --stage cut
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=6a09d772055d6ff2dddae7ebd150fb2333148338929e8f4de3e2d13b88b438bd; exit=0; EXPECT=matched; output-sha256=86ce11b5c0da215cf6c1423bee611cdf124d00e87aa3a39db46cb5948ae86c0f; output-bytes=86; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G10: final is 1080x1920, 18-25 s, audio at -16 +/- 1 LUFS
  CHECK: python3 -c "import subprocess,re;f='out/youtheory_b12b6_v1.mp4';p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,codec_type:format=duration','-of','compact',f],capture_output=True,text=True).stdout;d=float(re.search(r'duration=([0-9.]+)',p).group(1));e=subprocess.run(['ffmpeg','-nostats','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr;i=float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',e)[-1]);ok='width=1080|height=1920' in p and 'audio' in p and 18<=d<=25 and abs(i+16)<=1;print('FINAL_OK' if ok else 'BAD',d,i)"
  EXPECT: FINAL_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=1a8f9632e8c27a43a2eaff6e5639029e8a04e511c2fe8c159390c1d917fc7410; exit=0; EXPECT=matched; output-sha256=bc45b421dc3550baeea571615d39115e72a877f0d54fd937b2759204f1d96959; output-bytes=25; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G11: no freeze longer than 0.6 s and no black frames
  CHECK: python3 -c "import subprocess;e=subprocess.run(['ffmpeg','-nostats','-i','out/youtheory_b12b6_v1.mp4','-vf','freezedetect=n=0.002:d=0.6,blackdetect=d=0.1','-f','null','-'],capture_output=True,text=True).stderr;print('MOTION_OK' if 'freeze_start' not in e and 'black_start' not in e else 'BAD')"
  EXPECT: MOTION_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c441bf7525422f9b34fe530059323e19006096b2e97625fa56253454b2ae37ea; exit=0; EXPECT=matched; output-sha256=ad059e15b7d9efc8db91020748da25e4bd250aeedaca7e644e16bc7ac157fdef; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G12: voiceover echo gate <= 150 ms
  CHECK: cd ../.. && python3 grace/voice/echo.py ugc/youtheory-b12b6/vo/voiceover_paced.mp3 | python3 -c "import sys,re;v=int(re.search(r'rt60_est_ms=(\d+)',sys.stdin.read()).group(1));print('ECHO_OK' if v<=150 else 'BAD',v)"
  EXPECT: ECHO_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c2825cff25af1e2ecf0eb2509e5ac225c492c94a5542a12133739c654bbc7eb8; exit=0; EXPECT=matched; output-sha256=17ac3e11ae85c2e84c56957e9352a9fecd9bd43909637e02422de4d2547a697b; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G13: AI finish in the final render (grain + sharpen + saturation 0.92)
  CHECK: python3 -c "t=open('cut.py').read();print('FINISH_OK' if 'noise=alls=6' in t and 'saturation=0.92' in t and 'youtheory_b12b6_v1.mp4' in t else 'BAD')"
  EXPECT: FINISH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5faacbb7a0efc5c2b435824e9aca07ed3fc76496b2fca556b1e63e7b077a5207; exit=0; EXPECT=matched; output-sha256=df6d03e30a61feecfc415434513e258ad057ca50f7d81ca774ffa2b4dcd6898d; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-b12b6; path=7f4fb4b02918/15 entries
- [x] G14: every element checked against REMOVED.md + 2x print/hand QC (manual; qc/cut_sheet.jpg)
  EVIDENCE: REMOVED.md list checked on qc/cut_sheet.jpg + clip frames: no text/captions/cards, no Ken Burns, no freeze/black (G11), no screw cap/spout/lid, no "essential daily vitamins", straw only S5-S8 with neck whole, S1-S4 + S9 as sold; prints 2x: S7 + S9 real lines (Ralph OK), S6 box drifts after 2 s (cut at 2.43 s, Ralph OK), S9 glare avoided (first 1.3 s); hands 2x clean (S1, S3, S5, S9), one hand per shot
- [ ] G15: Ralph approves cut v1 (manual)
- [ ] G16: final + script doc in Drive "Grace Tiktok assets/Youtheory B12B6 (Grace)" as CURRENT, link in README + reply (manual)
