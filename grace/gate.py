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
    "line_sources":    "file showing the source of every script line (coach data / playbook / psychology / research)",
}
CUT_STEPS = {"compare": "tiktok.py compare <top winner> <our cut> output, after the final cut, and what was fixed"}
BANNED = [r"\border (it )?now\b", r"\bheads up\b", r"\bgame[- ]changer\b", r"\bobsessed\b", r"\byou need this\b", r"\bselling out\b",
          r"\bends tonight\b", r"\bmiracle\b", r"\bso cute\b", r"[–—]", r" -- "]


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
        proof = (c.get(k) or {}).get("proof") or []
        if not proof: errs.append(f"{k}: no proof. Needs: {why}"); continue
        for f in proof:
            fp = job / f
            if not fp.exists(): errs.append(f"{k}: proof file not found: {f}")
            elif k not in ("playbook", "coach_research", "viral_board", "product_facts") and fp.stat().st_mtime < newest:
                errs.append(f"{k}: {f} is older than the script: redo {k} on the current script")
    rd = (c.get("readability") or {}).get("max_grade")
    if rd is not None and rd > 6: errs.append(f"readability: max grade {rd} > 6")
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


def require(job, stage="plan"):
    errs = check(job, stage)
    if errs:
        sys.exit("SCRIPT GATE: paid call refused. Finish the checklist first (grace/PLAYBOOK.md §4):\n  - " + "\n  - ".join(errs[:25]))


if __name__ == "__main__":
    job = sys.argv[1]
    if "--init" in sys.argv: init(job)
    else:
        e = check(job, sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "plan")
        print("GATE OK" if not e else "GATE FAILED:\n  - " + "\n  - ".join(e)); sys.exit(1 if e else 0)
