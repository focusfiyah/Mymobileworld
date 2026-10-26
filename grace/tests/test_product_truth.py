"""Tests for the product-truth check in grace/prompt_check.py (Ralph 2026-10-26: real product photos always win).
  python3 grace/tests/test_product_truth.py   -> "ALL CHECKS PASSED (n)" or the failures"""
import contextlib, io, json, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import prompt_check as pc
R = []
def ok(n, c, d=""): R.append(c); print(("PASS " if c else "FAIL ") + n + ("" if c else f"  [{d[:300]}]"))
def exits(fn, *a):
    try:
        with contextlib.redirect_stderr(io.StringIO()): fn(*a)
        return False, ""
    except SystemExit as e: return True, str(e.code)
GOOD = "A pouch with a flat tear-off top, no screw cap and no spout; a straw stands in the torn opening. No text."
BAD = "The pouch's magenta screw cap has been twisted off and a straw stands in the spout. No text."
with tempfile.TemporaryDirectory() as t:
    j = Path(t) / "job"; (j / "refs").mkdir(parents=True); (j / "refs/front.jpg").write_bytes(b"x")
    (j / "checklist.json").write_text(json.dumps({"date": "2026-10-26"}))
    body = lambda p: {"input": {"prompt": p, "image_input": ["u"]}}
    e, m = exits(pc.require, str(j), body(GOOD)); ok("new job without product_truth.json is refused", e and "product_truth.json" in m, m)
    ok("mark refuses too without the file", any("product_truth" in x for x in pc.mark(str(j), [("a", GOOD, 1)])))
    (j / "product_truth.json").write_text(json.dumps({"photos": ["refs/front.jpg"], "facts": ["flat tear-off tab"], "forbid": ["screw cap", "spout"]}))
    ok("negated mentions pass", pc.truth_errors(GOOD, pc.truth(str(j))[0]) == [])
    ok("a described screw cap is caught", any("screw cap" in x for x in pc.truth_errors(BAD, pc.truth(str(j))[0])))
    ok("mark refuses the bad prompt", pc.mark(str(j), [("b", BAD, 1)]) != [])
    ok("mark accepts the good prompt", pc.mark(str(j), [("g", GOOD, 1)]) == [])
    e, m = exits(pc.require, str(j), body(GOOD)); ok("require passes a checked, true prompt", not e, m)
    (j / "product_truth.json").write_text(json.dumps({"photos": ["refs/missing.jpg"], "forbid": []}))
    e, m = exits(pc.require, str(j), body(GOOD)); ok("a missing real photo is refused", e and "does not exist" in m, m)
    old = Path(t) / "old"; old.mkdir(); (old / "checklist.json").write_text(json.dumps({"date": "2026-10-20"}))
    ok("jobs before 2026-10-26 need no file", pc.truth(str(old)) == (None, []))
print(f"ALL CHECKS PASSED ({len(R)})" if all(R) else f"FAILED {R.count(False)} of {len(R)}")
