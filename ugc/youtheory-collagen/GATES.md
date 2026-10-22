# Youtheory Collagen Liquid (Grace), 2026-10-22, phase 1: research + script gate + plan (no paid calls)

- [x] G1: script gate passes (audience, coach, viral board, facts, hooks, humanizer, readability override, line sources, banned phrases)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-collagen
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8bedfb0359f646b69b32d59f16d0517f77c3b5acb95968d57316978fc7331631; exit=0; EXPECT=matched; output-sha256=1c97b16c8da6889040a1ae659812e2a6a89e307e25edb10d90fdefa97fe17478; output-bytes=91; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G2: the script says no vitamin C and keeps the 5,000 mg line
  CHECK: python3 -c "t=open('scripts.md').read().split('## V1')[1].lower();print('VITC_OK' if 'vitamin c' not in t and 'five thousand milligrams' in t and 'need water' in t else 'BAD')"
  EXPECT: VITC_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=51051b8d3cf0000603abb127658364999d4d6c0983729ff1f1655b4128e0e552; exit=0; EXPECT=matched; output-sha256=f7d42894a3e2238f166a60b43aeb62c0c66e92c273bbac4016fae2aad7308397; output-bytes=8; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G3: Ralph's real photos saved and the product sheet built from them (sheet >= 1500 px)
  CHECK: python3 -c "import os;from PIL import Image;ok=all(os.path.exists('refs/real/'+f) for f in ['ralph_pouch_flat.jpg','ralph_pouches_in_box.jpg']);im=Image.open('refs/product_sheet.png');print('SHEET_OK' if ok and min(im.size)>=1500 else 'NO',im.size)"
  EXPECT: SHEET_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7a5b8a410afd33be7daa45c65fc6bcc130d86b692e785873f09e9c1946711cf2; exit=0; EXPECT=matched; output-sha256=ad7ebcebd50ed0ffa9e0fc26c22430555ed18d7c8eef089c776f6ff7b14f783d; output-bytes=22; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G4: shots.json marks every shot HAND or HAND-FREE, a third to half hand-free, every product shot on Omni, no Kling
  CHECK: python3 -c "import json;s=json.load(open('shots.json'))['videos'][0]['shots'];f=sum(1 for x in s if not x['hand'])/len(s);ok=1/3-0.01<=f<=0.51 and all((x['model']=='omni')==x['product'] for x in s) and not any(x['model']=='kling' for x in s);print('MIX_OK' if ok else 'BAD',f)"
  EXPECT: MIX_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=92cc184a909c7660cecaf2876fcfffbd70685efee884e6c351afbda791c380c4; exit=0; EXPECT=matched; output-sha256=6de9dce5ffd78b1e339570ba6e3e617384eb532f3955007b754f794c99e3edec; output-bytes=13; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G5: REMOVED.md carries the standing removals and vitamin C
  CHECK: python3 -c "t=open('REMOVED.md').read().lower();print('REMOVED_OK' if all(k in t for k in ['text','card','ken burns','vitamin c']) else 'NO')"
  EXPECT: REMOVED_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=6b974d714093ba6e6d8297d58e802e5b4f27e4e2a9973a522bcb2f2d872d6c1b; exit=0; EXPECT=matched; output-sha256=fdd0ffce6701454c76a66b240abb2c3bf4ad8cf481d672c18ea787906a38db7a; output-bytes=11; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G6: review page published with script, reference sheet, shot list and one total; push + email sent (manual)
  EVIDENCE: plan on artifact https://claude.ai/artifact/VD9ib3CWos6aH4hbrafzjX v1 with one total ($3.38, up to $3.79); push sent; email Gmail id 1a16193e390e46f8 (2026-10-22)

# Phase 2: production (Ralph 2026-10-22: "Go, French tips with rings and bracelets, size ok, paid stills")

