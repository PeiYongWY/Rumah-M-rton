"""Rumah Márton project brochure, in the style of the residence PDFs.

Source pages (images, map, plans) come from the October brochure; all text is set here.
Run:  python3 brochure.py   ->  out/Rumah-Marton-Brochure.pdf
"""
import fitz, io
from PIL import Image
import build as B

SRC = "/home/claude/work/bro/src.pdf"   # 2026_Rumah_Marton_WY_For_Claude.pdf
OUT = B.OUT / "Rumah-Marton-Brochure.pdf"   # build_lang.py changes this per language
EYEBROW = "Rumah Márton<br>Mártonhegy, Budapest"
t = B.t

# ============================== CONTENT ==============================
COVER = dict(lede="A thoughtful home of quiet luxury, nestled in Mártonhegy, Budapest.",
             facts=[("Address", "Mártonvölgyi út, Budapest XII"),
                    ("Status", "Building permit granted<br>Condominium establishment registered"), ("Completion", "Planned for Q3 2028")],
             image=B.IMG + "hero-living-night.png")
INTRO = dict(title="Thoughtful spaces. Tactile materials. Timeless presence.", body=[
    "Tucked into the tranquil hills of Mártonhegy, one of Budapest’s most sought-after enclaves, Rumah Márton is a rare collection of three exclusive residences, each conceived as a private villa. With one residence per floor, direct lift access, sun-filled interiors and expansive terraces that open to private gardens or rooftop views, each with provision for an outdoor kitchen, every home invites a new way of apartment living, where the seclusion of a villa meets the refinement of a curated retreat.",
    "This is not a typical development, but a crafted living experience shaped with care and intention by an award-winning team. Elegant spatial planning and thoughtful proportions guide the architecture, and every turn within the home reveals a view. A palette of finely grained oak, soft-toned limestone and mineral lime plaster is complemented by custom planter balconies and expansive triple-glazed glass walls with minimal frames, all reflecting a commitment to quiet, enduring luxury.",
    "As the second release in the WY Rumah series, Rumah Márton continues a vision of creating homes that are thoughtful, tactile and timeless, designed and built with genuine care and craft."])
LOCATION = dict(title="An elevated life in Budapest’s most distinguished, yet hidden retreat", body=[
    "Rumah Márton lies in the heart of District XII, one of Budapest’s oldest and most prestigious neighbourhoods, famed for its aristocratic villas, forested hills and timeless elegance. This historic enclave, known as Hegyvidék, offers a rare blend of natural beauty, cultural richness and modern ease.",
    "Set on a quiet one-way street, the residence is discreetly positioned on a gentle slope within a 1,100 m² plot, ensuring both privacy and low visibility. From its elevated position, the house offers panoramic views of Castle Hill and the Citadella. The surrounding greenery brings not only fresh air and serenity, but a sense of retreat, just minutes from the urban core.",
    "The neighbourhood is home to top-tier international and local schools, refined cafés such as Villa Bagatelle, and upscale destinations like Hegyvidék Shopping Centre, MOM Park and Mammut. Cultural landmarks and recreational escapes, from Normafa to the Buda Hills, are moments away."])
MAP_NAMES = {"Te British International School (BISB)": "The British International School (BISB)", "Hegyvidek Shopping Centre": "Hegyvidék Shopping Centre",
             "Mom Park": "MOM Park", "Margit Sziget": "Margaret Island", "Andrassy Ut": "Andrássy út", "Martonhegy": "Rumah Márton"}
POINTS = [("A single residence per floor.", "A rare trio of two apartments and one villa-style penthouse."),
                ("Private gardens, rooftop terraces and outdoor kitchens.", ""),
          ("Unfolding to panoramic views of Castle Hill and the Citadella.", ""),
          ("Private basement parking. Dedicated storage.", ""),
          ("Understated sophistication. Quiet luxury.", ""),
          ("Crafted with care.", "The second limited-edition series by WY Design.")]
