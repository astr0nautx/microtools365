import glob

files = glob.glob('microtools365/**/*.html', recursive=True)
has_dark_bg_style = []
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    if 'html.dark-mode' in c.split('<body')[0] and 'background' in c.split('<body')[0]:
        has_dark_bg_style.append(f)

print(f"Files with html.dark-mode background in head: {len(has_dark_bg_style)} / {len(files)}")
