"""Plan-stage checks for GATES.md (python3, stdlib only). Usage: checks.py truth|book|sent|nospend"""
import json, re, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parents[1]
def fail(m): print("FAIL:", m); sys.exit(1)
w = sys.argv[1]
if w == "truth":
    t = json.loads((J / "product_truth.json").read_text())
    for p in t["photos"]:
        if not (J / p).exists(): fail(f"missing photo {p}")
    if len(t["facts"]) < 3 or len(t["forbid"]) < 3: fail("thin truth file")
    r = subprocess.run([sys.executable, str(J.parents[1] / "grace/prompt_check.py"), "lint", str(J / "shots.json")], capture_output=True, text=True)
    if "PROMPT_LINT_OK" not in r.stdout: fail("prompt lint: " + r.stdout[-300:])
    print("TRUTH_OK")
elif w == "book":
    b = (J / "BOOK.md").read_text()
    s = json.loads((J / "shots.json").read_text())["shots"]
    tot = sum(x["window"][1] - x["window"][0] for x in s)
    if not 10.0 <= tot <= 12.0: fail(f"video length {tot}")
    vo = (J / "research/vo_script.txt").read_text()
    n = len(re.findall(r"[\w']+", vo)); sec = n / 3.3
    if not 26 <= sec <= 36: fail(f"VO {sec:.1f}s")
    if "It's in the orange cart." not in vo: fail("no orange cart close")
    for f in ["readability_v1.txt", "readability_v2.txt"]:
        g = float(re.search(r"Flesch-Kincaid\):\s*([\d.]+)", (J / "research" / f).read_text()).group(1))
        if g > 6: fail(f"{f} grade {g}")
    if s[-1]["kind"] != "HAND-FREE" or "only ring" not in s[-1]["still"]: fail("end shot is not one product")
    for x in s:
        if x["id"] not in b: fail(f"shot {x['id']} not in BOOK.md")
    if vo.splitlines()[0] not in b: fail("VO script not in BOOK.md")
    print(f"BOOK_OK video {tot:.1f}s, VO {n} words ~{sec:.0f}s")
elif w == "sent":
    b = (J / "BOOK.md").read_text()
    if len(re.findall(r"(?m)^TOTAL: \$\d", b)) != 1: fail("need exactly one TOTAL line")
    if not re.search(r"Month so far.*\$\d", b): fail("no month spend line")
    if not re.search(r"(?m)^Sent to Ralph: https://claude\.ai/\S+", b): fail("no Sent to Ralph link")
    print("SENT_OK")
elif w == "nospend":
    if (J / "paid_tasks.json").exists() or (J / "kie_log.json").exists(): fail("paid task found")
    print("NOSPEND_OK")
