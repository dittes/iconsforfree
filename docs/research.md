# Iconsforfree: product, icon, and discovery research

Research date: 17 September 2026. This is a qualitative coverage study of primary sources, not a keyword-volume study. The initial SVG geometry was drawn for this project; no external SVG artwork was imported. Shared concepts such as a house or a magnifying glass are conventional symbols.

## Recommended product

Make the homepage a working catalogue. A visitor should be able to find a symbol, see it at a useful scale, change its appearance, and get a usable file without an account. Search names and synonyms, expose categories, retain normal detail-page links, and explain the difference between an editable inline SVG and an externally linked image.

The implemented product is plain HTML, CSS, and JavaScript, with generated static pages. Python is an authoring convenience only; neither Python nor a server-side application is needed in production. No framework, icon-library runtime, tracking, paid service, or build-time package installation is required. Google Fonts is the sole external presentation dependency; generic fallbacks remain usable if it is blocked.

## Primary-source findings and implications

| Source | Observation | Decision for this project |
| --- | --- | --- |
| [Lucide catalogue](https://lucide.dev/icons/) | Browsing combines search, semantic categories, and color/size/stroke controls. | Treat finding and adapting an icon as one workflow. Index synonyms and related categories. |
| [Lucide contribution guide](https://lucide.dev/contribute/icons/) | Icon submissions are a design contribution process, not simply a file upload. | Require visual review and shared references before publishing generated SVGs. |
| [Tabler](https://tabler.io/icons) | A common grid and stroke support consistent customization. Its catalogue exposes size, stroke, and color controls. | Use one 24-unit coordinate system and inherited stroke properties. Our default weight is 1.75, with a limited supported range. |
| [Carbon category source](https://github.com/carbon-design-system/carbon/blob/main/packages/icons/categories.yml) | Actions contain subfamilies such as controls, formatting, navigation, and operations. | Plan complete workflow families instead of a disconnected list of objects. |
| [Phosphor core](https://github.com/phosphor-icons/core) | A flexible icon family is distributed as multiple weights. | Keep Line 01 deliberately narrow: one outline geometry with adjustable stroke. Separate filled and duotone styles would need separate rules. |
| [Material Symbols](https://developers.google.com/fonts/docs/material_symbols) | Weight, fill, grade, and optical size are distinct axes. | Do not describe a thicker stroke as a filled or optically corrected variant. Test small icons explicitly. |
| [MDN SVG color](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/color) | `currentColor` is available to paint attributes such as stroke. | Root `stroke="currentColor"` for reusable source; explicit hex for portable custom downloads. |
| [MDN stroke width](https://developer.mozilla.org/en-US/docs/Web/SVG/Reference/Attribute/stroke-width) | Stroke width changes SVG line thickness. | Keep stroke as an inherited attribute, never expanded into filled paths. |
| [W3C functional images](https://www.w3.org/WAI/tutorials/images/functional/) | An image used as a control needs an alternative describing its function. | Name icon-only controls and hide decorative SVGs from assistive technology. |
| [Google image SEO](https://developers.google.com/search/docs/appearance/google-images) | Discoverable image URLs, meaningful image landing pages, standard image elements, and descriptive context help search engines understand images. SVG is supported. | Generate real HTML pages and SVG files, include an `img` on each detail page, and add an image sitemap. |

## Production roadmap

`data/icon-roadmap.json` lists **760 unique concepts in 30 categories**, including the 220 implemented icons. Each concept has a slug, status, and production brief. The roadmap page links only to available icons; planned items do not get empty SEO pages.

| Priority | Concepts | Why this comes first |
| --- | ---: | --- |
| 1 | 333 | Core controls, communication, files, identity, security, editing, media, commerce, scheduling, technology, status, and accessibility. These let a designer finish an entire flow. |
| 2 | 272 | Weather, travel, analytics, typography, sustainability, food, health, education, productivity, transport, and finance. These broaden real product coverage. |
| 3 | 155 | Buildings, sport, animals, science/tools, shapes, and entertainment. Expand when the core families are coherent. |

The first release had 90 icons in 14 categories. The expanded collection has 220 icons in 18 categories. The priority numbers are proposed ordering, not observed demand, download counts, or promises about search rankings.

### Batch planning

1. Stabilize the existing six reference icons: home, search, mail, user, folder, heart.
2. Complete missing directional pairs and status variants. Keep the shared geometry aligned across a family.
3. Produce batches of 12–24 closely related concepts with the JSON contract and approved SVG references attached.
4. Review legibility at 16, 24, 32, and 48 pixels, at each supported weight, on light and dark backgrounds.
5. Resolve synonyms before production: a search alias should not become a duplicate drawing. Some planned concepts have overlapping meanings (medical vs general thermometer, travel vs transport aircraft); merge or deliberately distinguish them before drawing.
6. Publish only reviewed icons, their useful descriptions, and related links. Keep the roadmap status synchronized.

### How to validate actual demand later

Use Search Console queries, privacy-conscious on-site search summaries, and download events after launch. Record searches with no matches and map them to missing concepts. Prioritize recurring needs and incomplete families. The current build deliberately has no analytics integration or fabricated keyword-volume data.

## SVG technical contract

One `viewBox="0 0 24 24"`, no fill, round caps and joins, root stroke width 1.75. Geometry inherits root styles. Source backgrounds are transparent. Exports may prepend a separate fill-only rectangle; background color must never fill the actual pictogram.

Prefer centerlines in the 3–21 region; inspect the painted bounds at stroke 2.5. Use real editable strokes and simple primitives. Do not use a raster generation model to draw final SVG source: it cannot reliably produce clean, parameterized vector geometry. A code-capable generator can produce the JSON body, followed by validation and visual review.

An SVG embedded as an external `img` is a separate image document: the host page cannot recolor its internal stroke with its own `color`. The default direct URL is therefore fixed geometry and default appearance. Use inline markup for inherited color, download a customized file for fixed colors, or use a CSS mask for a single-color silhouette. Static query strings such as `?color=red` do not transform SVGs.

A future dynamic endpoint would need server-side input validation, caching, content-type handling, and abuse limits. It is intentionally outside this static build. Existing stable paths are `/icons/home.svg` for assets and `/icons/home/` for pages. If future revisions break compatibility, introduce versioned asset paths rather than silently changing established symbols.

## SEO template and information architecture

The template is `templates/icon.html`; the build renders it into a directory per available icon. Each page includes:

- A unique title, description, canonical URL, and descriptive H1.
- A normal `img` pointing at the real SVG, with meaningful alternative text.
- Unique visual/use description, tags, collection specifications, and customization controls.
- An original SVG download that works without JavaScript.
- Links to its category, related icons, guide, and license.
- `ImageObject` and `BreadcrumbList` JSON-LD that describes visible content.

Category pages are static too. The sitemap includes all 242 current indexable pages and images for the 220 icon pages. Search/filter query strings canonicalize to the underlying page rather than producing thousands of thin pages. The 404 page is noindex. No ratings, usage counts, fake reviews, or unsupported rich-result claims are inserted.

Structured data helps describe content; it does not guarantee indexing, rankings, or rich results. After launch, verify the domain in Search Console, submit the sitemap, and check the deployed canonical URLs, HTTPS, successful image responses, and crawler access. Social previews may benefit from dedicated PNG artwork later; the build includes text Open Graph metadata without pretending to have a rendered social-image pipeline.

## Deployment and maintenance

Serve the repository root as a static website at iconsforfree.com. The existing CNAME is preserved. Root-relative asset URLs assume a custom domain or root deployment, not a repository subpath. No production deployment or DNS change was performed by this build.

The public icon usage page grants free personal and commercial use and modification; it does not claim endorsement or third-party trademark rights. The name and logo are excluded from the icon permission. New contributors should explicitly authorize distribution before their artwork enters the collection.
