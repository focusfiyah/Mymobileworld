"""Final scripts doc for Drive (Ralph 2026-10-03): per video, the exact Grace B lines on the final timeline, what is on screen for each
line, the on-screen hook options and the caption. -> out/fusou_scripts_final.html (uploaded over the Drive doc with Composio)."""
import html, json, re
import cut
DRIVE = {1: "1E-Tffp3nBT-ofMLtamdnXcm0G_zpIszA", 2: "1CDcz7iwcGer8ru5uBObmjdycZZcaroLc", 3: "1MHezZ8ea6r6NtUaQK0HymGZ2ZBvbgZCR",
         4: "1FNw1mZXHC9JpZW-0vxv8BhRCH_sDl9zh", 5: "19EtRaHqmmEKosk9TLxmCb5zZYeBtxKRC", 6: "1zuSTR7qUdmGk1Ilzz_3Yd_qOlJYh0VrV"}
TITLE = {1: "Lights On", 2: "Drawer by Drawer", 3: "Count With Me", 4: "The Mirror Is a Door", 5: "Get Ready Hands", 6: "Clear the Counter"}
md = open("scripts.md").read()


def label(shot):
    if shot[0] == "kb":
        src, o = shot[1], shot[3]
        what = {"stills/V1A_fix.png": "Whole vanity, lights on", "refs/vanity_cabinet_open.jpg": "Side cabinet open, shelves inside",
                "refs/listing_01.jpg": "Full-length mirror door", "refs/vanity_power_strip.jpg": "Side power strip and dryer holder"}[src]
        return what + (", slow pull-back" if o.get("pull") else ", slow push-in")
    f, o = shot[1], shot[3]
    if o.get("dark") and "M1a" in f: return "Dark room; fingertip taps the mirror's touch button and the LED ring lights up"
    if o.get("dark"): return "Room lights go off; the mirror and door LEDs switch cold white, warm white (dim), warm yellow"
    for k, v in {"M1a": "Fingertip taps the mirror's touch button; the LED light fades on", "V1S3": "Whole vanity, the mirror light changes colour",
                 "V1S5": "Whole vanity, wide", "M3a": "Hand lifts a lipstick out of the glass-top tray", "M6a": "All the drawers open, slow push-in",
                 "M3b": "Fingertip taps the glass top", "M4a": "Hand pulls the stool drawer open", "M2a": "Fingertip points at the USB ports and outlet",
                 "M2b": "Hand presses the plug into the outlet", "M2c": "Fingertip taps the USB ports, then points at the outlet",
                 "M5a": "Hand on the edge of the mirror door", "B1a": "Hands sweep the messy bathroom counter",
                 "B1b": "Hands gather the makeup and line up the lipsticks"}.items():
        if k in f:
            return "Hand sets a lipstick back into the tray" if (k == "M3a" and o.get("reverse")) else v


def section(n):
    sec = md.split(f"## Video {n}:")[1].split("\n## ")[0]
    hooks = re.findall(r"^\d\. (.+)$", sec.split("On-screen hook")[1].split("**Caption")[0], re.M)
    cap = re.search(r"\*\*Caption:\*\* (.+)", sec).group(1)
    edl, _, t3 = cut.EDL(n); words = cut.words(n); dur = cut.dur_of(f"out/fusou_v{n}.mp4")
    st = [s for s, _ in edl] + [dur]; rows = []
    for i, (s, shot) in enumerate(edl):
        said = " ".join(w["text"] for w in words if s - 0.05 <= w["start"] < st[i + 1] - 0.05)
        scr = label(shot) + ("; the 3-boxes photo pops in" if s <= t3 < st[i + 1] else "")
        rows.append(f"<tr><td>{s:.1f}–{st[i + 1]:.1f}s</td><td>{html.escape(said) or '<i>(no voice)</i>'}</td><td>{html.escape(scr)}</td></tr>")
    full = " ".join(L["line"] for L in json.load(open(f"vo/v{n}_lines.json")))
    return (f"<h2>Video {n}: {TITLE[n]} ({dur:.0f}s)</h2>"
            f"<p><a href='https://drive.google.com/file/d/{DRIVE[n]}/view'>Watch the final video</a></p>"
            f"<p><b>Full voiceover (Grace B):</b> {html.escape(full)}</p>"
            "<table border='1' cellpadding='6' style='border-collapse:collapse'><tr><th>Time</th><th>Voice</th><th>On screen</th></tr>"
            + "".join(rows) + "</table>"
            f"<p><b>On-screen hook (pick one, add it in TikTok):</b></p><ol>" + "".join(f"<li>{html.escape(h)}</li>" for h in hooks) + "</ol>"
            f"<p><b>Caption:</b> {html.escape(cap)}</p><hr>")


doc = ("<html><head><meta charset='utf-8'><title>FUSOU Vanity – Grace hands-only scripts (final)</title></head><body>"
       "<h1>FUSOU 2-in-1 Vanity Desk: 6 hands-only videos for Grace (final, 2026-10-03)</h1>"
       "<ul><li>Product: <a href='https://shop.tiktok.com/us/pdp/1732251413004981161'>FUSOU 2-in-1 Vanity Desk</a> · $639.99 · white</li>"
       "<li>Voiceover: ElevenLabs <b>Grace B</b> (not Grace's own voice). Hands-only, the vanity is the brand's real listing photo.</li>"
       "<li>No text burned into the videos: pick one on-screen hook per video and add it in TikTok.</li>"
       "<li>Every video ends with the usual close: <b>“It's in the orange cart.”</b> Every caption must keep <b>#ad</b>.</li>"
       "<li>Each video says one honest thing (size, build time or only 2 outlets). Keep it in.</li></ul><hr>"
       + "".join(section(n) for n in range(1, 7)) + "</body></html>")
open("out/fusou_scripts_final.html", "w", encoding="ascii").write(doc.encode("ascii", "xmlcharrefreplace").decode())   # emoji as &#x..; (Drive upload garbled raw UTF-8 emoji)
print(len(doc), "chars")
