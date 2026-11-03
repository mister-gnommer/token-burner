# Fan continuation integration

## Surprises

- Actual extracted mention rows are A003: 4 total / 3 mapped; A005: 2 / 2; B001: 4 / 3. B001 has six names in the visible list, but only four mention records, of which three have frozen identities. The other list entries do not become graph identities.
- Four duplicate raw A posts were excluded before extraction. They are not new sources or skips; the three canonical inputs yielded 3 accepted records and 0 skips.
- The collection reservation write failed before the first open. The attempted open was counted afterward and the allowance remained within cap.
- A003 remains `fan_comparison` with unknown personal preferences. Its fan-authored style description is not performance-verified fallback evidence.

## Integration

Finalized both manifests as `completed`: source-first follow-up has 2 candidates / 2 extracted / 2 accepted; fan-forums-B follow-up has 1 / 1 / 1. Each has 0 uncertain, rejected, and skipped records. B001 is a historical 2012 favorite reply; only Abelard Giza, Kacper Ruciński, and Cezary Pazura map to frozen identities. A005 explicitly likes Katarzyna Piasecka and Grzegorz Dolniak. Unknown preferences were left unknown.

The build used 20 manifests: the 18 recorded in the source-first graph plus each new manifest once. The identity-reviewed batch-01 and context-reviewed batch-09 replacements remain included; their originals remain excluded. All evidence was reloaded through the strict graph loader. Aggregate relations and deferred records reproduced exactly (timestamps excluded from relation comparison).

## Graph changes

| Measure | Baseline | Current |
|---|---:|---:|
| Performers with displayable positive links | 41 | 43 |
| Displayable links | 52 | 54 |
| Corroborated-linked performers | 12 | 13 |
| Corroborated links | 11 | 12 |
| Largest displayable component | 31 | 31 |
| Displayable component sizes | 31, 2, 2, 2, 2, 2 | 31, 2, 2, 2, 2, 2, 2 |

Displayable degree totals are 104 baseline and 108 current; corroborated degree totals are 22 and 24. The two newly linked performers are Grzegorz Dolniak and Katarzyna Piasecka (displayable degree 1 each).

**New one-fan links (provisional):** Cezary Pazura — Kacper Ruciński (B001), and Grzegorz Dolniak — Katarzyna Piasecka (A005). Neither is corroborated. There are no new contested relations; the graph retains 20 contested candidates overall, which remain non-displayable.

**Corroborated changes:** Abelard Giza — Cezary Pazura moved from 1 fan / uncertain to 2 fans / accepted. Abelard Giza — Kacper Ruciński remains accepted and increased from 2 to 3 fans. No other existing relation changed fan count or status. A003 is deferred for its unresolved Borkowski mention; B001 has a deferred unresolved Krzysztof Piasecki mention. Its mapped positive identities can still score under the v2 scorer.

No gain is predicted from these observations. One-fan links remain provisional. The three new records come from separate source-local authors across Reddit, Gazeta, and Filmweb; those keys do not establish cross-platform identity. B001 is historical evidence, not current fandom, and the small source-family sample does not establish population coverage.

## Validation and artifacts

Source-candidate (3), evidence-v3 (3), and run-manifest (2) schemas passed via `evidence_pipeline.py`. Strict loading verified candidate/run lineage, source excerpt, language and context equality, source/context author hashes, extractor provenance, accepted reviewer fields, literal mention surfaces, preference quotes, run counts, and duplicate run/post constraints. 100 cached photos were copied before rendering; no downloads were made. JSON, editable D2, SVG, PNG, and interactive HTML were saved under `graph/coverage-fan-continuations/`. The pipeline's 2× raster conversion stalled at 23,054 × 6,912, so `graph.png` was rendered from the saved SVG at 4,000 px wide; a small SVG thumbnail was inspected.

Exact graph inputs, per-record mention accounting, validation results, relation changes, and the full one-fan/corroborated/contested lists are in [the integration record](runs/20261101-coverage-fan-continuations.integration.json). The manifest-count changes are limited to the two authorized manifests.

**TL;DR:** 3 accepted records integrated; +2 displayably linked performers, +1 corroborated-linked performer; largest component remains 31. No skips or new contested links.
