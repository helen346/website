# Imagination — website

The public site for [imaginationpr.co.uk](https://imaginationpr.co.uk): a static site with no database, no plugins and nothing to update.

## What is here

| Path | Purpose |
|---|---|
| `src/pages/*.html` | Page content, one file per page, with a small front-matter block |
| `src/layout.html` | Shared header, footer and `<head>` |
| `tools/build.py` | Assembles the pages into the root (`index.html`, `services/index.html`, …) |
| `css/site.css` | All styles. Palette and type are set as variables at the top |
| `js/site.js` | Mobile menu only. The site works without JavaScript |
| `assets/logo/` | Logo files: wordmark, stacked lockup, monogram, favicon (SVG outlines) |
| `assets/fonts/` | Self-hosted, subsetted fonts (Noto Serif Display, Instrument Sans) |
| `assets/img/` | Photography. See the README there for the file names each slot expects |
| `tools/gen_logo.py` | Regenerates the logo SVGs from the source fonts |
| `netlify.toml`, `_redirects` | Hosting config, caching and redirects from the old WordPress URLs |

## Editing a page

1. Edit the file in `src/pages/`.
2. Run `python3 tools/build.py` (Python 3, no packages needed).
3. Commit both the source and the generated HTML.

The generated HTML at the root is what gets served, so the site can be hosted on Netlify, Cloudflare Pages, GitHub Pages or any plain web host.

## Hosting

Netlify is the intended host: connect this repository, leave the build command empty and set the publish directory to `.`. The contact form uses Netlify Forms and sends submissions to the address configured in the Netlify dashboard (Forms → Notifications). Redirects and cache headers in `netlify.toml` are picked up automatically.

Point the domain at Netlify with a single DNS change once the preview has been approved.

## Photography

Placeholders are shown wherever a photograph is expected. Drop files into `assets/img/` using the names listed in `assets/img/README.md`, then replace the matching `<figure class="ph …">` placeholder in `src/pages/` with an `<img>` inside it.

## Logo

The mark is IMAGINATION in extra-condensed Didone capitals, nothing else. Files in `assets/logo/`:

- `wordmark.svg` / `wordmark-light.svg` / `wordmark-burgundy.svg` — the mark in ink, in porcelain for dark backgrounds, and in burgundy
- `stacked.svg` / `stacked-light.svg` — formal lockup with a hand-drawn rule and "Public Relations · London"
- `mark-i.svg` / `mark-i-light.svg` — the I alone, for small spaces
- `favicon.svg` — the I on a burgundy disc

All are outlines, so they need no fonts installed. Colours: ink `#171520`, burgundy `#6B1D2E`, porcelain `#F5F3EF`.
