# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# Licensed under SIL OFL 1.1: https://openfontlicense.org/ — see ../OFL.txt.
"""Mekholi 1.0 Regular, experimental derivative. Run: python source/build.py"""
from pathlib import Path
from fontTools.ttLib import TTFont, newTable
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.transformPen import TransformPen
from fontTools.pens.recordingPen import DecomposingRecordingPen
from fontTools.misc.roundTools import otRound
from fontTools.pens.boundsPen import BoundsPen
import hashlib,json
ROOT=Path(__file__).resolve().parents[1]
src=ROOT/'source/Kalpurush-0.258-upstream.ttf'
assert hashlib.sha256(src.read_bytes()).hexdigest()=='83613a03e53aad8337f2be9fb974409a23c1d99b3b4b494567ba9d156c492b01'
f=TTFont(src);gs=f.getGlyphSet();sx=1.03
new={}
for name in f.getGlyphOrder():
 rec=DecomposingRecordingPen(gs);gs[name].draw(rec)
 pen=TTGlyphPen(None);rec.replay(TransformPen(pen,(sx,0,0,1,0,0)));new[name]=pen.glyph()
for name,g in new.items():
 f['glyf'][name]=g
 aw,lsb=f['hmtx'][name];f['hmtx'][name]=(otRound(aw*sx),otRound(lsb*sx))
# Scale horizontal positioning to match transformed outlines. Vertical positioning unchanged.
seen=set()
def scale_layout(obj):
 if obj is None or isinstance(obj,(str,int,float,bytes)):return
 if id(obj) in seen:return
 seen.add(id(obj))
 if isinstance(obj,(list,tuple)):
  for x in obj:scale_layout(x)
 elif isinstance(obj,dict):
  for v in obj.values():scale_layout(v)
 elif hasattr(obj,'__dict__'):
  for key,v in list(vars(obj).items()):
   if key in ('XCoordinate','XPlacement','XAdvance') and isinstance(v,int):setattr(obj,key,otRound(v*sx))
   elif key=='Coordinate' and type(obj).__name__=='CaretValue' and isinstance(v,int):setattr(obj,key,otRound(v*sx))
   else:scale_layout(v)
for tag in ['GPOS','GDEF']:
 if tag in f:scale_layout(f[tag].table)
# Original grid-fitting and precomputed device metrics are invalid after changing outlines.
for tag in ['fpgm','prep','cvt ','hdmx','LTSH','VDMX','DSIG']:
 if tag in f:del f[tag]
f['gasp']=newTable('gasp');f['gasp'].version=1;f['gasp'].gaspRange={65535:15}
f['head'].fontRevision=1.0
f['head'].flags &= ~0x14 # no instruction dependency and no force-integer instruction behavior
f['head'].macStyle=0
f['hhea'].ascent=1050;f['hhea'].descent=-550;f['hhea'].lineGap=0
os=f['OS/2'];os.version=4;os.usWeightClass=400;os.usWidthClass=5;os.fsType=0;os.fsSelection=0x40|0x80
os.sTypoAscender=1050;os.sTypoDescender=-550;os.sTypoLineGap=0
os.usWinAscent=1100;os.usWinDescent=550
os.achVendID='NONE'
f['post'].italicAngle=0
# Retain original credits as derivative attribution, not an endorsement.
license_text=(ROOT/'OFL.txt').read_text()
copyright_text='Copyright (c) 2022, Tanbin Islam Siyam (https://omicronlab.com), with Reserved Font Name Kalpurush. Copyright (c) 2026, Surajit Singha Sisir and Ningshing Che, for the Mekholi modifications, with Reserved Font Name Mekholi.'
f['name'].names=[]
values={0:copyright_text,
1:'Mekholi',2:'Regular',3:'Mekholi:1.000:Regular:Prototype1:OFL2',4:'Mekholi Regular',5:'Version 1.000; Prototype 1',6:'Mekholi-Regular',
8:'Ningshing Che',9:'Surajit Singha Sisir',10:'Experimental Kalpurush-derived serif for Bishnupriya Manipuri. Horizontal outline/spacing expansion 3%; revised metrics. Original design: Md. Tanbin Islam Siyam; Latin based on Gentium. Not language-validated; unhinted; Regular only.',
13:license_text,14:'https://openfontlicense.org/',16:'Mekholi',17:'Regular',19:'Bishnupriya Manipuri — Mekholi Regular prototype'}
for nid,text in values.items():f['name'].setName(text,nid,3,1,0x409)
f.recalcTimestamp=False
out=ROOT/'fonts/ttf/Mekholi-Regular.ttf';out.parent.mkdir(parents=True,exist_ok=True);f.save(out)
for flavor in ['woff','woff2']:
 w=TTFont(out);w.flavor=flavor;w.save(ROOT/f'fonts/web/Mekholi-Regular.{flavor}')
print('Built TTF, WOFF, WOFF2')
