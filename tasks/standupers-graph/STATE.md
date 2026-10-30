# Current state

Last updated: 2026-10-30
Current stage: 3 — Worker framework (framework saved; context calibration still required)
Next slice: complete-context calibration with low-tier extraction and independent verification

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

## Latest checkpoint
- Stage 3 framework: source/evidence-v2/run schemas, versioned worker prompts, validator, pinned dependency, and four regression tests are saved.
- Initial low-tier extraction and both verification passes finished before provider failures. Preserved their original artifacts; final evidence now has candidate IDs and honest extraction lineage.
- Parent source-page audit found omitted evaluation context in two excerpts: final counts are 1 accepted, 2 uncertain, 0 rejected. Collection v2 now requires complete evaluation context.
- The initial run manifest is completed with corrected counts. Stage 3 remains unfinished: v2 extraction/verification prompts have not been calibrated on complete context.
- See `reports/20261030-stage-03-worker-framework.md` and `reports/runs/20261030-stage03-calibration.adjudication.json`. No performer batch has started. Calibration never feeds the graph.

## Open questions / risks
- The frozen ranking preserves source order rather than copying a separate 30-day trend metric; popularity is node context, never relation evidence.
- Entity review is complete, including persona and hosted-format edge cases, but broader entertainers are included only when their profiles document stand-up work.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested.
- Discover live low-tier model IDs for the next calibration; the prior model IDs are historical. Scoring and rendering remain Stage 4 work.
- Schema checks do not prove source-context completeness or candidate equality; these require a separate audit.

## Proposed next action
Finish Stage 3 only: recollect the three calibration posts with complete evaluation context into a new run, then use the v2 extraction/verifier prompts with low-tier workers and audit their output. Preserve the initial run. Do not start Stage 4 or a performer batch yet.
