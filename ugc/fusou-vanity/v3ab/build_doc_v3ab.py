"""Adds Grace's new V3 script ("ONE piece of furniture", cuts A and B) to the Drive scripts doc (Ralph 2026-10-04). Reads out/fusou_scripts_final.html, inserts a section ABOVE the
newest one and writes it back. Run ONCE per doc state from ugc/fusou-vanity:  python3 v3ab/build_doc_v3ab.py"""
import html, json, os, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, "v3ab")
import cut_v3 as C
DRIVE = {"A": "1w6Tnv2pVkn1L6QAv-8_VC8AhnJUu01NO", "B": "1xrpxbBIvklLWgQu84xxSOCqK57v4_3Ag"}
SCREEN = {"A": ["Wide shot of the real bedroom (doors, bed, rug): Grace's small hand comes in from the left edge and points at the lit mirror",
                "Whole bedroom wide, slow push-in", "Open side cabinet with bags, slow push-in", "Close on the lit makeup mirror, slow push-in",
                "Wide: Grace's small hand comes in from the right edge and points at the full-length mirror", "Hand opens the mirror door: bags on the shelves inside",
                "Hand at the built-in outlet next to the hair dryer", "Hand pulls the stool drawer open", "Open cabinet with bags, slow push-in",
                "Pull back to the whole bedroom", "Right side of the bedroom: full-length mirror, window and bed edge, slow push-in", "Whole bedroom wide, slow push-in"],
          "B": ["Close on the lit makeup mirror, slow push-in", "Wide shot of the real bedroom: Grace's small hand comes in from the left edge and points at the lit mirror",
                "Open side cabinet, slow push-in", "Pull back from the lit mirror to the whole bedroom", "Full-length mirror, slow push-in",
                "Hidden storage: bags on the shelves, slow push-in", "Built-in outlets for hair tools, slow push-in", "Hand pulls the stool drawer open",
                "Drawers open, hand lifts a lipstick from the tray", "Left side of the bedroom: door, drawers and rug, slow push-in", "Whole bedroom wide, slow push-in"]}
HOOKS = ["one piece of furniture", "how many things is this?", "my teenage self would be SCREAMING"]
CAPTION = "five things in one piece of furniture \U0001F92F #ad #vanitydesk #smallroomideas #roommakeover #tiktokshopfinds"
words = json.load(open("v3ab/vo/vA_final_words.json")); full = " ".join(x["line"] for x in json.load(open("v3ab/vo/vA_final_lines.json")))
end = C.dur_of(C.VO) + 0.4


def part(v):
    shots = C.edl(v); st = [s for s, _ in shots] + [end]; assert len(shots) == len(SCREEN[v]), (v, len(shots))
    rows = []
    for i in range(len(shots)):
        said = " ".join(w["text"] for w in words if st[i] - 0.05 <= w["start"] < st[i + 1] - 0.05)
        rows.append(f"<tr><td>{st[i]:.1f}–{st[i + 1]:.1f}s</td><td>{html.escape(said) or '<i>(no voice)</i>'}</td><td>{html.escape(SCREEN[v][i])}</td></tr>")
    return (f"<h3>Video 3{v}: ONE piece of furniture, version {v} ({end - 0.4:.0f}s)</h3><p><a href='https://drive.google.com/file/d/{DRIVE[v]}/view'>Watch the final video</a></p>"
            "<table border='1' cellpadding='6' style='border-collapse:collapse'><tr><th>Time</th><th>Voice</th><th>On screen</th></tr>" + "".join(rows) + "</table><hr>")


section = ("<h2>NEW: Video 3 again, Grace's new script \"ONE piece of furniture\" (final, 2026-10-04)</h2>"
           "<p>Two cuts on the <b>same voiceover</b> (ElevenLabs Grace B, Grace's words as she wrote them, only punctuation changed for the voice). Grace's small hand points at the vanity "
           "from the edge of the frame, in the real bedroom from Video 2 (doors, bed, rug), with a slow camera push-in. The room is never dark and there is no price and no pop-up card.</p>"
           f"<p><b>Full voiceover:</b> {html.escape(full)}</p><p>Version A opens on the wide bedroom with the pointing hand. Version B opens on the lit mirror and shows the pointing hand on the first line after the hook.</p><hr>"
           + part("A") + part("B")
           + "<p><b>On-screen hook (pick one, add it in TikTok):</b></p><ol>" + "".join(f"<li>{html.escape(h)}</li>" for h in HOOKS) + "</ol>"
           f"<p><b>Caption:</b> {html.escape(CAPTION)}</p><hr>")
doc = open("out/fusou_scripts_final.html").read(); anchor = "<h2>NEW: Video 1 again"
assert anchor in doc
if "<h2>NEW: Video 3 again" in doc:   # rebuild: drop the old V3 section first
    i0 = doc.index("<h2>NEW: Video 3 again"); doc = doc[:i0] + doc[doc.index(anchor):]
doc = doc.replace(anchor, section + anchor, 1)
open("out/fusou_scripts_final.html", "w", encoding="ascii").write(doc.encode("ascii", "xmlcharrefreplace").decode()); print(len(doc), "chars")
