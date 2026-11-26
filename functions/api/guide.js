// Buyer's Guide request: emails the visitor a link to the guide in the language they chose.
// Runs as a Cloudflare Pages Function at /api/guide.
// Needs two settings in Cloudflare Pages → Settings → Variables and secrets:
//   RESEND_API_KEY  (secret)  the API key from resend.com
//   GUIDE_FROM      (text)    e.g.  Rumah Márton <guide@rumahmarton.com>   (an address on the domain verified in Resend)
// Replies go to pei@wy-design.com.

const REPLY_TO = 'pei@wy-design.com';
const FILES = {
  en: '/downloads/guide/rumah-marton-buyers-guide-en-ef53243849.pdf',
  hu: '/downloads/guide/rumah-marton-vasarloi-utmutato-hu-ef53243849.pdf',
  zh: '/downloads/guide/rumah-marton-goufang-zhinan-zh-ef53243849.pdf',
};

const esc = (s) => String(s).replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const MAIL = {
  en: (name, link) => ({
    subject: 'Your Rumah Márton Buyer’s Guide',
    eyebrow: 'Buyer’s Guide', place: 'Mártonhegy · Budapest',
    lines: [
      name ? `Dear ${name},` : 'Hello,',
      'Thank you for your interest in Rumah Márton.',
      { link, label: 'Open your Buyer’s Guide', before: 'Open your guide here:' },
      'If you have any follow-up questions, or would like to talk about the next steps, simply reply to this email. We would be more than happy to talk with you further!',
    ],
    sign: ['Warmest regards,', 'Pei', 'Architect & Developer', 'rumahmarton.com'],
  }),
  hu: (name, link) => ({
    subject: 'Az Ön Rumah Márton vásárlói útmutatója',
    eyebrow: 'Vásárlói útmutató', place: 'Mártonhegy · Budapest',
    lines: [
      name ? `Kedves ${name}!` : 'Kedves Érdeklődő!',
      'Köszönjük érdeklődését a Rumah Márton iránt.',
      { link, label: 'Vásárlói útmutató megnyitása', before: 'Az útmutatót itt nyithatja meg:' },
      'Ha további kérdése van, vagy szeretne a következő lépésekről beszélni, egyszerűen válaszoljon erre az e-mailre. Nagy örömmel beszélgetünk Önnel!',
    ],
    sign: ['Üdvözlettel:', 'Pei', 'építész és fejlesztő', 'rumahmarton.com'],
  }),
  zh: (name, link) => ({
    subject: '您的玛顿山邸 Rumah Márton 购房指南',
    eyebrow: '购房指南', place: '玛顿山 · 布达佩斯', zh: true,
    lines: [
      name ? `${name} 您好：` : '您好：',
      '感谢您关注玛顿山邸 Rumah Márton。',
      { link, label: '打开购房指南', before: '请在此打开您的购房指南：' },
      '如您有任何进一步的问题，或希望垂询下一步事宜，直接回复此邮件即可。我们非常期待与您进一步交流！',
    ],
    sign: ['诚挚问候，', 'Pei', '建筑师 · 开发商', 'rumahmarton.com'],
  }),
};

// Typography follows the brochure: Newsreader (serif) and Albert Sans. Apple Mail and most phone
// mail apps load them; Gmail and Outlook fall back to Georgia and Helvetica, which keep the same feel.
const SERIF = "'Newsreader','Iowan Old Style','Palatino Linotype',Georgia,'Times New Roman',serif";
const SANS = "'Albert Sans','Helvetica Neue',Helvetica,Arial,sans-serif";
const SERIF_ZH = "'Newsreader','Songti SC','Noto Serif SC','STSong','SimSun',Georgia,serif";
const SANS_ZH = "'Albert Sans','PingFang SC','Noto Sans SC','Microsoft YaHei','Helvetica Neue',Arial,sans-serif";
const SITE = 'https://rumahmarton.com';

