# Rumah Márton website

Static site built with Astro. One page per language at /en/, /hu/ and /zh/, plus privacy and thank-you pages.

## Where things are
| What | File |
|---|---|
| Words, per language | `src/content/i18n/en.json` (hu.json and zh.json are English placeholders until translated) |
| Facts shared by all languages: contact, residences, files, images, analytics IDs, which languages are on | `src/content/settings.json` |
| Photographs used on the site | `src/assets/images/` (unused visualisations are kept in `image-library/`) |
| Film | `public/media/rumah-marton-film-1600.mp4` and `-960.mp4` |
| Brochure and floor plans | `public/downloads/` (they open in a new tab) |
| Look and layout | `src/styles/global.css` |

## Switching on a language
1. Translate `src/content/i18n/hu.json` (every value; keep the keys).
2. In `settings.json` set `"enabled": true` for `hu`.
3. To send Hungarian browsers to /hu/, ask Claude to add a language redirect (Cloudflare: a Redirect Rule or a small Pages function).
4. Rebuild. The language switch, hreflang links and sitemap update themselves.

## Commands
```
npm install
npm run dev      # http://localhost:4321/en/
npm run build    # site in /dist
```

## Tracking events
Pushed to `dataLayer` always; sent to GA4, Google Ads and Meta only after cookie consent (Consent Mode v2 defaults to denied):
- `enquiry_submit` (Google Ads conversion with `googleAdsLeadLabel`, Meta `Lead`)
- `private_viewing_request` (Ads conversion with `googleAdsViewingLabel`, Meta `Schedule`)
- `brochure_click`, `floor_plan_click`

Every enquiry also records `source` and `campaign` from ad links, e.g. `/en/?utm_source=instagram&utm_campaign=launch`.
