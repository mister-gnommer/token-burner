# Stage 2 — Ranking and data contract

Date: 2026-10-25
Status: complete

## Surprises

- The low-tier entity reviewer’s final message reported 116 includes and 19 excludes, but its saved file contained 119 and 16. Parent audit validated every position/name against the snapshot and used the file rather than the summary.
- Profile spot-checks found one additional misclassification outside the final cutoff: `Pytał Kacper Ruciński` is a late-night show format. It was corrected to exclude. Final audited totals are **118 includes, 17 excludes, zero unresolved**.
- Several catalog entries are podcasts or formats hosted by one comedian. A recognizable host does not make the format itself an individual node. Conversely, individual stage personas and performers from other disciplines remain eligible when their profiles document stand-up work.
- The source exposes global catalog positions in JSON-LD. Acquisition validation caught and rejected an initial incorrect position calculation before any ranking was frozen.

## Frozen ranking

Source: `https://standup.pl/komicy?sort=views`
Retrieved at: `2026-10-25T14:46:54Z`
Acquisition: 15 public HTML pages, 135 ordered candidates, page SHA-256 hashes retained

Selection used the user-approved rule: exclude groups, channels, organizations, podcasts, and multi-person formats, then take the first 100 individual comedians in cumulative-view source order. The source order is preserved; no separate 30-day trend enrichment was added in this stage.

- Final performers: **100**, with unique profile-slug IDs
- Batches: **10 batches of exactly 10**, all initially `pending`
- First five: Daniel Midas; Mama Na Obrotach (Klaudia Klimczyk); Łukasz Lotek Lodkowski; Rafał Pacześ; Magda Kubicka
- Rank 100: Cezary Piżewski, at unfiltered source position 114

## Artifacts

- `scripts/ranking.py` — standard-library-only acquisition and finalization. Fetch refuses non-contiguous/duplicate source orders; finalization refuses missing, duplicate, unresolved, or name-mismatched decisions and requires at least 100 eligible individuals.
- `data/ranking-candidates-20261025.json` — pre-filter source snapshot and page lineage.
- `data/ranking-decisions-20261025.json` — low-tier review (`opencode/big-pickle`), parent audit notes, correction, and one decision per candidate.
- `data/standupers.json` — frozen graph universe with rank, ID, canonical name, profile/image URLs, aliases, source position, batch, and processing status.
- `data/SCHEMA.md` — ranking lineage, evidence classes, relation semantics, and aggregation rules.
- `data/schemas/evidence.schema.json` — cited excerpts, source-scoped pseudonymous fan keys, per-performer sentiment, extraction lineage, and review state.
- `data/schemas/relation-candidate.schema.json` — undirected pairs, support/contradiction links, confidence, score versioning, and accepted/uncertain/rejected states.

## Contract decisions

Same-user rating overlap and co-endorsement require an author key and at least two performer mentions. Unresolved performer IDs cannot be aggregated. Fan-overlap and style-similarity relations stay separate. Accepted relations require at least one supporting evidence ID, one independent source, a score, scorer version, and explanation. Contradictory evidence remains stored.

Agents interpret evidence and propose structured judgments; aggregation code calculates final counts and scores. No fan evidence or graph edges were fabricated to test the schemas—validation used explicitly synthetic in-memory fixtures only.

## Validation

- Ranking: exactly 100 performers, ranks 1–100, unique IDs, sorted source positions, 10 batches of 10, and decisions consistent with the audited counts.
- JSON: candidate, decision, ranking, and schema files parse successfully.
- JSON Schema: both schemas pass `Draft202012Validator.check_schema` using the installed `jsonschema` package.
- Negative tests pass: missing same-user author key, single-mention overlap, accepted edge without evidence, and accepted edge with zero independent sources are rejected.
- `git diff --check` reports no whitespace errors.

## Next step

Stage 3: design the low-tier worker prompts, Polish-aware extraction rubric, validation/run manifests, and storage conventions. Test on a tiny sample without launching a performer batch.
