"""Review page for Vans V18-V37 (one page per job, republished each round). python3 review/build.py -> review/index.html"""
import html, json, re, sys
from pathlib import Path

J = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(J / "tools"))
S = json.loads((J / "shots.json").read_text())
book = (J / "BOOK.md").read_text()
total = re.search(r"\nTOTAL: \$([\d.]+)", book).group(1)
CAP = dict(re.findall(r"## (V\d\d)\n(.+)", (J / "scripts.md").read_text()))
import book as B  # noqa: E402  (SHORT, PLACE labels)
e = html.escape
LINKS = [("1", "ZPLnjUU3p", "@girlypopshopfinds", "7,953", "8 s", "Hand turns the shoe over her legs on concrete", "street", "V18-V20"),
         ("2", "ZPLnjhxGh", "@herstyledcloset", "5,367", "8 s", "One take seated on a rug, finger taps the tab", "roomL_wide", "V21-V23"),
         ("3", "ZPLnj2pMc", "@champagne.mami.xoxo", "1,735", "16 s", "In the car, held shoe close-ups, foot on the dash", "car", "V24-V26"),
         ("4", "ZPLnjFctx", "@mostly.millie", "507", "10 s", "Styled close-ups at a table (we keep it bright)", "living", "V27-V29"),
         ("5", "ZPLnjkDyF", "@sophmademebuyit", "14,400", "16 s", "Car door: held shoe beside the worn one", "car", "V30-V32"),
         ("6", "ZPLn2wKg5", "@sophmademebuyit", "367,800", "19 s", "Car + sidewalk: held angles, sole, walking", "street", "V33-V35")]
LOGO = {"real_vans_tab.jpg": "side tab", "real_heel_label.jpg": "heel label", "real_insole_logo.jpg": "insole", "shoe_closeup.jpg": "sequins", "real_top_sole.jpg": "sole"}
OUTF = {}
src = (J / "tools/make_shots.py").read_text()
OUT = eval(re.search(r"OUT = (\[.*?\])\n", src, re.S).group(1))
for i, v in enumerate(sorted({s["video"] for s in S.values()})): OUTF[v] = OUT[i % len(OUT)].split("|")[0]

links = "".join(f"""<article class="link"><div class="lh"><span class="ln">Link {n}</span><span class="lv">{vids}</span></div>
<img src="img/link{n}.jpg" alt="Link {n} frames" loading="lazy">
<p><b>{e(who)}</b> · {views} views · {dur}</p><p class="muted">{e(desc)}</p>
<p><a href="https://www.tiktok.com/t/{code}/">Open on TikTok</a></p></article>""" for n, code, who, views, dur, desc, _, vids in LINKS)

places = "".join(f'<figure><img src="img/place_{p}.jpg" alt="{e(t)}" loading="lazy"><figcaption>{e(t)}</figcaption></figure>' for p, t in
                 [("street", "Cafe sidewalk (Links 1, 5-6 outside the car)"), ("roomL_wide", "Grace's saved cream bedroom (Link 2, V37)"),
                  ("car", "Car with cream seats (Links 3, 5, 6, V36)"), ("living", "Bright living room (Link 4)")])

vids = []
for v in sorted({s["video"] for s in S.values()}):
    ss = [(k, s) for k, s in S.items() if s["video"] == v]
    rows = "".join(f'<tr><td class="t">{s["window"][0]:.1f}–{s["window"][1]:.1f}</td><td>{e(B.SHORT[s["beat"]])}</td>'
                   f'<td><span class="chip {"h" if s["kind"] == "HAND" else "f"}">{"hand" if s["kind"] == "HAND" else "hand-free"}</span></td>'
                   f'<td class="lg">{", ".join(LOGO[r.split("/")[-1]] for r in s["still_refs"] if r.split("/")[-1] in LOGO)}</td></tr>' for k, s in ss)
    src_links = sorted({s["beat"][0] for _, s in ss})
    vids.append(f"""<section class="vid"><div class="vhead"><span class="vnum">{v}</span><span class="from">from Link {" + ".join(src_links)}</span></div>
<dl><dt>Setting</dt><dd>{e(B.PLACE[ss[0][1]["place"]])}</dd><dt>Outfit</dt><dd>{e(OUTF[v])}</dd><dt>Caption</dt><dd>{e(CAP[v])}</dd></dl>
<div class="tw"><table><thead><tr><th>Time (s)</th><th>Shot</th><th>Kind</th><th>Logo refs</th></tr></thead><tbody>{rows}</tbody></table></div></section>""")

