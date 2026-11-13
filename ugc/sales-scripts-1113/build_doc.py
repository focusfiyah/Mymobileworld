#!/usr/bin/env python3
"""Build the Google Doc HTML for one product: scripts.md + the research verdict (Grace gets both in one doc)."""
import html, re, sys
from pathlib import Path
EMOJI = re.compile("[\U0001F000-\U0001FAFF☀-➿️‍\U0001F1E6-\U0001F1FF]")
def clean(t): return html.escape(re.sub(r"\s{2,}", " ", EMOJI.sub("", t)).strip())
def build(job, name):
    md = (Path(job) / "scripts.md").read_text()
    out = [f"<h1>Scripts - {html.escape(name)}</h1>", "<p><i>Made 2026-11-13 from your video that sold. Two scripts: one voiceover (no face needed) and one to say on camera. No prices, ends in the orange cart. On-screen text is optional.</i></p>"]
    for sec in re.split(r"\n(?=## )", md):
        if not sec.startswith("## "): continue
        title = sec.splitlines()[0][3:].strip()
        out.append(f"<h2>{html.escape(title)}</h2>")
        for line in sec.splitlines()[1:]:
            if not line.strip(): continue
            m = re.match(r"\*\*HOOK\*\*\s*\((H\d+)\)\s*\"(.+)\"", line)
            if m: out.append(f"<p><b>Hook:</b> {clean(m.group(2))} <span style='color:#888'>({m.group(1)})</span></p>"); continue
            m = re.match(r"\*\*SCRIPT\*\*\s*\"(.+)\"", line)
            if m: out.append(f"<p><b>Script:</b></p><p style='font-size:13pt'>{clean(m.group(1))}</p>"); continue
            if re.match(r"^(B-roll|Delivery):", line):
                lab, rest = line.split(":", 1); out.append(f"<p><b>{lab}:</b> {clean(rest)}</p>"); continue
            if line.startswith("- "): out.append(f"<p>&bull; {clean(line[2:])}</p>"); continue
            out.append(f"<p>{clean(line)}</p>")
    rs = (Path(job) / "research/RESEARCH.md").read_text()
    m = re.search(r"## Overall verdict\n(.+?)(?=\n## |\Z)", rs, re.S)
    if m:
        out.append("<h2>Research verdict</h2>")
        for line in m.group(1).splitlines():
            if not line.strip(): continue
            if line.startswith("### "): out.append(f"<p><b>{clean(line[4:])}</b></p>")
            elif line.startswith("- NEW:"): continue
            elif line.startswith("- "): out.append(f"<p>&bull; {clean(re.sub(r'^- H\d+:\s*', '', line))}</p>")
            else: out.append(f"<p>{clean(line)}</p>")
    return "\n".join(out)
if __name__ == "__main__":
    Path(sys.argv[3]).write_text(build(sys.argv[1], sys.argv[2])); print("wrote", sys.argv[3])
