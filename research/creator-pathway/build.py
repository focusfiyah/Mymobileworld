"""Builds one word-for-word Markdown doc per course + the community doc. Usage: python3 build.py <work dir>."""
import json,os,re,subprocess,sys,datetime
W=sys.argv[1];os.makedirs(W+'/out',exist_ok=True)
L=json.load(open(W+'/lessons_full.json'))
NAMES={'tiktok-shop':'TikTok Shop','ugc':'UGC','weekly-call-replays':'Weekly Call Replays (Live Coaching)','community-resources':'Community Resources','loom-lessons':'Loom Lessons','mindset':'Mindset'}
def inline(nodes):
    s=''
    for n in nodes or []:
        if n['type']=='text':
            t=n['text'];marks=[m['type'] for m in n.get('marks',[])]
            link=[m for m in n.get('marks',[]) if m['type']=='link']
            if 'bold' in marks: t=f'**{t}**'
            if 'italic' in marks: t=f'*{t}*'
            if link: t=f"[{t}]({link[0]['attrs'].get('href')})"
            s+=t
        elif n['type']=='hardBreak': s+='  \n'
        else: s+=inline(n.get('content'))
    return s
def block(n,ind=''):
    t=n['type'];c=n.get('content')
    if t=='heading': return '#'*min(6,n['attrs'].get('level',2)+2)+' '+inline(c)
    if t=='paragraph': return ind+inline(c)
    if t in('bulletList','orderedList'):
        out=[]
        for i,li in enumerate(c or []):
            mark='-' if t=='bulletList' else f'{i+1}.'
            parts=[block(x,ind+'   ') for x in li.get('content',[])]
            first=parts[0].strip() if parts else ''
            out.append(f'{ind}{mark} {first}'+''.join('\n'+p for p in parts[1:]))
        return '\n'.join(out)
    if t=='blockquote': return '\n'.join('> '+block(x) for x in c or [])
    if t=='codeBlock': return '```\n'+inline(c)+'\n```'
    if t=='horizontalRule': return '---'
    if t=='image': return f"![image]({n.get('attrs',{}).get('src','')})"
    return inline(c)
def desc_md(d):
    if not d: return ''
    if d.startswith('[v2]'):
        try: return '\n\n'.join(block(n) for n in json.loads(d[4:]))
        except Exception: pass
    return d
def fname(r): return re.sub(r'[\\/:*?"<>|]','-',r.get('file_name') or (r.get('title') or 'link')+'.link.txt')
def pdftext(p):
    try: return subprocess.run(['pdftotext','-layout',p,'-'],capture_output=True,text=True,timeout=60).stdout.strip()
    except Exception: return ''
today=datetime.date.today().isoformat()
for k,name in NAMES.items():
    ls=[l for l in L if l['course']==k];o=[f'# Creator Pathway: {name}',f'Pulled word for word from skool.com/creator-pathway-9391 on {today}. {len(ls)} lessons. Video words are Skool\'s own captions (Loom videos: local Whisper transcript).','']
    sec=None
    for l in ls:
        s=' / '.join(x for x in l['path'] if x)
        if s and s!=sec: o+=[f'## {s}',''];sec=s
        n=f"{l['n']:02d}";o+=[f"### {l['title']}",f"Lesson link: https://www.skool.com/creator-pathway-9391/classroom/{l['short']}?md={l['id']}"]
        if l.get('durationS'): o.append(f"Video length: {l['durationS']/60:.0f} min")
        o.append('')
        d=desc_md(l.get('desc'))
        if d.strip(): o+=['**Lesson text (word for word):**','',d,'']
        if l['resources']:
            o.append('**Attached files** (in the Files folder):')
            for r in l['resources']: o.append(f"- {n} {fname(r)}"+(f" ({r['link']})" if r.get('link') else ''))
            o.append('')
        tx=f"{W}/tx/{n}/transcript.txt"
        if os.path.exists(tx):
            t=open(tx).read().strip()
            if '\n' not in t: t=re.sub(r'(?<=[.?!])\s+(?=[A-Z])','\n',t)
            o+=['**Video transcript (word for word):**','',t,'']
        for r in l['resources']:
            p=f"{W}/files/{n} {fname(r)}"
            if p.lower().endswith('.pdf') and os.path.exists(p):
                pt=pdftext(p)
                if pt: o+=[f"**File text: {fname(r)}**",'','```',pt,'```','']
    open(f"{W}/out/{k}.md",'w').write('\n'.join(o))
# community
C=json.load(open(W+'/community_coaching.json'));LL=L
def user(p):
    u=p.get('user') or {}
    return ' '.join(x for x in [u.get('first_name') or u.get('firstName') or '',u.get('last_name') or u.get('lastName') or ''] if x).strip() or u.get('name','')
def when(p): return (p.get('created_at') or p.get('createdAt') or '')[:10]
def comments(cs,depth=0):
    out=[]
    for c in cs or []:
        p=c['post'];out.append(('  '*depth)+f"- **{user(p)}** ({p.get('created_at','')[:10]}): "+(p['metadata'].get('content') or '').replace('\n','\n'+'  '*depth+'  '))
        out+=comments(c.get('children'),depth+1)
    return out
o=[f'# Creator Pathway: Community posts on coaching or 1:1',f'Pulled {today}. {len(C)} threads whose post or comments mention coaching, coach, 1:1, 1 on 1 or one on one, with every comment.','']
for a in sorted(C,key=lambda a:when(a['postTree']['post']),reverse=True):
    p=a['postTree']['post'];m=p['metadata']
    o+=[f"## {m.get('title')}",f"{user(p)}, {when(p)} | {a['url']} | {m.get('upvotes',0)} likes, {m.get('comments',0)} comments",'',m.get('content') or '','']
    slug=a['url'].split('/')[-1][:40]
    for v in json.loads(m.get('videoLinksData') or '[]'): o.append(f"Video link: {v['url']}")
    tx=f"{W}/ctx/{slug}/transcript.txt"
    if os.path.exists(tx): o+=['','**Video transcript (word for word):**','',re.sub(r'(?<=[.?!])\s+(?=[A-Z])','\n',open(tx).read().strip()),'']
    else:
        for v in json.loads(m.get('videoLinksData') or '[]'):
            vid=v['url'].rstrip('/').split('/')[-1]
            hit=[l for l in LL if (l.get('videoLink') or '').endswith(vid)]
            if hit: o.append(f"(Same video as lesson \"{hit[0]['title']}\"; transcript is in the {NAMES[hit[0]['course']]} doc.)")
    atts=json.loads(m.get('attachmentsData') or '[]')
    if atts:
        o+=['','**Attachments** (in the Community attachments folder):']
        for x in atts:
            fn=(x['metadata'].get('file_name') or x['id']);full=f"{slug} - "+re.sub(r'[\\/:*?"<>|]','-',fn);o.append(f"- {full}")
            if full.lower().endswith('.pdf') and os.path.exists(f"{W}/cfiles/{full}"):
                pt=pdftext(f"{W}/cfiles/{full}")
                if pt: o+=['',f"**Attachment text: {fn}**",'','```',pt,'```','']
    o+=['','**Comments:**']+comments(a.get('comments'))+['']
open(f"{W}/out/community.md",'w').write('\n'.join(o))
for f in os.listdir(W+'/out'):
    if f.endswith('.md'): subprocess.run(['pandoc',f"{W}/out/{f}",'-o',f"{W}/out/{f[:-3]}.docx"],check=True)
print('BUILT',sorted(os.listdir(W+'/out')))
