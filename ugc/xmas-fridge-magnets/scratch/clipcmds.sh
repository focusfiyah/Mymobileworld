python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S1 --prompt-file prompts/S1_wan.txt --still stills/S1.png --ref refs/closeups/tree.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S1.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S3 --prompt-file prompts/S3_wan.txt --still stills/S3.png --ref refs/closeups/tree.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S3.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S4 --prompt-file prompts/S4_wan.txt --still stills/S4.png --ref refs/closeups/santa.png --ref refs/closeups/reindeer.png --ref refs/closeups/gifts.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S4.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S6 --prompt-file prompts/S6_wan.txt --still stills/S6.png --ref refs/closeups/tree.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S6.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S7 --prompt-file prompts/S7_wan.txt --still stills/S7.png --ref refs/closeups/tree.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S7.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S8 --prompt-file prompts/S8_wan.txt --still stills/S8.png --ref refs/closeups/reindeer.png --ref refs/closeups/santa.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S8.log 2>&1 &
python3 ../../.claude/skills/ugc-product-ad/scripts/wan_clip.py . S9 --prompt-file prompts/S9_wan.txt --still stills/S9.png --ref refs/closeups/tree.png --ref refs/closeups/santa.png --ref refs/product_sheet.png --seconds 5 > scratch/wan_S9.log 2>&1 &
python3 run.py seedance S2 > scratch/seed_S2.log 2>&1 &
wait; echo ALL_CLIPS_DONE
