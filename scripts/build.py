#!/usr/bin/env python3
"""Generate a dependency-free static site from reviewed icon data. Python 3.10+."""
from pathlib import Path
import json, re, html, xml.etree.ElementTree as ET
from string import Template
from urllib.parse import quote
ROOT=Path(__file__).resolve().parents[1]
BASE='https://iconsforfree.com'
ICONS=json.loads((ROOT/'data/icons.json').read_text())
ROADMAP=json.loads((ROOT/'data/icon-roadmap.json').read_text())
E=html.escape
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
 target=ROOT/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(content+'\n')
def card(i):
 return f'<a class="icon-card" href="/icons/{i["slug"]}/" data-slug="{i["slug"]}" aria-label="Customize {E(i["name"])} icon">{svg(i)}<span>{E(i["name"])}</span></a>'
def inspector(i):
 return f'''<aside class="inspector" id="customizer" aria-label="Icon customizer">
 <button class="text-button back-to-icons" id="back-to-icons" type="button">← Back to icons</button><div class="inspector-top"><div><h2 id="selected-name">{E(i['name'])}</h2><p id="selected-category">{E(i['category'])} / Line 01</p></div><a class="icon-button" id="detail-link" href="/icons/{i['slug']}/" aria-label="Open icon details">{glyph('external-link')}</a></div>
 <div class="preview-stage" id="preview">{svg(i,80)}</div><div class="preview-meta"><span>24 × 24 grid</span><span>SVG · editable stroke</span></div>
 <div class="controls"><div><label class="field-label" for="stroke-color">Stroke color <button class="text-button" id="reset" type="button">Reset</button></label><div class="color-field"><input type="color" id="stroke-color" value="#253047" aria-label="Stroke color picker"><input class="hex-field" id="stroke-hex" value="#253047" aria-label="Stroke color hex" maxlength="7" spellcheck="false"><div class="swatches"><button class="swatch" data-color="#253047" aria-label="Charcoal stroke" style="--swatch:var(--color-ink)"></button><button class="swatch" data-color="#2455db" aria-label="Cobalt stroke" style="--swatch:var(--color-accent)"></button></div></div></div>
 <div><label class="field-label" for="stroke-width">Stroke width <output id="stroke-output" for="stroke-width">1.75</output></label><input id="stroke-width" type="range" min="1" max="2.5" step="0.25" value="1.75"><div class="range-labels"><span>Light</span><span>Bold</span></div></div>
 <div><label class="field-label" for="icon-size">Export size <output id="size-output" for="icon-size">24 px</output></label><input id="icon-size" type="range" min="16" max="128" step="4" value="24"><div class="range-labels"><span>16 px</span><span>128 px</span></div></div>
 <div><label class="field-label" for="background-color">Background</label><div class="color-field"><input id="background-color" type="color" value="#eef2ff" aria-label="Background color picker" disabled><input class="hex-field" id="background-hex" value="#eef2ff" aria-label="Background color hex" maxlength="7" spellcheck="false" disabled></div><label class="check-label"><input type="checkbox" id="transparent" checked>Transparent background</label></div>
 <div class="actions"><button class="btn primary" id="download-svg">{glyph('download')}Download SVG</button><div class="action-row"><button class="btn" id="copy-svg">{glyph('code')}Copy SVG</button><button class="btn" id="download-png">PNG</button></div><button class="text-button direct-link" id="copy-link">Copy direct SVG link ↗</button><p id="action-status" class="status" role="status" aria-live="polite">Select an icon. Make it yours.</p></div></div>
 <div class="inspector-foot"><span>Free for every project</span><a href="/license/">License ↗</a></div></aside>'''
def nav():
 return f'''<a class="skip" href="#main">Skip to content</a><header class="topbar"><div class="shell topbar-inner"><a class="brand" href="/" aria-label="Icons for free home"><svg width="28" height="28" viewBox="0 0 28 28" fill="none" aria-hidden="true"><rect x="2" y="2" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/><rect x="17" y="2" width="9" height="9" rx="2" fill="currentColor"/><rect x="2" y="17" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/><rect x="17" y="17" width="9" height="9" rx="2" stroke="currentColor" stroke-width="2"/></svg><span>iconsforfree<span class="dotcom">.com</span></span></a><button class="search-trigger" id="open-search">{glyph('search')}<span>Find an icon…</span><kbd>⌘ K</kbd></button><nav class="nav-links" aria-label="Main navigation"><a href="/">Icons</a><a href="/guide/">How to use</a><a href="/roadmap/">The collection</a></nav></div></header>'''
def footer():
 return '<footer class="shell"><span>Small details. Better interfaces.</span><nav aria-label="Footer"><a href="/data/icon-generation.json">Icon prompt ↗</a><a href="/license/">License</a><a href="/roadmap/">Roadmap</a><span>© 2026 iconsforfree</span></nav></footer>'
