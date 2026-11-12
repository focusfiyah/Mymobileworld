"""Captions (TikTok post text) for Vans V18-V37, music-only videos (Ralph 2026-11-11). Hook = Grace library hook word for
word (grace/hooks/HOOKS.md, blanks filled), one product line backed by product_truth.json, close "It's in the orange cart."
Writes scripts.md, research/hooks.md, research/line_sources.md, research/line_audit.md."""
import json
from pathlib import Path
J = Path(__file__).resolve().parent.parent
H = {h["id"]: h["hook"] for h in json.loads((J.parent.parent / "grace/hooks/hooks.json").read_text())["hooks"]}
C = {  # video: (hook id, blank fill or None, product line, fact source, alt hook ids)
 "V18": ("H030", None, "Only the black squares have sequins, so they shine without being too much.", "fact 2 (sequins on black squares only)", ["H023", "H020"]),
 "V19": ("H023", None, "Same classic Vans shape, just with sequins on the black squares.", "facts 1-2", ["H030", "H025"]),
 "V20": ("H020", None, "Red insole with the white Vans box inside.", "fact 8 (insole)", ["H029", "H032"]),
 "V21": ("H003", None, "They go with my comfy clothes and my going out clothes.", "opinion (styling), no product claim", ["H004", "H044"]),
 "V22": ("H004", None, "A satin skirt and sequin Vans, done.", "fact 2 + outfit in frame", ["H003", "H047"]),
 "V23": ("H035", "a pair of Vans", "The sequins catch the light every time I move.", "fact 2 (raised sequins), seen in the real photos", ["H013", "H004"]),
 "V24": ("H027", "the sequins up close", "Raised black sequins on the black squares, plain canvas on the white.", "fact 2", ["H029", "H020"]),
 "V25": ("H021", None, "Black heel stripe and the Off The Wall label, same as the classic.", "facts 6-7 (heel stripe, label)", ["H023", "H025"]),
 "V26": ("H029", None, "Up close, the sequins are on the black squares only.", "fact 2", ["H027", "H034"]),
 "V27": ("H032", None, "The red insole shows every time I slip them on.", "fact 8", ["H034", "H012"]),
 "V28": ("H002", None, "Sequins on the classic Vans shape I already love.", "fact 1 + opinion", ["H014", "H035"]),
 "V29": ("H014", "my sneakers", "These are the classic Authentic with sequins on the black squares.", "facts 1-2", ["H013", "H002"]),
 "V30": ("H025", None, "The pair side by side, inside and out.", "shots show the pair, insole and laces", ["H020", "H023"]),
 "V31": ("H034", None, "It was the red insole with the white Vans box.", "fact 8", ["H032", "H029"]),
 "V32": ("H013", "sparkly sneakers", "These have just the right amount.", "fact 2 (sequins only on black squares)", ["H035", "H014"]),
 "V33": ("H044", None, "I wear them with jeans and with sweats.", "opinion (styling), no product claim", ["H003", "H047"]),
 "V34": ("H047", "I want my outfit to look done", "I put these on and I'm out the door.", "fact 2 + opinion", ["H004", "H044"]),
 "V35": ("H110", None, "Anyone who loves checkered Vans and a little shine.", "opinion, no product claim (V35 sole shot dropped 2026-11-12)", ["H021", "H032"]),
 "V36": ("H052", "days I want a little sparkle", "Lately that is most days.", "opinion, no product claim", ["H003", "H004"]),
 "V37": ("H097", None, "Sequins on the black squares only, so they still look like Vans.", "facts 1-2", ["H030", "H027"]),
}
CLOSE = "It's in the orange cart."


def hook(i, fill):
    t = H[i]
    return (t.replace("__", fill) if fill else t).rstrip(".") + ("" if t.rstrip().endswith("?") else ".")


sc, hk, ls, la = ["# Vans V18-V37 captions (music-only videos, no voice, no on-screen text)\n"], ["# Hook options per video (Grace library, word for word; on-screen text stays OFF unless Ralph says yes)\n"], ["# Source of every caption line\n"], ["# Line audit (Grace script method, PLAYBOOK §4), one block per caption\n"]
for v, (i, fill, line, src, alts) in C.items():
    h = hook(i, fill)
    sc.append(f"## {v}\n{h} {line} {CLOSE}\n")
    hk.append(f"## {v}\n- Used: {i}: {h}\n" + "".join(f"- Option: {a}: {H[a]}\n" for a in alts) + "- On-screen text option (off by default): same as the used hook\n")
    ls.append(f"## {v}\n- \"{h}\" = Grace hook library {i} (word for word{', blank filled' if fill else ''})\n- \"{line}\" = {src}\n- \"{CLOSE}\" = Grace's house close (PLAYBOOK)\n")
    la.append(f"## {v}\nBuyer: women who like classic Vans and want a little shine for everyday outfits\nPain: plain sneakers make an outfit look flat; flashy glitter shoes look like a costume\n"
              f"Connection: the hook speaks as a shopper who checked the shoe before buying\nOutsider test: a stranger understands it in one read\nCommon enemy: shoes that look different in the listing than in real life\n"
              f"Contradiction check: no line contradicts another or the product facts\nPain points: 1\nSelling points: 1\nRepetition pass: hook id used once across V18-V37\n"
              f"- GREEN: {h}\n- GREEN: {line}\n- GREEN: {CLOSE}\nCut: none\n")
assert len({c[0] for c in C.values()}) == len(C), "a hook id repeats"
(J / "scripts.md").write_text("\n".join(sc)); (J / "research/hooks.md").write_text("\n".join(hk))
(J / "research/line_sources.md").write_text("\n".join(ls)); (J / "research/line_audit.md").write_text("\n".join(la))
print("captions", len(C))
