import { defineConfig } from 'astro/config';
import settings from './src/content/settings.json' assert { type: 'json' };

// PREVIEW=1 builds a lighter single-size image set for the Claude preview.
export default defineConfig({
  site: settings.siteUrl,
  output: 'static',
  build: { inlineStylesheets: 'always', assets: '_assets' },
  image: { service: { entrypoint: 'astro/assets/services/sharp' } },
  compressHTML: true,
});