def dialog():
 return f'''<dialog id="search-dialog" aria-labelledby="command-title"><div class="dialog-head"><h2 id="command-title">Find your next icon</h2><button class="icon-button" id="close-search" aria-label="Close search">{glyph('close')}</button></div><label class="search-box">{glyph('search')}<input id="command-input" type="search" placeholder="Search icons and synonyms…" aria-label="Search all icons" autocomplete="off"></label><div class="command-results" id="command-results"></div><p class="dialog-hint">↑ ↓ to move · Enter to open · Escape to close</p></dialog>'''
def page(title,desc,path,body,structured=None):
 canonical=BASE+path
 schema=f'<script type="application/ld+json">{json.dumps(structured).replace("<","\\u003c")}</script>' if structured else ''
 return f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{E(title)}</title><meta name="description" content="{E(desc)}"><link rel="canonical" href="{canonical}"><meta property="og:type" content="website"><meta property="og:title" content="{E(title)}"><meta property="og:description" content="{E(desc)}"><meta property="og:url" content="{canonical}"><meta name="theme-color" content="#f8faff"><link rel="icon" href="/assets/favicon.svg" type="image/svg+xml"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400&family=Space+Grotesk:wght@400;500;600&display=swap" rel="stylesheet"><link rel="stylesheet" href="/styles.css">{schema}<script src="/assets/icons-data.js" defer></script><script src="/app.js" defer></script></head><body>{nav()}{body}{footer()}{dialog()}</body></html>'''
def catalogue(category=None):
 items=[i for i in ICONS if not category or i['category']==category]
 catnav=''
 for cat in ['All icons']+categories:
  count=len(ICONS) if cat=='All icons' else sum(i['category']==cat for i in ICONS)
  href='/' if cat=='All icons' else f'/categories/{slugify(cat)}/'
  symbol='grid' if cat=='All icons' else next(i['slug'] for i in ICONS if i['category']==cat)
  active=(cat==category or cat=='All icons' and not category)
  catnav+=f'<a href="{href}" data-category="{E(cat)}" class="{"active" if active else ""}"'+(' aria-current="page"' if active else '')+f'>{glyph(symbol)}<span>{E(cat)}</span><span class="count">{count}</span></a>'
 heading=f'{category} icons.' if category else 'Small icons. Endless possibilities.'
 return f'''<div class="shell"><section class="intro"><div><h1>{E(heading)}</h1><p>Original line icons for whatever you’re making. Customize, copy, and carry on.</p></div><div class="collection-note"><strong>Line 01 collection</strong>{len(ICONS)} icons · 24px grid · Free to use</div></section>
 <main id="main" class="workspace" data-category="{E(category or 'All icons')}"><aside class="sidebar"><div class="sidebar-title">Browse the collection</div><nav class="category-nav" aria-label="Icon categories">{catnav}</nav><div class="sidebar-bottom"><a href="/roadmap/">Explore the roadmap ↗</a><a href="/guide/#design">Our design principles ↗</a><p>One family.<br>A consistent point of view.<br>Room for your own style.</p></div></aside>
 <section class="catalogue" aria-label="Icon library"><noscript><p class="no-js">Choose an icon to open its page and download the original SVG. Enable JavaScript for customization.</p></noscript><label class="search-box">{glyph('search')}<input id="icon-search" type="search" placeholder="Search icons… try ‘arrow’ or ‘mail’" aria-label="Search this collection" autocomplete="off"><button class="clear-search" id="clear-search" aria-label="Clear search" hidden>{glyph('close')}</button></label><div class="results-head"><h2><span id="category-heading">{E(category or 'All icons')}</span> <span id="result-count" role="status">{len(items)} icons</span></h2><label><span class="sr-only" hidden>Sort icons</span><select id="sort" aria-label="Sort icons"><option value="collection">Collection order</option><option value="az">Name: A to Z</option><option value="za">Name: Z to A</option></select></label></div><div class="icon-grid" id="icon-grid">{''.join(card(i) for i in items)}</div><div class="empty-state" id="empty-state" hidden><h2>No icons found.</h2><p>Try a simpler word, like “mail”, “home”, or “arrow”.</p><button class="btn" id="reset-search">Clear filters</button></div><div class="catalogue-foot"><span>Same grid. Same stroke. Every icon belongs.</span><span>Click an icon to customize ↗</span></div></section>{inspector(items[0])}</main>
 <section class="use-strip"><div><h2>A little SVG. A lot of freedom.</h2><p>Change the color. Find your weight. Use it in a website, an app, or your next big idea.</p><a href="/guide/">A quick guide to using icons ↗</a></div><pre>&lt;svg viewBox="0 0 24 24"\n     fill="none"\n     stroke="currentColor"\n     stroke-width="1.75"&gt;\n  &lt;!-- Make it yours. --&gt;\n&lt;/svg&gt;</pre></section></div>'''
