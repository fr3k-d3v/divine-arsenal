# Divine Arsenal Universal — Visual Asset Manifest

**Revision:** 0.1
**Prepared:** 2026-11-13
**Target checkout:** `feat/source-atlas-psalms-visuals` on Omarchy
**Scope:** original generated artwork, historical-source imagery, and data-driven vector assets

## Visual direction

A coherent visual system combining illuminated manuscript craft, Renaissance engraving, celestial instrumentation, archival photography and restrained cyberpunk instrumentation. The application should feel like a working scholarly arsenal: atmospheric and powerful, but never a generic fantasy dashboard.

- **Core palette:** near-black / midnight navy, aubergine and indigo, antique gold, parchment; electric cyan is reserved for active instrumentation and evidence states.
- **Surface language:** dark vellum, fine grain, engraved borders, illuminated initials, restrained star fields, precise linework and deep shadow.
- **Composition:** artwork supports the interface; keep quiet negative space for real headings and controls. Do not bake UI text into artwork.
- **Typography:** real HTML/CSS fonts and verified Unicode; no generated lettering.
- **Evidence presentation:** generated artwork must be labelled **Original illustration**. Reproductions and institutional scans must retain source, shelfmark, rights and attribution.

## Generation rules

1. Generate scenes, atmospheric artwork and editorial illustrations; do not generate historical facsimiles.
2. Do not ask the image model to draw Hebrew, Enochian, Latin inscriptions, scripture, planetary glyphs, kamea numbers, pentacles or exact magical seals. These must be rendered from verified data with Unicode/SVG/canvas.
3. Never imply an AI illustration is an authentic manuscript, historical portrait, seal or artefact.
4. Keep 1 Enoch, 2 Enoch, 3 Enoch and Dee/Kelley Enochian material distinct in labels and source relationships.
5. Do not invent a visual reconstruction of Sloane MS 3189. Its grid content requires the actual manuscript data.
6. Avoid depicting an unresolved source as if its identity, edition or attribution were settled.
7. Generate responsive master compositions at the required aspect ratios; create WebP derivatives for delivery and preserve lossless PNG masters.

## A. Interface and section artwork — 4 assets

| ID | Filename | Composition / placement | Ratio | Status |
|---|---|---|---|---|
| DA-001 | `divine-arsenal-master-hero.webp` | Celestial armillary sphere, astronomical instruments and illuminated folio; right-weighted composition with clear title space on the left | 16:9 | INTEGRATED LOCALLY — 640×360 WebP derivative; 1672×941 master remains in chat |
| DA-002 | `source-atlas-hero.webp` | Archival reading room, manuscript folios, cataloguing tools and provenance motif | 16:9 | NOT STARTED |
| DA-003 | `psalter-hero.webp` | Psalter, harp, flowing water, mountains, prayer and praise; no lettering | 16:9 | NOT STARTED |
| DA-004 | `arsenal-studio-hero.webp` | Celestial instrument workshop with geometric drafting tools and blank vellum | 16:9 | NOT STARTED |

## B. Source Atlas editorial illustrations — 21 assets

These are editorial card/feature illustrations, not document reproductions. Use portrait 4:5 compositions unless otherwise noted.

