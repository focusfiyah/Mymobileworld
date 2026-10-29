"""Always Answered landing page, round 4 (Ralph 2026-10-29: "too wordy and need some graphics upgrades").

One page, built with the web-design-stack skill: same royal-blue world and facts as round 3 (looks.py "door"),
about half the words, drawn icons, a 100-call chart, a real photo with the call log laid over it, a coupon.

Usage: python3 build.py            writes /home/user/always-answered/index.html (+ a copy next to this file)
Edit TEXT / PLANS / FAQ below to change the words. Photo + licence: always-answered/img/SOURCES.md.
"""
import html, json, pathlib

HERE = pathlib.Path(__file__).parent
SITE = pathlib.Path("/home/user/always-answered")
e = html.escape

CONFIG = {"name": "Always Answered",
          "phone": "",  # the 516 Twilio line, once bought; call buttons stay hidden until then
          "booking": "https://calendly.com/teamrrgrp/30min"}  # 15-minute event (link kept /30min)

STATS = [("78%", "give up after nobody picks up.", "CallRail, 2025",
          "https://beside.com/blog/missed-calls-cost-small-business"),
         ("21%", "call the next business instead.", "CallRail, 2025",
          "https://beside.com/blog/missed-calls-cost-small-business")]
SRC44 = ("Invoca, 70 million calls, 2026", "https://justcall.io/blog/missed-call-statistics.html")
SRC74 = ("BrightLocal, 2026", "https://www.brightlocal.com/research/local-consumer-review-survey/")

CALLS = [("phone", "Answered 24/7 on your number"),
         ("forward", "Passed to you in your hours"),
         ("mail", "Bookings emailed in a minute"),
         ("list", "A Monday report of every call")]
REVIEWS = ["After every job: email, WhatsApp or counter card",
           "No fake reviews, ever"]
STEPS = [("calendar", "Book a 15-minute call", "Share your services and hours."),
         ("ear", "Hear it first", "We build it. You test it first."),
         ("forward", "Turn on forwarding", "Same number. We send the steps.")]
PLANS = [("Calls Only", "$197", "$297", False, ["Every call answered, 24/7", "Calls passed to you in your hours",
                                               "Bookings emailed in a minute", "Monday call report", "200 minutes a month"]),
         ("Front Desk", "$397", "$497", True, ["Everything in Calls Only", "500 minutes a month",
                                              "Review requests after every job", "Monthly review report"]),
         ("Pro", "$597", "$497", False, ["Everything in Front Desk", "1,000 minutes a month", "2 phone lines",
                                         "Review replies you approve", "Monthly check-in call"])]
FAQ = [("Does it sound like a robot?", "No. Hear it on a 15-minute call."),
       ("Does it pretend to be a person?", "No. It says it's your assistant and that calls may be recorded. Asked, it says it's AI."),
       ("Will it call my customers?", "No. It only answers calls.")]
LOG = [("6:48 PM", "Call answered", "“No heat upstairs.”"),
       ("6:49 PM", "Job booked", "Wed 8:00 AM. Sent to you."),
       ("9:15 PM", "Call answered", "Water heater quote. Number sent.")]

