"""Rumah Márton residence PDFs — editable source.

Edit the CONTENT section (wording, areas, page order) and run:  python3 build.py
Output: out/Rumah-Marton-Garden-Residence.pdf, out/Rumah-Marton-Penthouse-Residence.pdf,
        out/plans/*.pdf (standalone floor plans) and out/plans/*.png (for the website).
Needs: Python 3, playwright (chromium), pymupdf, pillow, qrcode; the brochure PDF and fonts below.
"""
import base64, io, json, pathlib
import fitz
from PIL import Image, ImageFilter
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
BRO = "/home/claude/rm/public/downloads/rumah-marton-brochure.pdf"   # the full October brochure
IMG = "/home/claude/rm/src/assets/images/"
FONTS = "/home/claude/fonts/"
OUT = HERE / "out"; (OUT / "plans").mkdir(parents=True, exist_ok=True)
SITE = "https://rumahmarton.com/"   # the live website address — must match the domain you buy
NUDGE = {}   # (brochure page, room number): (x, y) shift as a share of the drawing
NORTH = 30   # degrees clockwise from "up" on the plans and site diagram (same orientation)

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
INCLUDED = [("Privacy & access", ["One residence per floor", "Direct lift access to a private lobby"]),
            ("Comfort & technology", ["Geothermal or air-source heat-pump heating and cooling, with no gas connection",
                                      "Heat-recovery ventilation with filtered fresh air",
                                      "High-performance triple glazing with naturally finished oak frames"]),
            ("Materials & finishes", ["Oak and limestone flooring", "Refined mineral plaster wall finishes", "Quality-finished lobby and bathroom areas"]),
            ("Outdoor living", ["Private outdoor living spaces", "Provision for a dedicated outdoor kitchen"])]
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
/* closing */
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
.inc h3{font-size:7.2pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;font-weight:400;margin:6mm 0 2mm}
.inc ul{list-style:none;margin:0;padding:0}
.inc li{font-family:'Newsreader',serif;font-size:11.2pt;line-height:1.4;padding:1.1mm 0}
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
    a = np.asarray(im).astype(int); ys, xs = np.where(a.sum(axis=2) < 735)
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
                if len(tx) <= 3 and s["bbox"][0] > rect[0] and s["bbox"][2] < rect[2] and s["bbox"][1] > rect[1] and s["bbox"][3] < rect[3]:
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
  <p class="eyebrow">Rumah Márton<br>Mártonhegy, Budapest</p><h2>{u["name"]}</h2><p class="eyebrow" style="margin-top:2mm">{p["title"]}</p>
  {sched_html(p)}{note}
  <p class="foot">Areas in m², based on the permitted plans.</p>
</div><div class="r"><div class="head">{head}</div>
  <div class="draw"><div class="box" style="width:{wmm:.1f}mm"><img src="{data_uri(png,'image/png')}">{lbl}</div></div>
</div></div>''', png

def cover_page(u):
    facts = "".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in u["facts"])
    return f'''<div class="page cover"><div class="l">
  <p class="eyebrow">Rumah Márton<br>Mártonhegy, Budapest</p><h1>{u["name"]}</h1><p class="lede">{u["lede"]}</p>
  <dl class="facts">{facts}</dl></div>
<div class="r"><img src="{data_uri(jpeg(u["cover"]),'image/jpeg')}"></div></div>'''

def closing_page(u):
    left = "".join(f"<p>{t.format(name=u['name'])}</p>" for t in CLOSING_LEFT)
    inc = "".join(f"<h3>{h}</h3><ul>{''.join(f'<li>{x}</li>' for x in items)}</ul>" for h, items in INCLUDED)
    return f'''<div class="page closing"><div class="c">
  <p class="eyebrow">Rumah Márton<br>Mártonhegy, Budapest</p><h2 style="font-size:28pt;margin:6mm 0 6mm">Be in touch</h2>{left}
  <ul class="links">
    <li><a href="{u["vr"]}">Explore the Residence in 360° <span>↗</span></a></li>
    <li><a href="{SITE}">Visit the Rumah Márton website <span>↗</span></a></li>
    <li><a href="https://www.wy-design.com/">Explore WY Design <span>↗</span></a></li>
    <li><a href="https://roadster.hu/peiyee-yong-interju">Meet Pei Yong — Read the Interview <span>↗</span></a></li>
  </ul>
  <p class="addr">Rumah Márton<br>Mártonvölgyi út, District XII, Budapest<br><a href="mailto:pei@wy-design.com">pei@wy-design.com</a></p>
  <p class="done">Planned completion — Q3 2028</p>
