import os
import glob
import re

site_dir = r"x:\Antigravity-microtools365\microtools365"

TARGET_CSS_FONTS_REGEX = re.compile(
    r'[ \t]*<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*'
    r'<link rel="preconnect" href="https://fonts\.gstatic\.com"[^>]*>\s*'
    r'(?:<link rel="preload"[^>]+>\s*)?'
    r'<link [^>]+fonts\.googleapis\.com/css2[^>]+>\s*'
    r'(?:<noscript>.*?</noscript>\s*)?'
    r'<link rel="stylesheet" href="(?:\.\./)*css/style\.css">',
    re.DOTALL
)

REPLACEMENT_CSS_FONTS = """  <link rel="preload" href="/css/style.css?v=2.1" as="style">
  <link rel="stylesheet" href="/css/style.css?v=2.1">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" media="print" onload="this.onload=null;this.media='all'">
  <noscript>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap">
  </noscript>"""

OLD_GTAG_REGEX = re.compile(
    r'[ \t]*\(function\(\) \{\s*'
    r'function loadGtag\(\) \{\s*'
    r'if \(window\._gtagLoaded\) return;\s*'
    r'window\._gtagLoaded = true;\s*'
    r'var s = document\.createElement\(\'script\'\);\s*'
    r's\.async = true;\s*'
    r's\.src = \'https://www\.googletagmanager\.com/gtag/js\?id=G-19PMSNFG2R\';\s*'
    r'document\.head\.appendChild\(s\);\s*'
    r'\}\s*'
    r'if \(\'requestIdleCallback\' in window\) \{\s*'
    r'window\.addEventListener\(\'load\', function\(\) \{ requestIdleCallback\(loadGtag\); \}\);\s*'
    r'\} else \{\s*'
    r'window\.addEventListener\(\'load\', function\(\) \{ setTimeout\(loadGtag, 1000\); \}\);\s*'
    r'\}\s*'
    r'\}\)\(\);',
    re.DOTALL
)

NEW_GTAG = """    (function() {
      function loadGtag() {
        if (window._gtagLoaded) return;
        window._gtagLoaded = true;
        ['pointerdown', 'touchstart', 'scroll', 'keydown'].forEach(function(ev) {
          window.removeEventListener(ev, loadGtag, { passive: true });
        });
        var s = document.createElement('script');
        s.async = true;
        s.src = 'https://www.googletagmanager.com/gtag/js?id=G-19PMSNFG2R';
        document.head.appendChild(s);
      }
      ['pointerdown', 'touchstart', 'scroll', 'keydown'].forEach(function(ev) {
        window.addEventListener(ev, loadGtag, { once: true, passive: true });
      });
      setTimeout(loadGtag, 4000);
    })();"""

paths = glob.glob(os.path.join(site_dir, '**', '*.html'), recursive=True)
updated_count = 0

for p in paths:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content
    content = TARGET_CSS_FONTS_REGEX.sub(REPLACEMENT_CSS_FONTS, content, count=1)
    content = OLD_GTAG_REGEX.sub(NEW_GTAG, content, count=1)
    content = re.sub(r'href="/css/style\.css(?:\?[^"]*)?"', 'href="/css/style.css?v=2.1"', content)
    content = re.sub(r'<script[^>]+main\.js[^>]*>(?:</script>)?', '<script src="/js/main.js?v=2.1" defer></script>', content)

    if content != orig_content:
        with open(p, 'w', encoding='utf-8') as f:
            f.write(content)
        updated_count += 1

print(f"Updated {updated_count} files with cache-busted CSS/JS and lazy-loaded Gtag.")
