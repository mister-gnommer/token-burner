# Stage 6 — calibrated pilot

Date: 2026-10-31. Same ten focal performers; no batch 2.

## Outcome
Re-extracted 15 original candidates and one new corroborating post into evidence v3: 15 accepted representations, one rejected single-performer critique, no uncertain records. Accepted representations include unknown personal preferences and are not equivalent to supported edges.

Scorer v2 yields 28 relation candidates: three accepted, 17 uncontested one-fan provisional, eight contested/opposing-only. The readable diagram displays three solid and ten dashed links under the three-edge-per-node cap; all candidates remain in JSON. It shows ten focal performers plus six incidentally supported neighbors, not a second processed batch.

Solid links: Abelard Giza–Mateusz Socha, Abelard Giza–Rafał Pacześ, Cezary Jurkiewicz–Mateusz Socha. Each has two source-scoped supporting fans and no opposing record. Socha–Pacześ remains contested despite repeated support; contradictions were not discarded. Dashed links explicitly mean one supporting fan, never corroborated overlap. Scores describe this small, targeted sample and are not population probabilities.

## Changes and surprises
- Source-candidate v2 stores separately attributed parent/thread context; evidence v3 copies it and separates personal preference from sentiment/recommendation. Clear mentions survive unrelated ambiguity.
- A verified personal-favorites question makes its direct respondent's list a personal selection. General recommendation questions do not. The new Reddit list and parent were reopened by the main agent, independently of collection.
- The extractor reset previous confidence values to .9. Parent review capped retained identities to their earlier conservative confidence; Lutka and Jakub Dąbrowski remain unresolved. Wiolka's explicit liking of jokes survives her swearing criticism; historical decline is not generalized into current appreciation.
- Previously skipped contextual recommendations are now stored accurately, with unknown personal preference. Single-performer a003 remains outside pair evidence and is rejected for scoring.
- Six targeted queries/seven open requests including follow-up yielded one new fan. Context work used four opens/two alias queries. A deleted-author candidate was excluded; no fan identity was invented.

## Provenance and checks
Low-tier Codex gpt-6-luna medium workers: `/root/stage6_context`, `/root/stage6_corroboration`, `/root/stage6_extract`. Parent Codex gpt-6.1-sol audited extraction and checked the new source attribution; a separate low-tier semantic check confirmed the three accepted pairs and recovered links. Source collector provenance remains original for re-extracted posts. Worker outputs, context audits, prompt versions/hashes and parent review survive alongside final data.

All 20 tests pass; both completed manifests pass strict schema, source/quote/context lineage, provenance and count checks. D2/ELK SVG and PNG were rendered and PNG inspected. All 16 displayed profile photos are cached; the laughing-person fallback remains available. Original batch-01 graph and evidence remain unchanged.

## Reproduce

```sh
PYTHONDONTWRITEBYTECODE=1 python3 tasks/standupers-graph/scripts/graph_pipeline.py \
  --manifest tasks/standupers-graph/reports/runs/20261031-batch01-calibrated.json \
  --manifest tasks/standupers-graph/reports/runs/20261031-batch01-corroboration.json \
  --output tasks/standupers-graph/graph/batch-01-calibrated --batch-view 1 --render
```

These manifests replace the original pilot input. Loading its original manifest too is rejected as duplicate source evidence. Batch 2 (ranks 11–20) still requires explicit authorization. No Git staging, commit or push was performed.
