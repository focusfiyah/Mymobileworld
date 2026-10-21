"""Echo cleanup for one remix voiceover (2026-10-21, Ralph: "We need to fix that echo, the video 3 sounds better").
Same model as grace/voice/clean.py (resemble-enhance, tau 0.1), but every try is saved and judged by the stronger
Whisper (small) against the SCRIPT, not by exact equality with a base-model transcript (that rejected every try on 1, 2, 4
over plural s's). A try is kept only if it misses no more script words than the input does; the driest kept try wins.
  python3 declean.py N [--tries 4]   -> vo/vN_clean.mp3 + vo/vN_tries/ + prints the table"""
import difflib, json, os, re, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V = H.parents[2] / "grace/voice"
sys.path.insert(0, str(V / "stubs")); sys.path.insert(0, str(V))
import numpy as np, soundfile as sf, torch
from resemble_enhance.enhancer.inference import enhance
from echo import measure, load
from faster_whisper import WhisperModel
N = int(sys.argv[1]); T = int(sys.argv[sys.argv.index("--tries") + 1]) if "--tries" in sys.argv else 4
W = WhisperModel("small", device="cpu", compute_type="int8")
want = re.findall(r"[a-z']+", next(s for s in json.load(open(H / "scripts.json")) if s["video"] == N)["text"].lower().replace("’", "'").replace("-", " "))
def miss(p):
    segs, _ = W.transcribe(load(str(p))[0], language="en", initial_prompt="castor oil roll-on, grandmama, Imma do y'all a favor")
    heard = re.findall(r"[a-z']+", " ".join(s.text for s in segs).lower().replace("-", " "))
    sm = difflib.SequenceMatcher(None, want, heard)
    return [want[i] for o in sm.get_opcodes() if o[0] in ("delete", "replace") for i in range(o[1], o[2])]
inp = H / f"vo/v{N}_paced.mp3"; D = H / f"vo/v{N}_tries"; D.mkdir(exist_ok=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(inp), "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, check=True).stdout
wav = torch.from_numpy(np.frombuffer(raw, np.float32).copy())
b = measure(str(inp)); m0 = miss(inp)
print(f"input: rt {b[0]:.0f} ms, tail {b[1]:.1f} dB, misses {m0}", flush=True)
best = None
for seed in range(T):
    torch.manual_seed(seed)
    e, sr = enhance(wav, 44100, "cpu", nfe=64, solver="midpoint", lambd=0.5, tau=0.1)
    p = D / f"s{seed}.wav"; sf.write(str(p), e.numpy(), sr)
    rt, tail, _, _ = measure(str(p)); m = miss(p); ok = len(m) <= len(m0)
    print(f"seed {seed}: rt {rt:.0f} ms, tail {tail:.1f} dB, misses {m} {'OK' if ok else 'REJECT'}", flush=True)
    if ok and (best is None or (tail, rt) < best[:2]): best = (tail, rt, p)
if best is None: sys.exit("no try kept every word: keeping the paced voice")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(best[2]), "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", str(H / f"vo/v{N}_clean.mp3")], check=True)
print(f"kept {best[2].name}: tail {best[0]:.1f} dB (input {b[1]:.1f}), rt {best[1]:.0f} ms -> vo/v{N}_clean.mp3")
