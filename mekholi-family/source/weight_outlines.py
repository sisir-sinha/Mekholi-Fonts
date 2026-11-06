# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# SIL OFL 1.1: https://openfontlicense.org/ — see ../OFL.txt.
"""Mechanical contour offset through FreeType; overlap cleanup through Skia PathOps.
Requires the FreeType shared library (libfreetype.so.6 on Linux).
No hand-drawn masters or optical corrections are implied.
"""
import ctypes as C
import ctypes.util
from copy import deepcopy
from fontTools.misc.roundTools import otRound
from fontTools.ttLib.tables._g_l_y_f import GlyphCoordinates
from fontTools.pens.recordingPen import RecordingPen
from fontTools.pens.ttGlyphPen import TTGlyphPen
from fontTools.pens.cu2quPen import Cu2QuPen
import pathops
class Vector(C.Structure):_fields_=[('x',C.c_long),('y',C.c_long)]
class Outline(C.Structure):_fields_=[('n_contours',C.c_short),('n_points',C.c_short),('points',C.POINTER(Vector)),('tags',C.POINTER(C.c_byte)),('contours',C.POINTER(C.c_short)),('flags',C.c_int)]
lib=C.CDLL(ctypes.util.find_library('freetype'))
lib.FT_Outline_EmboldenXY.argtypes=[C.POINTER(Outline),C.c_long,C.c_long]
lib.FT_Outline_EmboldenXY.restype=C.c_int

def offset_glyph(glyph,glyf,amount):
 g=deepcopy(glyph)
 if g.numberOfContours<=0 or not amount:return g
 points=(Vector*len(g.coordinates))(*(Vector(otRound(x*64),otRound(y*64)) for x,y in g.coordinates))
 tags=(C.c_byte*len(g.flags))(*[flag&1 for flag in g.flags])
 ends=(C.c_short*len(g.endPtsOfContours))(*g.endPtsOfContours)
 outline=Outline(g.numberOfContours,len(points),points,tags,ends,0)
 err=lib.FT_Outline_EmboldenXY(C.byref(outline),otRound(amount*64),otRound(amount*64))
 if err:raise RuntimeError('FreeType embolden error %d'%err)
 g.coordinates=GlyphCoordinates([(p.x/64-amount/2,p.y/64-amount/2) for p in points])
 path=pathops.Path();g.draw(path.getPen(),glyf)
 clean=pathops.simplify(path,fix_winding=True,keep_starting_points=True)
 pen=TTGlyphPen(None);clean.draw(Cu2QuPen(pen,max_err=0.5,reverse_direction=False))
 return pen.glyph()