| ID | Filename | Subject and visual brief | Status |
|---|---|---|---|
| DA-005 | `folio-bible-1880.webp` | Aged black leather Bible, gilt page edges and a partially open page; inspired by the user's described 1880 Bible, not an exact cover or inscription | NOT STARTED |
| DA-006 | `folio-polyglot-bible.webp` | Open polyglot Bible with parallel text columns suggested by page layout; no legible or fabricated text | NOT STARTED |
| DA-007 | `scene-job-13-15.webp` | Job in reflective dialogue amid a spare, ancient landscape; solemn, non-sensational treatment | NOT STARTED |
| DA-008 | `scene-isaiah-2.webp` | Mountain of the Lord, nations gathering and weapons being reshaped as agricultural tools | NOT STARTED |
| DA-009 | `folio-first-enoch.webp` | Enochic literary world, ancient manuscript and visionary cosmology; explicitly an original illustration | NOT STARTED |
| DA-010 | `scene-watchers-nephilim.webp` | Watchers descending and the human world below; symbolic, non-graphic and clearly interpretive | NOT STARTED |
| DA-011 | `scene-enoch-ascent.webp` | Ascent through layered heavens toward a celestial archive / heavenly tablets | NOT STARTED |
| DA-012 | `scene-tower-of-babel.webp` | Monumental unfinished tower, dispersed communities and fractured communication; no fake scripts | NOT STARTED |
| DA-013 | `scene-creation-of-humankind.webp` | Philosophical creation / awakening scene; source attribution remains unresolved, so do not label it as a verified Pymander plate | NOT STARTED |
| DA-014 | `folio-hermetica.webp` | Hermetic book, celestial instrument and contemplative study; no invented historical symbols | NOT STARTED |
| DA-015 | `folio-agrippa.webp` | Renaissance natural-philosophy study with book, compass and celestial sphere; not a portrait or plate reproduction | NOT STARTED |
| DA-016 | `folio-the-magus.webp` | Early nineteenth-century occult-philosophy volume, engraved instruments and bookbinding | NOT STARTED |
| DA-017 | `folio-kabbalah-unveiled.webp` | Scholarly Kabbalistic study setting with manuscript and diagram space; no invented Tree of Life labels | NOT STARTED |
| DA-018 | `folio-dee-conferences.webp` | John Dee's angelic-conference research setting: diary, quill, crystal and archival desk; not a claimed likeness | NOT STARTED |
| DA-019 | `folio-liber-logaeth.webp` | Archival study of a dense manuscript grid, but with no purportedly accurate characters or 49×49 content | NOT STARTED |
| DA-020 | `folio-enochian-studies.webp` | Dee/Kelley research setting and blank chart folio; never fabricate the Enochian alphabet | NOT STARTED |
| DA-021 | `folio-armadel.webp` | Grimoire folio, bookbinding and blank diagram panel; no invented sigils | NOT STARTED |
| DA-022 | `folio-amulets-talismans.webp` | Historical-style metal, stone and parchment objects; no falsely attributed inscriptions | NOT STARTED |
| DA-023 | `folio-mythic-tarot.webp` | Original mythic archetype artwork, not a copy of a commercial deck | NOT STARTED |
| DA-024 | `folio-rosicrucian.webp` | Original rose-and-cross inspired scholarly illustration, clearly modern | NOT STARTED |
| DA-025 | `scene-michael-spiritual-warfare.webp` | Archangel Michael confronting the dragon; powerful, reverent, non-graphic composition | NOT STARTED |

## C. Psalter collection — 15 assets

Five book-divider illustrations and ten featured Psalm scenes. Other Psalm pages use the same visual system, category SVGs and typographic layouts; 150 unrelated AI images are not required.

| ID | Filename | Subject | Ratio | Status |
|---|---|---|---|---|
| DA-026 | `psalter-book-i.webp` | Book I, Psalms 1–41: wisdom, righteous tree, living water and lament | 16:9 | NOT STARTED |
| DA-027 | `psalter-book-ii.webp` | Book II, Psalms 42–72: longing, kingship, justice and water | 16:9 | NOT STARTED |
| DA-028 | `psalter-book-iii.webp` | Book III, Psalms 73–89: sanctuary, crisis and covenant | 16:9 | NOT STARTED |
| DA-029 | `psalter-book-iv.webp` | Book IV, Psalms 90–106: wilderness, divine kingship and refuge | 16:9 | NOT STARTED |
| DA-030 | `psalter-book-v.webp` | Book V, Psalms 107–150: restoration, pilgrimage, thanksgiving and praise | 16:9 | NOT STARTED |
| DA-031 | `psalm-001.webp` | Psalm 1: tree planted beside streams | 4:5 | NOT STARTED |
| DA-032 | `psalm-019.webp` | Psalm 19: heavens declaring glory | 4:5 | NOT STARTED |
| DA-033 | `psalm-023.webp` | Psalm 23: shepherd, valley and still waters | 4:5 | NOT STARTED |
| DA-034 | `psalm-027.webp` | Psalm 27: light, fortress and sanctuary | 4:5 | NOT STARTED |
| DA-035 | `psalm-042.webp` | Psalm 42: deer longing for flowing water | 4:5 | NOT STARTED |
| DA-036 | `psalm-051.webp` | Psalm 51: repentance, mercy and restoration | 4:5 | NOT STARTED |
| DA-037 | `psalm-091.webp` | Psalm 91: refuge and shelter beneath wings | 4:5 | NOT STARTED |
| DA-038 | `psalm-121.webp` | Psalm 121: mountains and the keeper | 4:5 | NOT STARTED |
| DA-039 | `psalm-139.webp` | Psalm 139: human existence within the vastness of creation | 4:5 | NOT STARTED |
| DA-040 | `psalm-150.webp` | Psalm 150: instruments, music and universal praise | 4:5 | NOT STARTED |

**Psalter data constraint:** the Hebrew/Masoretic and LXX/Vulgate numbering systems must remain separate. Bind art to the canonical work ID and edition-aware coordinate, never to a naked chapter number. Text and translations are a separate rights-reviewed data task.

## D. Planetary archetype illustrations — 7 assets

Square 1:1 editorial art, with no glyphs, numbers, seals or predictive claims.

