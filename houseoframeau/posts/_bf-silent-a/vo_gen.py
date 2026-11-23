"""Ralph's free Chatterbox voice (Take 2 settings, same as Sorry I Lied ep7) for the HofR Black Friday silent-video batch.
  ~/.presenter-tools/cbx/bin/python -I vo_gen.py POST [line numbers...]   (SEED=N for another take; default 1000 + line)
Reads POST/vo/lines.txt (one spoken line each; '|' splits say text from nothing else). Writes POST/vo/L<n>.wav. $0, local."""
import os, sys, time, torch, torchaudio as ta
from pathlib import Path
post = Path(sys.argv[1]).resolve()
lines = [l.strip() for l in (post / "vo/lines.txt").read_text().splitlines() if l.strip()]
pick = [int(x) for x in sys.argv[2:]] or range(len(lines))
REF = Path("/home/user/dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav")
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cpu")
for n in pick:
    t0 = time.time(); seed = int(os.environ.get("SEED", 1000)) + n; torch.manual_seed(seed)
    wav = model.generate(lines[n], audio_prompt_path=str(REF), exaggeration=0.75, cfg_weight=0.35)
    ta.save(str(post / f"vo/L{n}.wav"), wav, model.sr)
    print(f"VO_OK L{n} seed {seed} {wav.shape[-1] / model.sr:.1f}s in {time.time() - t0:.0f}s", flush=True)
print("VO_ALL_DONE", flush=True)
