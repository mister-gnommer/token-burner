# Current state

Last updated: 2026-11-03
Current stage: 7 — Batch 7 complete; ranks55–57 remain incomplete
Next stage: pause for user command; batch8 ranks71–80 or explicitly budgeted earlier catch-up

## Established with the user
- Target: 100 individual stand-uppers, processed in batches of 10.
- Node source: standup.pl’s current all-time popularity catalog, filtered to exclude groups/channels/formats before selection; 30-day trend is optional metadata.
- Purpose: discover similar performers and humor through fan preferences.
- Renderer: D2, with editable `.d2` sources and SVG snapshots (confirmed 2026-10-30).
- Nodes use available profile photos, with a laughing-person silhouette for missing/unavailable images; cache assets locally and embed them in SVG.
- A future interactive HTML view can reuse saved graph JSON and cited evidence as a separate presentation stage, without repeating research/extraction.
- The project should be substantially AI-driven, with low-tier subagents doing the main work.
- User reaffirmed on 2026-10-31: real batches must distribute research across multiple low-tier collectors, with separate low-tier extraction and verification; main-agent work is orchestration, integration, spot-checks and exceptions. Stage 6 involved substantial main-agent framework implementation and a full final audit; that is not the intended routine batch workflow.
- User doubled research allowance on 2026-10-31: from batch5 retain three low-tier collectors, each with24 queries/24 page attempts/up to16 verified candidates (previous12/12/8). Apply research-budget-v1 supplement and matching provenance. Spend added capacity on broader sources, browser verification and identity checks; evidence thresholds and separate extraction/verification stay unchanged.
- Main-agent work is limited to 10 minutes per turn, excluding subagent execution; planning and discovery must be split into visible stages.
- Each new batch requires an explicit user command.
- State must survive changes of conversation and provider.
- Git commands are authorized without per-command confirmation in this repository only; commits follow coherent milestone boundaries rather than individual edits.
- `standupers-human-input.md` is read-only except for an explicitly requested writing correction.

## Completed
- Interactive view (2026-10-31, user-requested): each graph build now also writes self-contained `interactive.html` (d3-force bubbles, draggable, evidence panel); `graph/batch-07/interactive.html` rendered from the saved snapshot. See `graph/README.md`.
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
- Hosting added 2026-11-03: GitHub Pages workflow publishes the newest `graph/batch-NN/view.html` at https://mister-gnommer.github.io/token-burner/standupers/. batch-06/07 views now use relative paths, CSS fallbacks and a phone-friendly zoom. It goes live after merging to `main` and setting Settings → Pages → Source to "GitHub Actions". Future batch views must keep relative links.
- Batch7 complete2026-10-31:7canonical candidates/3accepted representations/4solo skips; cumulative38records/48relations (8corroborated,25provisional,15contested). New one-fan Pałubski–Poczęty and Zalewski–Borkowski links. Diagram8solid/11dashed,71photos. Actual61queries/21pageattempts;B exceeded24query cap by4. All20tests and strict lineage/recomputedgraph pass.67completed/33pending;earlier55–57 still incomplete. See reports/20261031-batch-07.md.
- Batch6 recovered snapshot saved2026-10-31:5canonical candidates,2independently accepted representations,3solo skips; cumulative35records/46relations (8accepted,23provisional,15contested). New one-fan Jurkiewicz–Pańczyk link is in data but hidden by degree cap. Graph shows8solid/9dashed,61photos. Ranks55–57 research incomplete and remain pending;57completed/43pending. All20tests and strict lineage/recomputed graph pass. See reports/20261031-batch-06.md.
- Batch5 complete (2026-10-31):7 candidates/7 reviewed (6accepted,1uncertain); cumulative33 records,45 relations:8 accepted,22 provisional,15 contested/opposing-only. Two new accepted pairs (Jurkiewicz–Syrek-Dąbrowski and Jurkiewicz–Szumowski), none downgraded. Graph displays8 solid/9 dashed with51photos. Six Luna workers plus one targeted middle-tier Terra audit; see reports/20261031-batch-05.md.
- Batch4 complete (2026-10-31):2 verified candidates/2 independently accepted representations; cumulative26 records,37 relation candidates:6 accepted,19 provisional,12 contested/opposing-only. Four provisional pairs added; accepted pairs unchanged. Graph displays6 solid/12 dashed links with42 photos. Six low-tier workers handled collection, extraction, verification and integration; parent quarantined snippet-only leads, routed actual-source browser checks and final-audited counts. See reports/20261031-batch-04.md.
- Batch3 complete (2026-10-31): five raw/four canonical/four independently accepted representations; cumulative24 records and33 relation candidates:6 accepted,15 provisional,12 contested/opposing-only. Graph displays6 solid/9 dashed links with33 photos. Giza–Ruciński added (historical joint-improv scope); Giza–Pacześ downgraded after opposing evidence. Six low-tier workers handled collection, extraction, verification and artifact integration; parent routed exceptions and final checks. See reports/20261031-batch-03.md.
- Batch2 complete (2026-10-31): four new candidates/four independently accepted representations; cumulative six accepted pairs, 15 provisional candidates and eight contested/opposing-only. Graph displays six solid/eight dashed links and 24 photos. Three low-tier collectors plus separate low-tier extraction and verification performed the substantive work; parent integrated and handled reported exceptions. See reports/20261031-batch-02.md.
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
Batch7 graph/report saved;pause for explicit user command before batch8(ranks71–80). Earlier ranks55–57 remain incomplete and pending;no catch-up or renewed budget was implied. Current67completed/33pending. No active workers. Exact task IDs/options,usage and interventions:reports/runs/20261031-batch07.execution.json.

Three sequential Luna collectors plus separate extraction,scoped correction and independent verifier performed semantic work.7canonical candidates→3accepted representations+4solo skips. Initial extractor wrongly skipped recommendation/omitted skip reason;corrected with initial artifacts retained. Verifier lowered tentative Cezarytypo confidence to0.72. Parent labeled a C002note clarification after verifier contradicted unchanged positive event-scoped fields/accepted decision;initial reviewed file retained. No code/schema/scorer edits or main-agent source research.

61queries/21pageattempts (A15/5,B28/10,C18/6);B exceeded per-worker24query cap by4 and stopped. A access failures left0verified candidates;C used preview_evaluate successfully and recovered stale-pagination source on event-specific page. Recommendations remain unscored;event praise retains scope.38records/48relations:8corroborated,25provisional,15contested;19drawnlinks,71photos,14eligible provisional links hidden by degreecap.20tests,strict loading/lineage/quotes/counts/skip accounting/recomputedgraph pass. Original slices and initial outputs retained. User authorized commit and push on2026-10-31. Checkpoint scope:completed batches2–7,reviewed evidence,graphs,recovery provenance,prompts,rules and compact renderer labels. Precommit validation:20tests pass;all6saved batchgraphs reproduce exactly;schemas/strict lineage/JSON checks pass;frozen identities unchanged except completion statuses. Ranks55–57 remain pending.
