from pathlib import Path
import argparse,shutil
parser=argparse.ArgumentParser();parser.add_argument('--url',default='http://127.0.0.1:8765');parser.add_argument('--artifacts',default='/tmp/portfolio-section-reveals');args=parser.parse_args()
from playwright.sync_api import sync_playwright
out=Path(args.artifacts);out.mkdir(parents=True,exist_ok=True)
selectors='.section h2,.contact h2,.home-places,.about-story,.project-card,.past-project-row,.experience .experience-row,.leadership>.entry-list>.experience-row,.activity-card,.certificate,.interest-grid>div,.contact-links'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.revealStarts=[];document.addEventListener("animationstart",e=>{if(e.animationName==="gentle-reveal")window.revealStarts.push(e.target.tagName+"."+e.target.className)},true)')
  page.goto(args.url);page.wait_for_load_state('networkidle')
  before=page.evaluate('({height:document.documentElement.scrollHeight,positions:[...document.querySelectorAll("main>section")].map(e=>e.offsetTop)})')
  targets=page.locator(selectors).count()
  expected=page.locator('.reveal-pending').count()+len(page.evaluate('revealStarts'))
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>!es.some(other=>other!==e&&other.contains(e)))'),'Nested reveal targets'
  span=page.evaluate('document.documentElement.scrollHeight-innerHeight')
  for y in range(0,int(span)+600,500):
   page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(130)
  page.wait_for_timeout(950)
  assert len(page.evaluate('revealStarts'))==expected,(width,targets,page.evaluate('revealStarts'))
  after=page.evaluate('({height:document.documentElement.scrollHeight,positions:[...document.querySelectorAll("main>section")].map(e=>e.offsetTop)})');assert before==after
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>getComputedStyle(e).opacity==="1"&&getComputedStyle(e).transform==="none")')
  assert page.evaluate('document.getAnimations().every(a=>a.effect.target.matches(".reading-progress>span"))')
  for y in range(int(span),-600,-500):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(40)
  page.wait_for_timeout(100)
  assert len(page.evaluate('revealStarts'))==expected,'Entrance replayed on upward return'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.locator('nav a[href="#projects"]').evaluate('(e)=>e.click()');page.wait_for_timeout(850)
  assert page.locator('#projects').bounding_box()['y']>=page.locator('header').bounding_box()['height']
  assert page.locator('#projects .reveal-once').count()==0
  page.locator('.credential-link').first.focus();assert page.locator('.certificate.reveal-once').count()==0
  assert not errors,errors
  page.close()
 for variant in ['nojs','reduced','unavailable','failure','midSetupFailure','silentObserver','failedCleanup']:
  context=b.new_context(viewport={'width':390,'height':900},java_script_enabled=variant!='nojs',reduced_motion='reduce' if variant=='reduced' else 'no-preference');page=context.new_page()
  if variant=='unavailable':page.add_init_script('delete window.IntersectionObserver')
  if variant=='failure':page.add_init_script('window.IntersectionObserver=class{constructor(){throw new Error("simulated observer failure")}}')
  if variant=='midSetupFailure':page.add_init_script('const Native=window.IntersectionObserver;let created=0;window.IntersectionObserver=class extends Native{constructor(...args){super(...args);this.fail=++created===2;this.calls=0;}observe(e){if(this.fail&&++this.calls===3)throw new Error("simulated observe failure");return super.observe(e)}}')
  if variant=='silentObserver':page.add_init_script('window.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}}')
  if variant=='failedCleanup':page.add_init_script('window.addEventListener("animationend",e=>e.stopImmediatePropagation(),true)')
  page.goto(args.url);page.wait_for_load_state('networkidle')
  if variant=='silentObserver':page.wait_for_timeout(1100)
  if variant=='failedCleanup':
   span=page.evaluate('document.documentElement.scrollHeight-innerHeight')
   for y in range(0,int(span)+700,500):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(50)
   page.wait_for_timeout(1000)
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>getComputedStyle(e).opacity==="1")'),variant
  if variant!='failedCleanup':assert page.locator('.reveal-once').count()==0,variant
  else:assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>getComputedStyle(e).transform==="none")')
  context.close()
 # Runtime preference changes immediately clear active entrances.
 page=b.new_page(viewport={'width':390,'height':900});page.goto(args.url);page.wait_for_load_state('networkidle');page.evaluate('scrollTo({top:document.querySelector("#experience").offsetTop-300,behavior:"instant"})');page.wait_for_timeout(60);page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(50);assert page.locator('.reveal-once').count()==0
 b.close()
print('PASS: full down/up, eachtarget enters once, no nested effects/layoutshift/ongoingeffects, anchors/focus, noJS/reduced/IO-unavailable/failure visibility and runtime reduction.')
