missing = [
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

for p in missing:
    with open(p, 'r', encoding='utf-8') as f:
        content = f.read()
    has_preconnect = '<link rel="preconnect" href="https://fonts.googleapis.com">' in content
    print(f"{p}: preconnect={has_preconnect}")
