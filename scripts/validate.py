#!/usr/bin/env python3
"""Validate published data, static links, image references, and SEO contracts."""
import json,re,struct,xml.etree.ElementTree as ET
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlparse,unquote
ROOT=Path(__file__).resolve().parents[1]
PUBLIC=ROOT/'dist'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.ids=set();self.h1=0;self.canonical=[];self.desc=[];self.images=[];self.inputs={};self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag in ('script','img') and a.get('src'):self.links.append(a['src'])
  if tag=='link' and a.get('href') and a.get('rel') in ('stylesheet','icon'):self.links.append(a['href'])
  if tag=='link' and a.get('rel')=='canonical':self.canonical.append(a['href'])
  if tag=='meta' and a.get('name')=='description':self.desc.append(a.get('content',''))
  if tag=='img':self.images.append(a)
  if tag=='input' and a.get('id'):self.inputs[a['id']]=a
icons=json.loads((ROOT/'data/icons.json').read_text());roadmap=json.loads((ROOT/'data/icon-roadmap.json').read_text())
slugs={i['slug'] for i in icons};entries=[i for c in roadmap['categories'] for i in c['icons']]
assert len(slugs)==len(icons)
assert len({i['slug'] for i in entries})==len(entries)
assert slugs<={i['slug'] for i in entries}
assert all((i['status']=='available')==(i['slug'] in slugs) for i in entries)
assert {c['name'] for c in roadmap['categories']}>={i['category'] for i in icons}
pages=list(PUBLIC.rglob('*.html'))
assert not any((PUBLIC/p).exists() for p in ['data','docs','templates','scripts','roadmap'])
parsed={p:Page(p.read_text()) for p in pages}
for path,doc in parsed.items():
 assert '↗' not in path.read_text() and '/roadmap/' not in path.read_text() and '/data/icon-generation.json' not in path.read_text(),path
 assert doc.h1==1,(path,'h1')
 assert len(doc.canonical)==1 and doc.canonical[0].startswith('https://iconsforfree.com/'),path
 assert len(doc.desc)==1 and doc.desc[0],path
 if 'icon-size' in doc.inputs:
  for field in ['icon-size','size-number']:
   assert doc.inputs[field]['min']=='16' and doc.inputs[field]['max']=='2048' and doc.inputs[field]['step']=='1',(path,field,'export range')
 for url in doc.links:
  u=urlparse(url)
  if u.scheme or u.netloc:continue
  target=(PUBLIC/unquote(u.path).lstrip('/')) if u.path.startswith('/') else (path.parent/unquote(u.path)) if u.path else path
  if target.is_dir():target=target/'index.html'
  assert target.exists(),(path,url,'broken link')
  if u.fragment and target.suffix=='.html':assert u.fragment in parsed.get(target,Page(target.read_text())).ids,(path,url,'missing fragment')
 for img in doc.images:assert img.get('alt') and img.get('width') and img.get('height'),path
for i in icons:
 source=PUBLIC/f'icons/{i["slug"]}.svg';tree=ET.fromstring(source.read_text())
 assert tree.get('stroke')=='currentColor' and tree.get('viewBox')=='0 0 24 24'
 assert tree.get('fill')=='none' and tree.get('stroke-width')=='1.75'
 assert all(child.get('stroke') is None and child.get('stroke-width') is None for child in tree)
 path=PUBLIC/f'icons/{i["slug"]}/index.html';text=path.read_text()
 schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',text).group(1))
 assert schema['@graph'][0]['contentUrl'].endswith(f'/icons/{i["slug"]}.svg')
 assert i['description'] in text
sitemap=ET.fromstring((PUBLIC/'sitemap.xml').read_text())
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9','i':'http://www.google.com/schemas/sitemap-image/1.1'}
assert len(sitemap.findall('s:url',ns))==len(pages)-1
assert len(sitemap.findall('.//i:image',ns))==len(icons)
print(f'PASS: {len(icons)} SVG contracts, {len(entries)} unique roadmap concepts, {len(pages)} HTML pages and their local links, {len(icons)} ImageObject/breadcrumb records, sitemap and image references.')
