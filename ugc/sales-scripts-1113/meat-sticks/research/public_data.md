# Public data: Anthem meat sticks beef jerky

Source: tools/public_apis/lookup.py (Open Food Facts, Open Beauty Facts, openFDA), $0.
Open data is user-submitted and unvalidated: a lead to check against the real photos/listing, never a claim on its own.

## Product lookup
### food: 0 match(es)
- none found
### beauty: 0 match(es)
- none found

## Recall check (openFDA)
### food: 0 recall(s)
- none found
### drug: 0 recall(s)
- none found
### device: 0 recall(s)
- none found

## What it means for the script
- **Matches this exact product?** The job lookup ("Anthem meat sticks beef jerky") found 0 rows. A narrower Open Food Facts search ("Anthem beef stick", saved in `research/public/food_anthem.txt`) found 5 ANTHEM rows: HOT HONEY BEEF STICK (0850010448862), Chimichurri Beef Stick, Dill Pickle Beef Stick, Beef Stick (0850010448510), Beef Stick Hot Honey. Brand and flavor names match two of the four sticks in this pack (Original beef, Hot Honey beef). Every row has empty ingredients and quantity, so the database adds no fact we can use. Nothing about the turkey or chicken sticks or the Sweet Heat jerky.
- **Any recall on this brand or type to avoid in claims?** openFDA: 0 food, drug or device recalls for the brand words. The type searches ("beef jerky", "meat stick", `research/public/recalls_*.txt`) only hit other firms (jerky seasoning with undeclared peanuts 2014, seasoning Salmonella 2023, ground elk E. coli 2015). None is Anthem. Note: meat sticks and jerky are USDA FSIS products, which openFDA does not cover, so this check is partial. The scripts make no safety, health or "clean" medical claim, so nothing to steer around.
- **Anything to verify on the real photos:** (1) which sticks say ZERO SUGAR: seen on the pink TURKEY and red ORIGINAL BEEF wrappers in Grace's frames, not readable on Hot Honey (honey, so do not say all are zero sugar); (2) "100% American beef" is on the BEEF STICK wrappers only, never on turkey or chicken; (3) "gluten free" is printed on the stick wrappers and is in the listing for the jerky. Dated urgency: `research/public/holidays.txt` (Nager.Date) gives Thanksgiving 2026-11-26 and Christmas 2026-12-25, so "the holidays" is a real reason.