TEAM = dict(title="The team behind Rumah Márton", body=[
    "Rumah Márton is shaped by an award-winning team — WY Design, Kettőpera Architects and a trusted local builder — brought together by a shared commitment to quality, thoughtful design and enduring craftsmanship.",
    "Guided by a sensitivity to how spaces are lived in, made and built, the team is shaping a residence where care is present in every decision, from architectural intent to material selection to the precision of construction. Every element has been approached with a long view: designed to age gracefully, to support daily comfort and to embody a quiet kind of permanence.",
    "This is a home defined not by statement, but by substance — a place where quality is felt in its making, and in the way it continues to live over time."])
SPEC = [
 [[("Building services", "Comfort, conditioning and ventilation", ["Ceiling-integrated heating and cooling, complemented by underfloor heating, powered by high-efficiency geothermal or air-source heat pumps for year-round comfort", "Dedicated central air ventilation with integrated pollen and dust filters", "Smart-home infrastructure is included for future integration with Loxone or a comparable smart-home system; full smart controls are available as an optional upgrade", "Bathrooms feature underfloor heating and electric towel warmers", "An electrically heated driveway ensures safe access during winter"]),
   ("", "Ventilation", ["All rooms offer natural ventilation through openable windows", "Fresh air supplied via an energy-efficient heat-recovery system", "Mechanical exhaust ventilation provided for bathrooms"]),
   ("", "Renewable energy", ["Entirely electric-powered system, with no gas connection", "Energy sourced from sustainable geothermal systems", "Provision for a future solar energy system is included, with rooftop solar panels, inverters and integrated battery storage available as optional upgrades", "Shared systems, i.e. lighting, heating and driveway heating, are powered through a communal meter"]),
   ("", "Home automation (smart home)", ["Keyless access and the smart-ready infrastructure described below are included; additional control devices, software, programming, commissioning and system integrations are available as optional upgrades", "Keyless access by password or fob for garage doors, entrances, gates and lift", "Multi-room audio cabling, ready for the addition of ceiling-mounted speakers", "Provision for an in-wall touch-screen panel integrating lighting, climate, shutters and video intercom", "Provision for local control panels offering personalised zoned adjustment", "Remote access and management through a mobile app", "Smart automated window blinds for comfort and energy efficiency"])],
  [("Residents’ facilities", "Basement garage", ["Secure, access-controlled underground parking, with 6 parking spaces in total", "Dedicated three-phase EV-ready connection linked to the apartment’s individual meter; charging unit supplied separately", "Bicycle storage"]),
   ("", "Security", ["Controlled lift access with individual password or fob authorisation for each apartment", "High-security locks on all external doors", "Discreet CCTV coverage at principal corridors and access points", "Private CCTV at apartment entrances and terraces, accessible only to the respective residents", "Video intercom and apartment alarm systems are available as optional upgrades"]),
   ("", "Residential storage", ["Private, secured basement storage rooms of 15–18 m²"]),
   ("", "Garden and outdoor spaces", ["Exclusive garden access for designated apartments:", "Ground floor: private front garden (as per plans)", "First floor: designated rear gardens (as per plans)", "Penthouse: exclusive use of the rooftop terrace, with access to others only by agreement", "Each apartment includes provision for a private outdoor kitchen", "Automated irrigation system with programmable scheduling for effortless garden maintenance"])]],
 [[("Exterior finishes", "External walls", ["Enduring, water-repellent mineral plaster and limestone façade finish"]),
   ("", "Windows", ["Triple-glazed windows with naturally finished oak interiors, by Josko or an equivalent brand", "Woven textile blinds function as integrated mosquito screens for added comfort"]),
   ("", "External doors", ["Full-height pocket sliding doors onto terraces and minimal-frame sliding doors to balconies", "Natural wooden entrance doors for each apartment", "Fire-rated basement doors"]),
   ("", "Balconies and terraces", ["Sculpted metal railings softened by integrated greenery", "Frost-resistant, non-slip limestone flooring"]),
   ("Entrance areas and lift", "", ["Quietly inviting limestone-clad lobby with softly lit ceiling coffers", "Direct private lift access to each apartment, with upper-floor homes featuring a naturally finished private foyer, warmly illuminated by recessed lighting"]),
   ("Maintenance", "", ["Maintenance and housekeeping services for the garden, lift lobby and shared areas, included under an agreed management fee"])],
  [("Apartment finishes", "Flooring", ["Underfloor heating system with high-grade acoustic and thermal insulation", "Light-toned oak flooring with natural grain, laid in a contemporary pattern throughout all bedrooms and the penthouse living and dining areas", "Pale honed limestone flooring, or a comparable finish, to lower-floor living and kitchen areas", "Matching stone to bathroom floors and walls"]),
   ("", "Ceiling", ["Generous 2,700 mm ceiling height throughout all floors", "Lower-floor apartments feature suspended plasterboard ceilings with discreetly integrated building services and recessed ambient lighting", "The penthouse has treated slab ceilings, with lighting integrated into extruded linear profiles for a clean, minimalist finish"]),
   ("", "Internal walls and doors", ["Acoustically insulated internal walls with a refined plaster finish", "Understated interior doors in oak veneer or a comparable finish, with minimalist detailing"]),
   ("", "Bathrooms", ["Curated sanitary ware from Axor, Dornbracht, Duravit or a comparable manufacturer, with final selections confirmed in the unit-specific specification", "Architectural brassware in a refined, coordinated finish", "Heated towel rails for added comfort", "Openable windows in bathrooms provide natural ventilation"]),
   ("", "Kitchens", ["Tailored oak-veneered cabinetry, natural limestone worktops and splashbacks, together with stone-slab islands for larger apartments, are available as optional fit-out selections"]),
   ("", "Appliances and electrical fittings", ["Thoughtfully positioned plumbing and electrical connections for kitchen and laundry appliances", "Curated appliance packages from Gaggenau, Miele or comparable manufacturers are available as optional fit-out selections", "Elegantly detailed electrical outlets by Berker or an equivalent manufacturer are included, with Loxone controls available as part of the optional smart-home package"]),
   ("", "Interior lighting", ["Considered lighting design with direct and indirect illumination, including integrated LED strips", "Provision for advanced lighting control, including scene-setting and dimming", "Provision for table and floor-standing lamps to connect to the optional lighting control system"])]]]
