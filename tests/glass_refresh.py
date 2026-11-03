"""Real reload, glass hierarchy and curled-path regression checks."""
import argparse, math, shutil, json
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/glass-refresh');a=p.parse_args()
out=Path(a.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 page=b.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
 for width in [1440,2048,768,390,320]:
  page.set_viewport_size({'width':width,'height':900});page.goto(a.url);page.wait_for_timeout(180)
  for target in ['middle','bottom','hash']:
   if target=='hash':
    
    if width<=850:page.locator('.menu-toggle').click()
    page.locator('nav a[href="#projects"]').click();page.wait_for_timeout(700)
    assert page.evaluate('location.hash')=='#projects'
   else:
    page.evaluate('(t)=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*(t==="middle"?.5:1),behavior:"instant"})',target)
   assert page.evaluate('scrollY')>100
   page.reload();page.wait_for_timeout(350)
   assert page.evaluate('scrollY')==0,(width,target,page.evaluate('scrollY'))
   assert page.evaluate('location.hash')==''
   assert page.locator('#hero-title').is_visible()
  # Force a genuinely fresh document, rather than a same-document hash hop.
  page.goto('about:blank')
  page.goto(a.url+'/#experience');page.wait_for_timeout(700)
  assert page.evaluate('scrollY')>100 and page.evaluate('location.hash')=='#experience'
  if width<=850:page.locator('.menu-toggle').click()
  page.locator('nav a[href="#projects"]').click();page.wait_for_timeout(700)
  assert page.evaluate('location.hash')=='#projects'
  print('navigation',width,page.evaluate('({y:scrollY,hash:location.hash,project:document.querySelector("#projects").getBoundingClientRect().y})'))
  page.wait_for_function('Math.abs(document.querySelector("#projects").getBoundingClientRect().y)<180',timeout=4000)
  page.go_back();page.wait_for_timeout(500)
  assert page.evaluate('location.hash')=='#experience' and page.evaluate('scrollY')>100
  page.go_forward();page.wait_for_timeout(500)
  assert page.evaluate('location.hash')=='#projects'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  if width in [1440,390]:
   page.goto(a.url);page.wait_for_timeout(180)
   tiers=page.evaluate('''()=>['.about','.past-project-list','.leadership .entry-list','.training .entry-list','.experience .entry-list','.project-card'].filter(s=>document.querySelector(s)).map(s=>{const e=document.querySelector(s),c=getComputedStyle(e);return {selector:s,tint:c.backgroundColor,blur:c.backdropFilter,opacity:c.opacity}})''')
   print(width,'glass tiers',tiers)
   assert all(t['opacity']=='1' for t in tiers)
   assert '0.32' in tiers[0]['tint']
   assert '0.74' in tiers[-1]['tint']
   # Inspect the browser's actual generated offset geometry, independent of JS sampling.
   turns=page.evaluate('''()=>{const e=document.querySelector('.orbital-decoration');const value=e.style.getPropertyValue('--journey-path');const path=document.createElementNS('http://www.w3.org/2000/svg','path');path.setAttribute('d',value.slice(6,-2));const n=path.getTotalLength();const points=Array.from({length:801},(_,i)=>path.getPointAtLength(n*i/800));let total=0,previous;for(let i=1;i<points.length;i++){const angle=Math.atan2(points[i].y-points[i-1].y,points[i].x-points[i-1].x);if(previous!==undefined){let d=angle-previous;while(d>Math.PI)d-=2*Math.PI;while(d< -Math.PI)d+=2*Math.PI;total+=Math.abs(d);}previous=angle;}return total;}''')
   print(width,'path absolute turning radians',turns)
   assert turns>20,'Path lacks visible curling curvature'
   found=set();span=page.evaluate('document.documentElement.scrollHeight-innerHeight')
   for y in range(0,int(span),35):
    page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(30)
    hit=page.locator('.orbital-spark').evaluate('''e=>{const r=e.getBoundingClientRect();const p=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);for(const [name,s] of [['clear','.past-project-list'],['medium','.leadership .entry-list,.training .entry-list'],['strong','.experience .entry-list']])if(p?.closest(s))return name;return null;}''')
    if hit and hit not in found:
     page.screenshot(path=str(out/f'{width}-glass-{hit}.png'));found.add(hit)
    if len(found)==3:break
   assert len(found)==3,(width,found)
 assert not errors,errors
 b.close()
print('PASS: actual middle/bottom/hash reload resets, fresh incoming anchors, post-refresh navigation, tiered glass, content opacity, visible curled geometry and star-behind-tier screenshots.')
