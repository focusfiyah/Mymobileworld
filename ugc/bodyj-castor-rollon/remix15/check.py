"""Gate checks for the 15 s remixes. python3 check.py ref|inventory|scripts|cuts"""
import json, os, re, subprocess, sys
J = os.path.dirname(os.path.abspath(__file__))
def dur(p):
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",p],capture_output=True,text=True).stdout)
def ref():
    d = os.path.join(J, "ref/7697844264050511135")
    assert 31 < dur(os.path.join(d, "video.mp4")) < 33, "posted video length"
    assert "liquid gold" in open(os.path.join(d, "transcript.txt")).read().lower()
    print("REF_OK")
def inventory():
    t = open(os.path.join(J, "INVENTORY.md")).read()
    clips = sorted(f[:-4] for f in os.listdir(os.path.join(J, "../clips")) if f.endswith(".mp4"))
    miss = [c for c in clips if f"| {c} |" not in t]
    assert len(clips) == 12 and not miss, f"missing rows {miss}"
    print("INVENTORY_OK", len(clips))
def scripts():  # scripts.json: [{"id","text"}] x4, each 38-52 words, grade <= 6, no banned phrase
    S = json.load(open(os.path.join(J, "scripts.json")))
    assert len(S) == 4, "need 4 scripts"
    ban = ["order it now", "order now", "heads up", "the label says", "reviewer", "selling out", "$", "—", " - "]
    for s in S:
        w = len(s["text"].split()); assert 38 <= w <= 52, f'{s["id"]}: {w} words'
        g = subprocess.run([sys.executable, os.path.join(J, "../../../.claude/skills/tiktok-shop-coach/scripts/tiktok.py"), "readability", s["text"]], capture_output=True, text=True).stdout
        m = re.search(r"grade\D*([\d.]+)", g, re.I); assert m and float(m.group(1)) <= 6, f'{s["id"]}: grade {m and m.group(1)}'
        hit = [b for b in ban if b in s["text"].lower()]; assert not hit, f'{s["id"]}: banned {hit}'
    print("SCRIPTS_OK")
def cuts():  # out/remix15_v{1..4}_final.mp4, 1080x1920, 13.5-16.5 s, edit lists all different
    edits = json.load(open(os.path.join(J, "edits.json")))
    assert len({json.dumps(e["shots"]) for e in edits.values()}) == 4, "edit lists not all different"
    for v in range(1, 5):
        p = os.path.join(J, f"out/remix15_v{v}_final.mp4")
        wh = subprocess.run(["ffprobe","-v","error","-select_streams","v:0","-show_entries","stream=width,height","-of","csv=p=0",p],capture_output=True,text=True).stdout.strip()
        assert wh == "1080,1920", f"v{v} {wh}"; assert 13.5 <= dur(p) <= 16.5, f"v{v} {dur(p):.2f}s"
    print("CUTS_OK")
{"ref": ref, "inventory": inventory, "scripts": scripts, "cuts": cuts}[sys.argv[1]]()