SPEC_NOTE = "The final specification is tailored to the agreed purchase price and any optional upgrades selected, as confirmed in the unit-specific specification."
FIRST_FLOOR = dict(page=15, slug="first-floor-plan", title="Floor plan · Sold",
    rooms=[("01", "Entrance foyer", "4.25"), ("02", "Kitchen and dining", "19.98"), ("03", "Living", "26.41"), ("04", "Corridor", "4.00"),
           ("05", "Master suite", "16.32"), ("06", "Master bath", "5.76"), ("07", "Bedroom 02", "15.19"), ("08", "Bathroom", "5.44"),
           ("09", "Bedroom 03 / study", "10.08"), ("10", "Private lobby", "2.20")],
    totals=[("Interior", "109.63", "strong"), ("B1  Balcony", "7.39", ""), ("T1  Terrace", "25.82", ""), ("T2  Terrace", "12.69", ""), ("Outdoor", "45.90", "sub")])
CLOSING = ["We would love to show you the site and talk you through the plans for Rumah Márton.",
           "If you wish, we can also explore how the finishes, specifications and spaces might be tailored to your needs, guided by our award-winning architectural team and subject to design and construction feasibility.",
           "Detailed specifications, pricing, payment stages and terms, and the planned construction programme are available on request."]
LINKS = [("Explore the Garden Residence in 360°", B.GARDEN["vr"]), ("Explore the Penthouse in 360°", B.PENTHOUSE["vr"]),
         ("Visit the Rumah Márton website", B.SITE + ("" if B.LANG == "en" else B.LANG + "/")), ("Explore WY Design", "https://www.wy-design.com/"),
         ("Meet Pei Yong — Read the Interview", "https://roadster.hu/peiyee-yong-interju")]
PRESS = [("Designboom", "https://www.designboom.com/architecture/mirrored-twin-houses-wy-design-hungarian-village-charm-10-10-2024/"),
         ("EDGE International Award", "https://epiteszforum.hu/egy-uj-videki-tipologia-kiserlete--ket-szin-ikerhaz"),
         ("BIG SEE Architecture Award", "https://bigsee.eu/almost-mirrored-twin-house/"), ("BIG SEE Interior Award", "https://bigsee.eu/vamhaz/")]
