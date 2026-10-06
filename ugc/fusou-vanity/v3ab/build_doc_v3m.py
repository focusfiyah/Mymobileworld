"""Replaces the Video 3 section of the Drive scripts doc with the MOTION redo (Ralph approved 2026-10-05): library hooks (A H095, B H126), 3D moving shots.
Reads out/fusou_scripts_final.html (local copy of the Drive doc), swaps the 'NEW: Video 3 again' section, writes it back.  python3 v3ab/build_doc_v3m.py"""
import html, json, os, sys
sys.path.insert(0, os.getcwd()); sys.path.insert(0, "v3ab")
import cut_v3m as C
DRIVE = {"A": "1w6Tnv2pVkn1L6QAv-8_VC8AhnJUu01NO", "B": "1xrpxbBIvklLWgQu84xxSOCqK57v4_3Ag"}
HOOK = {"A": "H095 (Product Demo)", "B": "H126 (Humor)"}
SCREEN = {"A": ["Camera glides in and around the real bedroom; Grace's small hand slides in from the left edge and points at the vanity",
                "Camera pulls back to show the whole bedroom", "Low slide past the full-length mirror", "Camera circles the open drawers",
                "Slide past the open side cabinet", "Slow push on the drawers", "Camera rises from the stool to the lit makeup mirror",
                "Slide past the full-length mirror", "Hand opens the mirror door: hidden shelves", "Hand at the built-in outlets",
                "Hand at the outlets, closer", "Hand pulls the stool drawer open", "Hand lifts a lipstick from the drawer tray",
                "Camera pulls back to the whole bedroom", "Camera drops from the lit mirror to the stool", "Camera glides into the bedroom", "Slow push on the open drawers"],
          "B": ["Camera rises from the stool to the lit makeup mirror", "Camera pulls back to show the whole bedroom",
                "Low slide past the full-length mirror; Grace's small hand slides in from the right edge and points at it", "Camera circles the open drawers",
                "Slide past the open side cabinet", "Camera glides in on the lit mirror", "Slide past the full-length mirror (other way)",
                "Hand opens the mirror door: hidden shelves", "Hand at the built-in outlets", "Hand at the outlets, closer", "Hand pulls the stool drawer open",
                "Slow push on the open drawers", "Camera pushes in from the whole bedroom", "Camera circles the open drawers", "Camera drops from the lit mirror to the stool",
                "Camera pulls back to the whole bedroom"]}
CAPTION = "five things in one piece of furniture \U0001F92F #ad #vanitydesk #smallroomideas #roommakeover #tiktokshopfinds"


def part(v):
    L = json.load(open(f"v3ab/vo/v{v}h_final_lines.json")); words = json.load(open(f"v3ab/vo/v{v}h_final_words.json")) if os.path.exists(f"v3ab/vo/v{v}h_final_words.json") else None
    end = C.dur_of(f"v3ab/vo/v{v}h_final.wav") + 0.4; st = []
    for i, line in enumerate(C.EDL[v]):
        t = 0.0 if i == 0 else L[i]["start"]
        for _, d in line: st.append(t); t += d or 0
    st.append(end); assert len(st) - 1 == len(SCREEN[v]), (v, len(st) - 1)
    rows = []
    for i in range(len(st) - 1):
        said = " ".join(l["line"] for l in L if st[i] - 0.05 <= l["start"] < st[i + 1] - 0.05)
        rows.append(f"<tr><td>{st[i]:.1f}–{st[i + 1]:.1f}s</td><td>{html.escape(said) or '<i>(line continues)</i>'}</td><td>{html.escape(SCREEN[v][i])}</td></tr>")
    full = " ".join(l["line"] for l in L)
    return (f"<h3>Video 3{v}: ONE piece of furniture, version {v} ({end - 0.4:.0f}s), hook {HOOK[v]}</h3><p><a href='https://drive.google.com/file/d/{DRIVE[v]}/view'>Watch the final video</a></p>"
            f"<p><b>Full voiceover:</b> {html.escape(full)}</p>"
            "<table border='1' cellpadding='6' style='border-collapse:collapse'><tr><th>Time</th><th>Voice</th><th>On screen</th></tr>" + "".join(rows) + "</table><hr>")


section = ("<h2>NEW: Video 3 again, Grace's new script \"ONE piece of furniture\" (motion version, final 2026-10-05)</h2>"
           "<p>Redone with real camera movement in every shot (the camera glides, circles, rises and slides around the vanity in the real bedroom), no still pictures. "
           "Each version opens with a different hook from Grace's hook library, said word for word, then Grace's script as she wrote it (ElevenLabs Grace B). "
           "Grace's small hand points at the vanity from the edge of the frame. No price, no pop-up card, no text on the video.</p><hr>"
           + part("A") + part("B") + f"<p><b>Caption:</b> {html.escape(CAPTION)}</p><hr>")
doc = open("out/fusou_scripts_final.html").read(); anchor = "<h2>NEW: Video 1 again"
assert anchor in doc and "<h2>NEW: Video 3 again" in doc
i0 = doc.index("<h2>NEW: Video 3 again"); doc = doc[:i0] + doc[doc.index(anchor):]
doc = doc.replace(anchor, section + anchor, 1)
open("out/fusou_scripts_final.html", "w", encoding="ascii").write(doc.encode("ascii", "xmlcharrefreplace").decode()); print(len(doc), "chars")