# one icon set, 24px grid, 1.75 stroke, round joins (authored, currentColor)
ICONS = {
    "phone": '<path d="M5.5 3.5h3l1.6 4.2-2 1.3a11 11 0 0 0 5.9 5.9l1.3-2 4.2 1.6v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 3.5 5.7a2 2 0 0 1 2-2.2z"/>',
    "forward": '<path d="M5.5 3.5h3l1.6 4.2-2 1.3a11 11 0 0 0 5.9 5.9l1.3-2 4.2 1.6v3a2 2 0 0 1-2.2 2A16.5 16.5 0 0 1 3.5 5.7a2 2 0 0 1 2-2.2z"/><path d="M14.5 6.5h6M17.5 3.5l3 3-3 3"/>',
    "mail": '<rect x="3" y="5" width="18" height="14" rx="2.5"/><path d="m3.5 7 8.5 6 8.5-6"/>',
    "list": '<rect x="4.5" y="3.5" width="15" height="17" rx="2.5"/><path d="M8.5 8.5h7M8.5 12h7M8.5 15.5h4"/>',
    "calendar": '<rect x="3.5" y="5" width="17" height="15.5" rx="2.5"/><path d="M3.5 10h17M8 3v4M16 3v4"/><path d="M9.5 14.5l1.7 1.7 3.3-3.4"/>',
    "ear": '<path d="M4 15v-3a8 8 0 0 1 16 0v3"/><rect x="3.5" y="13.5" width="4" height="6.5" rx="1.6"/><rect x="16.5" y="13.5" width="4" height="6.5" rx="1.6"/>',
    "check": '<path d="M5 12.5l4.2 4.2L19 7"/>',
    "chev": '<path d="M7 10l5 5 5-5"/>',
    "star": '<path d="M12 3.4l2.6 5.4 5.9.8-4.3 4.1 1 5.9L12 16.8l-5.3 2.8 1-5.9-4.3-4.1 5.9-.8z"/>',
    "arrow": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}
SPRITE = '<svg width="0" height="0" style="position:absolute" aria-hidden="true">' + "".join(
    f'<symbol id="i-{k}" viewBox="0 0 24 24">{v}</symbol>' for k, v in ICONS.items()) + "</svg>"


def ic(name, cls="ic"):
    return f'<svg class="{cls}" aria-hidden="true"><use href="#i-{name}"/></svg>'


MARK = ('<svg class="mark" viewBox="0 0 40 40" aria-hidden="true"><rect width="40" height="40" rx="11" fill="#1f4fd8"/>'
        '<g fill="none" stroke="#fff" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" transform="translate(8 8)">'
        + ICONS["phone"] + '</g><circle cx="30.5" cy="9.5" r="5.5" fill="#7ee0a9" stroke="#1f4fd8" stroke-width="2"/></svg>')

