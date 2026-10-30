# Evidence extractor v2

Interpret supplied source candidates into `evidence-v2.schema.json` records. Do not search for new evidence, infer missing facts, or calculate graph edges.

## Inputs
- `run_id`, source-candidate JSONL, output paths, and `data/standupers.json`.
- Worker provider/model and prompt version from the run manifest.

## Entity resolution
Resolve Polish inflections, diminutives, aliases, and stage personas to canonical performer IDs using the frozen list. Examples: `Pacześ/Paczesia/Paczes` → `rafal-paczes`; `Lotek` → `lukasz-lotek-lodkowski`; `Mieszka Minkiewicza/Minkiewicz` → `mieszko-minkiewicz`. These are examples, not permission to guess: use `performer_id: null` when resolution is uncertain and retain the exact `surface_form`.

## Interpretation rubric
Assign sentiment independently to each mentioned performer:
- `positive`: explicit appreciation, enjoyment, or a sincere recommendation;
- `negative`: explicit dislike or criticism;
- `mixed`: meaningful appreciation and criticism of the same performer;
- `neutral`: mentioned without an expressed evaluation, including a performer used only as a comparison/reference anchor;
- `unclear`: an evaluation is present but sarcasm, negation, reference, or context makes its polarity unreliable.

Do not turn agreement with another comment, laughter at a clip, popularity, or familiarity into fandom without textual support. Do not hide contradictions or one-sided praise. A comparison anchor is not implicitly liked or disliked.

Choose one evidence class:
- `same_user_rating_overlap`: structured ratings by one source-scoped user covering at least two performers;
- `same_user_coendorsement`: one person explicitly appreciates at least two performers, including explicit liking with caveats;
- `fan_recommendation`: a fan recommends A in relation to B;
- `fan_comparison`: a fan compares/contrasts performers, including negative or one-sided comparisons;
- `style_similarity`: humor/style similarity that is not evidence of fan overlap.

Same-user overlap/co-endorsement requires at least two mentions and a non-null author key. Mere co-occurrence is never enough.

## Output
For every usable candidate, emit exactly one JSON object on one line conforming to `data/schemas/evidence-v2.schema.json`. Set `schema_version` to 2 and copy the source candidate’s `candidate_id` unchanged for direct lineage. Preserve source metadata and the exact excerpt. Use the candidate’s pseudonymous author key. Set `review` to `{ "status": "unreviewed", "reviewer": null, "notes": "" }` and `extraction.prompt_version` to `extract-evidence-v2`. Use calibrated, record-specific confidence values rather than copying one score everywhere.

Write rejected/skipped candidates to `extraction-skips.json` with candidate IDs, concrete reasons, and a leading `surprises` array. Do not silently drop records. Output JSON/JSONL only—no Markdown fences—and do not modify other files or run Git commands.
