"""Rumah Márton residence PDFs — editable source.

Edit the CONTENT section (wording, areas, page order) and run:  python3 build.py
Output: out/Rumah-Marton-Garden-Residence.pdf, out/Rumah-Marton-Penthouse-Residence.pdf,
        out/plans/*.pdf (standalone floor plans) and out/plans/*.png (for the website).
Needs: Python 3, playwright (chromium), pymupdf, pillow, qrcode; the brochure PDF and fonts below.
"""
import base64, io, json, pathlib, re
import fitz
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
BRO = "/home/claude/work/bro/src.pdf"   # the original October brochure (page numbers below refer to it)
IMG = "/home/claude/rm/src/assets/images/"
FONTS = "/home/claude/fonts/"
OUT = HERE / "out"; (OUT / "plans").mkdir(parents=True, exist_ok=True)
SITE = "https://rumahmarton.com/"   # the live website address — must match the domain you buy
NUDGE = {}   # (brochure page, room number): (x, y) shift as a share of the drawing
NORTH = 30   # degrees clockwise from "up" on the plans and site diagram (same orientation)
LANG = "en"; SUF = ""   # set by build_lang.py: "hu"/"zh" and "-hu"/"-zh"
T = {}                   # translated interface strings (empty = English)
def t(k, en): return T.get(k, en)
EYE = "Rumah Márton<br>Mártonhegy, Budapest"

