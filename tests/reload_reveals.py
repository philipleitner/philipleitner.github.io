"""Actual reloads must arm a fresh once-only reveal lifetime at scroll zero."""
import argparse,shutil,json,time
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/reload-reveals');a=p.parse_args();out=Path(a.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);results=[]
 for width in [1440,390,320]:
  page=b.new_page(viewport={'width':width,'height':900});page.add_init_script('window.headingStarts=0;document.addEventListener("transitionrun",e=>{if(e.propertyName==="opacity"&&e.target.matches("#experience h2"))headingStarts++},true)');page.goto(a.url);page.wait_for_timeout(1200)
  for mode in ['middle-warm','bottom-hash','delayed-script','restored-position-race']:
   page.evaluate('(mode)=>{history.replaceState(null,"",mode.includes("hash")?"#contact":location.pathname);scrollTo({top:mode==="middle-warm"?document.documentElement.scrollHeight*.5:document.documentElement.scrollHeight,behavior:"instant"})}',mode)
   if mode in ['delayed-script','restored-position-race']:
    def route(r):
     time.sleep(.25);response=r.fetch();body=response.text()
     if mode=='restored-position-race':body='if(performance.getEntriesByType("navigation")[0]?.type==="reload")scrollTo({top:document.documentElement.scrollHeight*.6,behavior:"instant"});\n'+body
     r.fulfill(response=response,body=body)
    page.route('**/script.js*',route)
   if mode=='delayed-script':page.route('**/philip-leitner-portrait.webp',lambda r:(time.sleep(.2),r.continue_()))
   page.reload();page.wait_for_timeout(1300)
   assert page.evaluate('scrollY')==0,(width,mode,'not top')
   assert page.evaluate('location.hash')=='',(width,mode,'hash retained')
   assert 'reveal-pending' in page.locator('#experience h2').get_attribute('class'),(width,mode,'not armed')
   data=page.evaluate('''async()=>{const e=document.querySelector('#experience h2'),top=e.getBoundingClientRect().top+scrollY;const wait=ms=>new Promise(r=>setTimeout(r,ms));for(let pass=0;pass<2;pass++){scrollTo({top:top-innerHeight-140,behavior:'instant'});await wait(80);for(let d=0;d<=450;d+=25){scrollTo({top:top-innerHeight-140+d,behavior:'instant'});await wait(20)}await wait(1000);if(getComputedStyle(e).opacity!=='1')throw Error('not visible')}return headingStarts}''')
   assert data==1,(width,mode,data)
   results.append({'width':width,'mode':mode,'starts':data});page.unroute('**/script.js*');page.unroute('**/philip-leitner-portrait.webp')
  page.screenshot(path=str(out/f'reload-{width}.png'));page.close()
 b.close()
(out/'results.json').write_text(json.dumps(results,indent=2));print('PASS: actual middle/bottom/hash/warm/delayed/race reloads at1440/390/320 reset top and produce one fresh entrance; second pass never replays.')
