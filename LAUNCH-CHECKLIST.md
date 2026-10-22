# Before launch: what is needed, and what must be tested

Nothing below is working until it has been set up and tested on the live host.

## You supply
- [ ] Domain name, and access to its DNS settings. `siteUrl` in settings.json is a placeholder (www.rumahmarton.com).
- [ ] Company legal name and registered address for the privacy policy (`privacy.sections[0]` in each language file).
- [ ] Final check of residence areas, bedrooms and availability (en.json and settings.json). They currently come from the October 2026 brochure; Residence 02 is marked sold.
- [ ] Optional: phone number for the enquiry section (settings.json, contact.phone).
- [ ] Approval of the English copy, then the Hungarian translation for review.

## Hosting and enquiries (Netlify)
- [ ] Connect this project to Netlify (from GitHub, or drag the built `dist` folder).
- [ ] Forms: enable form detection, redeploy. Expect a form called `enquiry-en` (and `enquiry-hu` once Hungarian is on).
- [ ] Forms → Notifications → email notification to pei@wy-design.com for each form.
- [ ] Spam: the honeypot field is built in. Optionally turn on reCAPTCHA in Netlify if spam appears.
- [ ] TEST: send an enquiry with "private viewing" ticked, confirm the thank-you message on the page, the entry in Netlify Forms, and the email arriving at pei@wy-design.com (check the spam folder).
- [ ] TEST: brochure and both floor plans open in a new tab on desktop and phone.
- [ ] TEST: the Enquire link in the header works on desktop and phone.
- [ ] Domain management: add the domain, set DNS as Netlify instructs, wait for HTTPS.

## Google
- [ ] Google Search Console: add the domain, paste the verification code into `analytics.searchConsoleVerification` (or verify by DNS), submit `/sitemap.xml`.
- [ ] Google Analytics 4: create a property, paste the Measurement ID (G-…) into `analytics.ga4`.
- [ ] Google Ads: paste the account ID (AW-…) into `analytics.googleAds`, create two conversion actions and paste their labels into `googleAdsLeadLabel` and `googleAdsViewingLabel`.
- [ ] TEST in GA4 DebugView / Ads Tag Assistant: accept cookies, then check page view, brochure_click, floor_plan_click, enquiry_submit and private_viewing_request.
- [ ] TEST: decline cookies and confirm no Google or Meta requests are made.

## Social advertising (when ready)
- [ ] Meta Pixel ID into `analytics.metaPixel`; test with Meta Pixel Helper.
- [ ] Give each advert its own link with `utm_source` and `utm_campaign`.
