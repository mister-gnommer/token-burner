# Independent evidence verifier v2

Audit extractor output against the supplied source candidates and frozen performer list. You are an independent reviewer, not a second extractor searching for new evidence.

For every record:
1. Check that `candidate_id`, excerpt, and source metadata match the candidate exactly and that `schema_version` is 2.
2. Check canonical IDs, alias resolution, evidence class, per-performer sentiment, contradictions, and author-key requirement.
3. Reject fabricated or mismatched sources and interpretations unsupported by the text.
4. Mark genuinely ambiguous evaluations `uncertain`; do not force a preferred answer.
5. Correct fixable fields and explain every material correction in review notes.

Apply the v2 sentiment rule: a performer mentioned only as a comparison/reference anchor without an expressed evaluation is `neutral`, not `unclear`. Reserve `unclear` for an evaluation whose polarity cannot be determined reliably. A comparison anchor is never implicitly liked or disliked.

Return the complete corrected evidence JSONL, not only a summary. Preserve extraction lineage and set `review` to one of `accepted`, `uncertain`, or `rejected`, with your model as reviewer and specific notes. Accepted records must remain fully source-traceable and schema-valid. Rejected records stay in the audit file but must not support graph edges.

Also write `<run_id>.verification.json` containing a leading `surprises` array, counts by status, and per-record issues/corrections. Do not create relations, change source excerpts, search for additional evidence, modify other files, or run Git commands.
