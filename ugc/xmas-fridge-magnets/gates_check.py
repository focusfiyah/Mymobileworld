"""Checks for GATES.md (Christmas Fridge Magnets)."""
import re, subprocess, sys
what = sys.argv[1]
if what == "book":
    t = open("BOOK.md").read()
    assert re.search(r"Sent to Ralph: https://claude\.ai/code/artifact/\S+", t)
    assert len(re.findall(r"(?m)^TOTAL: \$\d", t)) == 1
    print("BOOK_FIELDS_OK")
elif what == "spend":
    o = subprocess.run(["python3", "grace/spend.py"], capture_output=True, text=True, cwd="../..").stdout
    v = float(re.search(r"ugc/xmas-fridge-magnets\s+\$\s*([0-9.]+)", o).group(1))
    assert v <= 4.66, v
    print("SPEND_OK", v)
