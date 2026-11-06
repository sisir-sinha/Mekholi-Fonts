# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# SIL OFL 1.1: https://openfontlicense.org/ — see ../OFL.txt.
"""Build an EXPERIMENTAL mechanically weighted/slanted 18-style static family."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from fontTools.ttLib import TTFont
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.misc.roundTools import otRound
import subprocess,sys,tempfile,math,json
from weight_outlines import offset_glyph
ROOT=Path(__file__).resolve().parents[1]
WEIGHTS=[(100,'Thin',-28),(200,'Extra Light',-19),(300,'Light',-10),(400,'Regular',0),(500,'Medium',10),(600,'Semi Bold',20),(700,'Bold',32),(800,'Extra Bold',44),(900,'Black',58)]
subprocess.run([sys.executable,str(ROOT/'source/build_regular.py')],check=True)
base=ROOT/'fonts/ttf/Mekholi-Regular.ttf'
license_text=(ROOT/'OFL.txt').read_text();manifest=[]
def shear_layout(obj,s,seen):
 if obj is None or isinstance(obj,(str,int,float,bytes)) or id(obj) in seen:return
 seen.add(id(obj))
 if isinstance(obj,(list,tuple)):
  for v in obj:shear_layout(v,s,seen)
 elif isinstance(obj,dict):
  for v in obj.values():shear_layout(v,s,seen)
 elif hasattr(obj,'__dict__'):
  if hasattr(obj,'XCoordinate') and hasattr(obj,'YCoordinate'):obj.XCoordinate=otRound(obj.XCoordinate+s*obj.YCoordinate)
  if getattr(obj,'YPlacement',0):obj.XPlacement=otRound(getattr(obj,'XPlacement',0)+s*obj.YPlacement)
  for v in list(vars(obj).values()):shear_layout(v,s,seen)
def build(item,tmp):
 weight,label,delta=item
 original=TTFont(base)
 weighted_glyphs={name:offset_glyph(original['glyf'][name],original['glyf'],delta) for name in original.getGlyphOrder()}
 for italic in (False,True):
  f=TTFont(base);order=f.getGlyphOrder();gs=f.getGlyphSet();s=math.tan(math.radians(12)) if italic else 0
  glyphs={}
  for gid,name in enumerate(order):
   rec=DecomposingRecordingPen(gs)
   weighted_glyphs[name].draw(rec,original['glyf'])
   pen=TTGlyphPen(None);rec.replay(TransformPen(pen,(1,0,s,1,0,0)));glyphs[name]=pen.glyph()
  for name,g in glyphs.items():
   f['glyf'][name]=g;g.recalcBounds(f['glyf']);aw,_=f['hmtx'][name];f['hmtx'][name]=(aw,getattr(g,'xMin',0))
  if italic:
   shear_layout(f['GPOS'].table,s,set())
   # Coordinate caret values lie on the baseline, so shear leaves them unchanged.
  style=label+(' Italic' if italic else '');slug=style.replace(' ','')
  if weight in (400,700):legacy='Mekholi';sub=('Bold' if weight==700 else 'Regular')+(' Italic' if italic else '');sub='Italic' if weight==400 and italic else sub
  else:legacy='Mekholi '+label;sub='Italic' if italic else 'Regular'
  values={1:legacy,2:sub,3:f'Mekholi:1.000:{slug}:ExperimentalFamily1',4:'Mekholi '+style,5:'Version 1.000; Experimental Family 1',6:'Mekholi-'+slug,10:'Experimental Kalpurush-derived serif for Bishnupriya Manipuri. Mechanically generated weight; 12 degree slanted upright for italic styles, not true drawn italics. Unhinted; optical and native-language review required. Original design: Md. Tanbin Islam Siyam; Latin based on Gentium.',13:license_text,14:'https://openfontlicense.org/',16:'Mekholi',17:style}
  for nid,text in values.items():f['name'].setName(text,nid,3,1,0x409)
  f['OS/2'].usWeightClass=weight
  f['OS/2'].fsSelection=0x80|(1 if italic else 0)|(0x20 if weight==700 else 0)|(0x40 if not italic and weight!=700 else 0)
  f['head'].macStyle=(1 if weight==700 else 0)|(2 if italic else 0)
  f['post'].italicAngle=-12 if italic else 0
  f['hhea'].caretSlopeRise=1000;f['hhea'].caretSlopeRun=213 if italic else 0
  # Unified conservative family metrics; validation checks shaped glyph extents.
  f['OS/2'].usWinAscent=1300;f['OS/2'].usWinDescent=700
  f['hhea'].ascent=f['OS/2'].sTypoAscender=1100
  f['hhea'].descent=f['OS/2'].sTypoDescender=-650
  f['hhea'].lineGap=f['OS/2'].sTypoLineGap=0
  pan=f['OS/2'].panose;pan.bWeight={100:2,200:3,300:3,400:5,500:6,600:7,700:8,800:9,900:10}[weight]
  if italic:pan.bLetterForm=11
  f.recalcTimestamp=False
  dest=ROOT/f'fonts/ttf/Mekholi-{slug}.ttf';f.save(dest)
  for flavor in ['woff','woff2']:
   web=TTFont(dest);web.flavor=flavor;web.save(ROOT/f'fonts/web/Mekholi-{slug}.{flavor}')
  manifest.append({'style':style,'weight':weight,'italic':italic,'file':dest.name,'stroke_change_units':delta,'slant_degrees':12 if italic else 0,'status':'experimental-mechanical'})
with tempfile.TemporaryDirectory() as tmp:
 # Regular is the input to every job. Do it last to avoid replacing input mid-build.
 for item in [i for i in WEIGHTS if i[0]!=400]:build(item,tmp)
 build(WEIGHTS[3],tmp)
manifest.sort(key=lambda v:(v['weight'],v['italic']))
(ROOT/'documentation/family-manifest.json').write_text(json.dumps(manifest,indent=2))
css=['/* Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che. SIL OFL 1.1: https://openfontlicense.org/ */']
for v in manifest:
 slug=v['file'][:-4]
 css.append("@font-face { font-family: 'Mekholi'; src: url('./%s.woff2') format('woff2'), url('./%s.woff') format('woff'); font-weight: %s; font-style: %s; font-display: swap; }"%(slug,slug,v['weight'],'italic' if v['italic'] else 'normal'))
css.append(".mekholi { font-family: 'Mekholi', serif; font-synthesis: none; line-height: 1.75; }")
(ROOT/'fonts/web/mekholi.css').write_text('\n'.join(css)+'\n')
print('Built 18 TTF + 18 WOFF + 18 WOFF2 files')
