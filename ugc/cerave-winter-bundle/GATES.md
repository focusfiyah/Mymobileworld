# Gates: CeraVe Winter Skin Bundle, plan stage (2026-11-02)

OWNS: ugc/cerave-winter-bundle/**

Scope: the plan Ralph approves before any spend: script gate passed, 5 linted prompts with real references, a spoken script for later, BOOK.md with one total, sent on a review page with push + email.

- [x] G1: script gate passes (all PLAYBOOK §4 proofs newer than the script)
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/cerave-winter-bundle
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=d47e6d0a39699b44eab6a0032e22588003e803b07cbf135f117ebb5253b22734; exit=0; EXPECT=matched; output-sha256=6b0b104a30fc8aa0523456949ea9e7990e8d11d578e386f7ed202d7c6d16660c; output-bytes=166; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cerave-winter-bundle; path=7f4fb4b02918/15 entries

- [x] G2: every still and clip prompt passes the lint
  CHECK: cd /home/user/Mymobileworld && python3 grace/prompt_check.py lint ugc/cerave-winter-bundle/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c714dee3ddfe2723b55608d7e282723e3416ae4a56b032877db7352b569c8981; exit=0; EXPECT=matched; output-sha256=5c4f728c7c01f694f1f5cd0ff2c5c73b84f583e2b6210c48e82bf87254d8a796; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cerave-winter-bundle; path=7f4fb4b02918/15 entries

- [x] G3: every shot shows all four products and every reference file exists
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && python3 -c "import json,os;S=json.load(open('shots.json'));bad=[r for s in S for r in s['still_refs']+s['clip_refs'][1:] if not os.path.exists(r)];four=['Hydrating Facial Cleanser','AM Facial Moisturizing Lotion','Intensive','Healing Lip Balm'];w=[s['id'] for s in S if (s['group'] and not all(x in s['still'] for x in four)) or (not s['group'] and any(x in s['still']+s['clip'] for x in four[1:]))];n=sum(not s['group'] for s in S);print(len(S),n,bad,w);print('REFS_OK' if len(S)==5 and n==3 and not bad and not w else 'REFS_BAD')"
  EXPECT: REFS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=043ecfd176b3809847dc071a209d0e9ab4dd4cd161f938685ce014c277341a1a; exit=0; EXPECT=matched; output-sha256=8762901f7ea962c5c6f3985ce66257373b68f0b17fb9e61f0cb74cc20374b730; output-bytes=16; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cerave-winter-bundle; path=7f4fb4b02918/15 entries

- [x] G4: spoken script readability grade <= 6
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && python3 ../../.claude/skills/tiktok-shop-coach/scripts/tiktok.py readability scripts.md | python3 -c "import re,sys;g=float(re.search(r'Kincaid\): ([0-9.]+)',sys.stdin.read()).group(1));print('GRADE_OK' if g<=6 else 'GRADE_HIGH',g)"
  EXPECT: GRADE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a3a360f509f9506d51c40c45042a178106ba1d00c093c48c62d6168a2b377f3e; exit=0; EXPECT=matched; output-sha256=db90974d897a3b57460546ca506bb1170ce7d4f9b833be16661cc7c61667e9d8; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cerave-winter-bundle; path=7f4fb4b02918/15 entries

- [x] G5: BOOK.md has one TOTAL line and a Sent to Ralph line with a link
  CHECK: cd /home/user/Mymobileworld/ugc/cerave-winter-bundle && python3 -c "import re;b=open('BOOK.md').read();t=re.findall(r'(?m)^TOTAL: [$][0-9.]+$',b);s=re.findall(r'(?m)^Sent to Ralph: https://claude.ai/artifact/',b);print('BOOK_OK' if len(t)==1 and len(s)==1 else 'BOOK_BAD',len(t),len(s))"
  EXPECT: BOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=cd66e5ca68b35bd7f7720276a6fb7a5cdd31049d9bfeacb374976c2d708ba767; exit=0; EXPECT=matched; output-sha256=314bbafde5738464b38ec428c336d2f4d81df67001a874147b94a34a7f904ea8; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cerave-winter-bundle; path=7f4fb4b02918/15 entries

- [ ] G6: review page shows the storyboard, script, product sheet, room and hand sheet; Ralph notified by push + email
  EVIDENCE: v1 2026-11-02 review page https://claude.ai/artifact/MsGgDxqTuqxumSVXt4aH4m v1 (sections Total, Questions, Spoken script, Storyboard S1-S6 with prompts, References: sheet, room, both hand sheets); PushNotification "Mobile push requested"; Gmail sent id 1a19df46a55dda46
