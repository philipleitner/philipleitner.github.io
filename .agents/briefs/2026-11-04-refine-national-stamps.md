# Refine national stamp artwork

User likes stamp concept but finds drawings awkward/not representative; asks more detail, better country representation and actual national colours. Scope six inlineSVG artworks and scoped stampcolours only. Keep layout, caption, countries/names, biography/education/allothersections, responsive2cols, one-shotentrance/reduced/noJS and subtlehover. No new motion/heavyfilters/assets/libraries. Preserve current heading/progress/background.

Design revision must visibly improve illustration craft, not just recolour. Use precise balanced silhouettes with consistentstrokeweight, clearhierarchy and detail fitting smallsize. Six distinct country motifs, no inventedcities/dates/entrylabels/travelorder/officialseals:
- Austria: recognisable Alpine landscape, layeredpeaks/snowcaps/evergreen foothills; red/white palette.
- Romania: Carpathian/Transylvanian landscape with tasteful fortified-tower/roof detail and firs, blue/yellow/red accents; avoid current antenna-lookingfir.
- Greece: refined classical temple/column composition with accurate-looking capitals/steps, blue/white palette.
- Chile: tall Andeanpeaks with coast/waves and a small white-star/blue-red-white flag accent; differentiate fromAustria landscape.
- Singapore: more convincing Supertree/Gardens-inspired silhouette with branchedtrunks/canopy and planting detail; notwineglasses. Red/white accents. If a genericgarden silhouettecannotread clearly, usea recognizableMerlion-inspired stylisedicon (waterandlionform, no needphotorealism). No citylabel.
- Italy: well-proportioned Romanamphitheatre/archedfacade with multiple arches and greentouch(olivebranch), green/white/red palette; avoidplainrandomdoorway.

National colours are explicitly authorised withinstamps, sitepaletteoutside unchanged. Use small genuine flag/ribbon colourbands or fills insideoutline, nationalcolours ondetails, readable darkinklabels. Don'tmake everytinyline differentcolour. Texture/doubleborderstayssubtle; no fakecoatarms. Existingflags sourceassets may guide official colours. Limitdetailtosensibleat320 and cap total markup modest. Countryname normalclearsharedsans >=14px actual render, safe paddingwithinviewbox/rotations so noborder/textclipping. Stampoutlinescircle/oval/rect remainmixed but regularenoughprofessionallydrawn. Countrylabels notcrowdillustration or crossborder.

Builder artwork/targetedtests/screenshots, rootbrief/docs/review. Inspect1440/390/320 and compare previous. Test allnames read and notoverlapart/border, nooverflow, nationalpalettepresent, subtlehover notallnationalcoloursreplacedbynonsensicalred, no extra ongoinganimation. No fullbaseline needed unlessmarkupchangebreaksassertions. Preserveall outsidecountrygraphic HTML exactly ifpossible; minimalCSS colour additions. No commit/push.

## Coordinator review

Artwork gains layered Alpine/snow/fir details, Romanian fortified tower and mountain landscape, Greek temple façade/steps, Chilean Andes/coast/flag accent, Singapore three-tower sky-roof silhouette and Italian multi-arch amphitheatre/olive sprig. White paper, national colours and dark names improve recognition/contrast. Shape variety, angles and existing one-shot motion preserved.

Independent source review passed exact unchanged outside-artwork HTML and motion script. Chromium checks passed rendered national colour families for all six SVGs, >=14px scaled names at320, mobile2columns, panel alignment, nooverflow or repeatedmotion, reduced/noJS visibility. Desktop/320 closeups compared with prior artwork; motifs and detail improved. Requested own-colour hover darkening rather than universal navy. Syntax/whitespace checks passed.
