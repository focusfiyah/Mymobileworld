# Client websites: hosting, domains, forms (Ralph 2026-11-24)

Decided with Ralph (tapped "Cloudflare domain + Netlify host", then moved Grace's landing page as the Cloudflare test).
Design and polish: the `web-design-stack` skill. This file is only where a site lives and how it ships.

## The setup
- **Host: Netlify** (account life22watch, `api.netlify.com` is proxy-injected, tested 2026-11-24: user, sites list).
  Netlify is the default because Claude can publish updates itself (new deploy = one API call or a GitHub push).
- **Domain: Cloudflare Registrar, bought by the client in the client's own name** (wholesale price, about $10-12 a year for
  a .com, no renewal markup; prices from memory, check live before quoting). The client owns the login; DNS records point
  at the host. GoDaddy is steered away from (upsells, renewal markup); Wix/Squarespace/GoDaddy builders cannot be edited
  from here and read as templates.
- **Pages first, multi-page later:** a landing page ships first; build it so it can grow into a multi-page site without a redo.
  A review page (private Artifact) comes before anything goes live.
- Site code goes in a repo; media (photos, video) goes in Drive, never git (CLAUDE.md job-media rule).

## Cloudflare account (connected 2026-11-24)
- `api.cloudflare.com` token saved with `request_credential` (proxy-injected). Account id 4f352de90e0b0aabbfbd34db62d177f2,
  workers.dev subdomain `life22watch`. Needs an EDIT token (Workers, Pages, KV, Zone DNS); the first token was read-only and
  every write answered "Authentication error" (code 10000).
- Works from here: read account, list/create Pages projects (POST `/accounts/{id}/pages/projects`), read deployments.
- **Does NOT work from here: uploading site files.** Pages' asset upload uses its own one-time JWT (`/pages/assets/upload`);
  the session proxy overwrites the Authorization header with the account token, so wrangler and curl both fail with
  code 8000013. The legacy multipart POST `/deployments` creates a deployment but stores no files (every URL answers 500).
  Do not try to get around the proxy.
- **So a Cloudflare deploy is manual:** zip the site folder (index.html at the root), SendUserFile it, Ralph uploads it in
  Workers & Pages > project > Create deployment, then Claude checks the live URL (home page identical to the local copy,
  every media file 200 with the right size, no leftover text from the old host). A CDN warm-up shows brief 500s: retest.
- Because of that, new client sites stay on Netlify (Claude deploys); Cloudflare hosting only on Ralph's call.

## Moving a site off Netlify (the free-plan banner)
Netlify injects an HTML comment and `<script src="/.netlify/scripts/hud...">` into pages served from the free plan: strip
both (the deployed copy is not edited). Pull the files with the files API
(`/api/v1/deploys/{id}/files`) and download each path from the site. The Netlify Forms posts stop working on any other host.
First move: Grace's landing page, https://gracewiththeglow.pages.dev (project `gracewiththeglow`); the Netlify copy
(gracewiththeglow.netlify.app) was left up on Ralph's word.

## Forms without a server: Web3Forms
Chosen over Resend (free tier only mails the signup address, key must be pasted into Cloudflare by hand).
Web3Forms free: 250 submissions a month, the access key is public by design (safe to paste in chat), each submission is
emailed to the address on the account (change it in the form's settings on web3forms.com before real leads arrive).
Page code: hidden `access_key`, `subject`, `from_name`, a `botcheck` checkbox honeypot, and
`fetch("https://api.web3forms.com/submit", { method: "POST", body: new FormData(form) })` (plain form data: a JSON body with
an Accept header triggers a CORS preflight that Web3Forms fails). Server-side calls (curl, Playwright from the cloud) get
403 "Pro plan is required", so the form can only be tested from a real browser, i.e. Ralph's phone. Third party sees the lead's
name, email and link: say so to the client. Grace's key: 26901150-511e-470d-b5f8-b6e6af5017d4 (public).

## Netlify deploy budget (Ralph 2026-11-24)
Netlify Free = 300 credits per billing period for the WHOLE account (all sites); a production deploy costs 15 (about 20 deploys), bandwidth 20 per GB, requests 2 per 10k. On 2026-11-24 about 16 deploys (Ruiz proposal and preview, iterated per edit) hit "Account credit usage exceeded - new deploys are blocked" for every site. The account's next period starts 2026-12-03 00:00 PST (GET /api/v1/accounts: next_usage_period_start; the same record shows usages_exceeded and grace_topup_granted_at, but not credits used).
- Build and test locally; review rounds on a private Artifact; deploy a finished batch, at most 2 deploys per site per review round; say the month's deploy count before each deploy.
- Count deploys in this log (add a line per deploy):
  - 2026-11 (period from 3 Nov): about 16 on 2026-11-24 (ruiz-property-group-proposal x8, ruiz-property-group-preview x3, others earlier) then blocked.

## Two Netlify accounts (Ralph 2026-11-24)
- PRIMARY: life22watch / team "focusfiyah" (id 6ae97184bee70a7b489b7635), credits renew 2026-12-03 00:00 PST. Always first.
- BACKUP: realgoodhustles@gmail.com, team realgoodhustles (Free, 300 credits, period 24 Nov to 23 Dec, next usage period 2026-12-24 00:00 PST). Token saved 2026-11-25 with request_credential and it REPLACED the primary's (one injected token per host): the API now answers as the backup; verify with GET /api/v1/user before any deploy. To go back to the primary Ralph makes a new token there and it is saved the same way. Used only while the primary answers "Account credit usage exceeded"; the same sites get new addresses there.
- NOTE TO SELF: from 2026-12-03 08:00 UTC check the primary's next_usage_period_start / usages_exceeded; if it renewed, move everything back to the primary. If the primary runs out again and the backup has credits, use the backup. No scheduled task for this unless Ralph OKs one.
- Deploy count per account per month (add a line per deploy): primary 2026-11: about 16 by 2026-11-24 (blocked); backup: none yet.
- Backup deploys: 2026-11-25 #1 ruiz-property-group-preview-2.netlify.app (NYC imagery preview, site id 144dffb1-e0ee-4658-b87e-2c955024b8ce). New sites start login-protected: PATCH sso_login false.
- Sites still on the primary (not updatable while the backup is active): gracewiththeglow, dayoneai-proposal, shotcam-azariah, ruiz-property-group-proposal (778bc082...), ruiz-property-group-preview (76bb97a6..., old suburban version).
- Backup deploys: 2026-11-25 #2 ruiz-property-group-proposal-2.netlify.app (updated proposal with fee, questions and the preview-2 link; site id aa6b54a0-9fe4-4634-a969-a390dd5e527a). Backup total: 2 deploys (30 of 300 credits).
- Backup deploys: 2026-11-25 #3 ruiz-property-group-preview-2 (3-page site: home, /we-buy-houses, /property-management) and #4 ruiz-property-group-proposal-2 (three-page wording). Backup total: 4 deploys (60 of 300 credits). Netlify rewrote the menu links to pretty URLs (/we-buy-houses); a _headers entry per page keeps text/html on zip deploys.
- Backup deploys: 2026-11-25 #5 ruiz-property-group-preview-2 (phone (516) 233-0110 on all pages) and #6 ruiz-property-group-proposal-2 (service area, services and phone cards removed). Backup total: 6 deploys (90 of 300 credits). Period ends 23 Dec; next 24 Dec 00:00 PST.
