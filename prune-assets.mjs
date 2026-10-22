// After build: remove image files Astro copied into dist/_assets that no page refers to (the untouched originals).
import { readdirSync, readFileSync, statSync, unlinkSync } from 'node:fs';
import { join } from 'node:path';
const dir = process.argv[2] || 'dist';
const html = []; const walk = (d) => { for (const f of readdirSync(d)) { const p = join(d, f); statSync(p).isDirectory() ? walk(p) : /\.(html|css|js|xml)$/.test(f) && html.push(readFileSync(p, 'utf8')); } };
walk(dir); const all = html.join('\n'); let n = 0, bytes = 0;
for (const f of readdirSync(join(dir, '_assets'))) if (!/\.(js|css)$/.test(f) && !all.includes(f)) { const p = join(dir, '_assets', f); bytes += statSync(p).size; unlinkSync(p); n++; }
console.log(`pruned ${n} unused files, ${(bytes / 1048576).toFixed(1)} MB`);
