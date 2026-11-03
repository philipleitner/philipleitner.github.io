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
- `script.js`: accessible mobile navigation, Escape handling, and progressive section reveals. Content and navigation remain visible without JavaScript; reduced-motion preferences disable animation.
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

The View CV button opens `./assets/philip-leitner-cv.pdf` in a new tab. The separate Download CV link lives in the footer and downloads the same file. The current PDF is the public-safe original supplied by Philip, preserved byte-for-byte. Future replacements must also omit private details; copy the original PDF rather than regenerating it.

Credential buttons use the exact individual Bloomberg and Forage URLs supplied by Philip. Update the corresponding `credential-link` anchors in `index.html` if credentials are reissued. These external services may restrict automated access.


## Background, palette, and scrolling

The palette uses Sky Blue (`#0099FF`), Cloudy White (`#FDFDFE`), near-black text, and an orange-red accent (`#FF2B06`) visually matched to the supplied swatch. The reference's printed yellow-green hex was intentionally not used. The PL favicon retains its vector geometry with adapted colors.

The introduction and every content section stay in normal document flow: no sticky section stacking, negative section margins, scroll snapping, or wheel interception. Only the readable navigation header is sticky. CSS scroll padding and target margins keep headings clear of it.

A fixed, pointer-inert background layer contains a blue-to-white gradient, three soft forms and two oversized circular outlines. Lightweight requestAnimationFrame updates shift only the background slightly; mobile and reduced-motion users receive a static version. Content surfaces remain mostly open/translucent so the background shows through. IntersectionObserver starts short heading/content reveals on entry; everything is visible by default if JavaScript fails.

Only the current equity research project uses a large featured card. Past projects use compact separated rows without fake action links. Keep their IDs intact because Leadership & Activities links to them. Add document actions only after real files or URLs are supplied.

Leadership & Activities remains between Work Experience and Certifications. The current public-safe CV PDF and the individual credential URLs remain unchanged.

## Continuous ribbon and shared design tokens

Typography, spacing, surfaces, borders, radii and accent treatments share CSS variables in `:root`. Orange-red identifies primary actions, active navigation (with a bold label and underline), status dots, section markers and link details; text remains near-black. The reading-list placeholder is plain text until a genuine URL is supplied.

A single decorative SVG loop travels through named anchors for the introduction, About, Projects, the featured research card, Work Experience, Leadership, Certifications, Beyond Finance and Contact. Its position, rotation and scale are interpolated from native scroll position, so upward scrolling reverses the same journey. Resize measurements account for real section heights. Only SVG transforms change during scrolling; content remains in normal flow. A text-line/control mask keeps the ribbon clear of readable and clickable areas, and the complete decorative layer ignores pointer events. Mobile uses a smaller loop and simpler horizontal travel. Reduced motion keeps a static loop. Without JavaScript, the loop remains a quiet static decoration and content/navigation remain usable.
