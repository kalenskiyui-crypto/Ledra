# Ledra — landing page

Static one-page site deployed on Vercel from `main`.

## Files

- `index.html` — the page (built from the design canvas, see below)
- `support.js`, `vendor/` — runtime that renders the page in the browser
- `assets/` — logos, founder video and poster (hashed names, cached for a year)
- `robots.txt`, `sitemap.xml`, `404.html`, `site.webmanifest`, `og-image.png`, favicons
- `vercel.json` — clean URLs, redirects, security and cache headers

## Updating from the design canvas

1. Export / copy the canvas source `Main.dc.html`.
2. `python3 scripts/build.py path/to/Main.dc.html` — writes `index.html` with asset paths,
   the React runtime and the full SEO `<head>` (title, description, canonical, Open Graph,
   Twitter, JSON-LD).
3. Commit and push to `main`.

The production domain lives in `SITE` at the top of `scripts/build.py`; if it changes, update it
there and in `robots.txt` and `sitemap.xml`.
