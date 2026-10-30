# Standupers graph — working plan

## Intended result
A weighted graph of 100 individual comedians frozen from standup.pl’s current all-time popularity catalog, designed for discovering similar humor. The primary edges represent evidence that fans who appreciate one performer also appreciate another. Each exposed edge has support, confidence, and a short explanation linked to sources.

The graph will be provisional while batches are incomplete. An absent edge means “not established with current evidence,” not “dissimilar.”

## AI-driven method

### 1. Establish what the web can actually support
The completed source audit checked Standupedia and fresher alternatives. The user subsequently selected standup.pl’s all-time popularity catalog for nodes. Continue auditing fan evidence across public Polish-language sources: structured same-user ratings/favorites, explicit co-endorsements, and fan recommendations/comparisons. Record access constraints and coverage, and never assume suitable fan-level data exists.

### 2. Freeze identities and evidence
Save the ranking once with rank, canonical name, profile URL, aliases, and retrieval date. Agents collect focused evidence per performer and store source URL, excerpt, source/retrieval dates, and extraction confidence. Collect pair-relevant fan evidence, not profiles of individual fans.

Evidence classes remain labeled:
1. Structured same-user preference overlap.
2. Explicit same-user co-endorsement in natural language.
3. Fan recommendation or comparison linking performers.
4. Performer/style/humor similarity, which is a separate fallback layer rather than fan-overlap proof.

Negation, sarcasm, one-sided praise, and negative comparisons must be interpreted and labeled. Mere co-occurrence is not positive evidence.

### 3. Let AI extract judgments, then aggregate consistently
Low-tier agents use one versioned Polish-aware rubric to identify performers, resolve aliases, classify sentiment toward each, and produce structured candidate relations. A second agent verifies ambiguous or high-impact cases and audits a sample of routine cases. The main agent calibrates the rubric using disagreements instead of manually inventing edges.

A shared, versioned scorer combines accepted evidence. Choose its formula after the source audit: structured preference data can support prevalence-normalized statistics, while sparse quotations require conservative evidence weights and visible support/confidence rather than fake statistical precision. Normalize for performer popularity and evidence coverage, require minimum support, and retain contradictory evidence.

### 4. Build and audit the graph incrementally
For each commanded batch, collect evidence for the next 10, compare them with all already processed performers, then rebuild affected relations from stored evidence. Save rejected and uncertain candidates separately so they remain inspectable without cluttering the graph.

Store graph data independently of its renderer. Use D2 for visual checkpoints, saving editable `.d2` sources and rendered SVG snapshots in `graph/`. Keep node IDs and generation order stable between updates, inspect layout changes, and visually encode support/confidence. Limit displayed edges for readability without deleting underlying data.

Show profile photos where available; use a local laughing-person silhouette for missing or unavailable images. Cache photos with source metadata and embed them in SVG snapshots so rendering failures do not depend on remote image availability.

### 5. Make the result useful for discovery
The final view should let the user inspect a performer’s closest relations and understand why each edge exists. Coverage and evidence limitations stay visible. If the available fan evidence cannot support the original goal, pause and ask whether to add a separately labeled humor/style-similarity layer.

## Stages

- **Stage 0 — Governance:** persistent rules, method, and handoff state.
- **Stage 1 — Source audit:** check ranking access and fan-preference evidence; report feasibility and implications. Do not launch a performer batch.
- **Stage 2 — Ranking and data contract:** freeze the selected standup.pl top 100 and define evidence/relation schemas from what Stage 1 found.
- **Stage 3 — Worker framework:** write prompts, rubric, validation, run manifests, and storage conventions; test them on a tiny sample without processing a batch.
- **Stage 4 — Graph framework:** implement and test aggregation plus D2 rendering with clearly synthetic fixtures.
- **Stage 5 — Pilot batch:** on command, process ranks 1–10, render the first graph, and audit quality/cost before scaling.
- **Stage 6 — Calibration:** resolve pilot failures and obtain user direction if the evidence or graph is not useful.
- **Stage 7 — Remaining batches:** process exactly 10 per commanded run, updating evidence, relations, graph, coverage, and report each time.
- **Stage 8 — Final audit:** check unsupported edges, missing performers, source quality, reproducibility, and final usability.

A stage may be split into smaller turns to respect the time budget. Do not silently reorder dependencies or combine discovery, full framework design, and a batch into one turn.

## Planned storage
Create only when needed:

- `data/` — frozen ranking and canonical performer records.
- `evidence/` — cited source extracts and structured AI judgments, organized by batch.
- `prompts/` — versioned worker prompts and rubrics.
- `relations/` — accepted, uncertain, and rejected candidate relations.
- `graph/` — renderer-independent data, editable D2 sources, and rendered SVG snapshots.
- `reports/` — batch/stage reports and run manifests.
- `STATE.md` — short current checkpoint and next action.
