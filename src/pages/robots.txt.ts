import { abs } from '../lib/i18n';
export function GET() {
  return new Response(`User-agent: *\nAllow: /\nDisallow: /*/thank-you/\n\nSitemap: ${abs('/sitemap.xml')}\n`, { headers: { 'Content-Type': 'text/plain' } });
}
