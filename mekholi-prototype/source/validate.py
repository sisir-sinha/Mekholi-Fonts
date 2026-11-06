# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# Licensed under SIL OFL 1.1: https://openfontlicense.org/ — see ../OFL.txt.
from pathlib import Path
from fontTools.ttLib import TTFont
from fontTools.ttLib.sfnt import calcChecksum
from fontTools.pens.boundsPen import BoundsPen
from fontTools.misc.roundTools import otRound
import uharfbuzz as hb
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
a=ROOT/'source/Kalpurush-0.258-upstream.ttf';b=ROOT/'fonts/ttf/Mekholi-Regular.ttf'
f=TTFont(b);gs=f.getGlyphSet();c=f.getBestCmap();order=f.getGlyphOrder();raw=b.read_bytes()
def shape(path,text):
 font=hb.Font(hb.Face(path.read_bytes()));font.scale=(1000,1000);buf=hb.Buffer();buf.add_str(text);buf.guess_segment_properties();hb.shape(font,buf)
 return [(i.codepoint,i.cluster,p.x_advance,p.y_advance,p.x_offset,p.y_offset) for i,p in zip(buf.glyph_infos,buf.glyph_positions)]
cons=[i for i in range(0x995,0x9ba) if i in c]
samples=['বাংলা ভাষা ও বাংলা লিপি','কি কী কু কূ কৃ কে কৈ কো কৌ কং কঃ কঁ','র্ক ক্র র্য ক্য ক্ষ জ্ঞ ত্র শ্র স্ত্র ন্দ্র ক্ত ন্ত ন্ধ ষ্ট ষ্ণ হ্ম','০১২৩৪৫৬৭৮৯ 0123456789','The quick brown fox jumps over the lazy dog.','ক্ষ ক্ষি ক্ষী র্কি ক্রি জ্ঞা ত্রু শ্রু ক্‌ষ ক্‍ষ','র ৱ ৰ য় য় ড় ঢ়']
tests=samples+[chr(x)+'\u09cd'+chr(y)+s for x in cons for y in cons for s in ['', '\u09bf','\u09c1','\u09cb']]
missing=[];changed=[];outside=[];maxerror=0
for text in tests:
 before=shape(a,text);after=shape(b,text)
 if any(g[0]==0 for g in after):missing.append(text)
 if [(g[0],g[1]) for g in before]!=[(g[0],g[1]) for g in after]:changed.append(text)
 for p,q in zip(before,after):maxerror=max(maxerror,abs(q[2]-otRound(p[2]*1.03)))
 # accumulate actual shaped glyph bounds to check current Windows limits
 y=0
 for gid,cluster,ax,ay,dx,dy in after:
  pen=BoundsPen(gs);gs[order[gid]].draw(pen)
  if pen.bounds and (pen.bounds[1]+y+dy < -550 or pen.bounds[3]+y+dy>1100):outside.append({'text':text,'glyph':order[gid],'bottom':pen.bounds[1]+y+dy,'top':pen.bounds[3]+y+dy})
  y+=ay
bounds=[]
for n in order:
 pen=BoundsPen(gs);gs[n].draw(pen)
 if pen.bounds:bounds.append(pen.bounds)
checks=[]
for tag,e in f.reader.tables.items():
 data=f.reader[tag]
 if tag=='head':data=data[:8]+b'\0\0\0\0'+data[12:]
 if calcChecksum(data)!=e.checkSum:checks.append(tag)
r={'status':'PASS' if not(missing or changed or outside or checks) else 'REVIEW','cases':len(tests),'notdef_cases':missing,'changed_glyph_selection_cases':changed,'shaped_vertical_outliers':outside,'max_advance_rounding_difference_units':maxerror,'checksum_errors':checks,'whole_checksum':hex(calcChecksum(raw)),'glyphs':len(order),'codepoints':len(c),'outline_bounds':[min(x[0] for x in bounds),min(x[1] for x in bounds),max(x[2] for x in bounds),max(x[3] for x in bounds)],'upstream_sha256':hashlib.sha256(a.read_bytes()).hexdigest(),'sha256':hashlib.sha256(raw).hexdigest(),'limits':'Not a linguistic, bytecode, cross-platform, collision or full design certification.'}
for ext in ['woff','woff2']:
 web=TTFont(ROOT/f'fonts/web/Mekholi-Regular.{ext}');assert web.getBestCmap()==c;assert web.getGlyphOrder()==order
r['web_roundtrip']='WOFF and WOFF2 reopen with matching cmap and glyph order'
(ROOT/'documentation/validation.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in r.items() if k!='shaped_vertical_outliers'},ensure_ascii=False,indent=2));print('shaped outliers',len(outside))