# ============================== CONTENT ==============================
GARDEN = dict(
    key="garden", name="Garden Residence", file="Rumah-Marton-Garden-Residence.pdf",
    vr="https://vr.justeasy.cn/view/1778l51xq23bg9e2-1778512683.html",
    lede="A two-bedroom home with a study that opens directly onto its own private garden, with generous terraces and provision for a dedicated outdoor kitchen beyond expansive pocket sliding doors.",
    facts=[("Floor", "Ground floor"), ("Bedrooms", "2 bedrooms and a study, which may be used as a third bedroom"),
           ("Interior", "86 m²"), ("Terraces", "61 m²"), ("Private garden", "232 m²")],
    cover=IMG + "garden-residence.jpg",
    plans=[dict(page=11, slug="garden-residence-plan", title="Ground floor plan",
                rooms=[("01", "Private lobby", "3.45"), ("02", "Entrance hall", "4.49"), ("03", "Study", "3.24"), ("04", "Foyer", "2.13"),
                       ("05", "Powder room", "1.30"), ("06", "Kitchen and dining", "15.13"), ("07", "Living", "24.28"), ("08", "Corridor", "2.27"),
                       ("09", "Bedroom 01", "13.23"), ("10", "Bedroom 02", "11.40"), ("11", "Bathroom", "5.05")],
                totals=[("Interior", "85.97", "strong"),
                        ("T1  Terrace", "40.54", ""), ("T2  Terrace", "20.71", ""), ("Terraces", "61.25", "sub"),
                        ("Weighted area", "116.60", "strong", "terraces at 50%"),
                        ("Private garden", "232.17", "garden")],
                site=True)],
    visuals=[(12, ""), (13, "Master suite"), (14, "Second bedroom")],
)
PENTHOUSE = dict(
    key="penthouse", name="Penthouse Residence", file="Rumah-Marton-Penthouse-Residence.pdf",
    vr="https://vr.justeasy.cn/view/177c88pt51c31950-1778513346.html",
    lede="A private top-floor residence overlooking Budapest, with two balconies and an exclusive rooftop terrace designed for outdoor living and entertaining, with provision for a dedicated kitchen.",
    facts=[("Floor", "Top floor, with rooftop terrace"), ("Bedrooms", "3 bedrooms, or 2 with a grander master suite"),
           ("Interior", "100 m²"), ("Balconies", "21 m²"), ("Rooftop terrace", "39 m²")],
    cover=IMG + "penthouse-view.png",
    plans=[dict(page=20, slug="penthouse-plan-3-bedrooms", title="Floor plan · 3 bedrooms",
                rooms=[("01", "Entrance foyer", "4.30"), ("02", "Kitchen and dining", "18.90"), ("03", "Living", "22.27"), ("04", "Corridor", "3.50"),
                       ("05", "Master suite", "11.20"), ("06", "Master closet", "4.32"), ("07", "Master bath", "4.68"), ("08", "Bedroom 02", "13.44"),
                       ("09", "Bathroom", "4.59"), ("10", "Bedroom 03 / study", "10.23"), ("11", "Private lobby", "2.20")],
                totals=[("Interior", "99.63", "strong"),
                        ("B1  Balcony", "13.88", ""), ("B2  Balcony", "6.78", ""), ("Balconies", "20.66", "sub"),
                        ("T1  Rooftop terrace", "38.53", "", "with kitchen provision · see roof plan"),
                        ("Weighted area", "129.23", "strong", "outdoor areas at 50%")]),
           dict(page=19, slug="penthouse-plan-2-bedrooms", title="Floor plan · 2 bedrooms, grand master suite",
                rooms=[("01", "Entrance foyer", "4.30"), ("02", "Kitchen and dining", "18.90"), ("03", "Living", "22.27"), ("04", "Corridor", "3.50"),
                       ("05", "Master suite", "14.00"), ("06", "Master closet", "10.80"), ("07", "Master bath", "6.30"), ("08", "Bedroom 02", "13.44"),
                       ("09", "Bathroom", "4.59"), ("10", "Private lobby", "2.20")],
                totals=[("Interior", "100.30", "strong"),
                        ("B1  Balcony", "13.88", ""), ("B2  Balcony", "6.78", ""), ("Balconies", "20.66", "sub"),
                        ("T1  Rooftop terrace", "38.53", "", "with kitchen provision · see roof plan"),
                        ("Weighted area", "129.90", "strong", "outdoor areas at 50%")]),
           dict(page=21, slug="penthouse-roof-terrace-plan", title="Rooftop terrace plan",
                rooms=[], totals=[("T1  Rooftop terrace", "38.53", "strong", "private to the Penthouse, with provision for an outdoor kitchen")],
                note="The balconies B1 and B2 are on the residence floor below.")],
    visuals=[(26, ""), (27, ""), (23, "Master suite"), (24, "Second bedroom"), (25, "Study"), (28, "Rooftop terrace")],
)
CLOSING_LEFT = [
    "We would love to show you the site and talk you through the plans for the {name}.",
    "If you wish, we can also explore how the finishes, specifications and spaces might be tailored to your needs, guided by our award-winning architectural team and subject to design and construction feasibility.",
    "Detailed specifications, pricing, payment stages and terms, and the planned construction programme are available on request.",
]
INCLUDED = [("Privacy & access", ["One residence per floor, with direct lift access to a private lobby",
                                  "Keyless entry, secure basement storage and EV-ready parking connection"]),
            ("Comfort & technology", ["Geothermal or air-source heat-pump heating and cooling, with filtered fresh-air ventilation",
                                      "Smart-home-ready infrastructure for future integration"]),
            ("Materials & finishes", ["Triple-glazed windows with naturally finished oak frames to the interior",
                                      "Oak and limestone flooring, with refined mineral plaster walls",
                                      "Considered detailing and finishes to lobbies and bathrooms"]),
            ("Outdoor living", ["Private outdoor living spaces", "Provision for a dedicated outdoor kitchen"])]
BESPOKE = ("Bespoke interiors", "We would be delighted to work with you to create a fully fitted and furnished interior. Speak with us to explore the possibilities.")
SMALL_PRINT = "Illustrations are architectural visualisations. Areas, specifications, layout options and completion dates are subject to final confirmation in the sale and purchase documentation."
# =====================================================================

def font_css():
    out = []
    for fam, pkg, files in (("Newsreader", "fontsource-newsreader-5.3.0", ["300-normal", "300-italic", "400-normal"]),
                            ("Albert Sans", "fontsource-albert-sans-5.3.0", ["300-normal", "400-normal"])):
        base = pkg.split("-", 1)[1].rsplit("-", 1)[0]
        for f in files:
            w, st = f.split("-")
            for sub, rng in (("latin", "U+0000-00FF,U+2000-206F,U+2190-21FF,U+00B2"), ("latin-ext", "U+0100-024F")):
                d = base64.b64encode(open(f"{FONTS}{pkg}/files/{base}-{sub}-{f}.woff2", "rb").read()).decode()
                out.append(f"@font-face{{font-family:'{fam}';font-weight:{w};font-style:{st};unicode-range:{rng};src:url(data:font/woff2;base64,{d}) format('woff2')}}")
    return "".join(out)

