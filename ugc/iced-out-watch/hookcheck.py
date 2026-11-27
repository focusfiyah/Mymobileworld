import json,re
d=json.load(open('/home/user/Mymobileworld/grace/hooks/hooks.json'));H=d if isinstance(d,list) else d.get('hooks',d)
lib={h['id']:(h.get('hook') or h.get('text')) for h in H}
t=open('/home/user/Mymobileworld/ugc/iced-out-watch/script.md').read()
ok=True
for i,line in re.findall(r'^(H\d{3}): (.+)$',t,re.M):
    pat='^'+re.escape(lib[i]).replace('__','.+?')+'$'
    if not re.match(pat,line): ok=False;print('MISMATCH',i,line,'|',lib[i])
print('HOOKS_OK' if ok else 'HOOKS_BAD')
