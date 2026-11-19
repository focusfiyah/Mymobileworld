"""python3 close_gaps.py NAME: read the gap meter on out/wagbag_NAME.mp4 and add every quiet run > 0.25 s (and a long lead)
to videos.json as a source-time "drop" on its take, keeping KEEP_END after her voice and KEEP_START before it.
Prints how many drops were added; re-render with cut.py and run again until it adds 0."""
import json, subprocess, sys
from pathlib import Path
J = Path(__file__).parent; n = sys.argv[1]
sys.path.insert(0, str(J)); import cut
m = json.loads(subprocess.run([sys.executable, str(J / "gapmeter.py"), str(J / f"out/wagbag_{n}.mp4"), "0.25", "--json"], capture_output=True, text=True).stdout.splitlines()[1])
plan = json.loads((J / f"out/wagbag_{n}.json").read_text())
starts, t = [], 0.0
for s in plan["segs"]:
    d = round((s["b"] - s["a"]) * cut.FPS) / cut.FPS; starts.append((t, t + d, s)); t += d
def src(x):
    for a, b, s in starts:
        if a <= x < b: return s["src"], s["a"] + (x - a), a, b
    return None
V = json.loads((J / "videos.json").read_text()); v = [v for v in V["videos"] if v["name"] == n][0]
runs = [[l, st] for l, st in m["runs"]]
if m["lead"] > 0.15: runs.append([m["lead"] + cut.KEEP_END, -cut.KEEP_END])   # lead: drop up to KEEP_START before her first word
added, skipped = 0, 0
def drop(srcname, x, y):
    global added
    if y - x < 0.05: return
    for tk in v["takes"]:
        if tk["src"] == srcname and tk["a"] - 0.7 <= x <= tk["b"] + 0.7:
            dr = tk.setdefault("drop", [])
            if [round(x, 3), round(y, 3)] not in dr: dr.append([round(x, 3), round(y, 3)]); added += 1
            return
for l, st in runs:
    p, q = src(max(st, 0) + (cut.KEEP_END if st >= 0 else 0)), src(st + l - cut.KEEP_START - 1e-3)
    if not p or not q: skipped += 1; continue
    if p[2] == q[2]: drop(p[0], *sorted((p[1], q[1]))); continue
    # the gap spans a join between two segments: trim the tail of the first and the head of the second
    sp = [s for a, b, s in starts if a == p[2]][0]; sq = [s for a, b, s in starts if a == q[2]][0]
    drop(p[0], p[1], sp["b"] + 0.001); drop(q[0], sq["a"] - 0.001, q[1])
(J / "videos.json").write_text(json.dumps(V, indent=1))
print(f"{n}: {added} drops added, {skipped} skipped")
