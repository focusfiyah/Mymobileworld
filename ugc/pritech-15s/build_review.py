"""Builds review/index.html from BOOK.md, scripts.md and shots.json (one page per job, newest on top). python3 build_review.py"""
import html, json, re
from PIL import Image
e = html.escape
B = open("BOOK.md").read(); S = json.load(open("shots.json")); sc = open("scripts.md").read()
CUTS = json.load(open("review/cuts.json")) if __import__("os").path.exists("review/cuts.json") else []
ASK = open("review/ask.html").read() if __import__("os").path.exists("review/ask.html") else ""
NOTES = json.load(open("review/notes.json")) if __import__("os").path.exists("review/notes.json") else {}
rows, cur = {}, None
for line in B.splitlines():
    m = re.match(r"\*\*(V\d)\*\* \((.*?)\)$", line)
    if m: cur = m.group(1); rows[cur] = {"theme": m.group(2), "r": []}
    m = re.match(r'\| (S\d) \| "(.*?)" \| (.*?) \| (HAND|HAND-FREE) \| (.*?) \| (.*?) \| (.*?) \|', line)
    if m and cur: rows[cur]["r"].append(m.groups())
meta = {v: re.search(rf"\*\*{v}, hook (.*?)\*\*", B).group(1) for v in ["V2", "V3", "V4"]}
total = re.search(r"TOTAL: \$([\d.]+)", B).group(1)
files = {}
def thumb(sid):
    fn = f"img/sb/{sid}.jpg"; im = Image.open(f"stills/{sid}.png").convert("RGB"); im.thumbnail((540, 960)); im.save("review/" + fn, quality=84)
    files[fn] = "ugc/pritech-15s/review/" + fn; return fn
