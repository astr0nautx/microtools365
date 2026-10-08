with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

import re, json
matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

chunk = s16[837606:837606+15000].replace('\\"', '"').replace('\\\\', '\\')
# Find items in network-requests
m = re.search(r'"items":\s*(\[\{.*?\}\])', chunk)
if m:
    try:
        items = json.loads(m.group(1))
        print("Total items:", len(items))
        for it in items:
            print(f"URL: {it.get('url')}")
            print(f"  protocol: {it.get('protocol')}, mimeType: {it.get('mimeType')}")
            print(f"  transferSize: {it.get('transferSize')} B")
            print(f"  rendererStartTime: {it.get('rendererStartTime')}")
            print(f"  responseReceivedTime: {it.get('responseReceivedTime')}")
            print(f"  networkEndTime: {it.get('networkEndTime')}")
    except Exception as e:
        print("Error:", e)
        print(chunk[:1000])
else:
    print("Items not matched")
