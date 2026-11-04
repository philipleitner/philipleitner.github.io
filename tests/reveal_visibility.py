"""Measure rendered transition continuity and safe early/late enhancement."""
import argparse,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/soft-reveal-visibility');a=p.parse_args();out=Path(a.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox']);results=[]
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':900});page.goto(a.url);page.wait_for_load_state('networkidle')
  data=page.evaluate('''async()=>{const el=document.querySelector('#experience h2'),top=el.getBoundingClientRect().top+scrollY;let ratio;el.addEventListener('transitionrun',e=>{if(e.propertyName==='opacity')ratio=el.getBoundingClientRect().top/innerHeight});scrollTo({top:top-innerHeight-160,behavior:'instant'});await new Promise(r=>setTimeout(r,100));const start=scrollY,samples=[];await new Promise(resolve=>{let t0;function frame(t){t0??=t;const p=Math.min(1,(t-t0)/5500);scrollTo({top:start+500*p,behavior:'instant'});const r=el.getBoundingClientRect(),c=getComputedStyle(el);samples.push({t:t-t0,y:r.top,visible:r.top<innerHeight&&r.bottom>85,opacity:+c.opacity});if(p<1)requestAnimationFrame(frame);else resolve();}requestAnimationFrame(frame)});return{ratio,samples};}''')
  visible=[s for s in data['samples'] if s['visible']];changing=[s for s in visible if .03<s['opacity']<.97]
  assert all(n['opacity']>=p['opacity']-.001 for p,n in zip(visible,visible[1:])), 'Visible full-to-transparent flash'
  assert len(changing)>=6 and changing[-1]['t']-changing[0]['t']>=200
  assert .84<=data['ratio']<=.92,(width,data['ratio'])
  assert visible[-1]['opacity']==1
  page.screenshot(path=str(out/f'visible-transition-{width}.png'));results.append({'width':width,**data})
  page.goto('about:blank');page.goto(a.url);page.wait_for_load_state('networkidle')
  if width==390:page.locator('.menu-toggle').click()
  page.locator('nav a[href="#projects"]').click();page.wait_for_timeout(1100)
  row=page.locator('.past-project-row').last;assert 'reveal-pending' in row.get_attribute('class')
  row.evaluate('(e)=>scrollTo({top:e.getBoundingClientRect().top+scrollY-innerHeight*.86,behavior:"instant"})');page.wait_for_timeout(100)
  assert 'reveal-entering' in row.get_attribute('class')
  page.locator('.activity-link').last.focus();assert page.locator('.activity-card.reveal-pending,.activity-card.reveal-entering').count()<2
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');page.close()
 for variant in ['early','late','uncertain']:
  context=b.new_context(viewport={'width':1440,'height':900});page=context.new_page()
  if variant=='early':page.add_init_script('const original=performance.getEntriesByType.bind(performance);performance.getEntriesByType=t=>t==="paint"?[]:original(t)')
  if variant=='late':page.add_init_script('const original=performance.getEntriesByType.bind(performance);performance.getEntriesByType=t=>t==="paint"?[{name:"first-contentful-paint"}]:original(t)')
  if variant=='uncertain':page.add_init_script('Object.defineProperty(PerformanceObserver,"supportedEntryTypes",{value:[]})')
  page.add_init_script('window.heroTransitions=0;document.addEventListener("transitionrun",e=>{if(e.propertyName==="opacity"&&e.target.closest(".hero"))heroTransitions++},true)')
  page.goto(a.url);page.wait_for_timeout(1200)
  assert page.locator('.hero h1,.hero-copy,.hero-links,.hero-portrait').evaluate_all('(es)=>es.every(e=>getComputedStyle(e).opacity==="1")')
  assert page.locator('header').evaluate('(e)=>getComputedStyle(e).opacity')=='1'
  assert (page.evaluate('heroTransitions')>0)==(variant=='early'),variant
  context.close()
 b.close();(out/'transition-continuity.json').write_text(json.dumps(results,indent=2))
print('PASS: monotonic rendered transitions at88%viewport, meaningful visiblefade, safeearly/late/uncertain initialization and anchors/focus.')
