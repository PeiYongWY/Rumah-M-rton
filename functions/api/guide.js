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
    lines: [
      name ? `Dear ${name},` : 'Hello,',
      'Thank you for your interest in Rumah Márton.',
      { link, label: 'Open your Buyer’s Guide', before: 'Open your guide here:' },
      'If you have any follow-up questions, or would like to talk about the next steps, simply reply to this email. We would be more than happy to talk with you further!',
    ],
    sign: ['Warm regards,', 'Pei', 'Architect & Developer', 'rumahmarton.com'],
  }),
  hu: (name, link) => ({
    subject: 'Az Ön Rumah Márton vásárlói útmutatója',
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
    lines: [
      name ? `${name} 您好：` : '您好：',
      '感谢您关注玛顿山邸 Rumah Márton。',
      { link, label: '打开购房指南', before: '请在此打开您的购房指南：' },
      '如您有任何进一步的问题，或希望垂询下一步事宜，直接回复此邮件即可。我们非常期待与您进一步交流！',
    ],
    sign: ['诚挚问候，', 'Pei', '建筑师 · 开发商', 'rumahmarton.com'],
  }),
};

function render(m) {
  const p = (t) => `<p style="margin:0 0 16px">${t}</p>`;
  const body = m.lines.map((l) => typeof l === 'string' ? p(esc(l)) :
    p(esc(l.before)) + `<p style="margin:0 0 24px"><a href="${esc(l.link)}" style="display:inline-block;padding:13px 22px;background:#1E1C19;color:#FAF7F1;text-decoration:none;font-size:13px;letter-spacing:.14em;text-transform:uppercase">${esc(l.label)} →</a></p>`).join('');
  const sign = `<p style="margin:24px 0 0">${m.sign.map((s, i) => i === m.sign.length - 1 ? `<a href="https://rumahmarton.com" style="color:#6B5846">${esc(s)}</a>` : esc(s)).join('<br>')}</p>`;
  const html = `<!doctype html><html><body style="margin:0;background:#F4EFE7"><div style="max-width:560px;margin:0 auto;padding:40px 28px;font-family:Helvetica,Arial,sans-serif;font-size:16px;line-height:1.6;color:#1E1C19">`
    + `<p style="margin:0 0 32px;font-family:Georgia,serif;letter-spacing:.24em;text-transform:uppercase;font-size:14px">Rumah Márton</p>${body}${sign}</div></body></html>`;
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
