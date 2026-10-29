# Paste into COMPOSIO_REMOTE_WORKBENCH with IDS = the list printed by  media.py need UNIT , then:
#   curl -sSL <printed link> -o links.json   and   media.py get UNIT links.json   (links last 1 hour)
import json
IDS = []   # paste here
links = {}
for i in IDS:
    d, e = run_composio_tool("GOOGLEDRIVE_DOWNLOAD_FILE", {"fileId": i}, account="googledrive_lin-ernst")
    links[i] = d["data"]["downloaded_file_content"]["s3url"] if not e else None
json.dump(links, open("/mnt/files/links.json", "w"))
r, e = upload_local_file("/mnt/files/links.json"); print(e or r["s3_url"], sum(v is None for v in links.values()), "failed")
