import os
import re
from collections import defaultdict

site_dir = r"x:\Antigravity-microtools365\microtools365"
html_files = []
for root, dirs, files in os.walk(site_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

print(f"Total HTML files: {len(html_files)}")

missing_og_image = []
missing_canonical = []
missing_desc = []
missing_schema = []
index_html_links = defaultdict(list)
broken_internal_links = []
canonical_mismatches = []
title_tags = {}
canonical_tags = {}

for file in html_files:
    rel_path = os.path.relpath(file, site_dir).replace('\\', '/')
    with open(file, 'r', encoding='utf-8') as f:
        html = f.read()

    # Title
    m_title = re.search(r'<title>([^<]+)</title>', html)
    if m_title:
        t_val = m_title.group(1).strip()
        if t_val in title_tags:
            title_tags[t_val].append(rel_path)
        else:
            title_tags[t_val] = [rel_path]
    else:
        print(f"Missing title: {rel_path}")

    # Canonical
    m_canon = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    if m_canon:
        c_val = m_canon.group(1).strip()
        if c_val in canonical_tags:
            canonical_tags[c_val].append(rel_path)
        else:
            canonical_tags[c_val] = [rel_path]

        # Check if canonical matches expected path
        expected_sub = rel_path.replace('index.html', '')
        expected_url = f"https://www.microtools365.com/{expected_sub}"
        if c_val != expected_url:
            canonical_mismatches.append((rel_path, c_val, expected_url))
    else:
        missing_canonical.append(rel_path)

    if 'og:image' not in html:
        missing_og_image.append(rel_path)
    if '<meta name="description"' not in html:
        missing_desc.append(rel_path)
    if 'application/ld+json' not in html:
        missing_schema.append(rel_path)

    # find internal links
    hrefs = re.findall(r'href=["\']([^"\'#:]+)["\']', html)
    for h in hrefs:
        if 'index.html' in h:
            index_html_links[rel_path].append(h)
        # Check link resolution
        # resolve relative to current file's directory
        cur_dir = os.path.dirname(file)
        if h.startswith('/'):
            target_file = os.path.normpath(os.path.join(site_dir, h.lstrip('/')))
        else:
            target_file = os.path.normpath(os.path.join(cur_dir, h))
        
        # If target is directory, look for index.html
        if os.path.isdir(target_file):
            target_file = os.path.join(target_file, 'index.html')
        elif not os.path.exists(target_file) and os.path.exists(target_file + '/index.html'):
            target_file = target_file + '/index.html'

        if not os.path.exists(target_file):
            broken_internal_links.append((rel_path, h, target_file))

print(f"Duplicate titles: {[k for k, v in title_tags.items() if len(v) > 1]}")
print(f"Duplicate canonicals: {[k for k, v in canonical_tags.items() if len(v) > 1]}")
print(f"Canonical mismatches: {canonical_mismatches}")
print(f"Missing canonical: {missing_canonical}")
print(f"Missing description: {missing_desc}")
print(f"Missing og:image: {len(missing_og_image)} files")
print(f"Missing schema: {missing_schema}")
print(f"Broken internal links: {broken_internal_links}")
print(f"Files with href linking to index.html: {len(index_html_links)}")
sample_file = list(index_html_links.keys())[0] if index_html_links else None
if sample_file:
    print(f"Sample index.html links in {sample_file}: {index_html_links[sample_file][:5]}")