function render(m) {
  const serif = m.zh ? SERIF_ZH : SERIF, sans = m.zh ? SANS_ZH : SANS;
  const ls = m.zh ? '.12em' : '.28em';
  const [greet, ...rest] = m.lines;
  const para = (t, mb = 18) => `<p style="margin:0 0 ${mb}px;font-family:${sans};font-size:16px;line-height:1.75;font-weight:300;color:#2A2723">${esc(t)}</p>`;
  const body = rest.map((l, i) => typeof l === 'string' ? para(l, typeof rest[i + 1] === 'object' ? 4 : 18) :
    para(l.before) + `<table role="presentation" cellpadding="0" cellspacing="0" border="0" style="margin:6px 0 34px"><tr><td style="background:#1E1C19">`
    + `<a href="${esc(l.link)}" style="display:inline-block;padding:16px 30px;font-family:${sans};font-size:12px;font-weight:400;letter-spacing:${m.zh ? '.2em' : '.18em'};text-transform:uppercase;color:#FAF7F1;text-decoration:none">${esc(l.label)}&nbsp;&nbsp;&rarr;</a>`
    + `</td></tr></table>`).join('');
  const [bye, who, role, site] = m.sign;
  const html = `<!doctype html><html lang="${m.zh ? 'zh' : ''}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">`
    + `<meta name="color-scheme" content="light only"><meta name="supported-color-schemes" content="light">`
    + `<link href="https://fonts.googleapis.com/css2?family=Albert+Sans:wght@300;400&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&display=swap" rel="stylesheet">`
    + `<title>${esc(m.subject)}</title></head>`
    + `<body style="margin:0;padding:0;background:#F4EFE7;-webkit-font-smoothing:antialiased">`
    + `<div style="display:none;max-height:0;overflow:hidden;opacity:0">${esc(m.lines[1])}</div>`
    + `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="background:#F4EFE7"><tr><td align="center" style="padding:44px 16px 56px">`
    + `<table role="presentation" width="100%" cellpadding="0" cellspacing="0" border="0" style="max-width:560px">`
    // wordmark
    + `<tr><td align="center" style="padding:0 0 30px"><a href="${SITE}" style="text-decoration:none;color:#1E1C19;font-family:${SERIF};font-size:21px;font-weight:300;letter-spacing:.34em;text-transform:uppercase">Rumah&nbsp;Márton</a></td></tr>`
    // image
    + `<tr><td><a href="${SITE}"><img src="${SITE}/media/email-guide.jpg" width="560" alt="Rumah Márton" style="display:block;width:100%;max-width:560px;height:auto;border:0"></a></td></tr>`
    // paper panel
    + `<tr><td style="background:#FAF7F1;padding:46px 44px 44px">`
    + `<p style="margin:0 0 22px;font-family:${sans};font-size:11px;font-weight:400;letter-spacing:${ls};text-transform:uppercase;color:#8C7F70">${esc(m.eyebrow)}</p>`
    + `<p style="margin:0 0 22px;font-family:${serif};font-size:21px;line-height:1.3;font-weight:300;color:#1E1C19">${esc(greet)}</p>`
    + body
    + `<table role="presentation" width="48" cellpadding="0" cellspacing="0" border="0" style="margin:34px 0 26px"><tr><td style="border-top:1px solid #CFC5B6;font-size:0;line-height:0">&nbsp;</td></tr></table>`
    + `<p style="margin:0 0 6px;font-family:${sans};font-size:15px;font-weight:300;color:#2A2723">${esc(bye)}</p>`
    + `<p style="margin:0 0 4px;font-family:${serif};font-size:19px;font-style:${m.zh ? 'normal' : 'italic'};font-weight:300;color:#1E1C19">${esc(who)}</p>`
    + `<p style="margin:0;font-family:${sans};font-size:12px;font-weight:400;letter-spacing:${m.zh ? '.1em' : '.08em'};color:#8C7F70">${esc(role)}</p>`
    + `</td></tr>`
    // footer
    + `<tr><td align="center" style="padding:30px 0 0;font-family:${sans};font-size:11px;font-weight:400;letter-spacing:${m.zh ? '.12em' : '.2em'};text-transform:uppercase;color:#8C7F70">`
    + `${esc(m.place)}&nbsp;&nbsp;·&nbsp;&nbsp;<a href="${SITE}" style="color:#6B5846;text-decoration:none">${esc(site)}</a></td></tr>`
    + `</table></td></tr></table></body></html>`;
  const text = m.lines.map((l) => typeof l === 'string' ? l : `${l.before}\n${l.link}`).join('\n\n') + '\n\n' + m.sign.join('\n');
  return { html, text };
}

const json = (o, status = 200) => new Response(JSON.stringify(o), { status, headers: { 'Content-Type': 'application/json' } });

export async function onRequestPost({ request, env }) {
  let d;
  try { d = await request.json(); } catch { return json({ ok: false, error: 'bad_request' }, 400); }
  if (d.botcheck) return json({ ok: true });                       // honeypot: quietly ignore bots
  const email = String(d.email || '').trim();
  const name = String(d.name || '').trim().slice(0, 80);
  const lang = FILES[d.lang] ? d.lang : 'en';
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email) || email.length > 200) return json({ ok: false, error: 'email' }, 400);
  if (!env.RESEND_API_KEY || !env.GUIDE_FROM) return json({ ok: false, error: 'not_configured' }, 503);

  const link = new URL(FILES[lang], request.url).href;
  const m = MAIL[lang](name, link);
  const { html, text } = render(m);
  const r = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from: env.GUIDE_FROM, to: [email], reply_to: REPLY_TO, subject: m.subject, html, text }),
  });
  if (!r.ok) return json({ ok: false, error: 'send_failed' }, 502);
  return json({ ok: true });
}
