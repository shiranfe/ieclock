## Cursor Cloud specific instructions

This is a **static HTML/CSS website** (IEC Lock product site, Hebrew RTL). There is no build system, no package manager, no backend, no database, no JavaScript framework.

### Running the site

Serve files with Python's built-in HTTP server from the repo root:

```bash
python3 -m http.server 8080
```

Then open `http://localhost:8080` in Chrome.

### Project structure

- Root HTML files: `index.html`, `how-it-works.html`, `applications.html`, `case-studies.html`
- Product pages: `products/index.html` and 15 individual product HTML files under `products/`
- Assets: `assets/img/` (logo SVG, product JPGs, tech spec PNGs, application/case-study images)
- Utility script: `update_mobile_css.py` — one-time Python script for injecting mobile CSS (not part of runtime)

### Key notes

- **No lint/test/build tooling exists.** There are no `package.json`, `requirements.txt`, CI configs, or test suites.
- All styling is **inline CSS** within each HTML file (no external stylesheets).
- The site uses **Google Fonts** (Heebo, Barlow Condensed) loaded via CDN `<link>` tags and **YouTube embeds** on the How it Works page — both require network access.
- The site is **RTL Hebrew** (`<html lang="he" dir="rtl">`).
