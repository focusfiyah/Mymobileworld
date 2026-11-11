# Gates: Vans sequin V18-V37 (20 music-only videos, 16 s)

- [ ] G1: script gate passes for the plan
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/vans-v18
  EXPECT: GATE OK
- [ ] G2: every still and clip prompt passes the prompt lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/vans-v18/shots.json
  EXPECT: PROMPT_LINT_OK
- [ ] G3: 100 shots planned, 5 per video, 20 videos
  CHECK: cd /home/user/Mymobileworld/ugc/vans-v18 && python3 -c "import json,collections;S=json.load(open('shots.json'));c=collections.Counter(s['video'] for s in S.values());print('SHOTS_OK' if len(S)==100 and len(c)==20 and set(c.values())=={5} else 'BAD')"
  EXPECT: SHOTS_OK
- [ ] G4: Ralph's OK recorded on the plan before any paid call (manual: --approve-book with his tapped words)
- [ ] G5: 100 stills downloaded, each 9:16
  CHECK: cd /home/user/Mymobileworld/ugc/vans-v18 && python3 -c "import glob;from PIL import Image;f=glob.glob('stills/*.png');ok=[x for x in f if abs(Image.open(x).size[0]/Image.open(x).size[1]-9/16)<0.02];print('STILLS_OK' if len(ok)==100 else f'{len(ok)} of 100')"
  EXPECT: STILLS_OK
- [ ] G6: stills QC'd at 2x (side tab black with white VANS, checkerboard toe, held shoe = other foot's shoe, max 2 shoes, hands whole, no text) and storyboard sent (manual)
- [ ] G7: 20 cuts rendered, each 16 s, 1080x1920
  CHECK: cd /home/user/Mymobileworld/ugc/vans-v18 && python3 tools/cutqc.py --len 16
  EXPECT: CUTS_OK
- [ ] G8: every cut checked against REMOVED.md, drift strip and 2x edges, AI finish applied (manual)
- [ ] G9: Ralph OK'd the cuts, then Drive "Vans sequin (Grace)" holds CURRENT - Vans V18..V37 and the captions doc (manual)
- [ ] G10: job media packed to Drive
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check
  EXPECT: MEDIA_OK