CSS = font_css() + """
@page{size:297mm 210mm;margin:0}
*{box-sizing:border-box}
html,body{margin:0;background:#FAFAF8;color:#1D1C1A;font-family:'Albert Sans',sans-serif;font-weight:300;-webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:297mm;height:210mm;overflow:hidden;position:relative;page-break-after:always}
.eyebrow{font-size:7.2pt;letter-spacing:.22em;text-transform:uppercase;color:#77736D;margin:0}
h1{font-family:'Newsreader',serif;font-weight:300;font-size:36pt;line-height:1;margin:8mm 0 6mm;letter-spacing:-.01em}
h2{font-family:'Newsreader',serif;font-weight:300;font-size:22pt;line-height:1.05;margin:5mm 0 2mm}
.lede{font-family:'Newsreader',serif;font-weight:300;font-size:13pt;line-height:1.45;margin:0 0 9mm}
.facts{margin:0;padding:0;display:grid;grid-template-columns:32mm 1fr;border-top:.25mm solid #DCD8D1}
.facts dt,.facts dd{margin:0;padding:2.6mm 0;border-bottom:.25mm solid #E6E3DD;font-size:9pt;line-height:1.35}
.facts dt{color:#77736D;font-size:7.2pt;letter-spacing:.16em;text-transform:uppercase;padding-top:3mm}
/* cover */
.cover{display:grid;grid-template-columns:96mm 1fr}
.cover .l{padding:17mm 9mm 14mm 15mm;display:flex;flex-direction:column}
.cover .r{display:flex;align-items:center;justify-content:center;padding:15mm 15mm 15mm 6mm}
.cover .r img{max-width:100%;max-height:180mm;width:auto;height:auto;display:block}
/* plan */
.plan{display:grid;grid-template-columns:64mm 1fr}
.plan .l{padding:14mm 4mm 11mm 12mm;display:flex;flex-direction:column}
.plan h2{font-size:17pt;margin:3mm 0 1mm}
.plan .r{position:relative;padding:10mm 10mm 8mm 4mm;display:flex;flex-direction:column}
.sched{width:100%;border-collapse:collapse;margin-top:4mm;font-size:7.6pt}
.sched td{padding:1.15mm 0;border-bottom:.2mm solid #ECE9E3;vertical-align:baseline}
.sched td.n{width:7mm;color:#8C877F;font-family:'Newsreader',serif;font-size:8.5pt}
.sched td.a{text-align:right;font-family:'Newsreader',serif;font-size:8.8pt;font-variant-numeric:tabular-nums lining-nums;white-space:nowrap}
.sched tr.gap td{border:0;padding:1.6mm 0}
.sched tr.strong td{border-top:.3mm solid #1D1C1A;border-bottom:0;padding-top:1.8mm;font-weight:400}
.sched tr.strong td.a{font-size:10pt;font-weight:400}
.sched tr.sub td{color:#4A4743;border-bottom:.2mm solid #D5D1CA}
.sched tr.garden td{border-top:.3mm solid #5E7154;color:#3E4E36;padding-top:1.8mm}
.sched tr.garden td.a{font-size:10pt}
.sched .note{display:block;font-size:6.6pt;color:#8C877F;letter-spacing:.02em;margin-top:.6mm}
.unit{font-size:6.6pt;color:#8C877F;margin-left:1mm}
.plan .head{display:flex;justify-content:flex-end;align-items:center;gap:4mm;height:14mm}
.plan .draw{flex:1;position:relative;display:flex;align-items:center;justify-content:center;min-height:0}
.plan .draw .box{position:relative}
.plan .draw img{display:block;width:100%;height:auto;mix-blend-mode:multiply}
.lbl{position:absolute;transform:translate(-50%,-50%);font-family:'Albert Sans',sans-serif;font-size:5.5pt;letter-spacing:.03em;color:#4A4743}
.cap{font-size:7.2pt;letter-spacing:.22em;text-transform:uppercase;color:#77736D;text-align:center;margin:4mm 0 0}
.foot{margin-top:auto;font-size:7pt;color:#8C877F;line-height:1.5}
.vis{display:flex;align-items:center;justify-content:center;padding:14mm 18mm 12mm}
.vis .frame{display:flex;flex-direction:column;align-items:center;max-width:100%}
.vis img{display:block;max-width:261mm;max-height:166mm;width:auto;height:auto}
.vis .cap{margin:5mm 0 0}
.tag{position:absolute;transform:translate(-50%,-50%);background:rgba(241,227,218,.94);padding:.8mm 1.6mm;text-align:center;white-space:nowrap;font-size:5.6pt;line-height:1.3;letter-spacing:.06em;color:#1D1C1A}
.tag b{display:block;font-weight:400;text-transform:uppercase;letter-spacing:.14em;font-size:5pt}
.tag.home{background:#1D1C1A;color:#FAFAF8}
.loc{display:grid;grid-template-columns:82mm 1fr}
.loc .l{padding:17mm 8mm 14mm 15mm;display:flex;flex-direction:column}
.loc .l p{font-size:9.4pt;line-height:1.65;margin:0 0 3.6mm}
.loc .l h2{margin:8mm 0 6mm}
.loc .r{display:flex;flex-direction:column;align-items:center;justify-content:center;padding:12mm 12mm 12mm 4mm}
/* closing */
.closing .bespoke{font-family:'Newsreader',serif;font-size:9.2pt;line-height:1.45;margin:0;max-width:100mm;color:#6E6A64}
.closing{display:grid;grid-template-columns:1fr 1fr}
.closing .c{padding:17mm 14mm 13mm 15mm;display:flex;flex-direction:column}
.closing .c + .c{background:#F2EEE7}
.closing p{font-size:9.4pt;line-height:1.6;margin:0 0 3.2mm;max-width:112mm}
.closing .links{list-style:none;margin:6mm 0 0;padding:0;display:grid;gap:3.4mm}
.closing .links a{font-size:7.6pt;letter-spacing:.2em;text-transform:uppercase;color:#1D1C1A;text-decoration:none;border-bottom:.25mm solid #1D1C1A;padding-bottom:.8mm}
.closing .links a span{letter-spacing:0}
.closing .addr{font-family:'Newsreader',serif;font-size:12pt;line-height:1.5;margin-top:auto}
.closing .addr a{color:inherit;text-decoration:none}
.closing .done{font-size:7.2pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;margin-top:4mm}
.inc h3{font-size:6.4pt;letter-spacing:.2em;text-transform:uppercase;color:#9A958D;font-weight:400;margin:5mm 0 1.4mm}
.inc ul{list-style:none;margin:0;padding:0}
.inc li{font-family:'Newsreader',serif;font-size:9.2pt;line-height:1.4;padding:.7mm 0;color:#6E6A64}
.closing .small{margin:auto 0 0;font-size:6.8pt;line-height:1.5;color:#8C877F;max-width:118mm}
"""

