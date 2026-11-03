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

// One ribbon, one section-anchored journey. No wheel handlers or scroll pinning.
const ribbon = document.querySelector('.journey-ribbon');
const ribbonBody = document.querySelector('.ribbon-body');
const cutouts = document.querySelector('.ribbon-cutouts');
const maskBase = document.querySelector('.ribbon-mask-base');
const sectionLinks = [...navigation.querySelectorAll('a[href^="#"]')];
const mainSections = [...document.querySelectorAll('main > section')];
const svgNS = 'http://www.w3.org/2000/svg';
let journeyStops = [];
let journeyFrame = 0;
let layoutFrame = 0;

function measureJourney() {
  const width = window.innerWidth;
  const height = window.innerHeight;
  const compact = width <= 850;
  const maxScroll = Math.max(1, document.documentElement.scrollHeight - height);
  ribbon.setAttribute('viewBox', `0 0 ${width} ${height}`);
  maskBase.setAttribute('width', width);
  maskBase.setAttribute('height', height);
  // Named anchors deliberately alternate margins beside each section.
  const anchors = [
    ['#home', .90, .38, -20, .93],
    ['#about', .07, .43, 35, .80],
    ['#projects', .93, .35, 105, .86],
    ['.project-card', .07, .65, 155, .95],
    ['#experience', .93, .42, 225, .78],
    ['#leadership', .07, .48, 285, .90],
    ['#training', .93, .45, 350, .78],
    ['#beyond', .07, .48, 415, .86],
    ['#contact', .89, .63, 480, .95]
  ];
  journeyStops = anchors.map(([selector, x, y, angle, scale], index) => {
    const element = document.querySelector(selector);
    const top = element.getBoundingClientRect().top + window.scrollY;
    return { scroll: index ? Math.min(maxScroll, Math.max(0, top - height * .32)) : 0,
      x: (compact ? (x < .5 ? .12 : .88) : x) * width,
      y: (compact ? (index === 0 ? .72 : .27) : y) * height, angle: compact ? angle * .5 : angle, scale: compact ? .38 : scale, selector };
  }).filter((stop, index, list) => !index || stop.scroll > list[index - 1].scroll);
  // Text-line masks prevent the decoration from showing through any copy.
  const fragment = document.createDocumentFragment();
  const reserve = rect => {
    if (!rect.width || !rect.height) return;
    const node = document.createElementNS(svgNS, 'rect');
    node.setAttribute('x', rect.left - 10);
    node.setAttribute('y', rect.top + window.scrollY - 14);
    node.setAttribute('width', rect.width + 20);
    node.setAttribute('height', rect.height + 28);
    node.setAttribute('rx', 4);
    fragment.appendChild(node);
  };
  const walker = document.createTreeWalker(document.querySelector('main'), NodeFilter.SHOW_TEXT);
  let textNode;
  while ((textNode = walker.nextNode())) {
    if (!textNode.textContent.trim() || textNode.parentElement.closest('[aria-hidden="true"]')) continue;
    const range = document.createRange();
    range.selectNodeContents(textNode);
    [...range.getClientRects()].forEach(reserve);
  }
  document.querySelectorAll('main a, main button').forEach(element => reserve(element.getBoundingClientRect()));
  cutouts.replaceChildren(fragment);
  document.documentElement.classList.add('journey-ready');
  updateJourney();
}

function curve(a, b, c, d, t) {
  // Catmull–Rom interpolation gives continuous curved motion through anchors.
  return .5 * ((2 * b) + (-a + c) * t + (2 * a - 5 * b + 4 * c - d) * t * t + (-a + 3 * b - 3 * c + d) * t * t * t);
}
function updateJourney() {
  journeyFrame = 0;
  if (!journeyStops.length) return;
  const scroll = window.scrollY;
  let index = 0;
  while (index < journeyStops.length - 2 && scroll > journeyStops[index + 1].scroll) index++;
  const b = journeyStops[index];
  const c = journeyStops[Math.min(index + 1, journeyStops.length - 1)];
  const a = journeyStops[Math.max(0, index - 1)];
  const d = journeyStops[Math.min(index + 2, journeyStops.length - 1)];
  const progress = Math.max(0, Math.min(1, (scroll - b.scroll) / Math.max(1, c.scroll - b.scroll)));
  const point = {};
  for (const key of ['x', 'y', 'angle', 'scale']) point[key] = curve(a[key], b[key], c[key], d[key], progress);
  if (reduceMotion.matches) Object.assign(point, { x: innerWidth * .91, y: innerHeight * .42, angle: -20, scale: innerWidth <= 850 ? .42 : .85 });
  ribbonBody.setAttribute('transform', `translate(${point.x} ${point.y}) rotate(${point.angle}) scale(${point.scale})`);
  cutouts.setAttribute('transform', `translate(0 ${-scroll})`);
  const atEnd = scroll + innerHeight >= document.documentElement.scrollHeight - 3;
  const active = atEnd ? mainSections[mainSections.length - 1] : [...mainSections].reverse().find(section => section.getBoundingClientRect().top <= innerHeight * .4);
  sectionLinks.forEach(link => {
    if (active && link.hash === `#${active.id}`) link.setAttribute('aria-current', 'location');
    else link.removeAttribute('aria-current');
  });
}
function queueJourney() {
  if (!journeyFrame) journeyFrame = requestAnimationFrame(updateJourney);
}
function queueMeasure() {
  if (!layoutFrame) layoutFrame = requestAnimationFrame(() => { layoutFrame = 0; measureJourney(); });
}
window.addEventListener('scroll', queueJourney, { passive: true });
window.addEventListener('resize', queueMeasure);
reduceMotion.addEventListener('change', queueJourney);
document.fonts.ready.then(queueMeasure);
if ('ResizeObserver' in window) new ResizeObserver(queueMeasure).observe(document.querySelector('main'));
measureJourney();
