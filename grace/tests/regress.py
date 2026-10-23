"""G2: the script-gate output of 4 real jobs (plan + cut) matches the baseline saved before the 2026-10-22 change,
apart from the new BOOK line, which must be there."""
import subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("baseline")
same = 0
for f in sorted(BASE.glob("*.txt")):
    job, cut = f.name.split(".")[0], f.name.endswith(".cut.txt")
    args = [sys.executable, str(ROOT / "grace/gate.py"), str(ROOT / "ugc" / job)] + (["--stage", "cut"] if cut else [])
    out = subprocess.run(args, capture_output=True, text=True, cwd=ROOT)
    lines = (out.stdout + out.stderr).splitlines()
    rest = [l for l in lines if not l.startswith("BOOK: ")]
    if rest == f.read_text().splitlines() and len(rest) < len(lines):
        same += 1
    else:
        print("DIFFERS:", f.name)
print(f"REGRESSION OK {same}/{len(list(BASE.glob('*.txt')))}" if same == len(list(BASE.glob("*.txt"))) else f"REGRESSION {same} same")