CSS = """
:root{--navy:#0b1e5b;--navy2:#132a76;--royal:#1f4fd8;--royal2:#5b84ff;--sky:#e8eefc;--paper:#fff;--wash:#f4f7fd;
  --ink:#101a33;--muted:#4a5878;--line:#d5def3;--onblue:#fff;--onblue2:#c9d6fb;--miss:#ff8a6b;--ok:#7ee0a9;--star:#f5b301;
  --display:"DM Serif Display",Georgia,serif;--body:"Work Sans",system-ui,sans-serif;
  --ease-smooth-out:cubic-bezier(0.22,1,0.36,1);--duration-quick:150ms;--duration-fast:250ms;
  --acc-expand:250ms;--acc-collapse:250ms;--acc-chevron:250ms;--acc-ease:cubic-bezier(0.22,1,0.36,1);
  --sh-1:0 1px 2px rgba(0,0,0,.06),0 4px 14px -6px rgba(0,0,0,.18);
  --sh-2:0 2px 4px rgba(0,0,0,.08),0 18px 40px -18px rgba(0,0,0,.45);color-scheme:light}
/* Single light look on purpose (Ralph 2026-10-28: royal blue reads trustworthy); every colour set explicitly. */
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scrollbar-color:var(--royal) var(--wash)}
body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--body);font-size:1.0625rem;line-height:1.55;-webkit-font-smoothing:antialiased}
::selection{background:var(--royal);color:#fff}
p,h1,h2,h3,ul,ol,figure{margin:0}
p{text-wrap:pretty}
a{color:var(--royal);text-underline-offset:.18em}
.wrap{max-width:68rem;margin:0 auto;GUTTER}
.ic{width:1.35rem;height:1.35rem;flex:none;fill:none;stroke:currentColor;stroke-width:1.75;stroke-linecap:round;stroke-linejoin:round}
.mark{width:2.25rem;height:2.25rem;flex:none}
.num{font-variant-numeric:tabular-nums}
h1,h2{font-family:var(--display);font-weight:400;line-height:1.04;text-wrap:balance;letter-spacing:-.01em}
h2.t{color:var(--navy);font-size:clamp(1.9rem,4.6vw,2.7rem);margin-bottom:1.6rem}
section{padding-block:clamp(3rem,8vw,5.5rem)}
.btn{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:.5rem;min-height:3rem;padding:.65rem 1.3rem;border-radius:999px;
  text-decoration:none;font-weight:600;color:var(--royal);background:var(--paper);box-shadow:inset 0 0 0 1.5px var(--royal);
  transition:background-color var(--duration-quick) ease-out,color var(--duration-quick) ease-out,scale var(--duration-quick) ease-out}
.btn.primary{background:var(--royal);color:#fff;box-shadow:0 1px 2px rgba(0,0,0,.2),0 8px 20px -10px rgba(0,0,0,.35)}
.btn .ic{width:1.15rem;height:1.15rem;stroke-width:2}
@media (hover:hover){.btn:hover{background:var(--sky)}.btn.primary:hover{background:var(--navy)}}
.btn:active{scale:.96}
.btn:focus-visible,.acc-head:focus-visible,a:focus-visible{outline:3px solid var(--royal2);outline-offset:3px}
[data-call][hidden]{display:none!important}

/* top: the problem */
.top{background:var(--navy);color:var(--onblue)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:1rem;padding-block:1.1rem}
.logo{display:flex;align-items:center;gap:.6rem;color:#fff;text-decoration:none;font-family:var(--display);font-size:1.35rem}
.bar .btn{min-height:2.75rem;padding:.5rem 1.05rem;background:transparent;color:#fff;box-shadow:inset 0 0 0 1.5px rgba(201,214,251,.55)}
@media (hover:hover){.bar .btn:hover{background:var(--navy2)}}
.hook{display:grid;grid-template-columns:minmax(0,1.25fr) minmax(0,1fr);gap:clamp(2rem,5vw,4rem);align-items:center;padding-block:clamp(2rem,6vw,4rem) clamp(2.5rem,6vw,4.5rem)}
.hook h1{font-size:clamp(2.4rem,6.4vw,4.3rem);max-width:15ch}
.side{display:flex;flex-wrap:wrap;gap:1.2rem 2.4rem;margin-top:2rem}
.side div{display:flex;align-items:baseline;gap:.6rem;max-width:17rem}
.side b{font-family:var(--display);font-weight:400;font-size:2.6rem;line-height:1;color:var(--miss)}
.side span{color:var(--onblue2);font-size:1rem;line-height:1.4}
.chart{background:var(--navy2);border-radius:22px;padding:1.4rem;box-shadow:0 30px 60px -30px rgba(0,0,0,.6);max-width:24rem;justify-self:end;width:100%}
.dots{display:grid;grid-template-columns:repeat(10,1fr);gap:7px}
.dots i{aspect-ratio:1;border-radius:50%;background:rgba(201,214,251,.22)}
.dots i.m{background:var(--miss)}
.chart p{margin-top:1.1rem;display:flex;align-items:baseline;gap:.6rem;color:var(--onblue2);line-height:1.35}
.chart p b{font-family:var(--display);font-weight:400;font-size:2.6rem;line-height:1;color:#fff}
.src{display:block;margin-top:.35rem;font-size:.78rem;color:var(--onblue2)}
.src a{color:var(--onblue2)}
.cost{background:var(--royal);color:#fff}
.cost .wrap{display:flex;flex-wrap:wrap;align-items:center;gap:.8rem 1.4rem;padding-block:1.6rem}
.term{display:flex;flex-direction:column;line-height:1.15}
.term b{font-family:var(--display);font-weight:400;font-size:clamp(2rem,5vw,2.8rem)}
.term span{font-size:.92rem;color:var(--onblue2)}
.op{font-family:var(--display);font-size:2rem;color:var(--onblue2)}
.term.total b{color:#fff}
.cost small{flex-basis:100%;color:var(--onblue2);font-size:.82rem}

/* solution */
.hero{background:linear-gradient(180deg,var(--sky),var(--paper) 85%);padding-bottom:clamp(2rem,5vw,3rem)}
.hero .wrap{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1.15fr);gap:clamp(2rem,5vw,4rem);align-items:center}
.hero h2{color:var(--navy);font-size:clamp(2.4rem,6vw,4rem)}
.lead{color:var(--muted);font-size:1.15rem;max-width:30rem;margin-top:1.1rem;text-wrap:pretty}
.ctas{display:flex;flex-wrap:wrap;gap:.7rem;margin-top:1.7rem}
.shot{position:relative;padding-bottom:3.5rem}
.shot img{display:block;width:100%;height:auto;aspect-ratio:1600/924;object-fit:cover;border-radius:24px;outline:1px solid rgba(0,0,0,.1);outline-offset:-1px;box-shadow:var(--sh-2)}
.stack{position:absolute;left:-2.2rem;bottom:0;width:min(21rem,82%);display:flex;flex-direction:column;gap:.55rem}
.note{display:grid;grid-template-columns:2.25rem 1fr;gap:.15rem .7rem;align-items:center;background:rgba(255,255,255,.94);border-radius:20px;padding:.7rem .85rem;
  box-shadow:0 1px 2px rgba(0,0,0,.1),0 14px 30px -14px rgba(0,0,0,.5);-webkit-backdrop-filter:blur(10px);backdrop-filter:blur(10px)}
.note .mark{grid-row:span 2;width:2.25rem;height:2.25rem}
.note .h{display:flex;justify-content:space-between;gap:.5rem;font-size:.82rem;color:var(--muted)}
.note .h b{color:var(--ink);font-weight:600}
.note p{font-size:.95rem;line-height:1.35;color:var(--ink)}
.note.ok .h b::before{content:"";display:inline-block;width:.5rem;height:.5rem;border-radius:50%;background:#1f9d5c;margin-right:.4rem;vertical-align:.08em}

/* what you get */
.get{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);gap:clamp(1.5rem,4vw,3rem);align-items:start}
.get h3{font-family:var(--display);font-weight:400;color:var(--navy);font-size:1.6rem;margin-bottom:1rem}
.rows{list-style:none;padding:0;display:flex;flex-direction:column}
.rows li{display:flex;gap:.9rem;align-items:center;padding:.85rem 0;border-bottom:1px solid var(--line)}
.rows li:first-child{border-top:1px solid var(--line)}
.rows .ic{color:var(--royal);width:2.6rem;height:2.6rem;padding:.6rem;border-radius:12px;background:var(--sky)}
.panel{background:var(--wash);border-radius:24px;padding:1.4rem}
.msg{background:#fff;border-radius:18px 18px 18px 6px;padding:1rem 1.1rem;box-shadow:var(--sh-1);max-width:22rem}
.msg .who{font-size:.8rem;color:var(--muted);margin-bottom:.3rem}
.msg .stars{display:flex;gap:.2rem;margin-top:.7rem}
.msg .stars .ic{width:1.6rem;height:1.6rem;fill:var(--star);stroke:var(--star);stroke-width:1}
.panel ul{margin-top:1.2rem;padding:0;list-style:none;display:flex;flex-direction:column;gap:.55rem}
.panel li{display:flex;gap:.55rem;align-items:flex-start}
.panel li .ic{color:var(--royal);margin-top:.12rem;stroke-width:2}
.fact{margin-top:1.2rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--muted);font-size:.95rem;display:flex;gap:.6rem;align-items:baseline}
.fact b{font-family:var(--display);font-weight:400;font-size:2rem;color:var(--royal);line-height:1}
.fact a{font-size:.8rem;color:var(--muted)}

/* steps */
section.wash{background:var(--wash)}
.steps{list-style:none;padding:0;display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1.5rem;position:relative}
.steps li:not(:last-child)::after{content:"";position:absolute;top:1.75rem;left:4.25rem;right:calc(-1.5rem + .75rem);border-top:2px dashed #b9c8ef}
.steps li{position:relative;display:flex;flex-direction:column;align-items:flex-start;gap:.4rem}
.steps .ic{width:3.5rem;height:3.5rem;padding:.85rem;border-radius:50%;background:var(--royal);color:#fff;stroke-width:1.75;box-shadow:0 0 0 6px var(--wash)}
.steps b{font-size:1.1rem;color:var(--navy);margin-top:.6rem}
.steps span{color:var(--muted)}

/* plans */
.plans{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:1rem;align-items:stretch}
.plan{position:relative;display:flex;flex-direction:column;gap:.55rem;background:#fff;border-radius:20px;padding:1.5rem 1.35rem;box-shadow:0 0 0 1px var(--line),var(--sh-1)}
.plan.pop{box-shadow:0 0 0 2px var(--royal),0 24px 50px -24px rgba(0,0,0,.28)}
.badge{position:absolute;top:-.8rem;left:1.35rem;background:var(--royal);color:#fff;font-size:.75rem;font-weight:600;letter-spacing:.04em;padding:.25rem .7rem;border-radius:999px}
.plan h3{font-size:1.05rem;font-weight:600;color:var(--royal)}
.amt{display:flex;align-items:baseline;gap:.35rem}
.amt b{font-family:var(--display);font-weight:400;font-size:3rem;line-height:1;color:var(--navy)}
.amt span,.setup{color:var(--muted)}
.setup{font-size:.92rem}
.plan ul{list-style:none;padding:0;margin-top:.4rem;display:flex;flex-direction:column;gap:.45rem;flex:1}
.plan li{display:flex;gap:.5rem;align-items:flex-start;font-size:.98rem}
.plan li .ic{width:1.15rem;height:1.15rem;color:var(--royal);margin-top:.2rem;stroke-width:2.2}
.plan .btn{margin-top:.8rem}
.pnote{margin-top:1.1rem;color:var(--muted)}

/* coupon */
.coupon{margin-top:2rem;display:grid;grid-template-columns:auto 1fr;background:var(--navy);color:#fff;border-radius:22px;overflow:hidden;box-shadow:var(--sh-2);
  -webkit-mask:radial-gradient(circle at var(--cut) 0,#0000 13px,#000 13.5px) top/100% 51% no-repeat,radial-gradient(circle at var(--cut) 100%,#0000 13px,#000 13.5px) bottom/100% 51% no-repeat;
  mask:radial-gradient(circle at var(--cut) 0,#0000 13px,#000 13.5px) top/100% 51% no-repeat,radial-gradient(circle at var(--cut) 100%,#0000 13px,#000 13.5px) bottom/100% 51% no-repeat;--cut:11rem}
.stub{width:11rem;display:flex;flex-direction:column;align-items:center;justify-content:center;padding:1.4rem 1rem;border-right:2px dashed rgba(201,214,251,.4);text-align:center}
.stub b{font-family:var(--display);font-weight:400;font-size:3.4rem;line-height:1}
.stub span{color:var(--onblue2);font-size:.9rem}
.cbody{padding:1.5rem 1.6rem;display:flex;flex-wrap:wrap;align-items:center;justify-content:space-between;gap:1rem 1.5rem}
.cbody h3{font-family:var(--display);font-weight:400;font-size:1.7rem}
.cbody p{color:var(--onblue2);max-width:30rem;margin-top:.25rem}
.cbody .btn{background:#fff;color:var(--navy);box-shadow:none}
@media (hover:hover){.cbody .btn:hover{background:var(--sky)}}

/* questions: transitions.dev accordion (21) */
.faq{max-width:46rem}
.acc{border-bottom:1px solid var(--line)}
.acc-head{all:unset;box-sizing:border-box;display:flex;width:100%;min-height:3.4rem;align-items:center;justify-content:space-between;gap:1rem;cursor:pointer;font-weight:600;color:var(--navy);padding:.7rem 0}
.acc-head .ic{color:var(--royal);transition:transform var(--acc-chevron) var(--acc-ease)}
.acc-panel{display:grid;grid-template-rows:1fr}
.acc-in{overflow:hidden}
.acc-in p{color:var(--muted);padding-bottom:1rem;max-width:40rem}
.js .acc-panel{grid-template-rows:0fr;transition:grid-template-rows var(--acc-collapse) var(--acc-ease)}
.js .acc-in{opacity:0;transition:opacity var(--acc-collapse) var(--acc-ease)}
.js .acc[data-open="true"] .acc-panel{grid-template-rows:1fr;transition-duration:var(--acc-expand)}
.js .acc[data-open="true"] .acc-in{opacity:1;transition-duration:var(--acc-expand)}
.js .acc[data-open="true"] .acc-head .ic{transform:scaleY(-1)}
footer{padding-block:2.2rem;color:var(--muted);font-size:.88rem;border-top:1px solid var(--line);display:flex;flex-wrap:wrap;justify-content:space-between;gap:.5rem 1.5rem}
footer .logo{color:var(--navy);font-size:1.1rem}
footer .mark{width:1.75rem;height:1.75rem}

@media (max-width:820px){
  .hook,.hero .wrap,.get{grid-template-columns:1fr}
  .chart{justify-self:start;max-width:none}
  .shot{padding-bottom:0}
  .stack{position:relative;left:auto;bottom:auto;width:auto;margin:-3.2rem .9rem 0}
  .steps,.plans{grid-template-columns:1fr}
  .steps li:not(:last-child)::after{top:4.25rem;bottom:-.75rem;left:1.75rem;right:auto;border-top:0;border-left:2px dashed #b9c8ef}
  .steps li{display:grid;grid-template-columns:3.5rem 1fr;column-gap:1rem;align-items:start}
  .steps li .ic{grid-row:span 2}
  .steps b{margin-top:.35rem}
  .plans{gap:1.6rem}
  .coupon{grid-template-columns:1fr;--cut:0}
  .coupon{-webkit-mask:none;mask:none}
  .stub{width:auto;flex-direction:row;gap:.7rem;justify-content:flex-start;border-right:0;border-bottom:2px dashed rgba(201,214,251,.4);padding:1.1rem 1.4rem}
  .stub b{font-size:2.6rem}
}
@media (max-width:560px){
  .cost .wrap{display:grid;grid-template-columns:1.6rem 1fr;gap:.35rem .6rem;align-items:center}
  .cost .term{grid-column:2;flex-direction:row;align-items:baseline;gap:.6rem}
  .cost .op{grid-column:1;text-align:center;font-size:1.6rem}
  .cost small{grid-column:1/-1;margin-top:.4rem}
  .chart{max-width:22rem}
}
@media (max-width:420px){.bar .btn span{display:none}}
@media (prefers-reduced-motion:reduce){.btn,.acc-head .ic,.js .acc-panel,.js .acc-in{transition:none}.btn:active{scale:1}}
"""

