# Current state

Last updated: 2026-10-30
Current stage: 3 — Worker framework (complete)
Next stage: 4 — Aggregation and graph framework (not started)

## Established with the user
- Target: 100 individual stand-uppers, processed in batches of 10.
- Node source: standup.pl’s current all-time popularity catalog, filtered to exclude groups/channels/formats before selection; 30-day trend is optional metadata.
- Purpose: discover similar performers and humor through fan preferences.
- Renderer: D2, with editable `.d2` sources and SVG snapshots (confirmed 2026-10-30).
- The project should be substantially AI-driven, with low-tier subagents doing the main work.
- Main-agent work is limited to 10 minutes per turn, excluding subagent execution; planning and discovery must be split into visible stages.
- Each new batch requires an explicit user command.
- State must survive changes of conversation and provider.
- Git commands are authorized without per-command confirmation in this repository only; commits follow coherent milestone boundaries rather than individual edits.
- `standupers-human-input.md` is read-only except for an explicitly requested writing correction.

## Completed
- Stage 0: created `AGENTS.md`, `PLAN.md`, and this checkpoint.
- Stage 1: saved `reports/20261025-stage-01-source-audit.md`.
- Fresh-ranking follow-up: saved `reports/20261025-stage-01b-fresh-ranking-search.md`; the user confirmed option A.
- Repository governance: added root `AGENTS.md` with repo-local Git permission and commit policy.
- Initial checkpoint: commit `e0b2c9a` pushed to `origin/main`.
- Stage 2: froze 100 individual performers and created the data contract; see `reports/20261025-stage-02-ranking-and-schema.md`.
- Stage 3: saved and calibrated versioned collection/extraction/verification prompts, schemas, validation, and manifests; see `reports/20261030-stage-03b-context-calibration.md`.

## Decisions from source audits
- Standupedia’s ranking is YouTube view-minutes data dated 2023-09-07; its aggregate ratings cannot supply pairwise fan overlap.
- Proceed toward an evidence-based fan-relation graph, not a claim of representative collaborative filtering.
- Use cited public co-endorsements and fan comparisons as confirmed primary evidence; aggregate ratings are node context only.
- Filmweb, Reddit, and YouTube remain unconfirmed evidence-source adapters.
- Standup.pl provides a fresh 448-person catalog, daily YouTube trend rankings, and an all-time popularity sort; its cumulative-view metric differs from Standupedia’s formula.

## Latest checkpoint
- Complete-context calibration used separate low-tier Codex gpt-6-luna collector/extractor workers and an independent Claude Haiku 5.5 verifier (all medium effort). Parent audited the source posts.
- Final counts: 2 accepted, 1 uncertain, 0 rejected. Record 003's programme-scoped negative/mixed ambiguity is retained as uncertainty. Original extraction, verification, and earlier calibration remain preserved.
- Future briefs must include `prompts/extraction-decisions-v1.md`: one mention per performer, programme-scope notes, no absolute praise inferred from relative improvement, and pair-specific handling of mixed/neutral mentions.
- Existing tests and schema/lineage checks pass. Execution IDs/options and immutable prompt hashes are saved under `reports/runs/20261030-stage03-context-calibration.*`.
- No performer batch has started. All calibration is excluded from graph input.

## Open questions / risks
- The frozen ranking preserves source order rather than copying a separate 30-day trend metric; popularity is node context, never relation evidence.
- Entity review is complete, including persona and hosted-format edge cases, but broader entertainers are included only when their profiles document stand-up work.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested.
- Discover live low-tier model IDs before future collection. Scoring and rendering remain Stage 4 work.
- Three posts from one thread do not establish source yield or diversity. Unresolved aliases and rejected-record cases remain untested in real-source calibration; model confidence is not measured probability.
- Schema checks do not prove source-context completeness or candidate equality; these require a separate audit.

## Proposed next action
Run Stage 4 only: choose conservative aggregation, then implement and test it with D2 rendering and clearly synthetic fixtures. Test that neutral mentions, uncertain evidence, repeated names, and calibration records cannot create unsupported fan edges. Do not start a performer batch.