def data_uri(path_or_bytes, mime):
    b = path_or_bytes if isinstance(path_or_bytes, bytes) else open(path_or_bytes, "rb").read()
    return f"data:{mime};base64,{base64.b64encode(b).decode()}"

def jpeg(path, max_w=2600):
    im = Image.open(path).convert("RGB")
    if im.width > max_w: im = im.resize((max_w, round(im.height * max_w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "JPEG", quality=90, optimize=True); return buf.getvalue()

NORTH_SVG = f'''<svg viewBox="-24 -32 48 56" width="9mm" height="10.5mm"><circle r="17" fill="none" stroke="#1D1C1A" stroke-width=".8"/>
<g transform="rotate({NORTH})"><path d="M0 -13 L4.2 6 L0 3 L-4.2 6 Z" fill="#1D1C1A"/><path d="M0 3 L4.2 6 L0 13 L-4.2 6 Z" fill="none" stroke="#1D1C1A" stroke-width=".6"/>
<text x="0" y="-19.5" text-anchor="middle" transform="rotate({-NORTH} 0 -23.5)" font-family="Newsreader" font-size="11" fill="#1D1C1A">N</text></g></svg>'''

def site_svg():
    OX, OY = 161.4, 275.7
    P = lambda pts: " ".join(f"{x-OX:.1f},{y-OY:.1f}" for x, y in pts)
    plot = [(969.6, 561.4), (969.1, 275.7), (262.4, 275.7), (161.4, 561.4)]
    house = [(478.9, 351.7), (660.3, 351.7), (660.3, 500.3), (478.9, 500.3)]
    terr = [(478.9, 320.0), (712, 320.0), (712, 532), (478.9, 532)]
    gard = [(478.9, 561.4), (821.9, 561.4), (821.9, 320.0), (712, 320.0), (712, 532), (478.9, 532)]
    strip = [(478.9, 275.7), (821.9, 275.7), (821.9, 320.0), (478.9, 320.0)]
    return f'''<svg viewBox="-4 -4 816 294" width="40mm" height="14.4mm"><polygon points="{P(plot)}" fill="#F3F1EC" stroke="#1D1C1A" stroke-width="1.6" stroke-dasharray="10 4 2 4"/>
<polygon points="{P(strip)}" fill="#DFE6D5" stroke="#8C9C80" stroke-width="1.2" stroke-dasharray="5 4"/><polygon points="{P(gard)}" fill="#D3DCC7" stroke="#5E7154" stroke-width="1.4"/>
<polygon points="{P(terr)}" fill="#EFEAE0" stroke="#1D1C1A" stroke-width="1.4" stroke-dasharray="6 4"/><polygon points="{P(house)}" fill="#FFFFFF" stroke="#1D1C1A" stroke-width="2.6"/></svg>'''

def plan_image(pno):
    """Crop the drawing from the brochure page, enlarge it cleanly, return (png bytes, crop rect in pt, labels)."""
    d = fitz.open(BRO); pg = d[pno - 1]
    info = pg.get_image_info(xrefs=True)[0]
    pix = fitz.Pixmap(d, info["xref"]); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB")
    t = info["transform"]; k = im.width / t[0]; ox, oy = t[4], t[5]
    import numpy as np
    ink = np.asarray(im).astype(int).sum(axis=2) < 735
    cols = np.where(ink.sum(axis=0) >= 6)[0]; rows = np.where(ink.sum(axis=1) >= 6)[0]   # ignore stray specks
    def main_run(idx, gap=40):   # the largest continuous stretch of drawing, ignoring stray lines far away
        runs, cur = [], [idx[0], idx[0]]
        for v in idx[1:]:
            if v - cur[1] <= gap: cur[1] = v
            else: runs.append(cur); cur = [v, v]
        runs.append(cur); r = max(runs, key=lambda r: r[1] - r[0]); return np.array(r)
    xs, ys = main_run(cols), main_run(rows)
    m = 10
    x0, y0, x1, y1 = xs.min() - m, ys.min() - m, xs.max() + m, ys.max() + m
    crop = im.crop((x0, y0, x1, y1))
    crop = crop.resize((crop.width * 2, crop.height * 2), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=1.2, percent=60, threshold=2))
    buf = io.BytesIO(); crop.save(buf, "PNG", optimize=True)
    rect = (x0 / k + ox, y0 / k + oy, x1 / k + ox, y1 / k + oy)
    labels = []
    for b in pg.get_text("dict")["blocks"]:
        for l in b.get("lines", []):
            for s in l["spans"]:
                tx = s["text"].strip()
                if re.fullmatch(r"\d{2}|[TB]\d", tx) and s["bbox"][0] > rect[0] and s["bbox"][2] < rect[2] and s["bbox"][1] > rect[1] and s["bbox"][3] < rect[3]:
                    cx, cy = (s["bbox"][0] + s["bbox"][2]) / 2, (s["bbox"][1] + s["bbox"][3]) / 2
                    dx, dy = NUDGE.get((pno, tx), (0, 0))   # small hand adjustments so a number clears the drawing
                    labels.append((tx, (cx - rect[0]) / (rect[2] - rect[0]) + dx, (cy - rect[1]) / (rect[3] - rect[1]) + dy))
    return buf.getvalue(), rect, labels

def sched_html(p):
    rows = "".join(f'<tr><td class="n">{n}</td><td>{r}</td><td class="a">{a}</td></tr>' for n, r, a in p["rooms"])
    tot = ""
    for i, t in enumerate(p["totals"]):
        label, val, cls = t[0], t[1], t[2]; note = t[3] if len(t) > 3 else ""
        n, lab = (label.split("  ") + [""])[:2] if "  " in label else ("", label)
        if not lab: lab, n = n, ""
        if cls in ("strong", "garden") and (i or p["rooms"]): tot += '<tr class="gap"><td colspan="3"></td></tr>'
        tot += f'<tr class="{cls}"><td class="n">{n}</td><td>{lab}{f"<span class=note>{note}</span>" if note else ""}</td><td class="a">{val}<span class="unit">m²</span></td></tr>'
    return f'<table class="sched">{rows}{tot}</table>'

def plan_page(u, p, standalone=False):
    png, rect, labels = plan_image(p["page"])
    w_pt, h_pt = rect[2] - rect[0], rect[3] - rect[1]
    # fit drawing in the right-hand area (mm): 297-70-16 wide, 210-12-10-24-10 high
    aw, ah = 297 - 64 - 14, 210 - 10 - 8 - 14 - 6
    s = min(aw / (w_pt * 25.4 / 72), ah / (h_pt * 25.4 / 72))
    wmm = w_pt * 25.4 / 72 * s
    lbl = "".join(f'<span class="lbl" style="left:{x*100:.2f}%;top:{y*100:.2f}%">{t}</span>' for t, x, y in labels)
    head = (site_svg() if p.get("site") else "") + NORTH_SVG
    note = f'<p class="foot" style="margin-top:5mm">{p["note"]}</p>' if p.get("note") else ""
    return f'''<div class="page plan"><div class="l">
  <p class="eyebrow">{t("eyebrow", EYE)}</p><h2>{u["name"]}</h2><p class="eyebrow" style="margin-top:2mm">{p["title"]}</p>
  {sched_html(p)}{note}
  <p class="foot">{t("areas_note", "Areas in m², based on the permitted plans.")}</p>
</div><div class="r"><div class="head">{head}</div>
  <div class="draw"><div class="box" style="width:{wmm:.1f}mm"><img src="{data_uri(png,'image/png')}">{lbl}</div></div>
</div></div>''', png

def cover_page(u):
    facts = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in u["facts"])
    return f'''<div class="page cover"><div class="l">
  <p class="eyebrow">{t("eyebrow", EYE)}</p><h1>{u["name"]}</h1><p class="lede">{u["lede"]}</p>
  <dl class="facts">{facts}</dl></div>
<div class="r"><img src="{data_uri(jpeg(u["cover"]),'image/jpeg')}"></div></div>'''

