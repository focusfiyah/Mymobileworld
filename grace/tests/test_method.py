"""Tests for the Grace script method check in grace/gate.py (Ralph 2026-11-09, "Yes, all 4 steps").
  python3 grace/tests/test_method.py   -> "METHOD_TESTS_OK (n)" or the failures"""
import sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import gate
R = []
def ok(n, c, d=""): R.append(c); print(("PASS " if c else "FAIL ") + n + ("" if c else f"  [{str(d)[:300]}]"))
FISH = "## Big Fish (why ladder)\n- feels heavy\n- can't make the gym\n- thinks she is lazy\nBiggest feeling: I'm lazy\n"
AUDIT = """## Script 1
Buyer: women 30+ with no time
Pain: feels lazy
Connection: it adds movement with no plan
Outsider test: broad, no qualifiers
Common enemy: complicated routines
Contradiction check: no whole-result claim
Repetition pass: no line said twice
Pain points: 1
Selling points: 2
| You're not lazy. | GREEN |
| It adds daily movement. | GREEN |
| It's in the orange cart. | YELLOW |
Cut: "So I step on" RED (narration)
"""
def run(fish=FISH, audit=AUDIT, created="2026-11-09", legacy=False):
    d = Path(tempfile.mkdtemp()); (d / "research").mkdir()
    (d / "research" / "RESEARCH.md").write_text("# R\n" + fish)
    (d / "research" / "line_audit.md").write_text(audit)
    c = {"created": created, "line_audit": {"proof": ["research/line_audit.md"]}}
    if legacy: c = {"created": created, "method_legacy": True}
    return gate.check_method(d, c)
ok("good passes", run() == [], run())
ok("old job skipped", gate.method_required({"created": "2026-11-05"}) is False)
ok("new job required", gate.method_required({"created": "2026-11-09"}) is True)
ok("legacy skipped", run(legacy=True) == [])
ok("no big fish", any("Big Fish" in e for e in run(fish="")))
ok("thin ladder", any("rungs" in e for e in run(fish="## Big Fish\n- one\nBiggest feeling: x\n")))
ok("no biggest feeling", any("Biggest feeling" in e for e in run(fish=FISH.replace("Biggest feeling: I'm lazy\n", ""))))
ok("missing connection", any("Connection" in e for e in run(audit=AUDIT.replace("Connection: it adds movement with no plan\n", ""))))
ok("4 pain points", any("pain points 4" in e for e in run(audit=AUDIT.replace("Pain points: 1", "Pain points: 4"))))
ok("RED left in", any("still RED" in e for e in run(audit=AUDIT.replace("| It adds daily movement. | GREEN |", "| It adds daily movement. | RED |"))))
ok("RED under Cut is fine", run() == [])
ok("too few marked lines", any("GREEN or YELLOW" in e for e in run(audit=AUDIT.replace("| GREEN |", "|"))))
ok("commercial scent banned", any(__import__("re").search(p, "run don't walk to get this", __import__("re").I) for p in gate.BANNED))
print(("METHOD_TESTS_OK" if all(R) else "METHOD_TESTS_FAILED") + f" ({sum(R)}/{len(R)})")
