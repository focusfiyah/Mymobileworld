"""Speech gaps in a cut: python3 gaps.py TRANSCRIPT_DIR [LIMIT] -> lead, tail, longest gap between spoken words and every gap > LIMIT (default 0.3 s).
Uses Whisper word timings (transcribe skill, medium.en). Whisper stretches word ends a little, so a real gap is a bit longer than shown.
Prints GAPS_OK when lead <= 0.15 s, every internal gap <= LIMIT, and tail <= 0.4 s."""
import json, sys, subprocess
d = sys.argv[1]; lim = float(sys.argv[2]) if len(sys.argv) > 2 else 0.3
w = [x for x in json.load(open(f"{d}/transcript_words.json"))["words"] if x.get("type", "word") == "word"]
dur = float(sys.argv[3]) if len(sys.argv) > 3 else w[-1]["end"]
g = [(round(b["start"] - a["end"], 2), round(a["end"], 2), a["text"].strip(), b["text"].strip()) for a, b in zip(w, w[1:])]
big = [x for x in g if x[0] > lim]
lead, tail = w[0]["start"], dur - w[-1]["end"]
mx = max(x[0] for x in g)
print(f"lead={lead:.2f}s tail={tail:.2f}s longest_gap={mx:.2f}s gaps_over_{lim}={len(big)} total_over={sum(x[0] for x in big):.1f}s")
for x in big: print("  ", x)
print("GAPS_OK" if lead <= 0.15 and not big and tail <= 0.4 else "GAPS_FAIL")
