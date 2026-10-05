"""Script gate (Ralph 2026-10-03, after FUSOU shipped without Humanizer): "everything means everything, I shouldn't have to ask".
Every paid runner (Kie stills/clips, ElevenLabs voice) calls require(job_dir) first. It refuses unless the job's checklist.json
proves EVERY step of grace/PLAYBOOK.md §4 was done, each with a real file in the job folder:

  python3 grace/gate.py <job_dir> --init        write a checklist.json to fill in
  python3 grace/gate.py <job_dir>               check before any paid call (stage "plan")
  python3 grace/gate.py <job_dir> --stage cut   check before a cut goes to Ralph (adds the coach compare)

Proof files must exist and be NEWER than the script file, so editing a script after a check forces that check again.
The VO lines are also scanned for Ralph's banned phrases and AI tells.
"""
import json, os, re, sys
from pathlib import Path

STEPS = {   # key: what proof it needs (PLAYBOOK §4 "Every script uses ALL of these" + script checklist + CTA rules)
    "playbook":        "grace/PLAYBOOK.md read this job; list the rules applied (house rules, structure, CTA, hooks, pacing)",
    "coach_research":  "tiktok-shop-coach output files: discover/tag/shop on the product keyword AND `video` on the top 3 shop videos",
    "viral_board":     "tiktok.py viral output (viral-<date>.json) for the product's category, from this job",
    "product_facts":   "file with every claim and its source (listing, box, brand site)",
    "hooks":           "file with 3 hook options per video: spoken line AND on-screen text, each modeled on a named winner",
    "humanizer":       "Humanizer report on the FINAL script + captions (tells found, what changed)",
    "readability":     "tiktok.py readability output for each script (grade must be <= 6)",
    "audience":        "research/audience.md from `grace/audience.py` data + verbatim voice-of-customer quotes: Who, Pain point experience, Communication style, What it means for the script (Ralph 2026-10-05)",
    "line_sources":    "file showing the source of every script line (coach data / playbook / psychology / research)",
}
CUT_STEPS = {"compare": "tiktok.py compare <top winner> <our cut> output, after the final cut, and what was fixed"}
BANNED = [r"\border (it )?now\b", r"\bheads up\b", r"\bgame[- ]changer\b", r"\bobsessed\b", r"\byou need this\b", r"\bselling out\b",
          r"\bends tonight\b", r"\bmiracle\b", r"\bso cute\b", r"[–—]", r" -- "]


AUDIENCE_HEADS = ["## who", "## pain point experience", "## communication style", "## what it means for the script"]
PROOF_FIRST = ("playbook", "coach_research", "viral_board", "product_facts", "audience")   # research that comes BEFORE the script: not required to be newer than it