| ID | Filename | Traditional visual theme | Status |
|---|---|---|---|
| DA-041 | `planet-saturn.webp` | Time, structure, limits and endurance | NOT STARTED |
| DA-042 | `planet-jupiter.webp` | Sovereignty, expansion and wisdom | NOT STARTED |
| DA-043 | `planet-mars.webp` | Conflict, courage and force | NOT STARTED |
| DA-044 | `planet-sun.webp` | Illumination, vitality and clarity | NOT STARTED |
| DA-045 | `planet-venus.webp` | Harmony, beauty and relationship | NOT STARTED |
| DA-046 | `planet-mercury.webp` | Language, exchange and intelligence | NOT STARTED |
| DA-047 | `planet-moon.webp` | Cycles, reflection and change | NOT STARTED |

## E. Reusable UI textures and ornament — 3 assets

| ID | Filename | Brief | Status |
|---|---|---|---|
| DA-048 | `texture-celestial-ink.webp` | Seamless near-black / aubergine ink field with extremely restrained star grain | NOT STARTED |
| DA-049 | `texture-antique-vellum.webp` | Seamless aged vellum / manuscript paper texture, low contrast | NOT STARTED |
| DA-050 | `ornament-gold-folio.png` | Transparent gold engraved corner and divider ornaments; no text or symbols | NOT STARTED |

## Assets that must be rendered from verified data, not image generation

- Hebrew alphabet, letter forms, divine names and vocalisation.
- Enochian alphabet and any chart transcription.
- The 49×49 and 36×72 Logaeth tables.
- Planetary kamea and their numeric arrangements.
- Solomonic pentacles, angelic seals and attributed sigils.
- The 72 Names and other exact Hebrew constructions.
- Tree of Life / Sephirotic diagrams and correspondence tables.
- Zodiac glyphs, planetary glyphs, chart wheels and actual astronomical positions.
- Psalm text, verse references, translation layouts and citations.
- Historical manuscript folios, title pages, portraits and institutional facsimiles.

These are structured SVG/canvas renderings or rights-cleared source images. Generated artwork may frame them, but must not supply their data.

## Source and rights research register

- **Psalter structure:** the USCCB Psalms introduction confirms 150 songs, five books and differences between Hebrew and Septuagint/Vulgate numbering: https://bible.usccb.org/bible/psalms/0
- **Agrippa:** Library of Congress, *Three Books of Occult Philosophy*, 1898, LCCN 11008996; the record explicitly states the digitised collection is public domain and free to use and reuse: https://www.loc.gov/item/11008996/
- **Barrett:** Library of Congress, *The Magus*, 1801, LCCN 11015009; 445 digitised images. The Library says it is not aware of U.S. copyright or other restrictions, which is not the same as a universal rights clearance: https://www.loc.gov/item/11015009/
- **Sloane MS 3188:** British Library catalogue identifies John Dee's conferences with angels, 1581–1583; current catalogue entry reports the digital images unavailable: https://searcharchives.bl.uk/catalog/040-002115572
- **Sloane MS 3189:** British Library catalogue identifies *Liber Mysteriorum Sextus et Sanctus / Book of Enoch / Liber Logaeth*, transcribed by Edward Kelley in 1583, with 49×49 grids; digital images are currently unavailable: https://searcharchives.bl.uk/
- **Psalter visual reference:** British Library Lansdowne MS 420 is an illuminated Psalter with decorated initials and marginal imagery; the linked rights note says public domain in most countries other than the UK and refers to BL terms: https://iiif.biblissima.fr/collections/manifest/e867d8e3a05b81f30c39abcc5f58b221cabeb760
- **Additional Psalter reference:** British Library Add MS 35283 is a bilingual Latin / Anglo-Norman Psalter with decorated initials; rights note also requires attention to UK terms: https://iiif.biblissima.fr/collections/manifest/7f6c88df74b0bcb87f027e78fd443e5209095136

## Integration order

1. Establish image dimensions, palette and crop rules using DA-001.
2. Add the image asset manifest and a local-only static asset route.
3. Build Source Atlas cards with source-specific art and visible provenance labels.
4. Build the Psalter book dividers, featured Psalm pages and reusable Psalm card template.
5. Add the planetary archetype art around the existing calculated data and vector seals.
6. Add remaining historical and narrative illustrations.
7. Test desktop/mobile crop, loading, contrast, reduced motion, accessibility and offline/local-only behaviour.

## Current state and blockers

- **DA-001:** original 1672×941 master generated in chat; 640×360 WebP derivative integrated into the Omarchy checkout at `divine/web/assets/divine-arsenal-master-hero.webp`.
- **Static delivery:** local-only `/assets/` mount added; hero background is responsive and uses the existing same-origin CSP.
- **Remaining artwork:** DA-002 through DA-050 are not yet integrated as standalone production assets.
- **Not started:** remaining 49 assets.
- **Historical images:** use institutional scans only after item-level rights, attribution and access checks.
- **Unresolved sources:** do not convert UNKNOWN catalogue records into definitive historical visual claims.
- **Release:** no deployment or public release is implied by this asset plan.
