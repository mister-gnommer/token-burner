# Stage 3 — complete-context calibration

Date: 2026-10-30. Stage 3 complete; Stage 4 not started.

## Surprises and decisions
- Complete context changes two earlier readings: Pacześ is liked with criticism in both posts, rather than simply positive or an unevaluated anchor. Lotek and Giza remain neutral in post 6; popularity and lighter style do not establish liking.
- The independent verifier changed Minkiewicz from negative to mixed in record 003. Parent review marks that record uncertain: criticism concerns the latest programme, and saying earlier programmes were better does not clearly establish absolute praise. Both model readings remain preserved.
- Different style assessments and attempted imitation do not establish a factual similarity/dissimilarity edge. No graph relation was created.

## Completed
Three full author posts were recollected from the [source thread](https://www.gry-online.pl/forum/quotkabareciarzequot-please-stand-up/zff63169): posts 16, 6, and 6.1. The parent independently checked author attribution, publication dates, evaluation context, and the third post's original ASCII spelling. Replies from other authors are excluded.

Separate low-tier Codex `gpt-6-luna` workers collected and extracted the posts with v2 prompts; independent Claude `claude-haiku-5-5` verified them. All used medium effort. Task identities, actual options, and prompt hashes are saved in `runs/20261030-stage03-context-calibration.execution.json`; used prompts remain unchanged.

The verifier accepted three records. Final parent counts are **2 accepted, 1 uncertain, 0 rejected**, covering five canonical performers. `evidence.unreviewed.jsonl` preserves extraction, `evidence.haiku.jsonl` preserves verification, and `evidence.jsonl` contains the final review status. Original calibration artifacts are unchanged.

`prompts/extraction-decisions-v1.md` records mention deduplication, programme scope, relative praise, and pair-specific caveats for future briefs. It was written after this run and is not claimed as a worker input.

## Validation and limits
The existing four regression tests pass. New source candidates, all extraction/review variants, and the completed run manifest pass schema validation. Cross-file checks cover candidate/source equality, author keys, worker provenance, counts, prompt hashes, and all 100 performers remaining pending.

This tiny single-thread calibration exercises the worker/audit workflow, including abstention. It does not establish collection yield, source diversity, statistical confidence, unresolved-alias handling, or graph quality. All calibration is excluded from graph input.

## Next stage
Stage 4: design conservative aggregation and a renderer using clearly synthetic fixtures, including neutral mentions and qualified liking. Do not start a performer batch without an explicit command.
