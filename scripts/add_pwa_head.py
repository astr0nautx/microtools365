import os

site_dir = r"x:\Antigravity-microtools365\microtools365"
needle = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
replacement = """  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <link rel="manifest" href="/manifest.json">
  <meta name="theme-color" content="#FF5A1F">
  <link rel="apple-touch-icon" href="/icon-192.png">"""

updated = 0
for root, dirs, files in os.walk(site_dir):
    for f in files:
        if f.endswith('.html'):
            path = os.path.join(root, f)
            with open(path, 'r', encoding='utf-8') as fp:
                content = fp.read()

            if '/manifest.json' not in content and needle in content:
                content = content.replace(needle, replacement, 1)
                with open(path, 'w', encoding='utf-8') as fp:
                    fp.write(content)
                updated += 1

print(f"Added PWA tags to {updated} HTML files.")
