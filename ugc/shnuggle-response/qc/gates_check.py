"""Job gate checks for GATES.md. python3 qc/gates_check.py <name> -> prints '<name> PASS' or the reason."""
import json, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parents[1]; name = sys.argv[1]
def dur(f): return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(f)], capture_output=True, text=True).stdout or 0)
def ok(c, why): print(f"{name} PASS" if c else f"{name} FAIL: {why}"); sys.exit(0 if c else 1)
S = json.loads((J / "shots.json").read_text())
if name == "vo_match":
    ok(all(" ".join(s["vo"] for s in S["videos"][v]).split() == (J / f"vo/{v}.txt").read_text().split() for v in ("R1", "R2")), "shot VO differs from script")
if name == "plan_gate":
    r = subprocess.run([sys.executable, str(J.parents[1] / "grace/gate.py"), str(J)], capture_output=True, text=True); ok(r.returncode == 0, r.stdout + r.stderr)
if name == "finals":
    fs = [J / f"out/shnuggle_{v}.mp4" for v in ("R1", "R2")]; ok(all(f.exists() and dur(f) > 30 for f in fs), "final mp4 missing or short")
if name == "different":
    ids = [set(s.get("src", "") + s["id"] for s in S["videos"][v]) for v in ("R1", "R2")]
    srcs = [{s["src"] for s in S["videos"][v] if s["src"].startswith("plate")} for v in ("R1", "R2")]
    ok(not (srcs[0] & srcs[1]), "same plate used in both videos")
if name == "cut_gate":
    r = subprocess.run([sys.executable, str(J.parents[1] / "grace/gate.py"), str(J), "--stage", "cut"], capture_output=True, text=True); ok(r.returncode == 0, r.stdout + r.stderr)
if name == "qc_report":
    f = J / "qc/QC.md"; t = f.read_text() if f.exists() else ""; ok("ALL CLEAR" in t and "R1" in t and "R2" in t, "qc/QC.md missing or not all clear")
ok(False, "unknown check")
