# Stage 3 — worker framework checkpoint

Date: 2026-10-30. Framework saved; complete-context calibration remains before Stage 4. No performer batch started.

## Surprises
- Two source excerpts were verbatim but incomplete. In forum post 16, later paragraphs qualify praise of Pacześ with criticism; post 6 expresses liking and criticism of Pacześ before the selected Minkiewicz comparison. Both records are now uncertain.
- Both prior verifiers checked supplied excerpts rather than whole posts. Agreement did not detect the collection failure.
- Provider interruptions left `STATE.md` and the run manifest stale, and final records still used schema v1 despite the new lineage contract.

## Saved work
- Collector, extractor, and verifier prompts; source-candidate, evidence-v2, and run-manifest schemas; pinned `jsonschema==4.23.0`; validation and source-scoped fan-key utilities.
- Original low-tier extractor output, same-model verification, and independent Haiku verification remain preserved. The parent audit migrated final records to v2 with `candidate_id` while retaining `extract-evidence-v1` as actual extraction provenance.
- Four calibration performers have seeded aliases. Other aliases need source validation during assigned collection.
- Fixed malformed-record validation: structural errors are reported before semantic access, preventing crashes on missing fields and non-object JSON. Added four standard-library regression tests for invalid shapes, duplicate IDs, unknown performers, and source-scoped keys.

## Adjudication
The rubric defines an unevaluated comparison anchor as `neutral`; `unclear` requires an ambiguous evaluation. That resolves the original label disagreement but cannot excuse missing context. Final counts: **1 accepted, 2 uncertain, 0 rejected**. All calibration remains excluded from graph input.

The parent reopened the [source thread](https://www.gry-online.pl/forum/quotkabareciarzequot-please-stand-up/zff63169), checked authors and per-post dates, and confirmed the third excerpt's original ASCII spelling. The differing Minkiewicz comparisons concern subjective assessments and programmes; they do not establish fan overlap, similarity, or dissimilarity. Details are in `runs/20261030-stage03-calibration.adjudication.json`.

Collection prompt v2 now requires reading the entire author post and preserving all evaluation context for the relevant performers. The initial calibration run is complete with its audit outcome; Stage 3 remains in progress because the v2 extraction/verifier prompts have not been run on complete context.

## Checks and limits
Four regression tests pass. All saved schemas pass Draft 2020-12 checks; source candidates, v1 extraction/review artifacts, final v2 evidence, and the run manifest validate. Final candidate IDs, excerpts, source metadata, author keys, counts, and pending performer statuses were checked together.

This tiny single-thread sample does not establish collection yield, source diversity, uncertain-alias handling, or production readiness. Schema validation alone does not verify excerpt completeness or cross-file lineage.

## Next slice
Create a separate complete-context calibration run for the same three posts. Discover available low-tier models, run v2 extraction and independent verification, then audit before marking Stage 3 complete. Do not launch a batch or begin scoring/rendering yet.
