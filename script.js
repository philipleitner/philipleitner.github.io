// A real refresh starts a new visit at the introduction. Fresh deep links and
// ordinary anchor/back navigation retain their native browser behavior.
if (performance.getEntriesByType('navigation')[0]?.type === 'reload') {
  const previousRestoration = history.scrollRestoration;
  history.scrollRestoration = 'manual';
  if (location.hash) history.replaceState(history.state, '', location.pathname + location.search);
  window.addEventListener('pageshow', () => {
    window.scrollTo({ top: 0, behavior: 'instant' });
    requestAnimationFrame(() => {
      window.scrollTo({ top: 0, behavior: 'instant' });
      history.scrollRestoration = previousRestoration;
    });
  }, { once: true });
}

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
if (typeof window.IntersectionObserver === 'function') {
  try {
    const activeObserver = new IntersectionObserver(entries => {
      const visible = entries.filter(entry => entry.isIntersecting).sort((a, b) => a.boundingClientRect.top - b.boundingClientRect.top);
      if (visible.length) markActive(visible[0].target.id);
    }, { rootMargin: '-15% 0px -55% 0px', threshold: 0 });
    document.querySelectorAll('main > section').forEach(section => activeObserver.observe(section));
  } catch { /* Anchor clicks still track navigation if observer setup fails. */ }
}

