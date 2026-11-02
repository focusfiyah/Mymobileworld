"""Free product reference sheet + one label close-up per product, from REAL photos only (no AI views).
Fronts: CeraVe's own site photos (cleanser, AM SPF 50, lip balm); the cream TUBE only from the TikTok listing
(Ralph 2026-11-02: show the tube like the listing photos; its label has navy text, unlike Ulta's red-text tube)."""
from PIL import Image, ImageDraw, ImageFont
R = "refs/"
def trim(im, pad=12):
    g = im.convert("L").point(lambda v: 255 if v < 245 else 0); b = g.getbbox()
    return im.crop((max(b[0]-pad,0), max(b[1]-pad,0), min(b[2]+pad,im.width), min(b[3]+pad,im.height)))
cl = trim(Image.open(R+"dl/cleanser_front.jpg").convert("RGB"))
am = trim(Image.open(R+"dl/am50_front.jpg").convert("RGB"))
lb = Image.open(R+"dl/lipbalm_front.jpg").convert("RGB").crop((250, 40, 440, 785))   # tube only, no smear
lst = Image.open(R+"listing/listing1.jpg").convert("RGB")                              # 945x2048
tube = lst.crop((558, 1105, 712, 1500)); tube = tube.resize((tube.width*4, tube.height*4), Image.LANCZOS)
group = lst.crop((150, 1020, 790, 1505))
for k, im in {"cleanser": cl, "am50": am, "cream_tube": tube, "lipbalm": lb}.items():
    im.save(R+f"closeup_{k}.png")
W, H = 2400, 2000
S = Image.new("RGB", (W, H), "white"); d = ImageDraw.Draw(S)
try: f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 34)
except OSError: f = ImageFont.load_default()
x = 20
for name, im in [("Hydrating Facial Cleanser (real)", cl), ("AM Lotion SPF 50 (real)", am),
                 ("Intensive Cream TUBE (listing)", tube), ("Healing Lip Balm (real)", lb)]:
    h = 1100; w = int(im.width*h/im.height)
    if w > 560: w = 560; h = int(im.height*w/im.width)
    S.paste(im.resize((w, h), Image.LANCZOS), (x + (580-w)//2, 20 + 1100-h)); d.text((x, 1135), name, fill="black", font=f); x += 595
g2 = group.resize((int(group.width*780/group.height), 780), Image.LANCZOS); S.paste(g2, (20, 1200))
d.text((g2.width+50, 1220), "TRUE RELATIVE SIZE (listing):", fill="black", font=f)
for i, t in enumerate(["cleanser tallest (8 fl oz pump bottle, green pump)",
                       "AM lotion ~85% of cleanser height (3 fl oz,",
                       "  white pump + blue collar)",
                       "cream tube ~same height as lotion, cap DOWN",
                       "  (8 fl oz, white tube, blue flip cap)",
                       "lip balm ~half the cleanser, navy tube,",
                       "  silver cap DOWN (0.35 oz)"]):
    d.text((g2.width+50, 1280+i*56), t, fill="black", font=f)
S.save(R+"product_sheet.png"); print("sheet ok", S.size)
