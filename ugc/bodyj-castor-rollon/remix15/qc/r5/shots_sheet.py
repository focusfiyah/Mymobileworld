"""Round 5 free check: 3 frames per shot (start/mid/end) of each round-4 cut, beside Grace's real hand sheet."""
import json, subprocess, sys
from PIL import Image, ImageDraw
S, OUT = sys.argv[1], sys.argv[2]
hand = Image.open("../../../grace/ref/hand-sheets/without_bracelet.jpg").convert("RGB")
for n in "1234":
    plan = json.load(open(f"out/remix15_v{n}_plan.json"))
    st, ids, end = plan["starts"], plan["shots"], plan["audio"]
    rows = []
    for i, sid in enumerate(ids):
        a, b = st[i], (st[i+1] if i+1 < len(st) else end)
        tiles = []
        for t in (a+0.1, (a+b)/2, b-0.12):
            p = f"/tmp/_f.jpg"
            subprocess.run(["ffmpeg","-v","error","-y","-ss",f"{t:.2f}","-i",f"{S}/v{n}.mp4","-frames:v","1","-vf","scale=270:-1",p], check=True)
            tiles.append(Image.open(p).copy())
        row = Image.new("RGB", (60+3*275, 485), "white"); d = ImageDraw.Draw(row)
        d.text((4, 8), sid, fill="black")
        for k, im in enumerate(tiles): row.paste(im, (60+k*275, 0))
        rows.append(row)
    W = 60+3*275; hs = hand.resize((W, int(hand.height*W/hand.width)))
    cols = 3; per = (len(rows)+cols-1)//cols
    sheet = Image.new("RGB", (W*cols, hs.height + per*485), "white")
    for c in range(cols): sheet.paste(hs, (c*W, 0))
    for i, r in enumerate(rows): sheet.paste(r, ((i//per)*W, hs.height + (i % per)*485))
    sheet.save(f"{OUT}/r4_v{n}_shots.jpg", quality=80); print("ok", n, len(rows))