# visual pages: (source page, caption)
V = lambda n, c: ("vis", n, c)
SEQUENCE = [("cover",), ("intro",), V(4, "Mártonhegy, Budapest XII"), ("location",), ("map",),
            V(7, "Garden Residence"), ("points",), V(9, "The view from Mártonhegy"),
            V(10, "Garden Residence"), ("plan", "garden", 0), V(12, "Garden Residence · Living"), V(13, "Garden Residence · Master suite"), V(14, "Garden Residence · Second bedroom"),
            V(16, "Outdoor kitchen and dining"), V(18, "Bathroom · Concept"),
            ("plan", "penthouse", 0), ("plan", "penthouse", 1), ("plan", "penthouse", 2),
            V(22, "Penthouse Residence"), V(23, "Penthouse Residence · Master suite"), V(24, "Penthouse Residence · Second bedroom"), V(25, "Penthouse Residence · Study"),
            V(26, "Penthouse Residence"), V(27, "Penthouse Residence"), V(28, "Penthouse Residence · Rooftop terrace"),
            ("team",), ("spec", 0), ("spec", 1), ("closing",)]
# =====================================================================

CSS = B.CSS + """
.text{display:grid;grid-template-columns:1fr 1fr;padding:17mm 18mm 15mm 15mm;column-gap:16mm}
.text .h{display:flex;flex-direction:column}
.text h1{font-size:30pt;line-height:1.08;margin:8mm 0 0;max-width:118mm}
.text .b{align-self:end}
.text .b p{font-size:9.6pt;line-height:1.65;margin:0 0 4mm;max-width:118mm}
.pts{display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;padding:16mm}
.pts ol{list-style:none;margin:6mm 0 0;padding:0;display:grid;gap:5.2mm}
.pts .lead{font-family:'Newsreader',serif;font-size:17pt;margin:0}
.pts .det{font-size:8.6pt;color:#77736D;margin:1.2mm 0 0}
.map{display:flex;align-items:center;justify-content:center;flex-direction:column;padding:14mm 18mm 12mm}
.map .cap{margin:5mm 0 0}
.map .mb{position:relative}
.map .mb img{display:block}
.tag{position:absolute;transform:translate(-50%,-50%);background:rgba(250,250,248,.92);padding:.8mm 1.6mm;text-align:center;white-space:nowrap;font-size:5.6pt;line-height:1.3;letter-spacing:.06em;color:#1D1C1A}
.tag b{display:block;font-weight:400;text-transform:uppercase;letter-spacing:.14em;font-size:5pt}
.tag.home{background:#1D1C1A;color:#FAFAF8}
.spec{display:grid;grid-template-columns:1fr 1fr;column-gap:14mm;padding:13mm 16mm 10mm 15mm;grid-template-rows:auto 1fr auto}
.spec .top{grid-column:1/-1;margin-bottom:2mm}
.spec h4{font-size:6.4pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;font-weight:400;margin:3.4mm 0 1mm}
.spec h5{font-family:'Newsreader',serif;font-weight:400;font-size:9.4pt;margin:1.8mm 0 .5mm}
.spec ul{list-style:none;margin:0;padding:0}
.spec li{font-size:7.1pt;line-height:1.4;padding:.25mm 0 .25mm 3mm;position:relative;color:#3E3B37}
.spec li::before{content:"";position:absolute;left:0;top:2.1mm;width:1.2mm;border-top:.2mm solid #9A958D}
.spec .note{grid-column:1/-1;font-size:6.8pt;color:#8C877F;margin:4mm 0 0}
.pair{display:flex;gap:4mm;align-items:flex-start;justify-content:center}
.cl2{grid-template-columns:1.05fr 1fr}
.cl2 .c{padding:15mm 12mm 12mm 15mm}
.cl2 .c + .c{background:transparent;justify-content:center}
.cl2 p{font-size:8.8pt;line-height:1.55;margin-bottom:2.2mm}
.cl2 .bh{font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;font-weight:400;margin:4mm 0 1.6mm}
.cl2 .links{margin-top:4mm;gap:2.3mm}
.cl2 .links a{white-space:nowrap}
.cl2 .addr{margin-top:8mm}
.cl2 .ph .small{margin-top:6mm}
.cl2 figure{margin:0}
.cl2 figure img{width:100%;height:auto;display:block}
.cl2 .small{margin-top:auto}
.cl3 .c{padding:17mm 14mm 13mm 15mm}
.cl3 h2{font-size:28pt;margin:6mm 0 6mm}
.cl3 h3{font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;font-weight:400;margin:5mm 0 1.6mm}
.cl3 .c:first-child p{font-size:9.2pt;line-height:1.6;margin:0 0 3mm;max-width:112mm}
.cl3 .links{margin-top:5mm;gap:2.6mm}
.cl3 .addr{margin-top:auto;padding-top:8mm}
.cl3 .c:first-child p.addr{font-size:12pt;line-height:1.5;margin:0}\n.cl3 .c:first-child p.done{margin:5mm 0 0;font-size:7.2pt}
.cl3 .quiet{list-style:none;margin:3mm 0 0;padding:0;display:grid;gap:1.8mm}
.cl3 .quiet a{font-family:'Newsreader',serif;font-size:10pt;color:#6E6A64;text-decoration:none}
.cl3 .quiet a span{font-size:.8em}
.cl4{display:grid;grid-template-columns:1fr 1fr;grid-template-rows:auto auto 1fr;background:linear-gradient(90deg,#FAFAF8 50%,#F2EEE7 50%)}
.cl4 .a{padding:0 14mm 0 15mm}
.cl4 .b{padding:0 14mm 0 15mm}
.cl4 > .a:first-child{padding-top:17mm}
.cl4 h2{font-size:28pt;margin:6mm 0 6mm}
.cl4 h3{font-size:6.8pt;letter-spacing:.2em;text-transform:uppercase;color:#77736D;font-weight:400;margin:5mm 0 1.6mm}
.cl4 h3.first{margin-top:0}
.cl4 .a p{font-size:9.2pt;line-height:1.6;margin:0 0 3mm;max-width:112mm}
.cl4 .links{list-style:none;margin:5mm 0 0;padding:0;display:grid;gap:2.6mm}
.cl4 .b h3.first{margin-top:5mm}
.cl4 .links a{font-size:7.6pt;letter-spacing:.2em;text-transform:uppercase;color:#1D1C1A;text-decoration:none;border-bottom:.25mm solid #1D1C1A;padding-bottom:.8mm}
.cl4 .links a span{letter-spacing:0}
.cl4 .quiet{list-style:none;margin:0;padding:0;display:grid;gap:1.8mm}
.cl4 .quiet.top{margin-top:4.4mm;gap:2.6mm}
.cl4 .quiet a{font-family:'Newsreader',serif;font-size:10pt;color:#6E6A64;text-decoration:none}
.cl4 .quiet a span{font-size:.8em}
.cl4 .foot{align-self:end;padding-bottom:13mm}
.cl4 .mail a{font-family:'Newsreader',serif;font-size:15pt;color:#1D1C1A;text-decoration:none;border-bottom:.25mm solid #1D1C1A}
.cl4 .a p.mail{margin:0 0 2mm}
.cl4 .a p.form{margin:0 0 4mm;font-size:8.4pt}
.cl4 .form a{color:#4A4743;text-decoration:none;border-bottom:.2mm solid #B9B4AC}
.cl4 .a p.meta{font-size:6.6pt;letter-spacing:.14em;text-transform:uppercase;color:#8C877F;margin:0}
.cl4 .small{font-size:6.6pt;line-height:1.5;color:#8C877F;margin:0}
.fin{display:flex;flex-direction:column;align-items:center;text-align:center;padding:20mm 40mm 11mm}
.fin h2{font-style:italic;font-size:30pt;line-height:1.12;max-width:190mm;margin:9mm 0 8mm}
.fin .txt{max-width:132mm}
.fin .txt p{font-size:9pt;line-height:1.6;margin:0 0 2.6mm;color:#3E3B37}
.fin .mail{margin:6mm 0 1.5mm}
.fin .mail a{font-family:'Newsreader',serif;font-size:17pt;color:#1D1C1A;text-decoration:none;border-bottom:.25mm solid #1D1C1A}
.fin .ad{font-size:7pt;letter-spacing:.16em;text-transform:uppercase;color:#77736D;margin:2mm 0 7mm}
.fin .prim{display:flex;gap:8mm;justify-content:center}
.fin .prim a{font-size:7.4pt;letter-spacing:.2em;text-transform:uppercase;color:#1D1C1A;text-decoration:none;border-bottom:.25mm solid #1D1C1A;padding-bottom:.8mm}
.fin .prim a span{letter-spacing:0}
.fin .sec{margin:6mm 0 0;font-size:6.8pt;color:#8C877F;max-width:200mm;line-height:1.7}
.fin .sec a{color:#8C877F;text-decoration:none}
.fin .fine{margin-top:auto;font-size:6.2pt;color:#A39E96;max-width:200mm}
.closing .press{list-style:none;margin:2mm 0 0;padding:0;display:grid;gap:1.6mm}
.closing .press a{font-family:'Newsreader',serif;font-size:9.2pt;color:#6E6A64;color:#1D1C1A;text-decoration:none}
.closing .press a span{font-size:.8em}
"""

