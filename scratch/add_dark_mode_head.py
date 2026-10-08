import os

files_to_update = [
    'microtools365/index.html',
    'microtools365/blog/bmi-explained/index.html',
    'microtools365/blog/emi-amortization-explained/index.html',
    'microtools365/blog/how-to-calculate-gst-india/index.html',
    'microtools365/blog/old-vs-new-tax-regime/index.html',
    'microtools365/blog/passport-photo-size-india/index.html',
    'microtools365/blog/sip-vs-lump-sum/index.html',
    'microtools365/tools/compound-interest-calculator/index.html',
    'microtools365/tools/emi-calculator/index.html',
    'microtools365/tools/ideal-weight-calculator/index.html',
    'microtools365/tools/income-tax-calculator/index.html',
    'microtools365/tools/lorem-ipsum-generator/index.html',
    'microtools365/tools/pdf-merge/index.html',
    'microtools365/tools/pregnancy-due-date-calculator/index.html',
    'microtools365/tools/sip-calculator/index.html',
    'microtools365/tools/slug-generator/index.html',
    'microtools365/tools/tip-calculator/index.html'
]

block = '''  <style>html.dark-mode { background: #14161C; color-scheme: dark; }</style>
  <script>
    (function () {
      try {
        if (localStorage.getItem('mt365-theme') === 'dark') {
          document.documentElement.classList.add('dark-mode');
        }
      } catch (e) {}
    })();
  </script>
'''

updated_count = 0
for path in files_to_update:
    norm_path = os.path.normpath(path)
    with open(norm_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Check if already present
    if "localStorage.getItem('mt365-theme')" in content.split('<body')[0]:
        print(f"Skipping {norm_path}, already has script")
        continue

    target = '<link rel="preconnect" href="https://fonts.googleapis.com">'
    if target in content:
        new_content = content.replace(target, block + '  ' + target, 1)
        with open(norm_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {norm_path}")
        updated_count += 1
    else:
        print(f"Target not found in {norm_path}!")

print(f"\nDone! Successfully updated {updated_count} files.")
