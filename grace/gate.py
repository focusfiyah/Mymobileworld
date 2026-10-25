"""Script gate (Ralph 2026-10-03, after FUSOU shipped without Humanizer): "everything means everything, I shouldn't have to ask".
Every paid runner (Kie stills/clips, ElevenLabs voice) calls require(job_dir) first. It refuses unless the job's checklist.json
proves EVERY step of grace/PLAYBOOK.md §4 was done, each with a real file in the job folder:

  python3 grace/gate.py <job_dir> --init        write a checklist.json to fill in
  python3 grace/gate.py <job_dir>               check before any paid call (stage "plan")
  python3 grace/gate.py <job_dir> --stage cut   check before a cut goes to Ralph (adds the coach compare)

Proof files must exist and be NEWER than the script file, so editing a script after a check forces that check again.
The VO lines are also scanned for Ralph's banned phrases and AI tells.

Paid calls also need (Ralph 2026-10-22, three ideas taken from Video Factory):
  1. Production Book: the plan message saved as JOB/BOOK.md (script, every shot, prompts, one TOTAL: $X line).
       python3 grace/gate.py <job> --book-init                       copy the template to fill in
       python3 grace/gate.py <job> --approve-book "<Ralph's words>"  record his OK against the book's exact text
     Editing BOOK.md after his OK voids it until he OKs the new version.
  2. Budget lock: spend on the job since that OK, tasks in flight included, never passes the book TOTAL plus extras
     he approved later:  python3 grace/gate.py <job> --approve-extra 0.32 "<Ralph's words>" --what "S3 redo"
  4. Prompt check (grace/prompt_check.py, Ralph 2026-10-25): every prompt is linted and must be marked checked for the
     job (read in full first) before start_task() lets it through.
  3. Paid-task ledger (grace/paid.py): runners call start_task(job, body, label=...) right before each Kie createTask
     and task_submitted(job, key, task_id) right after. A request already started or paid in this job, here or on any
     session branch, is refused until GATE_REDO names it.
A scripts-only job (no paid calls) only needs the script gate; the book shows as information.
"""
import datetime, hashlib, json, os, re, sys
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


def check_readability(job, c):
    """Per-video readability (Ralph 2026-10-15: V5 of night-driving-glasses v2 kept word for word). Each readability proof file
    is one video (readability_vN.txt). A video above grade 6 passes ONLY if an override names that video, its rule is
    readability, and the grade in the override equals the measured grade in its file. Without per-video files, max_grade applies."""
    rp = (c.get("readability") or {})
    files = [job / f for f in rp.get("proof", []) if (job / f).exists()]
    if not files or not all(re.search(r"readability_v\d+\.txt$", f.name) for f in files):
        rd = rp.get("max_grade")
        return [f"readability: max grade {rd} > 6"] if rd is not None and rd > 6 else []
    errs = []
    for f in files:
        m = re.search(r"Grade level \(Flesch-Kincaid\):\s*([\d.]+)", f.read_text(errors="ignore"))
        if not m: errs.append(f"readability: no grade in {f.name}"); continue
        grade, vid = float(m.group(1)), "V" + re.search(r"v(\d+)", f.name).group(1)
        if grade <= 6: continue
        ok = [o for o in overrides(c) if o.get("rule") == "readability" and vid in (o.get("videos") or [])
              and o.get("grade") is not None and abs(float(o["grade"]) - grade) < 0.05]
        if not ok: errs.append(f"readability: {vid} grade {grade} > 6 with no matching override")
    return errs


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
    if not (data / "comments.md").exists():
        errs.append("audience: research/audience/comments.md missing (`python3 grace/audience.py comments <job>` pulls TikTok comments of the researched videos)")
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
    errs += check_readability(job, c)
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
    if stage == "cut":   # NO text burned into videos unless Ralph asked (Ralph 2026-10-02/03, restated 2026-10-05)
        ok = (c.get("text_overlay_ok") or {}).get("quote")
        for f in sorted({*job.glob("*cut*.py"), *job.parent.glob("*cut*.py")}):
            for i, line in enumerate(f.read_text(errors="ignore").splitlines(), 1):
                s = line.strip()
                if s.startswith(("#", "from ", "import ")): continue
                if re.search(r"classic_png\(|drawtext=|subtitles=|ass=", s) and not ok:
                    errs.append(f"text overlay in {f.name}:{i}: no text in videos unless Ralph asks (add checklist text_overlay_ok with his words): {s[:90]}")
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


