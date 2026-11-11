# Task ledger and gaps

| ID | Dependency | State | Work |
|---|---|---|---|
| P0-AUDIT | none | PASS | baseline reproduced; sandbox hang isolated |
| P1-ATLAS | P0 | IN PROGRESS | 27 records/schema/rights/search implemented; fresh source verification pending |
| P2-PSALTER | P1 model | IN PROGRESS | 150-record index/coordinate model implemented; text and verse review pending |
| P3-LANGUAGE | P1 model | IN PROGRESS | two named schemes/trace/RTL implemented; inventory/transformations pending |
| P4-IIIF | P1 model | IN PROGRESS | bounded local subset + synthetic viewer tested; institutional proof blocked |
| P5-SVG | existing arithmetic | IN PROGRESS | labelled SVG tested; full editor/source trace pending |
| P8-UI | model tests | IN PROGRESS | integrated UI/browser smoke; full a11y/manual checks pending |
| P9-SECURITY | P0 | IN PROGRESS | Host/origin/limits/import/path tests added; full audits pending |
| R-REMOTE | network | BLOCKED | PR/CI, fresh institutional/standards retrieval |
| R-RIGHTS | source evidence | BLOCKED | rights-cleared Psalm text edition |
| R-GRID | exact folio | UNKNOWN | 49×49 resemblance remains HYPOTHESIS |
| R-ENOCHIAN | chart edition | UNKNOWN | attested alphabet inventory |
| R-RELEASE | all release gates | NOT STARTED | external review, independent astronomy, TEI schema, a11y |

No global agent activation, scheduler, deployment or merge is authorized here.
The implementation session itself is the project-scoped agent; staged adapter
configuration is not evidence of a live provider task or completed agent bridge.
