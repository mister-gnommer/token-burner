# Current state

Last updated: 2026-10-31
Current stage: 6 — Pilot calibration (complete)
Next stage: 7 — Batch 2, ranks 11–20, only on explicit command

## Established with the user
- Target: 100 individual stand-uppers, processed in batches of 10.
- Node source: standup.pl’s current all-time popularity catalog, filtered to exclude groups/channels/formats before selection; 30-day trend is optional metadata.
- Purpose: discover similar performers and humor through fan preferences.
- Renderer: D2, with editable `.d2` sources and SVG snapshots (confirmed 2026-10-30).
- Nodes use available profile photos, with a laughing-person silhouette for missing/unavailable images; cache assets locally and embed them in SVG.
- A future interactive HTML view can reuse saved graph JSON and cited evidence as a separate presentation stage, without repeating research/extraction.
- The project should be substantially AI-driven, with low-tier subagents doing the main work.
- User reaffirmed on 2026-10-31: real batches must distribute research across multiple low-tier collectors, with separate low-tier extraction and verification; main-agent work is orchestration, integration, spot-checks and exceptions. Stage 6 involved substantial main-agent framework implementation and a full final audit; that is not the intended routine batch workflow.
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

- Stage 5: pilot ranks 1–10 processed; graph/report saved. See `reports/20261030-stage-05-pilot-batch.md`.
- Stage 6: calibrated pilot extraction/scoring and provisional rendering; see `reports/20261031-stage-06-calibration.md`. User authorized committing and pushing this milestone on 2026-10-31.

## Decisions from source audits
- Standupedia’s ranking is YouTube view-minutes data dated 2023-09-07; its aggregate ratings cannot supply pairwise fan overlap.
- Proceed toward an evidence-based fan-relation graph, not a claim of representative collaborative filtering.
- Use cited public co-endorsements and fan comparisons as confirmed primary evidence; aggregate ratings are node context only.
- Public Filmweb/Reddit discussions supplied pilot evidence; structured rating history and YouTube acquisition remain untested.
- Standup.pl provides a fresh 448-person catalog, daily YouTube trend rankings, and an all-time popularity sort; its cumulative-view metric differs from Standupedia’s formula.

## Latest checkpoint
- Stage 6 complete (2026-10-31): graph/batch-01-calibrated has three solid and ten displayed provisional links, all 16 visible photos cached, 20 passing tests and an independent low-tier semantic check. The pilot-v1 details below are historical.
- Run `20261030-batch01-pilot` complete: 15 canonical candidates, 12 reviewed records (9 accepted, 3 uncertain), 3 documented skips. Original collector/extractor/verifier outputs remain preserved; parent source/semantic corrections are recorded.
- Three low-tier Codex gpt-6-luna collectors, separate extraction, and independent Claude Haiku verification used medium effort. Actual task IDs/options and prompt hashes are saved in the execution JSON.
- Unchanged observed-coendorsement-v1 produced 16 uncertain relation candidates and zero accepted edges: no direct pair had two qualifying fans. Seven reviewed records are deferred. See the pilot report for the representation/collection bottleneck.
- `graph/batch-01/` contains the first real JSON/D2/SVG/PNG snapshot and ten cached photos. JSON retains all 100 nodes; the diagram shows ten focal performers. No accepted edges are drawn; physical distance and missing edges do not imply similarity/dislike.
- Pilot and avatar enhancements form one validated checkpoint; the user explicitly authorized committing and pushing it. See Git history for the milestone commit.
- All 17 tests and source/evidence/manifest/lineage checks pass. First ten performer statuses are completed (searched/reviewed, not evidence of relations); the other 90 remain pending. Ranks 11–20 have not started.

## Open questions / risks
- The frozen ranking preserves source order rather than copying a separate 30-day trend metric; popularity is node context, never relation evidence.
- Entity review is complete, including persona and hosted-format edge cases, but broader entertainers are included only when their profiles document stand-up work.
- Public fan evidence will be sparse and uneven, especially for lower-ranked performers; a fully connected graph is not guaranteed.
- Filmweb user-rating history accessibility/coverage and YouTube comment acquisition remain untested. The pilot source sample spans seven pages/four platforms but remains small and query-biased.
- Discover live low-tier model IDs before future collection.
- Qualified liking is deferred by the first scorer until pair-specific appreciation can be represented safely; pilot yield may be sparse.
- D2 physical distance is schematic; edge weights convey evidence. Readability at 100 nodes remains untested.
- Model confidence is not measured probability. Alias uncertainty, parent-context representation, qualified opinions, and sparse repeated pair support reduced pilot yield.
- Schema checks do not prove source-context completeness or candidate equality; these require a separate audit.

## Proposed next action
Stage 6 completed with user authorization: v3 extraction separates personal preference and parent context, v2 scorer localizes ambiguous mentions, and dashed one-fan links are enabled. See reports/20261031-stage-06-calibration.md and graph/batch-01-calibrated/. Three accepted pairs, 17 provisional candidates, eight contested/opposing-only; diagram cap shows three solid plus ten dashed. Original pilot stays unchanged. Fifteen reliable representations and one rejected single-performer critique; 20 tests and strict lineage checks pass. Parent restored prior conservative identity confidence after extractor inflation. A separate low-tier semantic check confirmed accepted pairs; parent corrections are explicit.

Next: batch 2 (ranks 11–20) only on explicit user command, with multiple low-tier collectors and separate extraction/verification workers. The user authorized committing and pushing the completed calibration; no new collection has started. Source corpus remains small and targeted; supported edges are exploratory, not representative audience statistics.
