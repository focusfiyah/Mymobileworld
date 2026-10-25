"""Builds review/index.html for OQQ pants from review/state.json (newest section first). Head/CSS from the JIYU page."""
import json, html
from pathlib import Path
R = Path(__file__).parent
st = json.loads((R / "state.json").read_text())
E = html.escape
out = [(R / "_head.html").read_text(), '<div class="wrap"><header><h1>OQQ wide-leg pants · black + brown</h1>',
       f'<p class="sub">{E(st["sub"])}</p></header>']
if st.get("ask"):
    out.append(f'<section class="ask"><strong>{E(st["ask"]["title"])}</strong><p style="margin:0">{st["ask"]["text"]}</p></section>')
for sec in st["sections"]:
    if sec["type"] == "grid":
        cells = []
        for c in sec["items"]:
            media = (f'<video controls playsinline preload="metadata" src="{c["src"]}"></video>' if c["src"].endswith(".mp4")
                     else f'<img src="{c["src"]}" alt="{E(c["n"])}">')
            cells.append(f'<div class="st">{media}<div class="h"><span class="n">{E(c["n"])}</span><span class="tag {c.get("cls","ok")}">{E(c["tag"])}</span></div><p>{E(c["p"])}</p></div>')
        out.append(f'<section class="box"><h2>{E(sec["h"])}</h2>' + (f'<p class="muted">{E(sec["note"])}</p>' if sec.get("note") else "")
                   + f'<div class="grid9">{"".join(cells)}</div></section>')
    elif sec["type"] == "kits":
        out.append(f'<section class="box"><h2>{E(sec["h"])}</h2><p class="muted">{E(sec["note"])}</p><p id="dlnote" class="muted dlnote">Saving is off on this page: long-press each image to save it, and use Copy prompt.</p></section>')
        for k in sec["items"]:
            imgs = "".join(f'<figure><img src="{p}" alt="{E(k["id"])} image {i+1}"><figcaption>{i+1} · {E(lbl)}</figcaption><button class="sv" data-src="{p}">Save</button></figure>'
                           for i, (p, lbl) in enumerate(k["imgs"]))
            out.append(f'<details class="box"{" open" if k.get("open") else ""}><summary><b>{E(k["id"])}</b> · {E(k["what"])}</summary>'
                       f'<ol><li>Flow: new project › Video › <b>Gemini Omni Flash</b> › 9:16 › 4 s</li><li>Add these {len(k["imgs"])} images in this order (tap Save under each one). Number 1 goes in the start frame if Flow asks.</li></ol>'
                       f'<div class="kitimgs">{imgs}</div><p style="margin:0">3. Paste this prompt: <button class="cp" data-p="p{k["id"]}">Copy prompt</button> <button class="svp" data-p="p{k["id"]}">Save prompt</button></p>'
                       f'<pre id="p{k["id"]}" class="kitp">{E(k["prompt"])}</pre><p class="muted">4. Download at 1080 and send it back in the chat.</p></details>')
        out.append((R / "_script.html").read_text())
    elif sec["type"] == "html":
        out.append(f'<section class="box"><h2>{E(sec["h"])}</h2>{sec["body"]}</section>')
out.append("</div>")
(R / "index.html").write_text("\n".join(out))
print("built", len("".join(out)))
