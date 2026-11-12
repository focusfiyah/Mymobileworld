"""Ralph's free Chatterbox voice for the NovaTabz HofR holiday test (Ralph 2026-11-12: "Do not use 11 Labs").
Settings as Sorry I Lied ep7 (exaggeration 0.75, cfg 0.35), one seed per line. Run with the Chatterbox venv:
  ~/.presenter-tools/cbx/bin/python -I vo_gen.py [line numbers to redo]   (SEED_<n>=... re-seeds one line; line 3 uses SEED_3=2003, the shortest of 4 seeds, to fit S3)
Writes vo/L<n>.wav (24 kHz). join.py builds vo/ralph_cbx.wav."""
import os, sys, time, torch, torchaudio as ta
from pathlib import Path
H = Path(__file__).resolve().parent
REF = "/home/user/dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
lines = [l for l in (H / "vo/lines.txt").read_text().split("\n") if l.strip()]
todo = [int(x) for x in sys.argv[1:]] or range(len(lines))
torch.set_num_threads(os.cpu_count())
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cpu")
for n in todo:
    t0 = time.time(); torch.manual_seed(int(os.environ.get(f"SEED_{n}", 1000 + n)))
    wav = model.generate(lines[n], audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)
    ta.save(str(H / f"vo/L{n}.wav"), wav, model.sr)
    print(f"VO_OK L{n} {wav.shape[-1] / model.sr:.1f}s in {time.time() - t0:.0f}s", flush=True)
