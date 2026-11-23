"""python3 drop_slivers.py NAME: any piece under 0.7 s in out/wagbag_NAME.json that holds no voice (its loudest 30 ms stays below
floor + 35% of (peak - floor) of its take) is noise between her lines: add it to that take's drops. Prints how many were added."""
import json, sys
from pathlib import Path
J = Path(__file__).parent; sys.path.insert(0, str(J)); import cut, numpy as np
n = sys.argv[1]; segs = json.loads((J / f"out/wagbag_{n}.json").read_text())["segs"]
V = json.loads((J / "videos.json").read_text()); v = [x for x in V["videos"] if x["name"] == n][0]; added = 0
for s in segs:
    if s["b"] - s["a"] >= 0.7: continue
    tk = [t for t in v["takes"] if t["src"] == s["src"] and t["a"] - 0.05 <= s["a"] < t["b"]][0]   # the take this piece starts in (2026-11-21: +-0.7 picked the take before)
    db = cut.env(tk["src"], tk["a"], tk["b"]); fl, pk = np.percentile(db, 10), np.percentile(db, 97)
    seg = cut.env(s["src"], s["a"], s["b"]); loud = np.convolve(seg, np.ones(3) / 3, "same").max()
    line = max(fl + 0.35 * (pk - fl), pk - 15)   # her voice is never more than 15 dB under her peak (2026-11-21: -39 dB breath slivers counted as voice)
    if loud < line:
        tk.setdefault("drop", []).append([round(s["a"] - 0.001, 3), round(s["b"] + 0.001, 3)]); added += 1
        print(f"  {n}: drop sliver {s['src']} {s['a']:.2f}-{s['b']:.2f} (max {loud:.0f} dB, voice line {line:.0f})")
    else:
        print(f"  {n}: keep {s['src']} {s['a']:.2f}-{s['b']:.2f} (voice, max {loud:.0f} dB)")
(J / "videos.json").write_text(json.dumps(V, indent=1)); print(f"{n}: {added} slivers dropped")
