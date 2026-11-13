#!/usr/bin/env python3
"""Gate checks for the 5 selling-video scripts job (Grace, 2026-11-13).

  python3 check.py scripts   each product's scripts.md: a VO script + a talk-to-camera script, each ending
                             "It's in the orange cart.", no banned phrase, no price number, no "label says"/"reviewer",
                             hook id named and the library hook said word for word (blanks filled) -> SCRIPTS_OK
  python3 check.py gates     grace/gate.py prints GATE OK for all 5 jobs -> ALL_GATES_OK
  python3 check.py selftest  the scripts check fails on a known-bad sample -> SELFTEST_OK
"""
import json, re, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
JOBS = ["haiti-flag", "ili-case", "meat-sticks", "bobbi-prep-duo", "mock-neck-sweatshirt"]
HOOKS = {h["id"]: h for h in json.loads((ROOT / "grace/hooks/hooks.json").read_text())["hooks"]} \
    if isinstance(json.loads((ROOT / "grace/hooks/hooks.json").read_text()), dict) else \
    {h["id"]: h for h in json.loads((ROOT / "grace/hooks/hooks.json").read_text())}
BANNED = [r"\border (it )?now\b", r"\bheads up\b", r"\bgame[- ]changer\b", r"\bobsessed\b", r"\byou need this\b",
          r"\bselling out\b", r"\bends tonight\b", r"\bmiracle\b", r"\bso cute\b", r"[–—]", r" -- ",
          r"\blabel says\b", r"\breviewers?\b", r"\$\s?\d", r"\b\d+\s?(dollars|bucks|percent|%)", r"% off",
          r"\bon sale\b", r"\bplenty to share\b", r"\bone is enough\b"]


def norm(t):
    t = t.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", t).strip().lower()


def hook_ok(hook_text, hid):
    h = HOOKS.get(hid)
    if not h:
        return f"hook id {hid} not in hooks.json"
    tpl = norm(h.get("hook") or h.get("text") or h.get("template") or "")
    parts = [re.escape(p.strip(" .?!,")) for p in re.split(r"_{2,}", tpl)]
    pat = r".+?".join(parts)
    if not re.search(pat, norm(hook_text).strip(" .?!,") + "", re.S):
        return f"hook not word for word with {hid}: template '{tpl}' vs '{hook_text}'"
    return None


def parse(md):
    """Each script is a '## ' section with **HOOK** (H###) "..." and a **SCRIPT** "..." block of the full spoken lines."""
    out = []
    for sec in re.split(r"\n(?=## )", md):
        if not sec.startswith("## ") or "**SCRIPT**" not in sec:
            continue
        title = sec.splitlines()[0][3:]
        hm = re.search(r"\*\*HOOK\*\*\s*\((H\d{3})\)\s*\"(.+?)\"", sec)
        sm = re.search(r"\*\*SCRIPT\*\*\s*\"(.+?)\"\s*$", sec, re.S | re.M)
        out.append((title, hm.group(1) if hm else None, hm.group(2) if hm else None, sm.group(1) if sm else None))
    return out


def check_md(md, name):
    errs, scripts = [], parse(md)
    kinds = [t.lower() for t, *_ in scripts]
    if not any("voiceover" in k for k in kinds): errs.append(f"{name}: no Voiceover script")
    if not any("camera" in k for k in kinds): errs.append(f"{name}: no Talk-to-camera script")
    for title, hid, htxt, body in scripts:
        if not hid: errs.append(f"{name}/{title}: no **HOOK** (H###) \"...\" line"); continue
        if not body: errs.append(f"{name}/{title}: no **SCRIPT** \"...\" block"); continue
        e = hook_ok(htxt, hid)
        if e: errs.append(f"{name}/{title}: {e}")
        if not norm(body).startswith(norm(htxt)[:25]): errs.append(f"{name}/{title}: script does not open with the hook")
        if not norm(body).endswith("it's in the orange cart."): errs.append(f"{name}/{title}: does not end \"It's in the orange cart.\"")
        for b in BANNED:
            if re.search(b, body, re.I): errs.append(f"{name}/{title}: banned pattern {b}")
    return errs


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scripts"
    if cmd == "scripts":
        errs = []
        for j in JOBS:
            p = HERE / j / "scripts.md"
            errs += check_md(p.read_text(), j) if p.exists() else [f"{j}: no scripts.md"]
        print("\n".join(errs) if errs else "SCRIPTS_OK"); sys.exit(1 if errs else 0)
    if cmd == "gates":
        bad = []
        for j in JOBS:
            r = subprocess.run([sys.executable, str(ROOT / "grace/gate.py"), str(HERE / j)], capture_output=True, text=True, cwd=ROOT)
            if "GATE OK" not in r.stdout: bad.append(f"{j}: {r.stdout.strip()[:600]}")
        print("\n".join(bad) if bad else "ALL_GATES_OK"); sys.exit(1 if bad else 0)
    if cmd == "selftest":
        bad = '## Voiceover\n**HOOK** (H999) "Hi"\n**SCRIPT** "Hi. Order it now for $20."\n'
        print("SELFTEST_OK" if check_md(bad, "bad") else "SELFTEST_FAILED"); return
    sys.exit("unknown command")


if __name__ == "__main__":
    main()
