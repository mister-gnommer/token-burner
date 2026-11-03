# Paused checkpoint — 2026-11-01

Paused at the user's request. No delegated workers or queued child runs remain active. Wait for explicit resume; completion notifications do not authorize restarting research.

## Reviewed graph

`graph/coverage-source-page-tail/interactive.html` is the current reviewed graph. It has 100 nodes, 45 with a positive fan link, 12 with a corroborated link, and 33 in the largest component. There are 93 reviewed evidence records, 109 canonical sources and 82 relations: 11 corroborated, 50 provisional and 21 contested. Coverage is below the minimum target of 70; the preferred target remains 85–90.

Strict source/schema loading, exact relation/deferred recomputation, all saved graph artifacts and 100 cached photos were checked at pause. D2/SVG/4000px PNG/HTML are saved. No evidence thresholds changed. The initial expansion baseline was 34 positive-linked/26 largest component; current gains include 4 nodes from saved-source repairs and 7 from new authored sources.

## First work after resume

1. Read `STATE.md` and `reports/runs/20261031-coverage-expansion.execution.json`; the registry contains full briefs, actual model/options, task/thread IDs and budgets. Start no further research until the following saved-source work is handled.
2. Canonicalize the two raw Błażej Krajewski/Adam Sobaniec posts in `evidence/coverage-expansion/blazej-krajewski.source-candidates.jsonl`. Both pass source-candidate-v2 schema; author hashes are still null and require deterministic canonicalization. Preserve raw files. Candidate IDs are `src_cov_bkrajewski_001` and `_002`. The collection report preserves exact locators, source spellings, review publication dates and distinct event dates.
3. Delegate separate low-tier extraction and independent review. No positive graph claim is authorized by collection alone. The second post uses surnames; verify context and identity without inventing missing first names.
4. Handle recovered Elwira post separately as a source-context repair of existing `src_b05b_003` / `ev_b05_b_003`. The collector found the exact post on the Świecie aggregate event page with a Legnica, 2025-03-20 review header. Evidence and locator are in `reports/runs/20261101-coverage-blazej-krajewski.collection.json` under `repair_of`. Preserve spelling Gośiński; recover verbatim parent context from saved source/tool history if needed. Independently adjudicate. If accepted, create a full versioned batch05 replacement and exclude its original manifest; never count this old post as an additional fan.
5. Rebuild from the current graph's exact `input_manifests`, adding reviewed new run and replacing batch05 only if the repair passes. Keep the existing batch01 identity-reviewed and batch09 context-reviewed replacements; never load original and replacement together.

## Remaining research allowances

Session restart does not renew quotas. Values are saved used/remaining, not promises to find evidence.

| Slice | Queries used / left | Opens used / left | Saved raw candidates |
|---|---:|---:|---:|
| Błażej Krajewski | 24 / 0 | 5 / 19 | 2; 14 slots left |
| Piotr Jeleń | 24 charged / 0 | 6 / 18 | 0 |
| Mama Na Obrotach | 22 / 2 | 5 / 19 | 0 |
| Original source-first A, all continuations | 24 / 0 | 21 / 3 | 13 raw slots used; 3 left |
| Original source-first B, including forums | 12 / 0 | 8 / 4 | 1 raw slot used; 7 left |
| Sawczuk | 10 / 14 | 7 / 17 | 0 |
| Magda Kubicka | 17 / 7 | 14 / 10 | 1 canonical, 3 quarantined |
| Olka Szczęśniak | 16 / 8 | 19 / 5 | 2 canonical |
| Karol Modzelewski | 8 conservatively charged / 16 | 9 / 15 | 9 canonical |
| Wojtek Pięta | 24 / 0 | 23 / 1 | 4 canonical |
| Wojciech Kamiński | 8 / 16 | 7 / 17 | 6 group-review skips |

Piotr's charged queries include an invalid six-query batch whose response was lost and separately charged retries; 24 is not a count of successful searches. Future batches must have at most four queries, guarded before calls, with raw results preserved before parsing. Empty Mama/Piotr slices were not extracted or integrated and do not prove overlap is absent. Parent audits preserve these limitations.

## Access and working-tree state

Shared preview capacity is blocked by five old-session tabs. Attempts to close them through their former child thread returned `agentMismatch`. No current worker created a tab; do not bypass ownership. Normal user/app tab closing or server reset is needed before retrying blocked archives.

The separately authorized performance-verified style fallback remains access-unverified: official video players advertised caption tracks, but caption responses were empty. No style facts or links were added. Reports are under `reports/runs/20261101-performance-*` and `20261101-caption-transport-diagnostic.json`.

Campaign data, graph outputs and state remain uncommitted. The small PNG export fix in `scripts/graph_pipeline.py` and `graph/README.md` is also uncommitted; it bounds raster width at 4000. Its 22 existing tests and PNG smoke check already passed. No new application code changed during pause, so the suite was not repeated. No Git add/commit/push was performed. Source/data changes must remain separate from unrelated user work when a future commit is explicitly requested.
