#!/usr/bin/env python3
"""Generate a dependency-free static site from reviewed icon data. Python 3.12+."""
from pathlib import Path
import json, re, html, hashlib, shutil, xml.etree.ElementTree as ET
from string import Template
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
BASE='https://iconsforfree.com'
ICONS=json.loads((ROOT/'data/icons.json').read_text())
ROADMAP=json.loads((ROOT/'data/icon-roadmap.json').read_text())
E=html.escape
PUBLIC_FILES=set()
categories=list(dict.fromkeys(i['category'] for i in ICONS))
def slugify(s):return s.lower().replace(' & ','-').replace(' ','-')
def validate():
 seen=set()
 allowed={'path':{'d'},'circle':{'cx','cy','r'},'ellipse':{'cx','cy','rx','ry'},'rect':{'x','y','width','height','rx','ry'},'line':{'x1','y1','x2','y2'},'polyline':{'points'},'polygon':{'points'}}
 for i in ICONS:
  assert re.fullmatch('[a-z0-9]+(?:-[a-z0-9]+)*',i['slug']) and i['slug'] not in seen, 'Invalid/duplicate slug'
  seen.add(i['slug'])
  assert i['name'] and i['category'] and i['description'] and isinstance(i['tags'],list)
  assert all(isinstance(t,str) for t in i['tags'])
  tree=ET.fromstring('<svg>'+i['body']+'</svg>')
  assert len(tree)>0
  for child in tree:
   assert child.tag in allowed and not list(child) and not (child.text or '').strip(), 'Unsafe geometry'
   assert set(child.attrib)<=allowed[child.tag], 'Unsupported SVG attribute'
   for key,val in child.attrib.items():
    pattern=r'[0-9eE+.,\sMmLlHhVvCcSsQqTtAaZz-]+' if key=='d' else r'[0-9eE+.,\s-]+'
    assert re.fullmatch(pattern,val), f'Unsafe SVG value: {val}'
   assert not (child.tail or '').strip()
  assert not (tree.text or '').strip()
def svg(i,size=24,decorative=True):
 return f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round"'+(' aria-hidden="true"' if decorative else '')+'>'+i['body']+'</svg>'
def glyph(name):return svg(next(i for i in ICONS if i['slug']==name))
def write(path,content):
 if not path.startswith('data/'):PUBLIC_FILES.add(path)
 target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content+'\n')
def card(i):
 return f'<a class="icon-card" href="/icons/{i["slug"]}/" data-slug="{i["slug"]}" aria-label="Customize {E(i["name"])} icon">{svg(i)}<span>{E(i["name"])}</span></a>'
def inspector(i):
 return f'''<aside class="inspector" id="customizer" aria-label="Icon customizer">
 <button class="text-button back-to-icons" id="back-to-icons" type="button">← Back to icons</button><div class="inspector-top"><div><h2 id="selected-name">{E(i['name'])}</h2><p id="selected-category">{E(i['category'])} / Line 01</p></div><a class="icon-button" id="detail-link" href="/icons/{i['slug']}/" aria-label="Open icon details">{glyph('info')}</a></div>
 <div class="preview-stage" id="preview">{svg(i,80)}</div><div class="preview-meta"><span>24 × 24 grid</span><span>SVG · editable stroke</span></div>
 <div class="controls"><div><div class="field-label"><label for="stroke-color">Stroke color</label><button class="text-button" id="reset" type="button">Reset</button></div><div class="color-field"><input type="color" id="stroke-color" value="#253047" aria-label="Stroke color picker"><input class="hex-field" id="stroke-hex" value="#253047" aria-label="Stroke color hex" maxlength="7" spellcheck="false"><div class="swatches"><button class="swatch" data-color="#253047" aria-label="Charcoal stroke" style="--swatch:var(--color-ink)"></button><button class="swatch" data-color="#2455db" aria-label="Cobalt stroke" style="--swatch:var(--color-accent)"></button></div></div></div>
 <div><label class="field-label" for="stroke-width">Stroke width <output id="stroke-output" for="stroke-width">1.75</output></label><input id="stroke-width" type="range" min="1" max="2.5" step="0.25" value="1.75"><div class="range-labels"><span>Light</span><span>Bold</span></div></div>
 <div><div class="field-label"><label for="icon-size">Export size</label><span class="size-entry"><input id="size-number" class="hex-field size-number" type="number" min="16" max="2048" step="1" value="24" aria-label="Export size in pixels"><span>px</span></span></div><input id="icon-size" type="range" min="16" max="2048" step="1" value="24"><div class="range-labels"><span>16 px</span><span>2048 px</span></div></div>
 <div><label class="field-label" for="background-color">Background</label><div class="color-field"><input id="background-color" type="color" value="#eef2ff" aria-label="Background color picker" disabled><input class="hex-field" id="background-hex" value="#eef2ff" aria-label="Background color hex" maxlength="7" spellcheck="false" disabled></div><label class="check-label"><input type="checkbox" id="transparent" checked>Transparent background</label></div>
 <div class="actions"><button class="btn primary" id="download-svg">{glyph('download')}Download SVG</button><div class="action-row"><button class="btn" id="copy-svg">{glyph('code')}Copy SVG</button><button class="btn" id="download-png">PNG</button></div><div class="embed-controls"><label class="field-label" for="direct-url">Use in your project</label><input id="direct-url" class="hex-field direct-url" value="{BASE}/icons/{i['slug']}.svg" readonly spellcheck="false"><div class="action-row"><button class="btn" id="copy-link">Copy link</button><button class="btn" id="copy-embed">Copy HTML</button></div><p class="embed-note">Direct links use the original SVG. Download or copy SVG for custom colors and strokes.</p></div><p id="action-status" class="status" role="status" aria-live="polite">Select an icon. Make it yours.</p></div></div>
 <div class="inspector-foot"><span>CC0 · No attribution required</span><a href="/license/">License</a></div></aside>'''
