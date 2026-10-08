import re

with open('scratch/ps_response.html', 'r', encoding='utf-8') as f:
    html = f.read()

matches = re.findall(r'<script[^>]*>(.*?)</script>', html, re.DOTALL)
s16 = matches[16]

matches_nr = [m.start() for m in re.finditer(r'network-requests', s16)]
print("Positions of network-requests:", matches_nr)
for p in matches_nr:
    print(repr(s16[p-20:p+100]))
