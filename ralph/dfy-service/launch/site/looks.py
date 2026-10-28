"""Always Answered landing page in three looks, built from ONE brand block (the thumbnail-looks method: one block changes,
each look is a familiar format described by its parts, and the looks are measured so no two share a layout).

Usage:
  python3 looks.py build            write looks/<band>.html (Artifact fragment) + looks/<band>.standalone.html
  python3 looks.py measure          phone + desktop screenshots, pairwise shared-frame score (thumbnail-looks cells()), sheet
  python3 looks.py pick <band>      copy that look to ../index.html + page.html (the page that gets hosted)

Bands: ticket (a carbon-copy service work order), door (a shop door's gold-leaf glass and hours plate),
lockscreen (a phone lock screen with notifications stacking up). Edit BRAND to change the words on all three.
"""
import html, json, pathlib, sys

HERE = pathlib.Path(__file__).parent
OUT = HERE / "looks"

BRAND = {
    "name": "Always Answered",
    "phone": "",          # our Twilio line, once bought (shown as a placeholder until then)
    "booking": "https://calendly.com/teamrrgrp/30min",        # Calendly link, once made
    "area": "Freeport, Baldwin and Brooklyn",
    "area_footer": "Serving Nassau County and Brooklyn",
    "h1a": "Every call answered.",
    "h1b": "Fresh reviews every month.",
    "sub": "When you're on a job, your phone still gets picked up. The assistant books the work or sends you the details "
           "within a minute, and new reviews keep coming in.",
    "check": "Try this tonight: call your own business at 7 PM. If it rings out, that customer is now calling someone else.",
    "stats": [
        ("44%", "of business calls go unanswered, out of 70 million calls studied.", "Invoca, 2026",
         "https://justcall.io/blog/missed-call-statistics.html"),
        ("78%", "of people have given up on a business after nobody picked up.", "CallRail survey, 2025",
         "https://beside.com/blog/missed-calls-cost-small-business"),
        ("74%", "of people look for reviews from the last 3 months before they choose.", "BrightLocal, 2026",
         "https://www.brightlocal.com/research/local-consumer-review-survey/"),
    ],
    "calls": [
        "Every call answered, day and night, on your own number.",
        "During your hours it can pass the call to you.",
        "Otherwise it books the job or takes the name, number and what they need, and emails you within a minute.",
        "Every Monday, a list of every call and what got booked.",
        "We set it up from your services, prices and hours, and fix it every week.",
    ],
    "reviews": [
        "After each job, your customer gets a short email or WhatsApp message, or scans a card at your counter, asking for a Google review.",
        "We ask every customer the same way. No fake reviews, ever.",
        "We write a reply to every new review in your voice. You approve it first.",
        "Each month, your new reviews and star average.",
    ],
    "steps": [
        ("Call or book a 15-minute call.", "Tell us your services, prices, hours and area."),
        ("We build your assistant", "on your business, and you call it to hear it before anything goes live."),
        ("Turn on call forwarding", "from your phone. We send the steps for your phone company. Your number stays the same."),
    ],
    "price": "$397", "price_line": "a month, plus $497 one-time setup. Month to month. Cancel any time.",
    "minutes": "Includes up to 500 call minutes a month. Most small businesses use far less.",
    "founding_t": "Founding offer: first 3 businesses",
    "founding": "No setup fee and the first 14 days free. If you like it, we ask for a short testimonial.",
    "faq": [
        ("Does it sound like a robot?", "Call our line and hear it for yourself. It talks like a calm front desk person and keeps calls short."),
        ("Does it pretend to be a person?", "No. It answers as your assistant and says the call may be recorded. If a caller asks, it says it's an AI assistant."),
        ("Do I need a new phone number?", "No. You forward your calls to us when you can't pick up, or all the time. Your customers call the same number they always have."),
        ("What if a caller wants me?", "During the hours you pick, it passes the call to you. After hours it takes a message and you get it by email right away."),
        ("Will it call my customers?", "No. It only answers calls. It never makes calls."),
        ("Is there a contract?", "No. It's month to month and you can cancel any time."),
    ],
    # the example evening, used by every look in its own form
    "log": [
        ("6:48 PM", "miss", "Rang out. Caller tried the next company."),
        ("6:48 PM", "ok", "Answered. No heat upstairs. Booked Wed 8:00 AM. Details sent to you."),
        ("9:15 PM", "ok", "Answered. Quote for a water heater. Name and number sent to you."),
    ],
}

e = html.escape
FONTS = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
GUTTER = "padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));"

