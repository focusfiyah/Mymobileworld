# Grace voice clones (ElevenLabs, Starter plan = instant clones only; professional clone not allowed, tested 2026-10-18)
- **2026-10-20 re-clone, WAITING ON RALPH'S PICK: "Grace" `gjmt5xZqVE6mjSY4NfQM`** (grace.json). Instant clone from 7 of Grace's own
  on-camera TikToks on @shewiththeglow (sources.json; posted Mar-Aug 2026, before any AI voice; @gracewiththeglow is a different woman).
  Picked from all 1,109 pre-2026-09-25 videos by `pick.py` (driest, no music bed in the gaps), speaker-checked (resemblyzer, see
  sources.json), trimmed to 172 s of speech, levelled. Echo at pauses (`echo.py`): new 52 ms vs old C 110 ms vs B 78 ms.
  Same settings as C (eleven_v4, stability 0.4, similarity 0.8, style 0); level to -16 LUFS. A/B: `grace_voice_AB_2026-10-20.mp3`
  (real Grace, old C, new), review page https://claude.ai/artifact/ERywTwEf9dwoxqgtH8jqyH. Gates: GATES.md (`check.py`).
  On Ralph's "keep": delete Grace B + old C on ElevenLabs, switch every rule/script/skill to the new id (G5, G6).
- **Grace C `P8OUGBCvq8OBS4xlb65A` = Grace's default voice (Ralph picked it 2026-10-18).** Instant clone from her 5 clean
  Wag Bag CURRENT V1-V5 takes (~155 s, Drive WagBag Final Edits). Settings: eleven_v4, stability 0.4, similarity 0.8, style 0.
  It renders ~7 dB quieter than B (-19.5 vs -12.8 LUFS on the same line): loudnorm to -16 LUFS before any cut or preview.
- Grace B `bGrsdLmwBbYUgHRuMFOI`: retired. 1-sample instant clone; Grace said it doesn't sound like her.
- `grace_voice_AB.mp3` = real Grace 7 s, then B, then C, each levelled to -16 LUFS.
- Source audio (src/) is gitignored; re-download from Drive if needed.
- **Open (Ralph 2026-10-19, LGXNDS v6):** Grace C has a slight room echo, baked into the clone (her Wag Bag takes have room echo).
  Free ffmpeg cleanup (highpass/afftdn/gate/EQ) changed nothing measurable; DeepFilterNet can't fetch its model (GitHub raw 403).
  Ralph chose "re-clone later": rebuild Grace C from de-echoed takes (quote the cleaning + clone cost first). Until then v6 keeps the current C.