- [x] G7: cut-stage gate passes (coach compare, no text overlay)
  CHECK: cd ../.. && python3 grace/gate.py ugc/youtheory-collagen --stage cut
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=5aa074f9c3ced0babc1f063403b38af26ce75ef5f5f18263fba5cf8bc459c6e8; exit=0; EXPECT=matched; output-sha256=1c97b16c8da6889040a1ae659812e2a6a89e307e25edb10d90fdefa97fe17478; output-bytes=91; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G8: final is 1080x1920, 25-35 s, audio at -16 +/- 1 LUFS
  CHECK: python3 -c "import subprocess,re;f='out/youtheory_collagen_v2.mp4';p=subprocess.run(['ffprobe','-v','error','-show_entries','stream=width,height,codec_type:format=duration','-of','compact',f],capture_output=True,text=True).stdout;d=float(re.search(r'duration=([0-9.]+)',p).group(1));e=subprocess.run(['ffmpeg','-nostats','-i',f,'-af','ebur128','-f','null','-'],capture_output=True,text=True).stderr;i=float(re.findall(r'I:\s+(-?[0-9.]+) LUFS',e)[-1]);ok='width=1080|height=1920' in p and 'audio' in p and 25<=d<=35 and abs(i+16)<=1;print('FINAL_OK' if ok else 'BAD',d,i)"
  EXPECT: FINAL_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=04f9b615792a8edcef829b6347fda26e81d767c6b1b33a5af646799a2cec62c6; exit=0; EXPECT=matched; output-sha256=78bd1847e36834e9b33bef7a113bbe5a5f3a837df60ce3b36df70b79e50a5108; output-bytes=25; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G9: no freeze longer than 0.6 s and no black frames
  CHECK: python3 -c "import subprocess;e=subprocess.run(['ffmpeg','-nostats','-i','out/youtheory_collagen_v2.mp4','-vf','freezedetect=n=0.002:d=0.6,blackdetect=d=0.1','-f','null','-'],capture_output=True,text=True).stderr;print('MOTION_OK' if 'freeze_start' not in e and 'black_start' not in e else 'BAD')"
  EXPECT: MOTION_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=7caaab3768ed4fd76b573ba12889965ddafdc95ba0323c0a5eaac588e254de10; exit=0; EXPECT=matched; output-sha256=ad059e15b7d9efc8db91020748da25e4bd250aeedaca7e644e16bc7ac157fdef; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G10: voiceover echo gate <= 150 ms
  CHECK: cd ../.. && python3 grace/voice/echo.py ugc/youtheory-collagen/vo/voiceover_paced.mp3 | python3 -c "import sys,re;v=int(re.search(r'rt60_est_ms=(\d+)',sys.stdin.read()).group(1));print('ECHO_OK' if v<=150 else 'BAD',v)"
  EXPECT: ECHO_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=131f452af7d0e461abea1d34487060366117fa6d3110761d0133bcbe9f642238; exit=0; EXPECT=matched; output-sha256=17ac3e11ae85c2e84c56957e9352a9fecd9bd43909637e02422de4d2547a697b; output-bytes=12; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G11: AI finish in the final render (grain + sharpen + saturation 0.92)
  CHECK: python3 -c "t=open('cut.py').read();print('FINISH_OK' if 'noise=alls=6' in t and 'saturation=0.92' in t and 'youtheory_collagen_v2.mp4' in t else 'BAD')"
  EXPECT: FINISH_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c623bd51170323547e693d8212262cbfbb3d50ae169b021628f07648c30539f8; exit=0; EXPECT=matched; output-sha256=df6d03e30a61feecfc415434513e258ad057ca50f7d81ca774ffa2b4dcd6898d; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/youtheory-collagen; path=7f4fb4b02918/15 entries
- [x] G12: every element checked against REMOVED.md + 2x label/hand QC (manual; qc/cut_sheet.jpg)
  EVIDENCE: no text/cards/Ken Burns/freeze, no vitamin C, no red-band box, box only as Ralph's photo; one hand per shot (S5b first 1.4 s, S7 second hand cut), Grace's rings/bracelets; labels 2x: big print right in every clip, small italic line wobbles (S5 'frelps', Ralph: let it go); S3 print tracked from its own frame 0
- [x] G13: Ralph approves cut v2 incl. the tracked S3 (manual)
  EVIDENCE: Ralph 2026-10-22: "OK, upload to Drive" after cut v2 (review page v8)
- [x] G14: final + script doc in Drive "Grace Tiktok assets/Youtheory Collagen Liquid (Grace)" as CURRENT, link in README + reply; push + email (manual)
  EVIDENCE: folder 1ZT1jiilH98fjxqJtE5_qZZXFQ-kDT-c9: video 1It_w2AZ3gc34biPFaY_PE7a-aSFFnHlv 67461558 bytes = local; doc 1lP_YXD5leUfe76RIVa4YCgaVZX-S8h94cXeYcN79gLg (emoji checked via export); README updated