BOOK = "BOOK.md"
BOOK_HEADS = ["## 3. script", "## 4. shot list", "## 6. cost", "## 8. prompts"]
TEMPLATE = Path(__file__).resolve().parents[1] / ".claude/skills/ugc-product-ad/templates/plan-message.md"
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import paid   # noqa: E402  (grace/paid.py, next to this file)


def _checklist(job):
    p = Path(job) / "checklist.json"
    return json.loads(p.read_text()) if p.exists() else {}


def _sha(text):
    return hashlib.sha256(text.encode()).hexdigest()


def book_problems(job):
    """(problems with BOOK.md itself, its TOTAL, its text) before anyone can approve it."""
    f = Path(job) / BOOK
    if not f.exists():
        return [f"no Production Book: `python3 grace/gate.py {job} --book-init`, fill it, send it to Ralph as the plan"], None, ""
    text = f.read_text(); low = text.lower(); errs = []
    if re.search(r"_{3,}|\$__", text):
        errs.append(f"{BOOK} still has blanks (___ or $__): fill every field, 'n/a' needs a reason")
    errs += [f"{BOOK} is missing the section '{h}'" for h in BOOK_HEADS if h not in low]
    totals = re.findall(r"(?m)^TOTAL:\s*\$(\d+(?:\.\d+)?)\s*$", text)
    if len(totals) != 1:
        errs.append(f"{BOOK} needs exactly one line 'TOTAL: $<amount>' (the paid total Ralph approves), found {len(totals)}")
    return errs, (float(totals[0]) if len(totals) == 1 else None), text


def book_errors(job, c):
    errs, total, text = book_problems(job)
    ok = c.get("book_ok")
    if errs:
        return errs
    if not ok:
        return [f"{BOOK} is not approved: send it to Ralph, then `python3 grace/gate.py {job} --approve-book \"<his words>\"`"]
    if ok.get("sha256") != _sha(text):
        return [f"{BOOK} changed after Ralph approved it ({ok.get('date')}): send him the new version and record his OK again"]
    return []


def allowance(c):
    ok = c.get("book_ok") or {}
    extra = sum(float(x["usd"]) for x in c.get("budget_extra", []) if x.get("book_sha256") == ok.get("sha256"))
    return float(ok.get("total", 0)) + extra, extra


def lock_errors(job, c, spent_now, add):
    """Budget lock: spend since Ralph's OK (in flight included) + this call must fit the approved total + extras."""
    ok = c["book_ok"]; allowed, extra = allowance(c)
    since = round(spent_now - float(ok.get("spent_at_approval", 0)), 4)
    print(f"BOOK: approved ${ok['total']:.2f} + extras ${extra:.2f}; spent since approval ${since:.2f}; this call ${add:.2f};"
          f" left after it ${allowed - since - add:.2f}", file=sys.stderr)
    if since + add > allowed + 1e-6:
        return [f"this call (${add:.2f}) would take the job to ${since + add:.2f} of the ${allowed:.2f} Ralph approved. Ask him"
                f" with the exact cost, then `python3 grace/gate.py {job} --approve-extra <usd> \"<his words>\" --what \"<what>\"`"]
    return []


def approve_book(job, quote):
    errs, total, text = book_problems(job)
    if errs:
        sys.exit("cannot approve:\n  - " + "\n  - ".join(errs))
    p = Path(job) / "checklist.json"
    if not p.exists():
        sys.exit(f"no {p}: run --init first")
    c = json.loads(p.read_text())
    if c.get("book_ok"):
        c.setdefault("book_history", []).append(c["book_ok"])
    c["book_ok"] = {"by": "Ralph", "date": datetime.date.today().isoformat(), "quote": quote, "total": total,
                    "sha256": _sha(text), "spent_at_approval": paid.job_spend(paid.entries(job))}
    p.write_text(json.dumps(c, indent=1))
    print(f"BOOK APPROVED: ${total:.2f} (job had spent ${c['book_ok']['spent_at_approval']:.2f} before this book)")


