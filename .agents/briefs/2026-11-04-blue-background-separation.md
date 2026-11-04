# Separate foreground panels from background

User likes panels but finds too much background white on left and insufficient foreground separation; invites experimentation with cream or more/light blue. Choose light blue to preserve established palette and avoid arbitrary cream. Modify background only (and at most shared border contrast if truly necessary), keeping current content/surfaces/layout/actions/links/nativebar and no heavy animation/filter.

Current historical gradient fades #edf8ff63% to#fdfdfe84%, with almostwhite radialglow. Replace nearwhite expanse with visible soft powderblue (e.g#c4e7ff/#d5edff), keep rich sky at edge and restrained lighterblues acrosswholeviewport. Reduce white radialglow; make softblueglow instead. Experiment visually and compare; white contentpanel should remain noticeably lighter than backdrop at intro/middle/bottom and bothsides, not justtop. Keep cloudwhitecontent and blue/reddesign. No CSSblur/backdrop/newmotion/no star. Respectmobile staticcheapbackground.

Builder source+targetedtest/screenshots; rootdocs/review. Verify3scrollpositions desktop/mobile, nooverflow/textcontrast/nav/progress/reduced motion and local assets. Existingbaseline if useful but no unnecessary fullreload rerun since unchanged. Preservecopy/hrefs/assetsbyteexact. Screenshots intro,work,certs. No commit/push.

## Coordinator review

Approved light-blue approach: gradient now ends in#cce9fc through#b6dfff instead of white; radialglows blue rather than white. Only three background colour declarations changed. Independent browser review passed exact unchanged HTML/script/CV/favicon, both margins visibly blue at intro/work/cert positions on1440/390, nooverflow/filter/extraanimation. Reviewed desktopwork and mobilecertification screenshots; whitepanels visibly distinct frombackdrop. No cream or layout/content changes needed.
