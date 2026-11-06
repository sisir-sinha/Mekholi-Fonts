/* Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
   SIL OFL 1.1 — https://openfontlicense.org/ — see mekholi-family/OFL.txt. */
'use strict';
(async () => {
 const $=id=>document.getElementById(id);
 const controls=['text','weight','style','size','leading','tracking','align','color','background'];
 const defaults={text:'মেখলি\nঅ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ\nক খ গ ঘ ঙ চ ছ জ ঝ ঞ\nর ৱ ৰ ক্ষ জ্ঞ কি কু\n০১২৩৪৫৬৭৮৯ · Mekholi',weight:'400',style:'normal',size:'48',leading:'1.75',tracking:'0',align:'left',color:'#193b35',background:'#fffef9'};
 const presets={name:'মেখলি\nMekholi',alphabet:'অ আ ই ঈ উ ঊ ঋ এ ঐ ও ঔ\nক খ গ ঘ ঙ চ ছ জ ঝ ঞ\nট ঠ ড ঢ ণ ত থ দ ধ ন\nপ ফ ব ভ ম য র ল শ ষ স হ\nড় ঢ় য় ৰ ৱ',marks:'কি কী কু কূ কৃ কে কৈ কো কৌ কং কঃ কঁ\nর্ক ক্র র্য ক্য ক্ষ জ্ঞ ত্র শ্র স্ত্র ন্দ্র ক্ত ন্ত ন্ধ ষ্ট ষ্ণ হ্ম\nক্ষ ক্ষি ক্ষী র্কি ক্রি জ্ঞা ত্রু শ্রু',numbers:'০১২৩৪৫৬৭৮৯\n0123456789\n৳ ১০০ · 2026',latin:'Mekholi\nThe quick brown fox jumps over the lazy dog.\nABCDEFGHIJKLMNOPQRSTUVWXYZ\nabcdefghijklmnopqrstuvwxyz\n0123456789'};
 let covered=null,coverageError=false,seq=0;
 function status(s){$('status').textContent=s;}
 function state(){return Object.fromEntries(controls.map(k=>[k,$(k).value]));}
 function set(s){for(const k of controls)$(k).value=s[k]??defaults[k];update();}
 function bounded(v,min,max,fallback){const n=Number(v);return Number.isFinite(n)?Math.min(max,Math.max(min,n)):fallback;}
 function sanitize(s){return {text:String(s.text??defaults.text).slice(0,20000),weight:/^[1-9]00$/.test(s.weight)?s.weight:'400',style:s.style==='italic'?'italic':'normal',size:String(bounded(s.size,16,120,48)),leading:String(bounded(s.leading,1,2.6,1.75)),tracking:String(bounded(s.tracking,-1,5,0)),align:['left','center','right'].includes(s.align)?s.align:'left',color:/^#[0-9a-f]{6}$/i.test(s.color)?s.color:defaults.color,background:/^#[0-9a-f]{6}$/i.test(s.background)?s.background:defaults.background};}
 function coverage(){
  if(!covered){$('coverage').textContent=coverageError?'Coverage data could not load. Use a web server and check assets/coverage.json.':'Loading character coverage…';return;}
  const unique=[...new Set([...$('text').value])];
  // Join controls are interpreted by the shaper, not standalone ink glyphs.
  const ignorable=new Set([9,10,13,0x200c,0x200d]);
  const missing=unique.filter(c=>!covered.has(c.codePointAt(0))&&!ignorable.has(c.codePointAt(0)));
  $('coverage').classList.toggle('warning',missing.length>0);
  $('coverage').textContent=missing.length?'Unmapped characters — may use fallback: '+missing.slice(0,24).map(c=>JSON.stringify(c)+' (U+'+c.codePointAt(0).toString(16).toUpperCase().padStart(4,'0')+')').join(', ')+(missing.length>24?' …':''):'All typed characters are directly mapped, or are supported whitespace/join controls. This is a cmap check, not linguistic or shaping certification.';
 }
 function css(s){return `.mekholi-sample {\n  font-family: 'Mekholi', serif;\n  font-weight: ${s.weight};\n  font-style: ${s.style};\n  font-size: ${s.size}px;\n  line-height: ${s.leading};\n  letter-spacing: ${s.tracking}px;\n  text-align: ${s.align};\n  color: ${s.color};\n  background: ${s.background};\n  font-synthesis: none;\n}`;}
 async function update(){
  const s=state(),el=$('preview');el.textContent=s.text;
  Object.assign(el.style,{fontWeight:s.weight,fontStyle:s.style,fontSize:s.size+'px',lineHeight:s.leading,letterSpacing:s.tracking+'px',textAlign:s.align,color:s.color,background:s.background});
  $('size-value').textContent=s.size+' px';$('leading-value').textContent=s.leading;$('tracking-value').textContent=s.tracking+' px';
  $('style-label').textContent=s.weight+' / '+(s.style==='italic'?'slanted italic':'upright');
  $('css-output').textContent=css(s);coverage();
  const thisSeq=++seq;
  try{const fonts=await document.fonts.load(`${s.style} ${s.weight} ${s.size}px Mekholi`,'মেখলি');if(thisSeq===seq)$('font-status').textContent=fonts.length?'Mekholi loaded':'Font not loaded — fallback may be visible';}
  catch(e){if(thisSeq===seq)$('font-status').textContent='Font load failed — check network and paths';}
 }
 async function copy(value,success){try{await navigator.clipboard.writeText(value);status(success);}catch(e){status('Clipboard unavailable. Select and copy the text below manually.');$('css-output').focus();}}
 for(const k of controls)$(k).addEventListener('input',update);
 $('preset').addEventListener('change',()=>{if(presets[$('preset').value]){$('text').value=presets[$('preset').value];update();}});
 $('reset').addEventListener('click',()=>{$('preset').value='';set(defaults);history.replaceState(null,'',location.pathname);status('Default settings restored.');});
 $('copy-css').addEventListener('click',()=>copy(css(state()),'CSS copied. Load fonts/web/mekholi.css on your own site first.'));
 $('share').addEventListener('click',()=>{const s=state();if(s.text.length>1500){status('Sharing is limited to 1,500 characters. Shorten the sample first.');return;}const url=new URL(location.href);url.search='';url.hash='sample='+encodeURIComponent(JSON.stringify(s));copy(url.href,'Share link copied. Your sample is stored in the URL fragment, not uploaded.');});
 $('export').addEventListener('click',async()=>{
  const button=$('export');button.disabled=true;status('Rendering PNG…');
  try{
   const s=state();const loaded=await document.fonts.load(`${s.style} ${s.weight} ${s.size}px Mekholi`,'মেখলি');
   if(!loaded.length)throw new Error('Mekholi is not loaded; PNG export cancelled to avoid fallback output.');
   const width=Math.max(320,Math.round($('preview').getBoundingClientRect().width)),padding=36;
   const probe=document.createElement('canvas'),ctx=probe.getContext('2d');ctx.font=`${s.style} ${s.weight} ${s.size}px Mekholi`;if('letterSpacing' in ctx)ctx.letterSpacing=s.tracking+'px';
   const lines=[];for(const paragraph of s.text.split('\n')){
    if(!paragraph){lines.push('');continue;}
    // Prefer word boundaries; never split within an Indic grapheme cluster.
    const words=typeof Intl.Segmenter==='function'?[...new Intl.Segmenter('bpy',{granularity:'word'}).segment(paragraph)].map(v=>v.segment):[paragraph];
    let line='';for(const word of words){if(line&&ctx.measureText(line+word).width>width-2*padding){lines.push(line);line=word;}else line+=word;}lines.push(line);
   }
   const lineHeight=Number(s.size)*Number(s.leading);const height=Math.max(240,Math.ceil(lines.length*lineHeight+padding*2+Number(s.size)*.4));
   if(height>16000||width*height>18000000)throw new Error('Sample too large to export safely. Shorten it or reduce the font size.');
   const canvas=document.createElement('canvas');canvas.width=width*2;canvas.height=height*2;const c=canvas.getContext('2d');c.scale(2,2);c.fillStyle=s.background;c.fillRect(0,0,width,height);c.font=ctx.font;c.fillStyle=s.color;c.textBaseline='alphabetic';c.textAlign=s.align;if('letterSpacing' in c)c.letterSpacing=s.tracking+'px';
   const x=s.align==='center'?width/2:s.align==='right'?width-padding:padding;
   lines.forEach((line,i)=>c.fillText(line,x,padding+Number(s.size)*1.25+i*lineHeight));
   const blob=await new Promise(resolve=>canvas.toBlob(resolve,'image/png'));if(!blob)throw new Error('PNG generation failed.');const a=document.createElement('a'),url=URL.createObjectURL(blob);a.href=url;a.download='Mekholi-'+s.weight+(s.style==='italic'?'-slanted':'')+'.png';a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);status('PNG exported at 2× resolution. Raster proof only; line wrapping can differ from the live preview.');
  }catch(e){status(e.message);}finally{button.disabled=false;}
 });
 try{const response=await fetch('assets/coverage.json');if(!response.ok)throw new Error();covered=new Set(await response.json());}catch(e){coverageError=true;}
 let initial=defaults;
 try{if(location.hash.startsWith('#sample='))initial=sanitize(JSON.parse(decodeURIComponent(location.hash.slice(8))));}catch(e){status('Invalid shared sample; defaults restored.');}
 set(initial);
})();
