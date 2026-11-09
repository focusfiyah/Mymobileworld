# "Get 3 free UGC ideas" form (Grace portfolio)

Same method as the Diaspo lead system (Ralph 2026-11-06: "The same way we created the form with Diaspo Auto School"):
a Google Apps Script web app that serves the form, saves each request to a Google Sheet and emails Grace.
Brands need no login. Runs on Ralph's Google account (life22watch@gmail.com), free.

Files: `Code.gs` (server), `ideas.html` (the form page). Copies in Drive "Grace Tiktok assets/UGC Portfolio (Grace)":
Ideas form - Code.gs.txt (1myFBvcd6rtfMyRn82VA-EcV-Ff6vpPd4), Ideas form - ideas.html.txt (1jc1jG5ZZgRipCtrGEzBXz4-lrMbqo6fm).

## Setup (Ralph, about 5 minutes)
1. script.google.com > New project. Name it "Grace ideas form".
2. Code.gs: replace everything with the Code.gs file.
3. File + (Add file) > HTML, name it `ideas` (exactly), paste ideas.html.
4. Pick `setup` in the function menu > Run > allow access (Sheets, Mail). The log shows the new sheet's link.
5. Deploy > New deployment > type Web app. Execute as: Me. Who has access: Anyone. Deploy, copy the Web app URL (ends in /exec).
6. Send the URL to Azariah: the portfolio's "Get 3 free UGC ideas" buttons then open it.
7. The sheet is created at the top of My Drive; it was moved into UGC Portfolio (Grace) 2026-11-07 (id 1lPvtCRuOkMs_8ztjPVfztuNBlb-cHniOah1Vueaq36k). Moving it is safe: the script finds it by id.
8. Test once: fill the form yourself. Expect a row in "Grace - 3 free UGC ideas", an email to Grace, a confirmation to you.

## What happens on submit
- Row: Received, Name, Brand, Email, Product link, Videos for, Notes, Status=New.
- Email to graceglows.ugc@gmail.com ("3 free UGC ideas request: <brand>"), Reply goes to the brand.
- Confirmation to the brand from "Grace With The Glow" (sent from life22watch@gmail.com, Reply-To Grace).
- Hidden field `zq_check` stops bots (named so browsers don't autofill it: Diaspo lesson 2026-11-05).

## Tested (2026-11-06, mocks, no Google call)
node mock: valid request -> 1 row + 2 emails (Grace, brand), bad email refused, honeypot saves nothing.
Playwright 390 px: empty submit shows the error, filled submit shows the thank-you; no page errors, no side scroll.
Not tested: the real Apps Script deployment (needs Ralph's paste + deploy).
