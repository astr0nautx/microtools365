import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Look for the JSON payload in s16
# Google WIZ format usually puts it in an array or object
# Let's see if we can find the start of the lighthouseResult or extract audits
# Let's search for the performance score and category scores
scores = re.findall(r'\\\"([a-z-]+)\\\":\{\\\"id\\\":\\\"([a-z-]+)\\\",\s*\\\"title\\\":\\\"([^\\]+)\\\",\s*\\\"score\\\":([0-9.]+)', s16)
print("Audits with numeric scores:")
for k, id_, title, score in scores[:25]:
    print(f"  {id_}: {score} ({title})")

# Specifically check categories
cat_matches = re.findall(r'\\\"categories\\\":\{([^\}]+)\}', s16)
print("Categories match found:", len(cat_matches))

# Let's extract displayValues of metrics
metrics = ['first-contentful-paint', 'largest-contentful-paint', 'total-blocking-time', 'cumulative-layout-shift', 'speed-index', 'server-response-time', 'interactive', 'render-blocking-resources']
for m in metrics:
    m_match = re.search(r'\\\"' + m + r'\\\":\{([^\}]+)\}', s16)
    if m_match:
        content = m_match.group(1).replace('\\"', '"')
        print(f"\nMetric: {m}")
        # print score and displayValue
        s_val = re.search(r'"score":\s*([0-9.]+|null)', content)
        d_val = re.search(r'"displayValue":\s*"([^"]+)"', content)
        num_val = re.search(r'"numericValue":\s*([0-9.]+)', content)
        print(f"  score: {s_val.group(1) if s_val else 'N/A'}")
        print(f"  displayValue: {d_val.group(1) if d_val else 'N/A'}")
        print(f"  numericValue: {num_val.group(1) if num_val else 'N/A'}")
