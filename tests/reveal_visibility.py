"""Ensure reveals are visible during slow scrolling, not finished off-screen."""
import argparse,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/reveal-visibility');p.add_argument('--record',action='store_true');a=p.parse_args();out=Path(a.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 for width,height in [(1440,900),(390,844)]:
  options={'viewport':{'width':width,'height':height}}
  if a.record:options.update(record_video_dir=str(out),record_video_size={'width':width,'height':height})
  context=b.new_context(**options);page=context.new_page();page.goto(a.url);page.wait_for_load_state('networkidle')
  top=page.locator('#experience h2').evaluate('(e)=>e.getBoundingClientRect().top+scrollY');start=top-height-100
  page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',start);page.wait_for_timeout(900)
  page.evaluate('window.visibleRevealStart=null;document.addEventListener("animationstart",e=>{if(e.target===document.querySelector("#experience h2")){const m=new DOMMatrixReadOnly(getComputedStyle(e.target).transform);window.visibleRevealStart=e.target.getBoundingClientRect().top-m.m42}})')
  visible=0;whole=0
  for n in range(70):
   page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',start+n*5);page.wait_for_timeout(40)
   state=page.locator('#experience h2').evaluate('(e)=>({top:e.getBoundingClientRect().top,bottom:e.getBoundingClientRect().bottom,opacity:+getComputedStyle(e).opacity})')
   if state['top']<height and state['bottom']>0 and state['opacity']<.95:
    visible+=1
    if state['bottom']<=height:whole+=1
  assert visible>=5 and whole>=3,(width,visible,whole)
  assert page.evaluate('visibleRevealStart')<=height-20,(width,page.evaluate('visibleRevealStart'))
  page.wait_for_timeout(900)
  # Fresh direct navigation must not mark later project entries as already seen.
  page.goto('about:blank');page.goto(a.url);page.wait_for_load_state('networkidle')
  page.evaluate('window.lateRowReveals=0;document.addEventListener("animationstart",e=>{if(e.animationName==="gentle-reveal"&&e.target.matches(".past-project-row"))window.lateRowReveals++})')
  page.locator('nav a[href="#projects"]').evaluate('(e)=>e.click()');page.wait_for_timeout(1000)
  page.locator('.past-project-row').last.scroll_into_view_if_needed();page.wait_for_timeout(900)
  assert page.evaluate('lateRowReveals')>0,'Anchor suppressed all later entries'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  video=page.video;page.close()
  if video:video.save_as(str(out/f'{width}-visible-reveal.webm'))
  context.close()
  print(width,'visible changing frames',visible,'fully on-screen changing frames',whole)
 b.close()
print('PASS: visible on-screen fade during slow scrolling, and later entries still reveal after anchor navigation.')
