# Polish the About facts strip

User screenshot targets bottom university/IB/languages strip only; wants betteralignment and purposefulred. Implement actualpolish, not justprompt. Preserve all wording/biography/countries/hero/othersections/links/assets, existingtop/bottompanelalignment and no newmotion/filters.

Design direction: turn current mismatched serif factheadings into a deliberate compact information strip. Use site's shared sans for all three fact titles, same font size (~16–18px) and weight600, aligned on same top baseline. Three desktopcolumns with degreearea onlyslightlywider if necessary; rowspacings consistent, title and supportingcopy start at shared verticalpositions. Degree/class support naturally in firstcell, do not insert fake filler in others. Avoid narrowclipping/languageorphan at1024. Add a slimred top rule/accent or small red icon/marker consistently for eachcell and subtlevertical separators, with faintblue/white surface if improves cohesion. No giantseparatecards/no arbitraryfontweight/large redblocks. Red shouldbe visible but readable bodyremainsink. Choose clean SVG icons (education/academicresult/languages) only if visualconsistency worthwhile; decorativelabelredundantariahidden. Allthree main titles equal visualweight, no oversizeddegree.

At phones use roomy stacked or universityfullrow+twofacts layout with sharedtypography/redmarkers and no overflow; atdesktop all3 inonehorizontalrow. Currentfigure/storypanelalignment mustremain exact (gridstretch). ScopeHTMLchanges withinfact-row only and CSSfactselectors only; don'tchange biography or headings/countries.

Builder owns source andtargetedchecks/screenshots; rootbrief/review. Test1440/1024/390/320 forfactsalignedtitlefont/verticalpositions desktop, nooverflow, equalpanelboundaries, legibility. Preserveexact factstrings. No fullbaselinererun needed unlessbroaderissue. Capture detailedfacts andsectiondesktop/mobile. No commit/push.

## Review

CSS-only strip polish uses16px/600sharedsans titles, slim red markers, fine separators and shared subgrid rows with fallback tracks. Final1.4/1/1.2 desktop proportions give IB support enough room at wider widths. No wording/HTML/assets changed.

Builder targeted1440/1024/390/320 checks passed. Coordinator independently verified exact fact and outside-facts HTML preservation, identical title typography, aligned desktop titles/supporting-copy starts, aligned About panel boundaries, mobile readability/no overflow. Desktop/mobile screenshots reviewed; requested wider IB column refinement applied and rechecked. Whitespace check passed.
