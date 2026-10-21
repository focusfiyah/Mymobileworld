# Cleanwaste Portable Toilet Bags (Grace), 2026-10-21, phase 1: research + script gate + plan (no paid calls)

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/cleanwaste-toilet-kit
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ec6a63b92366ae69c4c1317fff54b37486acb4b55b46ddcccb9add3ca51c2190; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G2: every script readability file is grade <= 6
  CHECK: python3 -c "import re,glob;fs=sorted(glob.glob('research/readability_v*.txt'));g=[float(re.search(r'Kincaid\):\s*([0-9.]+)',open(f).read()).group(1)) for f in fs];print('GRADES_OK' if fs and max(g)<=6 else 'BAD',g)"
  EXPECT: GRADES_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c707d2caefc96b3b2487f4946592d549d7a18415b4abbbfe05ba2bca651089c1; exit=0; EXPECT=matched; output-sha256=c7c82a0598c5ceaf8a9036a74e35cd7a01cdcad0c980817069685cea4701439a; output-bytes=21; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G3: Grace's script claims each have a source verdict in product_facts.md
  CHECK: python3 -c "t=open('research/product_facts.md').read().lower();ks=['gels','odor','toilet paper','wipe','zip','toilet that won']; m=[k for k in ks if k not in t];print('FACTS_OK' if not m else 'MISSING',m)"
  EXPECT: FACTS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=015f599d52c22ff1d6277a633d16509cf5d811649acd61e46d4fed3a787c8d81; exit=0; EXPECT=matched; output-sha256=38f4673593f304c3dabbcff73b594ce880df6dfa1574d20bd17b3c939de53d0a; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G4: real product photos saved (box front at least 800 px wide)
  CHECK: python3 -c "import glob;from PIL import Image;fs=[f for f in glob.glob('refs/real/*') if f.lower().endswith(('.jpg','.jpeg','.png','.webp'))];w=max([Image.open(f).size[0] for f in fs] or [0]);print('PHOTOS_OK' if len(fs)>=3 and w>=800 else 'NO',len(fs),w)"
  EXPECT: PHOTOS_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7580f9f0bdf4fd592026c330b386f3dc64cb986215c2bf31e000032e47debe88; exit=0; EXPECT=matched; output-sha256=5151b51cf888204a79850d50be90970bafb9b986c0d85dd8a6a07c23accbbfad; output-bytes=18; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G5: product reference sheet built from real pixels
  CHECK: python3 -c "from PIL import Image;im=Image.open('refs/product_sheet.png');print('SHEET_OK' if min(im.size)>=900 else 'SMALL',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=532f28ec3ad6eb2d1f80b50a9c3b24cc54acabe0fd1a6bdcf569b8a974edcc90; exit=0; EXPECT=matched; output-sha256=86c81dbf840520112d38d2552d1c87e83cf856e476ba2d16f80abcf3fd118f71; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G6: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every prompt passed through prompt-master rules
  CHECK: python3 -c "import json;d=json.load(open('shots.json'));r=[];[r.append((v['id'],sum(1 for s in v['shots'] if not s['hand'])/len(v['shots']))) for v in d['videos']];print('MIX_OK' if all(1/3-0.01<=x<=0.5+0.01 for _,x in r) else 'BAD',r)"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=ba839909f08094b1d694cbc90ef46fc81a8372c25bae8903306e8fed111b97ee; exit=0; EXPECT=matched; output-sha256=56acfad09edbe0e16cfd8b3ea95daff52916d11af54ca4f69a81d4618ddd2e97; output-bytes=49; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G7: REMOVED.md exists and carries Ralph's standing removals (no text, no cards, no Ken Burns)
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=013a407bf9538486765030b1ef6dfb1517e8b37c02c4fd804b29ca767557b9ea; exit=0; EXPECT=matched; output-sha256=fdd0ffce6701454c76a66b240abb2c3bf4ad8cf481d672c18ea787906a38db7a; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G8: review page published with the script + reference sheet; plan sent to Ralph with one total cost; push + email sent (manual)
  EVIDENCE: plan on artifact AiM9jZAQjFNExfb5A3rK2h v1 with one total; push sent; email Gmail id 1a15d1be98df4777

# Phase 2: V1 production (Ralph 2026-10-21: V1 only, word for word, visuals match, short French tips no rings, Kie only)

