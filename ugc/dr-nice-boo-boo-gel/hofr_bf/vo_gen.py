"""Boo-Boo Gel HofR Black Friday VO (Ralph 2026-11-12: "Do not use 11 Labs for voiceovers"): Ralph's free local
Chatterbox clone, Sorry I Lied settings (exaggeration 0.75, cfg 0.35, one seed per line). Copied from Dayone-ai
products/ai-on-autopilot/series/sorry-i-lied/ep7/vo_gen.py. Run: ~/.presenter-tools/cbx/bin/python -I vo_gen.py [n ...]
SEED=<base> re-seeds; writes vo/L<n>.wav."""
import json, os, sys, time, torch, torchaudio as ta
from pathlib import Path
HERE = Path(__file__).resolve().parent
REF = Path("/home/user/dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav")
lines = json.loads((HERE / "vo/lines.json").read_text())
only = [int(a) for a in sys.argv[1:]]
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cpu")
for n, l in enumerate(lines):
    if only and n not in only: continue
    t0 = time.time(); torch.manual_seed(int(os.environ.get("SEED", 1000)) + n)
    wav = model.generate(l["say"], audio_prompt_path=str(REF), exaggeration=0.75, cfg_weight=0.35)
    ta.save(str(HERE / f"vo/L{n}.wav"), wav, model.sr)
    print(f"VO_OK L{n} {wav.shape[-1] / model.sr:.1f}s in {time.time() - t0:.0f}s", flush=True)
print("VO_ALL_DONE", flush=True)
