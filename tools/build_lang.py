"""Build every Rumah Márton PDF in one language:  python3 build_lang.py hu|zh|en
Residence brochures, standalone floor plans, project brochure, and the website's plan data + downloads."""
import sys, shutil
import build as B
lang = sys.argv[1]
if lang != "en":
    import pdf_i18n as I
    B.LANG, B.SUF, B.T = lang, f"-{lang}", I.T[lang]
    tr = lambda d, x: d[lang].get(x, x)
    def cap(c): return " · ".join(tr(I.CAPTIONS, part) for part in c.split(" · ")) if c else c
    def tot(label):
        code, _, rest = label.partition("  ")
        return f"{code}  {tr(I.TOTALS, rest)}" if rest else tr(I.TOTALS, label)
    for u in (B.GARDEN, B.PENTHOUSE):
        u.update(I.UNITS[lang][u["key"]])
        u["visuals"] = [(n, tr(I.CAPTIONS, s)) for n, s in u["visuals"]]
        for p in u["plans"]:
            p["title"] = tr(I.PLAN_TITLES, p["title"])
            if p.get("note"): p["note"] = tr(I.PLAN_TITLES, p["note"])
            p["rooms"] = [(n, tr(I.ROOMS, r), a) for n, r, a in p["rooms"]]
            p["totals"] = [tuple([tot(x[0])] + list(x[1:3]) + ([tr(I.TOTALS, x[3])] if len(x) > 3 else [])) for x in p["totals"]]
    for k, v in I.RES[lang].items(): setattr(B, k, v)
import brochure as R
if lang != "en":
    b = I.BRO[lang]
    R.EYEBROW = b["EYEBROW"]; R.COVER = dict(R.COVER, lede=b["COVER_lede"], facts=b["COVER_facts"])
    for k in ("INTRO", "LOCATION", "POINTS", "TEAM", "SPEC", "SPEC_NOTE", "CLOSING"): setattr(R, k, b[k])
    R.LINKS = [(lab, url) for lab, (_, url) in zip(b["LINK_LABELS"], R.LINKS)]
    R.LINKS[2] = (R.LINKS[2][0], B.SITE + lang + "/")
    R.PRESS = [(lab, url) for lab, (_, url) in zip(b["PRESS_LABELS"], R.PRESS)]
    R.SEQUENCE = [("vis", s[1], cap(s[2])) if s[0] == "vis" else s for s in R.SEQUENCE]
    R.OUT = B.OUT / f"Rumah-Marton-Brochure-{lang.upper()}.pdf"
for u in (B.GARDEN, B.PENTHOUSE): B.build(u)
R.main()
B.web_plans()
shutil.copy(R.OUT, f"/home/claude/rm/public/downloads/rumah-marton-brochure{B.SUF}.pdf")
print("done", lang)