def nav():
 return f'''<a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="shell topbar-inner"><a class="brand" href="/" aria-label="Icons for free home"><svg width="28" height="28" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect x="2" y="2" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/><rect x="17" y="2" width="9" height="9" rx="2" fill="currentColor"/><rect x="2" y="17" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/><rect x="17" y="17" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/></svg><span>iconsforfree<span class="dotcom">.com</span></span></a><button class="search-trigger" id="open-search" aria-label="Find an icon">{glyph('search')}<span>Find an icon…</span><kbd>⌘ K</kbd></button><nav class="nav-links" aria-label="Main navigation"><a href="/">Icons</a><a href="/guide/">How to use</a></nav></div></header>'''
def footer():
 return '<footer class="shell"><span>Small details. Better interfaces.</span><nav aria-label="Footer"><a href="https://creativecommons.org/publicdomain/zero/1.0/deed.de" rel="license">Icons: CC0 1.0</a><a href="/license/">License details</a><a href="/imprint/">Imprint</a></nav></footer>'
def dialog():
 return f'''<dialog id="search-dialog" aria-labelledby="command-title"><div class="dialog-head"><h2 id="command-title">Find your next icon</h2><button class="icon-button" id="close-search" aria-label="Close search">{glyph('close')}</button></div><div class="search-box">{glyph('search')}<input id="command-input" type="search" placeholder="Search icons and synonyms…" aria-label="Search all icons" autocomplete="off"></div><div class="command-results" id="command-results"></div><p class="dialog-hint">↑ ↓ to move · Enter to open · Escape to close</p></dialog>'''
def asset(path):
 return "/"+path+"?v="+hashlib.sha256((ROOT/path).read_bytes()).hexdigest()[:12]
