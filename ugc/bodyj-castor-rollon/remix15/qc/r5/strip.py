"""Frames every 0.25 s across one shot of a cut -> strip (find when a hand enters)."""
import json, subprocess, sys
from PIL import Image, ImageDraw
S, n, sid, out = sys.argv[1:5]
plan = json.load(open(f"out/remix15_v{n}_plan.json")); i = plan["shots"].index(sid)
a = plan["starts"][i]; b = plan["starts"][i+1] if i+1 < len(plan["starts"]) else plan["audio"]
ts = [a + k*0.25 for k in range(int((b-a)/0.25)+1)]
tiles = []
for t in ts:
    subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.2f}","-i",f"{S}/v{n}.mp4","-frames:v","1","-vf","scale=180:-1","/tmp/_s.jpg"], check=True)
    im = Image.open("/tmp/_s.jpg").copy(); ImageDraw.Draw(im).text((4,4), f"{t-a:.2f}", fill="red"); tiles.append(im)
st = Image.new("RGB", (180*len(tiles), tiles[0].height), "white")
for k, im in enumerate(tiles): st.paste(im, (k*180, 0))
st.save(out); print(sid, f"len {b-a:.2f}s")
