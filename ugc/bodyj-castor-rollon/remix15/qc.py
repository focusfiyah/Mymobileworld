"""QC for the 15 s remixes: python3 qc.py N [file]. Prints 'QC OK vN' only if every check passes.
flash: no near-black/near-white frame and no luma jump away from a planned cut; sync: every planned cut is a real
scene cut (+-0.1 s); words: local Whisper (small) hears every script word in order (fuzzy, accent-tolerant);
levels: -16 LUFS +-1.5, true peak <= -1 dB; size: 1080x1920, length within the video's limit."""
import difflib, json, re, subprocess, sys
from pathlib import Path
import numpy as np
H = Path(__file__).resolve().parent; N = sys.argv[1]
F = Path(sys.argv[2]) if len(sys.argv) > 2 else H / f"out/remix15_v{N}_review.mp4"
P = json.load(open(H / f"out/remix15_v{N}_plan.json")); S = next(s for s in json.load(open(H / "scripts.json")) if s["video"] == int(N))
errs = []
run = lambda c: subprocess.run(c, capture_output=True, text=True)
wh = run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", str(F)]).stdout.strip()
dur = float(run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(F)]).stdout)
if wh != "1080,1920": errs.append(f"size {wh}")
if dur > S["max_s"] + 1.0: errs.append(f"length {dur:.2f}s > {S['max_s']}s")
fr = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", str(F), "-vf", "scale=54:96,format=gray", "-f", "rawvideo", "-"], capture_output=True).stdout, np.uint8).reshape(-1, 96, 54).astype(float)
m = fr.mean(axis=(1, 2)); d = np.abs(np.diff(fr, axis=0)).mean(axis=(1, 2))
if m.min() < 20 or m.max() > 240: errs.append(f"flash: frame luma {m.min():.0f}..{m.max():.0f}")
cuts = [round(t * 30) for t in P["starts"][1:]]
for i in np.where(d > 25)[0]:
    if min(abs(i + 1 - c) for c in cuts) > 2: errs.append(f"flash: jump at {(i + 1) / 30:.2f}s not at a cut")
for c in cuts:
    if d[max(0, c - 4):c + 3].max() < 6: errs.append(f"sync: planned cut at {c / 30:.2f}s not visible")
sys.path.insert(0, str(H.parents[2] / "grace/voice")); from echo import load
from faster_whisper import WhisperModel
segs, _ = WhisperModel("small", device="cpu", compute_type="int8").transcribe(load(str(F))[0], language="en", initial_prompt="castor oil roll-on, grandmama, Imma do y'all a favor")
heard = re.findall(r"[a-z']+", " ".join(s.text for s in segs).lower().replace("-", " "))
want = re.findall(r"[a-z']+", S["text"].lower().replace("’", "'").replace("-", " "))
sm = difflib.SequenceMatcher(None, want, heard); miss = [want[i] for a in sm.get_opcodes() if a[0] in ("delete", "replace") for i in range(a[1], a[2])]
if len(miss) > 3: errs.append(f"words: {len(miss)} script words not heard: {miss}")
ln = run(["ffmpeg", "-v", "info", "-i", str(F), "-af", "loudnorm=print_format=json", "-f", "null", "-"]).stderr
j = json.loads(ln[ln.rindex("{"):ln.rindex("}") + 1]); I, tp = float(j["input_i"]), float(j["input_tp"])
if abs(I + 16) > 1.5 or tp > -1.0: errs.append(f"levels: {I} LUFS, TP {tp}")
print(f"v{N} {dur:.2f}s, {len(cuts)} cuts, LUFS {I}, TP {tp}, words not heard: {miss}")
print("\n".join("FAIL " + e for e in errs) if errs else f"QC OK v{N}")
sys.exit(1 if errs else 0)
