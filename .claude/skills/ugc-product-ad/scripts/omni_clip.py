"""Product-lock clip: Google Gemini Omni reference-to-video through OpenMontage's gemini_omni_video tool
(Ralph 2026-10-21: "product lock on all products moving forward ... Google Omni to ensure product stay true to the original").

  python3 omni_clip.py JOB SHOT --prompt-file P.txt --first STILL.png --ref REAL1.png [--ref SHEET.png ...] \
      [--seconds 5] [--model gemini-omni-1.1-flash] [--dry]
  python3 omni_clip.py JOB SHOT --edit --prompt-file FIX.txt [--seconds 5]   # fix ONE detail of the last take

- JOB is the job folder (grace/gate.py require() runs first: script gate + monthly cap). --dry prints the cost and
  the request and spends nothing.
- Images are sent in order and bound by tag: --first is <IMAGE_REF_0> (the approved clean still; the prompt opens with
  "<FIRST_FRAME> <IMAGE_REF_0>" so it is the opening frame), each --ref is <IMAGE_REF_1>, <IMAGE_REF_2>, ... (real
  product photo close-ups, one per logo/label in frame, then the product reference sheet). Write the prompt with the
  prompt-master skill and name every tag (template: references/product-lock.md).
- --edit fixes one detail of the shot's last take with Omni's conversational edit (previous_interaction_id from
  omni_log.json): a short prompt naming only the change, ending "Keep everything else the same." Same price per
  second as a new take, but the rest of the shot stays as approved.
- Writes JOB/clips/SHOT.mp4 (audio stripped; Omni always renders audio) and appends JOB/omni_log.json
  {t, shot, model, seconds, usd, out}, which grace/spend.py counts.
- Price: about $0.10 per second at 720p, 3-10 s per clip, no free tier (ai.google.dev pricing, 2026-10). A redo is a
  new paid call: ask Ralph with the cost first.
"""
import argparse, datetime, json, os, subprocess, sys
from pathlib import Path

USD_PER_SEC = 0.1014


def find_up(start, rel):
    for p in [start, *start.parents]:
        if (p / rel).exists():
            return p / rel
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("job"); ap.add_argument("shot")
    ap.add_argument("--prompt-file", required=True)
    ap.add_argument("--first")
    ap.add_argument("--edit", action="store_true")
    ap.add_argument("--ref", action="append", default=[])
    ap.add_argument("--seconds", type=int, default=5)
    ap.add_argument("--model", default="gemini-omni-1.1-flash")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    job = Path(a.job).resolve()
    # resolve image paths now: the runner chdirs into OpenMontage before the call
    a.first = str(Path(a.first).resolve()) if a.first else None
    a.ref = [str(Path(r).resolve()) for r in a.ref]
    secs = max(3, min(10, a.seconds)); usd = round(USD_PER_SEC * secs, 3)
    prompt = Path(a.prompt_file).read_text().strip()
    log = job / "omni_log.json"; entries = json.loads(log.read_text()) if log.exists() else []
    prev = None
    if a.edit:
        takes = [e for e in entries if e.get("shot") == a.shot and e.get("ok") and e.get("interaction_id")]
        if not takes:
            sys.exit(f"--edit: no earlier take of {a.shot} with an interaction_id in {log}")
        prev = takes[-1]["interaction_id"]
        if "Keep everything else the same" not in prompt:
            sys.exit("--edit prompt must end with 'Keep everything else the same.'")
    else:
        if not a.first:
            sys.exit("--first STILL is required for a new take")
        for tag in ["<FIRST_FRAME>"] + [f"<IMAGE_REF_{i}>" for i in range(1 + len(a.ref))]:
            if tag not in prompt:
                sys.exit(f"prompt does not name {tag}: every image must be bound by its tag (references/product-lock.md)")
    print(f"{a.shot}: {a.model} {'edit of ' + prev if prev else 'new take'} {secs}s 720p 9:16 -> ${usd}")
    if a.dry:
        print(prompt); return
    gate = find_up(job, "grace/gate.py")
    if not gate:
        sys.exit("grace/gate.py not found above the job folder")
    sys.path.insert(0, str(gate.parent)); from gate import require; require(job)
    om = Path(os.environ.get("OPENMONTAGE", "")) if os.environ.get("OPENMONTAGE") else find_up(job, "OpenMontage") \
        or Path("/home/user/OpenMontage")
    sys.path.insert(0, str(om)); os.chdir(om)
    from tools.tool_registry import registry
    registry.discover(); tool = registry._tools["gemini_omni_video"]
    (job / "clips").mkdir(exist_ok=True)
    raw = job / "clips" / f"{a.shot}_omni_{len([e for e in entries if e.get('shot') == a.shot])}.mp4"
    req = {"prompt": prompt, "aspect_ratio": "9:16", "duration": str(secs), "model": a.model, "output_path": str(raw)}
    if prev:
        req.update(operation="edit_video", previous_interaction_id=prev)
    else:
        req.update(operation="reference_to_video",
                   reference_image_paths=[str(Path(a.first).resolve())] + [str(Path(r).resolve()) for r in a.ref])
    res = tool.execute(req)
    data = res.data if isinstance(getattr(res, "data", None), dict) else {}
    entries.append({"t": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "shot": a.shot, "model": a.model,
                    "interaction_id": data.get("interaction_id"), "edit_of": prev,
                    "seconds": secs, "usd": usd if res.success else 0.0, "ok": bool(res.success),
                    "error": None if res.success else str(res.error)[:300], "out": str(raw)})
    log.write_text(json.dumps(entries, indent=1))
    if not res.success:
        sys.exit(f"Omni failed (not billed for output): {res.error}")
    out = job / "clips" / f"{a.shot}.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", str(raw), "-an", "-c:v", "copy", str(out)], check=True)
    print(f"OK {out} (${usd}); QC the product at 2x on several frames before it goes anywhere")


if __name__ == "__main__":
    main()
