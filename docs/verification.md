# Verification

Completed 18 September 2026 in the local Codex browser preview.

## Expansion and 2048px exports — 18 September 2026

- Added 130 original icons; the collection now has 220 icons and 18 live categories. Rebuilt 242 indexable pages plus the 404 page.
- The numeric size field and slider both support every integer from 16 to 2048. Invalid sizes disable export; valid input, slider changes, and Reset restore the expected state.
- Browser checks confirmed 2049 is rejected, 2048 produces SVG with matching width/height, 147 is retained exactly, the slider reaches 2048, and Reset returns both controls to 24.
- A browser test harness inspected the real PNG Blob: 116,056 bytes, valid PNG signature, and IHDR dimensions 2048 × 2048. The normal local Downloads location did not contain this run's files, so byte-level generation was verified in the browser instead of claiming a saved-file check.
- Reviewed all 130 new icons at stroke widths 1, 1.75, and 2.5. Regenerate the contact sheets with `python3 scripts/proof.py`.
- Fixed a stale JavaScript cache mismatch by adding content-hash query versions for scripts and stylesheet in generated pages.
- `scripts/validate.py` now checks both export controls' bounds and step on every generated icon/category page, alongside existing SVG, roadmap, link, metadata, and sitemap checks.

The results below document the original 90-icon release and are retained as historical verification.

## Automated checks

- `python3 scripts/build.py` passes the SVG geometry/attribute allowlist and generates 90 SVG assets and 108 indexable pages.
- `python3 scripts/validate.py` passes: 90 SVG contracts; 760 unique roadmap slugs and accurate available/planned status; 109 HTML pages including the noindex 404; all local links and fragment targets; unique-page metadata; 90 image/breadcrumb structured-data records; sitemap and image references.
- `node --check app.js` passes.
- Named palette text/focus/control contrast pairs pass WCAG ratio thresholds. Exact computed OKLCH-to-linear-sRGB ratios are recorded in `.hallmark/contrast.json`. User-selected icon colors are intentionally unrestricted.

## Browser interactions verified

- Search synonym `envelope` returns Mail.
- Searching an unknown term displays the empty state; Clear filters restores the library.
- Arrows category shows eight icons; All icons restores 90.
- A–Z sorting begins Alarm, Arrow down, Arrow left, Arrow right, Arrow up.
- Selecting an icon updates the inspector and details link.
- Custom color, 2.5 stroke, and nontransparent background appear in copied SVG markup.
- Invalid hex input shows an error and does not enter the SVG export; Reset restores defaults.
- Keyboard search opens, filters, supports arrow navigation, and closes with Escape.
- SVG copy and direct-link copy succeed.
- SVG and PNG downloads create files. Downloaded `home.svg` parsed as XML with 128px width and a 24-unit viewBox; `home-128px.png` has the PNG signature and 128×128 dimensions.
- Mobile selection moves to the editor; Back to icons returns focus to the selected card.
- Heart detail page renders its canonical URL and image on mobile.
- No browser warnings/errors were captured in the tested flows.

The browser's download-event waiter timed out despite a completed file download. File signatures and dimensions were therefore checked directly instead of treating the event timeout as an export failure.

## Visual review

The homepage was viewed at 320, 375, 414, 768, and 1280px widths. Document/body scroll widths matched the viewport at every tested width. The 320px Heart detail page was also viewed and did not overflow. The mobile search button has a persistent accessible name; mobile editor navigation and desktop editor scroll containment were added during review.

The full 90-icon contact sheet was visually reviewed at stroke widths 1, 1.75, and 2.5. See `/docs/icon-proof.html` for the reusable comparison. No obvious missing geometry or clipping was observed at that proof size. This is not a substitute for reviewing each future batch at all four target optical sizes.

Hallmark review: Catalogue composition, Cobalt palette, N13 keyboard search, Ft2 compact footer, no marketing hero imagery, no fake browser chrome, no invented metrics, consistent original SVG family, token-based colors and fonts, visible focus states, and reduced-motion handling. Self-critique: Philosophy 4, Hierarchy 5, Execution 4, Specificity 5, Restraint 5, Variety 4. Catalogue repetition and editor control grouping are intentional product structures, not marketing feature tiles.

## Limits

- This is locally built and tested, not deployed. Public asset links become available when the site is hosted at the domain.
- Browser testing covered the available local browser, not a full Safari/Firefox/device lab. Keyboard behavior was exercised; a screen-reader audit was not performed.
- Clipboard-denial and PNG-error recovery paths are implemented but were not force-injected during browser testing.
- Core content and original download links are present in static HTML; a browser run with JavaScript fully disabled was not performed.
- The color editor can deliberately create low-contrast icons. No promise is made that arbitrary chosen colors are accessible.
- Research is qualitative coverage analysis, not search-volume or ranking evidence.
- The SVG validator rejects active content and unsupported attributes; it does not certify artistic quality, check every SVG path command geometrically, or establish legal originality.

