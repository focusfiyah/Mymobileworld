# GATES: Iced Out Watch, Grace msg 842 reply

- [x] G1: Script has no banned words (reviewer, label says, order it now, automatic, diamond, Cartier, price digits, dashes)
  CHECK: python3 -c "import re;t=open('script.md').read().split('## Script')[1].lower();bad=[w for w in ['review','label says','order it now','automatic','diamond','cartier','$','—',' - '] if w in t]+re.findall(r'\d',t);print('CLEAN' if not bad else bad)"
  EXPECT: CLEAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=6c78d42ec48db2bd845d8e5de18e0838bf536ed5e7e20a22355bbf302cefd694; exit=0; EXPECT=matched; output-sha256=0b98843240a0b1a2384483206c02be8968dd809eb73838820be24cb7d6d6aeb9; output-bytes=6; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G2: Each hook matches hooks.json word for word (blanks only filled)
  CHECK: python3 /home/user/Mymobileworld/ugc/iced-out-watch/hookcheck.py
  EXPECT: HOOKS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=876007c183655e5d204c1bf2694aa15aa41ac42ece5f3549d9b13aaa4888cbfd; exit=0; EXPECT=matched; output-sha256=944862c65f05100b001819b4976fff18e286c1fa374192792ec4e5dfe457115a; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G3: Script ends with the close line
  CHECK: python3 -c "print('CLOSE_OK' if open('script.md').read().strip().endswith(\"It's in the orange cart.\") else 'NO')"
  EXPECT: CLOSE_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c9c51978aea8dd85aa1ba09a2b9170ac4e0cac168de18933ff4479f3eca9d58b; exit=0; EXPECT=matched; output-sha256=e4c8ead1b5868fec9c474bd08dc7c96dfe5e47f42744f4bbbd61fdfc5326bf8c; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G4: Telegram: 1 why message + 3 hook pre blocks + 1 script pre block + 1 notes message sent as replies to 842
  CHECK: python3 -c "import json;d=json.load(open('sent.json'));print('SENT_OK' if len(d)==6 and all(x.get('ok') for x in d) else 'NO')"
  EXPECT: SENT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=3db0004d252e58a908e4db60f269bdbb4f4c8a45fa12803313394164249d8e34; exit=0; EXPECT=matched; output-sha256=77d46f61cccee7a708892be0c433f2d0a190e2e5ba494e53a290b6c4dcf802a0; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
