"""Gate checks for the Swyii agate necklace scripts job. Usage: python3 qc/verify.py <check>"""
import json, re, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parents[1]; R = J.parents[1]
spoken = sorted((J / "spoken").glob("s*.txt"))
_h = json.load(open(R / "grace/hooks/hooks.json")); hooks = {h["id"]: h["hook"] for h in (_h["hooks"] if isinstance(_h, dict) else _h)}
def fail(m): print("FAIL", m); sys.exit(1)
c = sys.argv[1]
if c == "scripts":
    if len(spoken) < 3: fail(f"{len(spoken)} spoken scripts")
    ids = []
    for f in spoken:
        t = f.read_text(); m = re.search(r"^# hook (H\d{3})", t, re.M)
        if not m: fail(f"{f.name}: no hook id"); ids.append(m.group(1))
        body = re.sub(r"^#.*$", "", t, flags=re.M).strip()
        if not body.startswith(hooks[m.group(1)].split("__")[0].strip().rstrip(".?")): fail(f"{f.name}: hook not word for word")
        if not body.rstrip().endswith("It's in the orange cart."): fail(f"{f.name}: close")
        n = len(body.split())
        if not 60 <= n <= 100: fail(f"{f.name}: {n} words")
    if len(set(ids)) != len(ids): fail("hook id reused")
    print("SCRIPTS_OK", len(spoken))
elif c == "banned":
    bad = [r"reviewer", r"label says", r"\$\s?\d", r"\b\d+\s?(dollars|bucks)\b", r"order (it )?now", r"\bsale\b", r"% off", r"[–—]",
           r"\bheal(s|ing)?\b", r"\benergy\b", r"\bsterling\b", r"\bpendant\b", r"\bobsessed\b", r"game.?changer"]
    for f in spoken + [J / "scripts.md"]:
        t = f.read_text().lower() if f.name != "scripts.md" else re.split(r"(?im)^## (what's in|notes)", f.read_text())[0].lower()
        for b in bad:
            if re.search(b, t): fail(f"{f.name}: '{b}'")
    print("BANNED_OK")
elif c == "readability":
    T = R / ".claude/skills/tiktok-shop-coach/scripts/tiktok.py"; out = []
    for f in spoken:
        body = "\n".join(l for l in f.read_text().splitlines() if not l.startswith("#"))
        r = subprocess.run([sys.executable, str(T), "readability", body], capture_output=True, text=True).stdout
        g = float(re.search(r"Grade level \(Flesch-Kincaid\):\s*([\d.]+)", r).group(1)); out.append(g)
        if g > 6: fail(f"{f.name} grade {g}")
    print("READABILITY_OK", out)
elif c == "gate":
    r = subprocess.run([sys.executable, str(R / "grace/gate.py"), str(J)], capture_output=True, text=True)
    print(r.stdout[-600:], r.stderr[-300:])
    if r.returncode == 0: print("GATE_OK")
    else: sys.exit(1)
elif c == "readme":
    t = (J / "README.md").read_text()
    if "drive.google.com/drive/folders/" not in t or "claude.ai/" not in t or "Status:" not in t: fail("README missing link/status")
    if "swyii" not in (R / "CLAUDE.md").read_text().lower(): fail("CLAUDE.md jobs line")
    print("README_OK")
elif c == "cues":
    h = re.findall(r'class="cue">([^<]*)', (J / "doc/swyii_scripts.html").read_text())
    m = [x.strip("[]") for x in re.findall(r"\[\d:\d\d[^\]]*\]", (J / "scripts.md").read_text())]
    if h != m: fail(f"html {len(h)} cues vs md {len(m)}")
    print("CUES_MATCH", len(m))
