# PRITECH V5-V9 (Grace), 2026-10-29: 5 videos on Grace's own VO from https://www.tiktok.com/t/ZPLDRXhd4, different visuals each

OWNS: ugc/pritech-vo5/**

Scope: five 20.9 s hands + hand-free AI videos over Grace's linked VO, each shot matching its words, no shot idea repeated across the five, approved by Ralph and filed in Drive.

# Phase 1: research + gate + plan (no paid calls)
- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability override, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/pritech-vo5
  EXPECT: GATE OK
  EVIDENCE: 2026-10-29 GATE OK (override V5-V9 7.1)
- [x] G2: every still and clip prompt passes the prompt lint
  CHECK: cd ../.. && python3 grace/prompt_check.py lint ugc/pritech-vo5/shots.json
  EXPECT: PROMPT_LINT_OK
  EVIDENCE: 2026-10-29 PROMPT_LINT_OK
- [x] G3: 5 videos x 9 shots, every VO beat covered once per video, 3-4 hand-free per video, no shot id or still prompt reused
  CHECK: python3 -c "import json;s=json.load(open('shots.json'));ok=len(s)==45 and len({x['still'] for x in s})==45;exec(\"for v in 'V5 V6 V7 V8 V9'.split():\n x=[a for a in s if a['video']==v];ok=ok and sorted(a['beat'] for a in x)==list(range(1,10)) and 3<=sum(not a['hand'] for a in x)<=4\");print('SHOTS_OK' if ok else 'BAD')"
  EXPECT: SHOTS_OK
  EVIDENCE: 2026-10-29 SHOTS_OK
- [x] G4: 10 new real rooms with sources, none used in V1-V4
  CHECK: python3 -c "import os,re;a=open('rooms/SOURCES.md').read();b=open('../pritech-15s/rooms/SOURCES.md').read()+open('../pritech-cleansing-brush/rooms/SOURCES.md').read();ids=re.findall(r'= (p[xb]_\d+)',a);print('ROOMS_OK' if len(set(ids))==10 and all(os.path.exists(f'rooms/room_V{v}{k}.jpg') for v in '56789' for k in 'AB') and not any(i in b for i in ids) else 'NO',ids)"
  EXPECT: ROOMS_OK
  EVIDENCE: 2026-10-29 ROOMS_OK (10 ids)
- [x] G5: the VO passes the echo gate (<= 150 ms) and the final VO file is Grace's audio
  CHECK: cd ../.. && python3 grace/voice/echo.py ugc/pritech-vo5/vo/voiceover_final.wav | python3 -c "import sys,re;m=re.findall(r'rt60_est_ms=(\d+)',sys.stdin.read());print('ECHO_OK' if m and int(m[-1])<=150 else 'ECHO_BAD',m)"
  EXPECT: ECHO_OK
  EVIDENCE: 2026-10-29 rt60_est_ms=150
- [x] G6: BOOK.md has one TOTAL line and a Sent to Ralph link
  CHECK: python3 -c "import re;t=open('BOOK.md').read();print('BOOK_OK' if len(re.findall(r'TOTAL: [$][0-9.]+',t))==1 and re.search(r'Sent to Ralph: https://claude\.ai/\S+',t) else 'NO')"
  EXPECT: BOOK_OK
  EVIDENCE: 2026-10-29 BOOK_OK
- [x] G7: review page published with the VO, shot lists, rooms and the total; push + email sent
  EVIDENCE: 2026-10-29 page https://claude.ai/artifact/V7f83RDGV3AqyAMYNQXDbt v1; Gmail 1a185abf6b712825; push 'Mobile push requested.'

# Phase 2+ (after Ralph's OK): stills -> storyboard -> clips -> cuts -> Drive
- [ ] G8: every still used passes 2x QC (product shape, buttons, chrome end, rings, grip, no eyes/mouth) before its clip is paid for
  EVIDENCE: pending
- [ ] G9: 5 cuts out/pritech_V5..V9.mp4, each within 0.15 s of the 20.9 s VO
  CHECK: python3 -c "import subprocess;d=[float(subprocess.run(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',f'out/pritech_V{v}.mp4'],capture_output=True,text=True).stdout or 0) for v in range(5,10)];print('CUTS_OK' if all(abs(x-20.95)<=0.15 for x in d) else 'BAD',d)"
  EXPECT: CUTS_OK
  EVIDENCE: pending
- [ ] G10: cut gate (compare vs the top winner) passes
  CHECK: cd ../.. && python3 grace/gate.py ugc/pritech-vo5 --stage cut
  EXPECT: GATE OK
  EVIDENCE: pending
- [ ] G11: every cut QC'd (2x edges, first second, REMOVED.md, flash/levels), AI finish applied, Ralph approved
  EVIDENCE: pending
- [ ] G12: Drive "PRITECH Face Scrubber (Grace)" has CURRENT - PRITECH V5..V9 + script doc, sizes match; brain check BRAIN_OK; branch merged to main
  EVIDENCE: pending
