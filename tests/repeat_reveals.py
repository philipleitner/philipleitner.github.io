"""Directional replay: three passes, viewport-safe resets and reversal safety."""
import argparse,json,shutil
from pathlib import Path
from playwright.sync_api import sync_playwright
p=argparse.ArgumentParser();p.add_argument('--url',default='http://127.0.0.1:8765');p.add_argument('--artifacts',default='/tmp/repeat-reveals');a=p.parse_args();out=Path(a.artifacts);out.mkdir(parents=True,exist_ok=True)
with sync_playwright() as pw:
 b=pw.chromium.launch(executable_path=shutil.which('chromium'),args=['--no-sandbox']);results=[]
 for width in [1440,390]:
  page=b.new_page(viewport={'width':width,'height':900});page.goto(a.url);page.wait_for_timeout(1300)
  data=page.evaluate('''async()=>{
   const el=document.querySelector('#experience h2'),pause=ms=>new Promise(r=>setTimeout(r,ms));
   const top=el.getBoundingClientRect().top+scrollY;let starts=0;const fades=[];
   el.addEventListener('transitionrun',e=>{if(e.propertyName==='opacity')starts++});
   for(let pass=0;pass<3;pass++){
    scrollTo({top:top-innerHeight-150,behavior:'instant'});await pause(160);
    if(!el.classList.contains('reveal-pending'))throw Error('Not rearmed below viewport');
    const values=[];
    for(let d=0;d<=470;d+=12){scrollTo({top:top-innerHeight-150+d,behavior:'instant'});await pause(35);const r=el.getBoundingClientRect();if(r.top<innerHeight)values.push(+getComputedStyle(el).opacity)}
    await pause(1100);if(getComputedStyle(el).opacity!=='1')throw Error('Incomplete downward pass');
    if(!values.some(v=>v>.01&&v<.99))throw Error('No visible fade');fades.push(values);
    // A small reversal while still visible must never rearm or dim it.
    for(const d of [-20,15,-12,10]){scrollBy({top:d,behavior:'instant'});await pause(50);if(getComputedStyle(el).opacity!=='1')throw Error('Visible reversal reset')}
   }
   // Reverse during an actual entrance: upward visibility resolves immediately.
   scrollTo({top:top-innerHeight-150,behavior:'instant'});await pause(120);
   scrollTo({top:top-innerHeight*.86,behavior:'instant'});await pause(140);
   scrollBy({top:-5,behavior:'instant'});await pause(60);
   if(getComputedStyle(el).opacity!=='1')throw Error('Upward entrance stayed faded '+JSON.stringify({opacity:getComputedStyle(el).opacity,classes:el.className,direction:revealDirection,y:scrollY,enabled:revealEnabled}));
   // Near-bottom boundary: fully visible text cannot be reset at shortened root.
   scrollTo({top:top-innerHeight+40,behavior:'instant'});await pause(80);
   if(el.classList.contains('reveal-pending'))throw Error('Real viewport edge reset');
   scrollTo({top:top-200,behavior:'instant'});await pause(100);
   if(getComputedStyle(el).opacity!=='1')throw Error('Fast deep arrival hidden');
   return{starts,fades};}''')
  assert data['starts']>=3;results.append({'width':width,**data});page.screenshot(path=str(out/f'repeat-{width}.png'));page.close()
 b.close()
(out/'repeat-results.json').write_text(json.dumps(results,indent=2));print('PASS: three downward fades, offscreen rearming, visible reversals, upward interruption, real bottom boundary and fast arrivals on desktop/mobile.')
