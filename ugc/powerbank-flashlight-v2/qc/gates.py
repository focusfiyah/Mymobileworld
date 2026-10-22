"""Gate checks for Flashlight V2 (GATES.md). python3 qc/gates.py <name>; prints <NAME>_OK only when every assertion passes."""
import json, pathlib, re, subprocess, sys
J = pathlib.Path(__file__).resolve().parent.parent
RALPH = ["Who in the world made this???",
 "Because what do you mean I can charge my phone with this, hang it up in my tent for hands-free lighting, AND use it as a regular flashlight with a focused beam?",
 "And it has a flickering mode, too, for emergencies!",
 "This is the kind of gadget that makes sense to keep with your camping gear or emergency kit.",
 "And it costs less than a McDonald's Happy Meal!",
 "I'm linking it in the orange cart for you!"]

def script():
    lines = [l.strip() for l in (J/"research/script.txt").read_text().splitlines() if l.strip()]
    assert lines == RALPH, "script differs from Ralph's words (flashing->flickering is his own fix)"
    return "SCRIPT_OK"

def size():
    t = (J/"research/size.md").read_text()
    assert "29.5 x 29.5 x 157 mm" in t and "90 g" in t and (J/"refs/box_specs_grace.jpg").exists()
    assert (J/"refs/view_hook_upright.png").exists()
    return "SIZE_OK"

def storyboard():
    t = (J/"review/storyboard.html").read_text()
    for s in range(1, 10): assert f'class="num">S{s}<' in t, f"S{s} missing"
    assert t.count("real_hook.jpg") >= 2 and "15.7 cm" in t and "McDonald" in t and "front lens" in t
    return "STORYBOARD_OK"

def stills():
    miss = [f"S{i}" for i in range(1, 10) if not (J/f"stills/S{i}.png").exists()]
    assert not miss, "missing " + " ".join(miss)
    return "STILLS_OK"

def clips():
    miss = [f"S{i}" for i in range(1, 10) if not (J/f"clips/S{i}.mp4").exists()]
    assert not miss, "missing " + " ".join(miss)
    return "CLIPS_OK"

def gate():
    out = subprocess.run(["python3", "grace/gate.py", "ugc/powerbank-flashlight-v2"], cwd=J.parent.parent, capture_output=True, text=True)
    assert "GATE OK" in out.stdout + out.stderr, (out.stdout + out.stderr)[-600:]
    return "SCRIPTGATE_OK"

if __name__ == "__main__":
    try: print(globals()[sys.argv[1]]())
    except AssertionError as e: print("FAIL:", e); sys.exit(1)
