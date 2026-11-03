# Builder correction brief: the shape must travel with scroll

## User correction

The user likes the visual treatment but says the moving shape remains in one place. Inspect the new longer reference closely and correct the movement. This is implementation through the standing two-agent workflow, not just a written suggestion.

## Reference and evidence

New local clip: `/workspace/attachments/e72531d0-a393-4fd1-9b2a-fc728b015de2/hihihi.mov` (26.38s, 640×416,60fps). Inspect it via extracted frames/contact sheets before editing. Artifacts: `/workspace/portfolio-review/reference-2/sheet-01.jpg`, `sheet-02.jpg`, and `/workspace/portfolio-review/reference-2/frames/f-*.png` (2fps). Browser chrome is y0–68; reference navigation y68–103; content y103–416. Ignore the browser menu/screenshot toolbar in the last seconds and the large static hero branding star behind its chat card.

Measured small main-star centres in recording pixels (time is a frame reference, NOT an assumed absolute scroll-progress value):
- 1.5s: (458,237)
- 2.5s: (297,294)
- 3.0s: (332,308)
- 3.5s: (280,229)
- 4.0s: (174,182)
- 5.5s: (361,153)
- 6.0s: (391,198)
- 8.0s: (528,268)
- 8.5s: (303,163)
- 9.0s: (225,159)
- 10.5s: (441,187)
- 13.5s: (431,197)
- 14.0s: (189,307)
- 15.5s: (538,267), while returning through the earlier content
- 17.0s: (316,309)
- 18–21s: approximately (273,251), position held while page is stationary.

The first implementation matched only a short shallow diagonal portion. The longer clip's main-star centres span x≈174–538 and y≈139–309; this cannot be represented faithfully by our single centred 22° oval. It traverses different regions with page progress and retraces when scrolling back. Cards naturally occlude it, and the trail/halo remains relevant.

## Core correction

Remove the fixed local ellipse and repeated `--orbit-travel` revolutions as the source of position. Keep one small four-point shape, halo, tapered direction-aware tail and existing palette. Create a continuous, broad, non-repeating scroll journey with intentional control points derived from the observed high/low/left/right motion and mapped to the portfolio's content landmarks. Local curved sweeps are welcome, but the origin/region must change with scroll rather than run the same oval repeatedly in a fixed lane.

Use native CSS scroll timeline + responsive offset-path/transform keyframes if feasible; measure layout only on initial/font-ready/resize as needed. Path position follows scroll progress directly, reverses on upward scrolling, and holds when scrolling stops. Do not add an autonomous time-driven loop. Keep only the existing small passive direction/idle handling if needed for the trail. Do not hijack scrolling or pin/overlap content.

Keep the approximate40px desktop /28px mobile size, constant star opacity, gentle rotation, pointer-inert decorative layer below navigation and readable content. Natural card occlusion is allowed; no text masks or per-section disappear/reappear animations. Reduced-motion/no-JS/unsupported-path fallbacks stay static. Mobile is a documented simpler adaptation; no mobile reference was supplied.

## Content constraints and ownership

Preserve every approved word, link, CV/favicon byte, current right-aligned header and orange-red entry styling. Current research remains featured, past projects compact. Builder owns necessary HTML/CSS/JS and test changes. Coordinator owns this brief and final README/review notes. Do not commit or push.

## Acceptance criteria: verify the user's complaint is actually solved

1. Inspect the reference frames yourself and report how the new path differs from the previous fixed oval.
2. Across a full desktop scroll, sample intermediate positions and section boundaries. Demonstrate a substantial horizontal AND vertical range, including left-of-centre/upper, central/lower and right/lower positions. Aim for x travel≥0.50W and y travel≥0.40H, while keeping viewport bounds/header clearance. Do not manufacture section jumps to satisfy these measurements.
3. A repeated scroll interval of1.7viewport heights must no longer simply return the shape to the same local ellipse position.
4. Small consecutive scroll increments yield continuous positions with no teleports. Scroll down/up to matching offsets and verify equal star coordinates; pause and verify stable position.
5. All sections remain in normal document flow. Preserve natural occlusion, reversal of the trail, idle fading and all accessibility/static fallbacks.
6. Run baseline browser_smoke.py and revise orbital_motion.py into real journey regression checks. Keep existing flow/link/CV/menu/keyboard/subpath checks.
7. Capture a slow desktop recording and a mobile recording, including down, pause, up and complete section transitions. Inspect them against both reference sheets; provide at least6 labelled journey samples, not only top/middle/bottom screenshots.

Use ports8765/8780; coordinator uses8888. Artifacts outside the repository. Clearly state limitations: exact source scroll offsets/easing and full original source code remain unavailable, so do not claim pixel-exact equivalence.

## Implementation and independent review outcome

The builder removed the fixed ellipse, its outline and repeated revolutions. One responsive cubic path now uses actual section landmarks to generate native scroll keyframes. The final footer leg was shortened after review found excessive local speed. Direction-aware tail and idle fade remain; content, URLs and original PDF/favicon bytes are preserved.

Baseline and journey suites passed. Coordinator independently measured desktop centres x≈372–1257px and y≈230–719px at1440×900, with78/122 samples exposed between solid surfaces. Fine5px probes at the fastest sweep found continuous positions; matching down/up offsets returned matching coordinates and held pauses remained stationary. Additional resize checks covered320–2048px. Desktop/mobile down-pause-up recordings and sampled/contact-sheet frames were inspected against the longer reference.

The26.38-second reference supports the broader journey correction, but does not reveal exact source scroll offsets/easing or mobile behavior. This remains a documented portfolio adaptation rather than a pixel-exact source-code reconstruction. Reference recordings/browser chrome are not included in the repository.
