import { enabled, abs, path } from '../lib/i18n';
import settings from '../content/settings.json';
export function GET() {
  const pages = [''];
  const urls = pages.flatMap((p) => enabled.map((l) => {
    const alts = enabled.map((a) => `<xhtml:link rel="alternate" hreflang="${a.htmlLang}" href="${abs(path(a.code, p))}"/>`).join('')
      + `<xhtml:link rel="alternate" hreflang="x-default" href="${abs(path(settings.defaultLanguage, p))}"/>`;
    return `<url><loc>${abs(path(l.code, p))}</loc>${alts}</url>`;
  })).join('');
  return new Response(`<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">${urls}</urlset>\n`,
    { headers: { 'Content-Type': 'application/xml; charset=utf-8' } });
}
