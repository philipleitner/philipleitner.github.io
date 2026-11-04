# Philip Leitner — Personal Portfolio

A responsive portfolio built with plain HTML, CSS, and JavaScript. No build step, framework, external fonts, or runtime dependencies.

## Preview locally

From this directory, run:

```sh
python3 -m http.server 8000 --bind 127.0.0.1
```

Open `http://127.0.0.1:8000` in your own browser. Stop with Ctrl+C. The site also works by opening `index.html` directly. This cloud environment may require command approval to run a local server/browser.

## Files and updates

- `index.html`: biography, projects, experience, education, certifications, interests, contact details, and navigation.
- `styles.css`: colors in `:root`, typography, layouts, mobile breakpoints, reduced-motion preferences, and subtle introductory animation.
- `script.js`: accessible mobile navigation, Escape handling, and active-section tracking. Content and navigation remain visible without JavaScript; CSS handles smooth anchor navigation and reduced-motion preferences.
- `assets/philip-leitner-portrait.webp`: the supplied portrait with subtle photographic retouch, encoded as a lightweight1254px WebP; used only in the introduction. Keep its descriptive alt text and explicit dimensions when replacing it.
- `assets/flags/`: retained public-domain flag source assets from an earlier design; current country stamps are inline SVG in `index.html`. Attribution is in `SOURCE.md`.
- `assets/background-field.svg`: lightweight static curves, arcs, dots and waves behind the blue gradient; no filters or embedded animation.
- `assets/favicon.svg`: the PL browser icon, drawn as vector paths for sharp small-size rendering.
- `assets/philip-leitner-cv.pdf`: the supplied public-safe original PDF, copied byte-for-byte to preserve layout and fonts. The earlier private CV is not included.

Edit the relevant text directly in `index.html`. Keep section IDs and navigation links aligned. Use relative paths (for example, `./assets/report.pdf`) so the site works at both a domain root and a GitHub Pages project path.

The attached CV is the factual source. The user supplied first-year status, the equity research project, investment banking interest, and Forage as the simulation platform. LinkedIn could not be read because environment access was blocked; only the supplied profile URL is linked. No additional profile details were inferred. Certification dates are omitted because none were supplied.

The equity research company, thesis, and publication date are labelled **to be added**. The research report, Excel model, and case presentation are **Coming soon** text, without fake or disabled download links. To publish a document later, add a reviewed file under `assets/` and replace its status span with a descriptive anchor, such as:

```html
<a href="./assets/equity-research.pdf" download>Download research report (PDF)</a>
```

For an Excel model, use a relative `.xlsx` link. Verify you have permission to distribute every document and check it for private information. Replace the public CV PDF after future updates with an address-free copy, keeping its filename or updating both CV links. Do not copy the original private PDF into the repository.

The abstract project graphics are decorative. The research graphic explicitly contains no market data. No analytics, tracking, or contact backend is included; contact uses email and LinkedIn.

## Validation

Serve the site locally and check desktop and mobile widths, menu open/close and Escape, keyboard navigation, section anchors, CV download, and reduced-motion settings. Confirm there is no horizontal scrolling, browser console error, or failed local asset request. There is no compilation or package installation step. Screenshots and browser validation are produced during review, outside the website's assets.

## Publish with GitHub Pages — only when approved

1. Review the content, public CV, and screenshots. Commit and push the approved files to `main`.
2. In GitHub, open this repository's **Settings → Pages**.
3. Under **Build and deployment**, choose **Deploy from a branch**.
4. Select **main**, **/ (root)**, then save.
5. Wait for GitHub's Pages deployment to complete and use the URL shown there. Verify all sections, downloads, and mobile navigation on the published site.

Repository ownership determines the Pages URL; use GitHub's displayed URL rather than assuming the repository name establishes a user-site address. GitHub Pages must be enabled in repository settings to publish the files pushed to `main`.

## CV and credential maintenance

The View CV button opens `./assets/philip-leitner-cv.pdf` in a new tab. The footer download was removed as requested; the original PDF remains accessible from View CV and can be saved using the browser’s PDF controls. The current PDF is the public-safe original supplied by Philip, preserved byte-for-byte. Future replacements must also omit private details; copy the original PDF rather than regenerating it.

Credential buttons use the exact individual Bloomberg and Forage URLs supplied by Philip. No missing-completion-date labels are displayed; visitors can open the original credentials for details. Update the corresponding `credential-link` anchors in `index.html` if credentials are reissued. These external services may restrict automated access.


## Design and content structure

Sky Blue (`#0099FF`), Cloudy White (`#FDFDFE`), near-black ink and orange-red (`#FF2B06`) form the shared palette. The layout uses a compact identity introduction, one featured research composition, compact past projects and aligned experience/leadership/credential entries. Cloudy-white grouped surfaces, fine blue borders, selected red edge details and shared padding separate detailed content from the background without making every row a separate card. Dark-red titles and red credential/link details establish the accent hierarchy. Shared typography, spacing, surface and action tokens live in `styles.css`.

