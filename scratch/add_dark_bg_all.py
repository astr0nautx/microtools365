import glob

files = glob.glob('microtools365/**/*.html', recursive=True)
updated = 0
for f in files:
    with open(f, 'r', encoding='utf-8') as fp:
        c = fp.read()
    
    head_part = c.split('<body')[0]
    if 'html.dark-mode' in head_part and 'background: #14161C' in head_part:
        continue
    
    # Check if has #mt-loader.mt-loader-dark { background: #14161C; }
    target = '#mt-loader.mt-loader-dark { background: #14161C; }'
    if target in c:
        new_c = c.replace(target, target + '\n    html.dark-mode { background: #14161C; color-scheme: dark; }', 1)
        with open(f, 'w', encoding='utf-8') as fp:
            fp.write(new_c)
        updated += 1
    else:
        print(f"Could not find target in {f}")

print(f"Updated {updated} files with html.dark-mode critical style in head.")