def closing_page(u):
    left = "".join(f"<p>{t.format(name=u['name'])}</p>" for t in CLOSING_LEFT)
    inc = "".join(f"<h3>{h}</h3><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>" for h, items in INCLUDED)
    return f'''<div class="page closing"><div class="c">
  <p class="eyebrow">{t("eyebrow", EYE)}</p><h2 style="font-size:28pt;margin:6mm 0 6mm">{t("be_in_touch", "Be in touch")}</h2>{left}
  <ul class="links">
    {f'<li><a href="{u["vr"]}">{t("l_vr", "Explore the Residence in 360°")} <span>↗</span></a></li>' if u.get("vr") else ""}
    <li><a href="{SITE}{'' if LANG == 'en' else LANG + '/'}">{t("l_site", "Visit the Rumah Márton website")} <span>↗</span></a></li>
    <li><a href="https://www.wy-design.com/">{t("l_wy", "Explore WY Design")} <span>↗</span></a></li>
    <li><a href="https://roadster.hu/peiyee-yong-interju">{t("l_pei", "Meet Pei Yong — Read the Interview")} <span>↗</span></a></li>
  </ul>
  <p class="addr">{t("addr", "Rumah Márton<br>Mártonvölgyi út, District XII, Budapest")}<br><a href="mailto:pei@wy-design.com">pei@wy-design.com</a></p>
  <p class="done">{t("done", "Planned completion — Q3 2028")}</p>
</div><div class="c inc"><p class="eyebrow">{t("included", "Included in every home")}</p>{inc}<h3>{BESPOKE[0]}</h3><p class="bespoke">{BESPOKE[1]}</p><p class="small">{SMALL_PRINT}</p></div></div>'''

