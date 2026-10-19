"""Runnable checks for GATES.md. python3 ugc/space-heater-ptc/qc/gates_check.py <name>   (prints '<name> PASS' or the reasons)."""
import json, re, subprocess, sys
from pathlib import Path
J = Path(__file__).resolve().parent.parent
HOOKS = {h["id"]: h["hook"] for h in json.loads((J / "../../grace/hooks/hooks.json").read_text())["hooks"]}
USED = {"V1": "H063", "V2": "H027", "V3": "H126"}

def sheets():
    e = [f"missing {f}" for f in ("refs/product_sheet.png", "refs/sheet_compare.jpg", "refs/ralph_sheet.jpg") if not (J / f).exists()]
    src = (J / "tools/make_sheet.py").read_text() if (J / "tools/make_sheet.py").exists() else ""
    if "refs/listing/" not in src: e.append("make_sheet.py does not build from refs/listing (real pixels)")
    return e

def rooms():
    src = (J / "rooms/SOURCES.md").read_text() if (J / "rooms/SOURCES.md").exists() else ""
    files = sorted(p.name for p in (J / "rooms").glob("V*_*.jpg"))
    e = [] if len(files) >= 8 else [f"only {len(files)} room plates"]
    e += [f"{f} has no source/licence line" for f in files if not re.search(re.escape(f) + r" \| V\d \| https://\S+ \| \S+", src)]
    return e

def scripts():
    e = []
    for v, hid in USED.items():
        t = (J / f"vo/{v}.txt").read_text().strip()
        hook = HOOKS[hid]; pre = hook.split("__")[0].strip()
        if not t.startswith(pre): e.append(f"{v} does not open with {hid} word for word: {pre!r}")
        if not t.endswith("It's in the orange cart."): e.append(f"{v} does not close with It's in the orange cart.")
    if len(set(USED.values())) != 3: e.append("hook id reused")
    return e

def shots():
    S = json.loads((J / "shots.json").read_text())["shots"]; e = []
    for v in ("V1", "V2", "V3"):
        vs = [s for s in S if s["video"] == v]; free = sum(s["kind"] == "HAND-FREE" for s in vs)
        if not all(s["kind"] in ("HAND", "HAND-FREE") for s in vs): e.append(f"{v}: unmarked shot")
        if not (len(vs) / 3 <= free <= len(vs) / 2): e.append(f"{v}: {free}/{len(vs)} hand-free, not a third to a half")
        if " ".join(s["line"] for s in vs) != (J / f"vo/{v}.txt").read_text().strip(): e.append(f"{v}: shot lines != vo/{v}.txt")
    for v in ("V1", "V2", "V3"):
        mine = {s["room"] for s in S if s["video"] == v}; other = {s["room"] for s in S if s["video"] != v}
        if mine & other: e.append(f"{v} shares rooms {mine & other}")
        if not all(r.split("/")[-1].startswith(v) for r in mine): e.append(f"{v} uses another video's plate")
    return e

def finals():
    e = []
    for v in ("V1",):   # Ralph 2026-10-19: V1 only
        f = J / f"out/heater_{v}.mp4"
        if not f.exists(): e.append(f"missing {f.name}"); continue
        p = json.loads(subprocess.run(["ffprobe", "-v", "quiet", "-print_format", "json", "-show_streams", str(f)], capture_output=True, text=True).stdout)
        vs = [s for s in p["streams"] if s["codec_type"] == "video"]; au = [s for s in p["streams"] if s["codec_type"] == "audio"]
        if not vs or vs[0]["width"] * 16 != vs[0]["height"] * 9: e.append(f"{v} not 9:16")
        if not au: e.append(f"{v} no audio")
        if not (J / f"out/heater_{v}.finish.json").exists(): e.append(f"{v} no AI-finish record")
    return e

if __name__ == "__main__":
    n = sys.argv[1]; errs = globals()[n]()
    print(f"{n} PASS" if not errs else f"{n} FAIL\n  " + "\n  ".join(errs))
