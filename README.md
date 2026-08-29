# microtools365

Free, no-signup, multi-purpose online tools. Plain HTML/CSS/JS — no build step, no framework. Deploys to Vercel as a static site.

microtools365 is a fast, no-signup utility website built for everyday tasks. It includes dedicated calculator and text tools, a practical blog for helpful guides, and core informational pages such as About, Privacy Policy, and Terms of Use. Each tool is a standalone static page, keeping the site lightweight, easy to navigate, and simple to deploy.

## Folder structure

```
microtools365/
├── index.html                          → homepage / tool directory
├── blog/                               → articles and guides
├── about/                              → about page
├── privacy-policy/                     → privacy policy page
├── terms-of-use/                       → terms of use page
├── css/style.css                       → ALL shared styles (colors, fonts, components)
├── js/main.js                          → shared behavior (mobile nav, search filter, toast)
└── tools/
    ├── word-counter/index.html         → live word/character counter
    ├── percentage-calculator/index.html→ 3-mode percentage calculator
    ├── gst-calculator/index.html       → GST calculator
    ├── emi-calculator/index.html       → EMI calculator
    ├── sip-calculator/index.html       → SIP calculator
    ├── compound-interest-calculator/index.html → compound interest calculator
    ├── income-tax-calculator/index.html → income tax calculator
    ├── in-hand-salary-calculator/index.html → in-hand salary calculator
    ├── fd-calculator/index.html        → FD calculator
    ├── hra-calculator/index.html       → HRA exemption calculator
    ├── case-converter/index.html       → case converter
    ├── text-diff-checker/index.html    → text diff checker
    ├── lorem-ipsum-generator/index.html → lorem ipsum generator
    ├── slug-generator/index.html       → slug generator
    ├── ideal-weight-calculator/index.html → ideal weight calculator
    └── random-name-picker/index.html   → random name picker
```

Each tool lives in its own folder as `tools/<tool-name>/index.html`. That gives it a clean URL
once deployed: `microtools365.com/tools/word-counter/`. The tool's own logic (the `<script>`
at the bottom of its HTML file) is self-contained, so you can open any tool file as a template
for the next one.

## Adding a new tool (the pattern)

1. Duplicate the `tools/percentage-calculator/` folder, rename it to your new tool's slug
   (e.g. `tools/age-calculator/`).
2. Edit the `<title>`, `<meta description>`, breadcrumb, `<h1>` and `<span class="catalog-tag">`.
3. Replace the `.panel` contents and the inline `<script>` with your tool's actual logic.
4. Add a card for it on `index.html` inside `.tool-grid`, and a link in the header `<nav>` on
   every page (homepage + every tool page).
5. Commit, push, done — Vercel redeploys automatically.

## Design tokens (in `css/style.css`)

- `--accent` (#FF5A1F) — the one accent color, used for buttons, links, and the catalog tags
- `--font-display` (Space Grotesk) — headings / logo
- `--font-body` (Inter) — body text
- `--font-mono` (JetBrains Mono) — numbers, calculator output, the catalog codes

Reuse the existing classes (`.panel`, `.field`, `.btn`, `.readout`, `.result-box`, `.tabs`)
instead of writing new CSS per tool — that's what keeps every tool feeling like part of the
same site.
