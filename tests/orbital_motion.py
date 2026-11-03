"""Section-mapped journey checks; no pixel-exact claims about the reference."""
import argparse
from pathlib import Path
import shutil
import json
import math
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:8765')
parser.add_argument('--artifacts', default='/tmp/portfolio-orbit')
args = parser.parse_args()
out = Path(args.artifacts)
out.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    browser = p.chromium.launch(executable_path=shutil.which('chromium'), headless=True, args=['--no-sandbox'])
    page = browser.new_page()
    errors = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.goto(args.url)
    page.wait_for_load_state('networkidle')
    assert page.locator('.orbital-spark').count() == 1
    assert page.locator('.orbital-trail-dot').count() == 6
    assert page.locator('.orbital-decoration').get_attribute('aria-hidden') == 'true'
    assert page.locator('.orbital-decoration').evaluate('(e)=>getComputedStyle(e).pointerEvents') == 'none'
    assert page.locator('.orbital-spark').evaluate('(e)=>getComputedStyle(e).offsetRotate') == '0deg'
    supported = page.evaluate("CSS.supports('animation-timeline: scroll()') && CSS.supports('offset-path: path(\"M0 0 L1 1\")')")
    if not supported:
        assert page.locator('.orbital-spark').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
        print('LIMITATION: native scroll-path unsupported; verified static fallback only.')
    else:
        for width, mode in [(1440, 'desktop'), (390, 'mobile')]:
            page.set_viewport_size({'width': width, 'height': 900})
            page.wait_for_timeout(200)
            max_scroll = page.evaluate('document.documentElement.scrollHeight-innerHeight')
            before_boxes = page.locator('main>section').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().top+scrollY)')
            positions = []
            covered = 0
            for scroll in range(0, int(max_scroll), 90):
                page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})', scroll)
                page.wait_for_timeout(35)
                state = page.locator('.orbital-spark').evaluate('''(e)=>{
                    const r=e.getBoundingClientRect();const v=e.querySelector('path').getBoundingClientRect();
                    const top=document.elementFromPoint(r.x+r.width/2,r.y+r.height/2);
                    return {x:r.x+r.width/2,y:r.y+r.height/2,width:getComputedStyle(e).width,
                      visibleWidth:v.width,opacity:getComputedStyle(e).opacity,distance:getComputedStyle(e).offsetDistance,
                      covered:!!top?.closest('.entry-list,.project-card')};}''')
                assert state['width'] == ('40px' if width == 1440 else '28px')
                assert state['opacity'] == '1'
                assert 0 < state['x'] < width and 85 < state['y'] < 900, (scroll,state)
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                positions.append((state['x'], state['y']))
                covered += int(state['covered'])
                current = page.locator('main>section').evaluate_all('(es)=>es.map(e=>e.getBoundingClientRect().top+scrollY)')
                assert all(abs(a-b)<1 for a,b in zip(before_boxes,current)), 'Section moved out of natural flow'
            assert max(x for x,y in positions)-min(x for x,y in positions) > width*.50
            assert max(y for x,y in positions)-min(y for x,y in positions) > 900*.40
            # Probe small increments separately: coarse 90px steps can cross a
            # short final section quickly without constituting a teleport.
            for target in range(0,int(max_scroll)-5,180):
                page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',target)
                page.wait_for_timeout(45)
                a=page.locator('.orbital-spark').bounding_box()
                page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',target+5)
                page.wait_for_timeout(45)
                b=page.locator('.orbital-spark').bounding_box()
                assert math.hypot(a['x']-b['x'],a['y']-b['y']) < 35, (target,a,b)
            print(mode, 'coordinate ranges', [min(x for x,y in positions),max(x for x,y in positions),min(y for x,y in positions),max(y for x,y in positions)], 'glass-surface crossings', covered, '/', len(positions))
            (out/f'{mode}-positions.json').write_text(json.dumps(positions))
            # A former 1.7-viewport interval must not just repeat the same lane.
            assert sum(math.dist(a,b) > 100 for a,b in zip(positions,positions[17:])) > 10
            assert covered, 'Journey did not pass beneath any content surfaces'
            # Reversing changes tail direction, not the star position at a given offset.
            for target in [450, 1200, 2200]:
                page.evaluate('(y)=>scrollTo({top:y-150,behavior:"instant"})',target)
                page.wait_for_timeout(80)
                page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',target)
                page.wait_for_timeout(120)
                forward = page.locator('.orbital-spark').bounding_box()
                assert page.locator('.orbital-decoration').get_attribute('data-direction') == 'forward'
                forward_tail = page.locator('.orbital-trail-dot').last.evaluate('(e)=>getComputedStyle(e).offsetDistance')
                page.evaluate('(y)=>scrollTo({top:y+150,behavior:"instant"})',target)
                page.wait_for_timeout(80)
                page.evaluate('(y)=>scrollTo({top:y,behavior:"instant"})',target)
                page.wait_for_timeout(120)
                reverse = page.locator('.orbital-spark').bounding_box()
                assert page.locator('.orbital-decoration').get_attribute('data-direction') == 'reverse'
                assert abs(reverse['x']-forward['x'])<.5 and abs(reverse['y']-forward['y'])<.5
                reverse_tail = page.locator('.orbital-trail-dot').last.evaluate('(e)=>getComputedStyle(e).offsetDistance')
                assert forward_tail != reverse_tail
            held = page.locator('.orbital-spark').bounding_box()
            page.wait_for_timeout(650)
            assert page.locator('.orbital-spark').bounding_box() == held
            for amount,label in [(0,'01-top'),(.15,'02-about'),(.30,'03-projects'),(.45,'04-experience'),(.60,'05-leadership'),(.75,'06-certifications'),(.90,'07-interests'),(1,'08-bottom')]:
                page.evaluate('(a)=>scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*a,behavior:"instant"})',amount)
                page.wait_for_timeout(200)
                page.screenshot(path=str(out/f'{mode}-{label}.png'))
        page.wait_for_timeout(500)
        assert float(page.locator('.orbital-trail-dot').last.evaluate('(e)=>getComputedStyle(e).opacity')) == 0
        assert page.locator('.orbital-spark').evaluate('(e)=>getComputedStyle(e).opacity') == '1'
        page.emulate_media(reduced_motion='reduce')
        page.wait_for_timeout(150)
        assert page.locator('.orbital-spark').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
        assert not page.locator('.orbital-trail-dot').first.is_visible()
        static = page.locator('.orbital-spark').bounding_box()
        page.evaluate('scrollTo({top:800,behavior:"instant"})')
        page.wait_for_timeout(150)
        assert page.locator('.orbital-spark').bounding_box() == static
    nojs = browser.new_context(java_script_enabled=False,viewport={'width':390,'height':844})
    plain = nojs.new_page()
    plain.goto(args.url)
    assert plain.locator('.orbital-spark').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
    assert not plain.locator('.orbital-trail-dot').first.is_visible()
    assert plain.locator('nav').is_visible()
    assert not errors, errors
    browser.close()
print('PASS: one native broad non-repeating journey, small constant star, no automatic tangent rotation, full-page desktop/mobile sampling, normal flow, natural glass-surface crossings, direction-aware trail, reversible star positions, reduced-motion/no-JS static fallbacks.')
