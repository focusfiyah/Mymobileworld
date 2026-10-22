"""G3: the runners new jobs copy save each paid task before createTask and record its taskId after."""
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
bad = []
for f in ["ugc/youtheory-collagen/kie.py", ".claude/skills/ugc-product-ad/scripts/omni_clip.py"]:
    s = (ROOT / f).read_text()
    start, create = s.find("start_task("), s.find("/createTask")
    if not (0 <= start < create) or len(re.findall(r"task_submitted\(", s)) < 2:
        bad.append(f)
print("WIRED OK" if not bad else f"NOT WIRED: {bad}")
