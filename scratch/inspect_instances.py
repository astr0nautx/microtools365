import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Let's find all occurrences of "first-contentful-paint"
fcps = [m.start() for m in re.finditer(r'\\\"first-contentful-paint\\\":\{', s16)]
print(f"Number of FCP occurrences: {len(fcps)}")

for idx, pos in enumerate(fcps):
    chunk = s16[pos:pos+1500].replace('\\"', '"').replace('\\\\', '\\')
    print(f"\n--- FCP Instance {idx+1} (pos {pos}) ---")
    for key in ['score', 'displayValue', 'numericValue']:
        m = re.search(r'"' + key + r'":\s*([0-9.]+|"[^"]+")', chunk)
        if m:
            print(f"  {key}: {m.group(1)}")

# Let's find all occurrences of "largest-contentful-paint"
lcps = [m.start() for m in re.finditer(r'\\\"largest-contentful-paint\\\":\{', s16)]
for idx, pos in enumerate(lcps):
    chunk = s16[pos:pos+1500].replace('\\"', '"').replace('\\\\', '\\')
    print(f"\n--- LCP Instance {idx+1} ---")
    for key in ['score', 'displayValue', 'numericValue']:
        m = re.search(r'"' + key + r'":\s*([0-9.]+|"[^"]+")', chunk)
        if m:
            print(f"  {key}: {m.group(1)}")

# Let's find all render-blocking-resources
rbrs = [m.start() for m in re.finditer(r'\\\"render-blocking-resources\\\":\{', s16)]
for idx, pos in enumerate(rbrs):
    chunk = s16[pos:pos+2500].replace('\\"', '"').replace('\\\\', '\\')
    print(f"\n--- Render Blocking Instance {idx+1} ---")
    # print items
    m_items = re.search(r'"items":\s*\[(.*?)\]', chunk)
    if m_items:
        print("  Items:", m_items.group(1)[:500])

# Let's find server-response-time
srts = [m.start() for m in re.finditer(r'\\\"server-response-time\\\":\{', s16)]
for idx, pos in enumerate(srts):
    chunk = s16[pos:pos+1500].replace('\\"', '"').replace('\\\\', '\\')
    print(f"\n--- Server Response Time Instance {idx+1} ---")
    for key in ['score', 'displayValue', 'numericValue']:
        m = re.search(r'"' + key + r'":\s*([0-9.]+|"[^"]+")', chunk)
        if m:
            print(f"  {key}: {m.group(1)}")