- [x] G9: cut-stage gate passes (incl. coach compare, no text overlay)
  CHECK: cd ../.. && python3 grace/gate.py ugc/cleanwaste-toilet-kit --stage cut
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=e7b81ec5cc0be318f45fe251f0634c39b433f49b2ae3bae824d92bc082606cf4; exit=0; EXPECT=matched; output-sha256=b4f6bb2295b31bed47ca6d21ff0ffa944ba3155c4d38827b2a8a3393e3c25609; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G10: final is 1080x1920, 28-36 s, audio present at -16 +/- 1 LUFS
  CHECK: python3 -c "import subprocess,re;f='out/cleanwaste_v1.mp4';p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,codec_type:format=duration','-of','compact',f],capture_output=True,text=True).stdout;d=float(re.search(r'duration=([0-9.]+)',p).group(1));e=subprocess.run(['ffmpeg','-nostats','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr;i=float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',e)[-1]);ok='width=1080|height=1920' in p and 'audio' in p and 28<=d<=36 and abs(i+16)<=1;print('FINAL_OK' if ok else 'BAD',d,i)"
  EXPECT: FINAL_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=765f07024cf553aa9e6e7bdf9cc16e1bbdf410819441c999506e98569d6c612c; exit=0; EXPECT=matched; output-sha256=59c140b15b568bb37a75f4ca2a7e75edb72f268ea0aa3c966a20cb6d802e5d63; output-bytes=25; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G11: voiceover says Grace's script word for word (STT)
  CHECK: python3 vo.py --retime
  EXPECT: WORDS_MATCH
  EVIDENCE: automatic-evidence=v1; definition-sha256=099fab1b35cb1587520b0fd0ede1fc6e8e580d78853d76b9c4f3ad3a6d37037f; exit=0; EXPECT=matched; output-sha256=6e1069ccec16f0ed0c34f5b1d140adb2c444993fcc2fbc8eac55322e278e6cc7; output-bytes=790; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G12: no freeze longer than 0.6 s and no black frames in the final
  CHECK: python3 -c "import subprocess;e=subprocess.run(['ffmpeg','-nostats','-i','out/cleanwaste_v1.mp4','-vf','freezedetect=n=0.002:d=0.6,blackdetect=d=0.1','-f','null','-'],capture_output=True,text=True).stderr;print('MOTION_OK' if 'freeze_start' not in e and 'black_start' not in e else 'BAD')"
  EXPECT: MOTION_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=b83ae8bd177196842e8cc13f8b7886f3fc278e4bdc42b56d1bc79ef70937b889; exit=0; EXPECT=matched; output-sha256=ad059e15b7d9efc8db91020748da25e4bd250aeedaca7e644e16bc7ac157fdef; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G13: AI finish applied (final differs from the review render: grain + sharpen + saturation 0.92, in cut.py --final)
  CHECK: python3 -c "t=open('cut.py').read();import os;print('FINISH_OK' if 'noise=alls=6' in t and 'saturation=0.92' in t and os.path.getmtime('out/cleanwaste_v1.mp4')>=os.path.getmtime('out/cleanwaste_v1_review.mp4') else 'BAD')"
  EXPECT: FINISH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=dd4fbeba5321b2bea40d528bfaffc044179abea2a84b13d4c0cd0023f66c22b4; exit=0; EXPECT=matched; output-sha256=df6d03e30a61feecfc415434513e258ad057ca50f7d81ca774ffa2b4dcd6898d; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G14: Kie spend within the approved $3.465 (log of credits: start 1428.2)
  CHECK: curl -sS https://api.kie.ai/api/v1/chat/credit | python3 -c "import json,sys;b=json.load(sys.stdin)['data'];s=(1428.2-b)*0.005;print('SPEND_OK' if s<=3.465+1e-6 else 'OVER',round(s,3))"
  EXPECT: SPEND_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=6b2f57a9ed4935744ead43c396e1bfa1d9dfa5ea1e8a9da1fdf12cee9406c77d; exit=0; EXPECT=matched; output-sha256=85962fe84869b910dd0bb4029226b0cd9e26619a84b7f5fec4f1bd1e31041331; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/cleanwaste-toilet-kit; path=7f4fb4b02918/15 entries
- [x] G15: every element of the cut checked against REMOVED.md + 2x hand edge check (manual; qc/cut_sheet.jpg, qc/*_frames.jpg)
  EVIDENCE: qc/cut_sheet.jpg 27 frames: no text/cards/pasted label/freeze, bright neutral, unused bags, no flushing, short French tips no rings; 2x hands S5/S7 clean
- [x] G16: final + script doc in Drive "Grace Tiktok assets" product folder as CURRENT, link in README + reply; push + email sent (manual)
  EVIDENCE: Drive video 1caLc7HSfxyOcTKMe3xa_4st9bn60B0y7 (75606569 bytes = local) + doc 1_0x0oMJZ_ltqqm0M2MU2yZuu5xAtnDYrWnSAey809cE in folder 1ZgU9Z8oQkT_Wca_EkXtfd6AbDFHZZgG8; README updated

Manual evidence (2026-10-21): G8 plan published (artifact AiM9jZAQjFNExfb5A3rK2h v1), push + email sent (Gmail id 1a15d1be98df4777). G15 qc/cut_sheet.jpg (start/mid/end of all 9 shots): no text, no cards, no pasted label, no Ken Burns/freeze, bright neutral grade, unused bags only, no flushing, short French tips no rings, forearm modest (Ralph OK); 2x hand edges S5/S7 clean, no halo. G16 Drive video 1caLc7HSfxyOcTKMe3xa_4st9bn60B0y7 size 75606569 = local, doc 1_0x0oMJZ_ltqqm0M2MU2yZuu5xAtnDYrWnSAey809cE, folder 1ZgU9Z8oQkT_Wca_EkXtfd6AbDFHZZgG8; push + email at delivery.
