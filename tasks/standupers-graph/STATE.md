# Current state

Last updated: 2026-10-25
Current stage: 2 — Ranking and data contract (complete)
Next stage: 3 — Worker framework (not started)

## Established with the user
- Target: 100 individual stand-uppers, processed in batches of 10.
- Node source: standup.pl’s current all-time popularity catalog, filtered to exclude groups/channels/formats before selection; 30-day trend is optional metadata.
- Purpose: discover similar performers and humor through fan preferences.
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

## Decisions from source audits
- Standupedia’s ranking is YouTube view-minutes data dated 2023-09-07; its aggregate ratings cannot supply pairwise fan overlap.
- Proceed toward an evidence-based fan-relation graph, not a claim of representative collaborative filtering.
- Use cited public co-endorsements and fan comparisons as confirmed primary evidence; aggregate ratings are node context only.
- Filmweb, Reddit, and YouTube remain unconfirmed evidence-source adapters.
- Standup.pl provides a fresh 448-person catalog, daily YouTube trend rankings, and an all-time popularity sort; its cumulative-view metric differs from Standupedia’s formula.

## Latest milestone
Stage 2 has been committed as one consolidated checkpoint: acquisition/finalization code, 135-candidate snapshot, audited entity decisions, frozen 100-person list, schemas, report, and this state. See Git history for the commit ID. No performer batch has started.

## Open questions / risks
- The frozen ranking preserves source order rather than copying a separate 30-day trend metric; popularity is node context, never relation evidence.
- Entity review is complete, including persona and hosted-format edge cases, but broader entertainers are included only when their profiles document stand-up work.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested.
- Worker prompts/models, scoring formula, and renderer remain decisions for their respective stages.

## Proposed next action
Run only Stage 3: prepare and test low-tier worker prompts, a Polish-aware extraction rubric, validation, run manifests, and storage conventions on a tiny sample without launching a performer batch.
