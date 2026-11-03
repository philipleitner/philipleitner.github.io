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
- `script.js`: accessible mobile navigation, Escape handling, and active-section tracking. Content and navigation remain visible without JavaScript; CSS handles native scroll motion and reduced-motion preferences.
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

Credential buttons use the exact individual Bloomberg and Forage URLs supplied by Philip. Update the corresponding `credential-link` anchors in `index.html` if credentials are reissued. These external services may restrict automated access.


## Background, palette, and scrolling

The palette uses Sky Blue (`#0099FF`), Cloudy White (`#FDFDFE`), near-black text, and an orange-red accent (`#FF2B06`) visually matched to the supplied swatch. The reference's printed yellow-green hex was intentionally not used. The PL favicon retains its vector geometry with adapted colors.

The introduction and every content section stay in normal document flow: no sticky section stacking, negative section margins, scroll snapping, or wheel interception. Only the readable navigation header is sticky. CSS scroll padding and target margins keep headings clear of it.

A fixed, pointer-inert background layer contains a blue-to-white gradient, three soft forms and two oversized circular outlines. The background is static on all devices. Solid white entry lists sit over open sections so the gradient still shows through between content groups. Everything is visible by default if JavaScript fails.

Only the current equity research project uses a large featured card. Past projects use compact separated rows without fake action links. Keep their IDs intact because Leadership & Activities links to them. Add document actions only after real files or URLs are supplied.

Leadership & Activities remains between Work Experience and Certifications. The current public-safe CV PDF and the individual credential URLs remain unchanged.

## Consistent entry styles and interaction

Work Experience, Leadership & Activities, Past Projects and Certifications share solid white list surfaces, fine separators, aligned typography and spacing tokens. Only the current equity research report uses the large featured composition. Noninteractive entries have no hover effects or pointer cursor. Real actions have subtle matching hover/focus treatments plus visible keyboard outlines.

The earlier gutter-following star was removed. The current, explicitly requested reference-based effect is described below. The decorative gradient background remains static and content stays in normal flow. Active navigation uses IntersectionObserver. Reduced motion disables scroll motion and smooth scrolling; content remains visible without JavaScript.

The complete available Git history contains four interests: Varsity football, Weightlifting, Poker, and the finance/philosophy reading entry. These are retained, with the final title Reading: Finance & Philosophy and a non-clickable Reading List — coming soon placeholder below it. A fifth interest must be supplied before it can be added; it is not invented.

## Skills and repeatable browser checks

Project-local skills: Anthropic frontend-design and webapp-testing, plus ibelick/ui-skills fixing-motion-performance. Each has a pinned source and licence under `.agents/skills/`; AGENTS.md defines when to use them. They do not install an animation library or change other projects.

The site now uses native CSS Scroll/View Timelines for a thin reading-progress line and subtle movement inside the PL illustration on wide screens. All content stays in normal flow. The reference-based journey described below adds a small decorative shape without an animation dependency. Repeated heading/card reveals were removed. Unsupported browsers and reduced-motion users get the complete static design; the illustration stays static on mobile.

With Python Playwright and system Chromium available, run from the repository root:

```sh
python3 .agents/skills/webapp-testing/scripts/with_server.py --help
python3 .agents/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8765 --bind 127.0.0.1" --port 8765 -- python3 tests/browser_smoke.py --url http://127.0.0.1:8765 --artifacts /tmp/portfolio-checks
```

This verifies responsive flow, native scroll progress at several positions, static fallbacks, menu/keyboard access, links and local PDF/favicon assets. Screenshots go outside the checkout. This is local browser validation, not proof of a GitHub Pages deployment or external credential access.

## Two-agent maintenance workflow

For website changes, AGENTS.md now directs a briefing/review coordinator and one website-builder agent. The coordinator writes an implementation brief under `.agents/briefs/`, the builder implements and browser-tests it, and the coordinator independently reviews the diff and screenshots before pushing to `main`.

Role instructions are saved in `.agents/roles/briefing-review.md` and `.agents/roles/website-builder.md`. These files persist the workflow for this repository; they do not create always-running agents or install a global app feature. If agent tools are unavailable, the coordinator must say so and perform the stages sequentially rather than claim a second agent ran.

## Reference-based scroll journey

Two supplied desktop clips were inspected frame by frame. The first7.59-second segment suggested a shallow local orbit; the longer26.38-second recording shows the star reaching different upper/lower and left/right regions as the page scrolls. The implementation now follows one continuous, non-repeating curve mapped to actual portfolio section landmarks, rather than revolving around one fixed oval.

The small four-point orange-red shape, local halo, tapered tail, faint field curves and natural occlusion by solid content surfaces are retained. Position follows native scroll progress, holds at rest and retraces when scrolling upward. Content stays in normal document flow. No Ferraria branding or product assets are included.

A small passive direction/idle listener controls only the tail side and its rest fade. Layout is measured on initial/font-ready/resize to calibrate the native path/keyframes; there is no wheel interception, per-frame layout polling or time-driven position loop. Mobile uses a simpler path; reduced-motion/no-JavaScript/unsupported-motion versions remain static. Exact source scroll offsets/easing and mobile behavior are not available, so the portfolio path remains a documented reference adaptation rather than a pixel-exact source reconstruction.

Source recordings, extracted frames, comparison screenshots and browser recordings stay outside the checkout. Do not publish the user's recording/browser chrome.

Additional reference-motion checks (using the same server helper):

```sh
python3 .agents/skills/webapp-testing/scripts/with_server.py --server "python3 -m http.server 8780 --bind 127.0.0.1" --port 8780 -- python3 tests/orbital_motion.py --url http://127.0.0.1:8780 --artifacts /tmp/portfolio-orbit
```

Use distinct ports for concurrent test/recording servers.
