"""Ralph's pick E (2026-10-21, "E sounds good"): pauses capped at 0.15 s with NO rubberband stretch, then a plain
ffmpeg atempo speed-up to the same length, then resemble-enhance at lambd 0.9 (stronger cleanup), -16 LUFS.
Kept only if Whisper (small) misses no more script words than the uncleaned voice. -> vo/vN.mp3 (+ vo/ab/ copies)
  python3 voice_e.py N TEMPO"""
import json, re, difflib, subprocess, sys
from pathlib import Path
H = Path(__file__).resolve().parent; V = H.parents[2] / "grace/voice"
sys.path.insert(0, str(V / "stubs")); sys.path.insert(0, str(V))
import numpy as np, soundfile as sf, torch
from resemble_enhance.enhancer.inference import enhance
from echo import measure, load
from faster_whisper import WhisperModel
N, T = int(sys.argv[1]), float(sys.argv[2]); A = H / "vo/ab"
W = WhisperModel("small", device="cpu", compute_type="int8")
want = re.findall(r"[a-z']+", next(s for s in json.load(open(H / "scripts.json")) if s["video"] == N)["text"].lower().replace("’", "'").replace("-", " "))
def miss(p):
    segs, _ = W.transcribe(load(str(p))[0], language="en", initial_prompt="castor oil roll-on, grandmama, Imma do y'all a favor")
    sm = difflib.SequenceMatcher(None, want, re.findall(r"[a-z']+", " ".join(s.text for s in segs).lower().replace("-", " ")))
    return [want[i] for o in sm.get_opcodes() if o[0] in ("delete", "replace") for i in range(o[1], o[2])]
d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(H / f"vo/v{N}_raw.mp3")], capture_output=True, text=True).stdout)
ns, at = A / f"v{N}_D_nostretch.mp3", A / f"v{N}_B_atempo.mp3"
out = subprocess.run([sys.executable, str(V / "pace.py"), str(H / f"vo/v{N}_raw.mp3"), str(ns), "--len", "999"], capture_output=True, text=True).stdout
cut = float(re.search(r"([\d.]+)s ->", out).group(1))
subprocess.run([sys.executable, str(V / "pace.py"), str(H / f"vo/v{N}_raw.mp3"), str(ns), "--len", f"{cut}"], check=True, capture_output=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(ns), "-af", f"atempo={T},loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", str(at)], check=True)
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(at), "-ac", "1", "-ar", "44100", "-f", "f32le", "-"], capture_output=True, check=True).stdout
torch.manual_seed(int(sys.argv[3]) if len(sys.argv) > 3 else 0)
e, sr = enhance(torch.from_numpy(np.frombuffer(raw, np.float32).copy()), 44100, "cpu", nfe=64, solver="midpoint", lambd=0.9, tau=0.1)
sf.write(str(A / f"v{N}_E.wav"), e.numpy(), sr)
E = A / f"v{N}_E_atempo_strongclean.mp3"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", str(A / f"v{N}_E.wav"), "-af", "loudnorm=I=-16:TP=-1.5", "-ar", "44100", "-b:a", "192k", str(E)], check=True)
m0, m1 = miss(at), miss(E); b, c = measure(str(at)), measure(str(E))
print(f"v{N}: atempo x{T} tail {b[1]:.1f} dB misses {m0} | E tail {c[1]:.1f} dB misses {m1}")
assert len(m1) <= len(m0), "cleanup changed words: not used"
(H / f"vo/v{N}.mp3").write_bytes(E.read_bytes()); print(f"v{N} -> vo/v{N}.mp3")
