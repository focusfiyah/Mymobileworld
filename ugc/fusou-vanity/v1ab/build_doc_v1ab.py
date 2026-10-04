"""Adds Grace's two V1 script versions (A, B) to the Drive scripts doc (Ralph 2026-10-04). Reads out/fusou_scripts_final.html (the 6 hands-only videos),
inserts a V1A/V1B section before "Video 1:" and writes out/fusou_scripts_final.html again. Run from ugc/fusou-vanity:  python3 v1ab/build_doc_v1ab.py
Timings come from the final v5 cut (v1ab/cut_ab.py EDL2, face=2)."""
import html, json, re, sys, os
sys.path.insert(0, os.getcwd()); sys.path.insert(0, "v1ab")
import cut_ab as C
DRIVE = {"A": "1cz_477QXARcQ1hDi1szs-DcfPwATwApp", "B": "1CWsMqHmF_L2RMuKmkh2cTJBlSjODdJqj"}
SCREEN = {"A": ["Grace at the bathroom mirror putting blush on her cheek under dull, flat bathroom light (face shown, mouth closed)",
                "Whole vanity in daylight, slow push-in toward it",
                "Whole vanity, the mirror light changes colour: cold white, warm white, dimmer, warm yellow",
                "Whole vanity, wide", "All the drawers open, slow push-in", "Hand opens the mirror door: bags on the shelves inside",
                "Hand pulls the stool drawer open", "Whole vanity, wide, slow push-in"],
          "B": ["Grace at the bathroom mirror putting blush on her cheek under dull, flat bathroom light (face shown, mouth closed)",
                "Whole vanity in daylight, slow push-in toward it",
                "Whole vanity, the mirror light changes colour: cold white, warm white, dimmer, warm yellow",
                "Whole vanity, wide", "Drawers open, hand lifts a lipstick out of the glass-top tray", "Hand opens the mirror door: bags on the shelves inside",
                "Hand pulls the stool drawer open", "Whole vanity, wide, slow push-in"]}
HOOKS = {"A": ["the lighting nobody checks", "your bathroom light is lying", "my teenage self would be SCREAMING"],
         "B": ["the lighting lied", "watch the light change", "why does it look different outside"]}
md = open("v1ab/scripts.md").read()


def part(v):
    cap = re.search(rf"Caption {v}: (.+)", md).group(1)
    edl, _, end = C.EDL2(v, face=2); words = C.words(v); st = [s for s, _ in edl] + [end]
    assert len(edl) == len(SCREEN[v]), (v, len(edl))
    rows = []
    for i in range(len(edl)):
        said = " ".join(w["text"] for w in words if st[i] - 0.05 <= w["start"] < st[i + 1] - 0.05)
        rows.append(f"<tr><td>{st[i]:.1f}–{st[i + 1]:.1f}s</td><td>{html.escape(said) or '<i>(no voice)</i>'}</td><td>{html.escape(SCREEN[v][i])}</td></tr>")
    full = " ".join(x["line"] for x in json.load(open(f"v1ab/vo/v{v}_final_lines.json")))
    name = {"A": "Script 1", "B": "Script 2"}[v]
    return (f"<h3>Video 1{v}: Lights On, Grace's {name} ({end - 0.4:.0f}s)</h3>"
            f"<p><a href='https://drive.google.com/file/d/{DRIVE[v]}/view'>Watch the final video</a></p>"
            f"<p><b>Full voiceover (Grace B, Grace's words as she wrote them):</b> {html.escape(full)}</p>"
            "<table border='1' cellpadding='6' style='border-collapse:collapse'><tr><th>Time</th><th>Voice</th><th>On screen</th></tr>" + "".join(rows) + "</table>"
            "<p><b>On-screen hook (pick one, add it in TikTok):</b></p><ol>" + "".join(f"<li>{html.escape(h)}</li>" for h in HOOKS[v]) + "</ol>"
            f"<p><b>Caption:</b> {html.escape(cap)}</p><hr>")


section = ("<h2>NEW: Video 1 again, in Grace's own two scripts (final, 2026-10-04)</h2>"
           "<p>Two versions of Video 1, one for each script Grace wrote. Same voice (ElevenLabs Grace B). These two show <b>Grace's face</b> for the first ~3 seconds "
           "(bad bathroom lighting), then the vanity in daylight. The room is never dark. The words are Grace's, only periods were added so it reads easily.</p><hr>"
           + part("A") + part("B"))
doc = open("out/fusou_scripts_final.html").read()
assert "Video 1A:" not in doc
doc = doc.replace("<h2>Video 1: Lights On", section + "<h2>Video 1: Lights On", 1)
open("out/fusou_scripts_final.html", "w", encoding="ascii").write(doc.encode("ascii", "xmlcharrefreplace").decode())
print(len(doc), "chars")
