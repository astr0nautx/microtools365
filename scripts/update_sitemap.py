import os

site_root = r"x:\Antigravity-microtools365\microtools365"
site_url = "https://www.microtools365.com"

index_files = []
for root, dirs, files in os.walk(site_root):
    for f in files:
        if f == 'index.html':
            index_files.append(os.path.join(root, f))

urls = []
for file in index_files:
    rel = os.path.relpath(file, site_root).replace('\\', '/').replace('index.html', '')
    url = f"{site_url}/{rel}" if rel else f"{site_url}/"
    urls.append(url)

urls.sort()

xml_lines = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
]
for u in urls:
    xml_lines.append(f'  <url><loc>{u}</loc></url>')
xml_lines.append('</urlset>\n')

sitemap_path = os.path.join(site_root, 'sitemap.xml')
with open(sitemap_path, 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml_lines))

print(f"Generated sitemap.xml with {len(urls)} URLs.")