GUTTER = "padding-left:16px;padding-right:16px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px));"

SCRIPT = """<script>
const CONFIG = %s;
(function(){
  document.querySelectorAll("[data-name]").forEach(el => el.textContent = CONFIG.name);
  const tel = (CONFIG.phone || "").replace(/[^0-9+]/g, "");
  document.querySelectorAll("[data-phone]").forEach(el => { el.textContent = CONFIG.phone; });
  document.querySelectorAll("[data-call]").forEach(a => { if (tel) { a.href = "tel:" + tel; a.hidden = false; } else a.hidden = true; });
  document.querySelectorAll("[data-book]").forEach(a => { a.href = CONFIG.booking; });
  document.querySelectorAll(".acc").forEach(item => {
    const b = item.querySelector(".acc-head");
    b.addEventListener("click", () => {
      const open = item.dataset.open !== "true";
      item.dataset.open = open; b.setAttribute("aria-expanded", open);
    });
  });
  window.addEventListener("DOMContentLoaded", () => {  // deferred GSAP has loaded by now
    if (!window.gsap || !window.ScrollTrigger) return;
    gsap.registerPlugin(ScrollTrigger);
    gsap.matchMedia().add("(prefers-reduced-motion: no-preference)", () => {
      // the one scroll moment: the evening's calls land on the photo, one after another
      gsap.from(".note", {y: 18, opacity: 0, filter: "blur(4px)", duration: .7, stagger: .25, ease: "expo.out",
        scrollTrigger: {trigger: ".stack", start: "top 85%", once: true}});
    });
  });
})();
</script>"""


