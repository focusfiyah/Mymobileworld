"""Gate oracle: python3 distinct.py -> DISTINCT_OK when V1 and V2 use no overlapping moment of the same source clip."""
import importlib.util, sys
s = importlib.util.spec_from_file_location("c", "cut.py"); c = importlib.util.module_from_spec(s); s.loader.exec_module(c)
a, b = c.PLANS["v1"]["segs"], c.PLANS["v2"]["segs"]
ov = [(x[:3], y[:3]) for x in a for y in b if x[0] == y[0] and min(x[2], y[2]) - max(x[1], y[1]) > 0]
print("DISTINCT_OK" if not ov else f"OVERLAP {ov}"); sys.exit(1 if ov else 0)
