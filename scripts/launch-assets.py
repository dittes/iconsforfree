#!/usr/bin/env python3
"""Create editable, deterministic launch artwork from the real icon library."""
from pathlib import Path
from html import escape
import json
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'launch/product-hunt';OUT.mkdir(parents=True,exist_ok=True)
icons={i['slug']:i for i in json.loads((ROOT/'data/icons.json').read_text())}
N=f'{len(icons):,}'
P={'paper':'#F8FAFF','white':'#FFFFFF','ink':'#253047','muted':'#596579','line':'#DCE3EF','blue':'#2455DB','soft':'#EAF0FF','green':'#287461','rose':'#BC5368'}
def rect(x,y,w,h,fill='white',rad=0,stroke=None):return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rad}" fill="{P.get(fill,fill)}"'+(f' stroke="{P.get(stroke,stroke)}"' if stroke else '')+'/>'
def text(x,y,s,size=24,color='ink',weight=400,family='Arial',spacing=None):return f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" font-weight="{weight}" fill="{P.get(color,color)}"'+(f' letter-spacing="{spacing}"' if spacing else '')+'>'+escape(s)+'</text>'
def line(x,y,x2,y2,color='line'):return f'<path d="M{x} {y}H{x2}" stroke="{P.get(color,color)}"/>' if y==y2 else f'<path d="M{x} {y}L{x2} {y2}" stroke="{P.get(color,color)}"/>'
def icon(slug,x,y,size=48,color='ink',weight=1.75):return f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" color="{P.get(color,color)}" stroke="currentColor" stroke-width="{weight}" stroke-linecap="round" stroke-linejoin="round">{icons[slug]["body"]}</svg>'
def brand(y=54,dark=False):
 col='white' if dark else 'blue';s=''
 for x,yy in [(56,y-22),(74,y-22),(56,y-4),(74,y-4)]:s+=rect(x,yy,11,11,col,2)
 return s+text(101,y+3,'iconsforfree.com',23,'white' if dark else 'ink',700)
