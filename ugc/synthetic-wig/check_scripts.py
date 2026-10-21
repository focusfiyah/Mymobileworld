#!/usr/bin/env python3
"""Checks for GATES.md: python3 check_scripts.py beats|scripts|grades"""
import json, re, subprocess, sys
from pathlib import Path

J = Path(__file__).resolve().parent
ROOT = J.parents[1]
CLIP = 59.2
WPS = 3.0
d = json.loads((J / "scripts.json").read_text())
lib = {h["id"]: h["hook"] for h in json.loads((ROOT / "grace/hooks/hooks.json").read_text())["hooks"]}
errs = []


def fills(template, text):
    """True if text is the library template word for word with only the __ blanks filled."""
    pat = "^" + r"\s+".join(re.escape(w) if w != "__" else r".+?" for w in template.replace("__", " __ ").split()) + r"[.?!]?$"
    return re.match(pat, text.strip()) is not None


def beats():
    t = (J / "footage/beats.md").read_text()
    rows = re.findall(r"^\| ([\d.]+) \| ([\d.]+) \|", t, re.M)
    if len(rows) < 10: errs.append(f"only {len(rows)} beat rows")
    if rows and float(rows[-1][1]) < 58: errs.append("beats stop before the clip ends")
    for (a, b), (c, _) in zip(rows, rows[1:]):
        if abs(float(b) - float(c)) > 0.01: errs.append(f"gap/overlap at {b} vs {c}")
    return "beats"


def scripts():
    used = []
    for v in d["videos"]:
        vid, lines = v["id"], v["lines"]
        hook = lines[0]["text"]
        if lib.get(v["hook_id"]) != v["hook_template"]: errs.append(f"{vid}: hook_template differs from library {v['hook_id']}")
        if not fills(lib.get(v["hook_id"], "?"), hook): errs.append(f"{vid}: hook not word for word: {hook}")
        for h in v["alt_hooks"]:
            if lib.get(h["id"]) != h["template"] or not fills(h["template"], h["text"]): errs.append(f"{vid}: alt {h['id']} not word for word")
        used += [v["hook_id"]] + [h["id"] for h in v["alt_hooks"]]
        if lines[-1]["text"].split(". ")[-1] != "It's in the orange cart.": errs.append(f"{vid}: does not end with It's in the orange cart.")
        words = sum(len(l["text"].split()) for l in lines)
        if not 70 <= words <= 95: errs.append(f"{vid}: {words} words (want 70-95)")
        text = " ".join(l["text"] for l in lines) + " " + v["caption"]
        for pat in [r"\$", r"\bdollars?\b", r"\bprice\b", r"\breviewers?\b", r"label says", r"\d", r"order (it )?now", r"[–—]", r"selling out", r"tangle"]:
            if re.search(pat, " ".join(l["text"] for l in lines) if pat == r"\d" else text, re.I): errs.append(f"{vid}: banned pattern {pat}")
        shot_len = 0
        for l in lines:
            for a, b in l["shots"]:
                if not (0 <= a < b <= CLIP): errs.append(f"{vid}: shot {a}-{b} outside the clip")
                shot_len += b - a
        vo = words / WPS
        if abs(shot_len - vo) > 0.15 * vo: errs.append(f"{vid}: shots {shot_len:.1f}s vs VO ~{vo:.1f}s")
        print(f"{vid}: {words} words, VO ~{vo:.1f}s, shots {shot_len:.1f}s, hook {v['hook_id']}")
    dup = {i for i in used if used.count(i) > 1}
    if dup: errs.append(f"hook ids reused: {dup}")
    return "scripts"


def grades():
    coach = ROOT / ".claude/skills/tiktok-shop-coach/scripts/tiktok.py"
    for v in d["videos"]:
        f = J / f"readability_{v['id'].lower()}.txt"
        spoken = (J / "spoken" / f"{v['id'].lower()}.txt").read_text()
        out = subprocess.run([sys.executable, str(coach), "readability", spoken], capture_output=True, text=True).stdout
        f.write_text(out)
        m = re.search(r"Grade level \(Flesch-Kincaid\):\s*([\d.]+)", out)
        g = float(m.group(1)) if m else 99
        print(f"{v['id']}: grade {g}")
        if g > 6: errs.append(f"{v['id']}: grade {g} > 6")
    return "grades"


def load_beats():
    rows = re.findall(r"^\| ([\d.]+) \| ([\d.]+) \| [^|]+\| (\w+) \| ([^|]+)\|", (J / "footage/beats.md").read_text(), re.M)
    return [(float(a), float(b), m, {x.strip() for x in tags.split(",")}) for a, b, m, tags in rows]


def visuals():
    """Every shot under a line must show what the line names: >=60% of the shot overlaps beats carrying its tag
    (line 'shows' = one tag per shot when the counts match, else any of the tags for every shot; 'any' = no visual claim).
    Also reports how much of each video's picture shows her talking mouth under the voiceover."""
    bt = load_beats()
    def overlap(a, b, pred):
        return sum(max(0, min(b, y) - max(a, x)) for x, y, m, tg in bt if pred(m, tg))
    for v in d["videos"]:
        total = mouth = 0
        for l in v["lines"]:
            tags = l.get("shows", "")
            if not tags: errs.append(f"{v['id']}: line without 'shows': {l['text'][:40]}"); continue
            want = tags.split("|")
            for i, (a, b) in enumerate(l["shots"]):
                total += b - a; mouth += overlap(a, b, lambda m, tg: m == "visible")
                if tags == "any": continue
                need = [want[i]] if len(want) == len(l["shots"]) else want
                got = overlap(a, b, lambda m, tg: bool(tg & set(need)))
                if got < 0.6 * (b - a): errs.append(f"{v['id']}: '{l['text'][:45]}' shot {a}-{b} does not show {need} ({got:.1f}/{b - a:.1f}s)")
        print(f"{v['id']}: talking mouth on screen {mouth:.1f}s of {total:.1f}s ({100 * mouth / total:.0f}%)")
    return "visuals"


name = {"visuals": visuals, "beats": beats, "scripts": scripts, "grades": grades}[sys.argv[1]]()
print(f"{name} OK" if not errs else "FAILED:\n  " + "\n  ".join(errs))
sys.exit(1 if errs else 0)