def approve_extra(job, usd, quote, what):
    p = Path(job) / "checklist.json"; c = json.loads(p.read_text()) if p.exists() else {}
    if book_errors(job, c):
        sys.exit("approve the current BOOK.md first: " + "; ".join(book_errors(job, c)))
    c.setdefault("budget_extra", []).append({"usd": usd, "what": what, "by": "Ralph", "quote": quote,
                                            "date": datetime.date.today().isoformat(), "book_sha256": c["book_ok"]["sha256"]})
    p.write_text(json.dumps(c, indent=1))
    print(f"EXTRA APPROVED: +${usd:.2f} for {what}; job allowance now ${allowance(c)[0]:.2f}")


def require(job, stage="plan", usd=0.0, lock=True):
    errs = check(job, stage)
    # Monthly cap (Ralph 2026-10-21: "blowing through my budget"): every paid runner calls require(), so the cap
    # stops all of them at once. Cap and Ralph's over-cap OKs live in grace/spend.json.
    from spend import budget_errors
    errs = errs + budget_errors(job)
    c = _checklist(job); berrs = book_errors(job, c)   # Production Book + budget lock (Ralph 2026-10-22)
    if lock and not berrs:   # start_task() runs the lock itself, under the ledger lock
        errs += lock_errors(job, c, paid.job_spend(paid.entries(job)), usd)
    errs += berrs
    for l in override_lines(job): print(l, file=sys.stderr)
    if errs:
        sys.exit("SCRIPT GATE: paid call refused. Finish the checklist first (grace/PLAYBOOK.md §4):\n  - " + "\n  - ".join(errs[:25]))


def start_task(job, body, label="", usd=None):
    """Call right before each Kie createTask: input fields (grace/kie_fields.py), script gate, cap, book, budget lock
    (in-flight tasks counted) and the paid-task ledger. Returns the key for task_submitted()."""
    from spend import price
    from kie_fields import check as field_errors   # a misnamed input field is ignored by Kie, not refused
    errs = field_errors(body)
    if errs:
        sys.exit("KIE FIELDS: paid call refused, nothing sent:\n  - " + "\n  - ".join(errs))
    import prompt_check   # Ralph 2026-10-25: prompts linted and read in full before any paid call
    prompt_check.require(job, body)
    usd = price(body)[1] if usd is None else usd
    require(job, lock=False)
    return paid.claim(job, body, usd, label, check=lambda spent: lock_errors(job, _checklist(job), spent, usd))


def task_submitted(job, key, task_id):
    """Call right after createTask with Kie's taskId, or None when no task was created (nothing charged)."""
    paid.submitted(job, key, task_id)


def book_line(job):
    c = _checklist(job); errs = book_errors(job, c)
    if errs:
        return "BOOK: not ready for paid calls: " + errs[0]
    allowed, extra = allowance(c)
    return f"BOOK: approved by Ralph {c['book_ok']['date']}, ${allowed:.2f} allowed (book ${c['book_ok']['total']:.2f} + extras ${extra:.2f})"


if __name__ == "__main__":
    job = sys.argv[1]
    if "--init" in sys.argv: init(job)
    elif "--book-init" in sys.argv:
        dst = Path(job) / BOOK
        if dst.exists(): sys.exit(f"{dst} exists")
        dst.write_text(TEMPLATE.read_text()); print("wrote", dst)
    elif "--approve-book" in sys.argv: approve_book(job, sys.argv[sys.argv.index("--approve-book") + 1])
    elif "--approve-extra" in sys.argv:
        i = sys.argv.index("--approve-extra")
        if "--what" not in sys.argv: sys.exit("--what \"<what the extra pays for>\" is required")
        approve_extra(job, float(sys.argv[i + 1]), sys.argv[i + 2], sys.argv[sys.argv.index("--what") + 1])
    else:
        e = check(job, sys.argv[sys.argv.index("--stage") + 1] if "--stage" in sys.argv else "plan")
        print("GATE OK" if not e else "GATE FAILED:\n  - " + "\n  - ".join(e))
        for l in override_lines(job): print(l)
        print(book_line(job))
        sys.exit(1 if e else 0)
