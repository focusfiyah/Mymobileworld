# Gates: FOODOLOGY Red Jelliquid Bundle (plan stage, 2026-11-03)

- [x] G1: Script gate passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/foodology-red-jelliquid
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=fda9808a46f2fba62092f54565139ca15768f8ccbdda4987f7539d0ab485bf11; exit=0; EXPECT=matched; output-sha256=4cad7e09f557458ca44805524c94bc00694a11b285010a216b24842e10d45100; output-bytes=169; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G2: Every still and clip prompt passes the prompt lint (17 files)
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && for f in prompts/*.txt; do python3 ../../grace/prompt_check.py lint $f | tail -n 1; done | grep -c PROMPT_LINT_OK
  EXPECT: /^17$/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=ee1f239d40bef87dff966244971c56a238c3e669f8a24f717a5a3cd019c030bf; exit=0; EXPECT=matched; output-sha256=54183f4323f377b737433a1e98229ead0fdc686f93bab057ecb612daa94002b5; output-bytes=3; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G3: Product reference sheet and the 11 real close-ups exist
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && ls refs/product_sheet.png refs/closeup_*.png | wc -l
  EXPECT: /^ *12$/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=c9c2cc9237b5de1d07af53197421e549268687e66511fc752c56c41f9edd5736; exit=0; EXPECT=matched; output-sha256=a1fb50e6c86fae1679ef3351296fd6713411a08cf8dd1790a4fd05fae8688164; output-bytes=3; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G4: BOOK.md has the review link and one TOTAL line, no blanks
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && grep -c "Sent to Ralph: https://claude.ai/\|^TOTAL: \$0.79" BOOK.md && ! grep -q "___\|PENDING" BOOK.md && echo NOBLANK
  EXPECT: /^2\nNOBLANK/m
  EVIDENCE: automatic-evidence=v1; definition-sha256=7341561c8aa3365ef16bcc66b5575e9f9e6cd4bdceecf14c22b19544bd1049f2; exit=0; EXPECT=matched; output-sha256=0fcf27406be4dda750349b8152b1a9ac9daacfd37ce1e8ab846164f53a05f3ec; output-bytes=10; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G5: Script has no banned phrase, no price, no weight claim, closes on the orange cart
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && ! grep -Eiq "order (it )?now|heads up|\\$[0-9]|reviewer|the label says|weight|fat|slim|debloat|glp|—|–" scripts.md && grep -q "It's in the orange cart." scripts.md && echo CLEAN
  EXPECT: CLEAN
  EVIDENCE: automatic-evidence=v1; definition-sha256=8c6a7f5146e279fe1b7b1c0402bd904176b81b652e0338a04be32a1e626b44bd; exit=0; EXPECT=matched; output-sha256=0b98843240a0b1a2384483206c02be8968dd809eb73838820be24cb7d6d6aeb9; output-bytes=6; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G6: Script is standard length (90-115 words) and grade <= 6
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && python3 -c "import re;t=open('scripts.md').read().strip().splitlines()[-1];n=len(t.split());g=float(re.search(r'Flesch-Kincaid\):\s*([\d.]+)',open('research/readability_v1.txt').read()).group(1));print('LEN_OK' if 90<=n<=115 and g<=6 else 'BAD',n,g)"
  EXPECT: LEN_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=8b504e5ff32e21f2b7d2f8f5456bb3fc1a2b04eb91ad14d4657cf9cb43376478; exit=0; EXPECT=matched; output-sha256=ce62ca874db4ca12c266a7f834fd2675b54b52965e08936796209ffc708ef647; output-bytes=15; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G7: Review page published with plan, script, sheet and prompts (manual: link in BOOK.md)
  EVIDENCE: https://claude.ai/code/artifact/edbe121f-62a8-4609-b860-c7410bde0844 v1 (9 script lines, 6 shots with still + clip prompts, sheet, rooms, winners, cost)
- [x] G8: Ralph notified (phone push + email) and asked with tap options (manual)
  EVIDENCE: Gmail id 1a1a1fd3c82e7920 sent 2026-11-03; PushNotification not offered in this session (ToolSearch select:PushNotification returned no match, tested); questions asked with AskUserQuestion

## Cut stage (2026-11-03)
- [x] G9: Cut gate passes
  CHECK: cd /home/user/Mymobileworld && python3 grace/gate.py ugc/foodology-red-jelliquid --stage cut
  EXPECT: GATE OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=c623ab20af15a587ea4fa3c538263b9d43510459376ea85eb34ea658d46094d9; exit=0; EXPECT=matched; output-sha256=3bbac99a1ff01142d77574ce6f47466d447a7f859608800f3197cf2cde55f8fd; output-bytes=86; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G10: Grace V1 is 12.0 s, 1080x1920, no audio stream
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && ffprobe -v error -show_entries format=duration:stream=codec_type,width,height -of csv=p=0 out/cut_v1.mp4 | tr '\n' ' '
  EXPECT: /^video,1080,1920 12\.0+ $/
  EVIDENCE: automatic-evidence=v1; definition-sha256=f5c3c60007d48c9dae6860acbc787c4e40e43a4d5bd6f5f66c7b9339957bd6f5; exit=0; EXPECT=matched; output-sha256=0149cd802de40d5b4a6ea4de29c12e2282b44a2658419b0273f240c34c12194c; output-bytes=26; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G11: HofR hook whole from frame 0, held 2 s
  CHECK: cd /home/user/Mymobileworld/ugc/foodology-red-jelliquid && python3 ../../tools/hookcheck/hook_check.py out/hofr_v1.mp4 --hook 200,1140,680,190
  EXPECT: HOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=2846df5acb585b354349b787309eff5c83bfdf809b89a22851b7cb9877bc8faf; exit=0; EXPECT=matched; output-sha256=fd9a04592fedf0a6aaae52c4ef20763bff36d897872078e98a523a589cce16da; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G12: Job media stored in Drive
  CHECK: cd /home/user/Mymobileworld && python3 tools/media/media.py check
  EXPECT: MEDIA_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a66385644360a15b9a16b370692a526fbf7beb23b8e8e7572560f8cd98ee8237; exit=0; EXPECT=matched; output-sha256=8083bc5e3d38fc4812679011f657b4c749435c73ae3358ae5426effe963edf5b; output-bytes=9; shell=/bin/sh; cwd=/home/user/Mymobileworld/ugc/foodology-red-jelliquid; path=7f4fb4b02918/15 entries
- [x] G13: Ralph approved cut v1 (tapped "Approve (Recommended)" 2026-11-03); Drive folder holds both videos (sizes 68638919 and 69192814 match local) + script doc + verdict doc (manual)
  EVIDENCE: Drive folder 1u1rlGuihgxPJbaQT2yMu-i3934-eImVy; files 1emKu_wHuKZeIrsTkUOAkowJjuooxjEgO (68638919 B), 1GbFA1VmwDZePZHRHLEldHJQfxRTXwyOY (69192814 B), docs 1Zrz3EKb6zFSPOf_k9E2nHYD-KwEn4VcJNkO6PK8v7Cg, 1o5kGNlUiHTJxk2ODWyixC6GlKpBPn9nwHaaOVkDgT7A
