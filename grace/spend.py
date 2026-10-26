"""Month-to-date spend vs Ralph's monthly cap (Ralph 2026-10-21: "spending close to a $100/month Higgsfield
subscription; funds are not coming in faster than I'm spending").

  python3 grace/spend.py                 # this month, all jobs
  python3 grace/spend.py --month 2026-10 # another month
  python3 grace/spend.py --job ugc/vans-sequin   # one job's total

Kie: every submitted task in ugc/**/kie_log.json and fungix/**/kie_log.json (an entry with a taskId), priced from
what Kie billed for it (grace/billed.py, cached in grace/billed.json; Ralph 2026-10-26), else PRICES below (Kie's
list price, 1 credit = $0.005). A task logged only as "submitted" (its run died) still counts at its billed figure. Anything paid outside Kie (Gemini API, fal.ai, Kling credits, ElevenLabs top-ups) goes in
grace/spend.json "other" by hand: {"date": "2026-10-21", "what": "...", "usd": 0.80}.
Every plan and every redo question shows this script's line: "month so far $X of $CAP, this job +$Y".
"""
import argparse, datetime, glob, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import billed

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# USD per call or per second, from the job runners' own notes (kie.py docstrings, modeltest/RESULTS.md)
PRICES = {
    "nano-banana-pro": ("call", 0.09),
    "gpt-image-2-text-to-image": ("call", 0.05),            # 2K; 1K $0.03, 4K $0.08 (kie.ai/gpt-image-2, 2026-10-26)
    "bytedance/seedance-2-mini": ("sec", 0.041),
    "kling-3.0-omni/image-to-video": ("sec", 0.07),
    "volcengine/video-to-video-lip-sync": ("call", 0.24),   # $0.04/s of audio, clips ~6 s
    "veo-3-1": ("call", 0.30),                             # veo3_fast 60 credits
    "hailuo/2-3-image-to-video-standard": ("call", 0.15),  # estimate, not in any runner note
    "google/gemini-omni-flash-1-1": ("call", 0.315),        # 4 s take (runners that log their own "usd" are counted from it)
    # Portrait + voice -> talking video, per second of audio (kie.ai/pricing 2026-10-24; highest tier where it varies).
    # These have no "duration" input, so their runners pass usd=<audio seconds> x rate to start_task().
    "kling/ai-avatar-standard": ("sec", 0.04),               # 720p
    "kling/ai-avatar-pro": ("sec", 0.08),                    # 1080p
    "omnihuman-1-5": ("sec", 0.135),
    "omnihuman-2-0": ("sec", 0.07),                          # 720p
    "infinitalk/from-audio": ("sec", 0.06),                  # 720p; 480p is $0.015
    "wan/2-2-a14b-speech-to-video-turbo": ("sec", 0.12),     # 720p; 580p $0.09, 480p $0.06
}


def price(request):
    """List price of one Kie request body (used by grace/paid.py before the task is submitted)."""
    model = request.get("model"); kind, usd = PRICES.get(model, ("call", 0.10))
    if kind == "sec":
        return model, usd * float((request.get("input") or {}).get("duration") or 5)
    return model, usd


def kie_cost(entry, billed_cache=None):
    """(model, usd) of one finished log entry: what Kie billed when grace/billed.json has it (Ralph 2026-10-26),
    else the list price."""
    r = entry.get("request") or {}
    if not isinstance(r, dict) or not entry.get("taskId"):
        return None, 0.0
    b = billed.usd(entry["taskId"], billed_cache)
    if b is not None:
        return r.get("model"), b
    if entry.get("fail"):   # Kie does not charge failed tasks
        return None, 0.0
    return price(r)


def entry_usd(e, billed_cache=None):
    """Charge of one finished log entry: Kie's billed figure, else the runner's own "usd", else the list price."""
    if e.get("taskId"):
        b = billed.usd(e["taskId"], billed_cache)
        if b is not None:
            return b
    if "usd" in e and e.get("taskId"):
        return 0.0 if e.get("fail") else float(e["usd"])
    return kie_cost(e)[1]