vids = ""
for v in ["V2", "V3", "V4"]:
    script = re.search(rf"## {v}:.*\n(.+)", sc).group(1).strip()
    sb = "".join(f'<figure class="st{" redo" if "REDO" in NOTES.get(s["id"], "") else ""}"><a href="{thumb(s["id"])}"><img src="img/sb/{s["id"]}.jpg" alt="{s["id"]}" loading="lazy"></a>'
                 f'<figcaption><b>{s["id"][2:]}</b> · {"HAND" if s["hand"] else "HAND-FREE"} · “{e(s["line"])}”' + (f'<br><span class="fix">{e(NOTES[s["id"]])}</span>' if s["id"] in NOTES else "") + "</figcaption></figure>"
                 for s in S if s["video"] == v)
    trs = "".join(f"<tr><td class='n'>{a}</td><td class='vo'>“{e(b)}”</td><td>{e(c)}</td><td><span class='pill {'free' if d == 'HAND-FREE' else 'hand'}'>{d}</span></td><td>{e(f)}</td></tr>" for a, b, c, d, _, f, g in rows[v]["r"])
    vids += f'''<section class="vid" id="{v.lower()}"><header><h2>{v}</h2><p class="meta">Hook {e(meta[v])}</p></header>
<blockquote>{e(script)}</blockquote><p class="look"><b>Theme:</b> {e(rows[v]["theme"])}</p>
<div class="sb">{sb}</div>
<div class="tbl"><table><thead><tr><th>#</th><th>Words</th><th>On screen</th><th>Shot</th><th>Clip</th></tr></thead><tbody>{trs}</tbody></table></div></section>'''
for k in "DEFGHI": files[f"img/room_{k}.jpg"] = f"ugc/pritech-15s/review/img/room_{k}.jpg"
files["img/sheet.jpg"] = "ugc/pritech-15s/review/img/sheet.jpg"
CUTHTML = ("<section class=\"vid\" id=\"cuts\"><h2>Cuts</h2><div class=\"cuts\">" + "".join(f'<figure><video src="{c["file"]}" controls playsinline preload="metadata"></video><figcaption><b>{e(c["title"])}</b><br><span class="small">{e(c["note"])}</span></figcaption></figure>' for c in CUTS) + "</div></section>") if CUTS else ""
for c in CUTS: files[c["file"]] = "ugc/pritech-15s/review/" + c["file"]
page = f"""<title>PRITECH Scrubber V2-V4</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Karla:wght@400;600&display=swap">
<style>
/* Layout: one reading column; your call first, then one section per video (script, stills, shot table) */
:root{{--bg:#f6f7f8;--card:#ffffff;--fg:#1d2329;--mute:#5d6873;--line:#dde2e7;--accent:#3d6f8f;--hand:#e8eef3;--free:#e9f3ec;--freefg:#2f6b45;--warn:#b5482d;
--display:'Fraunces',Georgia,serif;--body:'Karla',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#14181c;--card:#1c2228;--fg:#e6eaee;--mute:#9aa6b1;--line:#2c343c;--accent:#86b6d4;--hand:#22303b;--free:#1f3227;--freefg:#9fd3b0;--warn:#f08a6c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#14181c;--card:#1c2228;--fg:#e6eaee;--mute:#9aa6b1;--line:#2c343c;--accent:#86b6d4;--hand:#22303b;--free:#1f3227;--freefg:#9fd3b0;--warn:#f08a6c;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px}}
main{{max-width:900px;margin:0 auto;display:grid;gap:28px}}
h1,h2{{font-family:var(--display);font-weight:600;text-wrap:balance;margin:0}} h1{{font-size:1.9rem;line-height:1.15}} h2{{font-size:1.5rem}} h3{{font-size:1.05rem;margin:0}}
.eyebrow{{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;color:var(--accent);font-weight:600;margin:0}}
.meta,.look,.small{{color:var(--mute);font-size:.9rem;margin:0}}
.ask{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;display:grid;gap:10px}} .ask ol{{margin:0;padding-left:1.2em;display:grid;gap:6px}}
.total{{font-family:var(--display);font-size:1.6rem;margin:0}}
.vid{{display:grid;gap:12px;border-top:1px solid var(--line);padding-top:22px}}
blockquote{{margin:0;padding:12px 16px;border-left:3px solid var(--accent);background:var(--card);font-size:1.05rem}}
.sb{{display:grid;grid-template-columns:repeat(auto-fill,minmax(140px,1fr));gap:12px}}
figure{{margin:0;display:grid;gap:4px}} .st img{{border-radius:6px;aspect-ratio:9/16;object-fit:cover;width:100%;display:block}}
.st figcaption{{font-size:.8rem}} .fix{{color:var(--mute)}} .st.redo img{{outline:3px solid var(--warn);outline-offset:2px}} .st.redo .fix{{color:var(--warn);font-weight:600}}
.tbl{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:.9rem}}
th,td{{text-align:left;vertical-align:top;padding:8px;border-bottom:1px solid var(--line)}} th{{color:var(--mute);font-weight:600;font-size:.78rem;text-transform:uppercase;letter-spacing:.05em}}
td.n{{font-variant-numeric:tabular-nums;font-weight:600}} td.vo{{min-width:140px}}
.pill{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.75rem;font-weight:600;white-space:nowrap}} .pill.hand{{background:var(--hand);color:var(--accent)}} .pill.free{{background:var(--free);color:var(--freefg)}}
.cuts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(240px,1fr));gap:16px}} .cuts video{{width:100%;aspect-ratio:9/16;background:#000;border-radius:8px;display:block}}
.rooms{{display:grid;grid-template-columns:repeat(auto-fill,minmax(110px,1fr));gap:10px}} .rooms img{{border-radius:6px;width:100%;display:block}}
</style>
<main>
<header style="display:grid;gap:6px"><p class="eyebrow">Grace · PRITECH black face scrubber · 2026-10-27</p>
<h1>Three new 15-second videos: V2, V3, V4</h1>
<p class="meta">Book total ${total} on Kie. Black PRITECH wand, same as V1; all new rooms, shots and order.</p></header>
{ASK}
{CUTHTML}
{vids}
<section class="vid"><h2>Rooms and product reference</h2><p class="small">Six new real rooms (Pexels/Pixabay), none from V1, and the real-photo product sheet every still and clip uses.</p>
<div class="rooms">{"".join(f'<figure><img src="img/room_{k}.jpg" alt="Room {k}"><figcaption class="small">Room {k}</figcaption></figure>' for k in "DEFGHI")}</div>
<figure style="max-width:520px"><img src="img/sheet.jpg" alt="PRITECH product sheet"></figure></section>
</main>"""
open("review/index.html", "w").write(page)
json.dump(files, open("review/files.json", "w"), indent=0)
print(len(files), "files")
