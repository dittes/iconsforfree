# iconsforfree

A plain HTML/CSS/JavaScript icon catalogue for **iconsforfree.com**. Includes 1,154 original SVG icons, a live editor, SVG/PNG downloads, keyboard search, 30 category pages, and 1,154 individual icon pages.

## Preview

```sh
python3 scripts/build.py
python3 -m http.server 4188 --bind 127.0.0.1 --directory dist
```

Open http://127.0.0.1:4188. Serve the generated `dist/` folder; opening `index.html` as a `file://` document will not resolve root-relative paths.

## Important files

- `data/icon-generation.json` — reusable generation prompt, variables, style contract, references, and acceptance checklist.
- `data/icon-roadmap.json` — 1,279 unique concepts across 30 categories, with priorities and availability.
- `data/icons.json` — source of truth for the 1,154 implemented icons, safe geometry, descriptions, and synonyms.
- `docs/research.md` — source-linked product research, production plan, SVG decisions, and SEO strategy.
- `templates/icon.html` — reusable individual icon page template.
- `scripts/build.py` — standard-library static generator and SVG allowlist validator.
- `tokens.css`, `styles.css`, `app.js` — Hallmark Cobalt design and dependency-free interactions.

## Add an icon

1. Choose a planned concept and use `prompt_template` in `data/icon-generation.json`. Substitute `{{slug}}`, `{{category}}`, and `{{concept}}`; attach 4–6 approved reference SVGs.
2. Review the generated geometry in context. Do not blindly publish AI output or copy an existing library's paths.
3. Add `{slug, name, category, tags, description, body}` to `data/icons.json`. `body` contains SVG geometry only. It must inherit stroke/fill from the root.
4. Run:

```sh
python3 scripts/build.py
python3 scripts/validate.py
node --check app.js
```

The build updates the SVG files, HTML pages, embedded browser data, roadmap availability, sitemap, and robots file. No Node packages are required. Use Python 3.12+ (tested on 3.13).

Edit source templates/build functions rather than generated HTML. Removing or renaming an icon requires deciding what to do with its previously published URLs; the build does not delete old pages automatically. Prefer redirects for public URLs.

## Features

Search by name, category, or synonym; filter by category; sort alphabetically; use Cmd/Ctrl+K for keyboard search. Select an icon to customize stroke color, background color/transparency, stroke width (1–2.5 units), and export size (16–2048px). Enter an exact size using the numeric field. The enlarged preview is fixed at 80px for inspection. PNG export uses the exact selected dimensions.

The customizer applies color and weight across catalogue previews; background applies to the selected icon and exports. SVG copy/download bakes in your chosen color. Default source SVGs use `currentColor`. Clipboard failures expose a selectable text fallback. Basic page navigation and original downloads work without JavaScript.

## Direct links and hosting

- Asset: `https://iconsforfree.com/icons/home.svg`
- Detail page: `https://iconsforfree.com/icons/home/`

The inspector shows a production URL and can copy the URL or a ready-to-paste HTML image tag. Public URLs work after deployment. Direct URLs return default SVGs; custom appearance is carried by downloaded files or copied inline SVG. An external SVG image cannot inherit the surrounding page's text color. Query parameters on static SVG files do not customize them.

Deploy only `dist/` to a static host with directory index support. This allowlisted output excludes the generation prompt, roadmap, source data, templates, scripts, and internal documents. `CNAME` and `.nojekyll` support a custom-domain GitHub Pages setup. No hosting, DNS, or production changes have been made. If using another domain, update `BASE` in `scripts/build.py`, `directURL` in `app.js`, the guide's embedding example, and `CNAME`, then rebuild.

## Design and permission

Hallmark: Catalogue / Cobalt, system UI fonts with a system monospace stack for code. Cool near-white surfaces, cobalt selection, category rail, icon grid, and live inspector. Responsive layouts and reduced-motion support. No external fonts or font requests; all icon assets are local.

The original icons are dedicated to the public domain under CC0 1.0 Universal. Attribution is not required. See `LICENSE-ICONS` and `/license/`. No external icon library is bundled. The roadmap contains planned concepts, not additional finished artwork.

See `docs/verification.md` for validation results and limitations.

The earlier 600-icon expansion adds exactly 20 icons to each of the 30 categories. See `data/expansion-600.json` for the per-category counts and complete batch manifest. Existing category totals differ; the 600 additions are evenly distributed.

The latest batch adds 54 AI, desktop, window, phone and connectivity icons. Two-character searches such as `AI` match complete terms, so unrelated words such as “mail” are excluded.
