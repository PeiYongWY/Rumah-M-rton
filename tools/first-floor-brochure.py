"""First Floor Residence brochure, same structure as the Garden and Penthouse residence brochures."""
import build as B, fitz
import brochure as R   # its image-page helper sets paired images side by side, uncropped
B.CSS += ".pair{display:flex;gap:4mm;align-items:flex-start;justify-content:center}"
B.visual_page = lambda u, pno, sub: R.vis(fitz.open(B.BRO), pno, u["name"] + (f" · {sub}" if sub else ""))
FIRST = dict(
    key="first", name="First Floor Residence", file="Rumah-Marton-First-Floor-Residence.pdf", vr="",
    lede="A three-bedroom residence on the first floor, with generous terraces on two sides, a private garden and provision for a dedicated outdoor kitchen and dining terrace.",
    facts=[("Floor", "First floor"), ("Bedrooms", "3 bedrooms, the third may be used as a study"),
           ("Interior", "110 m²"), ("Balcony and terraces", "46 m²"), ("Private garden", "361 m²")],
    cover=B.IMG + "first-floor-residence.jpg",
    plans=[dict(page=15, slug="first-floor-residence-plan", title="First floor plan",
                rooms=[("01", "Entrance foyer", "4.25"), ("02", "Kitchen and dining", "19.98"), ("03", "Living", "26.41"), ("04", "Corridor", "4.00"),
                       ("05", "Master suite", "16.32"), ("06", "Master bath", "5.76"), ("07", "Bedroom 02", "15.19"), ("08", "Bathroom", "5.44"),
                       ("09", "Bedroom 03 / study", "10.08"), ("10", "Private lobby", "2.20")],
                totals=[("Interior", "109.63", "strong"),
                        ("B1  Balcony", "7.39", ""), ("T1  Terrace", "25.82", ""), ("T2  Terrace", "12.69", ""), ("Outdoor", "45.90", "sub"),
                        ("Weighted area", "132.58", "strong", "outdoor areas at 50%"),
                        ("Private garden", "360.50", "garden")])],
    visuals=[(17, "Outdoor kitchen and dining"), (18, "Bathroom · Concept")],
)
B.build(FIRST)
