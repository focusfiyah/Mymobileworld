"""Builds preview/index.html, the one review page for this job (republished to the same URL each round)."""
import json, html
S = json.load(open("shots.json"))["shots"]
E = html.escape
meta = {"V1": ("One cold room", "H063", "Rooms tour: bedroom, desk, couch. Modeled on @myfamilypov (765K) and @shun50111 (115K)."),
        "V2": ("Kids, dogs and tip-over", "H027", "Safety buyer guide. Answers the top searches: are space heaters safe, safe for pets. Modeled on @camronnbrown (3.1M)."),
        "V3": ("6 a.m. demo", "H126", "Identity humor + top-panel demo. Modeled on @drezilla13 (16.5% engagement) and @myfamilypov.")}
vids = ""
for v, (name, hid, why) in [("V1", meta["V1"])]:   # Ralph 2026-10-19: one script only, the best one (V1)
    vo = open(f"vo/{v}.txt").read().strip(); rows = ""
    for s in [x for x in S if x["video"] == v]:
        rows += f'<tr><td class="id">{s["id"][2:]}</td><td><span class="pill {"h" if s["hand"] else "f"}">{s["kind"]}</span></td><td>{E(s["line"])}</td><td class="muted">{E(s["still"])}<br><em>{E(s["motion"])}</em></td></tr>'
    vids += f'''<section class="vid" id="{v.lower()}"><h3>{v} · {E(name)} <span class="tag">hook {hid}</span></h3><p class="muted">{E(why)} About {len(vo.split())} words, ~{len(vo.split())/3.2:.0f} s.</p>
<blockquote>{E(vo)}</blockquote><figure><img src="{v}_layout.jpg" alt="{v} room per shot"><figcaption>Free layout: the room each shot uses (blue = hand-free, orange = hand). The paid stills put the heater and Grace's hand in.</figcaption></figure>
<div class="scroll"><table><thead><tr><th>#</th><th>Type</th><th>Line</th><th>What we see / motion</th></tr></thead><tbody>{rows}</tbody></table></div></section>'''
page = open("tools/review_template.html").read().replace("{{VIDEOS}}", vids)
open("preview/index.html", "w").write(page); print("ok", len(page))
