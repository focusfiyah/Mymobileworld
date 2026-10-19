# Fallback for `tiktok.py video` when TikTok's video pages return "Site Maintenance": take full item structs from hashtag pages.
import asyncio,json,os,sys
sys.path.insert(0,'/home/user/Mymobileworld/.claude/skills/tiktok-shop-coach/scripts')
import tiktok
from playwright.async_api import async_playwright
out=sys.argv[1]; tags=sys.argv[2].split(','); ids=set(sys.argv[3].split(','))
async def m():
    async with async_playwright() as p:
        b,ctx=await tiktok.new_ctx(p); items={}
        for t in tags: items.update(await tiktok.collect_tag(ctx,t))
        for i,it in items.items():
            if str(it.get('id')) not in ids: continue
            meta=tiktok.summarize(it); d=os.path.join(out,meta['id']); os.makedirs(d,exist_ok=True)
            segs,_=await tiktok.download_video(ctx,it,d); meta['has_transcript']=bool(segs)
            json.dump(meta,open(os.path.join(d,'meta.json'),'w'),indent=2); print('OK',meta['url'],meta['views'],'transcript',bool(segs))
        print('missing',ids-{str(k) for k in items})
        await b.close()
asyncio.run(m())