def page(title,desc,path,body,structured=None):
 canonical=BASE+path
 social_image=BASE+asset('assets/social/preview.png')
 social_alt=f'Icons for free: {len(ICONS):,} original customizable SVG icons, with a selection of line icons on a cobalt and white background.'
 schema=f'<script type="application/ld+json">{json.dumps(structured).replace("<","\\u003c")}</script>' if structured else ''
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canonical}"><meta property="og:site_name" content="Icons for free"><meta property="og:locale" content="en_US"><meta property="og:image" content="{social_image}"><meta property="og:image:secure_url" content="{social_image}"><meta property="og:image:type" content="image/png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta property="og:image:alt" content="{E(social_alt)}"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="{E(title)}"><meta name="twitter:description" content="{E(desc)}"><meta name="twitter:image" content="{social_image}"><meta name="twitter:image:alt" content="{E(social_alt)}"><meta name="theme-color" content="#f8faff"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{asset('styles.css')}">{schema}<script src="{asset('assets/icons-data.js')}" defer></script><script src="{asset('app.js')}" defer></script></head><body>{nav()}{body}{footer()}{dialog()}</body></html>'''
def catalogue(category=None):
 items=[i for i in ICONS if not category or i['category']==category]
 catnav=''
 for cat in ['All icons']+categories:
  count=len(ICONS) if cat=='All icons' else sum(i['category']==cat for i in ICONS)
  href='/' if cat=='All icons' else f'/categories/{slugify(cat)}/'
  symbol='grid' if cat=='All icons' else next(i['slug'] for i in ICONS if i['category']==cat)
  active=(cat==category or cat=='All icons' and not category)
  catnav+=f'<a href="{href}" data-category="{E(cat)}" class="{"active" if active else ""}"'+(' aria-current="page"' if active else '')+f'>{glyph(symbol)}<span>{E(cat)}</span><span class="count">{count}</span></a>'
 heading=f'{category} icons.' if category else 'Free icons. Made to be yours.'
 intro_text='Original line icons for whatever you’re making. Customize, copy, and carry on.' if category else f'{len(ICONS):,} original SVG icons. Customize color and stroke, then download SVG or PNG.'
 home_extras='' if category else '<div class="home-benefits"><span>No signup</span><a href="/license/">CC0 · No attribution required</a><span>PNG up to 2048 px</span></div>'
 share_controls='' if category else '<div class="collection-share"><button class="btn" id="share-collection" type="button" hidden>Share collection</button><p id="share-status" class="share-status" role="status" aria-live="polite"></p><input id="share-fallback" class="hex-field" aria-label="Collection link to copy" value="https://iconsforfree.com/" readonly hidden></div>'
 return f'''<div class="shell"><section class="intro"><div><h1>{E(heading)}</h1><p>{E(intro_text)}</p>{home_extras}</div><div class="collection-note{' has-share' if not category else ''}"><strong>Line 01 collection</strong>{len(ICONS):,} icons · 30 categories{share_controls}</div></section>
 <main id="main" class="workspace" data-category="{E(category or 'All icons')}"><aside class="sidebar"><div class="sidebar-title">Browse the collection</div><nav class="category-nav" aria-label="Icon categories">{catnav}</nav><div class="sidebar-bottom"><a href="/guide/#design">Our design principles</a><p>One family.<br>A consistent point of view.<br>Room for your own style.</p></div></aside>
 <section class="catalogue" aria-label="Icon library"><noscript><p class="no-js">Choose an icon to open its page and download the original SVG. Enable JavaScript for customization.</p></noscript><div class="search-box">{glyph('search')}<input id="icon-search" type="search" placeholder="Search icons… try ‘arrow’ or ‘mail’" aria-label="Search this collection" autocomplete="off"><button class="clear-search" id="clear-search" aria-label="Clear search" hidden>{glyph('close')}</button></div><div class="results-head"><h2><span id="category-heading">{E(category or 'All icons')}</span> <span id="result-count" role="status">{len(items)} icons</span></h2><label><span class="sr-only" hidden>Sort icons</span><select id="sort" aria-label="Sort icons"><option value="collection">Collection order</option><option value="az">Name: A to Z</option><option value="za">Name: Z to A</option></select></label></div><div class="icon-grid" id="icon-grid">{''.join(card(i) for i in items)}</div><div class="empty-state" id="empty-state" hidden><h2>No icons found.</h2><p>Try a simpler word, like “mail”, “home”, or “arrow”.</p><button class="btn" id="reset-search">Clear filters</button></div><div class="catalogue-foot"><span>Same grid. Same stroke. Every icon belongs.</span><span>Click an icon to customize</span></div></section>{inspector(items[0])}</main>
 <section class="use-strip"><div><h2>A little SVG. A lot of freedom.</h2><p>Change the color. Find your weight. Use it in a website, an app, or your next big idea.</p><a href="/guide/">A quick guide to using icons</a></div><pre>&lt;svg viewBox="0 0 24 24"\n     fill="none"\n     stroke="currentColor"\n     stroke-width="1.75"&gt;\n  &lt;!-- Make it yours. --&gt;\n&lt;/svg&gt;</pre></section></div>'''
validate()
for i in ICONS:write(f'icons/{i["slug"]}.svg',svg(i,24,False))
write('assets/icons-data.js','window.ICON_LIBRARY = '+json.dumps(ICONS).replace('<','\\u003c')+';')
write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2455db"/><path d="M8 8h6v6H8Zm10 0h6v6h-6ZM8 18h6v6H8Zm10 0h6v6h-6Z" fill="#f8faff"/></svg>')
write('index.html',page(f'{len(ICONS):,} free SVG icons · CC0 | Icons for free',f'Original icons for websites, apps and side projects. Customize colors and strokes. Download SVG or PNG up to 2048px. CC0, no attribution or signup.','/',catalogue(),{'@context':'https://schema.org','@type':'WebSite','name':'iconsforfree','url':BASE+'/'}))
urls=['/','/guide/','/license/','/imprint/']
for cat in categories:
 path=f'/categories/{slugify(cat)}/';urls.append(path)
 write(path.strip('/')+'/index.html',page(f'{cat} SVG icons — free downloads | iconsforfree',f'Browse original {cat.lower()} outline icons. Adjust colors and stroke weight, then download SVG or PNG.',path,catalogue(cat)))
