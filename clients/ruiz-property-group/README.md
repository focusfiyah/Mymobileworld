# Ruiz Property Group LLC (client: Luigi Ruiz)
Property management + buy, fix and flip investor (his voice note, 2026-11-24). Job note: obsidian-vault `Brain/Jobs/Ruiz Property Group.md`.
- `proposal/`: proposal page source (Day One AI brand). `build.py` writes the artifact page and the Netlify page. Live: https://ruiz-property-group-proposal.netlify.app
- `site/`: preview landing page (own brand: brick red on bluestone, Archivo condensed + Hanken Grotesk). Live: https://ruiz-property-group-preview.netlify.app. Photos (`site/img/`, not in git) are Pexels stand-ins listed in `SOURCES.md`.
- `GATES.md`: acceptance gates. Netlify site ids: proposal 778bc082-f718-414b-915a-d10e3b9f5a2a, preview 76bb97a6-5f41-4f95-aaad-dd6befebedbe (both on Ralph's account for now; move to Luigi's own account at launch).
- Deploy: zip the folder, POST to /api/v1/sites/{id}/deploys. Needs a `_headers` file giving `/` and `/index.html` Content-Type text/html (zip deploys were served as text/plain without it).
