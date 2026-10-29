# Paste into COMPOSIO_REMOTE_WORKBENCH (Composio_for_Social_Media), then run:  print(run("<hosted pending.json url>"))
# Resumable: finished parts are kept in /mnt/files/repo_media_results.json; re-run until "left": 0.
# Then:  print(results_link())  and  curl -sSL <link> -o results.json  locally, and  media.py record results.json
import json, os, time, requests, threading
from concurrent.futures import ThreadPoolExecutor
ROOTF = "1a_SwrVzG0Jmpi1cYzFTnqj1JySCxd7p2"; ACC = "googledrive_lin-ernst"   # Drive "Repo media (Claude, do not delete)"
FP = "/mnt/files/repo_media_folders.json"; RP = "/mnt/files/repo_media_results.json"
folders = json.load(open(FP)) if os.path.exists(FP) else {}
results = json.load(open(RP)) if os.path.exists(RP) else {}
lock = threading.Lock()

def folder(name, parent):
    k = parent + "/" + name
    with lock:
        if k in folders:
            return folders[k]
        r, e = run_composio_tool("GOOGLEDRIVE_CREATE_FOLDER", {"name": name, "parent_id": parent}, account=ACC)
        if e:
            raise RuntimeError(e)
        folders[k] = r["data"]["id"]; json.dump(folders, open(FP, "w")); return folders[k]

def one(p):
    if p["name"] in results:
        return results[p["name"]]
    fid = folder(p["folder"], folder(p["repo"], ROOTF))
    for a in range(3):
        r, e = run_composio_tool("GOOGLEDRIVE_UPLOAD_FROM_URL", {"source_url": p["kie_url"], "name": p["name"],
                                 "parent_folder_id": fid, "mime_type": "application/x-tar"}, account=ACC)
        if not e and r.get("data", {}).get("id"):
            break
        time.sleep(3)
    else:
        return {"name": p["name"], "error": str(e)}
    did = r["data"]["id"]
    m, e = proxy_execute("GET", f"https://www.googleapis.com/drive/v3/files/{did}", "googledrive",
                         query_params={"fields": "id,size,sha256Checksum"})
    out = {"name": p["name"], "id": did, "folder_id": fid, "size": m.get("size"), "sha256": m.get("sha256Checksum")}
    with lock:
        results[p["name"]] = out; json.dump(results, open(RP, "w"))
    return out

def run(url, workers=8, budget=150):
    items = requests.get(url, timeout=60).json(); t = time.time()
    todo = [p for p in items if p["name"] not in results]
    done = []
    with ThreadPoolExecutor(workers) as ex:
        futs = [ex.submit(one, p) for p in todo]
        for f in futs:
            try:
                done.append(f.result(timeout=max(1, budget - (time.time() - t))))
            except Exception as ex2:
                done.append({"error": repr(ex2)})
    errs = [d for d in done if "error" in d]
    left = [p for p in items if p["name"] not in results]
    return {"items": len(items), "done_now": len(done) - len(errs), "errors": errs[:5], "left": len(left),
            "secs": round(time.time() - t)}

def results_link():
    json.dump(list(results.values()), open("/mnt/files/results_out.json", "w"))
    r, e = upload_local_file("/mnt/files/results_out.json")
    return e or r["s3_url"]
