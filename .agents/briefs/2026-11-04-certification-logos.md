# Certification issuer logos

Add authentic Bloomberg and Bank of America logos to their certification entries. Preserve exact course text, issuer labels, credential URLs and current design outside this small addition. Use official-source or accurately sourced existing vector assets, locally saved with source attribution in assets/issuer-logos/SOURCE.md. Do not draw guessed logos, generate them with AI, or replace bank branding with a generic icon. Keep wordmarks legible, undistorted, modestly sized with comfortable spacing on desktop/mobile; no bulky logo cards. Avoid duplicate screen-reader output where issuer text already labels a decorative image. Use relative URLs and no runtime external image dependency. Coordinator owns brief/README/cache tokens; builder owns HTML logo markup, CSS, assets. Root will update cache tokens after implementation. Run relevant browser checks at desktop/390/320: images load, nooverflow, credential URLs unchanged, focus/navigation/CV intact. Capture certification screenshots outside repository. Do not commit/push; root reviews/publishes.

## Additional user request (5 November)

Keep “International Baccalaureate” on one line in the About facts row. Adjust available width responsively without clipping or shrinking unrelated content. Preserve wording, score and other facts. Include desktop and narrow-phone validation before the combined commit/push.

## Review outcome

Builder added authentic locally served assets with source attribution. Coordinator implemented the additional IB-label request using a nonwrapping label and responsive column allocation, with no font reduction. Independent local Chromium checks passed at 1440,1050,950,390 and320px: both logos loaded, IB text occupied one line inside its column, no horizontal overflow or console errors, credential focus worked, all existing href targets were preserved and the original PDF served successfully. Desktop certification and narrow-phone facts screenshots were visually inspected. Screenshots: /workspace/portfolio-review/issuer-logos-root/. No claim of live GitHub Pages verification.
