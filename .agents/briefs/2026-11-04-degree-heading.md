# Degree as bold fact heading

User wants “BSc in International Economics and Finance” as bold main first fact title instead of Bocconi University. Swap the two existing first-fact strings/classes: degree gets fact-title; Bocconi University becomes supporting text beneath; Class of2029 stays below. Preserve all other content/styles unless minimal wrapping fix necessary. Keep same main font size/weight as44/45/languages; allow degree wrap, shared subgrid title tracks keep all supporting lines aligned. No enlarging degree. Targeted desktop1440/1024/mobile390/320 check wrapping/nooverflow/title/supportalignment. HTMLonly if possible. No commit/push, root reviews.

## Review

Builder passed four-width wrapping/alignment tests and simulated non-subgrid fallback spacing; fallback title track now minmax(4.2rem,auto) to fit long degree safely. Coordinator verified exact heading/support swap only in HTML and independent desktop/mobile alignment, equal title typography, panel boundaries and nooverflow. Whitespace check passed.
