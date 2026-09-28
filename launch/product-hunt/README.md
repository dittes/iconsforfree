# Icons for free launch kit

Upload the five numbered PNGs in order: collection, customization, categories, developer usage, CC0. Each is 1270×760. thumbnail.png is the separate 240×240 product mark. contact-sheet.png is an overview for review. Editable SVG originals are included. Artwork uses the actual icon collection and locally rendered fonts.

The social preview is a dedicated 1200×630 adaptation of the cover, included in the ZIP under social/. The website uses this image for Open Graph and X cards. Deploy dist/ before sharing production links.

Regenerate from the project root after count changes:

```sh
python3 scripts/launch-assets.py
node scripts/render-launch.cjs
python3 scripts/build.py
```

The optional rasterization step requires Node and the Sharp module (resolvable through node_modules or NODE_PATH); the normal website build only requires Python. Recreate the launch ZIP after regenerating.

Gallery sizing reference: https://www.producthunt.com/launch/preparing-for-launch

Suggested tagline: Original SVG icons. Customize, download, use freely.
