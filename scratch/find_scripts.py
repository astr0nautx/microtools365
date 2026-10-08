with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
for i, m in enumerate(matches):
    if 'first-contentful-paint' in m:
        print(f"Script {i} has first-contentful-paint, len={len(m)}")
