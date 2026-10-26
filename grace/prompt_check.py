"""Prompt check before every paid generation (Ralph 2026-10-25, OQQ pants: "Make it a standard to double check your prompts
before putting them through, so to not have to keep redoing and spending credits"). Two stills on that job came back wrong
because shared prompt blocks fought the shot ("frame cuts at her chest" in a knees-down shot, a back-logo reference in a
front shot, "toes point the same way as her body" on a side view), and one Gemini still had the shoes on backwards.

grace/gate.py start_task() calls require() on every Kie body, so nothing is paid for until:
  1. lint(): the prompt passes the mechanical checks below, and
  2. the exact prompt text was read in full and marked checked for this job (JOB/proof/prompts_checked.json).
A refused prompt is saved to JOB/proof/pending_prompts/<hash>.txt; read it end to end against the shot (framing, which
way the toes point in frame terms, every "image N" names the right reference, nothing from another shot), fix the
prompt, then mark it:

  python3 grace/prompt_check.py lint <file.txt | shots.json> [--refs N]   lint only (free), prints PROMPT_LINT_OK
  python3 grace/prompt_check.py mark <job> <file.txt | shots.json ...>    lint + record each prompt as checked
  shots.json files: every string under "still", "clip" or "prompt" is a prompt; "still_refs" / "clip_refs" give N.

Product truth (Ralph 2026-10-26, Youtheory B12B6: "Yes make standing rule"): the real product photos always win. A detail
from research, another creator's video or a listing render goes into a product prompt only after it is checked against the
real photos. Every job from 2026-10-26 on has JOB/product_truth.json, written from the real photos BEFORE the first prompt:
  {"photos": ["refs/real/front.jpg", ...],            real photos the facts come from (must exist)
   "facts": ["flat magenta tear-off tab on top", ...], what the photos show (for the plan and the reader)
   "forbid": ["screw cap", "spout", ...]}              details the real product does NOT have
mark() and require() refuse a prompt that describes a forbidden detail (a mention inside a negation, "no spout", is fine).
Why: the B12B6 stills were sent with "screw cap twisted off" taken from a research note while Grace's photos showed a
tear-off top; all 9 came back with a spout ($0.81 redo).
"""
import datetime, hashlib, json, re, sys
from pathlib import Path

EFFECT = r"\b(sparkl\w*|glint\w*|glitter\w*|shimmer\w*|lens flare|light streak\w*|bokeh)\b"
NEG = r"\b(no|not|never|without|nor)\b"
FEET = r"\b(shoe|shoes|sneaker|sneakers|feet|foot|boots?|heels?)\b"
TOE_DIR = r"\btoes?\b[^.]{0,80}\b(point|face|faces|facing|aim)|\btoes?(?: caps?)? (?:to|at|toward|towards|away)\b"
FRAME_TOP = r"(frame (?:cuts|starts|begins) at (?:her|his) (\w+)|nothing above (?:her|his) (\w+))"


TRUTH_FROM = "2026-10-26"   # jobs dated on/after this need product_truth.json


def truth(job):
    """(truth dict or None, problems). Required for jobs whose checklist.json date is on/after TRUTH_FROM."""
    j = Path(job); f = j / "product_truth.json"
    if not f.exists():
        c = j / "checklist.json"
        date = json.loads(c.read_text()).get("date", "") if c.exists() else ""
        if date and date >= TRUTH_FROM:
            return None, [f"no {f}: write it from the real product photos first (photos, facts, forbid), Ralph 2026-10-26"]
        return None, []
    d = json.loads(f.read_text()); errs = []
    if not d.get("photos"):
        errs.append(f"{f.name}: list the real photos the facts come from")
    errs += [f"{f.name}: photo {x} does not exist" for x in d.get("photos", []) if not (j / x).exists()]
    return d, errs


def truth_errors(prompt, d):
    """A forbidden product detail described in the prompt (not inside a negation)."""
    errs, low = [], prompt.lower()
    for term in (d or {}).get("forbid", []):
        for m in re.finditer(r"\b" + re.escape(term.lower()) + r"\b", low):
            clause = re.split(r"[.;:()]", low[max(0, m.start() - 80):m.start()])[-1]
            if not re.search(NEG, clause):
                errs.append(f"describes '{term}', which the real product photos do not show (product_truth.json)"); break
    return errs


def _hash(text):
    return hashlib.sha256(text.strip().encode()).hexdigest()


