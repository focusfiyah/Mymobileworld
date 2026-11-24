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
