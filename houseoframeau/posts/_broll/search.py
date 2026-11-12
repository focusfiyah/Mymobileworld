import json,os,sys,urllib.request,urllib.parse
UA="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"
out={}
for q in sys.argv[1:]:
    u="https://api.pexels.com/videos/search?"+urllib.parse.urlencode({"query":q,"orientation":"portrait","per_page":12,"size":"medium"})
    r=json.load(urllib.request.urlopen(urllib.request.Request(u,headers={"Authorization":os.environ["PEXELS_API_KEY"],"User-Agent":UA}),timeout=30))
    for v in r["videos"]:
        fs=[f for f in v["video_files"] if f.get("width") and f["width"]>=1080 and f["height"]>f["width"]]
        if not fs: continue
        f=min(fs,key=lambda f:f["width"])
        out[v["id"]]={"q":q,"url":v["url"],"dur":v["duration"],"w":f["width"],"h":f["height"],"link":f["link"],"img":v["image"]}
json.dump(out,open("cand.json","w"),indent=1); print(len(out))
for k,v in out.items(): print(k,v["dur"],v["w"],v["q"],v["url"].split("/video/")[1][:70])
