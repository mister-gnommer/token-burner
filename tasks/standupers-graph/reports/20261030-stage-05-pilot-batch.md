# Stage 5 — pilot batch, ranks 1–10

Date: 2026-10-30. Pilot complete; ranks 11–20 have not started.

## Result
**15 distinct source candidates → 12 reviewed evidence records → 9 accepted, 3 uncertain, 0 rejected; 3 candidates skipped with reasons.** The unchanged scorer produced **16 uncertain relation candidates and zero accepted edges**. Thirteen pairs have one qualifying co-endorsing fan; three have only opposing preference evidence. None meets the two-fan acceptance threshold.

The saved D2/SVG/PNG graph shows the ten focal performers with photos and no edges. All 100 performers and all candidate relations remain in `graph/batch-01/graph.json`. Missing edges indicate insufficient established support, not dissimilarity. Scored-fan counts include only scoring-eligible statements.

## Coverage

| Performer | Candidate records | Accepted evidence records | Scored positive fans |
|---|---:|---:|---:|
| Daniel Midas | 7 | 4 | 2 |
| Mama Na Obrotach | 0 | 0 | 0 |
| Łukasz Lotek Lodkowski | 8 | 6 | 2 |
| Rafał Pacześ | 7 | 4 | 1 |
| Magda Kubicka | 4 | 1 | 1 |
| Mateusz Socha | 6 | 4 | 3 |
| Olka Szczęśniak | 3 | 2 | 1 |
| Cezary Pazura | 1 | 1 | 1 |
| Piotr Jeleń | 0 | 0 | 0 |
| Abelard Giza | 4 | 4 | 3 |

Record counts include neutral, negative, and qualified readings; they are not fan counts. One record may cover several performers. Mama/Piotr zero yields reflect the bounded search, not absence of fans. Pazura's one candidate is historical, from [Filmweb in 2012](https://www.filmweb.pl/person/Abelard%2BGiza-286174/discussion/Jakie%2Bs%C4%85%2Bwasze%2Bulubione%2Bkabarety-1936249).

## Collection and verification
Three separate low-tier Codex `gpt-6-luna` collectors covered all ten focal performers. Across their reports: 27 queries and 22 page-open requests, within each worker's 12-query/12-open limit. They returned 16 candidates from seven thread pages on Reddit, Gazeta, Wykop, and Filmweb; one duplicate author/post was removed. Separate `gpt-6-luna` extraction and independent Claude `claude-haiku-5-5` review followed, all at medium effort. Execution IDs/options and immutable prompt hashes are saved under `reports/runs/20261030-batch01-pilot.*`. Measured token/money usage was unavailable; no cost estimate is invented.

Parent audit reopened the sources, corrected a Reddit parent/reply author mix-up, canonicalized site labels before deriving fan keys, and retained only supported date precision. Raw worker collection files remain preserved. Candidate target lists needed corrections and must not replace source-text entity checks.

Independent verification removed a fabricated mention copied from another record, nulled an unsupported performer ID, corrected five sentiment overreaches and four non-verbatim surface forms, and retained three uncertain records. Parent review restored Kołecki's positive recommendation: a drugs/sex content description is not criticism. Both worker outputs and the parent decision are preserved. The verifier's stale-manifest warning was inaccurate; the actual parent checkpoint was already verifying with 12 extracted records.

## Why no edges
Seven reviewed records are deferred by v1: three uncertain reviews, two qualified/ambiguous interpretations, one missing fan key, and one below the identity-confidence threshold. A valid broad recommendation contributes observed positive coverage but is not automatic pairwise co-endorsement. Remaining direct pairs have only one qualifying fan each; some also have opposing preferences. The thresholds and evidence classes were not loosened to populate the diagram.

This pilot demonstrates a collection/representation bottleneck, not that the performers are unrelated. Relevant source examples include [explicit favorites and caveats on Gazeta](https://forum.gazeta.pl/forum/w,567,176877280,176877280,Stand_up.html), [genre-dependent recommendations](https://www.reddit.com/r/poland/comments/1egewxi/polish_standup_comedy/), and [comparisons on Wykop](https://wykop.pl/link/7849575/prokuratoura-czyli-jak-rafal-paczes-sprzedal-nam-bilety-do-rynsztoku).

## Artifacts and checks
- `evidence/batch-01/`: original collections, canonical source candidates, original extraction, skips, independent review snapshot, and final reviewed evidence.
- `reports/runs/20261030-batch01-pilot.*`: manifest, execution, source audit, independent verification, adjudication, normalization/deduplication, and coverage.
- `graph/batch-01/`: full JSON, editable D2, embedded-image SVG, PNG, and cached photo assets. All ten displayed photos downloaded successfully.
- All 17 tests and schema/lineage checks pass. The actual installed D2/ELK renderer produced the graph, and its PNG was inspected. The incremental batch view keeps unprocessed nodes in JSON without crowding the diagram; zero-edge views use a grid. Prior avatar enhancements are included in this milestone.

Rebuild from the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tasks/standupers-graph/scripts/graph_pipeline.py \
  --manifest tasks/standupers-graph/reports/runs/20261030-batch01-pilot.json \
  --output tasks/standupers-graph/graph/batch-01 --batch-view 1 --render
```

## Next step
Stage 6 calibration before another batch: distinguish explicit pairwise appreciation from sentiment/subject-matter caveats, store recommendation parent context without merging speakers, validate aliases, and target repeated support for the same pairs. Re-audit this pilot after any versioned contract/scorer change. Preserve the fan-preference goal; no style-similarity substitute or batch 2 has been authorized.
