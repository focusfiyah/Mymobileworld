# GATES: Always Answered page round 3 (Ralph 2026-10-28)
Request: stats first (problem + cost before the solution), 3 plans ($197/$397/$597, setup $297/$497/$497, Ralph picked "3 plans (Recommended)"), Black Friday special instead of founding offer (half off setup for a testimonial, ends Nov 30), no "one plan, one price", nothing that says we're new, royal blue theme.

- [ ] G1: the first text a visitor reads is a problem statistic, before the name/solution heading
  CHECK: python3 -c "import re;h=open('/home/user/always-answered/index.html').read();b=h[h.index('<body'):];i=b.find('44%');j=b.find('Every call answered');print('STATS_FIRST' if 0<i<j else 'NOT_FIRST',i,j)"
  EXPECT: STATS_FIRST
- [ ] G2: three plans with the approved prices, middle one marked most popular
  CHECK: python3 -c "h=open('/home/user/always-answered/index.html').read();ok=all(x in h for x in ['$197','$397','$597','$297','Most popular']);print('PLANS_OK' if ok else 'PLANS_BAD')"
  EXPECT: PLANS_OK
- [ ] G3: banned wording gone: one plan, founding, first 3 businesses, 14 days free
  CHECK: python3 -c "import re;h=open('/home/user/always-answered/index.html').read().lower();bad=[w for w in ['one plan','founding','first 3 businesses','14 days free','first 14 days'] if w in h];print('WORDING_OK' if not bad else 'WORDING_BAD',bad)"
  EXPECT: WORDING_OK
- [ ] G4: Black Friday special says half off setup, testimonial, November 30
  CHECK: python3 -c "h=open('/home/user/always-answered/index.html').read();ok=all(x in h for x in ['Black Friday','half off the setup fee','testimonial','November 30']);print('BF_OK' if ok else 'BF_BAD')"
  EXPECT: BF_OK
- [ ] G5: royal blue is the theme colour and the old gold is gone
  CHECK: python3 -c "h=open('/home/user/always-answered/index.html').read().lower();print('BLUE_OK' if '#1f4fd8' in h and '#d8a84a' not in h else 'BLUE_BAD')"
  EXPECT: BLUE_OK
- [ ] G6: live site serves the new page
  CHECK: python3 -c "import urllib.request,time;h=urllib.request.urlopen('https://focusfiyah.github.io/always-answered/?r='+str(time.time())).read().decode();print('LIVE_OK' if 'Black Friday' in h and '#1f4fd8' in h.lower() else 'LIVE_OLD')"
  EXPECT: LIVE_OK
- [ ] G7: looked at at 390 px and 1440 px full size, no side scroll (manual + screenshot)
- [ ] G8: the phone assistant script and OFFER.md quote the same plans and special (manual read)
