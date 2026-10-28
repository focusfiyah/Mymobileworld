#!/usr/bin/env python3
"""Gate checks for grace/winners (GATES.md). Usage: python3 grace/winners/check.py <fields|intake|export|patterns|versions|proofs>"""
import csv, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "grace"))
REQ = ["product", "url", "sales", "views", "faceless", "format", "hook", "hook_id", "hook_type", "pain_point",
       "problem_solved", "why_converted", "script", "onscreen_text"]
SEED = {"7696231728855223582", "7696285070046301470", "7696617399759555871", "7696627904985304351",
        "7697844264050511135", "7685441537894780190",
        "7699252578239925535", "7700400913759980831"}


def db():
    return json.load(open(os.path.join(HERE, "winners.json")))["videos"]


def fail(msg):
    print("FAIL", msg); sys.exit(1)


def fields():
    vs = db()
    if {v["id"] for v in vs} != SEED:
        fail(f"ids differ from the 6 seeded links: {sorted(v['id'] for v in vs)}")
    for v in vs:
        miss = [k for k in REQ if v.get(k) in (None, "")]
        if miss:
            fail(f"{v['id']} missing {miss}")
    print("PASS fields", len(vs))


def intake():
    """Pull one seeded link into a throwaway copy of the db and check the auto fields came from TikTok today."""
    from datetime import date
    tmp = tempfile.mkdtemp()
    env = dict(os.environ, WINNERS_OUT=tmp)
    code = ("import sys,json,os;sys.argv=['w'];sys.path.insert(0,%r);import winners as w;"
            "w.DB=os.path.join(%r,'db.json');v=w.pull('https://www.tiktok.com/t/ZPLARHa8G/',%r,sales=1);"
            "print('ROW',json.dumps(v))") % (HERE, tmp, tmp)
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, env=env, timeout=300)
    m = re.search(r"^ROW (.*)$", r.stdout, re.M)
    if not m:
        fail("pull failed: " + (r.stdout + r.stderr)[-600:])
    v = json.loads(m.group(1))
    ok = (v["id"] == "7696617399759555871" and "SoFyre" in v["product"] and v["views"] > 0 and len(v["script"]) > 100
          and v["pulled"] == date.today().isoformat() and v["posted"] == "2026-10-14" and v["caption"])
    if not ok:
        fail(f"unexpected row: {v['product']!r} views={v['views']} posted={v['posted']}")
    print("PASS intake")


def export():
    vs = db()
    rows = list(csv.DictReader(open(os.path.join(HERE, "winners.csv"))))
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(HERE, "winners.xlsx")).active
    if len(rows) != len(vs) or ws.max_row - 1 != len(vs):
        fail(f"rows csv={len(rows)} xlsx={ws.max_row - 1} json={len(vs)}")
    for v, r in zip(vs, rows):
        if r["Link to video"] != v["url"] or r["Product"] != v["product"] or int(r["Sales"]) != v["sales"]:
            fail(f"row mismatch {v['id']}")
    print("PASS export")


def patterns():
    t = open(os.path.join(HERE, "PATTERNS.md")).read()
    for key in ["Tiger Eye", "Night driving", "Throw Hands", "BodyJ", "SoFyre", "Mute"]:
        if key.lower() not in t.lower():
            fail(f"PATTERNS.md misses {key}")
    sec = t.split("## Shared patterns", 1)[1].split("\n## ", 1)[0]
    n = len(re.findall(r"^\d+\. ", sec, re.M))
    if n < 5:
        fail(f"only {n} patterns")
    print("PASS patterns", n)


