"""Builds the two inner pages and patches the home page nav, cards and form. Run from this folder."""
import re
LOGO='<svg viewBox="0 0 48 52" width="40" height="43" aria-hidden="true"><path d="M24 2 46 18v32H2V18Z" fill="var(--brick)"/><path d="M15 38V15h10.5c5 0 8 2.7 8 6.9 0 3.2-1.9 5.4-5 6.3L34 38h-6.2l-4.6-9H20.5v9Zm5.5-13.6h4.4c1.8 0 2.8-.9 2.8-2.4s-1-2.4-2.8-2.4h-4.4Z" fill="#fff"/></svg>'
def header(active):
    def a(href,label,key):
        cur=' aria-current="page"' if active==key else ''
        return f'<a href="{href}"{cur}>{label}</a>'
    if active=='home':
        nav=a('#properties','Properties','x')+a('#services','What we do','x')+a('we-buy-houses.html','We buy houses','b')+a('property-management.html','Property management','m')+a('#area','Where we work','x')
        top='#top'
    else:
        nav=a('index.html','Home','x')+a('we-buy-houses.html','We buy houses','b')+a('property-management.html','Property management','m')+a('index.html#area','Where we work','x')
        top='index.html'
    return f'''<div class="preview" role="note">Preview for Luigi Ruiz. Photos are samples.</div>

<header class="site-head">
  <div class="wrap bar">
    <a class="logo" href="{top}" aria-label="Ruiz Property Group, home">
      {LOGO}
      <span class="wm"><b>RUIZ</b><i>Property Group</i></span>
    </a>
    <nav aria-label="Main">{nav}</nav>
    <a class="btn small" href="#contact">Get in touch</a>
  </div>
</header>'''
FOOT='''<footer class="foot">
  <svg class="skyline" viewBox="0 0 1200 120" preserveAspectRatio="none" aria-hidden="true"><path d="M0 120V80h30V50h24V70h20V30h26V60h18V40h22V75h28V20h16V8h8V20h16V65h24V45h30V80h22V55h26V35h20V70h30V50h24V85h26V60h20V25h24V70h28V45h22V80h26V58h30V30h18V72h24V52h26V88h30V62h22V38h26V76h24V50h28V84h30V66h22V42h24V78h28V55h26V90h30V64h22V34h20V70h28V48h24V82h26V120Z" fill="currentColor"/></svg>
  <div class="wrap foot-in"><div><p><b>Ruiz Property Group LLC</b></p><p>Property buyer, renovator and manager. Serving the New York tri-state area.</p><div class="foot-links"><a href="we-buy-houses.html">We buy houses</a><a href="property-management.html">Property management</a><a href="index.html#area">Where we work</a></div></div><a class="btn small" href="#contact">Get in touch</a></div>
</footer>
<a class="sticky-cta" href="#contact">Get in touch</a>

<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/gsap.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/gsap/3.12.5/ScrollTrigger.min.js"></script>
<script src="app.js"></script>
</body>
</html>'''
def form(default):
    opts=['Sell my property','Buy a renovated home','Rent a home','Property management for my building','Something else']
    o=''.join(f'<option{" selected" if x==default else ""}>{x}</option>' for x in opts)
    return f'''<form id="lead" class="form" novalidate>
      <div class="field"><label for="name">Your name</label><input id="name" name="name" autocomplete="name" required></div>
      <div class="two">
        <div class="field"><label for="phone">Phone</label><input id="phone" name="phone" type="tel" autocomplete="tel" inputmode="tel"></div>
        <div class="field"><label for="email">Email</label><input id="email" name="email" type="email" autocomplete="email" required></div>
      </div>
      <div class="field"><label for="need">What do you need?</label><select id="need" name="need">{o}</select></div>
      <div class="field"><label for="addr">Property address</label><input id="addr" name="address" autocomplete="street-address"></div>
      <div class="field"><label for="msg">Anything else we should know?</label><textarea id="msg" name="message" rows="4"></textarea></div>
      <button class="btn" type="submit">Send</button>
      <p class="status" id="status" role="status" aria-live="polite"></p>
    </form>'''
def head(title,desc):
    return f'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@62..125,500..900&family=Hanken+Grotesk:wght@400;500;600&display=swap">
