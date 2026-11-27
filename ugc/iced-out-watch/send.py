import json,os,re,html,urllib.request
T=os.environ['TELEGRAM_BOT_TOKEN'];CHAT=-5234107715;R=842
s=open('script.md').read()
why=re.findall(r'^WHY\d: (.+)$',s,re.M)
hooks=re.findall(r'^H\d{3}: (.+)$',s,re.M)
script=s.split('## Script (any hook above, then)\n')[1].strip()
msgs=[]
msgs.append(("Why the original worked:\n\n1. "+"\n\n2. ".join(why[:1]+why[1:2])+"\n\n3. "+why[2]+"\n\n4. "+why[3]+"\n\nWhat we keep: point at each feature on camera, one mini demo, a friend-flexing-a-find tone and a real reason to buy now. New: your angle is shopping for him before Christmas.\n\nThree hooks next, each on its own so you can copy it. Then the script, which works after any of them.",None))
for h in hooks: msgs.append((h,'pre'))
msgs.append((script,'pre'))
msgs.append(("Notes:\n\n• Your footage fits this as a voiceover: wrist turns, face close-ups, the date window. Show the stones on the band for line 2, the blue hands for line 3.\n• The dial has a brand-style name printed on it. Keep it soft or out of the tight close-ups, and never say a brand name. I also kept the word \"diamond\" out: they're stones.\n• His video said automatic movement. Yours is quartz, so the script says quartz.\n• I left out the glow-in-the-dark hands, the adjuster and the clasp because I couldn't confirm them on the listing. If the listing shows them, a quick lights-off shot would be a great extra line.\n• If there's a real Black Friday deal on it, you can add \"and it's on sale right now\" before the last line.\n• Peel the plastic off the band before filming.",None))
out=[]
for text,mode in msgs:
    body={'chat_id':CHAT,'reply_to_message_id':R,'allow_sending_without_reply':True}
    if mode=='pre': body.update(text='<pre>'+html.escape(text,quote=False)+'</pre>',parse_mode='HTML')
    else: body['text']=text
    req=urllib.request.Request(f'https://api.telegram.org/bot{T}/sendMessage',json.dumps(body).encode(),{'Content-Type':'application/json'})
    r=json.load(urllib.request.urlopen(req));out.append({'ok':r.get('ok'),'id':r.get('result',{}).get('message_id')})
json.dump(out,open('sent.json','w'));print(out)
