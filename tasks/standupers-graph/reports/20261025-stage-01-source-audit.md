# Stage 1 — Source audit

Date: 2026-10-25
Status: complete

Node-source note: the original Standupedia recommendation below was superseded by the user-approved switch to standup.pl documented in `20261025-stage-01b-fresh-ranking-search.md`. The fan-evidence findings still apply.

## Surprises

- The requested ranking is a YouTube popularity ranking dated 2023-09-07, not a rating or fan-similarity ranking.
- Standupedia shows aggregate performer ratings, but the inspected public pages do not expose who voted or which performers each voter also rated.
- Public discussions contain exactly the kind of nuanced evidence AI should handle: co-endorsements, one-sided praise, changing opinions, contrasts, and style comparisons.

## Scope

Read-only inspection of Standupedia and a bounded scan of candidate external sources. No ranking freeze, performer batch, subagent swarm, credential use, or graph generation.

## Standupedia findings

### Ranking acquisition: good

The [performer ranking](https://standupedia.pl/najlepsi-standuperzy/) is publicly readable and contains 136 ranked performers, including names, profile links, video counts, minutes, views, points, and aggregate ratings. The requested first 100 are present.

Its published formula is `recording duration × YouTube views / 1,000,000`, summed over eligible recordings. The page says its data is current as of **2023-09-07**; the [update article](https://standupedia.pl/aktualizacja-rankingu-standuperow-i-rankingu-nagran-wrzesien-2023/) confirms that release. This date and the fact that the ranking measures view-weighted popularity must travel with the frozen dataset.

The site’s `robots.txt` does not disallow these public ranking pages. No access controls were bypassed.

### Fan-overlap data: not found on Standupedia

- Performer rows expose a 1–10 average and vote count. The page loads the GD Rating System plugin, but the inspected public markup contains rating item IDs and aggregates—not voter identities or per-voter histories.
- The [2022 audience-rating article](https://standupedia.pl/najlepsi-stand-uperzy-w-ocenie-publicznosci/) summarizes KupBilecik live-show ratings. It provides averages and counts for leading performers, not same-user ratings across performers; its live-audience and coverage limitations also differ from the YouTube ranking.
- [Standupedia’s surveys](https://standupedia.pl/ankiety/) mostly concern isolated preferences or aggregate poll choices. They do not provide a reusable fan-by-performer preference matrix.

Standupedia can therefore supply canonical nodes and useful context, but not the requested “fans of A also like B” relations by itself. Aggregate averages must not be turned into pairwise edges.

## External evidence scan

### Confirmed usable: public discussion threads

The [Gry-Online stand-up thread](https://www.gry-online.pl/forum/quotkabareciarzequot-please-stand-up/zff63169) is directly readable and has user-attributed posts with several performers discussed in context. Examples include an explicit “lubię Paczesia, Sochę i Lotka” and another user praising both Lotek and Pacześ. Other posts contrast performers or praise one while criticizing another.

This validates the need for AI extraction rather than name co-occurrence: the same thread also contains irony, negation, changing assessments, and comparisons of style. It supplies real co-endorsement and comparison evidence, but not a representative sample of all fans.

### Candidates requiring later validation

- **Reddit:** search finds relevant recommendation threads, including [Rekomendacje stand-upów](https://www.reddit.com/r/Polska/comments/105mykf/stand_up_rekomendacje/), with multi-performer recommendation snippets. Direct fetching returned no content in this audit, so acquisition remains unresolved.
- **Filmweb:** its [stand-up rankings](https://www.filmweb.pl/ranking/tvshow/genre/17/2025), performer pages, ratings, and reviews are readable. Public user rating histories appear to exist as a feature, but their accessibility and coverage for these 100 performers were not validated. This is a possible structured source, not yet a confirmed one.
- **YouTube:** Standupedia recording pages expose YouTube video IDs through embeds. Comment access was not tested. Even if available, commenting is not fandom; AI sentiment and same-commenter overlap would be necessary, with strong sampling caveats.

Do not link identities across platforms. Same-person evidence should remain source-scoped unless an explicit, reliable public identity link exists.

## Feasibility decision

**Conditional go for an evidence-based fan-relation graph; no-go for claiming statistically representative collaborative filtering from the confirmed data.**

Recommended approach:

1. Use the dated Standupedia ranking only to define the 100 nodes and initial metadata.
2. Make cited, same-person public co-endorsements and fan comparisons the confirmed primary relation evidence.
3. Keep aggregate ratings as optional node context, never as pairwise evidence.
4. Test Filmweb and YouTube later as separate source adapters; do not delay the ranking schema on unconfirmed sources.
5. Represent sparse support and uncertainty explicitly. Lower-ranked performers may remain isolated, and no edge must never be interpreted as dissimilarity.
6. Record source and coverage biases: publicly commenting fans are not all fans, search results are uneven, and performer popularity affects discoverability.

This preserves the discovery goal without pretending that sparse web evidence is a complete music-platform-style preference dataset.

## Sources inspected

- https://standupedia.pl/najlepsi-standuperzy/
- https://standupedia.pl/ranking-standup/
- https://standupedia.pl/aktualizacja-rankingu-standuperow-i-rankingu-nagran-wrzesien-2023/
- https://standupedia.pl/najlepsi-stand-uperzy-w-ocenie-publicznosci/
- https://standupedia.pl/ankiety/
- https://standupedia.pl/robots.txt
- https://standupedia.pl/rafal-paczes-puder-do-cery-zimnej/
- https://www.gry-online.pl/forum/quotkabareciarzequot-please-stand-up/zff63169
- https://www.reddit.com/r/Polska/comments/105mykf/stand_up_rekomendacje/
- https://www.filmweb.pl/ranking/tvshow/genre/17/2025

## Next step

Stage 2: freeze the dated top-100 ranking and define a source-scoped evidence/relation contract that supports sparse cited judgments, contradictory evidence, and later source adapters.