validate()
for i in ICONS:write(f'icons/{i["slug"]}.svg',svg(i,24,False))
write('assets/icons-data.js','window.ICON_LIBRARY = '+json.dumps(ICONS).replace('<','\\u003c')+';')
write('assets/favicon.svg','<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#2455db"/><path d="M8 8h6v6H8Zm10 0h6v6h-6ZM8 18h6v6H8Zm10 0h6v6h-6Z" fill="#f8faff"/></svg>')
write('index.html',page('Free SVG icons, made to be yours | iconsforfree',f'Browse {len(ICONS)} original outline icons. Customize stroke color, weight, size and background, then download SVG or PNG for free.','/',catalogue(),{'@context':'https://schema.org','@type':'WebSite','name':'iconsforfree','url':BASE+'/'}))
urls=['/','/guide/','/license/','/roadmap/']
for cat in categories:
 path=f'/categories/{slugify(cat)}/';urls.append(path)
 write(path.strip('/')+'/index.html',page(f'{cat} SVG icons — free downloads | iconsforfree',f'Browse original {cat.lower()} outline icons. Adjust colors and stroke weight, then download SVG or PNG.',path,catalogue(cat)))
for i in ICONS:
 path=f'/icons/{i["slug"]}/';urls.append(path)
 related=[j for j in ICONS if j['category']==i['category'] and j!=i][:5]
 body=Template((ROOT/'templates/icon.html').read_text()).substitute(slug=i['slug'],name=E(i['name']),lower_name=E(i['name'].lower()),category=E(i['category']),category_slug=slugify(i['category']),description=E(i['description']),tags=''.join(f'<a href="/?q={quote(t)}">{E(t)}</a>' for t in i['tags']),inspector=inspector(i),related=''.join(card(j) for j in related))
 structured={'@context':'https://schema.org','@graph':[{'@type':'ImageObject','name':i['name']+' SVG icon','description':i['description'],'contentUrl':BASE+f'/icons/{i["slug"]}.svg','url':BASE+path,'encodingFormat':'image/svg+xml','width':24,'height':24,'license':BASE+'/license/','acquireLicensePage':BASE+'/license/','creditText':'iconsforfree — Line 01','creator':{'@type':'Organization','name':'iconsforfree'}},{'@type':'BreadcrumbList','itemListElement':[{'@type':'ListItem','position':1,'name':'Icons','item':BASE+'/'},{'@type':'ListItem','position':2,'name':i['category'],'item':BASE+'/categories/'+slugify(i['category'])+'/'},{'@type':'ListItem','position':3,'name':i['name'],'item':BASE+path}]}]}
 write(path.strip('/')+'/index.html',page(f'{i["name"]} SVG icon — free download | iconsforfree',i['description']+' Download free SVG, customize color and stroke width.',path,'<div class="shell">'+body+'</div>',structured))
for name,title,desc in [('guide','How to use and customize SVG icons','Learn to download, embed and customize original Line 01 icons.'),('license','Free icon usage license','Use the original iconsforfree icons in personal and commercial projects.'),('roadmap','A collection with room to grow','Explore 760 icon concepts across 30 categories and download the generation prompt.')]:
 content=(ROOT/f'templates/{name}.html').read_text()
 if name=='roadmap':
  rows=''
  for cat in ROADMAP['categories']:
   entries=[]
   for item in cat['icons']:
    item['status']='available' if any(i['slug']==item['slug'] for i in ICONS) else 'planned'
    name_=item['slug'].replace('-',' ')
    entries.append(f'<a href="/icons/{item["slug"]}/">{E(name_)} ↗</a>' if item['status']=='available' else f'<span>{E(name_)}</span>')
   rows+=f'<details class="roadmap-category"><summary>{E(cat["name"])} · {len(cat["icons"])} concepts · Priority {cat["priority"]}</summary><p>{E(cat["rationale"])}</p><div class="roadmap-items">{"".join(entries)}</div></details>'
  content=content.replace('{{CATEGORIES}}',rows).replace('{{AVAILABLE}}',str(len(ICONS))).replace('{{CONCEPTS}}',str(sum(len(c['icons']) for c in ROADMAP['categories']))).replace('{{CATEGORY_COUNT}}',str(len(ROADMAP['categories'])))
 write(name+'/index.html',page(title+' | iconsforfree',desc,'/'+name+'/',f'<main id="main" class="prose">{content}</main>'))
write('data/icon-roadmap.json',json.dumps(ROADMAP,indent=2))
write('404.html',page('Page not found | iconsforfree','This icon or page is not in the collection.','/404.html','<main id="main" class="prose"><h1>This one is missing.</h1><p>The page may have moved, or the icon might still be on our roadmap.</p><a class="btn" href="/">Browse all icons</a></main>').replace('<meta name="description"','<meta name="robots" content="noindex"><meta name="description"'))
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
