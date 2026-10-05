"""Builds HOOKS.md from hooks.json. Run after adding a batch: python3 grace/hooks/build.py"""
import json, pathlib, collections
here = pathlib.Path(__file__).parent
data = json.loads((here / "hooks.json").read_text())
by_type = collections.OrderedDict()
for h in data["hooks"]:
    by_type.setdefault(h["type"], []).append(h)
out = ["# Grace hook library", "",
       "Fill-in-the-blank hook templates for Grace's videos. Source of truth: `hooks.json` (edit there, then run",
       "`python3 grace/hooks/build.py`). Batches: " + ", ".join(f"{b['id']} rows {b['rows']} ({b['count']} hooks, {b['date']})" for b in data["batches"]) + ".", "",
       "## How to use (every Grace job)",
       *[f"- {r}" for r in data["rules"]], "",
       "## Pick by category", ""]
cats = collections.defaultdict(list)
for h in data["hooks"]:
    for c in h["best_for"]:
        cats[c].append(h["id"])
for c in sorted(cats):
    out.append(f"- **{c}:** {', '.join(cats[c])}")
out.append("")
for t, hs in by_type.items():
    out += [f"## {t}", ""]
    for h in hs:
        out += [f"**{h['id']}. \"{h['hook']}\"**", f"- Use when: {h['use_when']}",
                f"- Best for: {', '.join(h['best_for'])}", f"- Note: {h['note']}"]
        if h.get("grace_caution"): out.append(f"- Grace note: {h['grace_caution']}")
        if h.get("used_in"): out.append(f"- Used in: {', '.join(h['used_in'])}")
        out.append("")
(here / "HOOKS.md").write_text("\n".join(out))
print(len(data["hooks"]), "hooks,", len(by_type), "types")
