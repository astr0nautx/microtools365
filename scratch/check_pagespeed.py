import urllib.request, re, json

url = 'https://pagespeed.web.dev/analysis/https-microtools365-com/2vzjlwup8j?hl=en&form_factor=mobile'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
try:
    with urllib.request.urlopen(req) as resp:
        html = resp.read().decode('utf-8', errors='ignore')
    
    with open('scratch/ps_response.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved response HTML, length:", len(html))
except Exception as e:
    print('Error:', e)
