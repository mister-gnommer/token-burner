# Data contract

## Ranking lineage

- `ranking-candidates-YYYYMMDD.json` preserves the source order and page metadata before filtering. It is the acquisition snapshot, not the graph universe.
- `ranking-decisions-YYYYMMDD.json` records an include/exclude decision and reason for every candidate. `uncertain` is a temporary review state and cannot be finalized.
- `standupers.json` is the frozen graph universe. Performer `id` is the unique standup.pl profile slug; `source_position` preserves the unfiltered catalog position, while `rank` is assigned after filtering. `batch` is 1–10 and `status` begins as `pending`.

Do not silently replace the frozen list with a newer trend. A refresh is a new, explicitly approved source decision.

## Evidence records

`schemas/evidence.schema.json` describes one cited source excerpt plus its AI interpretation. Store records as JSON Lines in `evidence/<batch>/`.

Evidence classes:

1. `same_user_rating_overlap` — structured evidence that one source-scoped user rated at least two performers.
2. `same_user_coendorsement` — one person explicitly expresses appreciation for multiple performers in natural language.
3. `fan_recommendation` — a fan recommends one performer in relation to another.
4. `fan_comparison` — a fan compares performers, including contrasts or one-sided praise.
5. `style_similarity` — humor/style similarity evidence, kept separate from fan overlap.

A name co-mention is not necessarily co-preference. Same-user overlap/co-endorsement records require at least two mentions and an author key. Each mention has its own sentiment and confidence. `performer_id: null` marks an unresolved entity and prevents automatic relation aggregation. `author_key`, when available, is pseudonymous and source-scoped; never join fan identities across platforms.

Preserve the exact excerpt, URL, retrieval time, extraction model/prompt version, and review status. Low confidence or rejected interpretations remain stored for audit but do not support accepted edges.

## Relation candidates

`schemas/relation-candidate.schema.json` describes one undirected performer pair. The two IDs in `pair` must be distinct and lexicographically sorted.

- `fan_overlap` relations may use only fan-preference evidence classes 1–4.
- `style_similarity` relations must remain separately labeled and must never be presented as measured fan overlap.
- `support_evidence_ids` and `contradictory_evidence_ids` retain both sides of the evidence.
- `independent_fan_count` is nullable when the number of distinct fans cannot be established.
- `score` is nullable until a versioned scorer exists. `confidence` communicates evidence confidence, not a fabricated statistical probability.
- An `accepted` relation needs at least one supporting evidence ID, a score, a scorer version, and an explanation. Rejected or uncertain candidates stay inspectable without appearing as accepted graph edges.

An absent relation means “not established with current evidence,” not dissimilarity or dislike.

## Aggregation rules

Aggregation code, not individual agents, calculates final counts and scores from accepted evidence. Agents propose structured interpretations and explanations. Scoring must account for performer popularity and uneven evidence coverage, require minimum support, and retain its version in every accepted relation.
