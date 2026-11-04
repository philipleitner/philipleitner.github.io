import argparse,json,shutil
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8765');parser.add_argument('--artifacts',default='/tmp/portfolio-reveal-visibility');args=parser.parse_args()
from pathlib import Path
from playwright.sync_api import sync_playwright
out=Path(args.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox']);results=[]
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':900});page.goto(args.url);page.wait_for_load_state('networkidle')
  data=page.evaluate('''async()=>{const el=document.querySelector('#experience h2');const top=el.getBoundingClientRect().top+scrollY;scrollTo({top:top-innerHeight-160,behavior:'instant'});await new Promise(r=>setTimeout(r,100));const start=scrollY,samples=[];await new Promise(resolve=>{let t0;function frame(t){t0??=t;const p=Math.min(1,(t-t0)/4000);scrollTo({top:start+420*p,behavior:'instant'});const r=el.getBoundingClientRect(),c=getComputedStyle(el);samples.push({t:t-t0,y:r.top,visible:r.top<innerHeight&&r.bottom>85,opacity:+c.opacity,transform:c.transform});if(p<1)requestAnimationFrame(frame);else resolve();}requestAnimationFrame(frame)});return samples;}''')
  visible=[s for s in data if s['visible']];moving=[s for s in visible if s['opacity']<.98]
  assert all(n['opacity']>=p['opacity']-.001 for p,n in zip(visible,visible[1:])), 'Visible opacity dropped'
  assert moving and moving[-1]['t']-moving[0]['t']>=230, 'Fade finished outside viewport'
  assert visible[0]['opacity']<.8 and visible[-1]['opacity']==1
  page.screenshot(path=str(out/f'visible-heading-{width}.png'));results.append({'width':width,'first_visible_opacity':visible[0]['opacity'],'visible_fade_ms':moving[-1]['t']-moving[0]['t'],'samples':data})
  # A fresh anchor must not suppress future rows below the visible destination.
  page.goto('about:blank');page.goto(args.url);page.wait_for_load_state('networkidle')
  if width==390:page.locator('.menu-toggle').click()
  page.locator('nav a[href="#projects"]').click();page.wait_for_timeout(850)
  row=page.locator('.past-project-row').last
  assert 'reveal-pending' in row.get_attribute('class')
  row.evaluate('(e)=>scrollTo({top:e.getBoundingClientRect().top+scrollY-innerHeight+100,behavior:"instant"})');page.wait_for_timeout(100)
  assert 'reveal-once' in row.get_attribute('class')
  page.locator('.activity-link').last.focus();assert page.locator('.activity-card.reveal-pending,.activity-card.reveal-once').count()<2
  page.close()
 b.close();(out/'continuity.json').write_text(json.dumps(results,indent=2))
print('PASS: no in-viewport opacitydrops, monotonic visiblefade>=230ms, firstvisiblechange and anchor preserves laterrowglides.')
