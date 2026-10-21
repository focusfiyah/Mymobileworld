# Grace voice clones (ElevenLabs, Starter plan = instant clones only; professional clone not allowed, tested 2026-10-18)
- **Grace C `P8OUGBCvq8OBS4xlb65A` = Grace's default voice (Ralph picked it 2026-10-18).** Instant clone from her 5 clean
  Wag Bag CURRENT V1-V5 takes (~155 s, Drive WagBag Final Edits). Settings: eleven_v4, stability 0.4, similarity 0.8, style 0.
  It renders ~7 dB quieter than B (-19.5 vs -12.8 LUFS on the same line): loudnorm to -16 LUFS before any cut or preview.
- Grace B `bGrsdLmwBbYUgHRuMFOI`: retired. 1-sample instant clone; Grace said it doesn't sound like her.
- `grace_voice_AB.mp3` = real Grace 7 s, then B, then C, each levelled to -16 LUFS.
- Source audio (src/) is gitignored; re-download from Drive if needed.
- **Open (Ralph 2026-10-19, LGXNDS v6):** Grace C has a slight room echo, baked into the clone (her Wag Bag takes have room echo).
  Free ffmpeg cleanup (highpass/afftdn/gate/EQ) changed nothing measurable; DeepFilterNet can't fetch its model (GitHub raw 403).
  Ralph chose "re-clone later": rebuild Grace C from de-echoed takes (quote the cleaning + clone cost first). Until then v6 keeps the current C.

- **2026-10-21: Grace C `P8OUGBCvq8OBS4xlb65A` is gone from the account (TTS returns 404).** The only Grace voice now is "Grace cloned" `Rh3oAQMqRVf78UIVpBoQ` (made 2026-10-20 from Ralph's 2026-10-19 example video + 10 Grace TikToks; its own description says it was picked that day, eleven_v4 0.4/0.8/0 then paced to 3.5 words/s; the pace.py it names is not in this repo). Used for the power bank flashlight ad (`ugc/powerbank-flashlight/vo.py`: pause trim, atempo up to 3.5 w/s if slower, loudnorm -16 LUFS). Ralph has not confirmed it in this repo yet.
