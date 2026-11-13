# Primary-source research addendum — Divine Arsenal

**Research date:** 2026-11-12  
**Purpose:** Extend the photographed-source catalogue with institutionally catalogued primary material, digital-humanities standards, textual distinctions and implementation consequences.

## Executive findings

1. The photographed material should be treated as a *research corpus with multiple provenance layers*, not as one unified occult canon.
2. The photographed 49×49-style letter/number grid is worth investigating against John Dee's Sloane MS 3189. The British Library catalogue identifies Sloane MS 3189 as *Liber Mysteriorum Sextus et Sanctus*, also called *The Book of Enoch* or *Liber Logaeth*, transcribed by Edward Kelley in 1583; it describes grids of 49 rows by 49 columns from folio 10r onwards. This is a strong research lead, **not yet proof that the user's photographed grid is a reproduction of that manuscript**.
3. Sloane MS 3188 records Dee's angelic conferences from 22 December 1581 to 30 May 1583 in five books. The catalogue notes the manuscript's relationship to Ashmole MS 3677 and missing leaves. Treat it as a distinct archival object from Sloane MS 3189.
4. The Library of Congress has digitised *The Magus* (Francis Barrett, 1801) and an 1898 edition of Agrippa's *Three Books of Occult Philosophy* (Book I). These are accessible research objects with image sequences, metadata and IIIF manifests. The 1898 Agrippa volume is an edition/translation/compilation, not the original sixteenth-century publication.
5. TEI P5 and IIIF Presentation API 3.0 provide a practical standards-based route for manuscript description, page structure, facsimile/transcription alignment and interoperable image viewing.
6. W3C PROV-DM gives a formal conceptual model for provenance: entities, activities, agents, derivations and responsibility. Use it as an interoperability target rather than inventing an opaque trust score.
7. Psalm numbering can differ between Hebrew/Masoretic and Septuagint/Vulgate traditions. Store canonical work identity separately from edition-specific chapter/verse coordinates.
8. Copyright must be tracked per edition, translation, image and dataset. A public-domain underlying work does not make every modern translation or digitised image automatically reusable for every commercial use.

## High-value archival sources

### British Library — Dee manuscripts

- **Sloane MS 3188 — John Dee's conferences with angels:** https://searcharchives.bl.uk/catalog/040-002115572
  - Catalogue describes folios 1r–169v, dated 22 December 1581–30 May 1583, in five books.
  - It notes that Ashmole made a fair copy, now Sloane MS 3677.
  - It describes the material as records of angelic/spirit communications mediated by a crystal ball; this is the catalogue's description of the historical document, not a verified supernatural event.
  - Some leaves are missing; catalogue records an anecdote about their reuse as pie-dish liners.
- **Sloane MS 3189 — Liber Mysteriorum Sextus et Sanctus / Book of Enoch / Liber Logaeth:** https://searcharchives.bl.uk/catalog/040-002115572 (catalogue collection result; search exact shelfmark)
  - British Library catalogue describes ff. 1r–65r and transcription by Edward Kelley in 1583.
  - From f. 10r onwards, the material includes letters and numbers in 49-row × 49-column grids.
  - This is directly relevant to the photographed letter/number grids. It remains a candidate comparison only until the image is matched to a specific folio, edition and plate.
- **Sloane collection digitised-content search:** https://searcharchives.bl.uk/?f%5Bmaterial_type_si%5D%5B%5D=Archives+and+Manuscripts&f%5Bproject_collections_ssim%5D%5B%5D=Sloane+Collection
  - Some catalogue entries may have digitised content marked unavailable. Do not imply that a scan can be downloaded where the catalogue says unavailable.

### Library of Congress and Science History Institute

- Francis Barrett, *The Magus, or Celestial Intelligencer* (London, 1801): https://www.loc.gov/item/11015009/
  - LOC record includes online text, image sequence (445 images), IIIF manifest and rights caveat.
  - LOC says it is not aware of U.S. copyright or other restrictions in the collection but warns some content may remain protected under applicable law.
