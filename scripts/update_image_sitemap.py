import os
import re
import xml.sax.saxutils as saxutils

site_dir = r"x:\Antigravity-microtools365\microtools365"
site_url = "https://www.microtools365.com"

# Collect all HTML files
html_files = []
for root, dirs, files in os.walk(site_dir):
    for f in files:
        if f == 'index.html':
            html_files.append(os.path.join(root, f))

html_files.sort()

entries = []

for file in html_files:
    rel_path = os.path.relpath(file, site_dir).replace('\\', '/')
    sub = rel_path.replace('index.html', '')
    page_url = f"{site_url}/{sub}" if sub else f"{site_url}/"

    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Title
    m_title = re.search(r'<title>([^<]+)</title>', content)
    title = m_title.group(1).strip() if m_title else "microtools365"
    # Clean up title suffix
    title = title.split('—')[0].split('|')[0].strip()

    # Description
    m_desc = re.search(r'<meta name="description" content="([^"]+)"', content)
    desc = m_desc.group(1).strip() if m_desc else ""

    # OG Image
    m_og = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    og_img = m_og.group(1).strip() if m_og else f"{site_url}/og-image.png"

    entries.append({
        'url': page_url,
        'rel_path': rel_path,
        'title': title,
        'desc': desc,
        'og_img': og_img
    })

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
    '        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">',
    ''
]

# 1. Homepage entry: includes all primary brand assets & icons
homepage_entry = next((e for e in entries if e['url'] == f"{site_url}/"), None)
if homepage_entry:
    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{site_url}/</loc>')
    
    # logo.svg
    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{site_url}/logo.svg</image:loc>')
    xml_lines.append('      <image:title>microtools365 Brand Logo</image:title>')
    xml_lines.append('      <image:caption>Official vector logo for microtools365</image:caption>')
    xml_lines.append('    </image:image>')

    # icon-512.png
    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{site_url}/icon-512.png</image:loc>')
    xml_lines.append('      <image:title>microtools365 High-Res Icon (512x512)</image:title>')
    xml_lines.append('      <image:caption>High-resolution application icon for microtools365</image:caption>')
    xml_lines.append('    </image:image>')

    # icon-192.png
    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{site_url}/icon-192.png</image:loc>')
    xml_lines.append('      <image:title>microtools365 PWA Icon (192x192)</image:title>')
    xml_lines.append('      <image:caption>Progressive Web App icon for microtools365</image:caption>')
    xml_lines.append('    </image:image>')

    # og-image.png
    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{site_url}/og-image.png</image:loc>')
    xml_lines.append('      <image:title>microtools365 — Free Productivity Utilities</image:title>')
    xml_lines.append('      <image:caption>Free in-browser tools for finance, documents, text, and calculations</image:caption>')
    xml_lines.append('    </image:image>')
    xml_lines.append('  </url>')
    xml_lines.append('')

# 2. Entries for all tools and blog pages
for entry in entries:
    if entry['url'] == f"{site_url}/":
        continue  # Already added above

    xml_lines.append('  <url>')
    xml_lines.append(f'    <loc>{saxutils.escape(entry["url"])}</loc>')
    xml_lines.append('    <image:image>')
    xml_lines.append(f'      <image:loc>{saxutils.escape(entry["og_img"])}</image:loc>')
    xml_lines.append(f'      <image:title>{saxutils.escape(entry["title"])}</image:title>')
    if entry['desc']:
        xml_lines.append(f'      <image:caption>{saxutils.escape(entry["desc"])}</image:caption>')
    xml_lines.append('    </image:image>')
    xml_lines.append('  </url>')
    xml_lines.append('')

xml_lines.append('</urlset>')

out_path = os.path.join(site_dir, 'image-sitemap.xml')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines) + '\n')

print(f"Generated image-sitemap.xml with {len(entries)} URL entries and all brand icons/images.")