# Same script on every look: fills name, phone and booking from BRAND, or marks them as drafts.
SCRIPT = """<script>
const CONFIG = %s;
(function(){
  document.querySelectorAll("[data-name]").forEach(el => el.textContent = CONFIG.name);
  const tel = (CONFIG.phone || "").replace(/[^0-9+]/g, "");
  document.querySelectorAll("[data-phone]").forEach(el => { if (CONFIG.phone) el.textContent = CONFIG.phone; else el.classList.add("draft"); });
  document.querySelectorAll("[data-call]").forEach(a => { if (tel) a.href = "tel:" + tel; else a.removeAttribute("href"); });
  document.querySelectorAll("[data-book]").forEach(a => { if (CONFIG.booking) a.href = CONFIG.booking; else { a.removeAttribute("href"); a.classList.add("draft"); } });
})();
</script>"""


def head(title_extra, fonts_q, css):
    return ("<title>Always Answered</title>\n<meta name=\"claude:viewport-fit-sides\" content=\"cover\">\n"
            "<meta name=\"description\" content=\"Every call answered and fresh reviews every month, for service businesses in "
            + e(BRAND["area"]) + ".\">\n" + FONTS + "\n<link rel=\"stylesheet\" href=\"https://fonts.googleapis.com/css2?"
            + fonts_q + "&display=swap\">\n<style>\n/* look: " + title_extra + " */\n" + css + "\n</style>\n")


def phone_text():
    return e(BRAND["phone"] or "(516) 000-0000")


def stats_html(cls):
    return "".join(f'<div class="{cls}"><b>{e(n)}</b><span>{e(t)}</span><a href="{u}" target="_blank" rel="noopener">{e(s)}</a></div>'
                   for n, t, s, u in BRAND["stats"])


def li(items):
    return "".join(f"<li>{e(i)}</li>" for i in items)


def faq_html():
    return "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in BRAND["faq"])


def steps_html():
    return "".join(f"<li><b>{e(a)}</b> {e(b)}</li>" for a, b in BRAND["steps"])


