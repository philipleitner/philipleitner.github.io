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

// One small star follows whitespace corridors, never section contents.
const star = document.querySelector('.journey-star');
const sections = [...document.querySelectorAll('main > section')];
const sectionLinks = [...navigation.querySelectorAll('a[href^="#"]')];
let crossings = [];
let starFrame = 0;
let measurementFrame = 0;
let starLayout = {};
const smooth = t => t * t * (3 - 2 * t);
const mix = (a, b, t) => a + (b - a) * t;

function measureStar() {
  const compact = innerWidth <= 850;
  const size = compact ? 28 : 44;
  // Side corridors sit outside text and controls. Crossings use measured gaps.
  const edge = compact ? 16 : Math.max(25, (innerWidth - 1240) / 2 - 36);
  const left = edge;
  const right = innerWidth - edge;
  const height = innerHeight;
  const bounds = sections.map(section => {
    const rect = section.getBoundingClientRect();
    return { top: rect.top + scrollY, bottom: rect.bottom + scrollY };
  });
  crossings = bounds.slice(1).map((section, index) => {
    const previous = bounds[index];
    const gap = (previous.bottom + section.top) / 2;
    const oldSide = compact ? Math.floor(index / 2) % 2 : index % 2;
    const newSide = compact ? Math.floor((index + 1) / 2) % 2 : (index + 1) % 2;
    return { start: gap - height * .68, end: gap - height * .32, gap,
      from: oldSide ? left : right, to: newSide ? left : right };
  });
  starLayout = { left, right, size, height };
  updateStar();
}

function updateStar() {
  starFrame = 0;
  if (!starLayout.size) return;
  const { right, size, height } = starLayout;
  let x = right;
  let y = height * .36;
  let previousEnd = 0;
  let previousY = y;
  for (const crossing of crossings) {
    if (scrollY < crossing.start) {
      const t = Math.max(0, Math.min(1, (scrollY - previousEnd) / Math.max(1, crossing.start - previousEnd)));
      y = mix(previousY, height * .68, smooth(t));
      break;
    }
    if (scrollY <= crossing.end) {
      const t = Math.max(0, Math.min(1, (scrollY - crossing.start) / (crossing.end - crossing.start)));
      // Smooth horizontal acceleration; the world-space Y remains in the gap.
      x = mix(crossing.from, crossing.to, smooth(t));
      y = crossing.gap - scrollY;
      break;
    }
    x = crossing.to;
    y = height * .32;
    previousEnd = crossing.end;
    previousY = y;
  }
  if (reduceMotion.matches) { x = right; y = height * .36; }
  const rotation = reduceMotion.matches ? 0 : Math.sin(scrollY / 850) * 9;
  star.style.transform = `translate3d(${x - size / 2}px, ${y - size / 2}px, 0)`;
  star.querySelector('path').setAttribute('transform', `rotate(${rotation})`);
  const atEnd = scrollY + innerHeight >= document.documentElement.scrollHeight - 3;
  const active = atEnd ? sections[sections.length - 1] : [...sections].reverse().find(section => section.getBoundingClientRect().top <= innerHeight * .4);
  sectionLinks.forEach(link => {
    if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
function queueStar() {
  if (!starFrame) starFrame = requestAnimationFrame(updateStar);
}
function queueStarMeasurement() {
  if (!measurementFrame) measurementFrame = requestAnimationFrame(() => { measurementFrame = 0; measureStar(); });
}
window.addEventListener('scroll', queueStar, { passive: true });
window.addEventListener('resize', queueStarMeasurement);
reduceMotion.addEventListener('change', queueStar);
document.fonts.ready.then(queueStarMeasurement);
if ('ResizeObserver' in window) new ResizeObserver(queueStarMeasurement).observe(document.querySelector('main'));
measureStar();