- Science History Institute, *The Magus* (1801): https://digital.sciencehistory.org/works/mnmbdim
  - Digitised plates and selected pages; rights shown as Public Domain Mark 1.0.
- Agrippa, *Three Books of Occult Philosophy or Magic*, Book I (Chicago, 1898 edition): https://www.loc.gov/item/11008996/
  - LOC describes a 1898 edition, with Willis F. Whitehead and Henry Morley also named in the record, and marks the digitised book public domain.
  - Do not describe this 1898 object as a sixteenth-century original. Use its bibliographic record and edition metadata.

### Enochic studies

- James C. VanderKam, “The Book of Enoch and the Qumran Scrolls,” *Oxford Handbook of the Dead Sea Scrolls*: https://doi.org/10.1093/oxfordhb/9780199207237.003.0011
  - Describes 1 Enoch as a collection of ancient booklets written at different times, mostly originally in Aramaic, and discusses textual witnesses and Qumran evidence.
- James C. VanderKam, “The Book of Enoch,” *R. H. Charles: A Biography* (OUP, 2023): https://doi.org/10.1093/oso/9780192869289.003.0003
  - Useful for the history of Western discovery, editing, translation and modern scholarship.
- John C. Reeves, “Enoch, Books of,” *Encyclopaedia Iranica*: https://www.iranicaonline.org/articles/enoch-books-of/
  - Useful reference on the surviving textual families and the Aramaic, Greek, Syriac, Latin and Ethiopic evidence.
- Gabriele Boccaccini, “Enochic Traditions”: https://doi.org/10.1093/oso/9780190863074.003.0020
  - Useful for reception history and the intersection with Christian Cabala, Hermetic circles and John Dee.

**Required modelling:** distinguish 1 Enoch, 2 Enoch, 3 Enoch and later Enochian/Dee material. Do not let the shared name imply shared date, language, authorship or textual origin.

### Kabbalah and Zohar

- Jeremy Philip Brown, “Zohar,” *Oxford Bibliographies in Jewish Studies* (published 22 September 2025): https://doi.org/10.1093/obo/9780199840731-0263
  - Notes the traditional attribution to Simeon bar Yochai and the late-thirteenth-century Castilian setting of the most formative Zoharic material.
- Pinchas Giller, *Reading the Zohar: A Sacred Text of Kabbalah* (OUP): https://doi.org/10.1093/acprof:oso/9780195118490.001.0001
  - Scholarly introduction to Zoharic textual traditions and classical Kabbalah.

**Required modelling:** keep Jewish Kabbalah, Christian Cabala, Hermetic Qabalah and later popular/esoteric adaptations distinct. Mathers' *The Kabbalah Unveiled* is a historically important Western esoteric translation path, not a neutral replacement for the Zohar or contemporary Jewish scholarship.

### Standards for digital editions and provenance

- **TEI P5 Guidelines:** https://guidelines.tei-c.de/en/html/index.html
  - Current version surfaced in research: 4.12.0, updated 28 July 2026.
  - TEI supports manuscript/printed-source descriptions, structural transcription, editorial interventions, uncertainty and parallel facsimile/transcription representations.
- **TEI representation of primary sources:** https://guidelines.tei-c.de/en/html/PH.html
  - The `facsimile`, `sourceDoc` and textual structures can be used in parallel; sourceDoc can combine facsimile and transcribed text.
- **IIIF Presentation API 3.0:** https://iiif.io/api/presentation/3.0/
  - Standard for compound digital objects and rich viewers.
- **IIIF API overview:** https://iiif.io/api/
  - Image API 3.0, Presentation API 3.0, Authorization Flow API 2.0, Change Discovery API 1.0 and Content Search API 2.0 are listed as current specifications.
- **W3C PROV-DM:** https://www.w3.org/TR/prov-dm/
  - Generic provenance model for entities, activities, agents, derivations, responsibility and bundles.
- **Manuscript workflow research:** https://iris.cnr.it/handle/20.500.14243/579481
  - Describes orchestration of IIIF, eScriptorium, ALTO XML, TEI P5 and TEI Publisher in a reproducible manuscript transcription/publishing workflow.

