# Builder brief: more curls, tiered glass surfaces, refresh to top

## User request

Make the current single star journey more dynamic, with visible swirls/curls. Make content surfaces translucent in tiers based on importance, matching the supplied examples: some show the shape clearly; important text surfaces soften it with more white/blur. Refresh must return to the top instead of restoring the previous scroll position.

## Design and scope

Preserve all approved content, URLs, CV/favicon, palette, right-aligned navigation and native scrolling. Keep sections in normal flow and one40px desktop/28px mobile shape. Improve the existing continuous non-repeating journey, rather than adding shapes or a time-driven animation loop. Add deliberate local curling/looping segments to broad page travel; retain continuous tangents, reversal and held pause, avoid self-resetting motion or excessive terminal speed. Mobile simplifies curls.

Use shared surface tokens with concrete tiers:
- Featured research and detailed Work Experience: stronger white tint and restrained static blur for legibility, but not completely opaque.
- Leadership and Certifications: medium-white glass with lighter blur.
- Past Projects and supplementary About surfaces: clearer glass so the moving red shape/trail remains visible beneath.
Keep text itself fully opaque; do not put opacity on entire containers. No animated blur or huge blur layers. Provide readable fallback when backdrop-filter is unavailable, and keep gradients/background field intact. Preserve subtle actual-action hover/focus and no fake card hover.

Reload behavior: set manual scroll restoration and return to scrollY0 on actual reload (including reload from an in-page hash), resetting old hash only on reload. Preserve ordinary in-page navigation, intentional incoming deep links on a fresh navigation, browser back/forward where feasible and no-JS accessibility. Avoid a perpetual scroll lock, repeated scroll listeners or breaking native anchor actions. Check real page.reload(), not just a new navigation.

Builder owns HTML/CSS/JS/test changes. Coordinator owns this brief and final README/review notes. Do not commit/push.

## Tests and evidence

Run baseline and journey suites, updating old natural-occlusion expectations for translucent surfaces without weakening normal-flow/accessibility checks. Add actual refresh regression at middle, bottom and a hash anchor: after reload scrollY0 and intro visible; navigation must still scroll normally afterwards. Also verify incoming deep link still works.

Prove the path has visible curling curvature, stays in viewport and remains continuous/reversible, with static reduced-motion/no-JS fallbacks and no excessive final leg. Check desktop1440, wide2048 and mobile320/390 plus intermediate widths. Inspect screenshots with star behind clear and blurred surfaces to demonstrate tiers. Capture down/pause/up recordings. Preserve and verify visible copy/link destinations and original PDF/favicon bytes.

Use8765/8780 ports; coordinator uses8888. Artifacts outside repo. Explain browser limitations honestly, especially backdrop-filter fallback and motion support.

## Review outcome

Builder completed three tangent-continuous local curls, shared clear/medium/strong glass tiers, and reload-only scroll reset. Baseline, journey and glass/reload browser suites passed, including desktop/mobile, real fresh-document anchors, navigation and back/forward. Coordinator independently checked original visible content/link ordering and CV/favicon bytes, real reloads, path geometry, all three actual translucent surfaces, worst-case red-under-glass text contrast, responsive overflow and screenshots. JavaScript syntax and Git whitespace checks passed. Screen recordings are stored outside the repository under `/workspace/portfolio-review/curls-glass/`.

Only system Chromium was exercised. Unsupported-backdrop solid fallback was reviewed in CSS rather than run in another engine; no-JavaScript keeps content accessible but cannot perform the refresh reset. Publication is a direct main push under existing authorization.