def img_bytes(doc, xref, q=92):
    pix = fitz.Pixmap(doc, xref); pix = fitz.Pixmap(fitz.csRGB, pix) if pix.n > 3 else pix
    im = Image.open(io.BytesIO(pix.tobytes("png"))).convert("RGB"); buf = io.BytesIO(); im.save(buf, "JPEG", quality=q); return buf.getvalue(), im.size

def vis(doc, n, cap):
    infos = sorted(doc[n - 1].get_image_info(xrefs=True), key=lambda i: i["bbox"][0])
    if len(infos) == 1:
        b, _ = img_bytes(doc, infos[0]["xref"])
        return f'<div class="page vis"><div class="frame"><img src="{B.data_uri(b,"image/jpeg")}"><p class="cap">{cap}</p></div></div>'
    parts = [img_bytes(doc, i["xref"]) for i in infos]
    H = 160  # mm, equal heights, widths follow each image's own proportions
    ws = [H * w / h for _, (w, h) in parts]; k = min(1, (261 - 4 * (len(ws) - 1)) / sum(ws))
    imgs = "".join(f'<img src="{B.data_uri(b,"image/jpeg")}" style="height:{H*k:.1f}mm;width:{w*k:.1f}mm;max-width:none;max-height:none">' for (b, _), w in zip(parts, ws))
    return f'<div class="page vis"><div class="frame"><div class="pair">{imgs}</div><p class="cap">{cap}</p></div></div>'

