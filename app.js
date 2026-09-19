/* Dependency-free catalogue and SVG customizer. Geometry is validated at build time. */
(() => {
 'use strict';
 const icons = window.ICON_LIBRARY || [];
 const $ = s => document.querySelector(s);
 const escape = value => String(value).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
 const directURL = icon => `https://iconsforfree.com/icons/${icon.slug}.svg`;
 const defaults = {color:'#253047', background:'#eef2ff', transparent:true, stroke:1.75, size:24};
 let settings = {...defaults};
 const main = $('#main');
 const catalogue = $('#icon-grid');
 const initialCategory = main?.dataset.category || 'All icons';
 let category = initialCategory;
 let selected = icons.find(i => i.slug === main?.dataset.icon) || icons.find(i => category === 'All icons' || i.category === category) || icons[0];
 const matches = (icon, query) => {
  const text = [icon.name, icon.slug, icon.category, ...icon.tags].join(' ').toLowerCase();
  const terms = text.split(/[^a-z0-9]+/);
  return query.toLowerCase().trim().split(/\s+/).filter(Boolean).every(word => word.length <= 2 ? terms.includes(word) : text.includes(word));
 };
 const hex = value => /^#[0-9a-f]{6}$/i.test(value);
 const status = (message, state='success') => { const node=$('#action-status'); if(node){node.textContent=message; node.dataset.state=state;} };
 function svg(icon, opts={}, decorative=false) {
  const {size=24, stroke=1.75, color='currentColor', background=null}=opts;
  const bg=background ? `<rect width="24" height="24" x="0" y="0" fill="${background}" stroke="none"/>` : '';
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${size}" height="${size}" viewBox="0 0 24 24" fill="none" stroke="${color}" stroke-width="${stroke}" stroke-linecap="round" stroke-linejoin="round"${decorative?' aria-hidden="true"':''}>${bg}${icon.body}</svg>`;
 }
 function exportSVG() { return svg(selected,{...settings, background:settings.transparent?null:settings.background}); }
 function selectIcon(icon, scroll=false) {
  selected=icon;
  $('#selected-name').textContent=icon.name;
  $('#direct-url').value=directURL(icon);
  $('#selected-category').textContent=`${icon.category} / Line 01`;
  $('#detail-link').href=`/icons/${icon.slug}/`;
  $('#detail-link').setAttribute('aria-label',`Open ${icon.name} icon details`);
  renderPreview();
  document.querySelectorAll('.icon-card').forEach(el => {el.classList.toggle('selected',el.dataset.slug===icon.slug); if(el.dataset.slug===icon.slug)el.setAttribute('aria-current','true');else el.removeAttribute('aria-current');});
  if(scroll && matchMedia('(max-width: 1023px)').matches) $('#customizer').scrollIntoView({block:'start',behavior:'instant'});
 }
 function renderPreview() {
  // Display at a constant inspection size; exports use the user's chosen dimensions.
  $('#preview').innerHTML=svg(selected,{...settings,size:80,background:settings.transparent?null:settings.background},true);
  $('#stroke-output').textContent=settings.stroke;
  $('#background-color').disabled=settings.transparent;
  $('#background-hex').disabled=settings.transparent;
  // Apply color and weight to every catalogue icon without changing card labels.
  document.querySelectorAll('.icon-card svg').forEach(el=>{el.setAttribute('stroke',settings.color);el.setAttribute('stroke-width',settings.stroke);});
 }
 function renderGrid(updateURL=true) {
  const query=$('#icon-search').value;
  let result=icons.filter(i=>(category==='All icons'||i.category===category)&&matches(i,query));
  const order=$('#sort').value;
  if(order!=='collection')result.sort((a,b)=>a.name.localeCompare(b.name)*(order==='az'?1:-1));
  catalogue.innerHTML=result.map(i=>`<a class="icon-card${i.slug===selected.slug?' selected':''}" href="/icons/${i.slug}/" data-slug="${i.slug}" aria-label="Customize ${escape(i.name)} icon"${i.slug===selected.slug?' aria-current="true"':''}>${svg(i,{color:settings.color,stroke:settings.stroke},true)}<span>${escape(i.name)}</span></a>`).join('');
  $('#result-count').textContent=`${result.length} icon${result.length===1?'':'s'}`;
  $('#category-heading').textContent=category;
  $('#empty-state').hidden=result.length>0;
  $('#clear-search').hidden=!query;
  document.querySelectorAll('.category-nav a').forEach(a=>{const active=a.dataset.category===category;a.classList.toggle('active',active);if(active)a.setAttribute('aria-current','page');else a.removeAttribute('aria-current');});
  if(updateURL){const url=new URL(location.href);query?url.searchParams.set('q',query):url.searchParams.delete('q');category!==initialCategory?url.searchParams.set('category',category):url.searchParams.delete('category');order!=='collection'?url.searchParams.set('sort',order):url.searchParams.delete('sort');history.replaceState({},'',url);}
 }
 if(catalogue) {
  const params=new URLSearchParams(location.search);
  $('#icon-search').value=params.get('q')||'';
  const requested=params.get('category');if(requested==='All icons'||icons.some(i=>i.category===requested))category=requested;
  if(['az','za'].includes(params.get('sort')))$('#sort').value=params.get('sort');
  $('#icon-search').addEventListener('input',()=>renderGrid());
  $('#sort').addEventListener('change',()=>renderGrid());
  const reset=()=>{$('#icon-search').value='';category='All icons';renderGrid();$('#icon-search').focus();};
  $('#clear-search').addEventListener('click',()=>{$('#icon-search').value='';renderGrid();$('#icon-search').focus();});
  $('#reset-search').addEventListener('click',reset);
  catalogue.addEventListener('click',e=>{const a=e.target.closest('[data-slug]');if(!a||e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();selectIcon(icons.find(i=>i.slug===a.dataset.slug),true);status(`${selected.name} selected.`);});
  document.querySelectorAll('.category-nav a').forEach(a=>a.addEventListener('click',e=>{if(e.metaKey||e.ctrlKey||e.shiftKey||e.altKey)return;e.preventDefault();category=a.dataset.category;renderGrid();}));
  renderGrid(false);
 }
 async function copy(text,button,message) {
  try {
   if(!navigator.clipboard?.writeText)throw Error('Clipboard unavailable');
   button.disabled=true;button.setAttribute('aria-busy','true');
   await navigator.clipboard.writeText(text);status(message);button.dataset.state='success';
  } catch {
   // A focused, selectable fallback also works in insecure or permission-denied contexts.
   let fallback=$('#copy-fallback');
   if(!fallback){fallback=document.createElement('textarea');fallback.id='copy-fallback';fallback.className='hex-field';fallback.rows=4;fallback.readOnly=true;fallback.setAttribute('aria-label','Copy this content manually');$('#action-status').after(fallback);}
   fallback.value=text;fallback.focus();fallback.select();status('Clipboard unavailable. Select and copy the text below.','error');
  } finally {button.disabled=false;button.removeAttribute('aria-busy');}
 }
 function download(blob,name) {
  const url=URL.createObjectURL(blob),a=document.createElement('a');a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),30000);
 }
 if($('#customizer')&&selected) {
  const syncControls=()=>{
   $('#stroke-color').value=settings.color;$('#stroke-hex').value=settings.color;
   $('#background-color').value=settings.background;$('#background-hex').value=settings.background;
   $('#stroke-width').value=settings.stroke;$('#icon-size').value=settings.size;$('#size-number').value=settings.size;$('#transparent').checked=settings.transparent;
   document.querySelectorAll('[aria-invalid=true]').forEach(el=>el.removeAttribute('aria-invalid'));
   renderPreview();
  };
  [['stroke','color'],['background','background']].forEach(([prefix,key])=>{
   $('#'+prefix+'-color').addEventListener('input',e=>{settings[key]=e.target.value;$('#'+prefix+'-hex').value=e.target.value;$('#'+prefix+'-hex').removeAttribute('aria-invalid');renderPreview();});
   $('#'+prefix+'-hex').addEventListener('input',e=>{const valid=hex(e.target.value);e.target.setAttribute('aria-invalid',String(!valid));if(valid){settings[key]=e.target.value;$('#'+prefix+'-color').value=e.target.value;renderPreview();status('Color updated.');}else status('Enter a six-digit hex color, such as #2455db.','error');});
  });
  document.querySelectorAll('[data-color]').forEach(el=>el.addEventListener('click',()=>{settings.color=el.dataset.color;$('#stroke-color').value=settings.color;$('#stroke-hex').value=settings.color;$('#stroke-hex').removeAttribute('aria-invalid');renderPreview();}));
  $('#stroke-width').addEventListener('input',e=>{settings.stroke=Number(e.target.value);renderPreview();});
  const setSizeValidity = valid => {
   $('#size-number').setAttribute('aria-invalid',String(!valid));
   for(const id of ['#download-svg','#download-png','#copy-svg']) $(id).disabled=!valid;
  };
  $('#icon-size').addEventListener('input',e=>{
   settings.size=Number(e.target.value);$('#size-number').value=settings.size;setSizeValidity(true);renderPreview();status(`Export size set to ${settings.size} × ${settings.size} pixels.`);
  });
  $('#size-number').addEventListener('input',e=>{
   const value=Number(e.target.value);
   const valid=e.target.value!==''&&Number.isInteger(value)&&value>=16&&value<=2048;
   setSizeValidity(valid);
   if(!valid){status('Enter a whole-number size from 16 to 2048 pixels.','error');return;}
   settings.size=value;$('#icon-size').value=value;
   status(`Export size set to ${value} × ${value} pixels.`);
  });
  $('#transparent').addEventListener('change',e=>{settings.transparent=e.target.checked;renderPreview();});
  $('#reset').addEventListener('click',()=>{settings={...defaults};setSizeValidity(true);syncControls();$('#copy-fallback')?.remove();status('Default style restored.');});
  $('#back-to-icons').addEventListener('click',()=>{const card=document.querySelector('.icon-card.selected')||document.querySelector('.icon-card');if(card){card.scrollIntoView({block:'center'});card.focus({preventScroll:true});}else location.href='/';});
  $('#copy-svg').addEventListener('click',e=>copy(exportSVG(),e.currentTarget,'SVG copied. Ready to paste.'));
  $('#copy-link').addEventListener('click',e=>copy(directURL(selected),e.currentTarget,'Default SVG link copied. Custom colors are in your downloads.'));
  $('#copy-embed').addEventListener('click',e=>copy(`<img src="${directURL(selected)}" width="24" height="24" alt="${escape(selected.name)}">`,e.currentTarget,'HTML embed copied. Uses the original SVG at 24 pixels.'));
  $('#direct-url').addEventListener('click',e=>e.target.select());
  $('#download-svg').addEventListener('click',()=>{download(new Blob([exportSVG()],{type:'image/svg+xml;charset=utf-8'}),`${selected.slug}.svg`);status('SVG download started.');});
  $('#download-png').addEventListener('click',async e=>{
   const button=e.currentTarget;button.disabled=true;button.setAttribute('aria-busy','true');status('Preparing PNG…');
   const slug=selected.slug,size=settings.size,source=exportSVG();
   const url=URL.createObjectURL(new Blob([source],{type:'image/svg+xml'}));
   try {
    const img=new Image();img.src=url;await img.decode();
    const canvas=document.createElement('canvas');canvas.width=size;canvas.height=size;
    const ctx=canvas.getContext('2d');if(!ctx)throw Error('Canvas unavailable');ctx.drawImage(img,0,0,size,size);
    const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw Error('PNG generation failed');
    download(blob,`${slug}-${size}px.png`);status(`PNG download started at ${size} × ${size} px.`);
   }catch{status('PNG export failed. Please try downloading the SVG.','error');}
   finally{URL.revokeObjectURL(url);button.disabled=false;button.removeAttribute('aria-busy');}
  });
  selectIcon(selected);
 }
 // Share the clean production URL; filters and local preview URLs are never published.
 const shareButton=$('#share-collection');
 if(shareButton){
  shareButton.hidden=false;
  shareButton.addEventListener('click',async()=>{
   const url='https://iconsforfree.com/';
   const feedback=$('#share-status');
   feedback.textContent='';$('#share-fallback').hidden=true;
   if(navigator.share){
    try{await navigator.share({title:'Icons for free',text:'Original SVG icons. Customize, download and use freely under CC0.',url});return;}
    catch(error){if(error.name==='AbortError')return;}
   }
   try{await navigator.clipboard.writeText(url);feedback.textContent='Collection link copied.';}
   catch{const field=$('#share-fallback');field.hidden=false;field.focus();field.select();feedback.textContent='Select and copy the link below.';}
  });
 }
 // Native dialog supplies focus containment, Escape handling, and background inertness.
 const dialog=$('#search-dialog'),input=$('#command-input'),results=$('#command-results');
 let returnFocus;
 function searchCommands() {
  const result=icons.filter(i=>matches(i,input.value)).slice(0,8);
  results.innerHTML=result.length?result.map(i=>`<a href="/icons/${i.slug}/">${svg(i,{},true)}<span>${escape(i.name)}</span><span>${escape(i.category)}</span></a>`).join(''):'<p class="status">No matching icons. Try “home” or “arrow”.</p>';
 }
 function openSearch(){returnFocus=document.activeElement;input.value='';searchCommands();dialog.showModal();input.focus();}
 $('#open-search')?.addEventListener('click',openSearch);
 $('#close-search')?.addEventListener('click',()=>dialog.close());
 dialog?.addEventListener('close',()=>returnFocus?.focus({preventScroll:true}));
 dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
 input?.addEventListener('input',searchCommands);
 dialog?.addEventListener('keydown',e=>{
  const items=[...results.querySelectorAll('a')],index=items.indexOf(document.activeElement);
  if(e.key==='ArrowDown'||e.key==='ArrowUp'){e.preventDefault();if(!items.length)return;const next=e.key==='ArrowDown'?Math.min(index+1,items.length-1):(index<=0?-1:index-1);(next<0?input:items[next]).focus();}
  if(e.key==='Enter'&&document.activeElement===input&&items[0]){e.preventDefault();items[0].click();}
 });
 document.addEventListener('keydown',e=>{if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='k'){e.preventDefault();dialog.open?dialog.close():openSearch();}});
})();
