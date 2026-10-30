# Graph framework

`scripts/graph_pipeline.py` validates completed batch manifests, source candidates, evidence lineage, counts, and worker provenance before aggregation. Production uses the frozen ranking. Calibration and incomplete runs are excluded. Synthetic runs require an explicit flag and a `yyyyMMdd-synthetic-` run ID; production rejects them.

## Scorer: observed-coendorsement-v1

- Only accepted records with source-scoped author keys and extraction/mention confidence at least 0.75 qualify. This threshold is a heuristic.
- Automated support uses positive mentions in `same_user_coendorsement` and `same_user_rating_overlap` records. Neutral mentions never support an edge; repeated names and repeated endorsements by the same source-scoped fan count once.
- Mixed, unclear, unresolved, and style records are deferred with reasons. Qualified liking can be useful, but v2 has no machine-readable pair-specific appreciation field; do not infer it from a mixed label. Keep those statements for later review rather than silently treating them as dislike.
- Positive/negative contrasts in accepted fan-evidence classes are retained as opposing preference evidence. Both-negative statements alone say nothing about pairwise overlap. An edge requires at least two source-scoped fans and no opposing record.
- Score = distinct fans explicitly co-endorsing this pair / distinct observed fans positively endorsing either performer. The denominator includes eligible positive statements from all four fan-evidence classes. This normalizes observed coverage, not population popularity or sampling bias. Low scores and missing edges do not mean dissimilarity.
- Confidence averages the strongest supporting confidence per fan. Numbers are model judgments, not probabilities. `independent_fan_count` counts source-scoped identities; it does not assert distinct real people across platforms. `independent_source_count` counts distinct supporting site/URL pairs.

All relation candidates, supporting IDs, contradictions, deferred records, source URLs, and node coverage are saved in `graph.json`. No ranking position enters the score. Relations use the existing relation-candidate schema.

## D2 output

`graph.d2` is editable; `graph.svg` retains evidence tooltips; `graph.png` is the visual-check preview. Stable node IDs/order make generation repeatable, but D2 layout can move nodes between batches. Edge width represents score and labels show support/confidence. Physical distance does not encode similarity.

The renderer greedily displays highest-scoring accepted edges with at most three edges per node, retaining all candidates in JSON. Isolated nodes remain visible. D2 does not supply an interactive recommendation interface; source excerpts remain in the cited input artifacts.

## Synthetic demo

All names, preferences, URLs, worker identities, and batch metadata in `fixtures/synthetic-graph/` are fabricated. The fixture has five nodes, repeated endorsements, opposing preferences, and an isolated node. It is not a performer batch.

From the repository root:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tasks/standupers-graph/scripts/graph_pipeline.py \
  --manifest tasks/standupers-graph/fixtures/synthetic-graph/manifest.json \
  --ranking tasks/standupers-graph/fixtures/synthetic-graph/ranking.json \
  --data-root tasks/standupers-graph/fixtures/synthetic-graph \
  --output tasks/standupers-graph/graph/synthetic-demo --synthetic --render
```

For production, omit `--synthetic`, `--ranking`, and `--data-root`; pass each completed batch manifest with `--manifest` and choose an output directory. `--render` uses installed `d2 --sketch --layout elk`, then `rsvg-convert -z 2`; no browser download or added Python dependency is required. Without `--render`, only JSON and D2 sources are produced.
