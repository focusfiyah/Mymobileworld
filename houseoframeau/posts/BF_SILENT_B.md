# HofR Black Friday, silent batch B (2026-11-12): Ralph's voice on 5 of Grace's silent cuts

Status: WAITING ON RALPH'S OK (review https://claude.ai/code/artifact/cb249720-2912-42fc-a4d7-da02f25a2e85, email 1a1d2031a5e0f711; push tool not in this session). $0.
Session session_01Y1Pt3pFXuhqRgggqDLNecT; hub session_01Y1Pt3pfP7HcKsjq5xn9T1H (queue owner). Next per OK'd cut: upload out/bf_<job>.mp4
(1080p, medium preset) as "HofR - <Product> BF.mp4" to the product folder (Kie host + Composio GOOGLEDRIVE_UPLOAD_FROM_URL, size check),
then send_message to the hub: "<product>, Drive file id <id>, <length> s, approved by Ralph <date>".

| Job | Length | Hook | Product folder |
|---|---|---|---|
| bf-calmi-ring | 22.7 s | H055 | 15pPvJub7AsVwEGS31R0TUnlTMnbUP8Vg |
| bf-cosrx-lip-care | 23.1 s | H134 | 1RXCL0JUxruMdRoDyVMQhFhWCz1fHKbYY |
| bf-waterproof-eyeliner | 23.1 s | H062 | 1n4iZ0gqaUgm1pBch2cRutY-fW5PCqv06 |
| bf-wig-milk-spray | 26.5 s | H028 | 1fGDnU6rqdqRnBK2Mzd6Vr8s8Ib7oOCEb |
| bf-pinmoco-chair | 23.6 s | H061 | 1tKHbDXt17PhjKuhQgFjwmkOufF6Xqbmk |

Rebuild (from houseoframeau/posts): restore sources (_src/<k>.mp4 = each product's CURRENT V1 from Drive; eyeliner and pinmoco
src/orig.mov = Grace's originals 1i29d8fq... and 1CosT6go...), voice ref Dayone-ai avatar/voice/ralph_ref.wav (media set 1).
  /root/.presenter-tools/cbx/bin/python -I _tools/vo_gen.py bf-<job>    (ONLY=n,n SEED_n=... to redo lines)
  /root/.presenter-tools/fw/bin/python -I _tools/vo_build.py bf-<job>   (whisper read-back + join -> vo/ralph.wav, words.json)
  python3 _tools/cut.py bf-<job> [--final] ; cd _tools && python3 qc.py silent|script|vo|cut   (GATES.md)
Lessons: Chatterbox ~20 s per line on 4 cores; a Pexels clip can pass freezedetect yet read as a still (tree 6111172, stocking
5765495): look at the sheet, use motion.py (mean < ~2 = still). Grace's V1 cuts are ~15 s; a 7-line VO runs ~22-27 s, so drop a line
that nothing on screen can show, then fill from her original before reaching for stock.