def versions():
    """Ralph 2026-10-20: Grace's looser wording. Each version names a library hook as its base, but does not read it word for word."""
    import gate
    hooks = {h["id"]: h["hook"] for h in json.load(open(os.path.join(REPO, "grace/hooks/hooks.json")))["hooks"]}
    t = open(os.path.join(HERE, "VERSIONS.md")).read()
    if "Check with Ralph" in t:
        fail("open 'Check with Ralph' note left")
    blocks = re.split(r"^### ", t, flags=re.M)[1:]
    S = os.path.join(REPO, ".claude/skills/tiktok-shop-coach/scripts/tiktok.py")
    per, used = {}, set()
    for b in blocks:
        name = b.split(":", 1)[0].strip()
        m = re.search(r"^- Hook base: (H\d{3})", b, re.M)
        if not m or m.group(1) not in hooks:
            fail(f"{name}: no library hook base")
        hid = m.group(1)
        lines = [l[2:].strip() for l in b.splitlines() if l.startswith("> ")]
        script = " ".join(lines)
        rx = r"\s*.+?\s*".join(re.escape(p.strip()) for p in hooks[hid].split("__")) + r"[.?!]"
        if re.match(rx, lines[0]):
            fail(f"{name}: opens with {hid} word for word; Ralph asked for Grace's looser wording")
        if "orange cart" not in lines[-1].lower():
            fail(f"{name}: close is {lines[-1]!r}")
        for p in gate.BANNED + [r"\$\s?\d", r"\b\d+(\.\d+)? ?(dollars|bucks)\b", r"\breviewers?\b", r"label says", r"\border\b"]:
            if re.search(p, script, re.I):
                fail(f"{name}: banned {p!r}")
        r = subprocess.run([sys.executable, S, "readability", script], capture_output=True, text=True)
        g = re.search(r"Flesch-Kincaid\):\s*(-?[\d.]+)", r.stdout)
        if not g or float(g.group(1)) > 6:
            fail(f"{name}: readability {g.group(1) if g else r.stdout[:200]}")
        prod = name.split("-")[0]
        if (prod, hid) in used:
            fail(f"{name}: hook {hid} used twice for {prod}")
        used.add((prod, hid))
        per[prod] = per.get(prod, 0) + 1
    if len(per) != 6 or any(n != 2 for n in per.values()):
        fail(f"per product {per}")
    print("PASS versions", sum(per.values()))


def promoted():
    ads = {"7696231728855223582", "7696285070046301470", "7696617399759555871", "7697844264050511135",
           "7699252578239925535", "7700400913759980831"}
    for v in db():
        want = "Yes, by the brand (TikTok ad label)" if v["id"] in ads else "No"
        if v.get("promoted") != want:
            fail(f"{v['id']} promoted={v.get('promoted')!r}")
    print("PASS promoted")


def proofs():
    for f in ["research/humanizer.md", "research/viral-2026-10-20.txt", "research/readability.txt"]:
        p = os.path.join(HERE, f)
        if not os.path.exists(p) or os.path.getsize(p) < 200:
            fail(f"missing proof {f}")
    if "shop videos posted" not in open(os.path.join(HERE, "research/viral-2026-10-20.txt")).read():
        fail("viral board file has no board")
    if os.path.getmtime(os.path.join(HERE, "research/humanizer.md")) < os.path.getmtime(os.path.join(HERE, "VERSIONS.md")) - 1:
        fail("humanizer proof older than VERSIONS.md")
    print("PASS proofs")


def style():
    t = open(os.path.join(HERE, "STYLE_pritech.md")).read()
    rows = re.findall(r"^\| (\d+) \| [\d.]+-[\d.]+ \|", t, re.M)
    if [int(r) for r in rows] != list(range(1, 15)):
        fail(f"shot map rows {rows}")
    for k in ["ZPLAonsjU", "ZPLAEVuMv", "Black Friday", "NOT made yet", "S2", "S6", "don't want to mix"]:
        if k not in t:
            fail(f"STYLE_pritech.md misses {k}")
    print("PASS style", len(rows))


def playbook():
    t = open(os.path.join(REPO, "grace/PLAYBOOK.md")).read()
    if "grace/winners/STYLE_pritech.md" not in t or "never mix her" not in t:
        fail("PLAYBOOK has no pointer to STYLE_pritech.md")
    print("PASS playbook")


if __name__ == "__main__":
    globals()[sys.argv[1]]()
