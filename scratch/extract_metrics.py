import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
script_text = matches[16]

# Look for json or data inside script_text
# In WIZ / angular / google web components, there's often something like data: '{"lighthouseResult": ...}' or similar
# Let's search for "first-contentful-paint"
pos = script_text.find('"first-contentful-paint"')
if pos != -1:
    snippet = script_text[max(0, pos-200):min(len(script_text), pos+600)]
    print("FCP snippet:")
    print(snippet)

# Let's find performance audit scores
for metric in ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index']:
    p = script_text.find(f'"{metric}":')
    if p != -1:
        print(f"\n--- {metric} ---")
        print(script_text[p:p+300])
