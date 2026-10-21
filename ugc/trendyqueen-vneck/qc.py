"""QC for the TrendyQueen cut. Prints '<gate> OK' only when the check passes.
  python3 -I qc.py spec|words|pauses|flash|loud [file]"""
import json, subprocess, sys, difflib
from pathlib import Path
import numpy as np
J = Path(__file__).resolve().parent
sys.path.insert(0, "/home/user/Mymobileworld/.claude/skills/ugc-take-combos/scripts")
import take_combos as t
F = Path(sys.argv[2]) if len(sys.argv) > 2 else Path(json.loads((J / "tmp/V1/edl.json").read_text())["final"])
F = F if F.is_absolute() else J / F
def fail(m): print("FAIL", m); sys.exit(1)
def probe(k): return subprocess.run(["ffprobe", "-v", "error", "-select_streams", k[0], "-show_entries", k[1], "-of", "csv=p=0", str(F)], capture_output=True, text=True).stdout.strip()
g = sys.argv[1]
if g == "spec":
    w, h = probe(("v", "stream=width,height")).split(",")
    c, a = probe(("v", "stream=codec_name")), probe(("a", "stream=codec_name"))
    d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(F)], capture_output=True, text=True).stdout)
    print(w, h, c, a, round(d, 2))
    if (w, h, c, a) != ("1080", "1920", "h264", "aac") or not 30 < d < 44: fail("spec")
    print("spec OK")
elif g == "words":   # every source word is in the cut, in order (whisper on the output vs the source transcript)
    from faster_whisper import WhisperModel
    src = [t.norm(x[2]) for x in json.loads((J / "tmp/tx_full.json").read_text())]
    m = WhisperModel("small.en", device="cpu", compute_type="int8")
    got = [t.norm(x.word) for s in m.transcribe(t.pcm16k(F), word_timestamps=True)[0] for x in s.words]
    ops = [(o, src[a:b], got[c:d]) for o, a, b, c, d in difflib.SequenceMatcher(None, src, got).get_opcodes() if o != "equal"]
    print("diffs:", ops)
    if any(o == "delete" for o, *_ in ops): fail("dropped words")
    if len(got) < len(src) - 2: fail("word count")
    print("words OK")
elif g == "pauses":   # longest gap in the cut (same local-floor measure as the engine)
    p = t.Job(str(J / "job.json")).pauses(F)[:5]
    print("longest:", p)
    if p and p[0][1] > 0.50: fail("pause > 0.5s")
    print("pauses OK")
elif g == "flash":   # no black or blown frame anywhere (cuts included)
    r = subprocess.run(["ffmpeg", "-v", "error", "-i", str(F), "-vf", "scale=108:192,format=gray", "-f", "rawvideo", "-"], capture_output=True)
    y = np.frombuffer(r.stdout, np.uint8).reshape(-1, 192 * 108).mean(1)
    print("frames", len(y), "luma min/max", round(y.min(), 1), round(y.max(), 1))
    if y.min() < 25 or y.max() > 235: fail("flash")
    print("flash OK")
elif g == "loud":
    r = subprocess.run(["ffmpeg", "-nostats", "-i", str(F), "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    i = float(r.split("Integrated loudness:")[1].split("I:")[1].split("LUFS")[0])
    print("LUFS", i)
    if not -16 <= i <= -12: fail("loudness")
    print("loud OK")
