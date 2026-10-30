# GATES: Always Answered page round 4 (Ralph 2026-10-29: "too wordy and need some graphics upgrades. Let use that skill")
Request: fewer words, better graphics, built with the web-design-stack skill. Keep everything Ralph set in round 3
(stats first, 3 plans + prices, Black Friday special, royal blue, Nassau County and Brooklyn, no "new business" tells).
Live site changes only on Ralph's OK of the preview.

- [ ] G1: visible words cut to 400 or fewer (round 3 page: 777)
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py words
  EXPECT: WORDS_OK
- [ ] G2: a problem statistic comes before the solution heading
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py order
  EXPECT: STATS_FIRST
- [ ] G3: three plans with the approved prices and setup fees, middle one most popular, $0.25 extra minutes
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py plans
  EXPECT: PLANS_OK
- [ ] G4: Black Friday special: half off setup, testimonial, November 30
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py bf
  EXPECT: BF_OK
- [ ] G5: banned wording absent (one plan, founding, first 3 businesses, 14 days free, Freeport, Baldwin, "we're new", eyebrow kicker)
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py banned
  EXPECT: WORDING_OK
- [ ] G6: graphics: real photo with alt text + at least 8 drawn SVG graphics/icons + the 100-call dot chart with exactly 44 missed
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py graphics
  EXPECT: GRAPHICS_OK
- [ ] G7: royal blue theme kept (#1f4fd8, #0b1e5b)
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py blue
  EXPECT: BLUE_OK
- [ ] G8: motion budget passes
  CHECK: python3 /home/user/Mymobileworld/.claude/skills/web-design-stack/scripts/motion_check.py /home/user/always-answered/index.html
  EXPECT: MOTION_OK
- [ ] G9: browser render: no side scroll at 390 and 1440, no console errors, cards visible with reduced motion and with JS off, scroll moment ends fully visible
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py render
  EXPECT: RENDER_OK
- [ ] G10: photo licence and source written down
  CHECK: python3 -c "t=open('/home/user/always-answered/img/SOURCES.md').read();print('SRC_OK' if 'pexels.com/photo/technician-inspecting-outdoor-hvac-unit-32497161' in t and 'Pexels License' in t else 'SRC_MISSING')"
  EXPECT: SRC_OK
- [ ] G11: Impeccable detector clean, or each finding named with its reason (manual: detector output read)
- [ ] G12: Make Interfaces Feel Better full review ends in Approve (manual)
- [ ] G13: phone + desktop screenshots looked at full size (manual)
- [ ] G14: preview on the private review page + push + email sent to Ralph (manual)

## Round 4b: motion graphics (Ralph 2026-10-29: "Can we add motion graphics as well", picked "Animate the graphics")
Dots fill in, 44% and $3,900 count up, the sum builds, the phone icon rings, the step line draws, stars fill, notes land.
Scroll budget raised from 2 to 5 on Ralph's pick (his words beat the skill's budget).
- [ ] G15: motion budget passes at the raised limit, reduced-motion path present
  CHECK: python3 /home/user/Mymobileworld/.claude/skills/web-design-stack/scripts/motion_check.py /home/user/always-answered/index.html --scroll-max 5 --tween-max 20
  EXPECT: MOTION_OK
- [ ] G16: after a full scroll every animated graphic ends in its true final state (44 orange dots, 44%, $3,900, notes, stars, step line), with motion on, with reduced motion and with JS off
  CHECK: python3 /home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/check.py final
  EXPECT: FINAL_OK
- [ ] G17: frames taken mid-animation looked at (dots filling, sum building) (manual)

## Round 4c: phone number (Ralph 2026-10-30: "Add phone number now")
- [ ] G18: the number is on the ElevenLabs Always Answered agent
  CHECK: curl -sS https://api.elevenlabs.io/v1/convai/phone-numbers | python3 -c "import sys,json;d=json.load(sys.stdin);print('NUMBER_OK' if any(p.get('phone_number')=='+15167887489' and (p.get('assigned_agent') or {}).get('agent_id')=='agent_9001m6504b34ft0tqkvzndktcpjw' for p in d) else 'NOT_YET')"
  EXPECT: NUMBER_OK
- [ ] G19: the live site shows (516) 788-7489 with working tel:+15167887489 buttons, no dashed placeholder
  CHECK: python3 -c "import urllib.request,time;h=urllib.request.urlopen('https://focusfiyah.github.io/always-answered/?r='+str(time.time())).read().decode();print('SITE_OK' if 'tel:+15167887489' in h and '(516) 788-7489' in h and '000-0000' not in h else 'NOT_YET')"
  EXPECT: SITE_OK
- [ ] G20: the round 4 page has the number as static text and links (works with JS off)
  CHECK: python3 -c "h=open('/home/user/always-answered/index.html').read() if False else open('/home/user/Mymobileworld/ralph/dfy-service/launch/site/v4/index.html').read();print('V4_OK' if h.count('href=\"tel:+15167887489\"')>=2 and '(516) 788-7489' in h and 'data-call hidden' not in h else 'V4_BAD')"
  EXPECT: V4_OK