def month_totals(month, job_prefix=None):
    """(per-job Kie dict, other usd) for a month. Each Kie task counts once, at what Kie billed when known
    (grace/billed.json), including tasks only logged as "submitted" (the run died before the result was logged)."""
    cfg = json.load(open(os.path.join(ROOT, "grace/spend.json")))
    bc = billed.load()
    jobs, seen, orphans = {}, set(), {}
    logs = glob.glob(os.path.join(ROOT, "ugc/**/kie_log.json"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "fungix/**/kie_log.json"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "ugc/**/omni_log.json"), recursive=True)
    for f in logs:
        job = os.path.relpath(os.path.dirname(f), ROOT)
        if job_prefix and not job.startswith(job_prefix.rstrip("/")):
            continue
        try:
            entries = json.load(open(f))
        except ValueError:
            continue
        for e in entries if isinstance(entries, list) else []:
            if not str(e.get("t", "")).startswith(month):
                continue
            if isinstance(e.get("submitted"), str):
                orphans.setdefault(e["submitted"], job); continue
            tid = e.get("taskId")
            if tid and tid in seen:
                continue
            if tid:
                seen.add(tid)
            if tid and billed.usd(tid, bc) is not None:
                jobs[job] = jobs.get(job, 0.0) + billed.usd(tid, bc); continue
            if "usd" in e:          # omni_log.json entries carry their own price
                jobs[job] = jobs.get(job, 0.0) + float(e["usd"]); continue
            model, usd = kie_cost(e, bc)
            if model:
                jobs[job] = jobs.get(job, 0.0) + usd
    for tid, job in orphans.items():   # paid, but the run never logged the result
        if tid not in seen and billed.usd(tid, bc):
            jobs[job] = jobs.get(job, 0.0) + billed.usd(tid, bc)
    other = 0.0 if job_prefix else sum(o["usd"] for o in cfg.get("other", []) if o["date"].startswith(month))
    return jobs, other, cfg


def cap_for(month, cfg):
    """The month's cap in USD, or None for no cap (caps_by_month overrides monthly_cap_usd)."""
    caps = cfg.get("caps_by_month", {})
    return caps[month] if month in caps else cfg["monthly_cap_usd"]


def budget_errors(job_dir):
    """Called by grace/gate.py require(): refuse paid calls once the month is at the cap, unless Ralph's OK for this
    job and month is recorded in grace/spend.json over_cap_ok (his words, like checklist overrides)."""
    month = datetime.date.today().strftime("%Y-%m")
    billed.refresh(limit_s=30, quiet=True)   # new tasks only; list prices stand in if Kie can't be reached
    jobs, other, cfg = month_totals(month)
    total, cap = sum(jobs.values()) + other, cap_for(month, cfg)
    job = os.path.relpath(os.path.abspath(job_dir), ROOT)
    capt = "no cap" if cap is None else f"cap ${cap:.2f}"
    print(f"BUDGET: month {month} so far ${total:.2f} ({capt}); this job ${jobs.get(job, 0.0):.2f}", file=sys.stderr)
    if cap is None or not cfg.get("enforce", True) or total < cap:
        return []
    ok = [o for o in cfg.get("over_cap_ok", []) if o.get("month") == month and job.startswith(o.get("job", "?"))
          and o.get("ralph")]
    return [] if ok else [f"monthly cap reached (${total:.2f} of ${cap:.2f}): ask Ralph with the exact cost and record his"
                          f" words in grace/spend.json over_cap_ok {{\"month\": \"{month}\", \"job\": \"{job}\", \"ralph\": \"...\"}}"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--month", default=datetime.date.today().strftime("%Y-%m"))
    ap.add_argument("--job")
    ap.add_argument("--offline", action="store_true", help="don't fetch new billed figures from Kie")
    a = ap.parse_args()
    if not a.offline:
        billed.refresh(limit_s=60, quiet=True)
    jobs, other, cfg = month_totals(a.month, a.job)
    kie = sum(jobs.values()); total = kie + other; cap = cap_for(a.month, cfg)
    for job, usd in sorted(jobs.items(), key=lambda x: -x[1])[:12]:
        print(f"  {job:45s} ${usd:6.2f}")
    if cap is None:
        print(f"KIE ${kie:.2f}  OTHER ${other:.2f}  MONTH {a.month} TOTAL ${total:.2f} (no cap this month)")
    else:
        print(f"KIE ${kie:.2f}  OTHER ${other:.2f}  MONTH {a.month} TOTAL ${total:.2f} of cap ${cap:.2f}"
              f" ({'OVER' if total > cap else 'left $%.2f' % (cap - total)})")
    print(f"(Kie: what Kie billed for {len(billed.load())} cached tasks, list price for any not cached yet; grace/billed.py)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