def visual_page(u, pno, sub):
    d = fitz.open(BRO); info = d[pno - 1].get_image_info(xrefs=True)[0]
    pix = fitz.Pixmap(d, info["xref"]); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
    cap = u["name"] + (f" · {sub}" if sub else "")
    return f'''<div class="page vis"><div class="frame"><img src="{data_uri(buf.getvalue(),'image/jpeg')}"><p class="cap">{cap}</p></div></div>'''

MAP_PAGE = 6   # brochure page with the neighbourhood map
MAP_NAMES = {"Te British International School (BISB)": "The British International School (BISB)", "Hegyvidek Shopping Centre": "Hegyvidék Shopping Centre",
             "Mom Park": "MOM Park", "Margit Sziget": "Margaret Island", "Andrassy Ut": "Andrássy út", "Martonhegy": "Rumah Márton"}
LOCATION_SHORT = dict(title="Mártonhegy, Budapest XII", body=[
    "Rumah Márton lies in Hegyvidék, District XII — one of Budapest’s oldest and most prestigious neighbourhoods, known for its villas, forested hills and timeless elegance.",
    "Set on a quiet one-way street on the slopes of Mártonhegy, the house looks out towards Castle Hill and the Citadella. Normafa and the Buda Hills are moments away, with international schools, Villa Bagatelle, MOM Park and the city centre all within easy reach."])

