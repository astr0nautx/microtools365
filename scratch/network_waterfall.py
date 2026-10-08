import re, json

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

# Let's search for "network-requests" in instance 2 (after pos 700000)
pos2 = s16.find(r'\\\"network-requests\\\":', 700000)
if pos2 != -1:
    chunk = s16[pos2:pos2+12000].replace('\\"', '"').replace('\\\\', '\\')
    # parse the items array
    m_items = re.search(r'"items":\s*(\[\{.*?\}\])', chunk)
    if m_items:
        items_str = m_items.group(1)
        try:
            items = json.loads(items_str)
            print(f"Total requests in Instance 2: {len(items)}")
            for req in items:
                print(f"URL: {req.get('url')}")
                print(f"  rendererStartTime: {req.get('rendererStartTime')}")
                print(f"  responseReceivedTime: {req.get('responseReceivedTime')}")
                print(f"  endTime: {req.get('endTime')}")
                print(f"  transferSize: {req.get('transferSize')}")
        except Exception as e:
            print("Failed to parse items json:", e)
            # regex extract
            urls = re.findall(r'"url":\s*"([^"]+)",.*?"rendererStartTime":\s*([0-9.]+),.*?"responseReceivedTime":\s*([0-9.]+),.*?"endTime":\s*([0-9.]+)', chunk)
            for u, st, rt, et in urls:
                print(f"{u}\n  start={st}, resp={rt}, end={et}")
