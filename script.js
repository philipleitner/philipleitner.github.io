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

// Adapted from the earlier reveal-once observer: finite effects on independent
// targets only. Content is visible before setup, after completion and on failure.
const revealMotion = matchMedia('(prefers-reduced-motion: reduce)');
const revealGroups = [
  '.section h2, .contact h2', '.home-places, .about-story', '.project-card',
  '.past-project-row', '.experience .experience-row',
  '.leadership > .entry-list > .experience-row', '.activity-card',
  '.certificate', '.interest-grid > div', '.contact-links'
];
const revealTargets = [];
revealGroups.forEach((selector, groupIndex) => {
  document.querySelectorAll(selector).forEach((element, index) => {
    if (revealTargets.includes(element)) return;
    element.style.setProperty('--reveal-order', groupIndex === 0 ? 0 : index);
    if (element.matches('h2')) element.classList.add('reveal-heading');
    revealTargets.push(element);
  });
});
const revealed = new WeakSet();
const activeReveals = new Set();
let revealObserver;
function finishReveal(element) {
  revealed.add(element);
  revealObserver?.unobserve(element);
  element.classList.remove('reveal-once');
  element.removeEventListener('animationend', revealEnded);
  activeReveals.delete(element);
}
function revealEnded(event) {
  if (event.target === event.currentTarget && event.animationName === 'gentle-reveal') finishReveal(event.currentTarget);
}
function finishDestination(hash) {
  let destination;
  try { destination = document.getElementById(decodeURIComponent(hash.slice(1))); } catch { return; }
  if (!destination) return;
  revealTargets.forEach(element => {
    if (destination.contains(element) || element.contains(destination)) finishReveal(element);
  });
}
if (typeof window.IntersectionObserver === 'function' && !revealMotion.matches) {
  try {
    revealObserver = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        const element = entry.target;
        if (!entry.isIntersecting || revealed.has(element)) return;
        revealed.add(element);
        revealObserver.unobserve(element);
        if (revealMotion.matches || element.contains(document.activeElement)) return;
        activeReveals.add(element);
        element.addEventListener('animationend', revealEnded);
        element.classList.add('reveal-once');
      });
    }, { rootMargin: '0px 0px 80px 0px', threshold: .01 });
    if (location.hash) finishDestination(location.hash);
    revealTargets.forEach(element => { if (!revealed.has(element)) revealObserver.observe(element); });
  } catch {
    revealTargets.forEach(element => {
      revealed.add(element);
      element.classList.remove('reveal-once');
      element.removeEventListener('animationend', revealEnded);
    });
    activeReveals.clear();
    revealObserver?.disconnect();
  }
}
// Navigation and keyboard focus never wait for a staggered entrance.
document.addEventListener('click', event => {
  const link = event.target.closest('a[href^="#"]');
  if (link) finishDestination(link.hash);
});
window.addEventListener('hashchange', () => finishDestination(location.hash));
document.addEventListener('focusin', event => {
  revealTargets.forEach(element => { if (element.contains(event.target)) finishReveal(element); });
});
revealMotion.addEventListener('change', event => {
  if (!event.matches) return;
  revealObserver?.disconnect();
  [...activeReveals].forEach(finishReveal);
});
