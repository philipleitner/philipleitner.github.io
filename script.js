const menuButton = document.querySelector('.menu-toggle');
const navigation = document.querySelector('#navigation');
function closeMenu() {
  menuButton.setAttribute('aria-expanded', 'false');
  navigation.classList.remove('open');
}
menuButton.addEventListener('click', () => {
  const expanded = menuButton.getAttribute('aria-expanded') === 'true';
  menuButton.setAttribute('aria-expanded', String(!expanded));
  navigation.classList.toggle('open', !expanded);
});
navigation.querySelectorAll('a').forEach(link => link.addEventListener('click', closeMenu));
document.addEventListener('keydown', event => {
  if (event.key === 'Escape' && menuButton.getAttribute('aria-expanded') === 'true') {
    closeMenu();
    menuButton.focus();
  }
});
// Enable the collapsed menu only after its event handlers are installed.
document.documentElement.classList.add('menu-ready');

// Active section tracking uses IntersectionObserver, with no scroll listeners.
const sectionLinks = [...navigation.querySelectorAll('a[href^="#"]')];
function markActive(id) {
  sectionLinks.forEach(link => {
    if (link.hash === `#${id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
sectionLinks.forEach(link => link.addEventListener('click', () => markActive(link.hash.slice(1))));
if ('IntersectionObserver' in window) {
  const activeObserver = new IntersectionObserver(entries => {
    const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
    if (visible.length) markActive(visible[0].target.id);
  }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
  document.querySelectorAll('main > section').forEach(section => activeObserver.observe(section));
}

// The native ScrollTimeline owns every position. Setup/resize maps one curved
// journey to section landmarks; scroll events only select tail direction/idle.
const orbitalDecoration = document.querySelector('.orbital-decoration');
const orbitalReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (CSS.supports('animation-timeline: scroll()') && CSS.supports('offset-path: path("M0 0 L1 1")')) {
  const journeyStyles = document.createElement('style');
  document.head.append(journeyStyles);
  function measureOrbitalJourney() {
    // Read layout only during setup/font-ready/resize. Each waypoint belongs to
    // a content landmark; the browser owns interpolation during native scroll.
    const span = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    const landmarks = [...document.querySelectorAll('main > section')];
    const stops = landmarks.map((section, index) => index === 0 ? 0 :
      Math.min(.97, Math.max(0, (section.getBoundingClientRect().top + scrollY - innerHeight * .25) / span)));
    stops.push(1);
    const mobile = innerWidth <= 850;
    const layout = mobile
      ? [[.78,.34],[.12,.72],[.88,.28],[.10,.68],[.86,.38],[.12,.78],[.88,.30],[.14,.65],[.20,.60]]
      : [[.72,.43],[.48,.78],[.26,.25],[.84,.72],[.86,.35],[.48,.80],[.27,.28],[.84,.68],[.78,.60]];
    const points = layout.map(([x,y]) => [x * innerWidth,y * innerHeight]);
    let path = `M ${points[0].join(' ')}`;
    const lengths = [0];
    let total = 0;
    for (let i = 0; i < points.length - 1; i++) {
      const p0 = points[Math.max(0,i-1)], p1 = points[i], p2 = points[i+1], p3 = points[Math.min(points.length-1,i+2)];
      // Shared tangent at each landmark gives continuous broad curves.
      const limits = [[innerWidth*(mobile?.08:.24),innerWidth*(mobile?.92:.88)],[innerHeight*.20,innerHeight*.84]];
      const clamp = (v,j) => Math.max(limits[j][0],Math.min(limits[j][1],v));
      const c1 = p1.map((v,j) => clamp(v + (p2[j]-p0[j]) / 7,j));
      const c2 = p2.map((v,j) => clamp(v - (p3[j]-p1[j]) / 7,j));
      const segment = `C ${c1.join(' ')} ${c2.join(' ')} ${p2.join(' ')}`;
      path += ` ${segment}`;
      let previous = p1;
      for (let step=1;step<=80;step++) {
        const t=step/80,u=1-t;
        const next=p1.map((v,j)=>u*u*u*v+3*u*u*t*c1[j]+3*u*t*t*c2[j]+t*t*t*p2[j]);
        total += Math.hypot(next[0]-previous[0],next[1]-previous[1]);
        previous=next;
      }
      lengths.push(total);
    }
    const frames = sign => stops.map((stop,index) =>
      `${(stop*100).toFixed(4)}%{offset-distance:calc(${(lengths[index]/total*100).toFixed(5)}% ${sign} var(--trail-gap,0px))}`).join('');
    orbitalDecoration.style.setProperty('--journey-path', `path("${path}")`);
    journeyStyles.textContent = `@keyframes orbital-travel{${frames('-')}}@keyframes orbital-return-trail{${frames('+')}}`;
  }
  measureOrbitalJourney();
  window.addEventListener('resize', measureOrbitalJourney);
  document.fonts.ready.then(measureOrbitalJourney);
  document.documentElement.classList.add('orbital-ready');
  let previousOrbitalScroll = window.scrollY;
  let orbitalIdleTimer;
  window.addEventListener('scroll', () => {
    const currentScroll = window.scrollY;
    const delta = currentScroll - previousOrbitalScroll;
    if (Math.abs(delta) < 2) return;
    previousOrbitalScroll = currentScroll;
    if (orbitalReducedMotion.matches) return;
    const direction = delta < 0 ? 'reverse' : 'forward';
    if (orbitalDecoration.dataset.direction !== direction) orbitalDecoration.dataset.direction = direction;
    if (orbitalDecoration.dataset.motion !== 'moving') orbitalDecoration.dataset.motion = 'moving';
    clearTimeout(orbitalIdleTimer);
    orbitalIdleTimer = setTimeout(() => { orbitalDecoration.dataset.motion = 'idle'; }, 260);
  }, { passive: true });
}
