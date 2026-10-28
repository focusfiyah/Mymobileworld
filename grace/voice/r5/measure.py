"""Closeness of each test voice to Grace's real take (resemblyzer) + echo. Run with /root/.demucs-venv/bin/python."""
import sys, os, json, subprocess, numpy as np
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
from resemblyzer import VoiceEncoder, preprocess_wav
import echo
H = os.path.dirname(os.path.abspath(__file__))
enc = VoiceEncoder("cpu")
def emb(p):
    w = os.path.splitext(p)[0] + "_16k.wav"
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", p, "-ac", "1", "-ar", "16000", w], check=True)
    e = enc.embed_utterance(preprocess_wav(w)); os.remove(w); return e
ref = emb(os.path.join(H, "ab/grace_real_take.mp3"))   # held out: not in the v5 clone
allg = np.mean([emb(os.path.join(H, "samples", f)) for f in sorted(os.listdir(os.path.join(H, "samples")))], 0)
out = {}
for n in ["v1_final", "v1_paced", "v5_paced"]:
    p = os.path.join(H, "ab", n + ".mp3"); e = emb(p)
    out[n] = {"to_real_take": round(float(np.dot(e, ref)), 3),
              "to_all_her_vos": round(float(np.dot(e, allg) / np.linalg.norm(allg)), 3),
              "rt60_est_ms": echo.measure(p)[0]}
    print(n, out[n])
json.dump(out, open(os.path.join(H, "ab/scores.json"), "w"), indent=1)
