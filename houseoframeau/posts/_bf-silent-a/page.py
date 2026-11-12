"""Builds review/index.html (batch review page) and each post's script.md from post.json + vo/timing.json + check output."""
import json, subprocess, html
from pathlib import Path
H = Path(__file__).resolve().parent; P = H.parent
ORDER = ["butter", "mirror", "ear", "coloring", "meat"]
cards = []
for n in ORDER:
    post = P / f"bf-{n}"; c = json.loads((post / "post.json").read_text()); t = json.loads((post / "vo/timing.json").read_text())
    stat = subprocess.run(["python3", str(H / "check.py"), str(post)], capture_output=True, text=True).stdout.split("\n")[0]
    rows, md = [], [f"# {c['product']}, House of Rameau Black Friday version (2026-11-12), Ralph's voice (free Chatterbox clone)\n",
                    f"Source: Grace's approved CURRENT V1 (HD) silent cut + free Pexels holiday b-roll (broll/SOURCES.md). Hook {c['hook_id']} word for word.",
                    f"On-screen hook text (frame 0, until {c.get('hook_until', 'line 2')} s): \"{c['hook_text'].replace('|', ' ')}\". No captions, no product cards.\n"]
    starts = []
    for s in c["segs"]:
        a = s["at"]; starts.append((t[a]["start"] if isinstance(a, int) else a) + s.get("off", 0))
    for i, ln in enumerate(t):
        nxt = t[i + 1]["start"] if i + 1 < len(t) else 99
        shots = [c["segs"][k]["what"] for k, st in enumerate(starts) if ln["start"] - 0.35 <= st < nxt - 0.35]
        if not shots or starts.index(min(starts, key=lambda s: abs(s - ln["start"]))) and min(abs(s - ln["start"]) for s in starts) > 0.35:
            cur = max(k for k, st in enumerate(starts) if st <= ln["start"] + 0.01)
            if c["segs"][cur]["what"] not in shots: shots.insert(0, c["segs"][cur]["what"])
        md.append(f"{i + 1}. [{'; '.join(shots)}] {ln['text']}")
        rows.append(f"<li><span class=line>{html.escape(ln['text'])}</span><span class=shot>{html.escape(' / '.join(shots))}</span></li>")
    (post / "script.md").write_text("\n".join(md) + "\n")
    cards.append(f"""<section class=post id={n}>
<h2>{html.escape(c['product'])}</h2>
<p class=meta>{html.escape(stat)} · hook {c['hook_id']} · on-screen text: “{html.escape(c['hook_text'].replace('|', ' '))}”</p>
<video controls playsinline preload=metadata poster="{n}.jpg" src="{n}.mp4"></video>
<ol>{''.join(rows)}</ol></section>""")
page = (H / "page_template.html").read_text().replace("{{CARDS}}", "\n".join(cards))
(H / "review/index.html").write_text(page); print("PAGE_OK")