def lint(prompt, n_images=None):
    """Mechanical checks; returns a list of problems (empty = pass)."""
    errs, low = [], prompt.lower()
    refs = [int(x) for x in re.findall(r"\b(?:reference )?images? (\d+)", low)]
    if n_images is not None:
        over = sorted({r for r in refs if r > n_images or r < 1})
        if over:
            errs.append(f"names image {over} but only {n_images} image(s) are sent")
        defined = [int(x) for x in re.findall(r"\bimage (\d+) (?:=|is)\b", low)]
        if defined and len(set(defined)) != len(defined):
            errs.append("an image number is defined twice")
    for m in re.finditer(EFFECT, low):
        before = low[max(0, m.start() - 60):m.start()]
        if not re.search(NEG, before.split(".")[-1]):
            errs.append(f"light-effect word '{m.group(0)}' (the model adds it as an effect)")
    if re.search(FEET, low) and re.search(r"\b(her|his|she|he)\b", low) and not re.search(TOE_DIR, low) \
            and not re.search(r"feet (?:\w+ )?out of (?:the )?frame", low):
        errs.append("shoes/feet on a person but no toe direction (say where the toes point in frame terms)")
    tops = {a or b for _, a, b in re.findall(FRAME_TOP, low)}
    if len(tops) > 1:
        errs.append(f"framing conflict: the frame top is set at {sorted(tops)}")
    if "no text" not in low and "no captions" not in low:
        errs.append("no 'no text' line (models add captions and labels)")
    return errs


def prompts_in(path):
    """[(label, prompt, n_images or None)] from a .txt (one prompt) or a shots.json."""
    p = Path(path)
    if p.suffix != ".json":
        return [(p.name, p.read_text(), None)]
    data = json.loads(p.read_text())
    items = data.get("shots", data) if isinstance(data, dict) else data
    items = items.items() if isinstance(items, dict) else [(x.get("id", i), x) for i, x in enumerate(items)]
    out = []
    for sid, s in items:
        for k, refs in (("still", "still_refs"), ("clip", "clip_refs"), ("prompt", "refs")):
            if isinstance(s, dict) and isinstance(s.get(k), str):
                out.append((f"{sid}.{k}", s[k], len(s[refs]) if isinstance(s.get(refs), list) else None))
    return out


def _store(job):
    return Path(job) / "proof" / "prompts_checked.json"


def mark(job, items):
    """Lint each (label, prompt, n) and record the clean ones as checked. Returns the problems found."""
    f = _store(job); f.parent.mkdir(parents=True, exist_ok=True)
    done = json.loads(f.read_text()) if f.exists() else {}
    d, problems = truth(job)
    if problems:
        return problems
    for label, text, n in items:
        e = lint(text, n) + truth_errors(text, d)
        if e:
            problems += [f"{label}: {x}" for x in e]
            continue
        done[_hash(text)] = {"label": str(label), "checked": datetime.datetime.now().isoformat(timespec="seconds"), "chars": len(text.strip())}
    f.write_text(json.dumps(done, indent=1))
    return problems


def _body_prompts(body):
    inp = body.get("input") or body
    imgs = None
    for k in ("image_input", "image_urls", "reference_image_urls", "input_urls", "imageUrls"):
        if isinstance(inp.get(k), list):
            imgs = (imgs or 0) + len(inp[k])
    for k in ("first_frame_url", "image_url", "last_frame_url"):
        if inp.get(k):
            imgs = (imgs or 0) + 1
    return [(k, inp[k], imgs) for k in ("prompt", "negative_prompt") if isinstance(inp.get(k), str) and k == "prompt"]


def require(job, body):
    """Refuse (sys.exit) a paid body whose prompt fails lint or was not marked checked for this job."""
    done = json.loads(_store(job).read_text()) if _store(job).exists() else {}
    d, terr = truth(job)
    for k, text, n in _body_prompts(body):
        e = terr + lint(text, n) + truth_errors(text, d)
        if e or _hash(text) not in done:
            pend = Path(job) / "proof" / "pending_prompts" / f"{_hash(text)[:12]}.txt"
            pend.parent.mkdir(parents=True, exist_ok=True); pend.write_text(text)
            why = ("lint: " + "; ".join(e)) if e else "not marked checked yet"
            sys.exit(f"PROMPT CHECK: paid call refused, nothing sent ({why}).\n  Read {pend} end to end against the shot, fix it, then:\n"
                     f"  python3 grace/prompt_check.py mark {job} <the prompt file or shots.json>")


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or a[0] not in ("lint", "mark"):
        sys.exit(__doc__)
    if a[0] == "lint":
        n = int(a[a.index("--refs") + 1]) if "--refs" in a else None
        items = [it for f in a[1:] if not f.startswith("--") and not f.isdigit() for it in prompts_in(f)]
        probs = [f"{lbl}: {x}" for lbl, t, m in items for x in lint(t, n if n is not None else m)]
        print("PROMPT_LINT_OK" if not probs else "PROMPT LINT FAILED:\n  - " + "\n  - ".join(probs))
    else:
        job, files = a[1], a[2:]
        probs = mark(job, [it for f in files for it in prompts_in(f)])
        print("MARKED_OK" if not probs else "NOT MARKED (fix these first):\n  - " + "\n  - ".join(probs))
