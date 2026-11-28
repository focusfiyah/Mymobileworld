"""Hide fake account-recovery spam on @azariah2244 TikTok videos (Ralph 2026-11-28: "Yea go ahead" to hiding them automatically).
Scam rings tag a fake "support"/"recovery" account ("@GEORGE_AGENCY :Help", "@blaze_cyber request help") or plant a setup line
("TT be frustrating, fixed mine", "Same, but mine was fixed"). TikTok refuses deleting other people's comments, so we hide them
(only the poster still sees them). Real comments (A/B votes, CHECK, questions) are never touched.
  python3 hide_spam.py [--dry]      -> prints HIDE / KEEP lines and SPAM_HIDDEN n
"""
import os, re, sys, json, requests
from requests.adapters import HTTPAdapter, Retry
S = requests.Session(); S.mount("https://", HTTPAdapter(max_retries=Retry(total=5, backoff_factor=2, allowed_methods=None, status_forcelist=[429, 500, 502, 503, 504])))
H = {"Authorization": f"Bearer {os.environ['Zernio_API_key']}"}; A = "6aec2c7b28ab1d8605a419e0"; B = "https://zernio.com/api/v1"
TAG = re.compile(r"@\S+.*\b(help|request|support|recover|fix|hack|agency|tech|consult|assist)", re.I)
TAG2 = re.compile(r"\b(help|request)\b.*@\S+", re.I)
SETUP = re.compile(r"(fixed mine|got mine fixed|mine was fixed|be frustrating|recommend you to @|helped me|highly recommend)", re.I)
KEEP = re.compile(r"\?|\b[AB]\b")   # questions and A/B votes are real people
def spam(msg): return not KEEP.search(msg) and bool(TAG.search(msg) or TAG2.search(msg) or SETUP.search(msg))
dry = "--dry" in sys.argv; n = 0
vids = S.get(f"{B}/inbox/comments", headers=H, params={"accountId": A}, timeout=60).json()["data"]
for v in vids[:20]:
    if not v.get("commentCount"): continue
    for x in S.get(f"{B}/inbox/comments/{v['id']}", headers=H, params={"accountId": A}, timeout=60).json().get("comments", []):
        if x.get("isHidden") or (x.get("from") or {}).get("username") == "azariah2244": continue
        if spam(x["message"]):
            print("HIDE", v["id"], x["id"], repr(x["message"][:80]))
            if not dry:
                r = S.post(f"{B}/inbox/comments/{v['id']}/{x['id']}/hide", headers={**H, "Content-Type": "application/json"}, json={"accountId": A}, timeout=60)
                n += r.status_code == 200 and r.json().get("hidden") is True
        else: print("KEEP", v["id"], repr(x["message"][:80]))
print("SPAM_HIDDEN", n)
