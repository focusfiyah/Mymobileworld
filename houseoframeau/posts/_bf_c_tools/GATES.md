# Gates: HofR Black Friday, Ralph VO on 5 Grace silent cuts, batch C (2026-11-12)

Request: Ralph 2026-11-12 "If we're going to use the [Grace] silent videos, we can just replace the silence with my voiceover."
Posts: bf-purcell, bf-jiyu-nad, bf-luvum, bf-momo-nashi, bf-manners. $0 only. No TikTok upload, no queue edit (hub session owns it).

- [x] G1: (manual) All 5 Grace CURRENT V1 (HD) cuts confirmed silent before use (no voice, no music)
  EVIDENCE: 2026-11-12 ffprobe on the Drive CURRENT files (sizes = Drive): purcell 14.8 s, jiyu 18.1 s, luvum 11.3 s, momo 16.0 s, manners 14.1 s, all with no audio stream at all
- [x] G2: PURCELL cut passes QC (>=15 s, 1080x1920, 30 fps, -16..-13.5 LUFS, no black/frozen stretch, hook word for word, close line, no banned words, every VO line heard)
  CHECK: cd ../bf-purcell && python3 ../_bf_c_tools/post_check.py bf_purcell H046
  EXPECT: POST_OK bf_purcell
  EVIDENCE: automatic-evidence=v1; definition-sha256=026b54e34a814f8e76f84c972fa947b5bc761d6a233f7e20223a267831cfe4fb; exit=0; EXPECT=matched; output-sha256=60c4d46214aa33029437395fb2edc61cda7ebfde7b05b3ccc6f5fc49fdafe93f; output-bytes=54; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G3: PURCELL hook whole in frame 0 and held, inside the safe zone
  CHECK: cd ../bf-purcell && python3 ../../../tools/hookcheck/hook_check.py out/bf_purcell.mp4 --hook 140,362,719,218 --hold 2.0
  EXPECT: HOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=1c341d4d9e0e7515fed5630ed7cafcd2c48c53ba9935c10bafcad81d976ee7c4; exit=0; EXPECT=matched; output-sha256=b665236fd77deda006b71c281e9456704d3799ed6073ed46982653ac91ab88f2; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G4: JIYU cut passes QC
  CHECK: cd ../bf-jiyu-nad && python3 ../_bf_c_tools/post_check.py bf_jiyu_nad H089
  EXPECT: POST_OK bf_jiyu_nad
  EVIDENCE: automatic-evidence=v1; definition-sha256=0070b5df41380a45a745e757e84b6c9dbbaf1a2fc422a8a5ef837a84a182ecca; exit=0; EXPECT=matched; output-sha256=bf39e48cdcf9a88606cbcbc3ddec3f8a805736fdd015e3b44803ad938989978e; output-bytes=55; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G5: LUVUM cut passes QC
  CHECK: cd ../bf-luvum && python3 ../_bf_c_tools/post_check.py bf_luvum H055
  EXPECT: POST_OK bf_luvum
  EVIDENCE: automatic-evidence=v1; definition-sha256=72b12fcbc8a0c3835f52b8b42fe7257524f9c2d1e828d0eecbb872025b826cb4; exit=0; EXPECT=matched; output-sha256=9fdbccfb965df4ea8077fce56a07d0de26a4e4805cfe061c1c33a6f153457c55; output-bytes=52; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G6: Momo & Nashi cut passes QC
  CHECK: cd ../bf-momo-nashi && python3 ../_bf_c_tools/post_check.py bf_momo_nashi H134
  EXPECT: POST_OK bf_momo_nashi
  EVIDENCE: automatic-evidence=v1; definition-sha256=d53f3f28def466a46a19a7f17dc9e1409ee1da64679284129de5670f6a7499cf; exit=0; EXPECT=matched; output-sha256=7c80033662a35e75bd8a5546cda24cccea28a2961d59108c532fc3e80479b4c5; output-bytes=57; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G7: Manners cut passes QC
  CHECK: cd ../bf-manners && python3 ../_bf_c_tools/post_check.py bf_manners H130
  EXPECT: POST_OK bf_manners
  EVIDENCE: automatic-evidence=v1; definition-sha256=9cf10b11ed90c8ba16876ccb7a33a225dcd1f55b2ce4bf3aa447493a431d1bbb; exit=0; EXPECT=matched; output-sha256=49ab54a1d14d36bd86ce5c58e05c602632d260fa1a917bd04048eaf02b1da583; output-bytes=54; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G8: hook check on all four other cuts (box read from each plan json)
  CHECK: python3 hooks_all.py
  EXPECT: HOOKS_ALL_OK 5
  EVIDENCE: automatic-evidence=v1; definition-sha256=2bb3e2ac3887601a112a97f117cce0acbb638e35417077db39e9b35c7bdee4ef; exit=0; EXPECT=matched; output-sha256=4d059a3590ebdd93a80bac77fa1b8311698359a2a6a18ee96bba154506a9fdaa; output-bytes=112; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/_bf_c_tools; path=7f4fb4b02918/15 entries