def map_block(width_mm):
    d = fitz.open(BRO); p = d[MAP_PAGE - 1]; info = p.get_image_info(xrefs=True)[0]; x0, y0, x1, y1 = info["bbox"]
    pix = fitz.Pixmap(d, info["xref"]); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=90)
    lines = [(l["bbox"], "".join(s["text"] for s in l["spans"]).strip()) for b in p.get_text("dict")["blocks"] for l in b.get("lines", [])]
    lines = [x for x in lines if x[1]]; used, tags = set(), []
    for bb, tx in lines:
        if tx.startswith("("): continue
        tm = next(((j, tt) for j, (b2, tt) in enumerate(lines) if tt.startswith("(") and j not in used and abs(b2[1] - bb[3]) < 4 and abs((b2[0] + b2[2]) / 2 - (bb[0] + bb[2]) / 2) < 30), None)
        if tm: used.add(tm[0])
        name_en = MAP_NAMES.get(tx, tx); name = T.get("map", {}).get(name_en, name_en); cx = ((bb[0] + bb[2]) / 2 - x0) / (x1 - x0) * 100; cy = (bb[1] - y0) / (y1 - y0) * 100 + 2
        tags.append(f'<span class="{"tag home" if name_en == "Rumah Márton" else "tag"}" style="left:{cx:.1f}%;top:{cy:.1f}%"><b>{name}</b>{tm[1].strip("()").replace("mins", T.get("mins", "mins")) if tm else ""}</span>')
    return f'<div class="mb" style="width:{width_mm}mm;position:relative"><img src="{data_uri(buf.getvalue(),"image/jpeg")}" style="width:100%;display:block">{"".join(tags)}</div>'

def location_page():
    body = "".join(f"<p>{x}</p>" for x in LOCATION_SHORT["body"])
    return f'''<div class="page loc"><div class="l"><p class="eyebrow">{t("eyebrow", EYE)}</p><h2>{LOCATION_SHORT["title"]}</h2>{body}</div>
<div class="r">{map_block(178)}<p class="cap">{t("map_cap", "The neighbourhood · approximate travel times")}</p></div></div>'''

def render(html, path):
    html = html.replace("Rumah Márton", "Rumah&nbsp;Márton")   # the name never breaks across lines
    css = CSS
    if LANG == "zh":   # Chinese: Noto CJK beside the Latin faces
        css = css.replace("'Newsreader',serif", "'Newsreader','Noto Serif CJK SC',serif").replace("'Albert Sans',sans-serif", "'Albert Sans','Noto Sans CJK SC',sans-serif").replace("font-family:Newsreader", "font-family:Newsreader,'Noto Serif CJK SC'")
        css += "body{line-break:strict;word-break:normal} h1,h2{word-break:keep-all} .cl4 .a p.form{font-size:11pt;margin:1mm 0 4mm} .text h1{font-size:27pt;line-height:1.25} .eyebrow,.cap,.facts dt,.closing .links a,.inc h3,.spec h4,.cl4 h3,.cl4 .links a{letter-spacing:.1em}"
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{css}</style></head><body>{html}</body></html>'
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.set_content(doc, wait_until="load"); pg.wait_for_timeout(400)
        pg.pdf(path=str(path), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True); b.close()

