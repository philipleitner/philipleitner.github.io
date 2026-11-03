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

// The native ScrollTimeline owns every position. JS measures travel once per
// resize and only changes the tail side when actual scroll direction reverses.
const orbitalDecoration = document.querySelector('.orbital-decoration');
const orbitalReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if (CSS.supports('animation-timeline: scroll()') && CSS.supports('offset-path: ellipse(50% 50% at 50% 50%)')) {
  function measureOrbitalTravel() {
    const viewportSpan = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    // Calibration: one shallow orbit per 1.7 viewport heights, not per section.
    const turns = Math.max(2, viewportSpan / (innerHeight * 1.7));
    orbitalDecoration.style.setProperty('--orbit-travel', `${turns * 100}%`);
  }
  measureOrbitalTravel();
  window.addEventListener('resize', measureOrbitalTravel);
  document.fonts.ready.then(measureOrbitalTravel);
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