prompts = "".join(f'<details><summary>{k} · {e(B.SHORT[s["beat"]])}</summary><p class="pl">Still ({len(s["still_refs"])} refs: {", ".join(r.split("/")[-1] for r in s["still_refs"])})</p>'
                  f'<pre>{e(s["still"])}</pre><p class="pl">Clip (Seedance 2.0 Mini, 4 s, first frame = the approved still)</p><pre>{e(s["clip"])}</pre></details>' for k, s in S.items())

FL = json.loads((J / "qc/flags.json").read_text())
SB = "".join(f'<figure class="sb"><img src="sb/{v}.jpg" alt="{v} storyboard, 5 stills" loading="lazy"><figcaption><b>{v}</b>{" · example" if v in ("V18","V21","V24","V27","V30","V33") else ""} · {e(B.PLACE[S[v+"S1"]["place"]])}'
             + "".join(f'<br><span class="flag">S{k[-1]}: {e(t)}</span>' for k, t in FL.items() if k.startswith(v)) + "</figcaption></figure>"
             for v in sorted({s["video"] for s in S.values()}))
page = f"""<title>Vans V18–V37 Plan</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700&family=Source+Sans+3:wght@400;600&family=JetBrains+Mono:wght@500&display=swap">
<style>
/* Layout: one reading column; the ask and the total first, then the six links, the settings, the 20 videos, the prompts */
:root{{--bg:#f7f6f2;--card:#ffffff;--fg:#1b1a17;--muted:#66625a;--line:#dedad1;--accent:#b4232a;--chip:#efece4;
--display:"Barlow Condensed",Impact,sans-serif;--body:"Source Sans 3",system-ui,sans-serif;--mono:"JetBrains Mono",ui-monospace,monospace}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#161512;--card:#1f1e1a;--fg:#ecebe6;--muted:#a7a397;--line:#34322c;--accent:#e2575c;--chip:#2a2924;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#161512;--card:#1f1e1a;--fg:#ecebe6;--muted:#a7a397;--line:#34322c;--accent:#e2575c;--chip:#2a2924;color-scheme:dark}}
body{{background:var(--bg);color:var(--fg);font:16px/1.55 var(--body)}}
.wrap{{max-width:900px;margin:0 auto;padding-block:28px 64px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));display:grid;gap:36px}}
h1,h2{{font-family:var(--display);font-weight:700;letter-spacing:.01em;text-wrap:balance;margin:0;line-height:1.05}}
h1{{font-size:clamp(2.2rem,6vw,3.4rem)}} h2{{font-size:1.9rem}}
.check{{height:10px;background:repeating-conic-gradient(var(--fg) 0 25%,var(--bg) 0 50%) 0 0/20px 20px;opacity:.85}}
.muted{{color:var(--muted)}} a{{color:var(--accent)}}
.ask{{display:grid;gap:10px}}
.total{{display:flex;flex-wrap:wrap;gap:16px 32px;align-items:baseline;border:1px solid var(--line);background:var(--card);padding:18px 20px;border-radius:6px}}
.total .n{{font-family:var(--display);font-size:2.6rem;color:var(--accent);font-variant-numeric:tabular-nums}}
.total ul{{margin:0;padding-left:18px}}
.links{{display:grid;gap:20px}}
.link{{display:grid;gap:6px;min-width:0}} .link p{{margin:0}}
.lh{{display:flex;gap:12px;align-items:baseline}} .ln{{font-family:var(--display);font-size:1.5rem}} .lv{{font-family:var(--mono);font-size:.8rem;color:var(--muted)}}
.link img{{width:100%;border-radius:4px;border:1px solid var(--line)}}
.places{{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px}}
.places figure{{margin:0}} .places img{{width:100%;aspect-ratio:3/4;object-fit:cover;border-radius:4px}} figcaption{{font-size:.85rem;color:var(--muted)}}
.vid{{border-top:1px solid var(--line);padding-top:16px;display:grid;gap:10px;min-width:0}}
.vhead{{display:flex;gap:12px;align-items:baseline}} .vnum{{font-family:var(--display);font-size:1.8rem}} .from{{font-family:var(--mono);font-size:.8rem;color:var(--muted)}}
dl{{display:grid;grid-template-columns:max-content 1fr;gap:4px 14px;margin:0}} dt{{font-size:.75rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted);padding-top:3px}} dd{{margin:0;min-width:0}}
.tw{{overflow-x:auto}} table{{border-collapse:collapse;width:100%;font-size:.92rem}} th,td{{text-align:left;padding:6px 8px;border-bottom:1px solid var(--line);vertical-align:top}}
th{{font-size:.72rem;text-transform:uppercase;letter-spacing:.08em;color:var(--muted)}} .t{{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}}
.lg{{color:var(--muted);font-size:.85rem}}
.chip{{display:inline-block;padding:1px 8px;border-radius:99px;font-size:.78rem;background:var(--chip);white-space:nowrap}} .chip.h{{color:var(--accent)}}
details{{border-bottom:1px solid var(--line);padding:6px 0}} summary{{cursor:pointer;font-weight:600}} pre{{white-space:pre-wrap;font:13px/1.5 var(--mono);background:var(--card);border:1px solid var(--line);padding:10px;border-radius:4px}}
.sb{{margin:0 0 18px;display:grid;gap:6px}} .sb img{{width:100%;border-radius:4px}} .flag{{color:var(--accent);font-size:.9rem}}
.pl{{margin:8px 0 4px;font-size:.85rem;color:var(--muted)}}
</style>
<div class="check" aria-hidden="true"></div>
<main class="wrap">
<header class="ask"><h1>Vans sequin V18–V37: the plan</h1>
<p>20 music-only videos, 16 s each, 5 shots of 3.2 s. Three from each of Grace's 6 links (same beats, new look), plus V36 and V37 that mix the best beats. Every video has its own setting angle, outfit, shot order and grade. No voice, no on-screen text.</p></header>
<section class="total"><div><div class="muted">Total on Kie</div><div class="n">${total}</div></div>
<ul><li>100 stills (Gemini 3 Pro Image) $9.00</li><li>100 clips (Seedance 2.0 Mini, 4 s) $16.40</li><li>Redo allowance $4.60, each redo asked first; the job never passes $30.00</li><li>Music: free tracks, $0</li><li>November: $39.90 so far, at most $69.90 after this job</li></ul>
<p class="muted">Order: all 100 stills → storyboard here → one example video per link (V18, V21, V24, V27, V30, V33; test clip V30S1 first, $4.92 for the 30 clips) → your OK → the other 14 videos. Every hand and ankle uses Grace's real complexion, taken from her own Vans post.</p></section>
<section><h2>Storyboard: all 100 stills</h2><p class="muted">Five shots per video, left to right. Red outline = needs a redo (25 stills, $2.25, not run yet; 2 added for arm and leg positions). Grace's complexion comes from her own Vans post: every hand and ankle should match it. Examples get made first: V18, V21, V24, V27, V30, V33.</p>{SB}</section>
<section><h2>The six links</h2><div class="links">{links}</div></section>
<section><h2>Settings</h2><p class="muted">One setting per video (Grace's rule). Real free photos; the bedroom is Grace's saved one.</p><div class="places">{places}</div></section>
<section><h2>The 20 videos</h2>{''.join(vids)}</section>
<section><h2>Prompts</h2><p class="muted">Every still and clip prompt, exactly as it will run.</p>{prompts}</section>
</main>
"""
(J / "review/index.html").write_text(page)
print("review/index.html", len(page) // 1024, "KB")
