"""Tests for Grace's research workflow check in grace/gate.py (Ralph + Grace 2026-11-02).
  python3 grace/tests/test_research.py   -> "RESEARCH_TESTS_OK (n)" or the failures"""
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import gate
R = []
def ok(n, c, d=""): R.append(c); print(("PASS " if c else "FAIL ") + n + ("" if c else f"  [{str(d)[:400]}]"))

W = "words " * 16
GOOD = f"""# Research: Test product
## Product differentiation
{W}
## Target buyer
{W}
## Pain points and desires
{W}
## Buyer motivation
{W}
## Existing content research
{W}
## Objections and purchase justification
{W}
## Content opportunities
{W}
## Overall verdict
Short verdict.
### The two-second setup is the hook.
- H002: This is the part I actually care about
- NEW: a fresh one
### The soft feel is the desire.
- H003: I keep reaching for this more than I expected
- H002: This is the part I actually care about
### The washable cover is the objection killer.
- H002: This is the part I actually care about
- NEW: another
### The two-pack is the purchase justification.
- H003: I keep reaching for this more than I expected
- NEW: one more
"""

def job(md=None, **c):
    d = Path(tempfile.mkdtemp())
    if md is not None: (d / "research").mkdir(); (d / "research" / "RESEARCH.md").write_text(md)
    return d, {"created": "2026-11-02", "research": {"proof": ["research/RESEARCH.md"]}, **c}

d, c = job(GOOD); e = gate.check_research(d, c); ok("filled research passes", e == [], e)
d, c = job(None); e = gate.check_research(d, c); ok("new job without RESEARCH.md fails", any("not found" in x for x in e), e)
d, c = job(GOOD); c["research"]["proof"] = []; e = gate.check_research(d, c); ok("new job with no proof fails", bool(e), e)
tpl = (Path(gate.__file__).parent / "research" / "TEMPLATE.md").read_text()
d, c = job(tpl); e = gate.check_research(d, c); ok("unfilled template fails on placeholders", any("placeholders" in x for x in e), e)
d, c = job(GOOD.replace("H003", "H999")); e = gate.check_research(d, c); ok("unknown hook id fails", any("H999" in x for x in e), e)
d, c = job(GOOD.replace("### The washable cover is the objection killer.", "### Washable cover.")); e = gate.check_research(d, c)
ok("missing role line fails", any("objection killer" in x for x in e), e)
d, c = job(GOOD.replace("- H002: This is the part I actually care about\n- NEW: another", "- NEW: only new\n- NEW: another"))
e = gate.check_research(d, c); ok("role with only NEW hooks fails", any("library hook" in x for x in e), e)
d, c = job(GOOD.replace("## Buyer motivation\n" + W, "## Buyer motivation\ntoo short")); e = gate.check_research(d, c)
ok("thin section fails", any("too thin" in x for x in e), e)
d, c = job(GOOD.replace("## Target buyer", "## Buyer")); e = gate.check_research(d, c); ok("missing section fails", any("target buyer" in x for x in e), e)
ok("old job (no created, no research key) is not required", gate.check_research(Path(tempfile.mkdtemp()), {"scripts": []}) == [])
ok("research_legacy skips it", gate.check_research(Path(tempfile.mkdtemp()), {"created": "2026-11-05", "research_legacy": True}) == [])
d, c = job(None); c.pop("research"); e = gate.check_research(d, c); ok("job created today with the step removed still fails", bool(e), e)
# the full check() lists the research step for a new job
d = Path(tempfile.mkdtemp()); gate.init(d); cl = json.loads((d / "checklist.json").read_text())
ok("--init writes created + research step", cl.get("created") and "research" in cl, cl.keys())
ok("check() reports missing research on a new job", any(x.startswith("research") for x in gate.check(d)))

print(("RESEARCH_TESTS_OK" if all(R) else "RESEARCH_TESTS_FAILED") + f" ({sum(R)}/{len(R)})")
sys.exit(0 if all(R) else 1)