## Public-site cleanup and expansion — 18 September 2026

Added 69 original icons: 289 total across 24 live categories. Reviewed the new contact sheet at stroke widths 1, 1.75 and 2.5. Build/validation passes for 289 SVG contracts, 760 unique roadmap concepts, 318 public HTML pages, local links, structured data and sitemap. JavaScript syntax check passes.

The inspector displays a production URL and copies either that URL or a 24px HTML image tag. Verified both clipboard results for Store and the updated URL after selecting Store in the catalogue. Mobile editor and imprint have no horizontal overflow at 375px.

Preview serves only `dist/`. HTTP checks: home, imprint and Store SVG return 200; roadmap and both internal prompt/roadmap JSON routes return 404. Source data and roadmap template remain in the repository. Decorative link arrows removed. No production deployment performed; production embed URLs require deployment.

## 500-icon expansion, CC0 and local typography — 18 September 2026

Added 211 icons, bringing the collection to 500 across all 30 categories. New categories include Home & buildings, Sports & outdoors, Animals, Science & tools, Games & entertainment, and Accessibility & inclusion. All new icons were reviewed in four contact sheets at stroke widths 1, 1.75 and 2.5. Refined edge spacing for books, octopus and spacing controls; closed calendar and archive silhouettes where no badge requires an opening.

CC0 1.0 now applies to the original icon artwork, SVGs and PNG exports. Updated the license page, every footer, inspector notice, 500 ImageObject license properties, authoring contract and LICENSE-ICONS. The official German Creative Commons deed was checked against the user-supplied URL. Removed the previous custom license restriction.

Removed Google Fonts links and preconnects. Display/body text use system-ui stacks and code uses a local monospace stack. No font files or font CSS are requested externally. Verified all 535 generated public HTML pages and CSS for absent external fonts; every footer links CC0.

Validation passes: 500 SVG contracts, 760 roadmap concepts, 535 HTML pages with local links, image metadata and sitemap; JavaScript syntax passes. Catalogue and license pages have no horizontal overflow at 320, 375, 414 and 768px. Browser checks confirmed 500-icon count, Octopus search returning one result, selection and copied SVG. Preview remains local; no production deployment performed.

## Equal 600-icon expansion — 18 September 2026

Added exactly 600 icons: 20 additions in each of the 30 categories, for 1,100 total. Earlier category totals differ; the new additions are equal. `data/expansion-600.json` records before/after counts and the complete batch. Validation now verifies its 600 unique slugs and category distribution. The internal roadmap has 1,228 concepts; additional concepts were authored editorially for this project, not claimed as new external research.

Reviewed every new icon in ten 60-icon contact sheets, each at 1, 1.75 and 2.5 stroke widths. New standalone pictograms and contextual action/state variants share inherited root strokes and the existing 24px grid. Corrected the duplicate cross geometry, replaced the pinned-note marker with a pushpin, and inset drawings that exceeded the 1.25-unit stroke-clearance bounds. A browser geometry check of all 600 new icons reported no remaining bounds violations before the final pinned-note refinement, which is also contained within the grid. No identical SVG body strings remain in the full library.

Build and validation pass: 1,100 SVG contracts, 1,228 unique roadmap concepts, 1,135 public HTML pages and local links, 1,100 ImageObject/breadcrumb records, sitemap and image references. JavaScript syntax passes.

Browser checks: home reports 1,100 icons; Files reports 47 (27 previous + 20 new); Pineapple search returns one result; copied SVG has 2048px width and height. PNG blob verification confirms the correct PNG signature, 2048×2048 dimensions and 175,583 bytes for Pineapple. New SVG, detail and category routes return HTTP 200. Catalogue has no horizontal overflow at 320, 375, 414 or 768px. CC0, system fonts and public-only dist output are preserved. No production deployment performed.

## AI and device expansion — 19 September 2026

Added 54 icons: 12 AI/model concepts, 10 desktop hardware/workflows, 10 Windows/window-management concepts, 12 mobile-phone concepts, and 10 connectivity/security concepts. Total: 1,154 icons, 30 categories. New concepts extend the internal roadmap to 1,279 entries.

Reviewed all 54 new drawings at stroke widths 1, 1.75 and 2.5. Corrected the AI workflow, phone-notification and hotspot bounds; browser getBBox checks with a 1.25-unit stroke reserve now report no violations. No identical SVG body strings found.

Two-character search terms now match whole tokens: searching AI returns exactly the 12 AI icons rather than unrelated mail icons. Verified Windows, desktop, phone and USB searches; the clear-search button restores all 1,154 icons. Verified AI chip selection, production direct-link clipboard content and 2048×2048 copied SVG dimensions. Catalogue has no horizontal overflow at 375px.

Build and validation pass: 1,154 SVG contracts, 1,189 public HTML pages with valid local links, 1,154 image/breadcrumb records, sitemap and image references. JavaScript syntax check passes. The prior interrupted build was regenerated completely. No production deployment performed.
