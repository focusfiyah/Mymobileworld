#!/usr/bin/env python3
"""Gate check for houseoframeau/videos.json: every public video from the Composio pull, shop products filled."""
import json, os, sys
db = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "videos.json")))
vs = db["videos"]
if len(vs) != db["stats"]["videos"] or len({v["id"] for v in vs}) != len(vs):
    print("FAIL", len(vs), "rows vs", db["stats"]["videos"], "videos on the account"); sys.exit(1)
bad = [v["id"] for v in vs if v["shop_video"] and not v["product"]]
if bad or not any(v["shop_video"] for v in vs):
    print("FAIL shop rows without product", bad); sys.exit(1)
print("PASS houseoframeau", len(vs), "videos,", sum(v["shop_video"] for v in vs), "shop")
