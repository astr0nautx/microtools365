import glob, re

files = glob.glob('microtools365/**/*.html', recursive=True)
snippets = set()

for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    m = re.search(r'(<script>\s*\(function\s*\(\)\s*\{\s*try\s*\{\s*if\s*\(localStorage\.getItem\(\'mt365-theme\'\)[^<]+</script>)', c)
    if m:
        snippets.add(m.group(1).strip())

print(f"Unique snippets found: {len(snippets)}")
for s in snippets:
    print("---")
    print(s)
