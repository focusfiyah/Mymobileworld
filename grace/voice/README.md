# Grace voice clones (ElevenLabs, Starter plan = instant clones only; professional clone not allowed, tested 2026-10-18)
- **"Grace" `Rh3oAQMqRVf78UIVpBoQ` = the ONLY Grace voice (Ralph 2026-10-21: "There is only Grace VO in elevenlabs, Grace C no longer exist").** Checked via the ElevenLabs API 2026-10-21: the account's cloned voices are Ralph Azariah and Grace only. Voice description: "Grace (@shewiththeglow, Haitian accent): Ralph's 2026-10-19 video + 10 TikToks closest to it. Picked 2026-10-20 (G): eleven_v4 0.4/0.8/0, then grace/voice/pace.py --wps 3.5" (11 samples).
- DELETED from the account (history only): Grace C `P8OUGBCvq8OBS4xlb65A` (Ralph picked it 2026-10-18). Instant clone from her 5 clean
  Wag Bag CURRENT V1-V5 takes (~155 s, Drive WagBag Final Edits). Settings: eleven_v4, stability 0.4, similarity 0.8, style 0.
  It renders ~7 dB quieter than B (-19.5 vs -12.8 LUFS on the same line): loudnorm to -16 LUFS before any cut or preview.
- Grace B `bGrsdLmwBbYUgHRuMFOI`: DELETED from the account. 1-sample instant clone; Grace said it doesn't sound like her.
- `grace_voice_AB.mp3` = real Grace 7 s, then B, then C, each levelled to -16 LUFS.
- Source audio (src/) is gitignored; re-download from Drive if needed.
- **Open (Ralph 2026-10-19, LGXNDS v6):** Grace C has a slight room echo, baked into the clone (her Wag Bag takes have room echo).
  Free ffmpeg cleanup (highpass/afftdn/gate/EQ) changed nothing measurable; DeepFilterNet can't fetch its model (GitHub raw 403).
  Ralph chose "re-clone later": rebuild Grace C from de-echoed takes (quote the cleaning + clone cost first). Until then v6 keeps the current C. Superseded 2026-10-20 by the new "Grace" clone.
