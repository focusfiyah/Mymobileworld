# SoFyre v2 gates (plan stage, 2026-10-15)

- [x] G1: script gate passes for Ralph's 3 scripts
  CHECK: python3 ../../grace/gate.py .
  EXPECT: GATE OK

- [x] G2: reference sheet saved with its 6 views
  CHECK: python3 -c "import glob;print('views', len(glob.glob('refs/view_*.jpg')))"
  EXPECT: views 6

- [x] G3: shot VO lines spell each script word for word
  CHECK: python3 -c "import json,re;J=json.load(open('shots.json'));t=open('scripts.md').read();n=lambda x:re.sub(r'\W','',x.lower());print('MATCH' if all(n(' '.join(s['vo'] for s in J['shots'] if s['vid']==v)) in n(t) for v in ('V1','V2','V3')) else 'DIFF')"
  EXPECT: MATCH

- [x] G4: quote equals 20 stills + 89 s of clips
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];print(round(0.09*len(s)+0.041*sum(x['dur'] for x in s),3))"
  EXPECT: 5.449

- [x] G5: every end shot shows ONE bag
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];e=[[x for x in s if x['vid']==v][-1] for v in ('V1','V2','V3')];print('ONEBAG' if all('One bag only' in x['video'] for x in e) else 'NO')"
  EXPECT: ONEBAG
