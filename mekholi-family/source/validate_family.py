# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# SIL OFL 1.1: https://openfontlicense.org/ — see ../OFL.txt.
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import calcChecksum
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.areaPen import AreaPen
import uharfbuzz as hb,json,hashlib,sys
ROOT=Path(__file__).resolve().parents[1]
manifest=json.loads((ROOT/'documentation/family-manifest.json').read_text())
reference=TTFont(ROOT/'source/Kalpurush-0.258-upstream.ttf');c=reference.getBestCmap();order=reference.getGlyphOrder()
cons=[i for i in range(0x995,0x9ba) if i in c]
samples=['বাংলা ভাষা ও বাংলা লিপি','কি কী কু কূ কৃ কে কৈ কো কৌ কং কঃ কঁ','র্ক ক্র র্য ক্য ক্ষ জ্ঞ ত্র শ্র স্ত্র ন্দ্র ক্ত ন্ত ন্ধ ষ্ট ষ্ণ হ্ম','০১২৩৪৫৬৭৮৯ 0123456789','The quick brown fox jumps over the lazy dog.','ক্ষ ক্ষি ক্ষী র্কি ক্রি জ্ঞা ত্রু শ্রু ক্‌ষ ক্‍ষ','র ৱ ৰ য় য় ড় ঢ়']
tests=samples+[chr(a)+'\u09cd'+chr(b)+v for a in cons for b in cons for v in ['', '\u09bf','\u09c1','\u09cb']]
def shape(font,text):
 buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf)
 return [(i.codepoint,i.cluster,p.y_offset,p.y_advance) for i,p in zip(buf.glyph_infos,buf.glyph_positions)]
font=hb.Font(hb.Face((ROOT/'source/Kalpurush-0.258-upstream.ttf').read_bytes()));font.scale=(1000,1000)
refshapes=[[(i,cl) for i,cl,_,_ in shape(font,t)] for t in tests]
results=[]
for entry in manifest:
 path=ROOT/'fonts/ttf'/entry['file'];f=TTFont(path);raw=path.read_bytes();gs=f.getGlyphSet();bounds={};area=0;empty=[];errors=[]
 for i,g in enumerate(order):
  try:
   p=BoundsPen(gs);gs[g].draw(p);bounds[i]=p.bounds
   if p.bounds is None and reference['glyf'][g].numberOfContours>0:empty.append(g)
   ap=AreaPen(gs);gs[g].draw(ap);area+=abs(ap.value)
  except Exception as e:errors.append([g,str(e)])
 checks=[]
 for tag,e in f.reader.tables.items():
  data=f.reader[tag]
  if tag=='head':data=data[:8]+b'\0\0\0\0'+data[12:]
  if calcChecksum(data)!=e.checkSum:checks.append(tag)
 hfont=hb.Font(hb.Face(raw));hfont.scale=(1000,1000);missing=[];changed=[];outside=[]
 miny=0;maxy=0
 for idx,text in enumerate(tests):
  shaped=shape(hfont,text)
  if any(i==0 for i,_,_,_ in shaped):missing.append(text)
  if [(i,cl) for i,cl,_,_ in shaped]!=refshapes[idx]:changed.append(text)
  y=0
  for gid,_,dy,ay in shaped:
   b=bounds[gid]
   if b:
    bottom=b[1]+dy+y;top=b[3]+dy+y;miny=min(miny,bottom);maxy=max(maxy,top)
    if bottom < -f['OS/2'].usWinDescent or top>f['OS/2'].usWinAscent:outside.append({'text':text,'glyph':order[gid],'bottom':bottom,'top':top})
   y+=ay
 names=f['name'];metadata=(names.getDebugName(13)==(ROOT/'OFL.txt').read_text() and names.getDebugName(14)=='https://openfontlicense.org/' and f['OS/2'].fsType==0 and f['OS/2'].usWeightClass==entry['weight'] and bool(f['OS/2'].fsSelection&1)==entry['italic'])
 webs=True
 for flavor in ['woff','woff2']:
  w=TTFont(ROOT/'fonts/web'/path.name.replace('.ttf','.'+flavor))
  webs &= w.getBestCmap()==c and w['name'].getDebugName(13)==(ROOT/'OFL.txt').read_text() and w.getGlyphOrder()==order
 ok=not(errors or checks or missing or changed or outside or empty) and metadata and webs and f.getBestCmap()==c and calcChecksum(raw)==0xb1b0afba
 r={**entry,'status':'PASS' if ok else 'REVIEW','test_strings':len(tests),'glyphs':len(order),'codepoints':len(c),'outline_errors':errors,'new_empty_glyphs':empty,'checksum_errors':checks,'notdef_cases':missing,'glyph_selection_changed_cases':changed,'shaped_vertical_outliers':outside,'tested_vertical_bounds':[miny,maxy],'metadata_ok':metadata,'web_roundtrips_ok':bool(webs),'total_abs_outline_area':round(area,2),'sha256':hashlib.sha256(raw).hexdigest()};results.append(r)
 print(entry['style'],r['status'],'empty',len(empty),'outliers',len(outside),'area',round(area),flush=True)
summary={'status':'PASS' if all(x['status']=='PASS' for x in results) else 'REVIEW','styles':len(results),'shaping_cases_total':len(tests)*len(results),'limitations':'Structural and representative/synthetic shaping checks only. No full intersection/collision/linguistic or optical correctness certification. Thin strokes can erode and heavy counters can close. Italics are slanted uprights.','results':results}
(ROOT/'documentation/validation.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2))
if summary['status']!='PASS':sys.exit(1)
