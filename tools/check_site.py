#!/usr/bin/env python3
# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# SIL OFL 1.1: https://openfontlicense.org/ — see mekholi-family/OFL.txt.
"""Dependency-free structural/link checks for the published static site."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,re,zipfile,sys
root=Path(__file__).resolve().parents[1]
class Parser(HTMLParser):
 def __init__(self):super().__init__();self.links=[];self.ids=[]
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.append(a['id'])
  for k in ['href','src']:
   if k in a:self.links.append(a[k])
errors=[];pages=['index.html','documentation.html','license.html','playground.html'];parsers={}
for name in pages:
 p=Parser();p.feed((root/name).read_text());parsers[name]=p
 if len(p.ids)!=len(set(p.ids)):errors.append(name+': duplicate IDs')
 if 'মেখলি' not in (root/name).read_text():errors.append(name+': Bengali name absent')
for name,p in parsers.items():
 for url in p.links:
  parts=urlsplit(url)
  if parts.scheme or parts.netloc:continue
  if parts.path.startswith('/'):errors.append(name+': non-portable domain-root path '+url);continue
  target=(root/unquote(parts.path)).resolve() if parts.path else root/name
  if target.is_dir():target=target/'index.html'
  if not target.is_file():errors.append(name+': missing '+url)
  elif parts.fragment and target.name in parsers and parts.fragment not in parsers[target.name].ids:errors.append(name+': missing fragment '+url)
for name in ['assets/site.css','mekholi-family/fonts/web/mekholi.css']:
 p=root/name
 for url in re.findall(r'url\([\'\"]?([^\)\'\"]+)',p.read_text()):
  if not urlsplit(url).scheme and not (p.parent/url).resolve().is_file():errors.append(name+': missing CSS asset '+url)
coverage=json.loads((root/'assets/coverage.json').read_text())
if len(coverage)!=210:errors.append('Unexpected coverage count')
for char in 'মেখলি':
 if ord(char) not in coverage:errors.append('Bengali name is not covered')
with zipfile.ZipFile(root/'downloads/Mekholi-v1.0-experimental-18-styles.zip') as z:
 names=z.namelist();prefix='Mekholi-v1.0-experimental/'
 for ext in ['ttf','woff','woff2']:
  if sum(n.endswith('.'+ext) and '/fonts/' in n for n in names)!=18:errors.append('ZIP count for '+ext)
 if z.read(prefix+'OFL.txt')!=(root/'mekholi-family/OFL.txt').read_bytes():errors.append('ZIP license out of sync')
 if z.testzip():errors.append('ZIP integrity failure')
if errors:print('\n'.join(errors));sys.exit(1)
print('PASS: four pages, relative links/anchors, CSS/font paths, Bengali name, 210 code points, ZIP integrity and 54 font outputs.')