**Architecture recommendation:** IIIF for image interoperability; TEI P5 for scholarly textual encoding; W3C PROV concepts for provenance; local database/search index for application queries. Do not build a proprietary page-image or transcription format when mature standards exist.

### Psalter numbering and licensing

- Oxford Academic source describing differences between Gallican/LXX and Masoretic/Hebrew Psalm numbering: https://academic.oup.com/edited-volume/45761/chapter/398724013
  - Psalm coordinates diverge at Psalm 9 onward in common numbering tables, with further split/merge differences.
- API.Bible licensing: https://care.api.bible/article/369-understanding-api-bible-licensing
  - Distinguishes open-access and copyrighted translations; commercial applications can require commercial agreements.
- Biblica permissions: https://www.biblica.com/permissions/
  - Full Bible permissions and eligible open licences have specific conditions.

**Required modelling:** Psalm 9 (Hebrew) is not always Psalm 9 (LXX/Vulgate); do not hard-code one universal coordinate. Canonical work ID, source edition, versification system and local coordinate must be separate fields. Store licensing/rights data for text and media independently.

## Critical new discovery: 49×49 grids

The photographed page shows a 49×49-looking letter/number table. The British Library description of Sloane MS 3189 explicitly mentions 49×49 letter/number grids in *Liber Logaeth*. This is a high-value lead.

Research task:
1. Obtain the full catalogue record and any available images or reliable facsimiles for Sloane MS 3189.
2. Find scholarly descriptions and plate reproductions of Liber Logaeth.
3. Compare the user's photographed grid only if a matching public-domain/licensed plate is located.
4. Record visual similarity as HYPOTHESIS until the plate/folio is matched.
5. If matched, record exact shelfmark, folio, edition, source URL and transformation history.
6. Implement grid structures as data: dimensions, cells, alphabet/encoding variant, row/column numbering, transcription confidence and source coordinate.
7. Never infer hidden messages or supernatural effects merely from a numerical pattern.

## Research confidence vocabulary

Use only explicit labels:
- **VERIFIED FACT:** supported by direct primary record or reproducible measurement.
- **HISTORICAL CLAIM:** attributed to a dated source or named scholar/catalogue.
- **TRADITIONAL INTERPRETATION:** meaning within a named tradition.
- **RECONSTRUCTION:** modern transcription, vectorisation, translation or restoration.
- **HYPOTHESIS:** proposed link awaiting evidence.
- **UNKNOWN:** unresolved or inaccessible.
- **CONTRADICTED:** evidence conflicts with the proposed claim.

No universal “truth score” and no unexplainable confidence percentage. Confidence is per claim and evidence chain.

## Research tasks to keep open

- [ ] Inspect full catalogue records for Sloane MS 3188 and MS 3189.
- [ ] Locate authoritative, rights-cleared Liber Logaeth images and compare to the photographed grid.
- [ ] Identify the exact source/edition of the photographed Enochian alphabet chart.
- [ ] Verify the user's *Kabbalah Unveiled* edition and title-page data.
- [ ] Verify the exact edition of *The Grimoire of Armadel* and manuscript witness.
- [ ] Identify *Secrets of the Magical Grimoires*, *The Mystical Traditions*, *Anatomy of Witchcraft*, *The Tarot Court Cards* and *I Am Healing* from title/copyright pages.
- [ ] Identify the Polyglot Bible edition and all languages represented; title page alone is insufficient.
- [ ] Transcribe the 1880 Bible inscription without guessing names or relationship.
- [ ] Build a Psalm versification mapping dataset from documented sources and test divergent coordinates.
- [ ] Create a per-edition rights matrix before importing full text or scans.

## Bibliographic caution

Search-result abstracts and collection catalogue pages are discovery aids, not substitutes for reading the full book, manuscript or critical edition. Record the exact source actually inspected, date accessed, page/folio and limitations. Where only an abstract or catalogue description is available, say so.
