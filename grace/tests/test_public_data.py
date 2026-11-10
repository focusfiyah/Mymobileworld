"""Tests for the public_data gate step (Ralph 2026-11-10: standard, then "Keep it only for food, supplements and skincare").
  python3 grace/tests/test_public_data.py -> "PUBLIC_DATA_TESTS_OK (n)" or the failures"""
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1])); import gate
R = []
def ok(n, c): R.append(c); print(("PASS " if c else "FAIL ") + n)
def errs(c, with_file=True):
    d = Path(tempfile.mkdtemp()); (d / "research").mkdir()
    if with_file: (d / "research" / "public_data.md").write_text("# x")
    (d / "checklist.json").write_text(json.dumps(c))
    return [e for e in gate.check(d) if e.startswith(("public_data", "product_type"))]
P = {"public_data": {"proof": ["research/public_data.md"]}}
for t in ("food", "supplement", "skincare"):
    ok(f"{t} without proof is refused", bool(errs({"created": "2026-11-10", "product_type": t})))
    ok(f"{t} with proof passes", not errs({"created": "2026-11-10", "product_type": t, **P}))
ok("other needs no proof", not errs({"created": "2026-11-10", "product_type": "other"}))
ok("new job with no product_type is refused", bool(errs({"created": "2026-11-10"})))
ok("bad product_type is refused", bool(errs({"created": "2026-11-10", "product_type": "gadget"})))
ok("old job is not asked", not errs({"created": "2026-11-09"}))
ok("public_legacy skips it", not errs({"created": "2026-11-10", "public_legacy": True}))
ok("missing proof file is refused", bool(errs({"created": "2026-11-10", "product_type": "food", **P}, with_file=False)))
print(f"PUBLIC_DATA_TESTS_OK ({len(R)})" if all(R) else "PUBLIC_DATA_TESTS_FAIL"); sys.exit(0 if all(R) else 1)
