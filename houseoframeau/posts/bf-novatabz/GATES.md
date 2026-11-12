# Gates: NovaTabz HofR holiday test, Chatterbox re-voice (2026-11-12)

OWNS: houseoframeau/posts/bf-novatabz/**

Scope: same script and shots, Ralph's free Chatterbox voice, shots re-timed to the new lines, QC'd, review page republished.

- [x] G1: VO is the Chatterbox take and every line reads back word for word (faster-whisper small.en)
  CHECK: python3 qc.py vo
  EXPECT: VO_OK 8 lines
  EVIDENCE: automatic-evidence=v1; definition-sha256=bdada3d5656ca4f9d67e4dd7a77048d054c52405c09b3827182162ba2736aca9; exit=0; EXPECT=matched; output-sha256=97ca095b7b8e6644df812c70f9c75020c3a8c1f4f832fc24b905e27097c5e7a4; output-bytes=14; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/bf-novatabz; path=7f4fb4b02918/15 entries

- [x] G2: cut.py uses vo/ralph_cbx.wav, no speed change, every shot starts on its line's first word
  CHECK: python3 qc.py cut
  EXPECT: CUT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=80985a5fd3304faba21ee6661651ee986e0a336d41c6ad36149b4c6a91207e03; exit=0; EXPECT=matched; output-sha256=145e191b155054fabdf1be8e8a5c21b4ef37f17868985cb2f3ac06d821b9314b; output-bytes=59; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/bf-novatabz; path=7f4fb4b02918/15 entries

- [x] G3: final cut is 15 s or longer, 1080x1920, -16 to -14 LUFS
  CHECK: python3 qc.py out
  EXPECT: OUT_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=a059ada4f0e856359a67f54fc659a98a2eb7938e64328df041199a57b8a8c26e; exit=0; EXPECT=matched; output-sha256=293faaba531ef30df5ae0b0ee5bbac926731b6446ccd5877d1e1dd08fff75b45; output-bytes=35; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/bf-novatabz; path=7f4fb4b02918/15 entries

- [x] G4: whole hook on screen in frame 0 and held 2 s, inside the safe zone
  CHECK: python3 ../../../tools/hookcheck/hook_check.py out/bf_novatabz.mp4 --hook 110,380,860,180
  EXPECT: HOOK_OK
  EVIDENCE: automatic-evidence=v1; definition-sha256=67d25b4ac581913908cc6ad3269c7bd801a402bb6069c0545c93c95d1c58dda4; exit=0; EXPECT=matched; output-sha256=46194575d95ff2d2d4d722cf593eede20585eaf25f25694e61c06d8087237ffc; output-bytes=63; shell=/bin/sh; cwd=/home/user/Mymobileworld/houseoframeau/posts/bf-novatabz; path=7f4fb4b02918/15 entries

- [x] G5: frame sheet looked at; 2x on hand edges and first second: no halo, smear, fringe; voice heard (no garble)
  EVIDENCE: frame sheet of 19 frames (every shot) looked at: each shot on its line, label unchanged, bright grade; 2x crops at 0 s, 0.9 s, 11 s, 18.5 s: hand, rings, lips, brush edges clean, no halo/smear/fringe; blackdetect 0 black frames; voice checked by whisper readback (all 8 lines word for word), not by ear

- [x] G6: review page republished to FHRFXAMvsgrQJKEHyzZYSN with the new cut and a "voice is now Chatterbox" note
  EVIDENCE: published 2026-11-12 as Version 3 (id 1794525258-3906) of FHRFXAMvsgrQJKEHyzZYSN with novatabz_holiday.mp4 (720p preview) and the section 'New: the voice is now Chatterbox'

- [x] G7: $0 spent (no Kie, Kling, ElevenLabs or other paid call this job)
  EVIDENCE: only local tools ran: Chatterbox and faster-whisper (CPU), ffmpeg, Pexels free downloads, Composio Drive downloads for media restore; no Kie, Kling, ElevenLabs or other paid call

- [x] G8: every person on screen is brown, light brown or dark brown skinned (Ralph 2026-11-12, campaign README)
  EVIDENCE: gift_wrap.mp4 (light-skinned hands) replaced by Pexels 5974733 (brown hands), frames 13.4-17.4 s and a 2x crop looked at; stockings.mp4 shows no people; Grace's clips show her own brown hands and face
