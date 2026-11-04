# Shorter hero and consistent country typography

User wants hero paragraph shorter by one word to avoid final 'finance.' orphan and country panel type to match site. Remove only word “extracurricular” from .hero-copy: “leadership and activities” replaces “leadership and extracurricular activities”. Preserve all other wording. Keep last phrase “beyond finance.” together using inline span white-space:nowrap (ordinary space, no hard linebreak), no broad changes to hero font or layout.

Country caption and country names should use shared --sans rather than --serif. Clean restrained sizing/weights: caption ~15–16px semibold and names ~16–18px medium, same line-height/ink as site's UI/body, not giant displayserif. Preserve caption words, flags, aligned panel dimensions, all content/links/CV/assets. Modify existing rules including mobile override so no serif reset. Do not change section headings/other site fonts.

Builder HTML/CSS + targetedbrowser check1440/1024/390/320 including countriesallvisible, alignedpanels desktop, nooverflow, hero ends with togetherphrase, nav unchanged. No fullregression needed for narrowcopy/style tweak. Screenshots hero/countries desktopmobile. No commit/push; root reviews. Root ownsbrief.

## Review

Builder targeted checks passed at1440/1024/390/320 for exact one-word shortening, single-box final phrase, sans country typography, flags, aligned panels and nooverflow. Root verified only extracurricular was removed from hero text and all other HTML unchanged, inspected country and hero screenshots, reviewed scoped CSS/no other fonts changed. Whitespace check passed.
