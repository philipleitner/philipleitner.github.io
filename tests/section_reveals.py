"""Full transition lifecycle, layout, accessibility and failure regression."""
import argparse,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/soft-reveals');a=p.parse_args();Path(a.artifacts).mkdir(parents=True,exist_ok=True)
selectors='.hero-main>.eyebrow,.hero h1,.hero-copy,.hero-links,.hero-portrait,.section-label,.section h2,.contact>.eyebrow,.contact h2,.home-places figcaption,.stamp-cell,.prose,.fact-row,.project-group-title,.project-card,.past-project-row,.experience .experience-row,.leadership>.entry-list>.experience-row,.activity-card,.certificate,.interest-grid>div,.contact-links'
with sync_playwright() as p:
 b=p.chromium.launch(executable_path=shutil.which('chromium'),headless=True,args=['--no-sandbox'])
 for width in [1440,390,320]:
  page=b.new_page(viewport={'width':width,'height':900});errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
  page.add_init_script('window.revealStarts=[];document.addEventListener("transitionrun",e=>{if(e.propertyName==="opacity"&&e.target.classList.contains("reveal-entering"))revealStarts.push(e.target)},true)')
  page.goto(a.url);page.wait_for_load_state('networkidle');page.wait_for_timeout(1200)
  before=page.evaluate('({height:document.documentElement.scrollHeight,positions:[...document.querySelectorAll("main>section")].map(e=>e.offsetTop)})')
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>!es.some(other=>other!==e&&other.contains(e)))')
  span=page.evaluate('document.documentElement.scrollHeight-innerHeight')
  for y in range(0,int(span)+600,400):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(120)
  page.wait_for_timeout(1300)
  assert page.locator('.reveal-pending,.reveal-entering').count()==0
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>getComputedStyle(e).opacity==="1"&&getComputedStyle(e).transform==="none")')
  after=page.evaluate('({height:document.documentElement.scrollHeight,positions:[...document.querySelectorAll("main>section")].map(e=>e.offsetTop)})');assert before==after
  assert page.evaluate('document.getAnimations().every(a=>a.effect.target.matches(".reading-progress>span"))')
  count=page.evaluate('revealStarts.length');assert page.evaluate('new Set(revealStarts).size===revealStarts.length')
  for y in range(int(span),-600,-600):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(50)
  assert page.evaluate('revealStarts.length')==count
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth');assert not errors,errors;page.close()
 for variant in ['nojs','reduced','unavailable','constructor','midSetup','silent','mainJSFail','failedCleanup']:
  context=b.new_context(viewport={'width':390,'height':900},java_script_enabled=variant!='nojs',reduced_motion='reduce' if variant=='reduced' else 'no-preference');page=context.new_page()
  if variant=='unavailable':page.add_init_script('delete window.IntersectionObserver')
  if variant=='constructor':page.add_init_script('window.IntersectionObserver=class{constructor(){throw new Error("failure")}}')
  if variant=='midSetup':page.add_init_script('const Native=IntersectionObserver;let n=0;window.IntersectionObserver=class extends Native{constructor(...a){super(...a);this.fail=++n===2;this.calls=0}observe(e){if(this.fail&&++this.calls===3)throw Error("failure");super.observe(e)}}')
  if variant=='silent':page.add_init_script('window.IntersectionObserver=class{observe(){}unobserve(){}disconnect(){}}')
  if variant=='mainJSFail':page.route('**/script.js*',lambda route:route.abort())
  if variant=='failedCleanup':page.add_init_script('window.addEventListener("transitionend",e=>e.stopImmediatePropagation(),true)')
  page.goto(a.url);page.wait_for_timeout(1500)
  if variant=='failedCleanup':
   span=page.evaluate('document.documentElement.scrollHeight-innerHeight')
   for y in range(0,int(span)+700,400):page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',y);page.wait_for_timeout(50)
   page.wait_for_timeout(1400)
  assert page.locator('.reveal-pending,.reveal-entering').count()==0,variant
  assert page.locator(selectors).evaluate_all('(es)=>es.every(e=>getComputedStyle(e).opacity==="1")'),variant
  context.close()
 page=b.new_page(viewport={'width':390,'height':900});page.goto(a.url);page.wait_for_load_state('networkidle');page.evaluate('scrollTo({top:document.querySelector("#experience").offsetTop-400,behavior:"instant"})');page.wait_for_timeout(50);page.emulate_media(reduced_motion='reduce');page.wait_for_timeout(50);assert page.locator('.reveal-pending,.reveal-entering').count()==0
 b.close()
print('PASS: full down/up, completed transitions/upward visibility/layoutshift,320overflow, noJS/reduced/IO/setup/silent/mainJS/cleanupfailure safety.')
