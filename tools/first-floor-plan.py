"""First Floor Residence plan, in the same format as the other standalone floor plans."""
import sys, build as B
B.BRO = sys.argv[1]   # the first-floor plan page (page 1 of the supplied PDF)
U = dict(name="First Floor Residence")
P = dict(page=1, slug="first-floor-residence-plan", title="First floor plan",
         rooms=[("01", "Entrance foyer", "4.25"), ("02", "Kitchen and dining", "19.98"), ("03", "Living", "26.41"), ("04", "Corridor", "4.00"),
                ("05", "Master suite", "16.32"), ("06", "Master bath", "5.76"), ("07", "Bedroom 02", "15.19"), ("08", "Bathroom", "5.44"),
                ("09", "Bedroom 03 / study", "10.08"), ("10", "Private lobby", "2.20")],
         totals=[("Interior", "109.63", "strong"),
                 ("B1  Balcony", "7.39", ""), ("T1  Terrace", "25.82", ""), ("T2  Terrace", "12.69", ""), ("Outdoor", "45.90", "sub"),
                 ("Weighted area", "132.58", "strong", "outdoor areas at 50%"),
                 ("Private garden", "360.50", "garden")])
html, png = B.plan_page(U, P)
out = B.OUT / "plans" / "rumah-marton-first-floor-residence-plan.pdf"
B.render(html, out); print(out)
