#!/usr/bin/env node
/**
 * Regenerates microtools365/sitemap.xml from the static site's index.html files.
 * Run from the repository root: node scripts/generate-sitemap.mjs
 */
import { readdir, writeFile } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';

const siteRoot = join(process.cwd(), 'microtools365');
const siteUrl = 'https://www.microtools365.com';

async function findIndexFiles(directory) {
  const entries = await readdir(directory, { withFileTypes: true });
  const matches = [];

  for (const entry of entries) {
    if (entry.name.startsWith('.') || entry.name === 'node_modules') continue;
    const fullPath = join(directory, entry.name);
    if (entry.isDirectory()) matches.push(...await findIndexFiles(fullPath));
    if (entry.isFile() && entry.name === 'index.html') matches.push(fullPath);
  }

  return matches;
}

const files = await findIndexFiles(siteRoot);
const urls = files
  .map(file => relative(siteRoot, file).split(sep).join('/').replace(/index\.html$/, ''))
  .map(path => path ? `${siteUrl}/${path}` : `${siteUrl}/`)
  .sort((a, b) => a.localeCompare(b));

const xml = [
  '<?xml version="1.0" encoding="UTF-8"?>',
  '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
  ...urls.map(url => `  <url><loc>${url}</loc></url>`),
  '</urlset>',
  ''
].join('\n');

await writeFile(join(siteRoot, 'sitemap.xml'), xml, 'utf8');
console.log(`Generated sitemap with ${urls.length} URLs.`);