def foot(n,dark=False):return line(56,693,1214,693,'#5E83E6' if dark else 'line')+text(56,725,'LINE 01  /  ORIGINAL SVG ICONS',13,'white' if dark else 'muted',400,'Arial',1.4)+text(1153,725,f'0{n} / 05',13,'white' if dark else 'muted',400,'Arial',1)
def svg(content,w=1270,h=760,bg='paper'):return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><!-- Hallmark pre-emit: P5 H5 E4 S5 R5 V4 -->'+rect(0,0,w,h,bg)+content+'</svg>'
def save(name,s): (OUT/(name+'.svg')).write_text(s)
# 01 — collection cover; the same composition is adapted to social aspect ratio below.
def cover(w=1270,h=760):
 social=h==630;head=210 if social else 240;s=brand()
 s+=text(56,head-66,f'{N} ORIGINAL ICONS. FREE UNDER CC0.',13,'blue',700,spacing=1)
 s+=text(52,head,'Small icons.',66,'ink',700,spacing=-2)+text(52,head+77,'Big freedom.',66,'blue',700,spacing=-2)
 s+=text(56,head+141,'Original SVG icons you can make your own.',22,'muted')
 s+=text(56,head+176,'Change the color. Find your weight. Ship it.',22,'muted')
 s+=rect(56,head+221,171,45,'blue',7)+text(78,head+250,'Free under CC0',18,'white',700)
 s+=text(56,head+313,'SVG + PNG    /    30 CATEGORIES    /    NO SIGNUP',12,'muted',700,spacing=.8)
 selected=['ai','home','desktop','heart','phone-call','headphones','leaf','camera','rocket','code','globe','gamepad','coffee','cloud-sun','fingerprint','graduation-cap','neural-network','windows','paw','sparkles']
 selected[-1]='star'
 tile=106 if social else 104;gap=12;startx=w-4*(tile+gap)-34;starty=91 if social else 100
 for n,slug in enumerate(selected):
  x=startx+(n%4)*(tile+gap);y=starty+(n//4)*(tile+gap)
  if social and n>=16:break
  blue=n in [0,7,14];s+=rect(x,y,tile,tile,'blue' if blue else 'white',12,None if blue else 'line')
  s+=icon(slug,x+(tile-48)/2,y+(tile-48)/2,48,'white' if blue else 'ink')
 if not social:s+=foot(1)
 else:s+=line(56,590,w-56,590)+text(56,615,'FREE ICONS FOR YOUR NEXT WEBSITE, APP OR SIDE PROJECT.',12,'muted',700,spacing=1)
 return svg(s,w,h)
save('01-collection',cover())
(ROOT/'assets/social/preview.svg').write_text(cover(1200,630))
# 02 — real geometry shown with supported customization settings.
s=brand()+text(56,151,'One icon. Your own style.',54,'ink',700,spacing=-1.5)+text(56,194,'Editable strokes, colors and backgrounds. Every icon stays in the family.',23,'muted')
for j,(color,weight,name,hex_) in enumerate([('blue',1,'Light / 1.0','#2455DB'),('green',1.75,'Regular / 1.75','#287461'),('rose',2.5,'Bold / 2.5','#BC5368')]):
 x=56+j*392;s+=rect(x,238,374,359,'white',12,'line')+rect(x+24,262,326,221,'soft' if j==0 else '#F0F6F3' if j==1 else '#FCF2F4',8)
 s+=icon('home',x+115,303,144,color,weight)+text(x+24,527,name,24,'ink',700)+rect(x+24,551,17,17,color,8)+text(x+52,566,hex_,16,'muted',400,'Menlo')
s+=text(56,649,'Same 24 × 24 grid. Three weights shown. One consistent collection.',20,'muted')+foot(2);save('02-customization',svg(s))
# 03 — catalogue breadth, with authentic original pictograms.
s=brand()+text(56,151,'From AI to everyday.',54,'ink',700,spacing=-1.5)+text(56,194,'30 categories. A shared visual language for your whole project.',23,'muted')
sections=[('AI & technology',['ai-chip','desktop','neural-network','phone-scan']),('Work & communication',['mail','calendar','task','message']),('Nature & everyday life',['leaf','coffee','paw','home']),('Travel & transport',['plane','globe','bicycle','suitcase']),('Design & development',['pen-tool','code','palette','app-window']),('Commerce & finance',['cart','credit-card','store','piggy-bank'])]
for n,(name,slugs) in enumerate(sections):
 x=56+(n%3)*392;y=238+(n//3)*202;s+=rect(x,y,374,182,'white',10,'line')+text(x+23,y+39,name,21,'ink',700)
 for j,slug in enumerate(slugs):s+=icon(slug,x+22+j*88,y+80,49,'blue' if j==0 else 'ink')
s+=foot(3);save('03-categories',svg(s))
# 04 — plain developer example, no fabricated browser chrome or UI.
s=brand()+text(56,200,'Ready for',62,'ink',700,spacing=-2)+text(56,273,'your next build.',62,'blue',700,spacing=-2)
s+=text(56,333,'Copy SVG. Download PNG.',25,'muted')+text(56,370,'Or embed a direct icon URL.',25,'muted')
for y,a,b in [(445,'SVG','Sharp at every size'),(515,'PNG','Exports up to 2048 px'),(585,'URL','Direct links for your project')]:s+=text(56,y,a,25,'blue',700)+text(141,y,b,23,'ink')
s+=rect(662,137,552,483,'ink',12)+icon('code',697,171,46,'#AFC4FF')+text(697,261,'<img',26,'#AFC4FF',400,'Menlo')
for y,t in [(307,'  src="https://iconsforfree.com/icons/home.svg"'),(367,'  width="24" height="24"'),(427,'  alt="Home"'),(487,'/>')]:s+=text(687,y,t,18,'white',400,'Menlo')
s+=text(697,570,'No package. No account.',20,'#BBC7DF')+foot(4);save('04-developer-ready',svg(s))
# 05 — license message; accurate scope is the icon artwork, not third-party rights.
s=brand(dark=True)+text(56,170,'Free means free.',62,'white',700,spacing=-2)
s+=text(51,377,'CC0',183,'white',700,spacing=-9)+text(57,426,'PUBLIC DOMAIN DEDICATION',15,'white',700,spacing=2)
s+=text(663,264,'Personal projects.',35,'white',700)+text(663,320,'Commercial projects.',35,'white',700)+text(663,396,'No attribution required.',26,'white')+text(663,438,'Copy, modify and redistribute.',26,'white')
for n,slug in enumerate(['heart','rocket','code','palette','globe','coffee','ai','leaf']):s+=icon(slug,64+n*150,552,56,'white',1.5)
s+=foot(5,True);save('05-cc0',svg(s,bg='blue'))
# Separate square thumbnail for the Product Hunt listing.
s=''
for x,y in [(58,58),(132,58),(58,132),(132,132)]:s+=rect(x,y,50,50,'white',9)
save('thumbnail',svg(s,240,240,'blue'))
print('Created five editable gallery SVGs, a square thumbnail and the social SVG.')
