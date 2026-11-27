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
- [x] G5: HofR V1 hook card whole in frame 0 and held (hook_check)
  CHECK: python3 /home/user/Mymobileworld/tools/hookcheck/hook_check.py out/hofr/watch_hofr_v1.mp4 --hook 130,400,800,190
  EXPECT: HOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=280312b085e7e4356a5e578571b7362ca5b2f0ba489425a96138a90f86013723; exit=0; EXPECT=matched; output-sha256=f8290acb6b1e144b8c67e65e89a58dee059e346a5b6c42dcdb243115687f0407; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G6: HofR VO readback matches every script line (punctuation aside)
  CHECK: python3 -c "import json,re;n=lambda s:re.sub(r'[^a-z ]','',s.lower()).split();L=[l for l in open('hofr/vo/lines.txt').read().splitlines() if l.strip()];W=json.load(open('hofr/vo/words.json'))['lines'];print('VO_MATCH' if len(L)==len(W) and all(n(a)==n(b['text']) for a,b in zip(L,W)) else 'VO_DIFF')"
  EXPECT: VO_MATCH
  EVIDENCE: automatic-evidence=v1; definition-sha256=9cf39433bba01dcbc1724ce401060674532bfec779ac9e88d179c13398aebead; exit=0; EXPECT=matched; output-sha256=c7633e890dcdb2c5cc5c3475711fd16bdd198bde34ae477f5813c6695e93f176; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G7: HofR shot windows never reuse the same seconds of her take
  CHECK: python3 -c "import json;L=json.load(open('hofr/vo/words.json'))['lines'];s=[27.0,19.3,6.9,2.4,35.4,23.6,39.72,15.0,33.0];d=[((L[i+1]['start'] if i+1<len(L) else L[i]['end']+0.5)-L[i]['start'])/1.08 for i in range(len(L))];d[0]+=0.1;v=sorted((a,a+b) for a,b in zip(s,d));print('NO_OVERLAP' if all(v[i][1]<=v[i+1][0] for i in range(len(v)-1)) and v[-1][1]<=43.187 else 'OVERLAP')"
  EXPECT: NO_OVERLAP
  EVIDENCE: automatic-evidence=v1; definition-sha256=98010b76f3d48fc42140be38871217ba44026bb315f8843097683061defd1b87; exit=0; EXPECT=matched; output-sha256=cb06039bc49f73ae005d31f6dbbd92a13b32498da5622c44d711b53cad68e21e; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/iced-out-watch; path=ce7df1b67db3/16 entries
- [x] G8: HofR review page published, Ralph notified (manual)
  EVIDENCE: https://claude.ai/artifact/NMabmiqiS7RJWgMQhynCF6 published 2026-11-27; push + email 1a21a7045194e05b + Telegram msg 856 to Ralph.