<link rel="stylesheet" href="styles.css">
</head>
<body>
'''
def ico(path): return f'<span class="ico"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="{path}"/></svg></span>'
# ---------- We buy houses ----------
buy_steps=[('Find the opportunity','We look for properties with potential: homes that need repairs, updates or a full transformation.'),
('Evaluate the property',"We assess its condition, the renovation needed and its investment potential to decide if it is the right project."),
('Purchase the property','We work toward a purchase agreement that makes sense for both the property and the seller.'),
('Renovate and improve',"We coordinate the repairs and improvements that raise the home's function, appearance and market appeal."),
('Transform and resell','We prepare the finished home for the market and connect with buyers who want a move-in-ready house.')]
reno=['Kitchen remodeling and upgrades','Bathroom renovations','Flooring installation and replacement','Interior and exterior painting','Roofing and exterior improvements','Plumbing and electrical upgrades','Landscaping and curb appeal','Structural and general repairs','Full interior and exterior renovations']
buy=head('We Buy Houses | Ruiz Property Group LLC','Ruiz Property Group buys houses in any condition, renovates them and sells them across the New York tri-state area.')+header('b')+f'''

<main id="top">
<section class="hero page">
  <img class="hero-bg" src="img/fixer.jpg" width="1300" height="975" alt="Small blue house with boarded windows waiting for renovation" fetchpriority="high">
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>We Buy Houses. We Renovate. We Transform.</h1>
      <p class="sub">Turning neglected houses into homes, and real estate opportunities into results.</p>
      <div class="cta-row"><a class="btn" href="#contact">Tell us about your property</a><a class="link light" href="#process">How we work</a></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap intro">
    <div>
      <div class="head"><p class="eyebrow">Welcome</p><h2>Welcome to Ruiz Property Group</h2></div>
      <div class="prose">
        <p>Ruiz Property Group is a real estate investment company that buys, renovates and sells residential properties across the New York tri-state area. We take distressed, outdated and neglected houses and turn them into modern homes with new value and purpose.</p>
        <p>Some properties need small improvements and others need a full renovation. Either way, we look for the potential in a house that others pass over, then plan the work and carry it out with quality craftsmanship.</p>
      </div>
    </div>
    <figure><img src="img/renovation.jpg" width="1300" height="866" loading="lazy" alt="Kitchen mid-renovation with new cabinets going in"></figure>
  </div>
</section>

<section id="what-we-do" class="block soft">
  <div class="wrap">
    <div class="head"><p class="eyebrow">What we do</p><h2>Buy it. Fix it. Sell it.</h2></div>
    <div class="svc">
      <article id="buy">{ico("M6 20 20 7l14 13 M10 18v16h20V18 M17 34V24h6v10")}<h3>We buy houses</h3><p>We buy residential properties in many conditions: houses that need repairs, outdated homes, vacant properties, inherited properties and distressed real estate.</p><p>We want selling to be simple for you. If repairs, money concerns or unexpected circumstances are making a sale hard, we will work with you to find a solution that fits.</p></article>
      <article id="renovate">{ico("M8 32 24 16 M22 10l8 8 M26 6l8 8 M6 34l4-4")}<h3>We renovate and restore</h3><p>After we buy a property, we improve its condition, how it works and how it looks.</p><p>Good renovation is more than appearance. It creates safe, functional and attractive homes for the people who will live in them.</p></article>
      <article id="flip">{ico("M6 30V10h14v20 M20 18h14v12 M6 34h28 M11 15h4 M11 21h4 M25 24h4")}<h3>We fix and flip houses</h3><p>We start by finding properties with renovation potential. We evaluate the house, build a renovation plan and make the repairs and upgrades that add the most value.</p><p>When the work is done, we prepare the property for sale, so buyers get a refreshed home without taking on the renovation themselves.</p></article>
    </div>
    <div class="panel" style="margin-top:22px">
      <h3>Our renovation projects can include</h3>
      <ul class="checks">{''.join(f"<li>{x}</li>" for x in reno)}</ul>
    </div>
  </div>
</section>

<section id="process" class="block dark">
  <div class="wrap sell">
    <div class="head"><p class="eyebrow">Our process</p><h2>From first look to move-in ready.</h2><a class="btn" href="#contact">Tell us about your property</a></div>
    <ol class="steps" id="steps">
{''.join(f'      <li><span class="n" aria-hidden="true">{i+1}</span><div><strong>{t}</strong><p>{d}</p></div></li>' + chr(10) for i,(t,d) in enumerate(buy_steps))}    </ol>
  </div>
</section>

