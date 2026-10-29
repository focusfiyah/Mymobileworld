"""Test line in Ralph's FREE voice clone (Chatterbox, Resemble AI, MIT), the clone Ralph approved 2026-10-29 for the
AI on Autopilot presenter reels: sample Dayone-ai products/ai-on-autopilot/avatar/voice/ralph_ref.wav, settings Take 2
(exaggeration 0.75, cfg 0.35). One sentence at a time (the reels' 4-7 s lines), joined with short pauses -> vo/line_cbx.wav.
Run: ~/.presenter-tools/cbx/bin/python -I vo_cbx.py   ($0, CPU)"""
import os, re, time, torch, torchaudio as ta
from pathlib import Path
HERE = Path(__file__).parent
REF = "/home/user/Dayone-ai/products/ai-on-autopilot/avatar/voice/ralph_ref.wav"
text = (HERE / "script.txt").read_text().strip()
parts = [p for p in re.split(r"(?<=[.!?])\s+", text) if p]
torch.set_num_threads(4)
from chatterbox.tts import ChatterboxTTS
model = ChatterboxTTS.from_pretrained(device="cpu")
out = []
for n, p in enumerate(parts):
    t0 = time.time(); torch.manual_seed(int(os.environ.get("SEED", 1000)) + n)
    w = model.generate(p, audio_prompt_path=REF, exaggeration=0.75, cfg_weight=0.35)
    out += [w, torch.zeros(1, int(model.sr * 0.18))]
    print(f"VO_OK part {n} {w.shape[-1] / model.sr:.1f}s in {time.time() - t0:.0f}s: {p}", flush=True)
ta.save(str(HERE / "vo/line_cbx.wav"), torch.cat(out[:-1], dim=1), model.sr)
print("VO_ALL_DONE", flush=True)
