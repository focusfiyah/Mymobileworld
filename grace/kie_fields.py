"""Kie input-field check (Ralph 2026-10-24, lead from github.com/Autom8AI/Open-Higgsfield-AI's data/models.json).
Kie accepts a createTask whose input has a misnamed field and silently ignores it: nano-banana-pro and nano-banana-2
take reference images as `image_input`, nano-banana-2-lite as `image_urls`, hailuo as `image_url`, Seedance 2.0 Mini as
`first_frame_url` / `reference_image_urls`. A wrong name means the model never sees the product photo and we pay for a
still or clip of the wrong product. grace/gate.py start_task() calls check() on every body before it is submitted.

  python3 grace/kie_fields.py build    re-read every page in DOCS from docs.kie.ai and rewrite grace/kie_fields.json
  python3 grace/kie_fields.py audit    run check() over every request our job logs hold (all must pass)

A model missing from kie_fields.json is let through: add its doc page to DOCS and run build when a runner starts using it.
"""
import datetime, glob, json, os, re, sys, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TABLE = os.path.join(ROOT, "grace", "kie_fields.json")
DOCS = [   # docs.kie.ai pages (OpenAPI spec inside), one per model we use or have priced
    "market/google/pro-image-to-image", "market/google/nanobanana2", "market/google/nano-banana-2-lite",
    "market/bytedance/seedance-2-mini", "market/google/gemini-omni-flash-1-1", "market/kling/v3-omni-image-to-video",
    "market/hailuo/2-3-image-to-video-standard", "veo3-api/generate-veo-3-video", "market/volcengine/video-to-video-lip-sync",
    "market/kling/ai-avatar-standard", "market/kling/ai-avatar-pro", "market/omnihuman-1-5", "market/omnihuman-2-0",
    "market/infinitalk/from-audio", "market/wan/2-2-a14b-speech-to-video-turbo",
]


def _fields(spec):
    """{model: sorted input field names} from one doc page's OpenAPI spec (input may be a oneOf of variants)."""
    out = {}
    for op in (spec.get("paths") or {}).values():
        schema = (((op.get("post") or {}).get("requestBody") or {}).get("content") or {}).get("application/json", {}).get("schema", {})
        props = schema.get("properties") or {}
        inp = props.get("input") or {}
        names = set((inp.get("properties") or {}).keys())
        for variant in inp.get("oneOf") or inp.get("anyOf") or []:
            names |= set((variant.get("properties") or {}).keys())
        if not inp:   # flat endpoints (veo3) put the inputs beside "model"
            names = set(props) - {"model", "callBackUrl"}
        m = props.get("model") or {}
        for model in m.get("enum") or [m.get("default")]:
            if model and names:
                out[model] = sorted(names)
    return out


def build():
    import yaml
    models = {}
    for page in DOCS:
        url = f"https://docs.kie.ai/{page}.md"
        text = urllib.request.urlopen(url, timeout=30).read().decode()
        block = re.search(r"```yaml\n(.*?)```", text, re.S)
        if not block:
            sys.exit(f"no OpenAPI spec in {url}")
        for model, names in _fields(yaml.safe_load(block.group(1))).items():
            models[model] = {"fields": names, "doc": url}
    json.dump({"built": datetime.date.today().isoformat(), "models": models}, open(TABLE, "w"), indent=1)
    print(f"wrote {TABLE}: {len(models)} models")


def check(body):
    """Errors for input fields the model's Kie doc does not list (Kie ignores them without an error)."""
    try:
        models = json.load(open(TABLE))["models"]
    except (OSError, ValueError):
        return []
    spec = models.get(body.get("model"))
    if not spec:
        return []
    extra = sorted(set((body.get("input") or {}).keys()) - set(spec["fields"]))
    if not extra:
        return []
    return [f"{body['model']} has no input field {', '.join(extra)}; Kie would ignore it silently. "
            f"Its fields: {', '.join(spec['fields'])} ({spec['doc']})"]


def audit():
    bad = n = 0
    files = glob.glob(os.path.join(ROOT, "ugc/**/*_log.json"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "fungix/**/*_log.json"), recursive=True) + \
        glob.glob(os.path.join(ROOT, "ugc/**/paid_tasks.json"), recursive=True)
    for f in files:
        try:
            d = json.load(open(f))
        except (OSError, ValueError):
            continue
        items = d if isinstance(d, list) else (d.get("tasks") or d.get("entries") or list(d.values()))
        for e in items:
            r = (e.get("request") or e.get("body")) if isinstance(e, dict) else None
            if isinstance(r, dict) and r.get("model"):
                n += 1
                for err in check(r):
                    bad += 1
                    print(os.path.relpath(f, ROOT), err)
    print(f"AUDIT {n} requests, {bad} with unknown fields")
    return bad


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "build":
        build()
    elif cmd == "audit":
        sys.exit(1 if audit() else 0)
    else:
        sys.exit(__doc__)
