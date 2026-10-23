"""Build the live rules text from REMEMBER_ME.txt and host it, for the Drive doc "Ralph standing rules (live)".

Ralph 2026-10-22: rule changes he OKs are saved everywhere by Claude and only confirmed to him; no more pasting.
Every claude.ai chat/project reads the Drive doc (his profile preferences point to it by title).

usage: python3 handoff/live_rules.py   -> prints a hosted URL. Then, in the session:
  1. Composio GOOGLEDRIVE_UPLOAD_FROM_URL (account googledrive_lin-ernst), source_url = that URL,
     name = "Ralph standing rules (live)", mime_type = application/vnd.google-apps.document
  2. read the new doc back (Google Drive connector read_file_content) and check the new rule is in it
  3. trash the old doc (Drive connector trash_file) so exactly one doc has that title; put the new id in LIVE_DOC.txt
"""
import os, pathlib, requests

H = pathlib.Path(__file__).parent
body = (H / "REMEMBER_ME.txt").read_text().split("\n", 2)[2]   # drop the "Remember all of this..." opener
text = ("RALPH STANDING RULES (LIVE). Claude keeps this doc current whenever Ralph OKs a rule change; the newest dated "
        "rule wins. Read it at the start of any task for Ralph or Grace. Source: GitHub focusfiyah/Mymobileworld "
        "handoff/REMEMBER_ME.txt (main).\n\n" + body)
out = H / "live_rules.txt"
out.write_text(text)
key = os.environ.get("KIE_API_KEY")   # the proxy injects auth for Kie; a key is only needed outside the cloud
r = requests.post("https://kieai.redpandaai.co/api/file-stream-upload",
                  headers={"Authorization": f"Bearer {key}"} if key else {},
                  files={"file": (out.name, text.encode())}, data={"uploadPath": "live-rules"}, timeout=120)
url = r.json()["data"]["downloadUrl"]
assert requests.get(url, timeout=60).text == text, "hosted copy differs"
print(url)