def text_page(d, facts=None):
    body = "".join(f"<p>{p}</p>" for p in d["body"])
    fx = f'<dl class="facts" style="margin-top:auto;max-width:105mm">{"".join(f"<dt>{a}</dt><dd>{b}</dd>" for a, b in facts)}</dl>' if facts else ""
    return f'<div class="page text"><div class="h"><p class="eyebrow">{EYEBROW}</p><h1>{d["title"]}</h1>{fx}</div><div class="b">{body}</div></div>'

def cover(doc):
    info = doc[2].get_image_info(xrefs=True)[0]; img, _ = img_bytes(doc, info["xref"])
    return f'''<div class="page cover"><div class="l"><p class="eyebrow">{EYEBROW}</p><h1>{t("cover_title", "Rumah Márton")}</h1><p class="lede">{COVER["lede"]}</p></div>
<div class="r"><img src="{B.data_uri(img,"image/jpeg")}"></div></div>'''

def points():
    li = "".join(f'<li><p class="lead">{a}</p>{f"<p class=det>{b}</p>" if b else ""}</li>' for a, b in POINTS)
    return f'<div class="page pts"><p class="eyebrow">{EYEBROW}</p><h2 style="margin:5mm 0 1.5mm;font-size:26pt">{t("pts_head", "A curated way of living")}</h2><p class="det" style="font-size:9pt;max-width:120mm;margin:0 0 3mm">{t("pts_sub", "Conceived by an award-winning team with a thoughtful approach to design and uncompromising attention to detail.")}</p><ol>{li}</ol></div>'