<section class="block">
  <div class="wrap vision">
    <div class="head"><p class="eyebrow">Our vision</p><h2>Better neighborhoods, one property at a time.</h2></div>
    <blockquote>To improve neighborhoods one property at a time, by turning neglected houses into attractive, functional homes that create new opportunities for owners, buyers and communities.</blockquote>
  </div>
</section>

<section class="block soft">
  <div class="wrap why">
    <div class="head"><p class="eyebrow">Why work with us</p><h2>Why work with Ruiz Property Group</h2><p class="lead sm">We value honesty, professionalism, quality and attention to detail. You can expect:</p></div>
    <ul class="checks">
      <li>A straightforward selling experience</li><li>Flexible solutions for properties in any condition</li><li>Careful renovation planning</li><li>Quality workmanship</li><li>A commitment to improving homes and neighborhoods</li>
    </ul>
    <p class="lead sm" style="margin-top:8px">Whether you are selling a house that needs repairs, selling an inherited property or looking for a newly renovated home, we aim to make the process a good experience.</p>
  </div>
</section>

<section id="contact" class="block tint">
  <div class="wrap contact">
    <div class="head"><p class="eyebrow">Get in touch</p><h2>Let's make your property our next project</h2>
      <div class="cta-copy"><p>Do you have a house you need to sell? Is your property outdated, vacant or in need of repairs? We are always looking at new opportunities.</p><p>Contact Ruiz Property Group today to talk about your property and see how we can help.</p></div>
      <p class="tagline">Buy. Renovate. Transform. Create value.</p></div>
    {form('Sell my property')}
  </div>
</section>
</main>

'''+FOOT
open('site/we-buy-houses.html','w').write(buy)
# ---------- Property management ----------
svc=[('Residential property management','Day-to-day management of your rental homes: tenant relations, rent collection, inspections, maintenance coordination and lease administration.',"M6 20 20 7l14 13 M10 18v16h20V18 M17 34V24h6v10"),
('Tenant placement and leasing','The right tenant protects your investment. We handle marketing, rental inquiries, tenant screening, lease preparation and move-in coordination.',"M14 14a6 6 0 1 0 12 0 6 6 0 1 0-12 0 M8 34c0-7 5-10 12-10s12 3 12 10 M26 8l3 3 5-6"),
('Rent collection and financial management','Steady rental income starts with organized collection. We track payments and expenses and send you clear financial reports.',"M6 34V22 M16 34V12 M26 34V20 M36 34V6 M4 34h34"),
('Maintenance and repairs','We coordinate routine maintenance, emergency repairs and vendor work, so small problems get fixed before they become expensive ones.',"M8 32 24 16 M22 10l8 8 M26 6l8 8 M6 34l4-4"),
('Property inspections','Regular inspections show us how your property is holding up and catch issues early.',"M17 8a9 9 0 1 0 0 18 9 9 0 1 0 0-18 M24 24l11 11"),
('Tenant relations','We are the point of contact for your tenants. We answer questions, handle service requests and resolve concerns quickly and respectfully.',"M6 8h28v18H20l-8 8v-8H6Z"),
('Lease administration','Renewals, notices, rental documents and lease management, handled for you.',"M10 4h14l8 8v24H10Z M24 4v8h8 M15 20h12 M15 27h12")]
cards=''.join(f'<article{" class=\"wide\"" if i==6 else ""}>{ico(p)}<h3>{t}</h3><p>{d}</p></article>' for i,(t,d,p) in enumerate(svc))
pm=head('Property Management | Ruiz Property Group LLC','Ruiz Property Group manages rental properties across the New York tri-state area: rent collection, maintenance, tenant relations and leasing.')+header('m')+f'''

<main id="top">
<section class="hero page">
  <img class="hero-bg" src="img/corner.jpg" width="1300" height="866" alt="Brick corner building on a tree-lined street" fetchpriority="high">
  <div class="hero-shade" aria-hidden="true"></div>
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <h1>Your Property, Professionally Managed</h1>
      <p class="sub">Property management that protects your investment, simplifies ownership and keeps your tenants happy.</p>
      <div class="cta-row"><a class="btn" href="#contact">Request a free property management consultation</a><a class="link light" href="#services">Our services</a></div>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap intro">
    <div>
      <div class="head"><p class="eyebrow">Welcome</p><h2>Welcome to Ruiz Property Group</h2></div>
      <div class="prose">
        <p>Ruiz Property Group manages rental properties for owners across the New York tri-state area. We help you collect rent on time, keep your building in good shape and keep tenants satisfied, so owning property takes less of your time.</p>
        <p>We manage single-family homes, multi-family buildings, apartment buildings, condominiums and commercial properties. Whatever you own, you get one dependable point of contact who knows your property.</p>
      </div>
      <ul class="chips2" style="margin-top:22px"><li>Single-family homes</li><li>Multi-family buildings</li><li>Apartment buildings</li><li>Condominiums</li><li>Commercial properties</li></ul>
    </div>
    <figure><img src="img/apartments.jpg" width="1300" height="866" loading="lazy" alt="Brick walk-up apartment building with fire escapes on a New York street"></figure>
  </div>