def norm(t):
    return re.sub(r"\s+", " ", t.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')).lower()


def check_audience(job, c):
    """Ralph 2026-10-05: find the target audience, their pain-point experience and the best way to talk to them, from
    AnswerThePublic-style data (grace/audience.py) and real quotes. The audience.md must have the 4 headings and >=5 quoted
    phrases (> "...") that really appear in the job's research/audience/ data, so it cannot be written from imagination."""
    if c.get("audience_legacy"): return []   # jobs finished before 2026-10-05: required only if their script is rewritten
    errs, a = [], c.get("audience") or {}
    proof = a.get("proof") or []
    md = [p for p in proof if p.endswith("audience.md")]
    if not md: return ["audience: proof must include research/audience.md (see grace/audience.py)"]
    f = job / md[0]
    if not f.exists(): return [f"audience: {md[0]} not found"]
    text = f.read_text(errors="ignore"); low = text.lower()
    for h in AUDIENCE_HEADS:
        if h not in low: errs.append(f"audience: {md[0]} is missing the heading '{h}'")
    data = job / "research" / "audience"
    if not (data / "raw.json").exists() or not (data / "questions.md").exists():
        errs.append("audience: research/audience/raw.json + questions.md missing (run `python3 grace/audience.py <job> \"<seed>\" ...`)")
        return errs
    pool = norm("".join(p.read_text(errors="ignore") for p in data.iterdir() if p.suffix in (".json", ".md", ".txt")))
    evidence = re.split(r"(?im)^## what it means", text)[0]   # quotes of OUR script lines in the last section are not evidence
    quotes = re.findall(r'"([^"\n]{12,})"', evidence)
    ok = [q for q in quotes if norm(q).rstrip(".!?,… ") in pool]
    bad = [q for q in quotes if q not in ok and len(q.split()) >= 5]
    if len(ok) < 5: errs.append(f"audience: only {len(ok)} quoted phrases found in research/audience/ data (need >= 5 real ones)")
    for q in bad[:5]: errs.append(f"audience: quote not found in the data (invented or altered?): \"{q[:70]}\"")
    if not (data / "voc.md").exists(): errs.append("audience: research/audience/voc.md (verbatim voice-of-customer quotes with URLs) missing")
    return errs


def init(job):
    p = Path(job) / "checklist.json"
    if p.exists(): sys.exit(f"{p} exists")
    p.write_text(json.dumps({"scripts": ["scripts.md"], "vo_lines": "files holding the exact spoken lines (e.g. vo/*_lines.json)",
                             **{k: {"proof": [], "note": v} for k, v in {**STEPS, **CUT_STEPS}.items()}}, indent=1))
    print("wrote", p)


def check(job, stage="plan"):
    job = Path(job); p = job / "checklist.json"
    if not p.exists(): return [f"no {p}: run `python3 grace/gate.py {job} --init` and do every step"]
    c = json.loads(p.read_text()); errs = []
    scripts = [job / s for s in c.get("scripts", [])]
    newest = max([s.stat().st_mtime for s in scripts if s.exists()] or [0])
    for s in scripts:
        if not s.exists(): errs.append(f"script file missing: {s}")
    for k, why in {**STEPS, **(CUT_STEPS if stage == "cut" else {})}.items():
        if k == "audience" and c.get("audience_legacy"): continue
        proof = (c.get(k) or {}).get("proof") or []
        if not proof: errs.append(f"{k}: no proof. Needs: {why}"); continue
        for f in proof:
            fp = job / f
            if not fp.exists(): errs.append(f"{k}: proof file not found: {f}")
            elif k not in PROOF_FIRST and fp.stat().st_mtime < newest:
                errs.append(f"{k}: {f} is older than the script: redo {k} on the current script")
    errs += check_audience(job, c)
    rd = (c.get("readability") or {}).get("max_grade")
    if rd is not None and rd > 6: errs.append(f"readability: max grade {rd} > 6")
    for o in overrides(c):   # a recorded exception covers ONLY the rule + videos it names; everything else still applies
        for f in ("rule", "videos", "by", "date", "quote", "grade"):
            if not o.get(f): errs.append(f"override missing '{f}': {o}")
        if o.get("rule") != "readability": errs.append(f"override for rule {o.get('rule')!r} not supported (only readability)")
    text = ""
    for g in [c.get("vo_lines")] if isinstance(c.get("vo_lines"), str) else c.get("vo_lines", []):
        for f in sorted(job.glob(g)): text += f.read_text(errors="ignore") + "\n"
    for s in scripts:
        if s.exists(): text += s.read_text(errors="ignore")
    for pat in BANNED:
        for m in re.finditer(pat, text, re.I):
            ctx = text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ")
            errs.append(f"banned/AI phrase {pat!r}: ...{ctx}...")
    return errs


def overrides(c):
    """Owner-approved exceptions (Ralph, 2026-10-03: a client's own script that fails readability, used verbatim).
    Each needs rule, videos, by, date, the owner's quoted words and the real measured grade. They are always printed."""
    return c.get("overrides") or []


def override_lines(job):
    p = Path(job) / "checklist.json"
    if not p.exists(): return []
    return [f"OVERRIDE (readability, video {o.get('videos')}, grade {o.get('grade')}): {o.get('by')} {o.get('date')}: \"{o.get('quote')}\""
            for o in overrides(json.loads(p.read_text()))]


def require(job, stage="plan"):
    errs = check(job, stage)
    for l in override_lines(job): print(l, file=sys.stderr)
    if errs:
        sys.exit("SCRIPT GATE: paid call refused. Finish the checklist first (grace/PLAYBOOK.md §4):\n  - " + "\n  - ".join(errs[:25]))


if __name__ == "__main__":
    job = sys.argv[1]
    if "--init" in sys.argv: init(job)
    else:
        e = check(job, sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "plan")
        print("GATE OK" if not e else "GATE FAILED:\n  - " + "\n  - ".join(e))
        for l in override_lines(job): print(l)
        sys.exit(1 if e else 0)
