import type { ImageMetadata } from 'astro';
const files = import.meta.glob<{ default: ImageMetadata }>('../assets/images/*.{jpg,jpeg,png,webp}', { eager: true });
const byName: Record<string, ImageMetadata> = {};
for (const [path, mod] of Object.entries(files)) {
  const name = path.split('/').pop()!.replace(/\.(jpe?g|png|webp)$/i, '');
  byName[name] = mod.default;
}
/** Look up an image in src/assets/images by file name (without extension). */
export function image(name: string): ImageMetadata {
  const img = byName[name];
  if (!img) throw new Error(`Image "${name}" not found in src/assets/images`);
  return img;
}
