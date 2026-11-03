# GATES: Nello Superfocus round 1 (plan + scripts)

- [x] G1: Script gate passes
  CHECK: cd ../.. && python3 grace/gate.py ugc/nello-superfocus 2>&1 | head -1
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=807b515afacc2be5e104915741602975b6945887b467a311c1d64497ee3a047a; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G2: Both scripts and the caption read at grade 6 or lower
  CHECK: python3 -c "import re;t=open('research/readability.txt').read();g=[float(x) for x in re.findall(r'Grade level \(Flesch-Kincaid\): ([0-9.]+)',t)];print('READ_OK' if len(g)==3 and max(g)<=6 else 'READ_FAIL',g)"
  EXPECT: READ_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7696025bb9baf8f57aa19a46fd6d5b0670f9a5335b98a5c70ce89ba24be59ca6; exit=0; EXPECT=matched; output-sha256=f76116c7e0beaccdc942771245ccc87e8402f9ebb85157b87dcfbf45404bff8e; output-bytes=24; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G3: Both scripts are standard length, 85-105 words (~27-33 s at 3.2 w/s)
  CHECK: python3 -c "n=[len(open(f).read().split()) for f in ('research/v1_script.txt','research/v2_script.txt')];print('LEN_OK' if all(85<=x<=105 for x in n) else 'LEN_FAIL',n)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=4a04411bd7f0d1926383b0337f6bad1830ecf4d587baf1c5d739f188a838de86; exit=0; EXPECT=matched; output-sha256=c1bc752039b9eba736b716b0e3284cc648365dc059f6aac8ff45162ff5ed72f0; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G4: Book has the sent link, a TOTAL and no blanks
  CHECK: python3 -c "t=open('BOOK.md').read();print('BOOK_OK' if 'Sent to Ralph: https://claude.ai/' in t and '2.396' in t.split('TOTAL:')[-1] and '____' not in t else 'BOOK_FAIL')"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=4871358a78a6895f37489e1bd86ce0e8b8c526b8634840ff111d05fc972cada8; exit=0; EXPECT=matched; output-sha256=9e3343135cc993ebad1c7063868498f46d4d79987594dbe5fd96d7c1283ddd4a; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G5: Close line once per script and no banned words or price
  CHECK: python3 -c "t=open('scripts.md').read().lower();bad=[w for w in ['order it now','reviewer','the label says','$','adhd','adderall','heads up'] if w in t];print('WORDS_OK' if not bad and t.count(\"it's in the orange cart\")==2 else ('WORDS_FAIL',bad))"
  EXPECT: WORDS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7f65847723323931fd62381d41c505b4a936c7b727547db7d1b049e2801395cc; exit=0; EXPECT=matched; output-sha256=98ccd398ae5865a23676830a5587ef144b4d896b43e8cff818ec99c2b9eb6c98; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G6: All 12 prompts pass the prompt lint
  CHECK: python3 ../../grace/prompt_check.py lint shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=07a95a46b40cb6de9f4fef1fb408028b9367814cc51eed67b882e882415f04b7; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G7: Every reference the prompts name exists on disk and there are 6 shots, 3 hand-free
  CHECK: python3 -c "import json,os;s=json.load(open('shots.json'))['shots'];m=[r for x in s for r in x['still_refs']+[c for c in x['clip_refs'] if not c.startswith('stills/')] if not os.path.exists(r)];h=sum(x['kind']=='HAND-FREE' for x in s);print('REFS_OK' if len(s)==6 and h==3 and not m else ('REFS_FAIL',m,h))"
  EXPECT: REFS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b4b07393f80c4077fa0b7b623d9d9a2a8f9550306d1f41510f0cad637618e1c0; exit=0; EXPECT=matched; output-sha256=2f575726671e2a7928635cea0175d39a9c81b723764725a004f68f3b1c05b071; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G8: No forbidden product detail is described positively (caffeine badge only in a negation)
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['shots'];t=' '.join(x['still']+x['clip'] for x in s);print('TRUTH_OK' if t.count('+ CAFFEINE')==t.count(\"no '+ CAFFEINE' tag\") and 'cherr' not in t and 'pouch or packets' in t else 'TRUTH_FAIL')"
  EXPECT: TRUTH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7a705c3b4bc82e674a8d6a151562cfc04d69fbd56d530de1b15b74a740615541; exit=0; EXPECT=matched; output-sha256=be3a515e39e9388a549ac4fdfd9834edfef39a978001a2cbcd008c643382692e; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
- [x] G9: Review page is the one linked in the Book and README
  CHECK: python3 -c "u='ba19b895-a976-46e2-8404-413ec9044288';print('LINK_OK' if u in open('BOOK.md').read() and u in open('README.md').read() else 'LINK_FAIL')"
  EXPECT: LINK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=23a6bdf7f3af68465526fb645fb562d38c36b5c3324239ac29695d2bd402da93; exit=0; EXPECT=matched; output-sha256=c0dc32111c94098bd34b43b685f868eecc438dabf0aab3cf4a99181702acca07; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/nello-superfocus; path=7f4fb4b02918/15 entries
