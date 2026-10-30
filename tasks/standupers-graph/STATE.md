# Current state

Last updated: 2026-10-30
Current stage: 4 — Aggregation and graph framework (complete)
Next stage: 5 — Pilot batch, ranks 1–10 (requires explicit command)

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

- Stage 4: conservative aggregation, D2 rendering, synthetic fixture and 12 passing tests; see `reports/20261030-stage-04-graph-framework.md`.

## Decisions from source audits
- Standupedia’s ranking is YouTube view-minutes data dated 2023-09-07; its aggregate ratings cannot supply pairwise fan overlap.
- Proceed toward an evidence-based fan-relation graph, not a claim of representative collaborative filtering.
- Use cited public co-endorsements and fan comparisons as confirmed primary evidence; aggregate ratings are node context only.
- Filmweb, Reddit, and YouTube remain unconfirmed evidence-source adapters.
- Standup.pl provides a fresh 448-person catalog, daily YouTube trend rankings, and an all-time popularity sort; its cumulative-view metric differs from Standupedia’s formula.

## Latest checkpoint
- D2 renderer decision committed as `73904e1`.
- `scripts/graph_pipeline.py` validates completed batch/source/evidence lineage, excludes calibration, deduplicates source-scoped fans, and saves all relation candidates with support/contradictions and deferred records.
- `observed-coendorsement-v1`: two co-endorsing fans minimum, observed-union normalization, no opposing evidence for visible edges. Mixed/unclear/unresolved and low-confidence records are deferred; neutral mentions never create support.
- Editable D2, SVG with tooltips, PNG preview, and graph JSON are saved in `graph/synthetic-demo/`. These are fabricated fixtures, not fan findings. Installed D2/ELK rendering was visually checked; all 12 tests pass.
- No performer batch has started. All calibration remains excluded from graph input. See `graph/README.md` for scoring and rerun commands.

## Open questions / risks
- The frozen ranking preserves source order rather than copying a separate 30-day trend metric; popularity is node context, never relation evidence.
- Entity review is complete, including persona and hosted-format edge cases, but broader entertainers are included only when their profiles document stand-up work.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested.
- Discover live low-tier model IDs before future collection.
- Qualified liking is deferred by the first scorer until pair-specific appreciation can be represented safely; pilot yield may be sparse.
- D2 physical distance is schematic; edge weights convey evidence. Readability at 100 nodes remains untested.
- Three posts from one thread do not establish source yield or diversity. Unresolved aliases and rejected-record cases remain untested in real-source calibration; model confidence is not measured probability.
- Schema checks do not prove source-context completeness or candidate equality; these require a separate audit.

## Proposed next action
Wait for an explicit command to start Stage 5, the pilot batch of ranks 1–10. Collect and independently verify evidence, include `prompts/extraction-decisions-v1.md` in briefs, audit yield and deferred cases, then render and save the first real graph/report. Do not start another batch automatically.
