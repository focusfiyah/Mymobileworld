# GATES: Zernio live post test (House of Rameau)

- G1 Key present in env (Zernio_API_key), never printed.
  CHECK: test -n "$Zernio_API_key" && echo KEY_OK
  EXPECT: KEY_OK
- G2 Accounts endpoint lists House of Rameau (TikTok) with connection type: manual (output of curl, read).
- G3 Ralph named video + caption via AskUserQuestion before posting: manual.
- G4 Live public post made with caption and AI label (video_made_with_ai): manual, Zernio response.
- G5 Post status polled; URL or error reported verbatim: manual.
- G6 Comments fetched and reported: manual.
- G7 Brain note updated, tools/brain/check.py prints BRAIN_OK: manual.
