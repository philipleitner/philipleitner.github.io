# Urgent scroll regression repair

User reports lag persists and requests a decisive fix. Remove the newly added scroll-following decoration altogether (HTML, native keyframes, path generation, direction/idle listeners, halo/trail), rather than retaining the known regression. Also remove nonessential scroll timelines/reading progress/hero parallax to restore plain native scrolling. Preserve static gradient background, alpha surfaces, content, navigation, links, CV/favicon, reload-to-top and palette. No replacement animation. Plain static view is deliberate performance fallback.

Builder owns source/tests; root owns docs. Update tests to assert removed decoration/timeline/listeners, retain responsive/nav/keyboard/CV/reload/reduced/noJS tests. Remove obsolete orbital test or replace with static-scroll regression. Browser inspect desktop/mobile, capture screenshots. No claim of user device FPS; record no active animations while scrolling and no JS errors. Do not commit/push. Root independently reviews and publishes. Keep change bounded; no prolonged profiling.

## Coordinator review

Independently verified no decorative markup, scroll timeline declarations, scroll listeners or running animations at five full-page positions. Visible copy and href ordering match prior version; CV/favicon bytes unchanged. Three translucent tiers remain, navigation/reload and responsive overflow checks pass. Desktop/mobile screenshots inspected; syntax and whitespace checks pass. This removes the complete new animation subsystem rather than making an unverified frame-rate claim. Real-device results cannot be proven from cloud Chromium.
