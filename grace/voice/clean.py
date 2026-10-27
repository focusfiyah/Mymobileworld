"""Free echo cleanup for a Grace voiceover: resemble-enhance (Resemble AI, MIT; weights download from HuggingFace on first run).

Usage: python3 clean.py IN OUT [--tries 3] [--first 0] [--tau 0.1] [--lambd 0.5]
The model samples randomly, so one run can come out drier or echoier than the input (2026-10-20 test on one line: fast
decay 100 / 150 / 200 / 200 ms across runs, input 171). It runs --tries seeds and keeps the driest by echo.measure
(lowest fast-decay rt, then lowest tail) among the runs whose words still match the input, levels it with one plain gain toward -16 LUFS (peak <= -1 dBFS; a limiter raised the echo reading, 2026-10-27),
and warns if no run beat the input. The word check matters: one run turned "I'm obsessed" into "I hope Cess". Both sides
are transcribed by the same local Whisper model, so its own mishearings cancel out. If no run keeps every word, the
uncleaned input is kept. --tau is the model's randomness: at the package default 0.5, 7 of 8 runs changed a word; at
0.1 all 3 kept every word and came out about as dry (tested 2026-10-20), so 0.1 is the default.
About 5x real time per try on 4 CPU cores (a 30 s voiceover x 3 tries is roughly 8 minutes).

Setup once per session (the package pins an old pandas that won't build on Python 3.13, and imports deepspeed only
for training):
  pip install --no-deps resemble-enhance && pip install omegaconf librosa resampy rich tabulate tqdm celluloid matplotlib pandas ptflops
  pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
  sed -i 's/x0=0))/x0=0)[0])/' $(python3 -c "import resemble_enhance,os;print(os.path.dirname(resemble_enhance.__file__))")/enhancer/lcfm/cfm.py
The stubs/ folder next to this file stands in for deepspeed; this script puts it on the path itself.
"""
import argparse, os, subprocess, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "stubs"))
sys.path.insert(0, HERE)
import numpy as np, soundfile as sf, torch
from resemble_enhance.enhancer.inference import enhance
from echo import measure, load
import re
from faster_whisper import WhisperModel
WHISPER = WhisperModel("base", device="cpu", compute_type="int8")


def words(path):
    segs, _ = WHISPER.transcribe(load(path)[0], language="en", beam_size=5)
    return re.sub(r"[^a-z' ]", " ", " ".join(s.text for s in segs).lower()).split()

ap = argparse.ArgumentParser()
ap.add_argument("inp"); ap.add_argument("out")
ap.add_argument("--tries", type=int, default=3); ap.add_argument("--first", type=int, default=0); ap.add_argument("--lambd", type=float, default=0.5); ap.add_argument("--tau", type=float, default=0.1)
a = ap.parse_args()

raw = subprocess.run(["ffmpeg", "-v", "error", "-i", a.inp, "-ac", "1", "-ar", "44100", "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
wav = torch.from_numpy(np.frombuffer(raw, np.float32).copy())
base = measure(a.inp)
ref = words(a.inp)
print(f"input: rt {base[0]:.0f} ms, tail {base[1]:.1f} dB, {len(ref)} words")
best = None
with tempfile.TemporaryDirectory() as d:
    for seed in range(a.first, a.first + a.tries):   # --first: try new seeds after a run where every seed changed a word
        torch.manual_seed(seed)
        e, sr = enhance(wav, 44100, "cpu", nfe=64, solver="midpoint", lambd=a.lambd, tau=a.tau)
        p = os.path.join(d, f"s{seed}.wav")
        sf.write(p, e.numpy(), sr)
        rt, tail, _, _ = measure(p)
        got = words(p); same = got == ref
        diff = "" if same else " " + str([(x, y) for x, y in zip(ref, got) if x != y][:3]) + ("" if len(ref) == len(got) else f" {len(ref)}->{len(got)} words")
        print(f"seed {seed}: rt {rt:.0f} ms, tail {tail:.1f} dB, words {'match' if same else 'CHANGED'}{diff}", flush=True)
        if same and (best is None or (rt, tail) < best[:2]):
            best = (rt, tail, p)
    if best is None:
        print("WARNING: every try changed a word; keeping the uncleaned input")
        best = (base[0], base[1], a.inp)
    # Level with ONE plain gain, no limiter: toward -16 LUFS but never past -1 dBFS peak. Any limiter (one-pass loudnorm, or loudnorm
    # linear=true with its true-peak cap) reshaped the word tails and pushed echo.py from the kept take's 150 ms to 171
    # (PRITECH V2, 2026-10-27: four runs read 171 after leveling; the raw take and a plain-gain copy read 150).
    import re as _re
    st = subprocess.run(["ffmpeg", "-v", "info", "-i", best[2], "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    li = float(_re.findall(r"^\s+I:\s+(-?[\d.]+) LUFS", st, _re.M)[-1]); pk = float(_re.findall(r"^\s+Peak:\s+(-?[\d.]+) dBFS", st, _re.M)[-1])
    g = min(-16 - li, -1.0 - pk)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", best[2], "-af", f"volume={g:.2f}dB", "-ar", "44100"] + ([] if a.out.endswith(".wav") else ["-b:a", "192k"]) + [a.out], check=True)
    import shutil as _sh; _sh.copy(best[2], a.out + ".raw.wav")   # the kept take before leveling, to measure (echo.py) without the encoder
print(f"kept: rt {best[0]:.0f} ms, tail {best[1]:.1f} dB -> {a.out}")
if not (best[0] < base[0] or best[1] < base[1] - 1):
    print("WARNING: no try came out drier than the input; listen before using it")
