# Source-first checkpoint integration — partial

## Surprises

- Parent brief formatting error: the reviewer was given a concatenated, nonexistent manifest filename. The real manifest at `reports/runs/20261031-coverage-source-first-01.json` exists and passes run-manifest schema validation.
- The reviewer accepted both records but did not run automated JSON Schema validation. My required `evidence_pipeline.py` validation fails on reviewed record `ev_csf01a_001`: the unresolved `Abelarda` mention has `sentiment: "unknown"`, which `evidence-v3.schema.json` rejects. I left the reviewed evidence and original review report untouched.

## Checks completed

- Canonical source candidates: 2; schema validation passed.
- Unreviewed evidence: 2; schema validation passed.
- Reviewed evidence: 2 records parsed; schema validation failed on line 1 at `mentions/0/sentiment` (`unknown` is outside the schema enum).
- Actual manifest: schema validation passed.
- Both candidate IDs (`src_csf01a_001`, `src_csf01a_002`) occur exactly once in both evidence files; no skips.
- Canonical source fields, excerpts, languages, contexts, literal mention surfaces and preference quotes match. Source author hashes rederive correctly. Actual run ID and extractor provider/model/prompt match the manifest. Both reviewed records have accepted status and reviewer `codex/gpt-6-luna`.
- `Abelarda` remains unresolved (`performer_id: null`, unknown preference, null preference quote).

## Integration status

Stopped before finalizing manifest counts/status or loading/rendering a graph, as required when a check fails. The manifest remains `verifying`; no graph artifacts or metrics were produced. The reviewer did not validate the schema, and this report does not attribute that validation to them.

Slice B remains empty: public rating probes on Filmweb, Letterboxd, and IMDb yielded no verified history. That is an access/provenance limitation, not evidence of absence. Disclosed posthoc reservations remain recorded in the manifest notes. No snippet, aggregate rating, or parent-author preference was promoted to evidence.

See `20261031-coverage-source-first-01.integration.json` for the exact commands and results.
