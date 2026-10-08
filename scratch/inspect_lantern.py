with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re, json
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Search for "lantern" or "simulator" or "optimistic" or "pessimistic"
pos_fcp2 = s16.find(r'3445.182')
if pos_fcp2 != -1:
    print("Found pos_fcp2:", pos_fcp2)
    chunk = s16[pos_fcp2-500:pos_fcp2+1500].replace('\\"', '"').replace('\\\\', '\\')
    print(chunk)
