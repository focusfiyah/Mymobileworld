"""Run tools/hookcheck/hook_check.py on all five batch-C cuts, with each cut's own hook box (out/<name>_plan.json).
Prints HOOKS_ALL_OK 5 when every one prints HOOK_OK."""
import json, subprocess
from pathlib import Path
HERE = Path(__file__).resolve().parent
POSTS = {"bf-purcell": "bf_purcell", "bf-jiyu-nad": "bf_jiyu_nad", "bf-luvum": "bf_luvum", "bf-momo-nashi": "bf_momo_nashi", "bf-manners": "bf_manners"}
ok = 0
for d, n in POSTS.items():
    p = HERE.parent / d
    try:
        box = ",".join(map(str, json.loads((p / f"out/{n}_plan.json").read_text())["hook_box"]))
        r = subprocess.run(["python3", str(HERE.parents[2] / "tools/hookcheck/hook_check.py"), str(p / f"out/{n}.mp4"), "--hook", box, "--hold", "2.0"],
                           capture_output=True, text=True).stdout
    except Exception as e:
        r = f"ERROR {e}"
    good = "HOOK_OK" in r; ok += good
    print(n, "HOOK_OK" if good else r.strip()[-200:])
print(f"HOOKS_ALL_OK {ok}" if ok == len(POSTS) else f"HOOKS_FAIL {ok}/{len(POSTS)}")
