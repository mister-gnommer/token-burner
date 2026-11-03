# Graph framework

`scripts/graph_pipeline.py` validates completed batch manifests, source candidates, evidence lineage, counts, and worker provenance before aggregation. Production uses the frozen ranking. Calibration and incomplete runs are excluded. Synthetic runs require an explicit flag and a `yyyyMMdd-synthetic-` run ID; production rejects them.

## Historical scorer: observed-coendorsement-v1

- Only accepted records with source-scoped author keys and extraction/mention confidence at least 0.75 qualify. This threshold is a heuristic.
- Automated support uses positive mentions in `same_user_coendorsement` and `same_user_rating_overlap` records. Neutral mentions never support an edge; repeated names and repeated endorsements by the same source-scoped fan count once.
- Mixed, unclear, unresolved, and style records are deferred with reasons. Qualified liking can be useful, but v2 has no machine-readable pair-specific appreciation field; do not infer it from a mixed label. Keep those statements for later review rather than silently treating them as dislike.
- Positive/negative contrasts in accepted fan-evidence classes are retained as opposing preference evidence. Both-negative statements alone say nothing about pairwise overlap. An edge requires at least two source-scoped fans and no opposing record.
- Score = distinct fans explicitly co-endorsing this pair / distinct observed fans positively endorsing either performer. The denominator includes eligible positive statements from all four fan-evidence classes. This normalizes observed coverage, not population popularity or sampling bias. Low scores and missing edges do not mean dissimilarity.
- Confidence averages the strongest supporting confidence per fan. Numbers are model judgments, not probabilities. `independent_fan_count` counts source-scoped identities; it does not assert distinct real people across platforms. `independent_source_count` counts distinct supporting site/URL pairs.

All relation candidates, supporting IDs, contradictions, deferred records, source URLs, and node coverage are saved in `graph.json`. No ranking position enters the score. Relations use the existing relation-candidate schema.

## D2 output

`graph.d2` is editable; `graph.svg` retains evidence tooltips; `graph.png` is a 4,000-pixel-wide visual-check preview to keep raster memory bounded. Stable node IDs/order make generation repeatable, but D2 layout can move nodes between batches. Edge width represents score and labels show support/confidence. Physical distance does not encode similarity.

Nodes show saved profile avatars where available, with names below the image. On `--render`, HTTPS image URLs (including links relative to a performer's profile) are downloaded with a five-second timeout, decoded through Pillow, and normalized to 160×160 PNGs in the output's `assets/` directory. Cached photos work offline; missing, invalid, oversized, or unreachable images use the local laughing-person SVG. Graph JSON records source URL, cache path, status, and failure reason or retrieval time. Copy `assets/` with editable D2 sources; rendered SVG embeds the images.

Without `--render`, existing cached photos are used and uncached photos fall back without network access. Synthetic runs never download photos. `avatar-preview/` separately demonstrates two saved standup.pl profile photos and the fallback, with no preference evidence or batch processing. Pillow is pinned in `requirements.txt`.

The renderer prioritizes accepted edges, then highest-scoring uncontested one-fan candidates, with at most three such edges per node. Solid edges require two supporting source-scoped fans and no opposing record; dashed amber edges are explicitly provisional. Pairs with at least two supporting source-scoped fans and opposition appear as orange dotted **DISPUTED** links, including opposing source citations. These links remain uncertain and bypass the layout degree cap so a saturated neighbor cannot hide them. Opposition-only and one-supporter opposed pairs stay in JSON. Isolated nodes remain visible.

Display policy `supported-disputes-v1` changes presentation only. Scores, evidence, opposing records and relation acceptance are unchanged. Coverage including disputed connections is reported separately from strict unopposed coverage; disputed links are not called corroborated.

For incremental previews, `--batch-view 1` shows the first batch plus any supported neighbors, including focal performers without edges. Later values include all batches up to that number. All 100 nodes remain in JSON; photos are fetched only for visible nodes. Omit the flag for the full diagram.

When no displayable edges exist, the visible performers use a five-column grid. Node labels say "scored fans" to distinguish scoring-eligible positive observations from all collected opinions. The first pilot (`batch-01/`) has no accepted edges; its 16 uncertain relation candidates remain in JSON.

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

For production, omit `--synthetic`, `--ranking`, and `--data-root`; pass each completed batch manifest with `--manifest` and choose an output directory. `--render` uses installed `d2 --sketch --layout elk`, then `rsvg-convert -w 4000`; no browser download is required. Without `--render`, JSON, D2 source, and local avatar assets are produced.

## Stage 6 scorer: observed-coendorsement-v2

The current scorer preserves v1 behavior for historical evidence v2. For reviewed evidence v3 it uses each mention's explicit personal `preference`, confidence and verbatim support independently. Unknown, unresolved and low-confidence mentions cannot create edges, but do not discard unrelated clear endorsements. Positive recommendations without personal appreciation do not enter the fan denominator. Personal-favorites replies qualify only with verified, separately attributed question context. Style evidence stays excluded, and acceptance still requires two source-scoped fans with no opposing record. Contradictions and all candidates remain inspectable. Layout distance still does not imply similarity.

Stage 6 uses replacement pilot and separate corroboration manifests. Do not also load the original pilot manifest: that would duplicate interpretations of the same posts. `batch-01/` remains the original v1 snapshot; the calibrated output is `batch-01-calibrated/`.

## Public page

On every push to `main` that touches `graph/`, `.github/workflows/pages.yml` runs `scripts/build_site.sh`. It publishes the highest-numbered `batch-NN/` that has a `view.html` as `index.html`, with its `graph.svg` and `assets/`, at https://mister-gnommer.github.io/token-burner/standupers/. The site root redirects there. The URL never changes, so a new batch only needs its own `view.html`. That file must use relative links, and the build rejects `src`/`href` values that start with `/` or `file:`. On narrow screens the view opens zoomed to 500%.

Preview locally: `bash tasks/standupers-graph/scripts/build_site.sh /tmp/site && python3 -m http.server -d /tmp/site`, then open `http://localhost:8000/standupers/`.
## Interactive HTML view

Every `graph_pipeline.py` build also writes `interactive.html` next to `graph.json`: one self-contained page (vendored D3 7.9.0, embedded avatars and cited evidence). It presents saved relations without rescoring.

The default Explore view shows one selected comedian and up to five immediate connections. Arrow buttons page through larger neighborhoods; the adjacent list includes every connection under the filters. Expand a row for supporting/opposing excerpts and known publication dates, or follow its Explore button to change focus. Opening a row on another map page brings that connection into view. Other collected evidence remains accessible below the list even when excluded by filters. All100performers, including isolates, are selectable through the name picker; its search ignores case and Polish diacritics. Focused positions are arranged for readability and do not encode similarity.

Full map retains the force layout as an optional overview. Names appear on hover or when zoomed in; clicking a comedian returns to focused exploration. Corroborated and provisional links attract as before. Supported disputes are visible by default but exert no pull; weaker contested pairs and unlinked performers have separate toggles. The collapsible coverage/legend section reports strict unopposed coverage separately. Desktop uses a persistent evidence sidebar; narrow screens put the map above the evidence list.

To re-render an existing snapshot without rebuilding it (run from the repository root):

```sh
python3 tasks/standupers-graph/scripts/render_interactive.py \
  --graph tasks/standupers-graph/graph/batch-07/graph.json \
  --output tasks/standupers-graph/graph/batch-07/interactive.html
```
