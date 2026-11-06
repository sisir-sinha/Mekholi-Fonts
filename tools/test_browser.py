# Copyright (c) 2026 Surajit Singha Sisir and Ningshing Che.
# SIL OFL 1.1: https://openfontlicense.org/ — see mekholi-family/OFL.txt.
from playwright.sync_api import sync_playwright
from pathlib import Path
import os,tempfile
import json
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 context=browser.new_context(viewport={'width':1440,'height':1000},permissions=['clipboard-read','clipboard-write'],accept_downloads=True)
 page=context.new_page();errors=[];bad=[]
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append((r.status,r.url)) if r.status>=400 else None)
 base=os.environ.get('MEKHOLI_SITE_URL','http://127.0.0.1:8000/').rstrip('/')+'/'
 for path in ['', 'documentation.html','license.html','playground.html']:
  page.goto(base+path);page.evaluate('document.fonts.ready');assert page.locator('h1').count()==1
 page.wait_for_function("document.getElementById('font-status').textContent==='Mekholi loaded'")
 assert 'All typed characters' in page.locator('#coverage').inner_text()
 for weight in range(100,1000,100):
  page.select_option('#weight',str(weight))
  for style in ['normal','italic']:
   page.select_option('#style',style)
   page.wait_for_function(f"document.fonts.check('{style} {weight} 48px Mekholi')")
   assert page.locator('#preview').evaluate('(e)=>getComputedStyle(e).fontWeight')==str(weight)
 page.select_option('#preset','name');assert page.locator('#preview').inner_text()=='মেখলি\nMekholi'
 page.fill('#text','মেখলি 😀');assert 'U+1F600' in page.locator('#coverage').inner_text()
 page.fill('#text','মেখলি');page.click('#copy-css');page.wait_for_function("document.getElementById('status').textContent.includes('CSS copied')")
 page.click('#share');page.wait_for_function("document.getElementById('status').textContent.includes('Share link copied')");link=page.evaluate('navigator.clipboard.readText()');assert '#sample=' in link
 page.goto(link);page.wait_for_function("document.getElementById('preview').textContent==='মেখলি'")
 with page.expect_download() as download:page.click('#export')
 dl=download.value;dl.save_as(str(Path(tempfile.gettempdir())/'mekholi-playground-export.png'));assert Path(str(Path(tempfile.gettempdir())/'mekholi-playground-export.png')).stat().st_size>1000
 page.click('#reset');assert page.locator('#weight').input_value()=='400';assert '#sample=' not in page.url
 page.set_viewport_size({'width':390,'height':844})
 for path in ['', 'documentation.html','license.html','playground.html']:
  page.goto(base+path);page.evaluate('document.fonts.ready');assert page.evaluate('document.documentElement.scrollWidth<=innerWidth'),path+' horizontal overflow'
 print(json.dumps({'pages':4,'font_faces':18,'tests':['controls','presets','coverage warning','copy CSS','share restore','PNG export','reset','mobile overflow'],'js_errors':errors,'http_errors':bad},indent=2))
 assert not errors and not bad
 browser.close()
