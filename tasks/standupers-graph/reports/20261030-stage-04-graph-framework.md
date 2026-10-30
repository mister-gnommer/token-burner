# Stage 4 — aggregation and D2 framework

Date: 2026-10-30. Stage 4 complete; no performer batch started.

## Decisions and surprises
- D2 selection committed separately as `73904e1`, as requested. Installed D2 is `v0.6.9-HEAD`, with bundled ELK; `rsvg-convert` is installed. No dependency was added.
- Scorer `observed-coendorsement-v1` requires two source-scoped fans explicitly endorsing the same pair, excludes calibration/incomplete runs, and blocks visible edges when opposing preference evidence exists.
- Score divides distinct co-endorsing fans by the observed union of fans positively endorsing either performer. This reduces observed coverage/popularity bias but cannot correct unobserved sampling bias or estimate population preference.
- The current evidence contract lacks explicit pair-specific appreciation for mixed records. V1 conservatively defers those records, including explicit liking with caveats, rather than infer every pair from a mixed label. Useful evidence remains saved; pilot yield may be sparse.
- D2 gives schematic layouts. Node distance is not a similarity metric; width and labels convey evidence. Node order is stable, but coordinates can change between batches.

## Outputs
- `scripts/graph_pipeline.py`: schema/lineage checks, conservative aggregation, source-scoped deduplication, contradictory/deferred evidence, graph JSON, D2 generation, SVG/PNG rendering.
- `fixtures/synthetic-graph/`: five fabricated performers, six source/evidence records, and clearly synthetic batch-shaped metadata. No real collection or worker run is implied.
- `graph/synthetic-demo/`: JSON, editable D2 source, SVG with citation tooltips, and inspected PNG preview. Three relation candidates are stored; two are shown, one opposing-only candidate stays uncertain. The duplicate fan does not inflate support, and isolated nodes remain visible.
- `graph/README.md`: scoring rules, caveats, and reproducible commands. The renderer displays at most three strongest accepted edges per node while retaining every candidate in JSON.

## Verification
All 12 standard-library tests pass. Checks cover observed-coverage normalization, duplicate fans/names, neutral/comparison exclusions, opposing preferences, review/interpretation/confidence gates, calibration exclusion, source tampering, synthetic/production separation, and isolated nodes. Generated relations pass the existing schema inside aggregation.

The actual installed CLI rendered the fixture through D2/ELK to SVG and then PNG without a browser download. The image was inspected and layout adjusted for readable labels and a visible synthetic disclaimer. Used D2 syntax was checked against Context7's [official D2 source documentation](https://github.com/d2lang/d2).

## Limits and next step
No real batch, source-yield audit, statistical calibration, or 100-node readability check occurred. The static graph has tooltips and saved citations, not an interactive recommendation interface. Confidence values are model judgments. Cross-site fan keys do not prove distinct people.

Next is Stage 5: process ranks 1–10 only on an explicit user command, audit evidence yield, and save its graph/report before considering another batch.
