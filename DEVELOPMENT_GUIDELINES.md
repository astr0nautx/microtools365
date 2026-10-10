# microtools365 — Development & Architectural Guidelines

This document defines the permanent engineering, performance, SEO, accessibility, and architectural standards for [microtools365.com](https://www.microtools365.com/). All future pages, tools, blog articles, and updates must follow these rules.

---

## 1. Zero-Build & Deployment Rules
- **No Build Tools**: Strictly plain HTML, CSS, and vanilla JS.
- **NEVER create a `package.json`** anywhere in this repository. Vercel auto-detects `package.json` as a Node.js project and breaks the static site deployment.
- **100% Client-Side Processing**: Every calculator, document processor (PDF, Excel, images), formatter, and generator runs in browser memory. Never send user files or personal data to any server.

---

## 2. Mobile Performance & Core Web Vitals (Target: 95+ Score)
Every HTML page must adhere to these performance practices:

### ① Critical CSS & Google Fonts Priority
- Always prioritize the core stylesheet before external font links:
  ```html
  <link rel="preload" href="/css/style.css" as="style">
  <link rel="stylesheet" href="/css/style.css">
  ```
- **Never use `@import url(...)` in CSS files.**
- In `<head>`, always include DNS preconnects and the non-blocking font pattern:
  ```html
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" media="print" onload="this.onload=null;this.media='all'">
  <noscript>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap">
  </noscript>
  ```

### ② `<head>` Tag Order
Place `<meta charset="UTF-8">` and `<meta name="viewport" ...>` on lines 1 & 2 of `<head>` before any external stylesheets or analytics scripts:
```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>...</title>
  ...
  <link rel="preload" href="/css/style.css" as="style">
  <link rel="stylesheet" href="/css/style.css">
  ...
```

### ③ Script Loading & Telemetry
- Always add `defer` to the shared script:
  ```html
  <script src="../../js/main.js" defer></script>
  ```
- Lazy-load Google Analytics (`gtag.js`) on first user interaction (`pointerdown`, `touchstart`, `scroll`, `keydown`) with a 4-second idle fallback to keep TBT at 0ms and avoid forced reflows during initial paint.

### ④ Semantic `<main>` Landmark & Touch Targets (Accessibility 100%)
- Always wrap the core page content between `<header>` and `<footer>` inside `<main id="main-content"> ... </main>`.
- Interactive buttons and mobile nav toggles must meet the minimum touch target standard (min-height ≥ 24px–28px with comfortable padding).

---

## 3. URL, SEO & Metadata Standards
- **Clean Trailing Slashes**: Always link to root-relative paths with trailing slashes (e.g. `/tools/watermark-pdf/`, `/blog/`, `/`). **Never link to `/index.html`**.
- **Canonical Tags**: Every page must have a self-referencing canonical URL:
  ```html
  <link rel="canonical" href="https://www.microtools365.com/path/">
  ```
- **Social Sharing (Open Graph & Twitter)**: Every page must specify `og:title`, `og:description`, `og:url`, `og:type`, and a category-specific social card:
  - Default: `https://www.microtools365.com/og-image.png`
  - Finance tools: `https://www.microtools365.com/og-finance.png`
  - Document tools: `https://www.microtools365.com/og-documents.png`
  - Text tools: `https://www.microtools365.com/og-text.png`
  - Personal/Health: `https://www.microtools365.com/og-personal.png`
  - Generators: `https://www.microtools365.com/og-generators.png`
  - Blog posts: `https://www.microtools365.com/og-blog.png`
- **Structured Data**: Use valid JSON-LD (`WebApplication` for tools, `BlogPosting` for blog posts, `WebPage` for info pages).

---

## 4. Blog Post Structure
- **Target audience**: Practical explainers tailored for real-world use in India (tax regimes, KYC verification, rent receipts, retirement math).
- **Breadcrumb**: `<p class="breadcrumb"><a href="/">Home</a> / <a href="/blog/">Blog</a> / Post Title</p>`
- **Catalog tag**: E.g. `<span class="catalog-tag">DOC 08</span>`
- **CTA box**: Always end with a branded box linking directly to the corresponding tool:
  ```html
  <div class="cta-box">
    <p>...</p>
    <a href="/tools/tool-slug/" class="btn btn-primary">Try the Tool →</a>
  </div>
  ```
- **Comments**: Include the Cusdis comment section container before `</article>`:
  ```html
  <section class="comments-section" style="margin-top: 48px; padding-top: 32px; border-top: 1px solid var(--border);">
    <h3 style="margin: 0 0 16px; font-size: 1.25rem;">Comments &amp; Discussion</h3>
    <div id="cusdis_thread"
      data-host="https://cusdis.com"
      data-app-id="YOUR_CUSDIS_APP_ID"
      data-page-id="slug"
      data-page-url="https://www.microtools365.com/blog/slug/"
      data-page-title="Title"
      data-theme="auto"
    ></div>
    <script async defer src="https://cusdis.com/js/cusdis.es.js"></script>
  </section>
  ```

---

## 5. Maintenance Scripts (in `scripts/`)
- `python scripts/update_sitemap.py`: Automatically rescans HTML files and writes updated `sitemap.xml`.
- `python scripts/audit_site.py`: Comprehensive audit verifying 0 broken links, 0 canonical mismatches, valid Open Graph tags, and 0 links pointing to `index.html`.
- `python scripts/sync_navigation.py`: Synchronizes the header navigation dropdowns and footer links across all pages.

---

## 6. Git Identity & Pseudonymity
- Maintain the pseudonym **astronautx**.
- All git commits must be authored as:
  - Name: `astr0nautx`
  - Email: `astr0nautx@users.noreply.github.com`
