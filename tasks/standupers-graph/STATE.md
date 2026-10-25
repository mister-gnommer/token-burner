# Current state

Last updated: 2026-10-25
Current stage: 1 — Source audit and fresh-ranking follow-up (complete)
Next stage: 2 — Ranking and data contract (not started)

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

## Decisions from source audits
- Standupedia’s ranking is YouTube view-minutes data dated 2023-09-07; its aggregate ratings cannot supply pairwise fan overlap.
- Proceed toward an evidence-based fan-relation graph, not a claim of representative collaborative filtering.
- Use cited public co-endorsements and fan comparisons as confirmed primary evidence; aggregate ratings are node context only.
- Filmweb, Reddit, and YouTube remain unconfirmed evidence-source adapters.
- Standup.pl provides a fresh 448-person catalog, daily YouTube trend rankings, and an all-time popularity sort; its cumulative-view metric differs from Standupedia’s formula.

## Current milestone
The initial framework, source audits, confirmed ranking basis, and repository Git policy form one consolidated checkpoint commit. No ranking has been frozen and no performer batch has started.

## Open questions / risks
- Standup.pl includes non-individual catalog entries that need documented filtering.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested.
- The scoring formula, worker model, and renderer remain decisions for their respective stages.

## Proposed next action
Run only Stage 2: freeze the confirmed current top 100 and define source-scoped evidence/relation schemas supporting citations, contradictory judgments, sparse coverage, and future source adapters.