</section>

<section id="services" class="block soft">
  <div class="wrap">
    <div class="head"><p class="eyebrow">Our services</p><h2>Our property management services</h2></div>
    <div class="svc">{cards}</div>
  </div>
</section>

<section class="block dark">
  <div class="wrap vision">
    <div class="head"><p class="eyebrow">Why owners choose us</p><h2>Why owners choose Ruiz Property Group</h2></div>
    <div class="why">
      <ul class="checks" style="grid-template-columns:1fr">
        <li style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff">We protect and maintain your investment</li>
        <li style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff">We help reduce vacancies and improve rental performance</li>
        <li style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff">We keep tenants satisfied and respond to maintenance requests promptly</li>
        <li style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff">We keep you informed and involved</li>
        <li style="background:rgba(255,255,255,.08);border-color:rgba(255,255,255,.2);color:#fff">We tailor our management to your property's needs</li>
      </ul>
    </div>
  </div>
</section>

<section class="block">
  <div class="wrap vision">
    <div class="head"><p class="eyebrow">Our mission</p><h2>Our mission</h2></div>
    <blockquote>To give property owners confidence in their investment through dependable, high-quality management. We look after the property, support the tenants and help owners reach their real estate goals.</blockquote>
  </div>
</section>

<section id="contact" class="block tint">
  <div class="wrap contact">
    <div class="head"><p class="eyebrow">Get in touch</p><h2>Let us manage your property</h2>
      <div class="cta-copy"><p>Whether you are a first-time landlord or an experienced investor, Ruiz Property Group can take over the daily work of managing your property while you focus on growing your portfolio.</p><p>Contact Ruiz Property Group today to talk about your property and how we can manage it.</p></div>
      <p class="tagline">Your property. Our priority.</p></div>
    {form('Property management for my building')}
  </div>
</section>
</main>

'''+FOOT
open('site/property-management.html','w').write(pm)
# ---------- patch home ----------
h=open('site/index.html').read()
hdr=header('home')
i=h.index('<div class="preview"');j=h.index('</header>')+len('</header>')
h=h[:i]+hdr+h[j:]
# services section: four ways
h=h.replace('<h2>One owner. Three ways to work with us.</h2>','<h2>One owner. Four ways to work with us.</h2>')
h=h.replace('<div class="cards">','<div class="cards cards4">',1)
h=h.replace('<a class="link" href="#sell">How it works</a>','<a class="link" href="we-buy-houses.html">How it works</a>')
h=h.replace('<a class="link" href="#contact">Ask about available homes</a>','<a class="link" href="we-buy-houses.html#renovate">See how we renovate</a>')
mg='''      <article class="card"><div class="media"><img src="img/mixeduse.jpg" width="1400" height="933" loading="lazy" alt="Three-story mixed-use building with shopfronts on the ground floor"><span class="ico"><svg viewBox="0 0 40 40" aria-hidden="true"><path d="M10 4h14l8 8v24H10Z M24 4v8h8 M15 20h12 M15 27h12"/></svg></span></div><div class="body"><h3>Let us manage your property</h3><p>Rent collection, maintenance, tenant relations and leasing for owners who want their building looked after.</p><a class="link" href="property-management.html">Property management</a></div></article>
'''
k=h.index('</div>\n  </div>\n</section>\n\n<section id="sell"')
h=h[:k]+mg+h[k:]
h=h.replace('<option>Sell my property</option><option>Buy a renovated home</option><option>Rent a home</option><option>Something else</option>','<option>Sell my property</option><option>Buy a renovated home</option><option>Rent a home</option><option>Property management for my building</option><option>Something else</option>')
# footer
k=h.index('<footer class="foot">');e=h.index('</body>')
h=h[:k]+FOOT[:-len('</body>\n</html>')].split('<script')[0].strip()+'\n\n'+FOOT[FOOT.index('<script'):]
open('site/index.html','w').write(h)
print('built')