</div><div class="c inc"><p class="eyebrow">Included in every home</p>{inc}<p class="small">{SMALL_PRINT}</p></div></div>'''

def visual_page(u, pno, sub):
    d = fitz.open(BRO); info = d[pno - 1].get_image_info(xrefs=True)[0]
    pix = fitz.Pixmap(d, info["xref"]); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=92)
    cap = u["name"] + (f" · {sub}" if sub else "")
    return f'''<div class="page vis"><div class="frame"><img src="{data_uri(buf.getvalue(),'image/jpeg')}"><p class="cap">{cap}</p></div></div>'''

def render(html, path):
    doc = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS}</style></head><body>{html}</body></html>'
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(); pg.set_content(doc, wait_until="load"); pg.wait_for_timeout(400)
        pg.pdf(path=str(path), width="297mm", height="210mm", print_background=True, prefer_css_page_size=True); b.close()

def build(u):
    tmp = OUT / f"_{u['key']}"; tmp.mkdir(exist_ok=True)
    render(cover_page(u), tmp / "cover.pdf")
    plan_pdfs = []
    for p in u["plans"]:
        html, png = plan_page(u, p)
        f = OUT / "plans" / f"rumah-marton-{p['slug']}.pdf"; render(html, f); plan_pdfs.append(f)
        (OUT / "plans" / f"rumah-marton-{p['slug']}.png").write_bytes(png)
    render(closing_page(u), tmp / "closing.pdf")
    src = fitz.open(BRO); out = fitz.open()
    out.insert_pdf(fitz.open(tmp / "cover.pdf"))
    for f in plan_pdfs: out.insert_pdf(fitz.open(f))
    render("".join(visual_page(u, n, sub) for n, sub in u["visuals"]), tmp / "visuals.pdf")
    out.insert_pdf(fitz.open(tmp / "visuals.pdf"))
    out.insert_pdf(fitz.open(tmp / "closing.pdf"))
    out.set_metadata({"title": f"Rumah Márton · {u['name']}", "author": "WY Design"})
    out.save(OUT / u["file"], garbage=4, deflate=True)
    print(u["file"], out.page_count, "pages", (OUT / u["file"]).stat().st_size // 1024, "KB")

if __name__ == "__main__":
    for u in (GARDEN, PENTHOUSE): build(u)

# ---------- website: plan images (room numbers and north arrow included) and plan data ----------
WEB_MEDIA = pathlib.Path("/home/claude/rm/public/media/plans")
WEB_DATA = pathlib.Path("/home/claude/rm/src/content/plans.json")
TABS = {"penthouse-plan-3-bedrooms": "3 bedrooms", "penthouse-plan-2-bedrooms": "2 bedrooms", "penthouse-roof-terrace-plan": "Rooftop terrace", "garden-residence-plan": "Ground floor"}

def web_plans():
    WEB_MEDIA.mkdir(parents=True, exist_ok=True)
    data = {}
    with sync_playwright() as pw:
        b = pw.chromium.launch(); pg = b.new_page(device_scale_factor=2.4, viewport={"width": 1200, "height": 1000})
        for u in (GARDEN, PENTHOUSE):
            items = []
            for p in u["plans"]:
                png, rect, labels = plan_image(p["page"])
                w = 1000
                lbl = "".join(f'<span class="lbl" style="left:{x*100:.2f}%;top:{y*100:.2f}%;font-size:11.5px">{t}</span>' for t, x, y in labels)
                north = NORTH_SVG.replace('width="15mm" height="17.5mm"', 'width="54" height="63"')
                html = f'<!doctype html><html><head><meta charset="utf-8"><style>{CSS} body{{background:#fff}} .lbl{{position:absolute;transform:translate(-50%,-50%);font-family:Newsreader}}</style></head><body><div id="b" style="position:relative;width:{w}px;padding:0"><img src="{data_uri(png,"image/png")}" style="width:100%;display:block">{lbl}</div></body></html>'
                pg.set_content(html, wait_until="load"); pg.wait_for_timeout(250)
                shot = pg.locator("#b").screenshot(type="png")
                Image.open(io.BytesIO(shot)).convert("RGB").save(WEB_MEDIA / f"{p['slug']}.webp", "WEBP", quality=88, method=6)
                items.append(dict(slug=p["slug"], tab=TABS[p["slug"]], title=p["title"], image=f"/media/plans/{p['slug']}.webp",
                                  pdf=f"/downloads/rumah-marton-{p['slug']}.pdf",
                                  rooms=[list(r) for r in p["rooms"]], totals=[list(t) for t in p["totals"]], note=p.get("note", "")))
            data[u["key"]] = dict(name=u["name"], facts=u["facts"], plans=items)
        b.close()
    WEB_DATA.write_text(json.dumps(data, ensure_ascii=False, indent=1))
    # downloads for the website
    dl = pathlib.Path("/home/claude/rm/public/downloads")
    (dl / "rumah-marton-residence-01-garden.pdf").write_bytes((OUT / GARDEN["file"]).read_bytes())
    (dl / "rumah-marton-residence-03-penthouse.pdf").write_bytes((OUT / PENTHOUSE["file"]).read_bytes())
    for f in (OUT / "plans").glob("*.pdf"): (dl / f.name).write_bytes(f.read_bytes())
    print("web plans", sorted(x.name for x in WEB_MEDIA.iterdir()))

if __name__ == "__main__":
    web_plans()
