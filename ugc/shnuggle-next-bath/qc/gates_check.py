"""Gate oracles for GATES.md (run from the repo root). Each prints '<name> PASS' or '<name> FAIL: why' and exits 0/1."""
import hashlib, json, re, subprocess, sys
from pathlib import Path
JOB = Path(__file__).resolve().parents[1]; ROOT = JOB.parents[1]
def ok(n, good, why=""):
    print(f"{n} PASS" if good else f"{n} FAIL: {why}"); sys.exit(0 if good else 1)
def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)], capture_output=True, text=True).stdout or 0)
n = sys.argv[1]; S = json.loads((JOB / "shots.json").read_text())
if n == "plan_gate":
    r = subprocess.run([sys.executable, str(ROOT / "grace/gate.py"), str(JOB)], capture_output=True, text=True); ok(n, r.stdout.startswith("GATE OK"), r.stdout[:300])
if n == "cut_gate":
    r = subprocess.run([sys.executable, str(ROOT / "grace/gate.py"), str(JOB), "--stage", "cut"], capture_output=True, text=True); ok(n, r.stdout.startswith("GATE OK"), r.stdout[:300])
if n == "shot_mix":
    sh = S["shots"]; free = sum(not s["hand"] for s in sh) / len(sh); ok(n, 1 / 3 <= free <= 0.5, f"hand-free share {free:.2f}")
if n == "vo_match":
    lines = " ".join((JOB / "vo/V1_lines.txt").read_text().split()); shots = " ".join(s["vo"] for s in S["shots"])
    AL = {"schnuggle": "shnuggle", "wanna": "wantto"}   # same aliases as vo.py (STT spelling of the brand; fast "want to")
    norm = lambda t: "".join(AL.get(w, w) for w in re.sub(r"[^a-z ]", "", t.lower().replace("’", "'").replace("'", "")).split())
    stt = JOB / "vo/stt.json"
    if not stt.exists(): ok(n, False, "no vo/stt.json yet")
    heard = norm(json.loads(stt.read_text())["text"])
    ok(n, norm(lines) == norm(shots) == heard, "script/shots/STT differ")
if n == "product_lock":
    k = (JOB / "kie.py").read_text(); sheet = JOB / "refs/product_sheet.png"
    ok(n, sheet.exists() and "tub_refs" in k and "reference_image_urls" in k and not any(w in k for w in ("pasteback", "label_track", "label.py")), "sheet missing or kie.py does not pass tub_refs / ref mode")
if n == "finals":
    f = JOB / "out/shnuggle_next_bath.mp4"
    if not f.exists(): ok(n, False, "no final")
    d = dur(f); fin = (JOB / "cut.py").read_text()
    ok(n, 25 <= d <= 35 and "ai_finish" in fin, f"duration {d:.2f}s or no ai_finish in cut.py")
if n == "different":
    old = {hashlib.sha256(p.read_bytes()).hexdigest() for p in (ROOT / "ugc/shnuggle-response").glob("clips*/*.mp4")}
    new = [p for p in (JOB / "clips").glob("*.mp4")]
    shared = [p.name for p in new if hashlib.sha256(p.read_bytes()).hexdigest() in old]
    ok(n, bool(new) and not shared, f"shared clips {shared} or no clips")
if n == "qc_report":
    q = JOB / "qc/QC.md"; ok(n, q.exists() and "ALL CLEAR" in q.read_text() and "FAIL" not in q.read_text(), "QC.md missing, not ALL CLEAR, or has FAIL")
ok(n, False, "unknown check")