def build(u):
    tmp = OUT / f"_{u['key']}{SUF}"; tmp.mkdir(exist_ok=True)
    render(cover_page(u) + location_page(), tmp / "cover.pdf")
    plan_pdfs = []
    for p in u["plans"]:
        html, png = plan_page(u, p)
        f = OUT / "plans" / f"rumah-marton-{p['slug']}{SUF}.pdf"; render(html, f); plan_pdfs.append(f)
        if not SUF: (OUT / "plans" / f"rumah-marton-{p['slug']}.png").write_bytes(png)
    render(closing_page(u), tmp / "closing.pdf")
    src = fitz.open(BRO); out = fitz.open()
    out.insert_pdf(fitz.open(tmp / "cover.pdf"))
    for f in plan_pdfs: out.insert_pdf(fitz.open(f))
    render("".join(visual_page(u, n, sub) for n, sub in u["visuals"]), tmp / "visuals.pdf")
    out.insert_pdf(fitz.open(tmp / "visuals.pdf"))
    out.insert_pdf(fitz.open(tmp / "closing.pdf"))
    out.set_metadata({"title": f"{t('doc_prefix', 'Rumah Márton')} · {u['name']}", "author": "WY Design"})
    out.save(OUT / u["file"], garbage=4, deflate=True)
    print(u["file"], out.page_count, "pages", (OUT / u["file"]).stat().st_size // 1024, "KB")

if __name__ == "__main__":
    for u in (GARDEN, PENTHOUSE): build(u)

# ---------- website: plan images (room numbers and north arrow included) and plan data ----------
WEB_MEDIA = pathlib.Path("/home/claude/rm/public/media/plans")
WEB_DATA = pathlib.Path("/home/claude/rm/src/content/plans.json")
TABS = {"penthouse-plan-3-bedrooms": "3 bedrooms", "penthouse-plan-2-bedrooms": "2 bedrooms", "penthouse-roof-terrace-plan": "Rooftop terrace", "garden-residence-plan": "Ground floor"}

def web_plans():
    """Plan images (English run only; they carry no words) + plan data and downloads for the current language."""
    WEB_MEDIA.mkdir(parents=True, exist_ok=True)
    data = {}
    pw = sync_playwright().start() if not SUF else None
    pg = pw.chromium.launch().new_page(device_scale_factor=2.4, viewport={"width": 1200, "height": 1000}) if pw else None
    for u in (GARDEN, PENTHOUSE):
        items = []
        for p in u["plans"]:
            png, rect, labels = plan_image(p["page"])
            if pg:
                html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{background:#fff}}</style></head><body><div id="b" style="position:relative;width:1000px;padding:0"><img src="{data_uri(png,"image/png")}" style="width:100%;display:block"></div></body></html>'
                pg.set_content(html, wait_until="load"); pg.wait_for_timeout(250)
                Image.open(io.BytesIO(pg.locator("#b").screenshot(type="png"))).convert("RGB").save(WEB_MEDIA / f"{p['slug']}.webp", "WEBP", quality=88, method=6)
            items.append(dict(slug=p["slug"], tab=T.get("tabs", TABS)[p["slug"]], title=p["title"], image=f"/media/plans/{p['slug']}.webp",
                              pdf=f"/downloads/rumah-marton-{p['slug']}{SUF}.pdf", labels=[[x, round(a, 4), round(b, 4)] for x, a, b in labels],
                              rooms=[list(r) for r in p["rooms"]], totals=[list(x) for x in p["totals"]], note=p.get("note", "")))
        data[u["key"]] = dict(name=u["name"], facts=u["facts"], plans=items)
    if pw: pw.stop()
    WEB_DATA.with_name(f"plans{SUF}.json").write_text(json.dumps(data, ensure_ascii=False, indent=1))
    dl = pathlib.Path("/home/claude/rm/public/downloads")
    (dl / f"rumah-marton-residence-01-garden{SUF}.pdf").write_bytes((OUT / GARDEN["file"]).read_bytes())
    (dl / f"rumah-marton-residence-03-penthouse{SUF}.pdf").write_bytes((OUT / PENTHOUSE["file"]).read_bytes())
    for p in GARDEN["plans"] + PENTHOUSE["plans"]:
        f = OUT / "plans" / f"rumah-marton-{p['slug']}{SUF}.pdf"; (dl / f.name).write_bytes(f.read_bytes())
    print("web plans", LANG, WEB_DATA.with_name(f"plans{SUF}.json").name)

if __name__ == "__main__":
    web_plans()
