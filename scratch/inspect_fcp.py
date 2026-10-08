with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]
pos = s16.find('first-contentful-paint')
print(f"Position: {pos}")
print("Surrounding 300 chars:")
print(repr(s16[pos-50:pos+250]))
