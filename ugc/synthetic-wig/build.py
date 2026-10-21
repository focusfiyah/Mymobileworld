#!/usr/bin/env python3
"""Build scripts.md + spoken/vN.txt from scripts.json (one source for the doc, the VO lines and the checks)."""
import json
from pathlib import Path

WPS = 3.0   # Grace's VO pace (PLAYBOOK §5: 3.0-3.6 words/s; Grace C reads ~3.0-3.2)
J = Path(__file__).parent
d = json.loads((J / "scripts.json").read_text())
(J / "spoken").mkdir(exist_ok=True)


def sec(a, b):
    return f"{a:.1f}-{b:.1f} s"


out = [f"# Synthetic wig voiceover scripts (Grace), {d['product']}", "",
       f"Footage: {d['footage']}. Grace reads the VOICEOVER lines; the shot map says which part of her clip plays under each line.",
       "Hooks are from Grace's hook library, said word for word. V1 is the main script; V2 and V3 are extra posts.", ""]
for v in d["videos"]:
    words = sum(len(l["text"].split()) for l in v["lines"])
    out += [f"## {v['id']}: {v['title']} (hook {v['hook_id']}, {words} words, about {round(words / WPS)} s)", ""]
    for l in v["lines"]:
        shots = " + ".join(sec(a, b) for a, b in l["shots"])
        out.append(f"- **{l['beat']}** [{shots}] {l['text']}")
        if l.get("live_option"):
            out.append(f"  - Option: {l['live_option']}")
    out += ["", "Alternate hooks (film or record each, same body):"]
    out += [f"- {h['id']}: {h['text']}" for h in v["alt_hooks"]]
    out += ["", "On-screen text (only if Ralph says yes): " + " / ".join(v["text_options"]),
            "", f"Caption: {v['caption']}", "", f"Edit note: {v['edit_note']}", ""]
    (J / "spoken" / f"{v['id'].lower()}.txt").write_text("\n".join(l["text"] for l in v["lines"]) + "\n")
(J / "scripts.md").write_text("\n".join(out))
print("built", len(d["videos"]), "scripts")