# ---------------------------------------------------------------- band 1: carbon-copy service work order
def ticket():
    css = """
:root{--desk:#d9dee3;--paper:#fbf4cf;--paper2:#fff9df;--ink:#1d2740;--carbon:#2b4c9b;--stamp:#c3361f;--rule:#d8c98a;--muted:#5a5f6e;
  --head:"Barlow Condensed","Arial Narrow",sans-serif;--body:"Barlow",Arial,sans-serif;--hand:"Kalam","Comic Sans MS",cursive;--mono:"Courier Prime",Courier,monospace}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--desk:#151b24;--paper:#2a2a1f;--paper2:#302f23;--ink:#efe9cf;--carbon:#8fb0ff;--stamp:#ff7a5c;--rule:#4e4a33;--muted:#b8b39a;color-scheme:dark}}
:root[data-theme="dark"]{--desk:#151b24;--paper:#2a2a1f;--paper2:#302f23;--ink:#efe9cf;--carbon:#8fb0ff;--stamp:#ff7a5c;--rule:#4e4a33;--muted:#b8b39a;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--desk);color:var(--ink);font-family:var(--body);font-size:1.0625rem;line-height:1.55}
.desk{GUTTER padding-block:1.5rem 3rem}
.sheet{max-width:52rem;margin:0 auto;background:var(--paper);border-radius:4px;box-shadow:0 1px 0 var(--rule),0 18px 40px -24px rgba(0,0,0,.45);position:relative;overflow:hidden}
.sheet::before{content:"";position:absolute;inset:0 0 auto;height:14px;background:radial-gradient(circle at 7px 7px,var(--desk) 3px,transparent 3.5px) 0 0/24px 14px repeat-x}
.top{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem 1rem;align-items:flex-end;padding:1.8rem 1.2rem .8rem;border-bottom:3px double var(--ink)}
.firm{font-family:var(--head);font-weight:800;font-size:1.6rem;letter-spacing:.02em;text-transform:uppercase}
.no{font-family:var(--mono);font-size:.9rem}.no b{color:var(--stamp);font-size:1.1rem}
.row{display:grid;grid-template-columns:7.5rem 1fr;border-bottom:1px solid var(--rule);min-height:2.6rem}
.row>span:first-child{font-family:var(--head);text-transform:uppercase;letter-spacing:.08em;font-size:.78rem;color:var(--muted);padding:.75rem .6rem .3rem 1.2rem;border-right:1px solid var(--rule)}
.row>.v{padding:.45rem 1.2rem .45rem .8rem;min-width:0}
.hand{font-family:var(--hand);color:var(--carbon);font-size:1.15rem;line-height:1.35}
h1{font-family:var(--head);font-weight:800;font-size:clamp(2.3rem,8vw,3.8rem);line-height:.98;text-transform:uppercase;margin:0;text-wrap:balance}
h2{font-family:var(--head);font-weight:800;text-transform:uppercase;letter-spacing:.04em;font-size:1.35rem;margin:0}
.hero{padding:1.3rem 1.2rem 1.4rem;display:flex;flex-direction:column;gap:1rem;position:relative}
.lead{max-width:34rem;color:var(--muted);font-size:1.12rem}
.stamp{position:absolute;right:1rem;top:1.1rem;transform:rotate(-11deg);border:3px solid var(--stamp);color:var(--stamp);font-family:var(--head);font-weight:800;font-size:1.25rem;letter-spacing:.12em;padding:.15rem .6rem;border-radius:6px;opacity:.85;text-transform:uppercase}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem}
.btn{display:inline-flex;flex-wrap:wrap;align-items:center;gap:.2rem .5rem;min-height:3rem;padding:.6rem 1.1rem;font-family:var(--head);font-size:1.15rem;font-weight:700;letter-spacing:.04em;text-transform:uppercase;text-decoration:none;border:2px solid var(--ink);color:var(--ink);background:transparent;border-radius:3px}
.btn.primary{background:var(--ink);color:var(--paper)}
.btn:focus-visible,summary:focus-visible{outline:3px solid var(--carbon);outline-offset:2px}
.num{font-family:var(--mono);font-variant-numeric:tabular-nums;white-space:nowrap}
.draft{outline:1px dashed var(--stamp);outline-offset:2px}
.sec{padding:1.2rem;border-top:3px double var(--ink);display:flex;flex-direction:column;gap:.9rem}
.stats{display:grid;grid-template-columns:repeat(auto-fit,minmax(13rem,1fr));gap:0;border:1px solid var(--rule)}
.st{padding:.8rem 1rem;border:1px solid var(--rule);display:flex;flex-direction:column;gap:.2rem}
.st b{font-family:var(--head);font-size:2.6rem;line-height:1;color:var(--stamp)}
.st a{font-size:.82rem;color:var(--muted)}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1.2rem}
.cols>div{min-width:0}
ul.boxes{list-style:none;margin:.5rem 0 0;padding:0;display:flex;flex-direction:column;gap:.5rem}
ul.boxes li{display:grid;grid-template-columns:1.4rem 1fr;gap:.4rem}
ul.boxes li::before{content:"\\2713";font-family:var(--hand);color:var(--carbon);font-size:1.2rem;line-height:1.2;border:1.5px solid var(--ink);width:1.1rem;height:1.1rem;display:inline-flex;align-items:center;justify-content:center;margin-top:.25rem;font-size:.9rem}
ol.steps{margin:0;padding-left:1.9rem;display:flex;flex-direction:column;gap:.6rem}
ol.steps li::marker{font-family:var(--mono);color:var(--carbon)}
.total{display:grid;grid-template-columns:1fr auto;gap:.3rem 1rem;align-items:end;border:2px solid var(--ink);padding:.9rem 1rem}
.total .lbl{font-family:var(--head);text-transform:uppercase;letter-spacing:.08em;font-size:.85rem;color:var(--muted)}
.total .amt{font-family:var(--head);font-size:3.2rem;font-weight:800;line-height:1}
.total p{grid-column:1/-1;margin:0}
.found{border:2px dashed var(--stamp);padding:.8rem 1rem;color:var(--ink)}
.found b{color:var(--stamp);font-family:var(--head);text-transform:uppercase;letter-spacing:.06em}
details{border-bottom:1px solid var(--rule);padding:.6rem 0}
summary{cursor:pointer;font-weight:600}
details p{margin:.4rem 0 0;color:var(--muted)}
.sig{display:flex;flex-wrap:wrap;justify-content:space-between;gap:.4rem 1rem;padding:1rem 1.2rem 1.4rem;border-top:1px solid var(--rule);font-size:.85rem;color:var(--muted)}
.sig .hand{font-size:1.3rem}
a{color:var(--carbon)}
p{margin:0}
""".replace("GUTTER", GUTTER)
    b = BRAND
    log_rows = "".join(f'<div class="row"><span>{e(t)}</span><span class="v hand">{"&#10007; " if k == "miss" else "&#10003; "}{e(x)}</span></div>' for t, k, x in b["log"])
    body = f"""
<div class="desk"><main class="sheet">
  <div class="top"><span class="firm" data-name>{e(b['name'])}</span><span class="no">SERVICE TICKET &nbsp;No. <b>0001</b></span></div>
  <div class="row"><span>For</span><span class="v">Service businesses in {e(b['area'])}</span></div>
  <section class="hero">
    <span class="stamp" aria-hidden="true">Answered</span>
    <h1>{e(b['h1a'])}<br>{e(b['h1b'])}</h1>
    <p class="lead">{e(b['sub'])}</p>
    <div class="ctas">
      <a class="btn primary" data-call>Call and hear it: <span class="num" data-phone>{phone_text()}</span></a>
      <a class="btn" data-book target="_blank" rel="noopener">Book a 15-minute call</a>
    </div>
  </section>
  <div class="row"><span>Example</span><span class="v">Tuesday evening, your phone</span></div>
  {log_rows}
  <div class="row"><span>Try it</span><span class="v">{e(b['check'])}</span></div>
  <section class="sec"><h2>What missed calls and old reviews cost you</h2><div class="stats">{stats_html('st')}</div></section>
  <section class="sec"><h2>Work to be done</h2><div class="cols">
    <div><b>Your calls</b><ul class="boxes">{li(b['calls'])}</ul></div>
    <div><b>Your reviews</b><ul class="boxes">{li(b['reviews'])}</ul></div></div></section>
  <section class="sec"><h2>How it starts</h2><ol class="steps">{steps_html()}</ol></section>
  <section class="sec"><h2>Total</h2>
    <div class="total"><span class="lbl">Per month</span><span class="amt num">{e(b['price'])}</span><p>{e(b['price_line'])} {e(b['minutes'])}</p></div>
    <div class="found"><b>{e(b['founding_t'])}.</b> {e(b['founding'])}</div>
    <div class="ctas"><a class="btn primary" data-book target="_blank" rel="noopener">Book a 15-minute call</a></div></section>
  <section class="sec"><h2>Notes</h2><div>{faq_html()}</div></section>
  <div class="sig"><span><span data-name>{e(b['name'])}</span> · {e(b['area_footer'])} · <span class="num" data-phone>{phone_text()}</span></span><span>Numbers above come from the studies linked under each one.</span></div>
</main></div>"""
    return head("ticket: a carbon-copy service work order", "family=Barlow+Condensed:wght@700;800&family=Barlow:wght@400;600&family=Kalam:wght@400&family=Courier+Prime&", css) + body


