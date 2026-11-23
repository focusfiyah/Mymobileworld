"""Ralph's free Chatterbox clone (Sorry I Lied settings: exaggeration 0.75, cfg 0.35, one seed per line).
  <cbx>/bin/python -I vo_gen.py JOBDIR... ; ONLY=1,4 redoes those lines; SEED_<n>=<seed> overrides one line's seed.
Writes JOBDIR/vo/L<n>.wav. Ref: Dayone-ai products/ai-on-autopilot/avatar/voice/ralph_ref.wav (sha256 21b15d47...)."""
import os, sys, time, torch, torchaudio as ta
from pathlib import Path
JOBS = [Path(a) for a in sys.argv[1:]]; only = {int(x) for x in os.environ.get("ONLY", "").split(",") if x}
REF = "/home/user/dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
for J in JOBS:
  lines = [l.strip() for l in (J / "vo/lines.txt").read_text().splitlines() if l.strip()]
  for n, t in enumerate(lines):
      if only and n not in only: continue
      s = int(os.environ.get(f"SEED_{n}", 1000 + n)); torch.manual_seed(s); t0 = time.time()
      w = m.generate(t, audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)
      ta.save(str(J / f"vo/L{n}.wav"), w, m.sr)
      print(f"VO_OK L{n} seed {s} {w.shape[-1]/m.sr:.1f}s in {time.time()-t0:.0f}s", flush=True)
