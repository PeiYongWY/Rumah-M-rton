# Builds the Neighbourhood map overlay (src/content/neighbourhood/{lang}.json -> "map")
# on the brochure's aerial image (public/media/neighbourhood-aerial.jpg, 1056x711).
# Positions come from real coordinates through an affine fit to five landmarks (error < 4 px).
import json, re
W, H, TOP = 1056, 711, 16
AFF = [[10840.877926, -139.292541], [113.576181, -16407.119846], [-211029.115747, 782377.64459]]
def P(la, ln): return (AFF[0][0]*ln + AFF[1][0]*la + AFF[2][0], AFF[0][1]*ln + AFF[1][1]*la + AFF[2][1] - TOP)
LM = [('Castle Hill', 13, 718, 372), ('Buda Castle', 13, 770, 462), ('Parliament', 18, 836, 285),
      ('St Stephen’s Basilica', 20, 928, 386), ('Citadella', 13, 846, 606), ('Central Market Hall', 15, 975, 608)]
LMT = {'hu': {'Castle Hill': 'Vár', 'Buda Castle': 'Budavári Palota', 'Parliament': 'Parlament', 'St Stephen’s Basilica': 'Szent István-bazilika', 'Citadella': 'Citadella', 'Central Market Hall': 'Központi Vásárcsarnok'},
       'zh': {'Castle Hill': '城堡山', 'Buda Castle': '布达城堡', 'Parliament': '国会大厦', 'St Stephen’s Basilica': '圣伊什特万大教堂', 'Citadella': '城堡要塞', 'Central Market Hall': '中央市场'}}
MIN = {'en': '{} min', 'hu': '{} perc', 'zh': '车程{}分钟'}
HOME = {'en': 'Rumah Márton', 'hu': 'Rumah Márton', 'zh': '玛顿山邸 Rumah Márton'}
# guide numbering -> coordinates
C = {1: (47.49464, 19.00165), 2: (47.49207, 19.00455), 3: (47.50868, 19.01137), 4: (47.51999, 18.97300), 5: (47.49487, 19.00322),
     6: (47.49836, 19.00340), 7: (47.50380, 19.00301), 8: (47.51009, 18.98267), 9: (47.53022, 18.97947), 10: (47.57013, 18.89998),
     11: (47.49094, 18.99765), 12: (47.49139, 19.01155), 13: (47.49637, 19.01776), 14: (47.49564, 19.02207), 15: (47.49080, 19.02401), 16: (47.50332, 18.96581)}
CALL = {1: (322, 446), 5: (414, 440), 11: (284, 566)}          # pins moved off the cluster, with a leader line
EDGE = {9: (123, 18, '↑'), 10: (22, 22, '↖'), 16: (18, 327, '←')}   # beyond the image: shown at the edge, pointing the way
pct = lambda x, y: f'left:{x / W * 100:.2f}%;top:{y / H * 100:.2f}%'
for lang in ['en', 'hu', 'zh']:
    p = f'src/content/neighbourhood/{lang}.json'; d = json.load(open(p))
    rows = {int(n): (c, nm) for c, n, nm in re.findall(r'<div class="k" data-place="\d+" data-cat="([a-z]+)"><span class="dot [a-z]+">(\d+)</span><span>(?:<a class="kn"[^>]*>|<span class="kn">)(.*?)(?:<span class="kgo"|</span>)', d['keys'])}
    lines, pins = [], []
    for n, (la, ln) in C.items():
        cat, name = rows[n]; x, y = P(la, ln); arrow = ''
        if n in EDGE: x, y, arrow = EDGE[n]
        elif n in CALL:
            cx, cy = CALL[n]; lines.append(f'<line x1="{x:.0f}" y1="{y:.0f}" x2="{cx}" y2="{cy}"/><circle cx="{x:.0f}" cy="{y:.0f}" r="2.6"/>'); x, y = cx, cy
        a = f'<span class="pin-arr" aria-hidden="true">{arrow}</span>' if arrow else ''
        pins.append(f'<button type="button" class="pin{" edge" if arrow else ""}" data-place="{n}" data-cat="{cat}" style="{pct(x, y)}" aria-label="{name}"><span class="pin-dot dot {cat}">{n}</span>{a}</button>')
    tags = []
    for nm, m, x, y in LM:
        t = LMT.get(lang, {}).get(nm, nm)
        tags.append(f'<span class="nb-lm{" nb-lm-pt" if nm == "Citadella" else ""}" style="{pct(x, y)}"><b>{t}</b><i>{MIN[lang].format(m)}</i></span>')
    hx, hy = 348, 513
    tags.append(f'<span class="nb-home" style="{pct(hx, hy + 14)}">{HOME[lang]}</span>')
    d['map'] = (f'<img src="/media/neighbourhood-aerial.jpg" width="{W}" height="{H}" alt="" loading="lazy" decoding="async">'
                f'<svg class="nb-lines" viewBox="0 0 {W} {H}" preserveAspectRatio="none" aria-hidden="true">{"".join(lines)}</svg>'
                + ''.join(tags) + ''.join(pins))
    d['keys'] = re.sub(r'<a class="kn"[^>]*>(.*?)<span class="kgo" aria-hidden="true"> ↗</span></a>', r'<span class="kn">\1</span>', d['keys'])
    d.pop('svg', None); d.pop('note', None)
    d['lead'] = {'en': 'Strong Hungarian schools nearby.', 'hu': 'Kiváló magyar iskolák a közelben.', 'zh': '附近有优质的匈牙利学校。'}[lang]
    json.dump(d, open(p, 'w'), ensure_ascii=False, indent=1)
    print(lang, len(pins), 'pins', d['keys'].count('class="kn"'))