# ---------------------------------------------------------------- band 2: shop door glass, gold leaf + hours plate
def door():
    css = """
:root{--glass:#0f2b2c;--glass2:#123536;--gold:#d8a84a;--gold2:#f0cf7d;--vinyl:#f5f2ea;--plate:#101414;--ink:#e9efe9;--muted:#a9bcb7;--line:#2a4a49;--red:#e0624a;
  --display:"DM Serif Display",Georgia,serif;--body:"Work Sans",Arial,sans-serif;--sign:"Oswald","Arial Narrow",sans-serif;color-scheme:dark}
/* Single-look design on purpose: a dark glass door at dusk; every colour set explicitly. */
*{box-sizing:border-box}
body{background:var(--glass);color:var(--ink);font-family:var(--body);font-size:1.05rem;line-height:1.6}
.wrap{max-width:62rem;margin:0 auto;GUTTER}
.door{background:linear-gradient(160deg,var(--glass2),var(--glass) 55%);border-bottom:1px solid var(--line)}
.door .wrap{padding-block:2.2rem 2.6rem;display:grid;grid-template-columns:minmax(0,1.35fr) minmax(0,1fr);gap:2rem;align-items:start}
@media (max-width:760px){.door .wrap{grid-template-columns:1fr}}
.gold{font-family:var(--display);color:var(--gold);text-shadow:0 1px 0 #7a5418,0 0 1px var(--gold2)}
.since{font-family:var(--sign);letter-spacing:.3em;text-transform:uppercase;color:var(--gold);font-size:.8rem;border-top:1px solid var(--gold);border-bottom:1px solid var(--gold);display:inline-block;padding:.2rem .1rem}
h1{margin:.7rem 0 0;font-size:clamp(2.5rem,7.5vw,4.4rem);line-height:1.02;font-weight:400;text-wrap:balance}
.lead{color:var(--muted);max-width:32rem;margin-top:1rem;font-size:1.12rem}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.4rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;min-height:3rem;padding:.6rem 1.15rem;border-radius:999px;text-decoration:none;font-weight:600;border:1.5px solid var(--gold);color:var(--gold2)}
.btn.primary{background:var(--gold);color:#1a1405;border-color:var(--gold)}
.btn:focus-visible,summary:focus-visible{outline:3px solid var(--vinyl);outline-offset:2px}
.num{font-variant-numeric:tabular-nums;font-family:var(--sign);letter-spacing:.04em;white-space:nowrap}
.draft{outline:1px dashed var(--red);outline-offset:3px}
.plate{background:var(--plate);border-radius:10px;padding:1.2rem 1.3rem 1.3rem;box-shadow:inset 0 0 0 2px #2b2f2f,0 20px 40px -24px #000;font-family:var(--sign);color:var(--vinyl)}
.plate h2{font-family:var(--sign);font-weight:500;letter-spacing:.35em;text-align:center;font-size:1.05rem;margin:0 0 .6rem;color:var(--vinyl)}
.plate dl{margin:0;display:grid;grid-template-columns:auto 1fr;gap:.25rem 1rem;font-size:1.05rem;letter-spacing:.06em}
.plate dt{text-transform:uppercase;color:var(--muted)}
.plate dd{margin:0;text-align:right}
.plate .open{margin-top:.9rem;text-align:center;border:2px solid var(--red);color:var(--red);border-radius:6px;padding:.25rem;letter-spacing:.2em;font-weight:600}
.plate small{display:block;margin-top:.7rem;color:var(--muted);letter-spacing:.02em;font-family:var(--body);font-size:.85rem;text-align:center}
section{padding-block:2.6rem}
h2.t{font-family:var(--display);font-weight:400;color:var(--gold);font-size:clamp(1.7rem,4.5vw,2.4rem);margin:0 0 1.2rem;text-wrap:balance}
.decals{display:grid;grid-template-columns:repeat(auto-fit,minmax(11rem,1fr));gap:1.2rem}
.decal{display:flex;flex-direction:column;align-items:flex-start;gap:.35rem}
.decal b{font-family:var(--display);font-weight:400;font-size:3.2rem;line-height:1;color:var(--vinyl);border-bottom:2px solid var(--gold);padding-bottom:.2rem}
.decal a{color:var(--muted);font-size:.82rem}
.panes{display:grid;grid-template-columns:repeat(auto-fit,minmax(17rem,1fr));gap:1px;background:var(--line);border:1px solid var(--line);border-radius:8px;overflow:hidden}
.panes>div{background:var(--glass);padding:1.2rem;min-width:0}
.panes h3{font-family:var(--sign);text-transform:uppercase;letter-spacing:.2em;font-weight:500;color:var(--gold);font-size:.95rem;margin:0 0 .6rem}
.panes ul{margin:0;padding-left:1.1rem;display:flex;flex-direction:column;gap:.45rem}
ol.steps{margin:0;padding-left:1.9rem;display:flex;flex-direction:column;gap:.7rem}
ol.steps li::marker{font-family:var(--display);color:var(--gold)}
.price{display:flex;flex-wrap:wrap;gap:.3rem 1.2rem;align-items:baseline}
.price b{font-family:var(--display);font-weight:400;font-size:4rem;line-height:1;color:var(--gold)}
.price span{color:var(--muted);max-width:28rem}
.found{margin-top:1.2rem;border:1px solid var(--gold);border-radius:8px;padding:1rem 1.2rem}
.found h3{font-family:var(--display);font-weight:400;color:var(--gold2);margin:0 0 .3rem;font-size:1.3rem}
details{border-bottom:1px solid var(--line);padding:.75rem 0}
summary{cursor:pointer;font-weight:600}
details p{margin:.4rem 0 0;color:var(--muted)}
footer{padding-block:2rem;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line)}
a{color:var(--gold2)}
p{margin:0}
.check{margin-top:1.4rem;color:var(--muted);font-style:italic;max-width:32rem}
""".replace("GUTTER", GUTTER)
    b = BRAND
    days = [("Mon", "10 AM - 6 PM"), ("Tue", "10 AM - 6 PM"), ("Wed", "10 AM - 6 PM"), ("Thu", "10 AM - 6 PM"), ("Fri", "10 AM - 6 PM"), ("Sat", "10 AM - 6 PM"), ("Sun", "Closed")]
    hours = "".join(f"<dt>{d}</dt><dd>{h}</dd>" for d, h in days)
    body = f"""
<header class="door"><div class="wrap">
  <div>
    <span class="since" data-name>{e(b['name'])}</span>
    <h1 class="gold">{e(b['h1a'])}<br>{e(b['h1b'])}</h1>
    <p class="lead">For service businesses in {e(b['area'])}. {e(b['sub'])}</p>
    <div class="ctas">
      <a class="btn primary" data-call>Call and hear it: <span class="num" data-phone>{phone_text()}</span></a>
      <a class="btn" data-book target="_blank" rel="noopener">Book a 15-minute call</a>
    </div>
    <p class="check">{e(b['check'])}</p>
  </div>
  <aside class="plate" aria-label="Example: a shop's hours sign, and the phone line that keeps answering after closing">
    <h2>HOURS</h2>
    <dl>{hours}</dl>
    <div class="open">PHONE ANSWERED 24/7</div>
    <small>Your shop closes. Your phone doesn't. At 6:48 PM tonight, a "no heat upstairs" call gets booked for Wed 8:00 AM.</small>
  </aside>
</div></header>
<section><div class="wrap"><h2 class="t">What missed calls and old reviews cost you</h2><div class="decals">{stats_html('decal')}</div></div></section>
<section style="padding-top:0"><div class="wrap"><h2 class="t">What you get</h2><div class="panes">
  <div><h3>Your calls</h3><ul>{li(b['calls'])}</ul></div>
  <div><h3>Your reviews</h3><ul>{li(b['reviews'])}</ul></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2 class="t">How it starts</h2><ol class="steps">{steps_html()}</ol></div></section>
<section style="padding-top:0"><div class="wrap"><h2 class="t">One plan, one price</h2>
  <div class="price"><b class="num" style="font-family:var(--display)">{e(b['price'])}</b><span>{e(b['price_line'])} {e(b['minutes'])}</span></div>
  <div class="found"><h3>{e(b['founding_t'])}</h3><p>{e(b['founding'])}</p></div>
  <div class="ctas"><a class="btn primary" data-book target="_blank" rel="noopener">Book a 15-minute call</a></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2 class="t">Questions</h2>{faq_html()}</div></section>
<div class="wrap"><footer><span data-name>{e(b['name'])}</span> · {e(b['area_footer'])} · <span class="num" data-phone>{phone_text()}</span><br>Numbers on this page come from the studies linked under each one.</footer></div>"""
    return head("door: shop door glass with gold-leaf letters and an hours plate", "family=DM+Serif+Display&family=Work+Sans:wght@400;600&family=Oswald:wght@500;600&", css) + body


