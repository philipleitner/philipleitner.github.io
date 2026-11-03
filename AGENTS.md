# Portfolio maintenance

## Standing two-agent workflow

- For website implementation requests, use a briefing/review coordinator plus one website-builder agent. The user explicitly requested this as the default project workflow.
- The coordinator writes a concrete brief before implementation, delegates to the builder when agent tools are available, then independently reviews the result before committing/pushing.
- Follow [briefing-review](.agents/roles/briefing-review.md) and [website-builder](.agents/roles/website-builder.md). Keep briefs under `.agents/briefs/` and avoid overlapping file ownership.
- These files persist roles/instructions, not continuously running agents. If agent tools are unavailable in a future session, report that and execute the stages sequentially; do not claim delegation occurred.
- This workflow applies to implementation requests, not ordinary explanatory chat or trivial documentation-only edits. It does not add routine approval steps.

## Content and design

- Preserve approved content and working links unless the user requests changes.
- Use shared CSS design styles and variables for colours, typography, spacing, buttons, borders, and content entries.
- Keep the palette: sky blue `#0099FF`, cloudy white `#FDFDFE`, and orange-red `#FF2B06`, with readable near-black text.
- Keep sections in normal document flow. Do not add overlapping panels, section stacking, or moving decorative shapes unless explicitly requested.
- Keep the current equity research project as the only large featured project, clearly marked **In progress**. Keep past projects compact.
- Do not invent achievements, dates, URLs, credentials, or personal details. Ask for missing facts and keep unavailable resources clearly labelled without fake links.
- Preserve the original public-safe CV PDF and its appearance. Do not publish private addresses or phone numbers.
- Keep plain HTML, CSS, and JavaScript compatible with GitHub Pages. Use relative file paths, including for assets, the favicon, and the CV; support root and repository-subpath hosting.

## Design, motion and testing skills

- Before requested UI/design work, read [frontend-design](.agents/skills/frontend-design/SKILL.md) and apply its relevant design and review guidance.
- Before animation or scrolling changes, read [fixing-motion-performance](.agents/skills/fixing-motion-performance/SKILL.md). Prefer native Scroll/View Timelines and transform-only motion; do not add scroll-polling loops or a library without a concrete need.
- Before browser validation, read [webapp-testing](.agents/skills/webapp-testing/SKILL.md). Its Python Playwright helper can manage the local server; run it with `--help` first. Use local HTTP rather than its file-URL example because browser policy blocks file URLs here.
- These are project-local skills, not global installations. Each skill includes SOURCE.md and LICENSE.txt beside its SKILL.md.
- The user's requests and this repository's content, palette, layout, accessibility, and publishing rules take precedence over the skill's general suggestions. Do not rewrite approved copy, change the palette, add motion, or redesign unrelated areas merely to satisfy the skill.
- Adding or updating the skill does not itself authorise a website redesign. No additional packages or animation libraries are required.

## Validation

- For visual changes, inspect the actual result in a browser at desktop and mobile sizes, including narrow screens and intermediate scroll positions.
- Preview through a local HTTP server (for example, `python3 -m http.server 8000 --bind 127.0.0.1`); this environment blocks browser `file://` navigation.
- Use Playwright or an available browser-testing tool. Check scrolling, hover and matching keyboard-focus states, navigation, CV viewing/download access, clipping, horizontal overflow, and browser errors.
- Preserve reduced-motion support and content visibility without JavaScript. Do not imply that noninteractive entries are clickable.
- Test affected functionality and verify existing links and assets. Report checks that could not be performed; never claim unrun checks passed or confuse local checks with live-site verification.
- For documentation-only changes, check the instructions and Git diff; a full visual regression run is unnecessary.

## Tools and publishing

- Keep maintenance lightweight. Playwright and system Chromium are available in the current cloud environment; check availability in future environments before installing anything.
- Frontend-design, fixing-motion-performance and webapp-testing are available locally as described above. Use the existing Python Playwright/Chromium tools. Discover suitable existing skills first, and explain any missing capability before proposing an installation.
- Use the existing isolated checkout; do not create a worktree unless requested.
- Before editing, inspect Git status and repository instructions. Preserve unrelated changes and sync with remote `main` without overwriting remote work.
- The user has authorised committing and pushing requested, tested website changes directly to `main`, which publishes through GitHub Pages. Do not create a pull request or ask for routine confirmation.
- Do not force-push. If direct pushing or a required check is blocked, report the exact blocker and distinguish completed work from pending work.
- Summarise changes and validation; include screenshots for visual changes when available.