def page():
    book = '<a class="btn primary" data-book href="{b}" target="_blank" rel="noopener">{ic}Book a 15-minute call</a>'.format(
        b=CONFIG["booking"], ic=ic("calendar"))
    call = '<a class="btn" data-call hidden>{}Call and hear it <span class="num" data-phone></span></a>'.format(ic("phone"))
    dots = "".join('<i class="m"></i>' if k < 44 else "<i></i>" for k in range(100))
    side = "".join(f'<div><b>{e(n)}</b><span>{e(t)} <a class="src" href="{u}" target="_blank" rel="noopener">{e(s)}</a></span></div>'
                   for n, t, s, u in STATS)
    log = "".join(f'<div class="note ok">{MARK}<div class="h"><b>{e(t)}</b><span class="num">{e(tm)}</span></div><p>{e(x)}</p></div>'
                  for tm, t, x in LOG)
    rows = "".join(f"<li>{ic(i)}<span>{e(t)}</span></li>" for i, t in CALLS)
    revs = "".join(f"<li>{ic('check')}<span>{e(t)}</span></li>" for t in REVIEWS)
    steps = "".join(f"<li>{ic(i)}<b>{e(a)}</b><span>{e(b)}</span></li>" for i, a, b in STEPS)
    plans = "".join(
        f'<div class="plan{" pop" if pop else ""}">' + ('<span class="badge">Most popular</span>' if pop else "")
        + f'<h3>{e(n)}</h3><div class="amt"><b class="num">{e(p)}</b><span>a month</span></div>'
        + f'<div class="setup">+<span class="num">{e(s)}</span> one-time setup</div>'
        + "<ul>" + "".join(f"<li>{ic('check')}<span>{e(i)}</span></li>" for i in items) + "</ul>"
        + f'<a class="btn{" primary" if pop else ""}" data-book href="{CONFIG["booking"]}" target="_blank" rel="noopener">Book a call</a></div>'
        for n, p, s, pop, items in PLANS)
    faq = "".join(
        f'<div class="acc" data-open="false"><button class="acc-head" type="button" aria-expanded="false" aria-controls="q{k}">{e(q)}{ic("chev")}</button>'
        f'<div class="acc-panel" id="q{k}"><div class="acc-in"><p>{e(a)}</p></div></div></div>'
        for k, (q, a) in enumerate(FAQ))
    s44, u44 = SRC44
    s74, u74 = SRC74
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>Always Answered</title>
<meta name="description" content="Every call answered and fresh reviews every month, for service businesses in Nassau County and Brooklyn.">
<script>document.documentElement.classList.add("js")</script>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Work+Sans:wght@400;600&display=swap">
<link rel="preload" as="image" href="img/tech-1600.webp" imagesrcset="img/tech-800.webp 800w, img/tech-1600.webp 1600w" imagesizes="(max-width:820px) 100vw, 600px">
<style>{CSS.replace("GUTTER", GUTTER)}</style>
</head>
<body>
{SPRITE}
<header class="top">
  <div class="wrap bar"><a class="logo" href="#" aria-label="Always Answered, top of page">{MARK}<span data-name>Always Answered</span></a>
    <a class="btn" data-book href="{CONFIG['booking']}" target="_blank" rel="noopener">{ic('calendar')}<span>Book a call</span></a></div>
  <div class="wrap hook">
    <div>
      <h1>Almost half the calls to businesses never get answered.</h1>
      <div class="side">{side}</div>
    </div>
    <figure class="chart" aria-label="Chart: 44 of every 100 business calls go unanswered">
      <div class="dots" aria-hidden="true">{dots}</div>
      <p><b>44%</b><span>of calls ring out.<a class="src" href="{u44}" target="_blank" rel="noopener">{e(s44)}</a></span></p>
    </figure>
  </div>
