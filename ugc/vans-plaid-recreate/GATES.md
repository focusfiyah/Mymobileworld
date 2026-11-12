# Gates: Vans Plaid Old Skool, 2 shot-for-shot recreations (Grace's skin tone)

- [x] G1: script gate passes for the plan
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-plaid-recreate
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ba5034a4a153ada2dc2091c9507e61a0f36c76f1f0aebe9c7bcb1c6b1f212df6; exit=0; EXPECT=matched; output-sha256=503f24bed50be9341dd0de4f663afbc1b77404f43405b04b5e184faf32ad3fbd; output-bytes=86; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
- [x] G2: every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/vans-plaid-recreate/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5d41be399e5c1fe2297fc02e91844e50695c2faeef507a0080e357caaf3c75f7; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
- [x] G3: 5 shots planned, windows match the originals' cut times (V1 0-7.42; V2 0-2.1, 2.1-3.47, 3.47-5.57, 5.57-7.97)
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import json;S=json.load(open('shots.json'));w=[tuple(S[k]['window']) for k in ['V1S1','V2S1','V2S2','V2S3','V2S4']];print('SHOTS_OK' if w==[(0.0,7.42),(0.0,2.1),(2.1,3.47),(3.47,5.57),(5.57,7.97)] else w)"
  EXPECT: SHOTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b079267b44b6792692a7cc4aa2ac41e14cd242b71c097e76f91c320200253685; exit=0; EXPECT=matched; output-sha256=700c872acf04d834a37cb04f99353c2a855be2097154d9e9c53a93be6ca69ab4; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
- [x] G4: Ralph's OK recorded on the plan before any paid call (manual: --approve-book with his tapped words)
  EVIDENCE: Ralph tapped "Approve, $2.70 (Recommended)" 2026-11-12; gate.py BOOK APPROVED $2.70 + extra $0.45 (his tap)
- [x] G5: 5 stills downloaded, each 9:16
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import glob;from PIL import Image;f=glob.glob('stills/V?S?.png');ok=[x for x in f if abs(Image.open(x).size[0]/Image.open(x).size[1]-9/16)<0.02];print('STILLS_OK' if len(ok)==5 else f'{len(ok)} of 5')"
  EXPECT: STILLS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2dd100a579c55d6e2998ed0924459e1c2fd5188097b2c16b3e1ab71f84b4a151; exit=0; EXPECT=matched; output-sha256=3e4cefd4e84028c7541d488567d9183bc4f81181266f3f1ef912b44d4960d51b; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
- [x] G6: stills QC'd at 2x (Grace's skin tone on every hand/foot, real plaid/stripe/eyelets/insole logo/heel label, held shoe = other foot's shoe, max 2 shoes, whole wrists, no text) and storyboard sent (manual)
  EVIDENCE: 5 stills checked at 2x (skin, plaid, stripe, eyelets, insole logo, heel labels, held shoe = right shoe, 2 shoes max); storyboard rounds 1-3 on review page v2-v4
- [x] G7: 2 cuts rendered at 1080x1920, V1 7.4 s and V2 8.0 s (+-0.1)
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import subprocess;r={n:subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height:format=duration','-of','csv=p=0',f'out/{n}.mp4'],capture_output=True,text=True).stdout.split() for n in ['V1','V2']};ok=all(r[n] and r[n][0]=='1080,1920' for n in r) and abs(float(r['V1'][1])-7.42)<0.1 and abs(float(r['V2'][1])-7.97)<0.1;print('CUTS_OK' if ok else r)"
  EXPECT: CUTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=f385dd4b414e3e851e1ce73ff3eea388b9c77f30d4b8eb59efd58e20b7db6457; exit=0; EXPECT=matched; output-sha256=2d4f718d2719eaa1a3c77703b75c5837a814a3f128ef9fb997f420c4c8562304; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
- [x] G8: every cut checked frame by frame (no shoe flip, no grip switch, drift), 2x edges, against REMOVED.md, AI finish applied (manual)
  EVIDENCE: V1 at 12 fps, V2 windows at 24 fps (cut before V2S1 grip jump 1.96 s and V2S2 leg kick 1.25 s); 2x edges clean; REMOVED.md check appended; ai_finish.sh in cut.py; CUTQC_OK both
- [x] G9: Ralph OK'd the cuts, then Drive holds CURRENT - Vans Plaid V1/V2 + captions doc in the product folder, link sent (manual)
  EVIDENCE: Ralph 2026-11-12 'Both are approved'; Drive folder 148Qm6tI0MEpgUQp7F-g4ZmitxwMYZlwK holds CURRENT - Vans Plaid V1.mp4 (32567466 B) + V2.mp4 (37702860 B) + captions doc, sizes match; anyone-with-link writer; Telegram msg 489 to Grace's group
- [x] G10: spend stays inside the book total
  CHECK: cd /home/user/Mymobileworld && python3 grace/spend.py 2>&1 | python3 -c "import sys,re;t=sys.stdin.read();m=re.search(r'ugc/vans-plaid-recreate\s+\\$\s*([0-9.]+)',t);v=float(m.group(1)) if m else 0.0;print('SPEND_OK' if v<=2.70 else v)"
  EXPECT: SPEND_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=660d428f007a46036300b41b94dc8169592dc84a661cc7c21c926ff3b3c63c65; exit=0; EXPECT=matched; output-sha256=fc09867b9850cadcd6dbb44f8f062fa5d0f9fd00389375932440afac6b432a83; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/vans-plaid-recreate; path=7f4fb4b02918/15 entries
