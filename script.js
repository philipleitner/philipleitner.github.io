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

const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
if ('IntersectionObserver' in window && !reduceMotion.matches) {
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('reveal-once');
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });
  document.querySelectorAll('.section h2, .project-card, .past-project-row, .fact-row, .experience-row, .activity-card, .certificate, .interest-grid > div, .contact h2, .contact-links').forEach((element, index) => {
    element.style.setProperty('--reveal-delay', `${(index % 3) * 55}ms`);
    observer.observe(element);
  });
}

// Native scrolling is untouched; only the decorative background receives depth.
const drift = document.querySelector('.background-drift');
const wideScreen = window.matchMedia('(min-width: 851px)');
let backgroundFrame = 0;
function updateBackground() {
  backgroundFrame = 0;
  const offset = !reduceMotion.matches && wideScreen.matches ? Math.min(window.scrollY * 0.035, 120) : 0;
  drift.style.transform = `translate3d(0, ${-offset}px, 0)`;
}
function queueBackground() {
  if (!backgroundFrame) backgroundFrame = window.requestAnimationFrame(updateBackground);
}
window.addEventListener('scroll', queueBackground, { passive: true });
wideScreen.addEventListener('change', queueBackground);
reduceMotion.addEventListener('change', queueBackground);
updateBackground();
