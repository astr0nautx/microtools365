# microtools365

Free, no-signup, multi-purpose online tools. Plain HTML/CSS/JS — no build step, no framework. Deploys to Vercel as a static site.

microtools365 is a fast, no-signup utility website built for everyday tasks. It includes dedicated calculator and text tools, a practical blog for helpful guides, and core informational pages such as About, Privacy Policy, and Terms of Use. Each tool is a standalone static page, keeping the site lightweight, easy to navigate, and simple to deploy.


## Guidelines & Architecture

See [`DEVELOPMENT_GUIDELINES.md`](DEVELOPMENT_GUIDELINES.md) for permanent coding standards, Core Web Vitals optimization rules, SEO/metadata requirements, and blog/tool templates.

## Maintenance

Regenerate the sitemap after adding or removing a page:

```bash
python scripts/update_sitemap.py
```

Run comprehensive site audit (validates titles, canonical URLs, broken links, Open Graph tags, and zero `index.html` references):

```bash
python scripts/audit_site.py
```

Synchronize navigation and footer links across all pages:

```bash
python scripts/sync_navigation.py
```

The shared browser behavior in `microtools365/js/main.js` controls navigation links, footer links, related tools, recently used tools, dark mode, and theme behavior.
