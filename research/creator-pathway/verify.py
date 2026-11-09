"""Checks for the Creator Pathway pull. Usage: python3 verify.py <gate>. Work dir from env CP_WORK."""
import json,os,sys,glob
W=os.environ.get('CP_WORK','/tmp/claude-0/-home-user/c5113556-fd28-502d-a836-f2da8d77f539/scratchpad')
L=json.load(open(W+'/lessons_full.json')) if os.path.exists(W+'/lessons_full.json') else []
g=sys.argv[1];bad=[]
if g=='crawl':
    if len(L)!=70: bad.append(f'{len(L)} lessons')
    bad+= [l['title'] for l in L if l.get('err') or (l.get('videoId') and not l.get('m3u8'))]
elif g=='audio':
    bad=[l['title'] for l in L if (l.get('videoId') or l.get('videoLink')) and not os.path.getsize(f"{W}/audio/{l['n']:02d}.m4a") if os.path.exists(f"{W}/audio/{l['n']:02d}.m4a")] + [l['title'] for l in L if (l.get('videoId') or l.get('videoLink')) and not os.path.exists(f"{W}/audio/{l['n']:02d}.m4a")]
elif g=='transcripts':
    bad=[l['title'] for l in L if (l.get('videoId') or l.get('videoLink')) and not (os.path.exists(f"{W}/tx/{l['n']:02d}/transcript.txt") and os.path.getsize(f"{W}/tx/{l['n']:02d}/transcript.txt")>50)]
elif g=='files':
    import re
    nm=lambda r:re.sub(r'[\\/:*?"<>|]','-',r.get('file_name') or (r.get('title') or 'link')+'.link.txt')
    want=[(l['n'],nm(r)) for l in L for r in l['resources']]
    bad=[f"{n}:{f}" for n,f in want if not (os.path.exists(f"{W}/files/{n:02d} {f}") and os.path.getsize(f"{W}/files/{n:02d} {f}")>0)]
elif g=='community':
    p=W+'/community_coaching.json'
    if not os.path.exists(p) or len(json.load(open(p)))==0: bad.append('no community posts saved')
elif g=='docs':
    for c in ['tiktok-shop','ugc','weekly-call-replays','community-resources','loom-lessons','mindset']:
        if not os.path.exists(f"{W}/out/{c}.md"): bad.append(c)
print('\n'.join(map(str,bad[:20])))
print(f'{g.upper()}_OK' if not bad else f'{g.upper()}_FAIL {len(bad)}')
sys.exit(1 if bad else 0)