</header>
<div class="cost"><div class="wrap">
  <div class="term"><b class="num">3</b><span>missed calls a week</span></div><span class="op" aria-hidden="true">&times;</span>
  <div class="term"><b class="num">$300</b><span>a job</span></div><span class="op" aria-hidden="true">=</span>
  <div class="term total"><b class="num">$3,900</b><span>a month to someone else</span></div>
  <small>Example math. Put in your own numbers.</small>
</div></div>
<section class="hero"><div class="wrap">
  <div>
    <h2>Every call answered. Fresh reviews every month.</h2>
    <p class="lead">An AI front desk for service businesses in Nassau County and Brooklyn. You work. We answer.</p>
    <div class="ctas">{book}{call}</div>
  </div>
  <figure class="shot">
    <img src="img/tech-1600.webp" srcset="img/tech-800.webp 800w, img/tech-1600.webp 1600w" sizes="(max-width:820px) 100vw, 600px" width="1600" height="924"
      alt="A technician checks an air conditioner outside a house, hands busy, while his calls are answered">
    <div class="stack" aria-label="Example evening: calls answered while you work">{log}</div>
  </figure>
</div></section>
<section><div class="wrap">
  <h2 class="t">What you get</h2>
  <div class="get">
    <div><h3>Your calls</h3><ul class="rows">{rows}</ul></div>
    <div class="panel"><h3>Your reviews</h3>
      <div class="msg" aria-label="Example review request a customer gets after the job"><div class="who">Bayview Plumbing</div>
        Thanks for choosing us! Mind leaving a quick Google review?
        <div class="stars" aria-hidden="true">{ic('star')*5}</div></div>
      <ul>{revs}</ul>
      <p class="fact"><b>74%</b><span>want reviews from the last 3 months. <a href="{u74}" target="_blank" rel="noopener">{e(s74)}</a></span></p>
    </div>
  </div>
