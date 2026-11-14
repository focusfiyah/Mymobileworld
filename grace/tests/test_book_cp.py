"""Creator Pathway plan lines in BOOK.md (Ralph 2026-11-14 weekly audit): jobs created from 2026-11-14 need
'Product open: product-first|trust-first' and 'Product screen: ...'; older jobs are untouched.

  python3 grace/tests/test_book_cp.py   -> "BOOK_CP_TESTS_OK (n)" or the first failure
"""
import json, os, sys, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
os.environ.setdefault("SPEND_OFFLINE", "1")
import gate  # noqa: E402

BASE = ("Sent to Ralph: https://example 2026-11-14\n## 3. Script\nx\n## 4. Shot list\nx\n## 6. Cost\nx\nTOTAL: $1.00\n"
        "## 8. Prompts\nx\n")
n = 0
def check(name, cond):
    global n
    if not cond:
        sys.exit(f"FAIL {name}")
    n += 1

def run(created, extra=""):
    d = Path(tempfile.mkdtemp())
    (d / "checklist.json").write_text(json.dumps({"created": created}))
    (d / "BOOK.md").write_text(BASE + extra)
    errs, total, _ = gate.book_problems(str(d))
    return errs, total

e, t = run("2026-11-13")
check("old job not asked for the new lines", not any("Product open" in x or "Product screen" in x for x in e))
e, _ = run("2026-11-14")
check("new job missing both lines -> 2 errors", sum(("Product open" in x) or ("Product screen" in x) for x in e) == 2)
e, _ = run("2026-11-14", "Product open: trust-first (supplement)\nProduct screen: 4.6 stars, $19, 20k sold, high pain, free\n")
check("new job with both lines passes", not any("Product open" in x or "Product screen" in x for x in e))
e, _ = run("2026-11-14", "Product open: maybe\nProduct screen: 4.6 stars\n")
check("bad product-open value refused", any("Product open" in x for x in e))
check("total still parsed", t == 1.0)
print(f"BOOK_CP_TESTS_OK ({n})")
