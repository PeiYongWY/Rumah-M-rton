import sys
from playwright.sync_api import sync_playwright
ROT=float(sys.argv[1]); OUT=sys.argv[2]
OX,OY=161.4,275.7
def P(pts): return " ".join(f"{x-OX:.1f},{y-OY:.1f}" for x,y in pts)
plot=[(969.6,561.4),(969.1,275.7),(262.4,275.7),(161.4,561.4)]
house=[(478.9,351.7),(660.3,351.7),(660.3,500.3),(478.9,500.3)]   # terrace bands above and below both 31.7                      # a clean square block
terrace=[(478.9,320.0),(712,320.0),(712,532),(478.9,532)]   # wraps north, east and south; the house sits on top # wider L, east and south
garden=[(478.9,561.4),(821.9,561.4),(821.9,320.0),(712,320.0),(712,532),(478.9,532)]
strip=[(478.9,275.7),(821.9,275.7),(821.9,320.0),(478.9,320.0)]                      # may become theirs later
W,H=808.2,285.7
svg=f'''<svg viewBox="-12 -70 {W+90} {H+84}" xmlns="http://www.w3.org/2000/svg">
<defs><pattern id="h" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" stroke="#A89E8E" stroke-width=".5"/></pattern></defs>
<polygon points="{P(plot)}" fill="#F3F1EC" stroke="#1D1C1A" stroke-width=".9" stroke-dasharray="7 3 1.5 3"/>
<polygon points="{P(strip)}" fill="#DFE6D5" stroke="#8C9C80" stroke-width=".6" stroke-dasharray="3 2.5"/>
<polygon points="{P(garden)}" fill="#D3DCC7" stroke="#5E7154" stroke-width=".8"/>
<polygon points="{P(terrace)}" fill="#EFEAE0" stroke="#1D1C1A" stroke-width=".8" stroke-dasharray="4 3"/>
<polygon points="{P(house)}" fill="#FFFFFF" stroke="#1D1C1A" stroke-width="1.7"/>
<g transform="translate({W+40},-34) scale(1.25)">
 <circle r="17" fill="none" stroke="#1D1C1A" stroke-width=".8"/>
 <g transform="rotate({ROT})"><path d="M0 -13 L4.2 6 L0 3 L-4.2 6 Z" fill="#1D1C1A"/><path d="M0 3 L4.2 6 L0 13 L-4.2 6 Z" fill="none" stroke="#1D1C1A" stroke-width=".6"/>
 <text x="0" y="-19.5" text-anchor="middle" transform="rotate({-ROT} 0 -23.5)" font-family="Newsreader, serif" font-size="12" fill="#1D1C1A">N</text></g>
</g></svg>'''
open(OUT.replace('.pdf','.svg'),'w').write(svg)
html=f'''<!doctype html><html><head><meta charset="utf-8"><style>@page{{size:297mm 210mm;margin:0}}
html,body{{margin:0;background:#FAFAF8;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.p{{width:297mm;height:210mm;display:flex;align-items:center;justify-content:center;padding:18mm;box-sizing:border-box}} svg{{width:100%;height:auto}}</style></head>
<body><div class="p">{svg}</div></body></html>'''
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(); pg.set_content(html); pg.wait_for_timeout(300)
    pg.pdf(path=OUT,width='297mm',height='210mm',print_background=True); b.close()
