import settings from '../content/settings.json';
const files = import.meta.glob<{ default: any }>('../content/i18n/*.json', { eager: true });
export type Lang = { code: string; label: string; locale: string; htmlLang: string; enabled: boolean };
export const languages: Lang[] = settings.languages;
export const enabled = languages.filter((l) => l.enabled);
export function t(code: string) {
  const f = files[`../content/i18n/${code}.json`];
  if (!f) throw new Error(`Missing language file src/content/i18n/${code}.json`);
  return f.default;
}
export const site = settings.siteUrl.replace(/\/$/, '');
/** Path of a page in a language, e.g. path('hu', 'privacy') -> /hu/privacy/ */
export function path(code: string, page = '') { return `/${code}/${page ? page.replace(/^\/|\/$/g, '') + '/' : ''}`; }
export function abs(p: string) { return site + p; }
