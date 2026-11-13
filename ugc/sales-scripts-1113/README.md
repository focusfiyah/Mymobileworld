# Scripts for Grace's 5 selling videos (2026-11-13)

Status: DONE 2026-11-13, $0. Grace (Telegram group msg 493) sent 5 TikToks that made sales and asked for a voiceover script + a talk-to-camera script per product. All 5 logged in the sales tracker (grace/winners, sheet updated to 13 rows); each product went through the full Grace script gate (`python3 check.py gates` -> ALL_GATES_OK; `check.py scripts` -> SCRIPTS_OK); docs in Drive; Grace sent each on Telegram (msgs 499-503, ✅), Ralph told. Open: Grace's real sales counts (logged as 1 each) and her selling points (she offered, msg 496; asked for them).

| Product | Job folder | Drive folder | Doc |
|---|---|---|---|
| Haiti flag | haiti-flag/ | https://drive.google.com/drive/folders/1A5gJn-h-3vbgsmujYrMNWmGIA_OzntQo | Scripts - Haiti Flag (1nOQRFOxSF_jidL7YsCUMNKBTN15qkiHigjq50ReZlpA) |
| ili New York glasses case | ili-case/ | https://drive.google.com/drive/folders/1zqUWpLuZuvFU9nl1HUnSxPhGO3VfF5IC | Scripts - ili Eyeglass Case (1-CHmpNGsME7yioXjbYk07tYofJYxvLvFV24avOyoyDM) |
| Anthem meat sticks + jerky | meat-sticks/ | https://drive.google.com/drive/folders/1Mu9n46JVvRQ3Wo_dUOPjqqWt59YzGyG6 | Scripts - Meat Sticks + Jerky Pack (1Gt_CG7oX00_GCmhuEo-6Zv1GF0BpzbL30kp7PMng4-M) |
| Bobbi Brown Prep and Brighten Duo | bobbi-prep-duo/ | https://drive.google.com/drive/folders/1l2ibq62j_fNuFpFIhtV2zVCth6tPEEwD (new, + Originals 1kcw9UFuUtToFjKgyIDuVDTobeZM-e3Ej) | Scripts - Bobbi Brown Prep and Brighten Duo (1go6oMpg0gNaxIjxRV_wRhF8FBMe4l0W0f5RoCFMDMCk) |
| Asvivid reversible mock neck | mock-neck-sweatshirt/ | https://drive.google.com/drive/folders/1DR0W-VxVJzUyiga0Z0Vb_hHxeTiZc8-y | Scripts - Reversible Mock Neck Sweatshirt (1AV48BDKVAv8SLv-W5E_bx71vUx5Mc6dYrDE5IFNlRos) |

Files: `check.py` (scripts / gates / selftest), `build_doc.py` (scripts.md + RESEARCH verdict -> doc HTML), `GATES.md`. The research verdict is a section in each Scripts doc (not a separate doc).
Notes: the 5 winners are music-only real footage (no VO), so the "script as posted" column holds the on-screen text. Hooks are library hooks word for word (task brief); claims flagged per product in `<product>/research/product_facts.md`. Tool issues seen this session: TikTok hashtag pages/viral board returned 0 videos (rebuilt from discover pages), the Haiti flag listing page hit a captcha (facts from the G128 store + Amazon), `audience.py` needs video ids passed to pull comments, `lookup.py holidays HT` crashes (TypeError).