def mappage(doc):
    return f'''<div class="page map">{B.map_block(234)}<p class="cap">{t("map_cap", "The neighbourhood · approximate travel times")}</p></div>'''

def spec(i):
    cols = ""
    for col in SPEC[i]:
        h = ""
        for grp, head, lines in col:
            if grp: h += f"<h4>{grp}</h4>"
            if head: h += f"<h5>{head}</h5>"
            h += "<ul>" + "".join(f"<li>{x}</li>" for x in lines) + "</ul>"
        cols += f"<div>{h}</div>"
    note = f'<p class="note">{SPEC_NOTE}</p>' if i == 1 else ""
    return f'<div class="page spec"><div class="top"><p class="eyebrow">{EYEBROW}</p><h2>{t("spec_title", "Specification")}</h2></div>{cols}{note}</div>'

def SECONDARY(): return [l for l in LINKS if "wy-design.com" in l[1] or "roadster" in l[1]]
def PRIMARY(): return [l for l in LINKS if not ("wy-design.com" in l[1] or "roadster" in l[1])]

def closing(doc):
    info = doc[31].get_image_info(xrefs=True)[0]; img, _ = img_bytes(doc, info["xref"])
    photo = f'<div class="page vis"><div class="frame"><img src="{B.data_uri(img,"image/jpeg")}"></div></div>'
    paras = "".join(f"<p>{t}</p>" for t in CLOSING)
    li = lambda L: "".join(f'<li><a href="{u}">{t} <span>↗</span></a></li>' for t, u in L)
    form = B.SITE.rstrip("/") + f"/{B.LANG}/#enquire"
    # one grid for both columns, so the right-hand links start level with the residence links
    return photo + f'''<div class="page cl4">
<div class="a"><p class="eyebrow">{EYEBROW}</p><h2>{t("get_in_touch", "Get in touch")}</h2>{paras}<h3>{B.BESPOKE[0]}</h3><p>{B.BESPOKE[1]}</p></div>
<div class="b"></div>
<div class="a"><ul class="links">{li(PRIMARY())}</ul></div>
<div class="b"><ul class="quiet top">{li(SECONDARY())}</ul><h3>{t("recognition", "Selected recognition")}</h3><ul class="quiet">{li(PRESS)}</ul></div>
<div class="a foot"><p class="mail"><a href="mailto:pei@wy-design.com">pei@wy-design.com</a></p>
<p class="form"><a href="{form}">{t("online", "Or send us a message online")} ↗</a></p>
<p class="meta">{t("meta", "Mártonvölgyi út, Budapest XII · Completion Q3 2028")}</p></div>
<div class="b foot"><p class="small">{B.SMALL_PRINT}</p></div>
</div>'''

def main():
    doc = fitz.open(SRC); html = []
    for item in SEQUENCE:
        k = item[0]
        if k == "cover": html.append(cover(doc))
        elif k == "intro": html.append(text_page(INTRO, COVER["facts"]))
        elif k == "location": html.append(text_page(LOCATION))
        elif k == "team": html.append(text_page(TEAM))
        elif k == "map": html.append(mappage(doc))
        elif k == "points": html.append(points())
        elif k == "vis": html.append(vis(doc, item[1], item[2]))
        elif k == "plan":
            u = B.GARDEN if item[1] == "garden" else B.PENTHOUSE
            html.append(B.plan_page(u, u["plans"][item[2]])[0])
        elif k == "spec": html.append(spec(item[1]))
        elif k == "closing": html.append(closing(doc))
    B.CSS = CSS
    B.render("".join(html), OUT)
    out = fitz.open(OUT); out.set_metadata({"title": t("doc_title", "Rumah Márton · Mártonhegy, Budapest"), "author": "WY Design"}); out.save(str(OUT) + ".tmp", garbage=4, deflate=True)
    import os; os.replace(str(OUT) + ".tmp", OUT)
    print(OUT.name, fitz.open(OUT).page_count, "pages", OUT.stat().st_size // 1024, "KB")

if __name__ == "__main__":
    main()