for i in ICONS:
 path=f'/icons/{i["slug"]}/';urls.append(path)
 related=[j for j in ICONS if j['category']==i['category'] and j!=i][:5]
 body=Template((ROOT/'templates/icon.html').read_text()).substitute(slug=i['slug'],name=E(i['name']),lower_name=E(i['name'].lower()),category=E(i['category']),category_slug=slugify(i['category']),description=E(i['description']),tags=''.join(f'<a href="/?q={quote(t)}">{E(t)}</a>' for t in i['tags']),inspector=inspector(i),related=''.join(card(j) for j in related))
 structured={'@context':'https://schema.org','@graph':[{'@type':'ImageObject','name':i['name']+' SVG icon','description':i['description'],'contentUrl':BASE+f'/icons/{i["slug"]}.svg','url':BASE+path,'encodingFormat':'image/svg+xml','width':24,'height':24,'license':'https://creativecommons.org/publicdomain/zero/1.0/','acquireLicensePage':BASE+'/license/','creditText':'iconsforfree — Line 01','creator':{'@type':'Organization','name':'iconsforfree'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Icons','item':BASE+'/'},{'@type':'ListItem','position':2,'name':i['category'],'item':BASE+'/categories/'+slugify(i['category'])+'/'},{'@type':'ListItem','position':3,'name':i['name'],'item':BASE+path}]}]}
 write(path.strip('/')+'/index.html',page(f'{i["name"]} SVG icon — free download | iconsforfree',i['description']+' Download free SVG, customize color and stroke width.',path,'<div class="shell">'+body+'</div>',structured))
for name,title,desc in [('guide','How to use and customize SVG icons','Learn to download, embed and customize original Line 01 icons.'),('license','CC0 1.0 public domain icons','Original Line 01 icons are dedicated to the public domain under CC0 1.0. Copy, modify and redistribute them without attribution.'),('imprint','Imprint / Impressum','Provider information and contact details for Icons for free, operated by Andreas Dittes in Berlin.')]:
 content=(ROOT/f'templates/{name}.html').read_text()
 write(name+'/index.html',page(title+' | iconsforfree',desc,'/'+name+'/',f'<main id="main" class="prose">{content}</main>'))
for cat in ROADMAP['categories']:
 for item in cat['icons']:
  item['status']='available' if any(i['slug']==item['slug'] for i in ICONS) else 'planned'
write('data/icon-roadmap.json',json.dumps(ROADMAP,indent=2))
write('404.html',page('Page not found | iconsforfree','This icon or page is not in the collection.','/404.html','<main id="main" class="prose"><h1>This one is missing.</h1><p>The page may have moved, or the icon is not available yet.</p><a class="btn" href="/">Browse all icons</a></main>').replace('<meta name="description"','<meta name="robots" content="noindex"><meta name="description"'))
sitemap='<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">'
for url in urls:
 image=''
 if url.startswith('/icons/'):
  slug=url.split('/')[2];image=f'<image:image><image:loc>{BASE}/icons/{slug}.svg</image:loc></image:image>'
 sitemap+=f'<url><loc>{BASE}{url}</loc>{image}</url>'
write('sitemap.xml',sitemap+'</urlset>')
write('robots.txt','User-agent: *\nAllow: /\nSitemap: '+BASE+'/sitemap.xml')
write('.nojekyll','')
print(f'Built {len(ICONS)} validated SVGs, {len(categories)} categories, and {len(urls)} indexable pages.')

# Only allowlisted public assets go into the deployment folder.
public=ROOT/'dist'
if public.exists():shutil.rmtree(public)
public.mkdir()
for path in PUBLIC_FILES | {'styles.css','tokens.css','app.js','CNAME','LICENSE-ICONS','assets/social/preview.png'}:
 target=public/path;target.parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(ROOT/path,target)
print('Public-only deployment output: dist/ (project prompts, roadmap and docs excluded).')
