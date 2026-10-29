"""Builds review/index.html + review/files.json from BOOK.md and shots.json (one page per job, newest on top). python3 build_review.py"""
import html, json, os, re, shutil, subprocess
from PIL import Image
e = html.escape
B = open("BOOK.md").read(); S = json.load(open("shots.json"))
CUTS = json.load(open("review/cuts.json")) if os.path.exists("review/cuts.json") else []
ASK = open("review/ask.html").read() if os.path.exists("review/ask.html") else ""
NOTES = json.load(open("review/notes.json")) if os.path.exists("review/notes.json") else {}
os.makedirs("review/img/sb", exist_ok=True); os.makedirs("review/media", exist_ok=True)
files = {}
def pub(rel): files[rel] = "ugc/pritech-vo5/review/" + rel; return rel

rows, cur, theme = {}, None, {}
for line in B.splitlines():
    m = re.match(r"\*\*(V\d)\*\* \((.*?)\)$", line)
    if m: cur = m.group(1); theme[cur] = m.group(2); rows[cur] = []
    m = re.match(r'\| (S\d) \| "(.*?)" \| (.*?) \| (HAND|HAND-FREE) \| (.*?) \| (.*?) \|$', line)
    if m and cur: rows[cur].append(m.groups())
total = re.search(r"TOTAL: \$([\d.]+)", B).group(1)
vo = re.search(r"^> (.+)$", B, re.M).group(1)
flow = re.search(r"Kie total then \$([\d.]+)", B).group(1)

# media: Grace's VO (mp3 for the phone), her post's contact sheet, room thumbs
if not os.path.exists("review/media/vo.mp3"):
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "vo/voiceover_final.wav", "-b:a", "160k", "review/media/vo.mp3"], check=True)
pub("media/vo.mp3")
im = Image.open("research/7701760026418990367/sheet.png").convert("RGB"); im.thumbnail((1400, 1400)); im.save("review/img/post_sheet.jpg", quality=82); pub("img/post_sheet.jpg")
def room(k):
    fn = f"img/room_{k}.jpg"
    if not os.path.exists("review/" + fn):
        r = Image.open(f"rooms/room_{k}.jpg").convert("RGB"); r.thumbnail((360, 640)); r.save("review/" + fn, quality=80)
    return pub(fn)
def thumb(sid):
    fn = f"img/sb/{sid}.jpg"
    if not os.path.exists(f"stills/{sid}.png"): return None
    im = Image.open(f"stills/{sid}.png").convert("RGB"); im.thumbnail((540, 960)); im.save("review/" + fn, quality=84); return pub(fn)

