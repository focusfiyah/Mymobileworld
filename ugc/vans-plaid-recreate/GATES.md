# Gates: Vans Plaid Old Skool, 2 shot-for-shot recreations (Grace's skin tone)

- [ ] G1: script gate passes for the plan
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-plaid-recreate
  EXPECT: GATE OK
- [ ] G2: every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/vans-plaid-recreate/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G3: 5 shots planned, windows match the originals' cut times (V1 0-7.42; V2 0-2.1, 2.1-3.47, 3.47-5.57, 5.57-7.97)
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import json;S=json.load(open('shots.json'));w=[tuple(S[k]['window']) for k in ['V1S1','V2S1','V2S2','V2S3','V2S4']];print('SHOTS_OK' if w==[(0.0,7.42),(0.0,2.1),(2.1,3.47),(3.47,5.57),(5.57,7.97)] else w)"
  EXPECT: SHOTS_OK
- [ ] G4: Ralph's OK recorded on the plan before any paid call (manual: --approve-book with his tapped words)
- [ ] G5: 5 stills downloaded, each 9:16
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import glob;from PIL import Image;f=glob.glob('stills/V?S?.png');ok=[x for x in f if abs(Image.open(x).size[0]/Image.open(x).size[1]-9/16)<0.02];print('STILLS_OK' if len(ok)==5 else f'{len(ok)} of 5')"
  EXPECT: STILLS_OK
- [ ] G6: stills QC'd at 2x (Grace's skin tone on every hand/foot, real plaid/stripe/eyelets/insole logo/heel label, held shoe = other foot's shoe, max 2 shoes, whole wrists, no text) and storyboard sent (manual)
- [ ] G7: 2 cuts rendered at 1080x1920, V1 7.4 s and V2 8.0 s (+-0.1)
  CHECK: cd /home/user/Mymobileworld/ugc/vans-plaid-recreate && python3 -c "import subprocess;r={n:subprocess.run(['ffprobe','-v','error','-select_streams','v','-show_entries','stream=width,height:format=duration','-of','csv=p=0',f'out/{n}.mp4'],capture_output=True,text=True).stdout.split() for n in ['V1','V2']};ok=all(r[n] and r[n][0]=='1080,1920' for n in r) and abs(float(r['V1'][1])-7.42)<0.1 and abs(float(r['V2'][1])-7.97)<0.1;print('CUTS_OK' if ok else r)"
  EXPECT: CUTS_OK
- [ ] G8: every cut checked frame by frame (no shoe flip, no grip switch, drift), 2x edges, against REMOVED.md, AI finish applied (manual)
- [ ] G9: Ralph OK'd the cuts, then Drive holds CURRENT - Vans Plaid V1/V2 + captions doc in the product folder, link sent (manual)
- [ ] G10: spend stays inside the book total
  CHECK: cd /home/user/Mymobileworld && python3 grace/spend.py 2>&1 | python3 -c "import sys,re;t=sys.stdin.read();m=re.search(r'ugc/vans-plaid-recreate\s+\\$\s*([0-9.]+)',t);v=float(m.group(1)) if m else 0.0;print('SPEND_OK' if v<=2.70 else v)"
  EXPECT: SPEND_OK
