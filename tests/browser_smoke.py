"""Local portfolio regression checks. Requires existing Python Playwright + Chromium."""
import argparse
from pathlib import Path
import shutil
from playwright.sync_api import sync_playwright

parser = argparse.ArgumentParser()
parser.add_argument('--url', default='http://127.0.0.1:8765')
parser.add_argument('--artifacts', default='/tmp/portfolio-checks')
args = parser.parse_args()
artifacts = Path(args.artifacts)
artifacts.mkdir(parents=True, exist_ok=True)

with sync_playwright() as p:
    executable = shutil.which('chromium') or shutil.which('chromium-browser')
    assert executable, 'System Chromium is required; no browser was installed automatically.'
    browser = p.chromium.launch(executable_path=executable, headless=True, args=['--no-sandbox'])
    page = browser.new_page()
    errors = []
    failed_assets = []
    page.on('pageerror', lambda error: errors.append(str(error)))
    page.on('response', lambda response: failed_assets.append(response.url) if response.status >= 400 else None)
    page.goto(args.url)
    page.wait_for_load_state('networkidle')
    assert page.locator('.journey-star,.star-layer,.journey-ribbon').count() == 0
    assert page.locator('.project-card').count() == 1
    assert page.locator('.project-card .badge').inner_text() == 'In progress'
    assert page.locator('.credential-link').count() == 2
    assert page.locator('.reading-pending').inner_text() == 'Reading List — coming soon'
    for width in [320, 375, 390, 600, 768, 850, 1024, 1440, 1920, 2048]:
        page.set_viewport_size({'width': width, 'height': 900})
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth'), f'Overflow at {width}'
        boxes = page.locator('main > section').evaluate_all('(els) => els.map(e => {const r=e.getBoundingClientRect();return {top:r.top,bottom:r.bottom,position:getComputedStyle(e).position}})')
        for previous, current in zip(boxes, boxes[1:]):
            assert current['top'] >= previous['bottom'], f'Overlapping sections at {width}'
            assert current['position'] not in ['sticky', 'fixed', 'absolute']
    for width in [1440, 1920, 2048]:
        page.set_viewport_size({'width': width, 'height': 900})
        logo = page.locator('.site-header .wordmark').bounding_box()
        action = page.locator('nav .nav-contact').bounding_box()
        assert abs(logo['x'] - width * .04) <= 1, f'Unexpected logo inset at {width}'
        assert abs(width - action['x'] - action['width'] - width * .04) <= 1, f'Navigation is not right aligned at {width}'
    assert page.locator('.entry-list h3').first.evaluate('(e)=>getComputedStyle(e).color') == 'rgb(169, 35, 11)'
    assert page.locator('.entry-list').first.evaluate('(e)=>getComputedStyle(e).borderLeftColor') == 'rgb(255, 43, 6)'
    page.set_viewport_size({'width': 1440, 'height': 900})
    supported = page.evaluate("CSS.supports('animation-timeline: scroll()')")
    if supported:
        scales = []
        for progress in [0, .25, .5, .75, 1]:
            page.evaluate('(p) => scrollTo({top:(document.documentElement.scrollHeight-innerHeight)*p,behavior:"instant"})', progress)
            page.wait_for_timeout(120)
            scale = page.locator('.reading-progress > span').evaluate('(e) => new DOMMatrixReadOnly(getComputedStyle(e).transform).a')
            assert abs(scale - progress) < .025, f'Incorrect reading progress: {progress}/{scale}'
            scales.append(scale)
        assert scales == sorted(scales)
        page.evaluate('scrollTo({top:0,behavior:"instant"})')
        page.wait_for_timeout(120)
        before = page.locator('.art-monogram').evaluate('(e)=>getComputedStyle(e).transform')
        page.evaluate('scrollTo({top:450,behavior:"instant"})')
        page.wait_for_timeout(120)
        assert page.locator('.art-monogram').evaluate('(e)=>getComputedStyle(e).transform') != before
    else:
        print('LIMITATION: Chromium lacks native scroll timelines; static fallback checked.')
    for width, name in [(1440, 'desktop'), (390, 'mobile')]:
        page.set_viewport_size({'width': width, 'height': 900})
        for section, suffix in [('home', 'intro'), ('projects', 'projects'), ('training', 'credentials')]:
            page.evaluate('(id)=>scrollTo({top:Math.max(0,document.getElementById(id).getBoundingClientRect().top+scrollY-120),behavior:"instant"})', section)
            page.wait_for_timeout(150)
            page.screenshot(path=str(artifacts / f'{name}-{suffix}.png'))
    assert page.locator('.art-monogram').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
    page.get_by_role('button', name='Menu').click()
    page.locator('nav a[href="#training"]').click()
    page.wait_for_timeout(900)
    assert page.get_by_role('button', name='Menu').get_attribute('aria-expanded') == 'false'
    assert page.locator('#training h2').bounding_box()['y'] >= page.locator('header').bounding_box()['height']
    page.get_by_role('button', name='Menu').click()
    page.keyboard.press('Escape')
    assert page.get_by_role('button', name='Menu').get_attribute('aria-expanded') == 'false'
    for href in page.locator('a[href^="#"]').evaluate_all('(els)=>els.map(e=>e.hash)'):
        assert page.locator(href).count() == 1, f'Broken section anchor {href}'
    assert page.get_by_role('link', name='View CV', exact=True).get_attribute('target') == '_blank'
    pdf = page.request.get(args.url + '/assets/philip-leitner-cv.pdf')
    assert pdf.status == 200 and pdf.body().startswith(b'%PDF')
    assert page.request.get(args.url + '/assets/favicon.svg').status == 200
    for selector in ['.button', '.credential-link', '.contact-link']:
        link = page.locator(selector).first
        link.hover()
        page.wait_for_timeout(250)
        hover = link.evaluate('(e)=>getComputedStyle(e).backgroundColor')
        page.mouse.move(0, 0)
        link.focus()
        page.wait_for_timeout(250)
        assert link.evaluate('(e)=>getComputedStyle(e).backgroundColor') == hover
    page.goto(args.url)
    page.keyboard.press('Tab')
    assert page.locator(':focus').inner_text() == 'Skip to content'
    page.keyboard.press('Enter')
    assert page.url.endswith('#main')
    page.emulate_media(reduced_motion='reduce')
    page.set_viewport_size({'width': 1440, 'height': 900})
    assert not page.locator('.reading-progress').is_visible()
    assert page.locator('.art-monogram').evaluate('(e)=>getComputedStyle(e).animationName') == 'none'
    assert page.locator('html').evaluate('(e)=>getComputedStyle(e).scrollBehavior') == 'auto'
    plain = browser.new_context(java_script_enabled=False, viewport={'width': 390, 'height': 844})
    plain_page = plain.new_page()
    plain_page.goto(args.url)
    assert plain_page.locator('nav').is_visible()
    assert plain_page.locator('.project-card').evaluate('(e)=>getComputedStyle(e).opacity') == '1'
    def serve_subpath(route):
        suffix = route.request.url.split('/portfolio/', 1)[1]
        route.fulfill(response=page.request.get(args.url + '/' + suffix))
    page.route('**/portfolio/**', serve_subpath)
    page.goto(args.url + '/portfolio/')
    assert page.evaluate("async () => (await fetch(document.querySelector('.hero-links a').href)).status") == 200
    assert page.evaluate("async () => (await fetch(document.querySelector('link[rel=icon]').href)).status") == 200
    assert not errors, errors
    assert not failed_assets, failed_assets
    browser.close()
print('PASS: ten widths, right-aligned wide navigation, orange-red entry accents, normal-flow sections, native scroll motion, mobile/static/reduced-motion fallbacks, navigation, hover/focus, no-JS content, PDF/favicon, no browser errors.')