vids = ""
for v in ["V5", "V6", "V7", "V8", "V9"]:
    vs = [s for s in S if s["video"] == v]
    have = [s for s in vs if os.path.exists(f"stills/{s['id']}.png")]
    sb = "".join(f'<figure class="st{" redo" if "REDO" in NOTES.get(s["id"], "") else ""}"><a href="{thumb(s["id"])}"><img src="img/sb/{s["id"]}.jpg" alt="{s["id"]} still" loading="lazy"></a>'
                 f'<figcaption><b>{s["id"][2:]}</b> · {"HAND" if s["hand"] else "HAND-FREE"} · “{e(s["line"])}”' + (f'<br><span class="fix">{e(NOTES[s["id"]])}</span>' if s["id"] in NOTES else "") + "</figcaption></figure>"
                 for s in have)
    rooms = "".join(f'<figure class="room"><img src="{room(k)}" alt="room {k}" loading="lazy"><figcaption>{k}</figcaption></figure>' for k in sorted({s["room"] for s in vs}))
    trs = "".join(f"<tr><td class='n'>{a}</td><td class='vo'>“{e(b)}”</td><td>{e(c)}</td><td><span class='pill {'free' if d == 'HAND-FREE' else 'hand'}'>{d}</span></td><td>{e(f2)}</td><td>{e(g)}</td></tr>" for a, b, c, d, f2, g in rows[v])
    vids += f'''<section class="vid" id="{v.lower()}"><header><h2>{v}</h2><p class="look">{e(theme[v])}</p></header>
{f'<div class="sb">{sb}</div>' if sb else f'<div class="rooms">{rooms}</div>'}
<div class="tbl"><table><thead><tr><th>#</th><th>Words</th><th>On screen</th><th>Shot</th><th>Clip</th><th>Room</th></tr></thead><tbody>{trs}</tbody></table></div></section>'''
CUTHTML = ("<section class=\"vid\" id=\"cuts\"><h2>Cuts</h2><div class=\"cuts\">" + "".join(f'<figure><video src="{pub(c["file"])}" controls playsinline preload="metadata"></video><figcaption><b>{e(c["title"])}</b><br><span class="small">{e(c["note"])}</span></figcaption></figure>' for c in CUTS) + "</div></section>") if CUTS else ""
ASKHTML = ASK or f"""<section class="ask"><p class="eyebrow">Your call</p>
<p class="total">${total} <span class="small">Kie total, or ${flow} if you make the 30 product clips in Flow</span></p>
<ol><li><b>Product clips:</b> Kie Omni (in the total) or your Flow app (30 takes, 360 credits; October's credits end in 2 days)?</li>
<li><b>Voice:</b> is this Grace's own voice, not our clone? If yes I add it to her clone samples ($0).</li>
<li><b>Text:</b> her post has on-screen hook text; these five stay text-free unless you say yes. House of Rameau versions get the hook text, free, after you approve.</li>
<li><b>Approve</b> the plan below and I make all 45 stills first (storyboard is your next stop).</li></ol></section>"""
page = f"""<title>PRITECH Scrubber V5-V9</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Karla:wght@400;600&display=swap">
<style>
/* Layout: one reading column; your call first, then the VO, then one section per video (theme, rooms or stills, shot table) */
:root{{--bg:#f5f7f7;--card:#ffffff;--fg:#1c2426;--mute:#5a6a6d;--line:#d9e1e2;--accent:#2f7069;--hand:#e6efee;--free:#eef3e6;--freefg:#4b6a2a;--warn:#b5482d;
--display:'Fraunces',Georgia,serif;--body:'Karla',system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#131a1b;--card:#1b2325;--fg:#e4ecec;--mute:#97a8aa;--line:#2b3638;--accent:#7cc2b8;--hand:#20302f;--free:#263022;--freefg:#b5d396;--warn:#f08a6c;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#131a1b;--card:#1b2325;--fg:#e4ecec;--mute:#97a8aa;--line:#2b3638;--accent:#7cc2b8;--hand:#20302f;--free:#263022;--freefg:#b5d396;--warn:#f08a6c;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px}}
main{{max-width:920px;margin:0 auto;display:grid;gap:28px}}
h1,h2{{font-family:var(--display);font-weight:600;text-wrap:balance;margin:0}} h1{{font-size:1.9rem;line-height:1.15}} h2{{font-size:1.5rem}}
.eyebrow{{text-transform:uppercase;letter-spacing:.08em;font-size:.75rem;color:var(--accent);font-weight:600;margin:0}}
.look,.small{{color:var(--mute);font-size:.9rem;margin:0}}
.ask{{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:18px;display:grid;gap:10px}} .ask ol{{margin:0;padding-left:1.2em;display:grid;gap:6px}}
.total{{font-family:var(--display);font-size:1.6rem;margin:0}}
.vid{{display:grid;gap:12px;border-top:1px solid var(--line);padding-top:22px}} .vid header{{display:grid;gap:4px}}
blockquote{{margin:0;padding:12px 16px;border-left:3px solid var(--accent);background:var(--card);font-size:1.05rem}}
audio{{width:100%}}
.sb{{display:grid;grid-template-columns:repeat(auto-fill,minmax(130px,1fr));gap:12px}}
.rooms{{display:grid;grid-template-columns:repeat(auto-fill,minmax(120px,160px));gap:12px}}
figure{{margin:0;display:grid;gap:4px;min-width:0}} .st img,.room img{{border-radius:6px;aspect-ratio:9/16;object-fit:cover;width:100%;max-width:100%;display:block}}
figcaption{{font-size:.8rem}} .fix{{color:var(--mute)}} .st.redo img{{outline:3px solid var(--warn);outline-offset:2px}} .st.redo .fix{{color:var(--warn);font-weight:600}}
.tbl{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:.88rem}}
th,td{{text-align:left;vertical-align:top;padding:7px;border-bottom:1px solid var(--line)}} th{{color:var(--mute);font-weight:600;font-size:.75rem;text-transform:uppercase;letter-spacing:.05em}}
td.n{{font-variant-numeric:tabular-nums;font-weight:600}} td.vo{{min-width:150px}}
.pill{{display:inline-block;padding:2px 8px;border-radius:999px;font-size:.72rem;font-weight:600;white-space:nowrap}} .pill.hand{{background:var(--hand);color:var(--accent)}} .pill.free{{background:var(--free);color:var(--freefg)}}
.cuts{{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px}} video{{width:100%;max-width:100%;aspect-ratio:9/16;background:#000;border-radius:8px}}
.post img{{border-radius:8px;width:100%;max-width:100%}}
a{{color:var(--accent)}} a:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
</style>
<main>
<header><p class="eyebrow">Grace · PRITECH heated face scrubber, black · 2026-10-29</p><h1>Five new videos on Grace's voiceover</h1>
<p class="look">Same 20.9 s VO from her post in all five, 9 shots each, 45 shot ideas with none repeated, 10 new real rooms. Script gate OK.</p></header>
{ASKHTML}
{CUTHTML}
<section class="vid" id="vo"><h2>The voiceover</h2><blockquote>{e(vo)}</blockquote>
<audio controls preload="metadata" src="media/vo.mp3"></audio>
<p class="small">Grace's own audio from <a href="https://www.tiktok.com/t/ZPLDRXhd4">her post</a>, as posted: echo 150 ms (passes), no music. Flag: “towels just transfer bacteria” isn't on the listing; it stays (her audio) and shows as a used towel only.</p>
<figure class="post"><img src="img/post_sheet.jpg" alt="frames from Grace's post"><figcaption>Her post re-uses our V1-V4 clips, so none of these shot ideas come back.</figcaption></figure></section>
{vids}
</main>"""
open("review/index.html", "w").write(page)
json.dump(files, open("review/files.json", "w"), indent=1)
print("review page:", len(files), "files")