</div></section>
<section class="wash"><div class="wrap"><h2 class="t">How it starts</h2><ol class="steps">{steps}</ol></div></section>
<section><div class="wrap"><h2 class="t">Plans and prices</h2>
  <div class="plans">{plans}</div>
  <p class="pnote">Month to month. Cancel any time. Extra minutes $0.25 each.</p>
  <div class="coupon">
    <div class="stub"><b>50%</b><span>off setup</span></div>
    <div class="cbody"><div><h3>Black Friday special</h3><p>Half off the setup fee for a short testimonial after month one. Sign up by November 30.</p></div>
      <a class="btn" data-book href="{CONFIG['booking']}" target="_blank" rel="noopener">Claim it{ic('arrow')}</a></div>
  </div>
</div></section>
<section class="wash"><div class="wrap"><h2 class="t">Questions</h2><div class="faq">{faq}</div></div></section>
<div class="wrap"><footer><span class="logo">{MARK}<span data-name>Always Answered</span></span><span class="num" data-phone></span></footer></div>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/gsap.min.js" defer></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.15.0/ScrollTrigger.min.js" defer></script>
{SCRIPT.replace("%s", json.dumps(CONFIG), 1)}
</body>
</html>
"""


if __name__ == "__main__":
    out = page()
    (SITE / "index.html").write_text(out)
    (HERE / "index.html").write_text(out)
    print("BUILT", len(out), "bytes")
