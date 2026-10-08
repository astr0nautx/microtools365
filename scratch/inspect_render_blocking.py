import re

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

audits_chunk = s16[700000:1300000].replace('\\"', '"').replace('\\\\', '\\')

for audit_id in ['render-blocking-insight', 'render-blocking-resources', 'unused-javascript', 'network-dependency-tree-insight']:
    pos = audits_chunk.find(f'"{audit_id}":')
    if pos != -1:
        print(f"\n==================== {audit_id} ====================")
        sub = audits_chunk[pos:pos+4000]
        # find end of json object or print first 1500 chars
        print(sub[:2000])
