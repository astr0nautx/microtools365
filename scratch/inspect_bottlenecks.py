import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Find render-blocking-resources in instance 2 (after pos 700000)
pos2 = s16.find(r'\\\"render-blocking-resources\\\":', 700000)
if pos2 != -1:
    chunk = s16[pos2:pos2+3000].replace('\\"', '"').replace('\\\\', '\\')
    print("--- Render Blocking in Instance 2 ---")
    print(chunk[:1000])

# Find network-requests in instance 2
pos_net = s16.find(r'\\\"network-requests\\\":', 700000)
if pos_net != -1:
    chunk = s16[pos_net:pos_net+5000].replace('\\"', '"').replace('\\\\', '\\')
    # print the urls and response times
    print("\n--- Network Requests in Instance 2 ---")
    reqs = re.findall(r'\{"url":\s*"([^"]+)",.*?"transferSize":\s*([0-9]+),.*?"totalBytes":\s*([0-9]+)', chunk)
    for u, ts, tb in reqs[:20]:
        print(f"  {u} (transferSize: {ts})")

# Let's find diagnostics or opportunities in instance 2
# Search for audits with score < 1
audits_chunk = s16[700000:1200000].replace('\\"', '"').replace('\\\\', '\\')
bad_audits = re.findall(r'"([a-z-]+)":\{"id":"([a-z-]+)",\s*"title":"([^"]+)",[^}]*?"score":([0-9.]+)', audits_chunk)
print("\n--- Audits with score < 1 in Instance 2 ---")
for id_, id2, title, score in bad_audits:
    if float(score) < 0.95:
        print(f"  {id_}: score={score} ({title})")
