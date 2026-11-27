"""Baby Girl Floral Cherry 10-Piece Set (Grace edit, 2026-11-27): hard cuts of Grace's real footage, silent.
V1: up to 29 s, every set + the stretch features, Grace adds music (her msg 843).
V2: cut to the voiceover script (scripts.md) Grace records herself; different moments, order and framing (1.12x punch-in) from V1.
Sources: orig/IMG_09xx.MOV (her Drive originals, 1080x1920 after rotation, 30 fps, no talking).
Sets: 0923 leopard-heart, 0924 pink hearts, 0925 white floral, 0926 burgundy big flower, 0927 burgundy rainbow;
0921 flip through all sets; 0928 rainbow top stretch; 0929 rainbow pants stretch; 0930 floral pants waistband/leg stretch.
Run: python3 cut.py v1|v2 [preset]"""
import subprocess, sys, json, os

PLANS = {
  "v1": {"zoom": 1.0, "segs": [
    ("0921", 6.3, 10.6, 1.25),  # hook: pants of four sets fanned one after another (1.25x)
    ("0923", 0.6, 2.6),    # set 1 leopard-heart
    ("0924", 0.4, 2.4),    # set 2 pink hearts
    ("0925", 1.0, 3.0),    # set 3 white floral
    ("0926", 1.0, 3.0),    # set 4 burgundy big flower
    ("0927", 0.3, 2.3),    # set 5 burgundy rainbow
    ("0928", 1.8, 4.8),    # stretch: rainbow top neckline
    ("0929", 0.2, 3.0),    # stretch: rainbow pants leg
    ("0930", 0.0, 2.6),    # stretch: floral waistband
    ("0921", 22.5, 25.2, 1.25),  # end: tops flip, rainbow to big flower (1.25x)
  ]},
  "v2": {"zoom": 1.12, "segs": [
    ("0921", 14.7, 18.3, 1.25),  # L1 You're not behind on laundry. (tops flip, leopard to hearts, 1.25x)
    ("0925", 9.0, 10.8),   # L2 Your baby goes through clothes faster...
    ("0923", 3.2, 4.8),
    ("0927", 4.6, 6.4),    # L3 With ten pieces, a clean one's ready...
    ("0924", 8.0, 9.8),
    ("0924", 3.0, 5.2),    # L4 soft and breathable (fingers on the fabric)
    ("0926", 12.8, 14.6),
    ("0928", 8.0, 10.4),   # L5 They stretch... (sleeve)
    ("0930", 5.4, 7.4),    #    (pants leg)
    ("0921", 18.8, 22.4, 1.25),  # L6 Stock her drawer... (tops flip, floral to rainbow, 1.25x)
    ("0927", 7.4, 9.2),    # L7 It's in the orange cart.
  ]},
}

def render(tag, preset="medium"):
    p = PLANS[tag]; segs = p["segs"]; z = p["zoom"]
    crop = f",crop=iw/{z}:ih/{z}" if z != 1.0 else ""
    ins = []
    f = ""
    segs = [x if len(x) == 4 else (*x, 1.0) for x in segs]
    for i, (s, a, b, sp) in enumerate(segs):
        ins += ["-ss", str(a), "-t", str(round(b - a, 3)), "-i", f"orig/IMG_{s}.MOV"]
        f += f"[{i}:v]setpts=(PTS-STARTPTS)/{sp},fps=30{crop},scale=1080:1920:flags=lanczos,setsar=1,format=yuv420p[v{i}];"
    f += "".join(f"[v{i}]" for i in range(len(segs))) + f"concat=n={len(segs)}:v=1:a=0[out]"
    out = f"out/cherry_{tag}.mp4"
    subprocess.run(["ffmpeg", "-v", "error", "-y", *ins, "-filter_complex", f, "-map", "[out]", "-an", "-c:v", "libx264",
                    "-preset", preset, "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "-threads", "4", out], check=True)
    durs = [(b - a) / sp for _, a, b, sp in segs]
    json.dump({"segs": [[0, round(d, 3)] for d in durs], "src": segs, "zoom": z,
               "expected": round(sum(durs), 2)}, open(f"out/cherry_{tag}.json", "w"))
    print(out)

if __name__ == "__main__":
    os.makedirs("out", exist_ok=True)
    render(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else "medium")
