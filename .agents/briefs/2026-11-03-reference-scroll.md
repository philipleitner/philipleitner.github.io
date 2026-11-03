# Builder brief: reference-based orbital scroll motion

## Reference successfully inspected

Local video (do not copy into the repository): `/workspace/attachments/9f950e88-f554-4827-8bbf-b5d65e8a163b/real video.mov`. 640×416, 60fps, 7.59s. Frames: `/workspace/portfolio-review/reference/frames/`; contact sheet: `/workspace/portfolio-review/reference/contact-sheet.jpg`. Open individual frames yourself before implementation. Browser chrome occupies y≈0–68; reference sticky navigation y≈68–103; content viewport y≈103–416.

Observed: ordinary content scrolls over a fixed decorative field with broad diagonal curved lines and oversized circular outlines. A red curved four-point star moves around a broad curved/orbital path, rather than visiting section corners. It has a soft local red halo and a short tapered dotted trail. Cards naturally cover the decoration while it passes underneath; the decoration is not manually masked around text. The main star's observed width stays about 15–18px at 640px recording width (roughly 36–44px at typical desktop width). It moves across the centre/right, with small rotation; no huge ribbon or loop. The same journey reverses as the user scrolls back. No content pinning/stacking is visible in this clip.

Observed main-star frame coordinates, useful for visual calibration (not an inferred absolute scroll-time function):
- 0.0–0.5s: centre (390,201), about 16px.
- 2.0s: (522,249); 2.25s: (538,268), about 16px.
- 2.5s: (500,262); 2.75s: (373,202).
- 3.0s: (251,140); 3.25s: (227,139).
- 4.0s: (297,161), trail extending up/left.
- 4.25–4.75s: (478,254)→(526,268)→(527,251).
Some intervening frames hide the star beneath opaque cards. Final seconds show the screen-recording selection UI; ignore that UI.

## Implementation goal

Reproduce the observed character and movement on Philip's existing portfolio: a small red four-point orbital shape with a restrained halo/dotted trail, thin curved field lines, naturally scrolling content and reversal. This is explicitly authorised motion. Retain sky-blue/cloudy-white palette, recent orange-red typography, right-aligned navigation and all current content/links. Do not copy Ferraria branding, product content, cards, fonts, or its full layout.

The short recording does NOT show the whole source website, exact scroll offsets/velocities, original code or mobile behavior. Do not claim a pixel-exact complete reproduction. Calibrate the observed segment, adapt one consistent journey to this portfolio's length, and document mobile/static/reduced-motion adaptations honestly.

## Technical direction and boundaries

Read AGENTS.md and all relevant local skills. Prefer native CSS ScrollTimeline with transform/offset-path or equivalent lightweight native mechanism. No scroll hijacking, wheel interception, section stacking, or repeated layout reads. No animation library is needed unless a demonstrated constraint prevents the lightweight approach. Use a dedicated pointer-inert decoration behind readable content/white surfaces and below navigation, with no horizontal overflow. Respect reduced motion, unsupported CSS and no-JS fallbacks. Mobile should be smaller and less expansive; it cannot be called reference-verified.

Builder owns HTML/CSS/JS changes necessary for the effect, regression-test changes and a new dedicated motion test if useful. Coordinator owns this brief and final review documentation. Do not commit or push.

## Acceptance and deliverables

- Inspect actual video frames and report how implementation matches those observations.
- Verify constant small star, smooth continuous curved travel, tapered trail, local halo, reversal, no resets at section boundaries, and natural card occlusion.
- Keep body copy/controls readable and functional; preserve original CV/favicon bytes and URLs.
- Existing browser tests must still pass; intentionally update the old test asserting that all motion shapes are absent, without weakening flow/accessibility tests.
- Test the full page and intermediate scroll offsets at desktop/mobile, reduced motion, keyboard/menu, CV and subpath assets.
- Capture a browser recording (down and up) and screenshots; inspect them against reference frames before reporting completion.
- Use port 8765 or 8780; coordinator uses 8888 for independent review. Artifacts outside repo.

## Implementation and coordinator review

Builder implemented a 40px desktop / 28px mobile four-point star on a native CSS ellipse, with local halo, six tapered trail dots and faint field curves. Position stays on the native ScrollTimeline. Initial/font-ready/resize measurement adapts the cadence to one orbit per1.7 viewport heights; one passive direction/idle listener controls trail side and260ms idle/150ms fade behavior. No frame polling, wheel interception, text masks or pinned sections. Static/no-JS/reduced-motion fallbacks are included.

Builder's browser_smoke.py and orbital_motion.py suites passed. Coordinator independently measured a22.0° major-axis tilt and horizontal centre range0.364–0.840 viewport widths, compared screenshots and the down/up recording against source frames, and verified unchanged approved copy, all link destinations, CV and favicon bytes. Desktop/mobile layout and menu checks also passed. The short source clip cannot support a pixel-exact full-site, timing or mobile claim. No reference video/browser-chrome assets are published in the repository.
