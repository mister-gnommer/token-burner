# Worker framework

## Roles and models
- Collector: `collect-fan-evidence-v2.md` finds cited source candidates with complete evaluation context and proposes validated aliases for orchestration to merge.
- Extractor: `extract-evidence-v2.md` performs Polish-aware entity/sentiment/class extraction with direct candidate lineage.
- Verifier: `verify-evidence-v2.md` independently audits the complete extraction.

The initial calibration used `opencode/big-pickle` for extraction/first verification and `claude-haiku-5-5` for secondary verification. Discover available low-tier models before each new run; these are historical IDs, not guaranteed defaults. Prefer different models for extraction and verification. Run the verifier as a separate task with the source candidates, not merely the extractor’s conclusions. The main agent checks source context and adjudicates disagreements. Same-model verification is weaker independence. Record any escalation and its reason in the run manifest.

Prompt files are immutable once used. Create a new versioned file for material changes; never silently alter a prompt referenced by an earlier run.

## Run storage
Use `calibration` for framework tests and `batch-01` … `batch-10` only for explicitly commanded performer batches:

- `evidence/<scope>/source-candidates.jsonl`
- `evidence/<scope>/evidence.unreviewed.jsonl`
- `evidence/<scope>/extraction-skips.json`
- `evidence/<scope>/evidence.jsonl` — verifier-reviewed records
- `reports/runs/<run_id>.json` — manifest and lifecycle
- `reports/runs/<run_id>.verification.json` — verifier audit

Lifecycle: `prepared → collecting → extracting → verifying → validated → completed`. Use `blocked` or `failed` with notes when appropriate. Calibration never feeds graph relations.

A completed run can expose failures that leave its stage unfinished. The initial calibration ended with one accepted and two uncertain records after source-context checks; see `reports/runs/20261030-stage03-calibration.adjudication.json`. The v2 extractor/verifier prompts still need a complete-context calibration. Version-1 extractor and worker-review artifacts remain unchanged; final `evidence.jsonl` was migrated to v2 by the parent audit without relabeling its original extraction prompt.

## Fan keys
Collectors may preserve a source-local public `author_hint` in source-candidate records. Final evidence contains only `author_key`, computed by `scripts/evidence_pipeline.py author-key` as `fan_` plus the first 16 hex characters of SHA-256 for `<lowercase-site>:<casefolded-author-hint>`. This is pseudonymization for same-source deduplication, not anonymity or permission to link identities across sites.

## Validation
Run `scripts/evidence_pipeline.py validate --kind <source-candidate|evidence|evidence-v1|relation|run-manifest> <path>` after each worker step. Use `evidence-v1` only for the initial calibration artifacts. JSONL is validated record by record with line-specific errors. The validator also checks canonical performer IDs, duplicate IDs, relation-pair ordering, and accepted-evidence reviewer presence.

Schema validation does not establish that an excerpt includes all relevant context or matches its candidate. Audit both separately. Run the validator regression checks with `PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tasks/standupers-graph/scripts -p 'test_*.py' -v` from the repository root.