# ---------------------------------------------------------------- band 3: phone lock screen, notifications stacking
def lockscreen():
    css = """
:root{--sky1:#c7c0ef;--sky2:#f3d9e6;--sky3:#ffc9a8;--ink:#18232e;--muted:#4f5d6a;--card:rgba(255,255,255,.42);--cardline:rgba(24,35,46,.08);--accent:#0f7a6c;--accent-ink:#ffffff;--warn:#b5432c;--panel:#ffffff;--line:#e3e7ea;
  --clock:"Outfit","Avenir Next",Arial,sans-serif;--body:"Nunito Sans",Arial,sans-serif}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--sky1:#2b2340;--sky2:#1b2233;--sky3:#13202a;--ink:#eef2f5;--muted:#b0bcc6;--card:rgba(30,38,52,.78);--cardline:rgba(255,255,255,.08);--accent:#4fd1bd;--accent-ink:#0b1a17;--warn:#ff8f73;--panel:#161d27;--line:#273241;color-scheme:dark}}
:root[data-theme="dark"]{--sky1:#2b2340;--sky2:#1b2233;--sky3:#13202a;--ink:#eef2f5;--muted:#b0bcc6;--card:rgba(30,38,52,.78);--cardline:rgba(255,255,255,.08);--accent:#4fd1bd;--accent-ink:#0b1a17;--warn:#ff8f73;--panel:#161d27;--line:#273241;color-scheme:dark}
*{box-sizing:border-box}
body{background:var(--panel);color:var(--ink);font-family:var(--body);font-size:1.05rem;line-height:1.6}
.w{background:var(--sky2)}
.sky{background:linear-gradient(180deg,var(--sky1),var(--sky2) 55%,var(--sky3))}
.wrap{max-width:60rem;margin:0 auto;GUTTER}
.sky .wrap{padding-block:1.6rem 2.4rem;display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:2rem;align-items:center}
@media (max-width:760px){.sky .wrap{grid-template-columns:1fr}}
.lock{text-align:center;display:flex;flex-direction:column;gap:.7rem;max-width:24rem;justify-self:center;width:100%}
.date{font-weight:600;color:var(--muted);letter-spacing:.02em}
.clock{font-family:var(--clock);font-weight:300;font-size:clamp(4.4rem,18vw,6.4rem);line-height:.9;letter-spacing:-.03em}
.note{text-align:left;background:var(--card);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);border:1px solid var(--cardline);border-radius:18px;padding:.7rem .9rem;display:grid;grid-template-columns:2.1rem 1fr auto;gap:.1rem .65rem;align-items:start}
.note i{grid-row:span 2;width:2.1rem;height:2.1rem;border-radius:9px;background:var(--accent);display:flex;align-items:center;justify-content:center}
.note i.miss{background:var(--warn)}
.note .who{font-weight:700;font-size:.92rem}
.note .when{font-size:.78rem;color:var(--muted)}
.note .txt{grid-column:2/4;font-size:.95rem;min-width:0}
@media (prefers-reduced-motion:no-preference){.note{animation:drop .5s ease-out both}.note:nth-child(4){animation-delay:.15s}.note:nth-child(5){animation-delay:.3s}.note:nth-child(6){animation-delay:.45s}}
@keyframes drop{from{transform:translateY(-6px);opacity:.4}to{transform:none;opacity:1}}
.pitch{display:flex;flex-direction:column;gap:1rem}
.brand{font-family:var(--clock);font-weight:600;font-size:1.1rem;color:var(--accent)}
h1{font-family:var(--clock);font-weight:600;font-size:clamp(2.2rem,6vw,3.3rem);line-height:1.05;margin:0;text-wrap:balance;letter-spacing:-.01em}
.lead{color:var(--muted);font-size:1.12rem;max-width:30rem}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem}
.btn{display:inline-flex;align-items:center;gap:.5rem;min-height:3rem;padding:.6rem 1.2rem;border-radius:14px;text-decoration:none;font-weight:700;border:1.5px solid var(--ink);color:var(--ink)}
.btn.primary{background:var(--accent);border-color:var(--accent);color:var(--accent-ink)}
.btn:focus-visible,summary:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
.num{font-variant-numeric:tabular-nums;white-space:nowrap}
.draft{outline:1px dashed var(--warn);outline-offset:3px}
.check{font-size:.95rem;color:var(--muted)}
section{padding-block:2.6rem}
h2{font-family:var(--clock);font-weight:600;font-size:clamp(1.6rem,4.2vw,2.2rem);margin:0 0 1.2rem;text-wrap:balance}
.widgets{display:grid;grid-template-columns:repeat(auto-fit,minmax(11.5rem,1fr));gap:.9rem}
.w{background:var(--sky2);border-radius:22px;padding:1.1rem;display:flex;flex-direction:column;gap:.3rem;min-width:0}
.w b{font-family:var(--clock);font-weight:600;font-size:2.6rem;line-height:1;color:var(--accent)}
.w a{font-size:.8rem;color:var(--muted)}
.apps{display:grid;grid-template-columns:repeat(auto-fit,minmax(16rem,1fr));gap:1rem}
.apps>div{border:1px solid var(--line);border-radius:22px;padding:1.2rem;min-width:0}
.apps h3{margin:0 0 .5rem;font-family:var(--clock);font-weight:600;font-size:1.2rem}
.apps ul{margin:0;padding-left:1.1rem;display:flex;flex-direction:column;gap:.45rem}
ol.steps{margin:0;padding-left:1.9rem;display:flex;flex-direction:column;gap:.7rem}
ol.steps li::marker{font-family:var(--clock);font-weight:600;color:var(--accent)}
.price{display:flex;flex-wrap:wrap;align-items:baseline;gap:.3rem 1rem}
.price b{font-family:var(--clock);font-weight:600;font-size:3.6rem;line-height:1}
.price span{color:var(--muted)}
.found{margin-top:1rem;background:var(--sky2);border-radius:22px;padding:1rem 1.2rem}
.found h3{margin:0 0 .2rem;font-family:var(--clock);font-weight:600}
.found + .ctas{margin-top:1rem}
details{border-bottom:1px solid var(--line);padding:.75rem 0}
summary{cursor:pointer;font-weight:700}
details p{margin:.4rem 0 0;color:var(--muted)}
footer{padding-block:2rem;color:var(--muted);font-size:.85rem;border-top:1px solid var(--line)}
a{color:var(--accent)}
p{margin:0}
""".replace("GUTTER", GUTTER)
    b = BRAND
    icon = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2a1 1 0 0 1 1-.25 11.4 11.4 0 0 0 3.6.57 1 1 0 0 1 1 1V20a1 1 0 0 1-1 1A17 17 0 0 1 3 4a1 1 0 0 1 1-1h3.5a1 1 0 0 1 1 1c0 1.25.2 2.45.57 3.57a1 1 0 0 1-.25 1z"/></svg>'
    star = '<svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true"><path fill="#fff" d="M12 2.5l2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6L2.5 9.4l6.6-.8z"/></svg>'
    body = f"""
<header class="sky"><div class="wrap">
  <div class="lock" role="img" aria-label="Example: an owner's phone lock screen at 9:16 PM showing a missed call, a booked job and a new review">
    <span class="date">Tuesday, October 27</span>
    <span class="clock num">9:16</span>
    <div class="note"><i class="miss">{icon}</i><span class="who">Before: Missed call</span><span class="when">6:48 PM</span><span class="txt">Rang out. The caller tried the next company.</span></div>
    <div class="note"><i>{icon}</i><span class="who" data-name>{e(b['name'])}</span><span class="when">6:49 PM</span><span class="txt">Booked: no heat upstairs, Wed 8:00 AM. Details in your email.</span></div>
    <div class="note"><i>{icon}</i><span class="who" data-name>{e(b['name'])}</span><span class="when">9:15 PM</span><span class="txt">New lead: quote for a water heater. Name and number sent.</span></div>
    <div class="note"><i>{star}</i><span class="who">Review reply ready</span><span class="when">now</span><span class="txt">A new 5-star review came in. Your reply is drafted. Tap to approve.</span></div>
  </div>
  <div class="pitch">
    <span class="brand" data-name>{e(b['name'])}</span>
    <h1>{e(b['h1a'])} {e(b['h1b'])}</h1>
    <p class="lead">For service businesses in {e(b['area'])}. {e(b['sub'])}</p>
    <div class="ctas">
      <a class="btn primary" data-call>Call and hear it: <span class="num" data-phone>{phone_text()}</span></a>
      <a class="btn" data-book target="_blank" rel="noopener">Book a 15-minute call</a>
    </div>
    <p class="check">{e(b['check'])}</p>
  </div>
</div></header>
<section><div class="wrap"><h2>What missed calls and old reviews cost you</h2><div class="widgets">{stats_html('w')}</div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>What you get</h2><div class="apps">
  <div><h3>Your calls</h3><ul>{li(b['calls'])}</ul></div>
  <div><h3>Your reviews</h3><ul>{li(b['reviews'])}</ul></div></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>How it starts</h2><ol class="steps">{steps_html()}</ol></div></section>
<section style="padding-top:0"><div class="wrap"><h2>One plan, one price</h2>
  <div class="price"><b class="num">{e(b['price'])}</b><span>{e(b['price_line'])} {e(b['minutes'])}</span></div>
  <div class="found"><h3>{e(b['founding_t'])}</h3><p>{e(b['founding'])}</p></div>
  <div class="ctas"><a class="btn primary" data-book target="_blank" rel="noopener">Book a 15-minute call</a></div></div></section>
<section style="padding-top:0"><div class="wrap"><h2>Questions</h2>{faq_html()}</div></section>
<div class="wrap"><footer><span data-name>{e(b['name'])}</span> · {e(b['area_footer'])} · <span class="num" data-phone>{phone_text()}</span><br>Numbers on this page come from the studies linked under each one.</footer></div>"""
    return head("lockscreen: a phone lock screen with notifications stacking up", "family=Outfit:wght@300;600&family=Nunito+Sans:wght@400;700&", css) + body


