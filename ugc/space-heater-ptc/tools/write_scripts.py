"""scripts.md from shots.json + vo/*.txt (the human-readable script + shot list Ralph reviews)."""
import json
S = json.load(open('shots.json'))['shots']
meta = {"V1": ("One cold room (rooms tour)", "H063 Recognition", "I know I cannot be the only one who __", "Modeled on @myfamilypov 765K (each feature + where you use it: 'from bed, your office or garage') and @shun50111 115K (rooms named one by one)."),
        "V2": ("Safety, kids and pets", "H027 Reassurance", "Before you buy this, look at __", "Answers the top audience questions ('are space heaters safe', 'safe for pets'); modeled on @camronnbrown 3.1M (features one by one, what each does)."),
        "V3": ("6 a.m. demo, humor", "H126 Humor", "I am apparently at the age where this excites me", "Identity humor like @drezilla13 'My emotional support heater' (16.5% eng) and @kris.hc.home (13.8% eng); top-panel demo like @myfamilypov.")}
caps = dict(l.split(": ", 1) for l in open('vo/captions.txt').read().strip().splitlines())
L = ["# Antarctic Star 1500W PTC space heater: script (Grace, hands-only AI video)", "",
     "Voice: Grace C (eleven_v4), loudnorm -16 LUFS. No on-screen text. Every shot a moving clip, 6 rooms. Close: \"It's in the orange cart.\"", ""]
for v, (name, hid, tmpl, why) in [("V1", meta["V1"])]:   # Ralph 2026-10-19: one script, the best one
    vo = open(f'vo/{v}.txt').read().strip(); n = len(vo.split())
    L += [f"## {v}: {name}", f"Hook: {hid} \"{tmpl}\" (word for word, blank filled). {why}", f"~{n} words, about {n/3.2:.0f} s at Grace's pace.", "",
          vo, "", f"Caption: {caps[v]}", "", "| Shot | Line | Room | Type | What we see | Motion |", "|---|---|---|---|---|---|"]
    L += [f"| {s['id']} | {s['line']} | {s['room'].split('/')[-1][3:-4]} | {s['kind']} | {s['still']} | {s['motion']} |" for s in S if s['video'] == v]
    L.append("")
open('scripts.md', 'w').write("\n".join(L))
