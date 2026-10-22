"""Builds gemini_app/kit.html (the Gemini-app kit page) from make_prompts.py. python3 gemini_app/make_kit.py"""
import html, importlib.util, sys
from pathlib import Path
D = Path(__file__).resolve().parent
sys.argv = ["x", "B"]
spec = importlib.util.spec_from_file_location("mp", D / "make_prompts.py"); mp = importlib.util.module_from_spec(spec); spec.loader.exec_module(mp)
names = {"ref1": "1 · Real photos sheet", "ref2": "2 · Real, upright, clip on top", "ref3": "3 · Lens shape only", "ref4": "4 · Grace's hand",
         "ref5": "5 · Real USB-A port", "ref6": "6 · Real logo close-up"}
files = {v[0].split("_", 1)[0]: v[0] for v in mp.REF.values()}
refgrid = "".join(f'<figure><img src="{files[k]}" alt="{n}"><figcaption>{n}</figcaption></figure>' for k, n in sorted(names.items()))
cards = []
for sid, line, rl, hand, scene in mp.SHOTS:
    text, fl = mp.prompt(sid, line, rl, hand, scene)
    ups = "".join(f'<figure><img src="{f}" alt="{f}"><figcaption>Upload {i}: {f.split("_", 1)[0]}</figcaption></figure>' for i, f in enumerate(fl, 1))
    cards.append(f'''<article class="shot" id="{sid.lower()}"><div class="head"><span class="num">{sid}</span><span class="chip{'' if hand else ' free'}">{'Hand' if hand else 'Hand-free'}</span></div>
<p class="say">{html.escape(line)}</p>
<p class="lbl">Upload in this order</p><div class="ups">{ups}</div>
<p class="lbl">Paste this prompt</p><pre id="p-{sid}">{html.escape(text)}</pre>
<button type="button" class="copy" data-t="p-{sid}" id="c-{sid}">Copy prompt</button></article>''')
css = (D / "kit.css").read_text()
page = f'''<title>Flashlight V2 Gemini Kit</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>{css}</style>
<div class="wrap">
<header><h1>Flashlight V2 · Gemini kit</h1><p class="sub">9 stills for Grace's flashlight video, built from your real photos: light blue-grey body, panel then power button, dark metal end cap with the Smiling Shark logo, 15.7 cm with the clip.</p></header>
<section class="box"><h2>How to do each shot</h2><ol>
<li>Save the 6 images below once (press and hold an image, then Save). They replace every earlier set.</li>
<li>For each shot, open a <b>new</b> Gemini chat and pick the image model (Nano Banana Pro if it offers a choice).</li>
<li>Upload that shot's images <b>in the order shown</b>, tap Copy prompt, paste and send.</li>
<li>Send the picture back here. I'll check it at 2x and do any free fixes. A Gemini mark in the corner is fine; I crop it.</li></ol></section>
<section class="box"><h2>The 6 reference images</h2><div class="refs">{refgrid}</div></section>
{"".join(cards)}
</div>
<script>
document.querySelectorAll('.copy').forEach(b=>b.addEventListener('click',()=>{{const el=document.getElementById(b.dataset.t);const t=el.textContent;
const done=()=>{{b.textContent='Copied';setTimeout(()=>b.textContent='Copy prompt',1600)}};
const sel=()=>{{const r=document.createRange();r.selectNodeContents(el);const s=getSelection();s.removeAllRanges();s.addRange(r);b.textContent='Selected: press Copy'}};
try{{navigator.clipboard.writeText(t).then(done,sel)}}catch(e){{sel()}}}}));
</script>'''
(D / "kit.html").write_text(page); print("kit.html", len(page))
