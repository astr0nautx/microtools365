import os
import re

site_dir = r"x:\Antigravity-microtools365\microtools365"

NAV_TEMPLATE_DEFAULT = """      <nav class="nav">
        <a href="/">All tools</a>
        <a href="/blog/">Blog</a>

        <div class="nav-item">
          <button class="nav-dropdown-toggle">Finance <span class="caret">▾</span></button>
          <div class="nav-dropdown-menu">
            <a href="/tools/percentage-calculator/">Percentage Calculator</a>
            <a href="/tools/gst-calculator/">GST Calculator</a>
            <a href="/tools/emi-calculator/">EMI Calculator</a>
            <a href="/tools/sip-calculator/">SIP Calculator</a>
            <a href="/tools/income-tax-calculator/">Income Tax Calculator</a>
            <a href="/tools/compound-interest-calculator/">Compound Interest</a>
            <a href="/tools/in-hand-salary-calculator/">In-Hand Salary</a>
            <a href="/tools/fd-calculator/">FD Calculator</a>
            <a href="/tools/hra-calculator/">HRA Exemption</a>
            <a href="/tools/discount-calculator/">Discount Calculator</a>
            <a href="/tools/simple-interest-calculator/">Simple Interest</a>
            <a href="/tools/ppf-calculator/">PPF Calculator</a>
            <a href="/tools/gratuity-calculator/">Gratuity Calculator</a>
            <a href="/tools/retirement-calculator/">Retirement Calculator</a>
          </div>
        </div>

        <div class="nav-item">
          <button class="nav-dropdown-toggle">Text <span class="caret">▾</span></button>
          <div class="nav-dropdown-menu">
            <a href="/tools/word-counter/">Word Counter</a>
            <a href="/tools/case-converter/">Case Converter</a>
            <a href="/tools/text-diff-checker/">Text Diff Checker</a>
            <a href="/tools/lorem-ipsum-generator/">Lorem Ipsum Generator</a>
            <a href="/tools/slug-generator/">Slug Generator</a>
            <a href="/tools/json-formatter/">JSON Formatter</a>
          </div>
        </div>

        <div class="nav-item">
          <button class="nav-dropdown-toggle">Personal <span class="caret">▾</span></button>
          <div class="nav-dropdown-menu">
            <a href="/tools/age-calculator/">Age Calculator</a>
            <a href="/tools/bmi-calculator/">BMI Calculator</a>
            <a href="/tools/calorie-calculator/">BMR &amp; Calorie Calculator</a>
            <a href="/tools/ideal-weight-calculator/">Ideal Weight Calculator</a>
            <a href="/tools/pregnancy-due-date-calculator/">Pregnancy Due Date</a>
            <a href="/tools/days-between-dates/">Days Between Two Dates</a>
          </div>
        </div>

        <div class="nav-item">
          <button class="nav-dropdown-toggle">Documents <span class="caret">▾</span></button>
          <div class="nav-dropdown-menu">
            <a href="/tools/image-to-pdf/">Image to PDF</a>
            <a href="/tools/text-to-pdf/">Text to PDF</a>
            <a href="/tools/xls-to-pdf/">Excel to PDF</a>
            <a href="/tools/image-editor/">Image Editor</a>
            <a href="/tools/pdf-merge/">Merge PDF</a>
            <a href="/tools/pdf-split/">Split PDF</a>
            <a href="/tools/rent-receipt-generator/">Rent Receipt Generator</a>
            <a href="/tools/watermark-pdf/">Watermark PDF</a>
            <a href="/tools/pdf-editor/">PDF Editor</a>
          </div>
        </div>

        <div class="nav-item">
          <button class="nav-dropdown-toggle">Generators <span class="caret">▾</span></button>
          <div class="nav-dropdown-menu">
            <a href="/tools/random-name-picker/">Name Picker</a>
            <a href="/tools/password-generator/">Password Generator</a>
            <a href="/tools/qr-code-generator/">QR Code Generator</a>
            <a href="/tools/tip-calculator/">Tip Calculator</a>
            <a href="/tools/uuid-generator/">UUID Generator</a>
          </div>
        </div>
      </nav>"""

NAV_TEMPLATE_HOME = NAV_TEMPLATE_DEFAULT.replace('<a href="/">All tools</a>', '<a href="/" class="active">All tools</a>')
NAV_TEMPLATE_BLOG_INDEX = NAV_TEMPLATE_DEFAULT.replace('<a href="/blog/">Blog</a>', '<a href="/blog/" class="active">Blog</a>')

FOOTER_LINKS_TEMPLATE = """      <div class="footer-links">
        <a href="/about/">About</a>
        <a href="/request-tool/">Request a Tool</a>
        <a href="/privacy-policy/">Privacy Policy</a>
        <a href="/terms-of-use/">Terms of Use</a>
        <a href="/blog/">Blog</a>
      </div>"""

def process_file(file_path):
    rel_path = os.path.relpath(file_path, site_dir).replace('\\', '/')
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    orig_content = content

    if rel_path == 'index.html':
        target_nav = NAV_TEMPLATE_HOME
    elif rel_path == 'blog/index.html':
        target_nav = NAV_TEMPLATE_BLOG_INDEX
    else:
        target_nav = NAV_TEMPLATE_DEFAULT

    content = re.sub(r'[ \t]*<nav class=["\']nav["\']>.*?</nav>', target_nav, content, flags=re.DOTALL)
    content = re.sub(r'[ \t]*<div class=["\']footer-links["\']>.*?</div>', FOOTER_LINKS_TEMPLATE, content, flags=re.DOTALL)

    if content != orig_content:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False

html_files = []
for root, dirs, files in os.walk(site_dir):
    for f in files:
        if f.endswith('.html'):
            html_files.append(os.path.join(root, f))

updated = 0
for file in html_files:
    if process_file(file):
        updated += 1

print(f"Updated navigation with GEN 05 in {updated} files.")