- [x] G9: (manual) Every cut viewed as a 10 fps frame sheet: frame 0 = hook + product, no leaked/blurred frames, hook card not over the label, holiday b-roll bright and neutral and moving, shots match their words, order/framing differ from Grace's post
  EVIDENCE: 10 fps sheets of all five final cuts viewed 2026-11-12. Fixed on the way: leaked pre-roll frame at t=0 (exact trim in build.py), card over PURCELL cap and Luvum logo and Manners title (hook moved/shots changed), Grace's refocus/zoom blurs in PURCELL/JIYU, still Pexels clips 5765495 and 6098987 swapped, golden 5802516 swapped. Only real page-turn motion remains
- [x] G10: (manual) $0: no Kie, Kling, ElevenLabs or other paid call (voice = local Chatterbox, b-roll = Pexels free)
  EVIDENCE: calls this session: Drive/Composio downloads, Pexels API (free), local Chatterbox + faster-whisper, Gmail send. No Kie, Kling or ElevenLabs call
- [x] G11: (manual) Each job's REMOVED.md and Grace's dropped moments (blurs) checked against every cut
  EVIDENCE: only ugc/jiyu-nad-moisturizer/REMOVED.md exists (none listed). Grace's dropped moments kept out: PURCELL box blur 1.5-2.6 and refocus 39.75-41.1, LUVUM 0-0.4 and 7.9-9.4, JIYU zoom blurs 2, 15-16, 20 s, Manners page flip 24.2 s
- [ ] G12: (manual) ONE review page, videos stacked full width, script under each; link + phone push + email sent to Ralph; then STOP
  NOTE: page https://claude.ai/code/artifact/90f11b0d-ed64-4c5a-9368-43dede2d34e8 + email 1a1d2104ed140c6a sent 2026-11-12; phone push NOT sent: ToolSearch found no PushNotification tool in this session (searched twice)
- [x] G13: (manual) After Ralph's OK per cut: Drive "HofR - <Product> BF.mp4" in the product folder, size = local; one line per product to the hub session
  EVIDENCE: Ralph tapped "Yes, all 5" 2026-11-12. Drive ids (size = local): PURCELL 1A96OCUDtJ-TxNHxVBHuOr1SmrYElHgZh 25,686,145; JIYU 1uGnQe3s5yh3qZGFrg1aOeJj7RGwA829o 29,370,156; LUVUM 171hJpkdckVa2HascrdFR5pyh6UIUv3BF 32,992,731; Momo 1v_iq7nExFzGeWwGbhX9my8SuSXEwfK-E 44,495,445; Manners 1_mEObGda4Zr1ujAvlmYX17q0Svz82qJc 33,802,349. Hub session sent the five lines (delivered)
- [x] G14: (manual) Code committed and merged per CLAUDE.md; Brain note + session log; Active work line removed; BRAIN_OK
  EVIDENCE: merged to main (ad8b558) and pushed; Brain job note, session log, Index, Jobs, day log updated and pushed; Active work line removed. brain check passes every batch-C item; it still lists 3 items owned by the running silent-A and silent-B sessions (their notes, not touched here)

ABANDON: G12 phone push could not be sent: no PushNotification tool in this session (ToolSearch searched twice, 2026-11-12); email and review page did go out and Ralph read and approved
