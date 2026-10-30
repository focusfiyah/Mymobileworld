"""Builds review/index.html (one review page per job, newest on top) from shots.json + BOOK.md. python3 build_review.py"""
import html, json, os, re
from PIL import Image
e = html.escape
B = open("BOOK.md").read(); S = json.load(open("shots.json"))["shots"]
os.makedirs("review/img", exist_ok=True)
def thumb(src, dst, w=520):
    im = Image.open(src).convert("RGB"); im.thumbnail((w, w * 2)); im.save("review/img/" + dst, quality=82); return "img/" + dst
rooms = {"A": thumb("rooms/pick/A_armchair_tree.jpg", "room_A.jpg"), "B": thumb("rooms/pick/B_gift_table.jpg", "room_B.jpg"), "C": thumb("rooms/pick/C_coat_closet.jpg", "room_C.jpg")}
sheet = thumb("refs/product_sheet.png", "sheet.jpg", 1100)
front = thumb("refs/listing_1.jpg", "front.jpg", 900)
total = re.search(r"TOTAL: \$([\d.]+)", B).group(1)
script = re.search(r"^> (.+)$", B, re.M).group(1)
qs = re.findall(r"^\d\. (.+)$", B.split("## 7. Questions")[1].split("## 8.")[0], re.M)
cost = re.findall(r"^\| ([^|]+) \| ([^|]+) \| ([\d.]+) \|$", B, re.M)
ON = {m.group(1): m.group(2) for m in re.finditer(r'^\| (S\d) \| [^|]+ \| "[^"]+" \| ([^|]+) \|', B, re.M)}
rows = ""
for s in S:
    tag = "HAND" if s["hand"] else "HAND-FREE"
    rows += f"""<article class="shot"><img src="{rooms[s['room']]}" alt="Room {s['room']}" loading="lazy">
<div class="sb"><div class="meta"><b>{s['id']}</b><span class="pill {'hf' if not s['hand'] else ''}">{tag}</span><span class="t">{s['t'][0]:.1f}-{s['t'][1]:.1f} s</span></div>
<p class="line">&ldquo;{e(s['line'])}&rdquo;</p><p>{e(ON.get(s['id'], ''))}</p><p class="model">{e(s['model'])} &middot; room {s['room']}</p>
<details><summary>Still prompt</summary><p class="pr">{e(s['still'])}</p></details><details><summary>Clip prompt</summary><p class="pr">{e(s['clip'])}</p></details></div></article>"""
page = f"""<title>Christmas Cheer Review</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600&family=Source+Sans+3:wght@400;600&display=swap">
<style>
/* layout: one phone-width column, plan first, shots as stacked cards with the room photo beside the words */
:root{{--bg:#fbf8f6;--fg:#24201f;--muted:#6d6461;--line:#e6dcd8;--card:#ffffff;--accent:#c2185b;--pine:#2e5d3a;
--display:"Fraunces",Georgia,serif;--body:"Source Sans 3",system-ui,sans-serif}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#1b1718;--fg:#f1eaE7;--muted:#b3a7a3;--line:#3a3233;--card:#252021;--accent:#f06292;--pine:#7fbf8e;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#1b1718;--fg:#f1eae7;--muted:#b3a7a3;--line:#3a3233;--card:#252021;--accent:#f06292;--pine:#7fbf8e;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.5 var(--body);padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));padding-block:20px 48px}}
main{{max-width:760px;margin:0 auto;display:grid;gap:28px}}
h1,h2{{font-family:var(--display);text-wrap:balance;margin:0}} h1{{font-size:1.9rem;line-height:1.15}} h2{{font-size:1.25rem}}
.eyebrow{{text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;color:var(--pine);font-weight:600}}
section{{display:grid;gap:12px}} p{{margin:0}} .muted{{color:var(--muted)}}
.total{{display:flex;flex-wrap:wrap;gap:8px 20px;align-items:baseline;border-top:2px solid var(--accent);padding-top:12px}}
.total b{{font-family:var(--display);font-size:2rem;color:var(--accent);font-variant-numeric:tabular-nums}}
ol.q{{margin:0;padding-left:1.3em;display:grid;gap:8px}}
blockquote{{margin:0;font-family:var(--display);font-size:1.2rem;line-height:1.4;border-left:3px solid var(--pine);padding-left:14px}}
table{{border-collapse:collapse;width:100%;font-variant-numeric:tabular-nums}} td{{border-bottom:1px solid var(--line);padding:6px 4px;vertical-align:top}} td:last-child{{text-align:right}}
.shot{{display:grid;grid-template-columns:120px 1fr;gap:14px;background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}}
.shot img{{width:120px;border-radius:6px;object-fit:cover;aspect-ratio:2/3}} .sb{{min-width:0;display:grid;gap:6px}}
.meta{{display:flex;gap:8px;align-items:center;flex-wrap:wrap}} .t{{color:var(--muted);font-variant-numeric:tabular-nums;font-size:.9rem}}
.pill{{font-size:.72rem;letter-spacing:.06em;font-weight:600;padding:2px 8px;border-radius:99px;border:1px solid var(--accent);color:var(--accent)}} .pill.hf{{border-color:var(--pine);color:var(--pine)}}
.line{{font-weight:600}} .model{{color:var(--muted);font-size:.9rem}}
details summary{{cursor:pointer;color:var(--pine);font-weight:600;font-size:.9rem}} .pr{{font-size:.85rem;color:var(--muted);overflow-wrap:anywhere;margin-top:6px}}
figure{{margin:0;display:grid;gap:6px}} figure img{{border-radius:8px;border:1px solid var(--line)}} figcaption{{font-size:.88rem;color:var(--muted)}}
.two{{display:grid;grid-template-columns:repeat(auto-fit,minmax(220px,1fr));gap:14px}}
@media (max-width:440px){{.shot{{grid-template-columns:88px 1fr}} .shot img{{width:88px}}}}
</style>
<main>
<header style="display:grid;gap:6px"><span class="eyebrow">Grace &middot; plan v1 &middot; 2026-10-30</span><h1>Plant Therapy Christmas Cheer, 15 s</h1>
<p class="muted">Hands + hand-free AI video over Grace's voice. Nothing has been spent yet. Reply with your OK and the answers below.</p></header>
<section><h2>Your answers needed</h2><ol class="q">{''.join(f'<li>{e(q)}</li>' for q in qs)}</ol></section>
<section><div class="total"><b>${total}</b><span>total if Kie makes everything (includes one likely redo)</span></div>
<table>{''.join(f'<tr><td>{e(a)}</td><td>{e(b)}</td><td>${c}</td></tr>' for a,b,c in cost)}</table>
<p class="muted">Flow option: you make the 4 product clips free in your Flow app, Kie total $1.53. Month so far $232.92 (no cap in October).</p></section>
<section><h2>Script</h2><blockquote>{e(script)}</blockquote>
<p class="muted">52 words, reading grade 2.5, about 15 s. Hook H062. Gate 9 of 9. No on-screen text unless you say yes.</p></section>
<section><h2>Shots</h2>{rows}</section>
<section><h2>The real product</h2><div class="two"><figure><img src="{front}" alt="Real front labels"><figcaption>Real listing photo: Christmas Tree and Sugar Plum Fairy carry KidSafe, Vanilla Spice does not.</figcaption></figure>
<figure><img src="{sheet}" alt="Product reference sheet"><figcaption>Reference sheet from real photos only (front, box, cap off, back). Sent with every product prompt.</figcaption></figure></div></section>
<section><h2>What the research found</h2><p>On TikTok Shop this set has 74 sold and 4.4 stars. The best videos selling it reached 10.2K and 9.1K views. They open with the product next to a tree or a diffuser and describe Christmas Tree as smelling like a fresh-cut tree. People search for "christmas tree smell for fake trees", so the hook speaks to people with a fake tree.</p></section>
</main>"""
open("review/index.html", "w").write(page)
print(json.dumps({k: "ugc/plant-therapy-christmas-cheer/review/" + v for k, v in {**{f"img/room_{x}.jpg": f"img/room_{x}.jpg" for x in "ABC"}, "img/sheet.jpg": "img/sheet.jpg", "img/front.jpg": "img/front.jpg"}.items()}))