// One reusable transition observer. Only safely prepared targets become
// transparent; late or uncertain initialization keeps visible content visible.
const revealMotion = matchMedia('(prefers-reduced-motion: reduce)');
const revealGroups = [
  ['.hero-main>.eyebrow,.section-label,.contact>.eyebrow',0,false],
  ['.hero h1,.section h2,.contact h2',80,false],
  ['.hero-copy',160,false], ['.hero-links',240,false], ['.hero-portrait',160,false],
  ['.home-places figcaption',80,false], ['.stamp-cell',0,true],
  ['.prose,.fact-row',160,false], ['.project-group-title',80,false],
  ['.project-card',160,false], ['.past-project-row',0,true],
  ['.experience .experience-row',0,true], ['.leadership>.entry-list>.experience-row',0,true],
  ['.activity-card',0,true], ['.certificate',0,true], ['.interest-grid>div',0,true],
  ['.contact-links',160,false]
];
const revealTargets = [];
revealGroups.forEach(([selector, base, stagger]) => {
  document.querySelectorAll(selector).forEach((element,index) => {
    if (revealTargets.includes(element)) return;
    element.style.setProperty('--reveal-base-delay', `${base}ms`);
    element.style.setProperty('--reveal-order', stagger ? index : 0);
    revealTargets.push(element);
  });
});
const revealed = new WeakSet();
const activeReveals = new Set();
const initialReveals = new Set();
const revealTimers = new WeakMap();
let revealObserver;
let revealHeight = innerHeight;
function finishReveal(element) {
  revealed.add(element);
  initialReveals.delete(element);
  revealObserver?.unobserve?.(element);
  element.removeEventListener('transitionend', revealEnded);
  element.removeEventListener('transitioncancel', revealEnded);
  clearTimeout(revealTimers.get(element));
  element.classList.remove('reveal-pending','reveal-entering');
  activeReveals.delete(element);
}
function revealEnded(event) {
  if (event.target === event.currentTarget && event.propertyName === 'opacity') finishReveal(event.currentTarget);
}
function resetReveals() {
  revealTargets.forEach(finishReveal);
  revealObserver?.disconnect?.();
}
function enterReveal(element) {
  if (revealed.has(element)) return;
  if (revealMotion.matches || element.contains(document.activeElement)) { finishReveal(element); return; }
  revealed.add(element);
  initialReveals.delete(element);
  revealObserver?.unobserve?.(element);
  activeReveals.add(element);
  element.addEventListener('transitionend', revealEnded);
  element.addEventListener('transitioncancel', revealEnded);
  element.classList.replace('reveal-pending','reveal-entering');
  // Finite cleanup fallback; the entering state itself is already fully visible.
  revealTimers.set(element,setTimeout(() => finishReveal(element),1250));
}
function connectRevealObserver() {
  let responded = false;
  const observer = new IntersectionObserver(entries => {
    responded = true;
    try { entries.forEach(entry => {
      if (!entry.isIntersecting || revealed.has(entry.target)) return;
      if (entry.boundingClientRect.top < innerHeight*.5 && !initialReveals.has(entry.target)) finishReveal(entry.target);
      else enterReveal(entry.target);
    }); }
    catch { resetReveals(); }
  }, { rootMargin: `0px 0px -${Math.round(innerHeight*.12)}px 0px`, threshold: 0 });
  setTimeout(() => { if (revealObserver === observer && !responded) resetReveals(); },1000);
  return observer;
}
function destinationFor(hash) {
  try { return document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return null; }
}
function finishDestination(hash, arrival = false) {
  const destination = destinationFor(hash);
  if (!destination) return;
  const heading = destination.matches('section') ? destination.querySelector('h2') : null;
  const visibleArrival = arrival ? revealTargets.filter(element => {
    if (!destination.contains(element)) return false;
    const rect = element.getBoundingClientRect();
    return rect.top < innerHeight && rect.bottom > 0;
  }) : [];
  revealTargets.forEach(element => {
    if (element.contains(destination) || element === heading || visibleArrival.includes(element)) finishReveal(element);
  });
}
if (typeof window.IntersectionObserver === 'function' && !revealMotion.matches) {
  try {
    revealObserver = connectRevealObserver();
    if (location.hash) finishDestination(location.hash);
    revealTargets.forEach(element => { if (!revealed.has(element)) revealObserver.observe(element); });
    // Paint Timing support is required: an empty unsupported API is not proof
    // that users have never seen this content. Late initialization stays static.
    const early = typeof PerformanceObserver === 'function' &&
      PerformanceObserver.supportedEntryTypes?.includes('paint') &&
      performance.getEntriesByType('paint').length === 0;
    const positions = revealTargets.map(element => ({element,rect:element.getBoundingClientRect()}));
    const initial = [];
    positions.forEach(({element,rect}) => {
      if (revealed.has(element)) return;
      if (rect.bottom <= 0 || (rect.top < innerHeight && !early)) finishReveal(element);
      else {
        element.classList.add('reveal-pending');
        if (rect.top < innerHeight) { initial.push(element); initialReveals.add(element); }
      }
    });
    if (initial.length) requestAnimationFrame(() => {
      try {
        initial.forEach(element => getComputedStyle(element).opacity);
        initial.forEach(enterReveal);
      } catch { resetReveals(); }
    });
  } catch { resetReveals(); }
}
// Anchors/focus resolve immediately. Only visible arrival groups are completed;
// entries further down the destination section retain their natural entrance.
let arrivalTimer;
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (!link) return;
  finishDestination(link.hash);
  clearTimeout(arrivalTimer);
  arrivalTimer = setTimeout(() => finishDestination(link.hash,true),750);
});
window.addEventListener('hashchange', () => {
  finishDestination(location.hash);
  clearTimeout(arrivalTimer);
  arrivalTimer = setTimeout(() => finishDestination(location.hash,true),750);
});
window.addEventListener('pageshow', () => { if (location.hash) finishDestination(location.hash,true); });
document.addEventListener('focusin', event => {
  revealTargets.forEach(element => { if (element.contains(event.target)) finishReveal(element); });
});
revealMotion.addEventListener('change', event => { if (event.matches) resetReveals(); });
let revealResizeTimer;
window.addEventListener('resize', () => {
  if (!revealObserver || revealMotion.matches || Math.abs(innerHeight-revealHeight)<80) return;
  clearTimeout(revealResizeTimer);
  revealResizeTimer = setTimeout(() => {
    try {
      revealHeight=innerHeight;
      revealObserver.disconnect();
      revealObserver=connectRevealObserver();
      revealTargets.forEach(element => { if (!revealed.has(element)) revealObserver.observe(element); });
    } catch { resetReveals(); }
  },150);
});
