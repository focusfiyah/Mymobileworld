"""Pointer to the one script gate, grace/gate.py in focusfiyah/Mymobileworld (Ralph 2026-10-22). This file used to
be a copy that had drifted, so the runners here that do `from gate import require` skipped the monthly cap. Now they
get every check: script gate, cap, approved Production Book, budget lock, and start_task()/task_submitted() for the
paid-task ledger. `python3 scripts/gate.py <job> [--init|--book-init|--approve-book ...]` runs the real CLI.
"""
import importlib.util, os, runpy, sys
from pathlib import Path


def _find():
    for start in (os.environ.get("UGC_JOB"), os.getcwd(), __file__):
        if start:
            for p in [Path(start).resolve(), *Path(start).resolve().parents]:
                if (p / "grace" / "gate.py").is_file():
                    return p / "grace" / "gate.py"
    sys.exit("SCRIPT GATE: grace/gate.py not found (run inside the Mymobileworld repo); paid call refused")


_real = _find()
sys.path.insert(0, str(_real.parent))
if __name__ == "__main__":
    runpy.run_path(str(_real), run_name="__main__")
else:
    _spec = importlib.util.spec_from_file_location("grace_gate", _real)
    _mod = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(_mod)
    globals().update({k: v for k, v in vars(_mod).items() if not k.startswith("__")})
