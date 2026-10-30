# Fan evidence collector v2

Collect public fan statements linking assigned performers to the frozen 100. Inputs: run ID, performer scope, source limit, canonical list, output path, and worker model metadata. Do not interpret sentiment or calculate relations.

## Sources
Find explicit same-user appreciation, recommendations, comparisons, or publicly accessible structured ratings. Search Polish aliases and inflections. Prefer different fans and sources over repeated comments from one thread. Respect source access rules; do not bypass authentication or anti-bot controls.

## Context check
Read the entire author post before choosing an excerpt. Preserve a contiguous passage containing every evaluation of the relevant performers in that post, including caveats and criticism before or after praise. Include the whole post when needed. Never select a flattering sentence while dropping nearby criticism, or treat a comparison anchor as unevaluated when its author evaluates it elsewhere in the post.

Keep other authors' replies separate. If a reply depends on its parent and cannot be interpreted from the candidate alone, report the missing context rather than guessing. Record the post number or direct post link in your report for attribution checks.

## Output
Write JSONL conforming to `data/schemas/source-candidate.schema.json`, with exact excerpts, source URL, per-post publication date, retrieval time, language, source-local public author hint, and collector metadata. Use null for unknown dates and `author_key`; orchestration computes the key. Preserve spelling and diacritics exactly.

Reject unverified search snippets, editorial/promotional text, context-free fragments, duplicate evidence, and mere co-mentions. Propose only source-validated aliases; never link fan identities across sites.

Return `Surprises` first, then source counts, post locators, skipped-source reasons, and coverage gaps. Return early with partial output if the premise fails, scope expands materially, or continuation risks irreversible action. Ignore out-of-scope trivia. Modify only the assigned output and do not run Git commands.
