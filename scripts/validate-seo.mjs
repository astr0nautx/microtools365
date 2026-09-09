#!/usr/bin/env node
/**
 * Validates required SEO metadata across all static pages.
 * Run from the repository root: node scripts/validate-seo.mjs
 */
import { readFile, readdir } from 'node:fs/promises';
import { join, relative, sep } from 'node:path';

const siteRoot = join(process.cwd(), 'microtools365');

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

const pages = await findIndexFiles(siteRoot);
const titles = new Map();
const canonicals = new Map();
const problems = [];

for (const file of pages) {
  const html = await readFile(file, 'utf8');
  const label = relative(siteRoot, file).split(sep).join('/');
  const title = html.match(/<title>([^<]+)<\/title>/)?.[1];
  const canonical = html.match(/<link rel="canonical" href="([^"]+)"/)?.[1];

  for (const [name, present] of [
    ['title', Boolean(title)],
    ['meta description', /<meta name="description" content="[^"]+"/.test(html)],
    ['canonical URL', Boolean(canonical)],
    ['Open Graph title', /<meta property="og:title" content="[^"]+"/.test(html)],
    ['Twitter card', /<meta name="twitter:card" content="[^"]+"/.test(html)],
    ['structured data', /<script type="application\/ld\+json">/.test(html)]
  ]) {
    if (!present) problems.push(`${label}: missing ${name}`);
  }

  if (title) titles.set(title, [...(titles.get(title) || []), label]);
  if (canonical) canonicals.set(canonical, [...(canonicals.get(canonical) || []), label]);
}

for (const [title, files] of titles) {
  if (files.length > 1) problems.push(`Duplicate title "${title}": ${files.join(', ')}`);
}
for (const [url, files] of canonicals) {
  if (files.length > 1) problems.push(`Duplicate canonical "${url}": ${files.join(', ')}`);
}

if (problems.length) {
  console.error(problems.join('\n'));
  process.exitCode = 1;
} else {
  console.log(`SEO validation passed for ${pages.length} pages.`);
}
