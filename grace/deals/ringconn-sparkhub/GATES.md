# Gates: RingConn / SparkHub offer answer for Grace

OWNS: grace/deals/ringconn-sparkhub/**

Scope: legitimacy verdict, rate, humanized reply, all sent to Grace on Telegram with done, plus Brain note.

- [x] G1: reply has rate, 30-day code, review rounds, the four questions, email and portfolio link, no dashes
  CHECK: python3 -c "t=open('reply.txt').read();import sys;need=['\$450','30 days','2 rounds','model','timeline','payment','agreement','graceglows.ugc@gmail.com','gracewiththeglow.netlify.app'];m=[n for n in need if n not in t];bad=[c for c in '—–' if c in t];print('REPLY_OK' if not m and not bad else ('MISSING',m,bad))"
  EXPECT: REPLY_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8186c100b35d6b649ef752d1010c0b07384486c6fd4d2c90c1438ab1431eb9c5; exit=0; EXPECT=matched; output-sha256=2ff389349f9f4fa099e1c7168b9b6654f688afffe389433da657db2c9de522a3; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/grace/deals/ringconn-sparkhub; path=7f4fb4b02918/15 entries

- [x] G2: Telegram done message sent to Grace in group -5234107715 (message id logged in sent.log)
  CHECK: python3 -c "import re;t=open('sent.log').read();print('SENT_OK' if re.search(r'done_msg_id=\d+',t) else 'NO')"
  EXPECT: SENT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=41833fac0934d93a4e4979686983a2198bfc0e40b6dd4e3b01fd9a2fea3d553d; exit=0; EXPECT=matched; output-sha256=77d46f61cccee7a708892be0c433f2d0a190e2e5ba494e53a290b6c4dcf802a0; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/grace/deals/ringconn-sparkhub; path=7f4fb4b02918/15 entries

- [x] G3: Brain note pushed and tools/brain/check.py prints BRAIN_OK
  EVIDENCE: BRAIN_OK (343 notes, terms found) 2026-11-09, vault pushed to main