The About section puts “A little about me.” above two aligned panels: six illustrated SVG passport stamps with readable country names, more detailed national motifs and the countries’ own flag colours, and the unchanged biography with education details. Countries are shown without dates or a travel sequence. Degree, IB result and languages share one equally styled desktop row, with a responsive arrangement on mobile. Bocconi University and Class of 2029 share the same supporting line.

All content stays in normal document flow. The restored full-viewport sky-to-powder-blue gradient is fixed behind the naturally scrolling content, with static blue glows, fine flowing curves, circular outlines and a restrained dotted texture. It uses no blur filters or background animation. There are no moving stars, overlapping panels, backdrop filters or large blur filters. The PL logo/favicon identity, safe original PDF and supplied credential URLs remain intact. Unavailable reports, models and reading-list links remain non-clickable coming-soon text.

The recoverable interests remain Varsity football, Weightlifting, Poker and Reading: Finance & Philosophy. Do not invent a fifth interest.

## Skills and repeatable browser checks

Project-local skills: Anthropic frontend-design and webapp-testing, plus ibelick/ui-skills fixing-motion-performance. Each has a pinned source and licence under `.agents/skills/`; AGENTS.md defines when to use them. They do not install an animation library or change other projects.

The site uses ordinary native scrolling without continuous decorative animations or an animation library.

With Python Playwright and system Chromium available, run from the repository root:

```sh
python3 .agents/skills/webapp-testing/scripts/with_server.py --help
python3 .agents/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8765 --bind 127.0.0.1" --port 8765 -- python3 tests/browser_smoke.py --url http://127.0.0.1:8765 --artifacts /tmp/portfolio-checks
```

This verifies responsive flow, native scrolling at several positions, static fallbacks, menu/keyboard access, links and local PDF/favicon assets. Screenshots go outside the checkout. This is local browser validation, not proof of a GitHub Pages deployment or external credential access.

## Two-agent maintenance workflow

For website changes, AGENTS.md now directs a briefing/review coordinator and one website-builder agent. The coordinator writes an implementation brief under `.agents/briefs/`, the builder implements and browser-tests it, and the coordinator independently reviews the diff and screenshots before pushing to `main`.

Role instructions are saved in `.agents/roles/briefing-review.md` and `.agents/roles/website-builder.md`. These files persist the workflow for this repository; they do not create always-running agents or install a global app feature. If agent tools are unavailable, the coordinator must say so and perform the stages sequentially rather than claim a second agent ran.

## Scrolling and performance

The page uses native browser scrolling and smooth section links over the fixed decorative blue background, which stays visibly blue behind the lighter content surfaces. A thin red reading-progress bar uses only a native CSS scroll timeline and `transform: scaleX()` on one small element. One reusable IntersectionObserver system reveals section labels, headings and independent content groups using CSS opacity/transform transitions: transparent at 20px below, then fully visible in place, with soft 720ms easing and capped 80ms group staggers. The trigger follows viewport height near 88%. Navigation stays visible; anchors and focus complete their destination immediately. Content is visible by default and setup failures restore it. Initial on-screen content animates promptly only when first-paint timing makes that safe; late initialization leaves already-visible content untouched. Reduced motion disables the entrances. Stamp hover colour stays separate from its entrance wrapper. There is no JavaScript scroll-position animation, per-frame polling, moving star/trail, hero parallax or animation library. Browsers without scroll-timeline support omit the progress bar. Reduced-motion users receive static entrances and instant anchor navigation.

Actual browser reloads return to the introduction and remove an old section fragment. Fresh incoming section links and normal anchor/back navigation still work. This resets scroll position, not the browser cache. Reduced-motion preferences disable smooth anchor scrolling.

Browser regression suites check responsive layouts, progress at several scroll positions, keyboard navigation, local PDF/favicon assets, reload behavior and the absence of expensive decorative effects. Screenshots stay outside the repository. Cloud Chromium validation does not guarantee a particular frame rate on every device.

Reveal lifecycle regression (using the same local-server helper):

```sh
python3 .agents/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8782 --bind 127.0.0.1" --port 8782 -- python3 tests/section_reveals.py --url http://127.0.0.1:8782 --artifacts /tmp/portfolio-reveals
```

The implementation adapts commit `5525453`’s observer/unobserve pattern; its old background scroll handler is excluded. This check exercises full-page down/up motion, one-time completion, layout stability, anchor/focus access and failure/reduced-motion fallbacks.

Reveals start near the lower85–90% viewport boundary, smoothly continuing from their prepared state without an opacity reset. Anchor navigation completes its destination immediately while later entries remain eligible. CSS/JS links include a revision query to refresh cached assets; update it when publishing future asset changes.
