"""Week 3 Flow-kit review page (you-decide twin stories). Copies refs + rooms into week3/review/ and writes index.html."""
import json, shutil, html, pathlib
W = pathlib.Path(__file__).parent; R = W / "review"; R.mkdir(exist_ok=True)
old = (W.parent / "week2/review/index.html").read_text()
head = old[:old.index('<div class="wrap">')].replace("Content Batch Week 2", "Content Batch Week 3 Part 2s")
script = old[old.index("<script>"):]
for f in ["1_ralph_face_plain.jpg", "2_ralph_reference_sheet.jpg"]: shutil.copy(W.parent / "week2/review" / f, R / f)
S = json.load(open(W / "scripts.json"))
def two(p):  # 2-image backup (sheet + room) for Flow's prominent-people block (week 2 fix)
    a = p.index("Image 1 shows"); b = p.index("His body")
    p = p[:a] + "Image 1 is the character sheet of the man: same face, rimless glasses, smooth bald head and full beard with the grey at the chin, exactly as shown. " + p[b:]
    return p.replace("Image 3 is the room he is in", "Image 2 is the room he is in").replace(
        "Image 1 is only for his face; its plain grey backdrop and anything from the place it was taken never appear.", "The plain grey backdrop of image 1 never appears.")
def fig(src, n, cap, contain=False):
    st = ' style="object-fit:contain"' if contain else ""
    return f'<figure><img src="{src}" alt="Image {n}"{st}><figcaption>{n} · {cap}</figcaption><button class="sv" data-src="{src}">Save</button></figure>'
def btns(i): return f'<div class="btns"><button class="cp" data-p="{i}">Copy prompt</button><button class="svp" data-p="{i}">Save prompt</button></div>'
body = ['<div class="wrap">', '<header><h1>Week 3 · part 2 scripts + Flow kits</h1><p class="sub">The follow-ups R1-R3 promise. P1 posts Wed 11-25, P2 Fri 11-27, P3 Sun 11-29 (the day after each part 1), 7 PM ET, if you OK them. Every prompt asks for a US accent only.</p></header>',
        '<section class="ask"><strong>What I need from you</strong><ol><li>Read the 3 scripts below (each shot line is what you say). If they are OK, make the 12 clips in Flow (Veo 3.1 Lite, Ingredients to Video): for each shot save images 1-3 in that order, then copy the prompt.</li><li>If Flow blocks a shot, use the 2-image backup under it (sheet + room).</li><li>Send me the clips. I add your voice, the pace fix, the cards and the music, and put all 3 cuts here.</li></ol></section>',
        '<p class="muted dlnote" id="dlnote">Saving isn\'t available in this view: long-press an image to save it, and press and hold the prompt text to copy it.</p>']
for t in S["twin"]:
    kit = json.load(open(W / "kits" / t["id"] / "kit.json"))
    body.append(f'<section class="box"><h2>{t["id"]} · {html.escape(t["title"])} <span class="tag">part 2</span></h2><p class="muted">On screen from frame 0: {html.escape(" ".join(t["hook"]))}</p>')
    for k in kit:
        sid = k["shot"]; shutil.copy(W / "kits" / t["id"] / k["room"], R / k["room"])
        body.append(f'<details class="shot"><summary><span class="num">{sid}</span> <span class="tag">{k["angle"]}</span> <span class="say">{html.escape(k["line"])}</span></summary>')
        body.append('<div class="refs">' + fig("1_ralph_face_plain.jpg", 1, "your face") + fig("2_ralph_reference_sheet.jpg", 2, "athletic sheet v3", True) + fig(k["room"], 3, "room") + "</div>")
        body.append(btns("p" + sid) + f'<pre id="p{sid}">{html.escape(k["prompt"])}</pre>')
        body.append(f'<details><summary class="muted">Backup if Flow blocks it: 2 images</summary><div class="refs">' + fig("2_ralph_reference_sheet.jpg", 1, "athletic sheet", True) + fig(k["room"], 2, "room") + "</div>"
                    + btns("p" + sid + "b") + f'<pre id="p{sid}b">{html.escape(two(k["prompt"]))}</pre></details></details>')
    body.append("</section>")
out = head + "\n".join(body) + "\n</div>\n" + script
prev = R / "index.html"
if prev.exists() and "<video" in prev.read_text():   # keep the ask + videos block a later round added
    o = prev.read_text(); a = o.index('<section class="ask">'); b = o.index('<p class="muted dlnote"')
    x = out.index('<section class="ask">'); y = out.index('<p class="muted dlnote"'); out = out[:x] + o[a:b] + out[y:]
prev.write_text(out)
print("REVIEW_OK", len(list(R.glob("*_room.jpg"))))
