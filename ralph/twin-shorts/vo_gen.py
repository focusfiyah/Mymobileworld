"""Ralph's free Chatterbox clone (approved sample + Take 2 settings) -> vo/vo.wav, one sentence at a time."""
import os, sys, time, torch, torchaudio as ta
from pathlib import Path
HERE = Path(__file__).parent
REF = "/home/user/Dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
lines = [l.strip() for l in (HERE / "vo_script.txt").read_text().splitlines() if l.strip()]
only = [int(x) for x in sys.argv[1:]]
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
m = ChatterboxTTS.from_pretrained(device="cpu")
for n, p in enumerate(lines):
    f = HERE / f"vo/line{n}.wav"
    if only and n not in only: continue
    torch.manual_seed(int(os.environ.get("SEED", 1000)) + n); t0 = time.time()
    w = m.generate(p, audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)
    ta.save(str(f), w, m.sr); print(f"VO_OK {n} {w.shape[-1]/m.sr:.1f}s {time.time()-t0:.0f}s: {p}", flush=True)
