#!/usr/bin/env python3
"""Render a repeatable contact sheet for visual review of SVG weights."""
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
icons=json.loads((root/'data/icons.json').read_text())
new=set(json.loads((root/'data/new-icon-slugs.json').read_text()))
for filename,items in [('icon-proof',icons),('new-icons-proof',[i for i in icons if i['slug'] in new])]:
 rows=[]
 for i in items:
  previews=''.join(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{i["body"]}</svg>' for w in [1,1.75,2.5])
  rows.append(f'<div class="sample"><span>{i["slug"]}</span><div class="weights">{previews}</div></div>')
 (root/f'docs/{filename}.html').write_text('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><meta name="robots" content="noindex"><title>Line 01 weight proof</title><link rel="stylesheet" href="/tokens.css"><style>body{margin:32px;background:var(--color-paper);color:var(--color-ink);font-family:var(--font-body)}h1{font-family:var(--font-display)}.proof{display:grid;grid-template-columns:repeat(6,minmax(0,1fr));gap:16px}.sample{padding:16px;border:1px solid var(--color-rule);border-radius:6px}.sample span{font-size:12px}.weights{display:flex;justify-content:space-between;gap:8px;margin-top:16px}svg{width:28px;height:28px}@media(max-width:600px){.proof{grid-template-columns:repeat(2,minmax(0,1fr))}}</style></head><body><h1>Line 01 · '+str(len(items))+' icon weight proof</h1><p>Each icon at 1 / 1.75 / 2.5 stroke units. Same geometry, same grid.</p><div class="proof">'+''.join(rows)+'</div></body></html>')
