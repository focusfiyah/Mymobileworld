"""Gate checks for the Shnuggle slideshow. python3 qc/gates_check.py <name>"""
import hashlib, json, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parents[1]; R = J.parents[1]

def slides():
    from PIL import Image
    fs = sorted((J / "slides").glob("S*.jpg")); assert len(fs) == 6, f"{len(fs)} slides"
    for f in fs: assert Image.open(f).size == (1080, 1920), f"{f.name} {Image.open(f).size}"
    hs = {hashlib.sha256(f.read_bytes()).hexdigest() for f in fs}; assert len(hs) == 6, "duplicate slide"
    old = {hashlib.sha256(p.read_bytes()).hexdigest() for p in (R / "ugc/shnuggle-response/stills").glob("*.png")}
    assert not hs & old, "reuses an R1/R2 still"

def gate():
    out = subprocess.run([sys.executable, str(R / "grace/gate.py"), str(J)], capture_output=True, text=True); print(out.stdout[-400:])
    assert out.returncode == 0 and "GATE OK" in out.stdout

def spend():
    log = json.loads((J / "kie_log.json").read_text()) if (J / "kie_log.json").exists() else []
    ok = [e for e in log if e.get("result")]; cap = json.loads((J / "approved.json").read_text())["cap_usd"]
    usd = 0.09 * len(ok); print(f"{len(ok)} paid stills = ${usd:.2f} vs cap ${cap:.2f}"); assert usd <= cap + 1e-9

def qc():
    q = (J / "qc/QC.md").read_text(); assert "RESULT: ALL CLEAR" in q and q.count("| PASS") >= 6

if __name__ == "__main__":
    n = sys.argv[1]; globals()[n](); print(f"{n} PASS")
