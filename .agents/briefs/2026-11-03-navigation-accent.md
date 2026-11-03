# Builder brief: right-aligned navigation and stronger colour identity

## User request

The desktop navigation feels centred, and content entries look too monochrome. Move the navigation group to the right and use the existing orange-red more visibly. Establish a reusable briefing/review agent → website builder agent workflow.

## Design direction

Keep the PL logo at the left. Align the last desktop navigation action with a modest right viewport gutter, including at 1920–2048px; avoid the current large symmetric max-width header padding. Retain the mobile menu and its accessibility.

Retain Sky Blue #0099FF, Cloudy White #FDFDFE, orange-red #FF2B06 and near-black body text. Use the existing darker accent-ink token for readable red text on white. Make the colour change visibly intentional in Work Experience, Leadership, Past Projects, Certifications and Beyond Finance: e.g. warm entry titles on white, restrained orange-red rules/edges, coloured metadata or numbered markers, and consistent action details. Keep lengthy descriptions near-black/muted for legibility. Do not turn all text red or place low-contrast small red text on saturated blue.

## Boundaries

Preserve all approved wording, facts, URLs, CV bytes and favicon. Keep only the current research project featured and past projects compact. Keep existing sections in normal flow, native navigation and reduced-motion behavior. Do not add decorative motion, interactions on noninteractive entries, dependencies, new facts or links. Do not invent a fifth interest.

## Scope and ownership

Builder owns styles.css and any necessary regression-test updates. Prefer CSS-only presentation changes; modify HTML only if genuinely necessary. Coordinator owns AGENTS.md and .agents/roles/ documentation. Do not edit those workflow files. Do not commit, push, or create a PR; coordinator reviews and publishes.

## Acceptance checks

1. Browser: at 1440px, 1920px and 2048px, navigation ends close to the right gutter and the logo remains left; no clipping at smaller breakpoints.
2. Visually meaningful orange-red use on entry titles/details, without changing text or making rows look clickable.
3. Readable contrast and matching keyboard-focus/hover states for actual actions.
4. Existing Playwright regression suite passes; check 320px and 390px mobile, menu, anchors, intermediate scrolling, CV and relative paths.
5. Capture header, Past Projects, Work Experience and Beyond Finance desktop views plus representative mobile screenshots outside the checkout. Inspect them, then report exact changes, checks and any limitations.

## Required project instructions

Read AGENTS.md, frontend-design SKILL.md and webapp-testing SKILL.md. Review the brief before implementation and keep the solution proportional to these specific requests.

## Review outcome

Implemented by a separate website-builder agent and independently reviewed by the coordinator. Desktop navigation ends at a 4% viewport gutter at 1440, 1920 and 2048px. Orange-red entry titles/metadata, group rules and interest markers are visible; body text remains readable. Builder regression suite passed ten widths plus keyboard/menu, native scrolling/reduced motion, no-JavaScript fallback, CV/favicon and root/subpath assets. Coordinator separately verified alignment, overflow, mobile menu and unchanged HTML/CV/favicon. Screenshots were inspected. External live deployment was not verified from this environment.
