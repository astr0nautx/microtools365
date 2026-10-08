import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Let's search for JSON data in the HTML
# Typically pagespeed.web.dev embeds the lighthouse result or WIZ data
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
found_json = None
for idx, s in enumerate(matches):
    if 'first-contentful-paint' in s or 'FIRST_CONTENTFUL_PAINT' in s:
        print(f"Match in script {idx}, length: {len(s)}")
        # Check if WIZ_global_data or similar
        m_data = re.search(r'data:\s*(\{.*\})', s)
        if m_data:
            print("Found data object")
        # Let's search for performance score
        scores = re.findall(r'"performance":\{"score":([0-9.]+)', s)
        if scores:
            print("Performance scores found:", scores)

# Let's search for opportunities or diagnostics
diag_keywords = [
    'render-blocking-resources',
    'unused-css-rules',
    'server-response-time',
    'font-display',
    'largest-contentful-paint-element',
    'critical-request-chains'
]

for kw in diag_keywords:
    pos = html.find(kw)
    if pos != -1:
        snippet = html[max(0, pos-100):min(len(html), pos+300)]
        print(f"\n--- Keyword: {kw} ---")
        print(snippet.replace('\n', ' '))
