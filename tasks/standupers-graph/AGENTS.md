# Standupers graph — agent rules

## Mission
Create a useful, evidence-based discovery graph of 100 individual stand-uppers selected from standup.pl’s current all-time popularity catalog. Proximity should represent similar audience preferences and humor, not agent intuition or ranking position.

## Read first
At the start of a conversation, read `standupers-human-input.md`, `STATE.md`, and the relevant part of `PLAN.md`. Treat chat as transient: persist anything needed by another conversation or provider in this directory.

## Non-negotiables
- Never edit `standupers-human-input.md`, except to fix its writing when the user explicitly requests that.
- Do one bounded stage or slice per turn. Budget at most 10 minutes of main-agent work, excluding subagent execution time. Wrap up early enough to checkpoint within the limit; never chain a long discovery/planning marathon.
- After each turn, update `STATE.md` before reporting. Briefly tell the user what was done, decisions made, surprises, and the proposed next step. Ask when a finding changes the goal or approach.
- A batch contains 10 stand-uppers. Never start a batch without an explicit user command. Pause after its graph and report are saved.
- Use low-tier subagents for the main collection and extraction work. Main agents orchestrate and audit; escalate only work that demonstrably needs it, and record why.
- Real batches use multiple low-tier collectors, separate low-tier extraction, and separate low-tier verification. The main agent integrates outputs, spot-checks evidence, and resolves reported exceptions; do not routinely redo the workers' full semantic review. Report worker roles and main-agent interventions with each batch.
- From batch5, keep three low-tier collectors and double each collector's research allowance to24 queries/24 page-open or navigation attempts, with up to16 verified candidates. Apply `prompts/research-budget-v1.md`; extraction and independent verification remain separate.
- Before each batched search, enforce the remaining allowance with a code counter: count individual queries in the batch, not tool calls, and stop before exceeding the cap.
- Be AI-driven, not AI-vibes-driven: use AI for discovery, Polish-language interpretation, entity resolution, preference/sentiment extraction, and evidence-based relation explanations. Use code for repeatable aggregation and rendering.
- Every factual relation must trace to stored evidence. Never turn a mere co-mention into a co-preference, and never present missing evidence as dislike or dissimilarity.
- A web-cache miss does not prove a source is inaccessible. Within the worker budget, try the full result URL and T3 `preview_status` then `preview_open`; a closed preview reporting `available:false` still needs an open attempt. Never promote unverified search snippets.
- Keep fan-preference evidence distinct from performer/style similarity. Do not silently substitute one for the other if fan data is insufficient.
- Use D2 for graph rendering; save editable `.d2` sources alongside SVG snapshots.
- Each batch's `graph/batch-NN/view.html` is published by `.github/workflows/pages.yml` to https://mister-gnommer.github.io/token-burner/standupers/ (highest batch number wins). Use only relative links (`graph.svg`, `assets/…`), never local absolute paths; the build fails otherwise. Define fallback values for any CSS variables.
- Save schemas, prompts, model/provider details, source metadata, normalized outputs, and scorer versions so results are inspectable and resumable. Keep raw source excerpts and citations with their extracted claims.
- Prefer small, inspectable files over a monolithic log or a database until the data volume requires otherwise.

## Subagent briefs
Give each worker the relevant schema and rubric, exact scope, and output path. Require a leading `Surprises` section for invalidated assumptions, adjacent problems, and material edge cases. Tell workers to return early with partial work if the premise fails, the scope expands substantially, or continuation is risky. Ignore out-of-scope trivia.

## Git checkpoints
Follow the repository-root `AGENTS.md`. Expected milestones are the initial framework/source research, ranking and schema, worker framework, graph framework, one commit per completed batch, and final audit. Group small corrections into the current milestone rather than committing them separately.

## Definition of done for a stage
Outputs are saved, assumptions and failures are recorded, `STATE.md` identifies the completed and next steps, and the user receives a concise handoff. A stage is not done merely because an agent returned text in chat.
