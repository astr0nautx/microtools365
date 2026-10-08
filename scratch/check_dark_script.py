import os, glob

html_files = glob.glob('microtools365/**/*.html', recursive=True)
print(f"Total HTML files: {len(html_files)}")

has_head_theme_script = []
missing_head_theme_script = []
has_mt_loader = []
missing_mt_loader = []

for f in html_files:
    with open(f, 'r', encoding='utf-8') as fp:
        content = fp.read()
    
    # check for theme script before <body>
    head_content = content.split('<body')[0] if '<body' in content else ''
    if 'localStorage.getItem(\'mt365-theme\')' in head_content or 'localStorage.getItem("mt365-theme")' in head_content:
        has_head_theme_script.append(f)
    else:
        missing_head_theme_script.append(f)
        
    if 'id="mt-loader"' in content:
        has_mt_loader.append(f)
    else:
        missing_mt_loader.append(f)

print(f"Files WITH head theme script: {len(has_head_theme_script)}")
print(f"Files MISSING head theme script: {len(missing_head_theme_script)}")
print("Missing head theme script:", missing_head_theme_script)
print(f"\nFiles WITH mt-loader: {len(has_mt_loader)}")
print(f"Files MISSING mt-loader: {len(missing_mt_loader)}")