BANDS = {"ticket": ticket, "door": door, "lockscreen": lockscreen}


def standalone(frag):
    end = frag.index("</style>") + len("</style>")
    return ('<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
            'body{margin:0}img{max-width:100%}[hidden]{display:none!important}</style>\n'
            + frag[:end] + "\n</head>\n<body>" + frag[end:] + "</body>\n</html>\n")


def build():
    OUT.mkdir(exist_ok=True)
    cfg = json.dumps({k: BRAND[k] for k in ("name", "phone", "booking")})
    for band, fn in BANDS.items():
        frag = fn() + "\n" + (SCRIPT % cfg) + "\n"
        (OUT / f"{band}.html").write_text(frag)
        (OUT / f"{band}.standalone.html").write_text(standalone(frag))
        print("BUILT", band)


def measure():
    sys.path.insert(0, str(pathlib.Path("/home/user/Mymobileworld/.claude/skills/thumbnail-looks/scripts")))
    from looks import cells, shared as skill_shared  # the skill's own cell grid and sameness score
    from PIL import Image
    from playwright.sync_api import sync_playwright
    shots = {}
    pages = dict(BANDS)
    pages["v1-calllog"] = None
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium")
        for band in pages:
            src = (HERE / "index.html") if band == "v1-calllog" else (OUT / f"{band}.standalone.html")
            for vw, vh, tag in ((390, 844, "phone"), (1280, 800, "desktop")):
                for scheme in ("light", "dark"):
                    pg = br.new_page(viewport={"width": vw, "height": vh}, color_scheme=scheme)
                    pg.goto(src.resolve().as_uri()); pg.wait_for_timeout(900)
                    sw = pg.evaluate("document.documentElement.scrollWidth")
                    path = OUT / f"_{band}_{tag}_{scheme}.png"
                    pg.screenshot(path=str(path))
                    shots[(band, tag, scheme)] = (path, sw, vw)
                    pg.close()
        br.close()
    bad = [(k, sw) for k, (_, sw, vw) in shots.items() if sw > vw]
    print("side-scroll:", "none" if not bad else bad)

    def share(a, b, grid):
        return skill_shared(cells(a, grid), cells(b, grid))
    names = list(pages)
    worst = 0
    for tag, grid in (("phone", (18, 32)), ("desktop", (32, 18))):
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                s = share(shots[(names[i], tag, "light")][0], shots[(names[j], tag, "light")][0], grid)
                worst = max(worst, s)
                print(f"shared {tag:7s} {names[i]:10s} vs {names[j]:10s} {s:.2f}")
    # contact sheet: phone light row, phone dark row
    row = []
    for scheme in ("light", "dark"):
        ims = [Image.open(shots[(n, 'phone', scheme)][0]) for n in names]
        w = sum(i.width for i in ims) + 20 * (len(ims) - 1)
        sheet = Image.new("RGB", (w, max(i.height for i in ims)), "white")
        x = 0
        for im in ims:
            sheet.paste(im, (x, 0)); x += im.width + 20
        row.append(sheet)
    full = Image.new("RGB", (row[0].width, row[0].height * 2 + 20), "white")
    full.paste(row[0], (0, 0)); full.paste(row[1], (0, row[0].height + 20))
    full.save(OUT / "_looks_sheet.png")
    dsk = [Image.open(shots[(n, 'desktop', 'light')][0]).resize((640, 400)) for n in names]
    d = Image.new("RGB", (640 * 2 + 20, 400 * 2 + 20), "white")
    for k, im in enumerate(dsk):
        d.paste(im, ((k % 2) * 660, (k // 2) * 420))
    d.save(OUT / "_looks_desktop.png")
    print(f"worst shared {worst:.2f} (limit 0.30)")
    print("LOOKS_OK" if worst <= 0.30 and not bad else "LOOKS_FAIL")


def pick(band):
    frag = (OUT / f"{band}.html").read_text()
    (HERE / "page.html").write_text(frag)
    (HERE / "index.html").write_text(standalone(frag))
    print("PICKED", band)


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "build"
    {"build": build, "measure": measure}.get(cmd, lambda: pick(sys.argv[2]))()
