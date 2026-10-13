import os
import re

site_dir = r"x:\Antigravity-microtools365\microtools365"

physical_images = []
for r, d, fs in os.walk(site_dir):
    for f in fs:
        ext = os.path.splitext(f)[1].lower()
        if ext in ['.png', '.jpg', '.jpeg', '.svg', '.webp', '.ico', '.gif']:
            rel = os.path.relpath(os.path.join(r, f), site_dir).replace('\\', '/')
            physical_images.append(rel)

print("Physical images in repo:", physical_images)

img_by_page = {}
og_by_page = {}

for r, d, fs in os.walk(site_dir):
    for f in fs:
        if f.endswith('.html'):
            rel_page = os.path.relpath(os.path.join(r, f), site_dir).replace('\\', '/')
            with open(os.path.join(r, f), 'r', encoding='utf-8') as fp:
                content = fp.read()
            imgs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', content)
            if imgs:
                img_by_page[rel_page] = imgs
            m_og = re.search(r'<meta property="og:image" content="([^"]+)"', content)
            if m_og:
                og_by_page[rel_page] = m_og.group(1)

print("Pages with <img> tags:", img_by_page)
print("Pages with og:image:", len(og_by_page))
