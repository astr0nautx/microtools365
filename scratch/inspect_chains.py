import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Look for audits around FCP in instance 2
# Let's inspect audits: 'render-blocking-resources', 'critical-request-chains', 'diagnostics', 'mainthread-work-breakdown'
audits_chunk = s16[700000:1300000].replace('\\"', '"').replace('\\\\', '\\')

for a in ['critical-request-chains', 'diagnostics', 'mainthread-work-breakdown', 'long-tasks', 'bootup-time']:
    p = audits_chunk.find(f'"{a}":')
    if p != -1:
        print(f"\n--- {a} ---")
        print(audits_chunk[p:p+1200])
